package com.example.voiceassistant.data

import android.util.Base64
import android.util.Log
import com.example.voiceassistant.data.models.CodeBlock
import com.example.voiceassistant.viewmodel.AppLanguage
import java.io.IOException
import java.util.concurrent.TimeUnit
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject

const val GEMINI_API_KEY = "AQ.Ab8RN6JMgxW9_1H8CqZYKDmu8sDG2wHtH13ZmMqI-kgO-a7-Cw"
const val OPENAI_API_KEY = ""
const val CLAUDE_API_KEY = ""

// الترتيب = الأسرع والأكثر استقراراً أولاً. نماذج gemini-1.5 أُوقفت نهائياً من Google (تعطي model not found)،
// لذلك لا تضعها هنا. نماذج Flash-Lite هي الأسرع، و gemini-3.8-flash الأذكى كخيار احتياطي.
val GEMINI_MODELS = listOf(
    "gemini-2.5-flash-lite",    // الأسرع والأكثر استقراراً
    "gemini-3.1-flash-lite",    // سريع وحديث
    "gemini-3.8-flash",         // الأحدث والأقوى (أبطأ قليلاً)
    "gemini-2.5-flash"          // احتياطي أخير
)
const val IMAGE_MODEL = "gemini-2.5-flash-image"

private const val GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
private const val OPENAI_BASE = "https://api.openai.com/v1/chat/completions"
private const val CLAUDE_BASE = "https://api.anthropic.com/v1/messages"

private val RETRY_CODES = setOf(429, 500, 502, 503, 504)
private const val MAX_HISTORY_MESSAGES = 12
private const val TAG = "AiChat"

// أقصى زمن إجمالي لسلسلة نماذج Gemini كلها: بعده تظهر رسالة خطأ بدل أن تبقى "جارٍ المعالجة" معلّقة.
private const val GEMINI_TOTAL_TIMEOUT_MS = 40_000L

// عند وجود ملف عمل (قراءة/تعديل كود) يتضمن الرد الملف كاملاً، لذلك نمنحه وقتاً أطول.
private const val EDIT_TOTAL_TIMEOUT_MS = 110_000L

enum class AiError { NOT_CONFIGURED, BAD_KEY, RATE_LIMIT, NETWORK, EMPTY, OTHER }

sealed class AiResult {
    data class Success(val text: String, val code: List<CodeBlock> = emptyList()) : AiResult()
    data class Error(val kind: AiError, val detail: String = "") : AiResult()
}

sealed class ImageResult {
    class Success(val bytes: ByteArray) : ImageResult()
    data class Error(val kind: AiError, val detail: String = "") : ImageResult()
}

/** The code file the user is working on: read once, then explained / edited over several requests. */
data class WorkingFile(
    val name: String,
    /** Uri of the original file (null = unknown, so the edit can only be copied or saved as new). */
    val uri: String?,
    val content: String
)

class AiChatService {

    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .writeTimeout(10, TimeUnit.SECONDS)
        .readTimeout(20, TimeUnit.SECONDS)
        .callTimeout(25, TimeUnit.SECONDS)   // حد أقصى لكل محاولة (نموذج) حتى لا يعلق الطلب
        .build()

    // للطلبات الثقيلة فقط (توليد الصور / تحليل الملفات): تحتاج وقتاً أطول من الدردشة العادية.
    private val longClient: OkHttpClient = client.newBuilder()
        .readTimeout(90, TimeUnit.SECONDS)
        .callTimeout(100, TimeUnit.SECONDS)
        .build()

    // نماذج رجعت 404 (غير موجودة/متوقفة): نتجاوزها في بقية الجلسة بدل إعادة تجربتها كل مرة.
    private val unavailableModels: MutableSet<String> = java.util.concurrent.ConcurrentHashMap.newKeySet()

    private fun activeModels(): List<String> =
        GEMINI_MODELS.filter { it !in unavailableModels }.ifEmpty { GEMINI_MODELS }

    private val history = ArrayList<Pair<String, String>>()
    private val lock = Any()

    /** While set, its content is sent with every request so the AI can read and edit it. */
    @Volatile
    var workingFile: WorkingFile? = null

    fun isConfigured(): Boolean = GEMINI_API_KEY.isNotBlank() || OPENAI_API_KEY.isNotBlank() || CLAUDE_API_KEY.isNotBlank()

    fun clearHistory() {
        synchronized(lock) { history.clear() }
    }

    suspend fun ask(text: String, lang: AppLanguage): AiResult = withContext(Dispatchers.IO) {
        if (!isConfigured()) return@withContext AiResult.Error(AiError.NOT_CONFIGURED)

        val trace = ArrayList<String>()
        var lastError: AiResult.Error = AiResult.Error(AiError.OTHER, "No models tried")

        if (GEMINI_API_KEY.isNotBlank()) {
            var timedOut = true
            val editing = workingFile != null
            val totalTimeout = if (editing) EDIT_TOTAL_TIMEOUT_MS else GEMINI_TOTAL_TIMEOUT_MS
            // للتعديل على الكود نفضّل النماذج الأقوى (غير lite) أولاً.
            val models = if (editing) activeModels().sortedBy { if (it.contains("lite")) 1 else 0 } else activeModels()
            val geminiResult: AiResult? = withTimeoutOrNull(totalTimeout) {
                for (modelName in models) {
                    val started = System.currentTimeMillis()
                    val result = askGeminiModel(modelName, text, lang)
                    val took = System.currentTimeMillis() - started
                    if (result is AiResult.Success) {
                        Log.i(TAG, "$modelName OK in ${took}ms")
                        timedOut = false
                        return@withTimeoutOrNull result
                    }
                    if (result is AiResult.Error) {
                        val line = "$modelName ${took}ms ${result.kind} ${result.detail}".take(140)
                        Log.w(TAG, line)   // Logcat: فلتر AiChat
                        trace.add(line)
                        lastError = result
                        if (result.kind == AiError.BAD_KEY || result.kind == AiError.NOT_CONFIGURED) break
                    }
                }
                timedOut = false
                null
            }
            if (geminiResult is AiResult.Success) return@withContext geminiResult
            val summary = trace.joinToString(" | ").take(400)
            lastError = if (timedOut) {
                AiResult.Error(AiError.NETWORK, "timeout ${totalTimeout / 1000}s | $summary")
            } else {
                lastError.copy(detail = summary.ifBlank { lastError.detail })
            }
        }

        if (OPENAI_API_KEY.isNotBlank()) {
            val result = askChatGPT(text, lang)
            if (result is AiResult.Success) return@withContext result
            if (result is AiResult.Error) lastError = result
        }

        if (CLAUDE_API_KEY.isNotBlank()) {
            val result = askClaude(text, lang)
            if (result is AiResult.Success) return@withContext result
            if (result is AiResult.Error) lastError = result
        }

        return@withContext lastError
    }

    private suspend fun askGeminiModel(modelName: String, text: String, lang: AppLanguage): AiResult {
        try {
            val json = buildGeminiBody(text, lang).toString()
            val request = Request.Builder()
                .url("$GEMINI_BASE$modelName:generateContent")
                .header("x-goog-api-key", GEMINI_API_KEY)
                .post(json.toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()

            (if (workingFile != null) longClient else client).newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    if (response.code == 404) unavailableModels.add(modelName)
                    return AiResult.Error(kindForGemini(response.code, raw), apiError(response.code, raw))
                }
                val full = extractGeminiText(raw)
                if (full.isBlank()) return AiResult.Error(AiError.EMPTY)
                val (spoken, rawCode) = splitCode(full, lang)
                val code = applyEdit(rawCode)
                // The edited file already lives in the system prompt, so history only keeps the short summary.
                remember(text, if (code.any { it.isEdit }) spoken else full)
                return AiResult.Success(spoken, code)
            }
        } catch (e: IOException) {
            return AiResult.Error(AiError.NETWORK, e.toString().take(160))
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            return AiResult.Error(AiError.OTHER, e.toString().take(160))
        }
    }

    private suspend fun askChatGPT(text: String, lang: AppLanguage): AiResult {
        try {
            val json = JSONObject()
                .put("model", "gpt-4o-mini")
                .put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", text)))
                .toString()
            val request = Request.Builder()
                .url(OPENAI_BASE)
                .header("Authorization", "Bearer $OPENAI_API_KEY")
                .post(json.toRequestBody("application/json".toMediaType()))
                .build()
            client.newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    return AiResult.Error(if (response.code == 401) AiError.BAD_KEY else AiError.OTHER, "HTTP ${response.code}")
                }
                val full = JSONObject(raw).getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content")
                val (spoken, code) = splitCode(full, lang)
                return AiResult.Success(spoken, code)
            }
        } catch (e: Exception) {
            return AiResult.Error(AiError.NETWORK, e.toString().take(160))
        }
    }

    private suspend fun askClaude(text: String, lang: AppLanguage): AiResult {
        try {
            val json = JSONObject()
                .put("model", "claude-3-haiku-20240307")
                .put("max_tokens", 4096)
                .put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", text)))
                .toString()
            val request = Request.Builder()
                .url(CLAUDE_BASE)
                .header("x-api-key", CLAUDE_API_KEY)
                .header("anthropic-version", "2023-06-01")
                .post(json.toRequestBody("application/json".toMediaType()))
                .build()
            client.newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    return AiResult.Error(if (response.code == 401) AiError.BAD_KEY else AiError.OTHER, "HTTP ${response.code}")
                }
                val full = JSONObject(raw).getJSONArray("content").getJSONObject(0).getString("text")
                val (spoken, code) = splitCode(full, lang)
                return AiResult.Success(spoken, code)
            }
        } catch (e: Exception) {
            return AiResult.Error(AiError.NETWORK, e.toString().take(160))
        }
    }

    suspend fun generateImage(prompt: String): ImageResult = withContext(Dispatchers.IO) {
        if (GEMINI_API_KEY.isBlank()) return@withContext ImageResult.Error(AiError.NOT_CONFIGURED)
        try {
            val json = JSONObject()
                .put("contents", JSONArray().put(turn("user", prompt)))
                .put("generationConfig", JSONObject().put("responseModalities", JSONArray().put("TEXT").put("IMAGE")))
                .toString()
            val request = Request.Builder()
                .url("$GEMINI_BASE$IMAGE_MODEL:generateContent")
                .header("x-goog-api-key", GEMINI_API_KEY)
                .post(json.toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()
            longClient.newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    return@withContext ImageResult.Error(kindForGemini(response.code, raw), apiError(response.code, raw))
                }
                val parts = JSONObject(raw).optJSONArray("candidates")?.optJSONObject(0)?.optJSONObject("content")?.optJSONArray("parts")
                    ?: return@withContext ImageResult.Error(AiError.EMPTY)
                for (i in 0 until parts.length()) {
                    val part = parts.optJSONObject(i) ?: continue
                    val inline = part.optJSONObject("inlineData") ?: part.optJSONObject("inline_data")
                    val data = inline?.optString("data").orEmpty()
                    if (data.isNotBlank()) return@withContext ImageResult.Success(Base64.decode(data, Base64.DEFAULT))
                }
                return@withContext ImageResult.Error(AiError.EMPTY)
            }
        } catch (e: Exception) {
            return@withContext ImageResult.Error(AiError.NETWORK, e.toString().take(160))
        }
    }

    /** تنفيذ الطلب بشكل قابل للإلغاء: عند انتهاء المهلة أو إلغاء الكوروتين يُقطع الاتصال فعلاً. */
    private suspend fun Call.await(): Response = suspendCancellableCoroutine { cont ->
        cont.invokeOnCancellation { cancel() }
        enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                if (cont.isActive) cont.resumeWithException(e)
            }

            override fun onResponse(call: Call, response: Response) {
                cont.resume(response)
            }
        })
    }

    private fun kindForGemini(code: Int, raw: String): AiError = when (code) {
        401, 403 -> AiError.BAD_KEY
        400 -> if (raw.contains("API key", ignoreCase = true)) AiError.BAD_KEY else AiError.OTHER
        429 -> AiError.RATE_LIMIT
        else -> AiError.OTHER
    }

    private fun apiError(code: Int, raw: String): String {
        val msg = try { JSONObject(raw).optJSONObject("error")?.optString("message").orEmpty() } catch (e: Exception) { "" }
        return "HTTP $code: " + msg.replace("\n", " ").take(200)
    }

    /** Sends a question together with one attached file (image, PDF or text) to Gemini. */
    suspend fun askWithFile(
        text: String,
        lang: AppLanguage,
        mime: String,
        name: String,
        bytes: ByteArray
    ): AiResult = withContext(Dispatchers.IO) {
        if (!isConfigured()) return@withContext AiResult.Error(AiError.NOT_CONFIGURED)

        val isMedia = mime.startsWith("image/") || mime == "application/pdf"
        val parts = JSONArray()
        if (isMedia) {
            parts.put(JSONObject().put("text", text))
            parts.put(
                JSONObject().put(
                    "inline_data",
                    JSONObject()
                        .put("mime_type", mime)
                        .put("data", java.util.Base64.getEncoder().encodeToString(bytes))
                )
            )
        } else {
            // Any other file is sent as plain text, so it must be valid UTF-8 and reasonably small.
            if (bytes.size > 1_000_000) {
                return@withContext AiResult.Error(AiError.OTHER, lang.tr("الملف النصي كبير جداً.", "Text file is too large."))
            }
            val decoded = try {
                Charsets.UTF_8.newDecoder()
                    .onMalformedInput(java.nio.charset.CodingErrorAction.REPORT)
                    .decode(java.nio.ByteBuffer.wrap(bytes))
                    .toString()
            } catch (e: java.nio.charset.CharacterCodingException) {
                return@withContext AiResult.Error(AiError.OTHER, lang.tr("نوع هذا الملف غير مدعوم (الصور و PDF والملفات النصية فقط).", "This file type is not supported (images, PDF and text files only)."))
            }
            parts.put(JSONObject().put("text", "$text\n\n--- ${lang.tr("محتوى الملف", "File content")}: $name ---\n$decoded"))
        }

        try {
            val contents = JSONArray()
            synchronized(lock) {
                history.forEach { (role, t) -> contents.put(turn(role, t)) }
            }
            contents.put(JSONObject().put("role", "user").put("parts", parts))

            val body = JSONObject()
                .put(
                    "system_instruction",
                    JSONObject().put("parts", JSONArray().put(JSONObject().put("text", systemPrompt(lang))))
                )
                .put("contents", contents)
                .put("generationConfig", JSONObject().put("maxOutputTokens", 16384))

            val request = Request.Builder()
                .url("$GEMINI_BASE${GEMINI_MODELS.first()}:generateContent")
                .header("x-goog-api-key", GEMINI_API_KEY)
                .post(body.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()

            longClient.newCall(request).execute().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    return@withContext AiResult.Error(kindForGemini(response.code, raw), apiError(response.code, raw))
                }
                val full = extractGeminiText(raw)
                if (full.isBlank()) {
                    return@withContext AiResult.Error(AiError.EMPTY)
                }
                val (spoken, code) = splitCode(full, lang)
                remember("$text [$name]", full)
                AiResult.Success(spoken, code)
            }
        } catch (e: IOException) {
            AiResult.Error(AiError.NETWORK, e.toString().take(160))
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            AiResult.Error(AiError.OTHER, e.toString().take(160))
        }
    }

    private fun turn(role: String, text: String): JSONObject =
        JSONObject().put("role", role).put("parts", JSONArray().put(JSONObject().put("text", text)))

    private fun basePrompt(lang: AppLanguage): String = lang.tr(
        "أنت مساعد صوتي ذكي. أجب بالعربية وبإيجاز. إذا طلب المستخدم كوداً، اكتبه داخل كتلة markdown.",
        "You are a smart voice assistant. Answer briefly in English. If the user asks for code, provide it in a markdown block."
    )

    private fun editingRules(): String = """
        The user is working on the code file given below. You can read it, explain it, find bugs and edit it when asked.
        Rules:
        1. When asked to change, fix, add or refactor something, return the COMPLETE updated file (never only a snippet, never "rest unchanged") in exactly ONE code block. Write the word edit after the language on the opening fence, for example ```kotlin edit. Keep all unrelated code and formatting exactly as it was.
        2. Outside the code block write 1-3 short plain sentences saying what you changed. They are read aloud, so put no code or symbols there.
        3. If the user only asks a question or wants an explanation, answer in plain text and do NOT return the whole file.
        4. If the request is unclear, ask one short question instead of guessing.
        5. If the question is unrelated to this file, ignore the file.
    """.trimIndent()

    private fun systemPrompt(lang: AppLanguage): String {
        val base = basePrompt(lang)
        val file = workingFile ?: return base
        return base + "\n\n" + editingRules() +
            "\n\n=== BEGIN FILE: ${file.name} ===\n" + file.content + "\n=== END FILE ==="
    }

    private fun buildGeminiBody(text: String, lang: AppLanguage): JSONObject {
        val contents = JSONArray()
        synchronized(lock) { history.forEach { (role, t) -> contents.put(turn(role, t)) } }
        contents.put(turn("user", text))
        return JSONObject()
            .put("system_instruction", JSONObject().put("parts", JSONArray().put(JSONObject().put("text", systemPrompt(lang)))))
            .put("contents", contents)
            .put("generationConfig", JSONObject().put("maxOutputTokens", if (workingFile != null) 32768 else 8192))
    }

    private fun extractGeminiText(raw: String): String {
        val parts = JSONObject(raw).optJSONArray("candidates")?.optJSONObject(0)?.optJSONObject("content")?.optJSONArray("parts") ?: return ""
        val sb = StringBuilder()
        for (i in 0 until parts.length()) {
            parts.optJSONObject(i)?.optString("text")?.let { sb.append(it) }
        }
        return sb.toString().trim()
    }

    // group 1 = language, group 2 = extra words on the fence line (e.g. "edit"), group 3 = the code.
    private val fence = Regex("```([A-Za-z0-9+#._-]*)([^\\r\\n]*)\\r?\\n([\\s\\S]*?)```")

    private fun splitCode(full: String, lang: AppLanguage): Pair<String, List<CodeBlock>> {
        if (!full.contains("```")) return clean(full) to emptyList()
        val text = if (Regex("```").findAll(full).count() % 2 == 1) full + "\n```" else full
        val blocks = fence.findAll(text).map {
            CodeBlock(
                language = it.groupValues[1].lowercase(),
                content = it.groupValues[3].trimEnd(),
                isEdit = it.groupValues[2].contains("edit", ignoreCase = true)
            )
        }.toList()
        if (blocks.isEmpty()) return clean(full) to emptyList()
        var spoken = clean(fence.replace(text, " "))
        if (spoken.isBlank()) spoken = lang.tr("تفضل، هذا هو الكود.", "Here is the code.")
        return spoken to blocks
    }

    /**
     * If the answer holds the complete edited file, it becomes the new working file and the block is tagged
     * with the original file name / Uri so the UI can write it back. Short snippets are left untouched.
     */
    private fun applyEdit(blocks: List<CodeBlock>): List<CodeBlock> {
        val file = workingFile ?: return blocks
        val originalLines = file.content.lines().size
        val edited = blocks.firstOrNull { it.isEdit }
            ?: blocks.singleOrNull()?.takeIf { it.content.lines().size >= originalLines * 6 / 10 }
            ?: return blocks
        val trailing = if (file.content.endsWith("\n")) "\n" else ""
        workingFile = file.copy(content = edited.content + trailing)
        return blocks.map {
            if (it === edited) it.copy(isEdit = true, fileName = file.name, sourceUri = file.uri) else it
        }
    }

    private fun clean(text: String): String = text.replace("*", "").replace("#", "").replace("`", "").replace(Regex("\\n{2,}"), "\n").trim()

    private fun remember(userText: String, answer: String) {
        synchronized(lock) {
            history.add("user" to userText)
            history.add("model" to answer)
            while (history.size > MAX_HISTORY_MESSAGES) history.removeAt(0)
        }
    }
}

package com.zevorix.ai.local

import android.content.Context
import android.os.Environment
import com.google.mediapipe.tasks.genai.llminference.LlmInference
import com.google.mediapipe.tasks.genai.llminference.LlmInferenceSession
import com.google.mediapipe.tasks.genai.llminference.ProgressListener
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileNotFoundException
import java.util.concurrent.Executor

/** إعدادات النموذج المحلي. */
data class LocalAiConfig(
    /** اسم ملف النموذج (.task أو .bin) داخل مجلد voice assistant 2 */
    val modelFileName: String = "gemma-2b-it-cpu-int4.bin",
    /** الحد الأقصى لمجموع التوكنات (المدخل + المخرج) */
    val maxTokens: Int = 1024,
    val temperature: Float = 0.7f,
    val topK: Int = 40,
    val randomSeed: Int = 0,
    val backend: LlmInference.Backend = LlmInference.Backend.CPU,
    /** قالب المحادثة. هذا قالب Gemma؛ غيّره حسب النموذج المستخدم. */
    val promptTemplate: (String) -> String = { userText ->
        "<start_of_turn>user\n$userText<end_of_turn>\n<start_of_turn>model\n"
    },
)

sealed interface LocalAiState {
    data object Unloaded : LocalAiState
    data object Loading : LocalAiState
    data object Ready : LocalAiState
    data class Error(val message: String) : LocalAiState
}

/**
 * خدمة ذكاء اصطناعي محلية تعمل بالكامل على معالج الهاتف بدون إنترنت.
 * أنشئ نسخة واحدة فقط (Singleton) لأن تحميل النموذج مكلف.
 */
class LocalAiService(
    context: Context,
    private val config: LocalAiConfig = LocalAiConfig(),
) {
    private val appContext = context.applicationContext

    private val loadMutex = Mutex()
    private val inferenceMutex = Mutex() // طلب استدلال واحد في كل مرة

    @Volatile
    private var llm: LlmInference? = null

    private val _state = MutableStateFlow<LocalAiState>(LocalAiState.Unloaded)
    val state: StateFlow<LocalAiState> = _state.asStateFlow()

    val isReady: Boolean get() = llm != null

    /** يحمّل النموذج (آمن للاستدعاء المتكرر). */
    suspend fun load(): Result<Unit> = loadMutex.withLock {
        if (llm != null) return@withLock Result.success(Unit)
        withContext(Dispatchers.IO) {
            _state.value = LocalAiState.Loading
            runCatching {
                val modelFile = resolveModelFile()
                val options = LlmInference.LlmInferenceOptions.builder()
                    .setModelPath(modelFile.absolutePath)
                    .setMaxTokens(config.maxTokens)
                    .setPreferredBackend(config.backend)
                    .build()
                llm = LlmInference.createFromOptions(appContext, options)
                _state.value = LocalAiState.Ready
            }.onFailure {
                llm = null
                _state.value = LocalAiState.Error(it.message ?: "فشل تحميل النموذج")
            }
        }
    }

    /** يولّد الرد كاملاً (دالة suspend تعمل على Dispatchers.IO). */
    suspend fun generate(
        prompt: String,
        temperature: Float = config.temperature,
        topK: Int = config.topK,
    ): String = withContext(Dispatchers.IO) {
        generateStream(prompt, temperature, topK).toList().joinToString("")
    }

    /** يولّد الرد على دفعات (Streaming) لعرضه تدريجياً في الواجهة. */
    fun generateStream(
        prompt: String,
        temperature: Float = config.temperature,
        topK: Int = config.topK,
    ): Flow<String> = callbackFlow {
        load().getOrThrow()
        val engine = checkNotNull(llm) { "النموذج غير محمّل" }

        inferenceMutex.withLock {
            val sessionOptions = LlmInferenceSession.LlmInferenceSessionOptions.builder()
                .setTemperature(temperature)
                .setTopK(topK)
                .setRandomSeed(config.randomSeed)
                .build()
            val session = LlmInferenceSession.createFromOptions(engine, sessionOptions)

            try {
                session.addQueryChunk(config.promptTemplate(prompt))

                val future = session.generateResponseAsync(
                    ProgressListener<String> { partial, done ->
                        if (partial.isNotEmpty()) trySend(partial)
                        if (done) close()
                    }
                )
                future.addListener(
                    {
                        try {
                            future.get()
                        } catch (e: Exception) {
                            if (e !is CancellationException) close(e)
                        }
                    },
                    Executor { it.run() }
                )

                awaitClose {
                    // عند إلغاء الـ Flow نوقف التوليد
                    runCatching { session.cancelGenerateResponseAsync() }
                }
            } finally {
                runCatching { session.close() }
            }
        }
    }

    /** يحرر ذاكرة النموذج. استدعِه عند onCleared أو عند ضغط الذاكرة. */
    fun release() {
        runCatching { llm?.close() }
        llm = null
        _state.value = LocalAiState.Unloaded
    }

    // ---------------------------------------------------------------

    /**
     * يبحث عن ملف النموذج مباشرة في مجلد "voice assistant 2" على الذاكرة الخارجية،
     * مع وجود مسار التطبيق الداخلي كخيار احتياطي.
     */
    private fun resolveModelFile(): File {
        // 1. البحث في مجلد voice assistant 2 الخارجي
        val externalDir = File(Environment.getExternalStorageDirectory(), "voice assistant 2")
        val target = File(externalDir, config.modelFileName)
        if (target.exists() && target.length() > 0) {
            return target
        }

        // 2. خيار احتياطي: البحث في مجلد التطبيق الداخلي
        val internalDir = File(appContext.filesDir, "models")
        val internalTarget = File(internalDir, config.modelFileName)
        if (internalTarget.exists() && internalTarget.length() > 0) {
            return internalTarget
        }

        throw FileNotFoundException(
            "ملف النموذج ${config.modelFileName} غير موجود في مجلد 'voice assistant 2' ولا في مسار التطبيق الداخلي."
        )
    }
}

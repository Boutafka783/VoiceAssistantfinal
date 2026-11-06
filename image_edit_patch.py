#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
image_edit_patch.py  —  ملف مستقل (تعديل الصور + إصلاح توليد الصور) (ضعه بجانب setup.py في الجذر).
يُشغَّل بعد `python setup.py` ويضيف ميزة تعديل الصور:
  AiChatService.editImage  +  MainViewModel (isImageEditRequest / editAttachedImage)
آمن عند التكرار: إن كان الباتش مطبَّقاً من قبل يتخطّى ولا يغيّر شيئاً.
"""
import os
import sys

_PKG = "app/src/main/java/com/example/voiceassistant"


def insert_before(path, anchor, insertion):
    """Inserts `insertion` right before the single occurrence of `anchor`."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if text.count(anchor) != 1:
        raise RuntimeError("Anchor is not unique in {}: {!r} (found {})".format(path, anchor[:70], text.count(anchor)))
    text = text.replace(anchor, insertion + anchor, 1)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ==============================================================================
# إصلاح توليد الصور (كتابة / صوت)  — IMAGE-GEN-V2
#   1) كاشف طلب الصورة أوسع: «اعطني/أريد/عايز/هات صورة...» و«يا زيفوريكس ارسم...» و«ولّد» بالتشكيل
#      و«image of a cat» و«ارسم لي شعار لتطبيق». لا يلتقط طلبات الأكواد/الصفحات.
#   2) رسالة الخطأ الحقيقية القادمة من الخادم تظهر بين [ ] بدل رسالة عامة.
# ==============================================================================
import re

_VM_FILE = _PKG + "/viewmodel/MainViewModel.kt"
_AI_FILE2 = _PKG + "/data/AiChatService.kt"

_NEW_DETECTOR = r'''    private fun isImageRequest(text: String): Boolean {
        // IMAGE-GEN-V2: normalize (no tashkeel, one alef/teh-marbuta/yeh form) and drop wake / polite words.
        var t = text.lowercase()
            .replace(Regex("[\u064B-\u065F\u0670\u0640]"), "")
            .replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
            .replace('ة', 'ه').replace('ى', 'ي')
            .trim()
        t = t.replace(Regex("""^(?:يا\s+)?(?:زيفوريكس|زيفوركس|زيفورکس|zevorix)[\s,،:]*"""), "")
        t = t.replace(Regex("""^(?:من فضلك|لو سمحت|ممكن|رجاء|please|can you|could you|i want you to)\s+"""), "")
        if (t.isEmpty()) return false
        // Real code requests stay normal AI answers.
        if (Regex("""(html|css|javascript|kotlin|python|script|json|setup|code|كود|اكواد|برمجه|سكربت|سكريبت)""").containsMatchIn(t)) return false
        val noun = """(?:صوره|صور|لوحه|رسمه|رسمات|شعار|لوجو|ايقونه|بوستر|تصميم|خلفيه|image|images|picture|pictures|photo|photos|drawing|illustration|logo|painting|poster|wallpaper|icon)"""
        val filler = """(?:\s+(?:لي|لنا|me|us|a|an|the|some|new|جديده|جميله|حلوه|رائعه|واقعيه|احترافيه))*"""
        val drawVerb = Regex("""^(?:ارسم|ارسمي|ارسملي|ارسمها|draw|sketch|paint)(?:\s|$)""")
        if (drawVerb.containsMatchIn(t)) return true
        val verb = """(?:ولد|انشي|انشئ|اصنع|اعمل|سوي|انتج|توليد|رسم|صمم|اعطني|اعطيني|اريد|ابغي|ابي|عايز|عايزه|عاوز|هات|هاتلي|جيب|اعرض|اظهر|generate|create|make|design|produce|give me|show me|get me|i want|i need)"""
        if (Regex("""^$verb$filler\s+$noun(?:\s|$)""").containsMatchIn(t)) return true
        if (Regex("""^(?:$noun)\s+\S""").containsMatchIn(t) && Regex("""^(?:صوره|صور|image|picture|photo|drawing|logo)""").containsMatchIn(t)) return true
        return false
    }
'''

with open(_VM_FILE, "r", encoding="utf-8") as _f:
    _vm_text = _f.read()
if "IMAGE-GEN-V2" not in _vm_text:
    _m = re.findall(r"    private fun isImageRequest\(text: String\): Boolean \{\n.*?\n    \}\n", _vm_text, flags=re.S)
    if len(_m) != 1:
        raise RuntimeError("Expected exactly one isImageRequest in MainViewModel.kt, found {}".format(len(_m)))
    _vm_text = re.sub(r"    private fun isImageRequest\(text: String\): Boolean \{\n.*?\n    \}\n",
                      lambda _x: _NEW_DETECTOR, _vm_text, count=1, flags=re.S)
    with open(_VM_FILE, "w", encoding="utf-8", newline="\n") as _f:
        f_ = _f.write(_vm_text)
    print(">> Image detector upgraded (IMAGE-GEN-V2).")
else:
    print(">> Image detector already upgraded - skipping.")

with open(_AI_FILE2, "r", encoding="utf-8") as _f:
    _ai_text = _f.read()
_OLD_ERR = '''                        else -> ImageResult.Error(AiError.OTHER, "HTTP ${response.code}")
                    }
                }
                val json = JSONObject(raw)
                val b64 = json.optString("image", "")'''
_NEW_ERR = '''                        else -> {
                            // IMAGE-GEN-V2: show the server's real reason (it is printed between [ ] in the chat).
                            val srv = try { JSONObject(raw).let { it.optString("message", it.optString("error", "")) } } catch (e: Exception) { "" }
                            ImageResult.Error(AiError.OTHER, "HTTP ${response.code} $srv".trim().take(220))
                        }
                    }
                }
                val json = JSONObject(raw)
                val b64 = json.optString("image", "")'''
if "IMAGE-GEN-V2" not in _ai_text:
    if _ai_text.count(_OLD_ERR) != 1:
        raise RuntimeError("generateImage error branch not found exactly once in AiChatService.kt (found {})".format(_ai_text.count(_OLD_ERR)))
    with open(_AI_FILE2, "w", encoding="utf-8", newline="\n") as _f:
        _f.write(_ai_text.replace(_OLD_ERR, _NEW_ERR, 1))
    print(">> generateImage now reports the server's error message.")
else:
    print(">> generateImage error detail already applied - skipping.")


_AI_FILE = _PKG + "/data/AiChatService.kt"
if not os.path.isfile(_AI_FILE):
    print("ERROR: {} not found - run `python setup.py` first.".format(_AI_FILE))
    sys.exit(1)
with open(_AI_FILE, "r", encoding="utf-8") as _f:
    if "suspend fun editImage" in _f.read():
        print(">> Image editing already applied - skipping.")
        sys.exit(0)

# ==============================================================================
# تعديل الصور (Image Editing)
#   صورة المستخدم + نص التوجيه  →  الخادم /api/ai/image-edit (Gemini)  →  صورة جديدة في المحادثة.
#   - AiChatService.editImage(prompt, mime, bytes): يرسل الصورة (Base64) إلى الخادم مع رخصة الجهاز.
#   - MainViewModel: إذا أرفق المستخدم صورة وكتب أمر تعديل (غيّر/احذف/أضف/Edit/Remove...) يُنفَّذ التعديل
#     (يخصم نقطتين)، وإلا تبقى الصورة تُحلَّل عبر askWithFile كما كانت.
#   تعديل الفيديو موجود مسبقاً (editVideoRequest + /edit-video) ولا يتغير.
# ==============================================================================
print(">> Adding image editing (editImage + MainViewModel hook)...")

_IE_AI = _PKG + "/data/AiChatService.kt"
_IE_VM = _PKG + "/viewmodel/MainViewModel.kt"

# 1) AiChatService.editImage (قبل قسم Document، بعد generateImage)
insert_before(
    _IE_AI,
    "    // ------------------------------------------------------------------ Document\n",
    r'''    // ------------------------------------------------------------------ Image editing
    /** Phone photos are huge: scale big pictures down (max 2048 px, JPEG) so the request stays small and fast. */
    private fun shrinkForEdit(mime: String, bytes: ByteArray): Pair<String, ByteArray> {
        if (bytes.size <= 3_000_000) return mime to bytes
        return try {
            val bounds = android.graphics.BitmapFactory.Options().apply { inJustDecodeBounds = true }
            android.graphics.BitmapFactory.decodeByteArray(bytes, 0, bytes.size, bounds)
            var sample = 1
            while (maxOf(bounds.outWidth, bounds.outHeight) / sample > 2048) sample *= 2
            val opts = android.graphics.BitmapFactory.Options().apply { inSampleSize = sample }
            val bmp = android.graphics.BitmapFactory.decodeByteArray(bytes, 0, bytes.size, opts)
                ?: return mime to bytes
            val out = java.io.ByteArrayOutputStream()
            bmp.compress(android.graphics.Bitmap.CompressFormat.JPEG, 90, out)
            bmp.recycle()
            "image/jpeg" to out.toByteArray()
        } catch (e: Throwable) {
            mime to bytes
        }
    }

    /** Edits a picture: original image + instruction -> a new image (Gemini image model, through the backend). */
    suspend fun editImage(prompt: String, mime: String, bytes: ByteArray): ImageResult = withContext(Dispatchers.IO) {
        val key = LicenseManager.getBackendKey()
        if (key.isEmpty()) return@withContext ImageResult.Error(AiError.NOT_CONFIGURED)
        val did = CreditsManager.currentDeviceId()
        if (did.isEmpty()) return@withContext ImageResult.Error(AiError.NOT_CONFIGURED, "no device id")
        val (sendMime, sendBytes) = shrinkForEdit(mime, bytes)
        val body = JSONObject()
            .put("licenseKey", key)
            .put("deviceId", did)
            .put("prompt", prompt)
            .put("mime", sendMime)
            .put("image", Base64.encodeToString(sendBytes, Base64.NO_WRAP))
        try {
            val request = Request.Builder()
                .url("$BACKEND_BASE/api/ai/image-edit")
                .post(body.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()
            longClient.newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    val detail = try { JSONObject(raw).optString("error", "") } catch (e: Exception) { "" }
                    return@use when (response.code) {
                        402 -> ImageResult.Error(AiError.INSUFFICIENT_CREDITS)
                        401, 403 -> ImageResult.Error(AiError.BAD_KEY)
                        429 -> ImageResult.Error(AiError.RATE_LIMIT)
                        503 -> ImageResult.Error(AiError.NOT_CONFIGURED)
                        422 -> ImageResult.Error(AiError.EMPTY, detail)
                        else -> ImageResult.Error(AiError.OTHER, "HTTP ${response.code} $detail".trim())
                    }
                }
                val b64 = JSONObject(raw).optString("image", "")
                if (b64.isEmpty()) return@use ImageResult.Error(AiError.EMPTY)
                ImageResult.Success(Base64.decode(b64, Base64.DEFAULT))
            }
        } catch (e: IOException) {
            ImageResult.Error(AiError.NETWORK, e.toString().take(160))
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            ImageResult.Error(AiError.OTHER, e.toString().take(160))
        }
    }

''')

# 2) MainViewModel: دالتان جديدتان (قبل replyAiError)
insert_before(
    _IE_VM,
    "    /** Speaks the friendly message and also prints the technical detail (not spoken) so the real cause is visible. */\n",
    r'''    /** True when the text is an instruction to change a picture ("غيّر الخلفية", "remove the person"), not a question about it. */
    private fun isImageEditRequest(text: String): Boolean {
        val t = text.trim().lowercase()
        if (t.isEmpty()) return false
        val arabic = Regex("^(?:(?:من فضلك|لو سمحت|ممكن|رجاء|يا زيفوريكس)\\s+)?(?:عدّل|عدل|غيّر|غير|بدّل|بدل|احذف|امسح|أزل|ازل|أضف|اضف|حوّل|حول|لوّن|لون|اجعل|خلّي|خلي|نظّف|نظف|حسّن|حسن|ركّب|ركب|زد|زوّد|زود|اطمس|طبّق|طبق)(?:\\s|$)")
        val english = Regex("^(?:(?:please|can you|could you)\\s+)?(?:edit|change|remove|erase|delete|add|replace|make|turn|convert|colorize|enhance|retouch|blur|crop|restyle|swap|fix|put)\\b")
        return arabic.containsMatchIn(t) || english.containsMatchIn(t)
    }

    /** Sends the attached picture + the instruction to the image editor and shows the edited picture in the chat. */
    private suspend fun editAttachedImage(instruction: String, lang: AppLanguage, attachment: com.example.voiceassistant.data.AttachmentData) {
        if (!ensureQuota(lang, false, 2)) return
        repository.addAssistantPlaceholder(lang.tr("جاري تعديل الصورة...", "Editing the image..."))
        when (val result = ai.editImage(instruction, attachment.mime, attachment.bytes)) {
            is ImageResult.Success -> {
                val path = withContext(Dispatchers.IO) { saveImage(result.bytes) }
                if (path == null) {
                    reply(aiErrorMessage(AiError.OTHER, lang), lang, speak = false)
                } else {
                    reply(lang.tr("تفضل، هذه هي الصورة بعد التعديل.", "Here is your edited image."), lang, imagePath = path, speak = false)
                    CreditsManager.recordSuccess(2)
                }
            }
            is ImageResult.Error -> replyAiError(result.kind, result.detail, lang, speak = false)
        }
    }

''')

# 3) MainViewModel.sendTyped: صورة + أمر تعديل => تعديل بدل التحليل
insert_before(
    _IE_VM,
    "            if (!ensureQuota(lang, attachment.speakReply)) return@launch\n"
    "            repository.addAssistantPlaceholder(\n",
    r'''            // Image editing: a picture + an edit instruction (not a question) gives a new picture.
            if (attachment.mime.startsWith("image/") && !attachment.speakReply && isImageEditRequest(clean)) {
                editAttachedImage(clean, lang, attachment)
                return@launch
            }
''')

print(">> Image editing applied: AiChatService.editImage (/api/ai/image-edit), MainViewModel.isImageEditRequest + editAttachedImage.")

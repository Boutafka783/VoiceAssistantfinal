#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
image_edit_patch.py  —  ملف مستقل (ضعه بجانب setup.py في الجذر).
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

import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_VM = PKG_DIR + "/viewmodel/MainViewModel.kt"
SPEECH_MGR = PKG_DIR + "/speech/SpeechRecognizerManager.kt"

def replace_once(file_path, old, new):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if new in content:
        return
    if content.count(old) == 1:
        content = content.replace(old, new, 1)
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"✅ Fixed call site in {file_path}")

print(">> Applying Smart Translator Patch...")

# 1) إنشاء ملف TranslatorManager.kt
os.makedirs(PKG_DIR + "/data", exist_ok=True)
translator_mgr_code = r'''package com.zevorix.assistant.data

import com.zevorix.assistant.viewmodel.AppLanguage

object TranslatorManager {
    private val cache = object : android.util.LruCache<String, String>(100) {}

    fun detectTargetLanguage(sourceLang: AppLanguage): AppLanguage {
        return if (sourceLang == AppLanguage.ARABIC) AppLanguage.ENGLISH else AppLanguage.ARABIC
    }

    fun buildPrompt(text: String, targetLang: AppLanguage): String {
        return if (targetLang == AppLanguage.ENGLISH) {
            "You are a professional translator. Translate the following Arabic text into natural English. " +
            "Output ONLY the translation, with no quotes, notes, or explanations:\n\n$text"
        } else {
            "أنت مترجم محترف. ترجم النص الإنجليزي التالي إلى العربية الفصحى البسيطة. " +
            "اكتب الترجمة فقط بدون علامات اقتباس أو ملاحظات أو شرح:\n\n$text"
        }
    }

    fun getCached(text: String, targetLang: AppLanguage): String? = cache.get("${targetLang.name}_$text")

    fun cacheResult(text: String, targetLang: AppLanguage, result: String) {
        cache.put("${targetLang.name}_$text", result)
    }
}
'''
with open(PKG_DIR + "/data/TranslatorManager.kt", "w", encoding="utf-8") as f:
    f.write(translator_mgr_code)

# 2) استبدال الكود القديم داخل MainViewModel.kt
with open(MAIN_VM, "r", encoding="utf-8") as f:
    vm = f.read()

old_translator_pattern = re.compile(r"    // ---------------- Translator mode ----------------.*?(?=    // ---------------- Screen recording by voice ----------------)", re.DOTALL)

new_vm_code = r'''    // ---------------- Advanced Translator Mode ----------------
    private val translatorPrefs = application.getSharedPreferences("voice_translator", android.content.Context.MODE_PRIVATE)
    private val _translatorMode = MutableStateFlow(translatorPrefs.getBoolean("enabled", false))
    val translatorMode: StateFlow<Boolean> = _translatorMode.asStateFlow()

    @Volatile
    private var translatorPrimary: AppLanguage = AppLanguage.ARABIC

    fun setTranslatorMode(enabled: Boolean) {
        if (_translatorMode.value == enabled) return
        _translatorMode.value = enabled
        translatorPrefs.edit().putBoolean("enabled", enabled).apply()
        val lang = _uiState.value.language
        reply(
            if (enabled) lang.tr("تم تفعيل المترجم الفوري. تحدث بأي لغة وسأترجمها فوراً.", "Instant translator is on. Speak in any language.")
            else lang.tr("تم إيقاف المترجم.", "Translator is off."),
            lang, speak = false
        )
    }

    private suspend fun handleTranslation(parsed: ParsedCommand, text: String, lang: AppLanguage, speak: Boolean) {
        val typing = parsed is ParsedCommand.TypeText
        val source = (parsed as? ParsedCommand.TypeText)?.prompt ?: text
        val sourceLang = AppLanguage.detect(source)
        val targetLang = com.zevorix.assistant.data.TranslatorManager.detectTargetLanguage(sourceLang)

        val cached = com.zevorix.assistant.data.TranslatorManager.getCached(source, targetLang)
        if (cached != null) {
            if (!typing) reply(cached, targetLang, speak = speak)
            else reply(lang.tr("الترجمة (من الذاكرة): $cached", "Translation (cached): $cached"), lang, speak = speak)
            return
        }

        if (!ensureQuota(lang, speak)) return
        _uiState.update { it.copy(status = AssistantStatus.PROCESSING, partialText = "") }
        
        val prompt = com.zevorix.assistant.data.TranslatorManager.buildPrompt(source, targetLang)
        
        when (val result = ai.ask(prompt, targetLang)) {
            is AiResult.Success -> {
                val translated = result.text.trim().trim('"', '“', '”', '«', '»').trim()
                com.zevorix.assistant.data.TranslatorManager.cacheResult(source, targetLang, translated)
                
                if (!typing) {
                    reply(translated, targetLang, speak = speak)
                    CreditsManager.recordSuccess()
                    return
                }
                
                repository.addAssistantMessage("🌐 $translated")
                if (VoiceAccessibilityService.isRunning) {
                    _backgroundRequests.tryEmit(Unit)
                    delay(700)
                }
                val success = VoiceAccessibilityService.instance?.performTypeText(translated) == true
                reply(
                    if (success) lang.tr("كتبت الترجمة. قل «أرسل» للإرسال.", "Typed the translation. Say send to send.")
                    else lang.tr("لم أجد حقل كتابة على الشاشة.", "Couldn't find a text field."),
                    lang, speak = speak
                )
                CreditsManager.recordSuccess()
            }
            is AiResult.Error -> replyAiError(result.kind, result.detail, lang, speak)
        }
    }

'''
if old_translator_pattern.search(vm):
    vm = old_translator_pattern.sub(new_vm_code, vm)
    with open(MAIN_VM, "w", encoding="utf-8", newline="\n") as f:
        f.write(vm)
    print("✅ Replaced legacy translator code in MainViewModel.kt")

# 3) إصلاح مكان استدعاء الدالة في process() (سبب فشل البناء)
replace_once(MAIN_VM, "handleTranslation(text, lang, speak)", "handleTranslation(parsed, text, lang, speak)")

# 4) تحديث SpeechRecognizerManager لدعم اللغتين
with open(SPEECH_MGR, "r", encoding="utf-8") as f:
    speech = f.read()

if "EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES" not in speech:
    replace_once(
        SPEECH_MGR,
        'putExtra("android.speech.extra.EXTRA_ADDITIONAL_LANGUAGES", arrayOf(extraLanguageTag))',
        'putExtra("android.speech.extra.EXTRA_ADDITIONAL_LANGUAGES", arrayOf(extraLanguageTag))\n'
        '                val bothLanguages = arrayListOf(languageTag, extraLanguageTag)\n'
        '                if (android.os.Build.VERSION.SDK_INT >= 33) {\n'
        '                    putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_DETECTION, true)\n'
        '                    putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES, bothLanguages)\n'
        '                }\n'
        '                if (android.os.Build.VERSION.SDK_INT >= 34) {\n'
        '                    putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_SWITCH, RecognizerIntent.LANGUAGE_SWITCH_BALANCED)\n'
        '                    putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_SWITCH_ALLOWED_LANGUAGES, bothLanguages)\n'
        '                }'
    )

print(">> Translator Patch applied successfully! Build should pass now.")
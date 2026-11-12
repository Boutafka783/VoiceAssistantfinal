import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_VM = PKG_DIR + "/viewmodel/MainViewModel.kt"
SPEECH_MGR = PKG_DIR + "/speech/SpeechRecognizerManager.kt"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"

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

print(">> Applying Smart Translator Patch (Voice forced to Auto)...")

# 1) إنشاء ملف TranslatorManager.kt
os.makedirs(PKG_DIR + "/data", exist_ok=True)
translator_mgr_code = r'''package com.zevorix.assistant.data

import android.content.Context
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.State

object TranslatorManager {
    data class LanguageOption(val code: String, val label: String)

    val languages = listOf(
        LanguageOption("auto", "تلقائي"),
        LanguageOption("ar-SA", "العربية"),
        LanguageOption("en-US", "English"),
        LanguageOption("fr-FR", "Français"),
        LanguageOption("es-ES", "Español"),
        LanguageOption("tr-TR", "Türkçe"),
        LanguageOption("de-DE", "Deutsch")
    )

    private const val PREFS = "zevorix_translator"
    private const val KEY_TARGET = "target_language"
    private val cache = object : android.util.LruCache<String, String>(100) {}
    private val _targetLanguage = mutableStateOf("auto")
    val targetLanguage: State<String> get() = _targetLanguage
    @Volatile private var initialized = false

    @Synchronized
    fun initialize(context: Context) {
        if (initialized) return
        val prefs = context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val saved = prefs.getString(KEY_TARGET, "auto") ?: "auto"
        _targetLanguage.value = languages.firstOrNull { it.code == saved }?.code ?: "auto"
        initialized = true
    }

    fun setTargetLanguage(context: Context, code: String) {
        val safe = languages.firstOrNull { it.code == code }?.code ?: "auto"
        _targetLanguage.value = safe
        context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putString(KEY_TARGET, safe).apply()
        cache.evictAll()
    }

    fun buildPrompt(text: String, targetLangCode: String = _targetLanguage.value): String {
        if (targetLangCode == "auto") {
            return "You are a professional translator. Detect the source language automatically. " +
                   "If the input is Arabic, translate it into natural English. " +
                   "If the input is not Arabic, translate it into clear Modern Standard Arabic. " +
                   "Return ONLY the translation, without explanations, labels, quotes, or notes.\n\nText:\n$text"
        }
        val target = when (targetLangCode) {
            "ar-SA" -> "Arabic (Modern Standard Arabic)"
            "en-US" -> "English"
            "fr-FR" -> "French"
            "es-ES" -> "Spanish"
            "tr-TR" -> "Turkish"
            "de-DE" -> "German"
            else -> "Arabic"
        }
        return "You are a professional translator. Translate the text into $target. " +
               "Preserve meaning, tone, names, numbers, and formatting. " +
               "Return ONLY the translation, without explanations, labels, quotes, or notes.\n\nText:\n$text"
    }

    fun getCached(text: String, targetLangCode: String = _targetLanguage.value): String? =
        cache.get("$targetLangCode|$text")

    fun cacheResult(text: String, targetLangCode: String, result: String) {
        cache.put("$targetLangCode|$text", result)
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

    /** لغة الاستماع الأساسية في وضع المترجم (كانت معرّفة في الكتلة القديمة وتستخدمها أجزاء أخرى من الملف). */
    private var translatorPrimary: AppLanguage = AppLanguage.ARABIC

    fun setTranslatorMode(enabled: Boolean) {
        if (_translatorMode.value == enabled) return
        _translatorMode.value = enabled
        translatorPrefs.edit().putBoolean("enabled", enabled).apply()
        val lang = _uiState.value.language
        reply(
            if (enabled) lang.tr("تم تفعيل المترجم الفوري.", "Instant translator is on.")
            else lang.tr("تم إيقاف المترجم.", "Translator is off."),
            lang, speak = false
        )
    }

    private suspend fun handleTranslation(parsed: ParsedCommand, text: String, lang: AppLanguage, speak: Boolean) {
        val typing = parsed is ParsedCommand.TypeText
        val source = (parsed as? ParsedCommand.TypeText)?.prompt ?: text
        
        // التعديل هنا: إذا كان الكلام صوتياً، نتجاهل الزر ونستخدم "تلقائي" دائماً
        val targetCode = if (typing) {
            com.zevorix.assistant.data.TranslatorManager.targetLanguage.value
        } else {
            "auto"
        }

        val cached = com.zevorix.assistant.data.TranslatorManager.getCached(source, targetCode)
        if (cached != null) {
            if (!typing) reply(cached, lang, speak = speak)
            else reply(lang.tr("الترجمة (من الذاكرة): $cached", "Translation (cached): $cached"), lang, speak = speak)
            return
        }

        if (!ensureQuota(lang, speak)) return
        _uiState.update { it.copy(status = AssistantStatus.PROCESSING, partialText = "") }
        
        val prompt = com.zevorix.assistant.data.TranslatorManager.buildPrompt(source, targetCode)
        
        when (val result = ai.ask(prompt, lang)) {
            is AiResult.Success -> {
                val translated = result.text.trim().trim('"', '“', '”', '«', '»').trim()
                com.zevorix.assistant.data.TranslatorManager.cacheResult(source, targetCode, translated)
                
                if (!typing) {
                    reply(translated, lang, speak = speak)
                    CreditsManager.recordSuccess()
                    return
                }
                
                repository.addAssistantMessage("🌐 $translated")
                if (com.zevorix.assistant.service.VoiceAccessibilityService.isRunning) {
                    _backgroundRequests.tryEmit(Unit)
                    delay(700)
                }
                val success = com.zevorix.assistant.service.VoiceAccessibilityService.instance?.performTypeText(translated) == true
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

replace_once(MAIN_VM, "handleTranslation(text, lang, speak)", "handleTranslation(parsed, text, lang, speak)")

# 3) تحديث SpeechRecognizerManager لدعم اللغات المتعددة
with open(SPEECH_MGR, "r", encoding="utf-8") as f:
    speech = f.read()

if "EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES" not in speech:
    replace_once(
        SPEECH_MGR,
        'putExtra("android.speech.extra.EXTRA_ADDITIONAL_LANGUAGES", arrayOf(extraLanguageTag))',
        'putExtra("android.speech.extra.EXTRA_ADDITIONAL_LANGUAGES", arrayOf(extraLanguageTag))\n'
        '                val bothLanguages = arrayListOf("ar-SA", "en-US", "fr-FR", "tr-TR", "de-DE")\n'
        '                if (android.os.Build.VERSION.SDK_INT >= 33) {\n'
        '                    putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_DETECTION, true)\n'
        '                    putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES, bothLanguages)\n'
        '                }\n'
        '                if (android.os.Build.VERSION.SDK_INT >= 34) {\n'
        '                    putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_SWITCH, RecognizerIntent.LANGUAGE_SWITCH_BALANCED)\n'
        '                    putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_SWITCH_ALLOWED_LANGUAGES, bothLanguages)\n'
        '                }'
    )

# 4) تحديث MainScreen.kt لإضافة زر اختيار اللغة
with open(MAIN_SCREEN, "r", encoding="utf-8") as f:
    screen = f.read()

if "TranslatorLanguageSelector" not in screen:
    imports_to_add = """
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.platform.LocalContext
import com.zevorix.assistant.data.TranslatorManager
"""
    pkg_match = re.search(r"(?m)^package\s+[^\n]+\n", screen)
    if pkg_match:
        screen = screen[:pkg_match.end()] + imports_to_add + screen[pkg_match.end():]

    # تعديل داخل الذاكرة (كان replace_once يكتب للملف ثم يُستبدل بالنسخة القديمة screen فتضيع التعديلات)
    _a = "    val state by viewModel.uiState.collectAsStateWithLifecycle()\n"
    if "isTranslatorOn" not in screen and screen.count(_a) >= 1:
        screen = screen.replace(_a, _a + "    val isTranslatorOn by viewModel.translatorMode.collectAsStateWithLifecycle()\n", 1)
    else:
        print("WARNING: state anchor not found / already patched")

    _b = re.search(r"([ \t]*)if \(!typing\) \{\n", screen)
    if _b and "TranslatorLanguageSelector()" not in screen:
        _ind = _b.group(1)
        screen = screen[:_b.end()] + _ind + "    if (isTranslatorOn) {\n" + _ind + "        TranslatorLanguageSelector()\n" + _ind + "    }\n" + screen[_b.end():]
    else:
        print("WARNING: '!typing' anchor not found")

    screen += r'''

@Composable
private fun TranslatorLanguageSelector() {
    val context = LocalContext.current
    var expanded by remember { mutableStateOf(false) }
    val selectedCode = TranslatorManager.targetLanguage.value
    val selectedLabel = TranslatorManager.languages.firstOrNull { it.code == selectedCode }?.label ?: "تلقائي"

    LaunchedEffect(Unit) {
        TranslatorManager.initialize(context)
    }

    Box(modifier = Modifier.padding(vertical = 4.dp)) {
        OutlinedButton(onClick = { expanded = true }) {
            Text("لغة الترجمة: $selectedLabel")
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            TranslatorManager.languages.forEach { option ->
                DropdownMenuItem(
                    text = { Text(option.label) },
                    onClick = {
                        TranslatorManager.setTargetLanguage(context, option.code)
                        expanded = false
                    }
                )
            }
        }
    }
}
'''
    with open(MAIN_SCREEN, "w", encoding="utf-8", newline="\n") as f:
        f.write(screen)

print(">> Safe Translator Patch applied successfully! Voice is now always Auto.")
import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_VM = PKG_DIR + "/viewmodel/MainViewModel.kt"
SPEECH_MGR = PKG_DIR + "/speech/SpeechRecognizerManager.kt"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"

PROBLEMS = []


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def replace_once(file_path, old, new, what):
    """Replace exactly one occurrence. Unlike v1 it NEVER fails silently."""
    if not os.path.exists(file_path):
        PROBLEMS.append(f"{what}: file not found: {file_path}")
        return False
    content = read(file_path)
    if new in content:
        print(f"-- {what}: already applied")
        return True
    n = content.count(old)
    if n != 1:
        PROBLEMS.append(f"{what}: anchor found {n} times in {file_path} (expected 1)")
        return False
    write(file_path, content.replace(old, new, 1))
    print(f"OK {what}")
    return True


print(">> Applying Smart Translator Patch v2 (voice always Auto, loud failures)...")

# 1) TranslatorManager.kt
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
write(PKG_DIR + "/data/TranslatorManager.kt", translator_mgr_code)
print("OK TranslatorManager.kt written")

# 2) MainViewModel.kt : replace legacy translator block
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

        // إذا كان الكلام صوتياً نتجاهل الزر ونستخدم "تلقائي" دائماً
        val targetCode = if (typing) {
            com.zevorix.assistant.data.TranslatorManager.targetLanguage.value
        } else {
            "auto"
        }

        // لغة النطق/العرض للترجمة: عكس لغة الكلام (عربي -> إنجليزي، وغير ذلك -> عربي)
        val outLang = if (!typing) {
            if (AppLanguage.detect(source) == AppLanguage.ARABIC) AppLanguage.ENGLISH else AppLanguage.ARABIC
        } else lang

        val cached = com.zevorix.assistant.data.TranslatorManager.getCached(source, targetCode)
        if (cached != null) {
            if (!typing) reply(cached, outLang, speak = speak)
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
                    reply(translated, outLang, speak = speak)
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

if not os.path.exists(MAIN_VM):
    PROBLEMS.append(f"MainViewModel: file not found: {MAIN_VM}")
else:
    vm = read(MAIN_VM)
    legacy = re.compile(
        r"    // ---------------- Translator mode ----------------.*?(?=    // ---------------- Screen recording by voice ----------------)",
        re.DOTALL,
    )
    if "Advanced Translator Mode" in vm:
        print("-- MainViewModel translator block: already applied")
    elif legacy.search(vm):
        write(MAIN_VM, legacy.sub(lambda m: new_vm_code, vm))
        print("OK MainViewModel translator block replaced")
    else:
        PROBLEMS.append("MainViewModel: legacy '// ---- Translator mode ----' block not found (markers changed?)")

replace_once(MAIN_VM, "handleTranslation(text, lang, speak)", "handleTranslation(parsed, text, lang, speak)",
             "handleTranslation call site")

# 3) SpeechRecognizerManager.kt : multi-language recognition
ANCHOR = 'putExtra("android.speech.extra.EXTRA_ADDITIONAL_LANGUAGES", arrayOf(extraLanguageTag))'
SPEECH_NEW = (
    ANCHOR + '\n'
    '                val bothLanguages = arrayListOf("ar-SA", "en-US", "fr-FR", "es-ES", "tr-TR", "de-DE")\n'
    '                if (android.os.Build.VERSION.SDK_INT >= 33) {\n'
    '                    putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_DETECTION, true)\n'
    '                    putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES, bothLanguages)\n'
    '                }\n'
    '                if (android.os.Build.VERSION.SDK_INT >= 34) {\n'
    '                    putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_SWITCH, RecognizerIntent.LANGUAGE_SWITCH_BALANCED)\n'
    '                    putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_SWITCH_ALLOWED_LANGUAGES, bothLanguages)\n'
    '                }'
)
if os.path.exists(SPEECH_MGR) and "EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES" in read(SPEECH_MGR):
    print("-- SpeechRecognizerManager: already applied")
else:
    replace_once(SPEECH_MGR, ANCHOR, SPEECH_NEW, "SpeechRecognizerManager multi-language")

# 4) MainScreen.kt : language selector
if not os.path.exists(MAIN_SCREEN):
    PROBLEMS.append(f"MainScreen: file not found: {MAIN_SCREEN}")
else:
    screen = read(MAIN_SCREEN)
    if "TranslatorLanguageSelector" in screen:
        print("-- MainScreen selector: already applied")
    else:
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

        _a = "    val state by viewModel.uiState.collectAsStateWithLifecycle()\n"
        if "isTranslatorOn" not in screen and screen.count(_a) >= 1:
            screen = screen.replace(_a, _a + "    val isTranslatorOn by viewModel.translatorMode.collectAsStateWithLifecycle()\n", 1)
        else:
            PROBLEMS.append("MainScreen: 'val state by viewModel.uiState...' anchor not found")

        _b = re.search(r"([ \t]*)if \(!typing\) \{\n", screen)
        if _b and "TranslatorLanguageSelector()" not in screen:
            _ind = _b.group(1)
            screen = (screen[:_b.end()] + _ind + "    if (isTranslatorOn) {\n" + _ind
                      + "        TranslatorLanguageSelector()\n" + _ind + "    }\n" + screen[_b.end():])
        else:
            PROBLEMS.append("MainScreen: 'if (!typing) {' anchor not found")

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
        write(MAIN_SCREEN, screen)
        print("OK MainScreen selector added")

# ---------------------------------------------------------------------------
# 5) Verification + diagnostics for the "language lock" bug
# ---------------------------------------------------------------------------
print("\n>> Verifying...")


def has(path, needle):
    return os.path.exists(path) and needle in read(path)


if not has(MAIN_VM, "Advanced Translator Mode"):
    PROBLEMS.append("VERIFY: MainViewModel still has the OLD translator block")
if not has(MAIN_VM, "handleTranslation(parsed, text, lang, speak)"):
    PROBLEMS.append("VERIFY: handleTranslation call site not updated (build will fail)")
if not has(SPEECH_MGR, "EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES"):
    PROBLEMS.append("VERIFY: recognizer has NO multi-language config -> it stays locked to ONE language")
if not has(MAIN_SCREEN, "TranslatorLanguageSelector()"):
    PROBLEMS.append("VERIFY: selector not shown in MainScreen")

print("\n>> Language-lock suspects (send me these lines if the bug persists):")
pat = re.compile(r"translatorPrimary|extraLanguageTag|RecognizerIntent\.EXTRA_LANGUAGE\b|EXTRA_LANGUAGE,|setLanguage\(|\.language\s*=")
for path in (MAIN_VM, SPEECH_MGR):
    if not os.path.exists(path):
        continue
    for i, line in enumerate(read(path).splitlines(), 1):
        if pat.search(line):
            print(f"   {os.path.basename(path)}:{i}: {line.strip()}")

if PROBLEMS:
    print("\n!! PROBLEMS:")
    for p in PROBLEMS:
        print("   -", p)
else:
    print("\n>> Translator Patch v2 applied with no problems.")

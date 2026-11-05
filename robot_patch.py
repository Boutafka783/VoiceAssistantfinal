import os
import re

ROOT = os.environ.get("PROJECT_DIR", ".")
PKG_DIR = os.path.join(ROOT, "app", "src", "main", "java", "com", "example", "voiceassistant")
MAIN_SCREEN = os.path.join(PKG_DIR, "ui", "MainScreen.kt")
MANIFEST = os.path.join(ROOT, "app", "src", "main", "AndroidManifest.xml")
ROBOT_ACTIVITY_PATH = os.path.join(PKG_DIR, "RobotStudioActivity.kt")

# ==============================================================================
# 1. RobotStudioActivity.kt
#    ملف واحد مستقل: يحمل داخله كل أصول مختبر الروبوتات V21
#    (robot_lab.html + مكتبات JS + CSS) مضغوطة ZIP ومشفّرة Base64،
#    ويفكّها عند أول تشغيل إلى filesDir/robot_lab. لا حاجة لنسخ أي ملفات إلى assets.
# ==============================================================================
ROBOT_ACTIVITY_KT = r'''package com.example.voiceassistant

import android.annotation.SuppressLint
import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import com.example.voiceassistant.speech.SpeechRecognizerManager
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import com.example.voiceassistant.data.LicenseManager
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.ByteArrayInputStream
import java.io.File
import java.util.concurrent.TimeUnit
import java.util.zip.ZipInputStream

/**
 * مختبر الروبوتات V21 (Robot Studio).
 *
 * ملف واحد مستقل: يحمل داخله كل أصول المختبر (robot_lab.html + مكتبات JS + CSS)
 * مضغوطة (ZIP) ومشفّرة Base64، ويفكّها عند أول تشغيل (أو عند تغيّر النسخة) إلى
 * filesDir/robot_lab ثم يفتحها في WebView. لا حاجة لنسخ أي ملفات إلى assets.
 *
 * الجسر "Android" مطابق لجسر MechSimulatorActivity:
 *   close / saveImage / startVoice / stopVoice / askAi
 *
 * ملف مُولَّد آلياً بواسطة build_robot_studio_activity.py — لا تعدّل كتلة RobotLabBundle
 * يدوياً؛ عدّل الأصول ثم أعد التوليد.
 */
class RobotStudioActivity : ComponentActivity() {
    private var web: WebView? = null

    private val client: OkHttpClient by lazy {
        OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(70, TimeUnit.SECONDS)
            .build()
    }

    private var activeSpeech: SpeechRecognizerManager? = null
    private var pendingVoiceId: String? = null

    private val micPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            if (granted) beginRecognition()
            else deliverVoice(false, "permission_denied")
        }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WebView.setWebContentsDebuggingEnabled(true)
        val wv = WebView(this)
        wv.settings.javaScriptEnabled = true
        wv.settings.domStorageEnabled = true
        wv.settings.allowFileAccess = true
        wv.settings.allowFileAccessFromFileURLs = true
        wv.settings.allowUniversalAccessFromFileURLs = true
        wv.settings.useWideViewPort = true
        wv.settings.loadWithOverviewMode = true
        wv.settings.builtInZoomControls = false
        wv.settings.displayZoomControls = false
        wv.settings.setRenderPriority(android.webkit.WebSettings.RenderPriority.HIGH)
        wv.setLayerType(WebView.LAYER_TYPE_HARDWARE, null)
        wv.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                view?.evaluateJavascript(LAYOUT_FIX_JS, null)
            }
        }
        wv.addJavascriptInterface(Bridge(), "Android")
        web = wv
        setContentView(wv)
        wv.loadUrl(resolveEntryUrl())

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() { finish() }
        })
    }

    /** الأصول المدمجة أولاً؛ وإن فشل فكّها نرجع إلى assets/robot_lab (نسخة robot_patch.py). */
    private fun resolveEntryUrl(): String {
        return try {
            val dir = RobotLabBundle.prepare(this)
            "file://" + File(dir, RobotLabBundle.ENTRY).absolutePath
        } catch (e: Exception) {
            "file:///android_asset/robot_lab/" + RobotLabBundle.ENTRY
        }
    }

    override fun onDestroy() {
        web?.removeJavascriptInterface("Android")
        web?.destroy()
        web = null
        activeSpeech?.destroy()
        activeSpeech = null
        super.onDestroy()
    }

    private fun beginRecognition() {
        if (pendingVoiceId == null) return
        val speech = SpeechRecognizerManager(this)
        speech.listener = object : SpeechRecognizerManager.Listener {
            override fun onReady() {}
            override fun onPartial(text: String) {}
            override fun onResult(text: String) { deliverVoice(true, text) }
            override fun onError(code: Int) { deliverVoice(false, "error_$code") }
            override fun onEnd() {}
        }
        speech.start(if ((getSharedPreferences("app_lang", MODE_PRIVATE).getString("lang", "ar") ?: "ar") == "ar") "ar-SA" else "en-US")
        activeSpeech = speech
    }

    private fun deliverVoice(ok: Boolean, text: String) {
        val id = pendingVoiceId ?: return
        pendingVoiceId = null
        activeSpeech?.destroy()
        activeSpeech = null
        runOnUiThread {
            web?.evaluateJavascript(
                "window.onVoiceResult(${JSONObject.quote(id)}, $ok, ${JSONObject.quote(text)})",
                null
            )
        }
    }

    private fun deliver(id: String, ok: Boolean, text: String) {
        runOnUiThread {
            web?.evaluateJavascript(
                "window.onAiResult(${JSONObject.quote(id)}, $ok, ${JSONObject.quote(text)})",
                null
            )
        }
    }

    private fun deliverSaved(ok: Boolean, msg: String) {
        runOnUiThread {
            web?.evaluateJavascript("window.onImageSaved($ok, ${JSONObject.quote(msg)})", null)
        }
    }

    inner class Bridge {
        @JavascriptInterface
        fun close() { runOnUiThread { finish() } }

        @JavascriptInterface
        fun saveImage(dataUrl: String, name: String) {
            Thread {
                try {
                    val bytes = android.util.Base64.decode(dataUrl.substringAfter("base64,"), android.util.Base64.DEFAULT)
                    val fileName = name.replace(Regex("[^A-Za-z0-9_]"), "_") + ".png"
                    val savedPath: String
                    if (android.os.Build.VERSION.SDK_INT >= 29) {
                        val values = android.content.ContentValues().apply {
                            put(android.provider.MediaStore.Images.Media.DISPLAY_NAME, fileName)
                            put(android.provider.MediaStore.Images.Media.MIME_TYPE, "image/png")
                            put(android.provider.MediaStore.Images.Media.RELATIVE_PATH, "Pictures/RobotLab")
                        }
                        val uri = contentResolver.insert(android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)
                            ?: throw java.io.IOException("MediaStore insert failed")
                        contentResolver.openOutputStream(uri)?.use { it.write(bytes) }
                        savedPath = "Pictures/RobotLab/$fileName"
                    } else {
                        val dir = getExternalFilesDir(android.os.Environment.DIRECTORY_PICTURES) ?: filesDir
                        val f = java.io.File(dir, fileName)
                        f.writeBytes(bytes)
                        savedPath = f.absolutePath
                    }
                    deliverSaved(true, savedPath)
                } catch (e: Exception) {
                    deliverSaved(false, e.message ?: "error")
                }
            }.start()
        }

        @JavascriptInterface
        fun startVoice(requestId: String) {
            runOnUiThread {
                if (pendingVoiceId != null) {
                    deliverVoice(false, "busy")
                    return@runOnUiThread
                }
                pendingVoiceId = requestId
                if (ContextCompat.checkSelfPermission(
                        this@RobotStudioActivity, Manifest.permission.RECORD_AUDIO
                    ) == PackageManager.PERMISSION_GRANTED) {
                    beginRecognition()
                } else {
                    micPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
                }
            }
        }

        @JavascriptInterface
        fun stopVoice() {
            runOnUiThread {
                activeSpeech?.cancel()
                activeSpeech?.destroy()
                activeSpeech = null
                val id = pendingVoiceId ?: return@runOnUiThread
                pendingVoiceId = null
                web?.evaluateJavascript(
                    "window.onVoiceResult(${JSONObject.quote(id)}, false, \"cancelled\")",
                    null
                )
            }
        }

        @JavascriptInterface
        fun askAi(id: String, mode: String, payload: String) {
            Thread {
                try {
                    val base = BuildConfig.VIDEO_SERVER_URL.trim()
                        .replace("/api/generate-video", "")
                        .removeSuffix("/api")
                        .trimEnd('/')
                    val key = LicenseManager.getBackendKey()
                    val body = JSONObject()
                        .put("licenseKey", key)
                        .put("mode", mode)
                        .put("prompt", payload)
                        .put("cost", 1)
                    val req = Request.Builder()
                        .url("$base/api/ai/circuit")
                        .post(body.toString().toRequestBody("application/json".toMediaType()))
                        .build()
                    client.newCall(req).execute().use { r ->
                        val raw = r.body?.string() ?: "{}"
                        val json = try { JSONObject(raw) } catch (e: Exception) { null }
                        val text = json?.optString("text", "") ?: ""
                        if (r.isSuccessful && text.isNotEmpty()) {
                            deliver(id, true, text)
                        } else {
                            val err = json?.optString("error", "") ?: ""
                            deliver(id, false, if (err.isNotEmpty()) err else "HTTP ${r.code}")
                        }
                    }
                } catch (e: Exception) {
                    deliver(id, false, "Network Error")
                }
            }.start()
        }
    }

    companion object {
        private val LAYOUT_FIX_JS: String = """
            (function() {
                if (window.__zsDockInstalled) return;
                window.__zsDockInstalled = true;

                var GREEN = '#00ff66', RED = '#ff4444';
                var logs = [];
                var box = null;
                var timer = null;
                var docked = false;
                var MOVE_TO_BODY = true; // يحمي الـ Canvas من أي transform في العناصر الأب

                // ===== شاشة التصحيح (أسفل الشاشة) =====
                function makeBox() {
                    if (box) return;
                    box = document.createElement('div');
                    box.id = '__zs_debug_box';
                    box.style.cssText =
                        'position:fixed;bottom:0;left:0;right:0;z-index:2147483647;max-height:30vh;' +
                        'overflow:hidden;background:rgba(0,0,0,0.8);padding:3px 5px;margin:0;' +
                        'font:10px/1.3 monospace;color:#00ff66;white-space:pre-wrap;word-break:break-all;' +
                        'pointer-events:none;direction:ltr;text-align:left;';
                    document.documentElement.appendChild(box);
                }

                function render() {
                    makeBox();
                    box.textContent = '';
                    for (var i = 0; i < logs.length; i++) {
                        var d = document.createElement('div');
                        d.style.color = logs[i].c;
                        d.textContent = logs[i].m;
                        box.appendChild(d);
                    }
                }

                function log(msg, color) {
                    logs.push({ m: String(msg), c: color || GREEN });
                    if (logs.length > 12) logs.shift();
                    try { render(); } catch (e) {}
                }

                // ===== التقاط الأخطاء (باللون الأحمر) =====
                var prevOnError = window.onerror;
                window.onerror = function(msg, src, line) {
                    log('ERR: ' + msg + ' @' + String(src || '').split('/').pop() + ':' + line, RED);
                    if (typeof prevOnError === 'function') {
                        try { return prevOnError.apply(this, arguments); } catch (e) {}
                    }
                    return false;
                };
                window.addEventListener('unhandledrejection', function(ev) {
                    var r = ev && ev.reason;
                    log('PROMISE: ' + (r && r.message ? r.message : r), RED);
                });
                try {
                    var origConsoleError = console.error;
                    console.error = function() {
                        try {
                            log('console.error: ' + Array.prototype.slice.call(arguments).join(' ').slice(0, 160), RED);
                        } catch (e) {}
                        return origConsoleError.apply(console, arguments);
                    };
                } catch (e) {}

                // ===== الأدوات =====
                function setS(el, props) {
                    for (var k in props) {
                        el.style.setProperty(k, props[k], 'important');
                    }
                }

                function ensureViewport() {
                    if (document.querySelector('meta[name="viewport"]')) return;
                    var m = document.createElement('meta');
                    m.name = 'viewport';
                    m.content = 'width=device-width, initial-scale=1, maximum-scale=1';
                    (document.head || document.documentElement).appendChild(m);
                }

                function fireResize() {
                    try { window.dispatchEvent(new Event('resize')); } catch (e) {}
                }

                function isDocked(cv) {
                    var cs = window.getComputedStyle(cv);
                    return cs.position === 'fixed' && cs.zIndex === '9999';
                }

                // ===== تثبيت الـ Canvas في الأعلى =====
                function dock() {
                    try {
                        var cv = document.getElementById('cv');
                        if (!cv || !document.body) return false;

                        ensureViewport();

                        setS(document.documentElement, {
                            margin: '0', padding: '0', height: 'auto', 'overflow-y': 'auto'
                        });

                        setS(document.body, {
                            'padding-top': '45vh',
                            margin: '0',
                            'overflow-y': 'auto',
                            display: 'block',
                            height: 'auto',
                            'box-sizing': 'border-box'
                        });

                        if (MOVE_TO_BODY && cv.parentElement !== document.body) {
                            document.body.insertBefore(cv, document.body.firstChild);
                        }

                        setS(cv, {
                            position: 'fixed',
                            top: '0',
                            left: '0',
                            right: 'auto',
                            bottom: 'auto',
                            width: '100vw',
                            height: '45vh',
                            'max-width': '100vw',
                            'z-index': '9999',
                            'background-color': '#0d1117',
                            display: 'block',
                            margin: '0'
                        });

                        if (!docked) {
                            docked = true;
                            log('Canvas Docked Successfully', GREEN);
                        }
                        return true;
                    } catch (e) {
                        log('dock error: ' + e.message, RED);
                        return false;
                    }
                }

                function applyAll() {
                    dock();
                    fireResize();
                }

                function schedule() {
                    clearTimeout(timer);
                    timer = setTimeout(function() {
                        var cv = document.getElementById('cv');
                        if (cv && !isDocked(cv)) applyAll();
                    }, 120);
                }

                // ===== التنفيذ =====
                dock();
                setTimeout(applyAll, 100);
                setTimeout(applyAll, 500);
                setTimeout(applyAll, 1500);
                setTimeout(function() {
                    var cv = document.getElementById('cv');
                    if (!cv) {
                        log('Canvas #cv NOT FOUND', RED);
                    } else {
                        var r = cv.getBoundingClientRect();
                        log('cv rect=' + Math.round(r.width) + 'x' + Math.round(r.height), GREEN);
                    }
                }, 2500);

                // ===== مراقبة البناء المتأخر وإعادة كتابة التنسيق =====
                try {
                    new MutationObserver(schedule).observe(document.documentElement, {
                        childList: true,
                        subtree: true,
                        attributes: true,
                        attributeFilter: ['style', 'class']
                    });
                } catch (e) {}

                window.addEventListener('orientationchange', function() { setTimeout(applyAll, 300); });
            })();
        """.trimIndent()
    }
}

/**
 * الأصول المدمجة (ZIP + Base64). الملفات: robot_lab.html, mech_style.css, robot_parts.js, robot_physics.js, robot_kinematics.js, mech_core.js, robot_studio.js, quadruped_balance.js, terrain_lab.js, terrain_contact.js, footstep_planner.js, robot_path_planner.js, robot_sensors.js, environment_map.js, robot_localization.js, robot_autonomy.js, robot_task_executor.js, quadruped_gait.js, robot_kinematics_ui.js
 */
private object RobotLabBundle {
    const val ENTRY = "robot_lab.html"
    private const val VERSION = "b14924a93f7d"

    fun prepare(ctx: Context): File {
        val dir = File(ctx.filesDir, "robot_lab")
        val marker = File(dir, ".version")
        if (marker.exists() && marker.readText() == VERSION && File(dir, ENTRY).exists()) return dir
        dir.deleteRecursively()
        dir.mkdirs()
        val bytes = android.util.Base64.decode(DATA.joinToString(""), android.util.Base64.DEFAULT)
        ZipInputStream(ByteArrayInputStream(bytes)).use { zin ->
            var entry = zin.nextEntry
            while (entry != null) {
                if (!entry.isDirectory) {
                    val flat = File(entry.name).name          // اسم مسطح: يمنع الخروج من المجلد
                    File(dir, flat).outputStream().use { out -> zin.copyTo(out) }
                }
                entry = zin.nextEntry
            }
        }
        marker.writeText(VERSION)
        return dir
    }

    private val DATA = arrayOf(
        "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"
    )
}
'''

# ==============================================================================
# 2. تعديل MainScreen.kt و AndroidManifest.xml
#    الفكرة: نستنسخ عنصراً موجوداً فعلاً (المختبر الميكانيكي، وإن لم يوجد
#    فمختبر الإلكترونيات) بكل متغيراته، ونستبدل الاسم والـ Activity،
#    فلا نفترض أسماء متغيرات غير موجودة.
# ==============================================================================
ELEC_AR = "مختبر الإلكترونيات"
ELEC_EN = "Electronics Lab"
MECH_AR = "المختبر الميكانيكي"
MECH_EN = "Mechanical Lab"
ROBOT_AR = "مختبر الروبوتات"
ROBOT_EN = "Robot Lab"

# (الاسم العربي، الاسم الإنجليزي، اسم الـ Activity) بترتيب الأفضلية للاستنساخ
SOURCES = [
    (MECH_AR, MECH_EN, "MechSimulatorActivity"),
    (ELEC_AR, ELEC_EN, "CircuitSimulatorActivity"),
]

DEFAULT_ACTIVITY_BLOCK = (
    '        <activity\n'
    '            android:name=".RobotStudioActivity"\n'
    '            android:exported="false"\n'
    '            android:theme="@style/Theme.VoiceAssistant" />\n'
)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def find_matching_paren(s, i):
    """i = فهرس '(' ، يرجع فهرس ')' المقابل مع تجاهل النصوص بين علامتي اقتباس."""
    depth = 0
    in_str = False
    j = i
    n = len(s)
    while j < n:
        c = s[j]
        if in_str:
            if c == "\\":
                j += 2
                continue
            if c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return j
        j += 1
    return -1


def patch_main_screen():
    if not os.path.isfile(MAIN_SCREEN):
        print("   ! MainScreen.kt غير موجود:", MAIN_SCREEN)
        return
    text = read_file(MAIN_SCREEN)
    if "RobotStudioActivity" in text:
        print("   = MainScreen.kt (الزر موجود مسبقاً)")
        return

    for src_ar, src_en, src_act in SOURCES:
        pos = text.find(src_ar)
        if pos < 0:
            pos = text.find(src_en)
        if pos < 0:
            continue

        start = text.rfind("DropdownMenuItem(", 0, pos)
        if start < 0 or pos - start > 1000:
            continue

        end = find_matching_paren(text, start + len("DropdownMenuItem"))
        if end < 0:
            continue

        block = text[start:end + 1]
        if src_act not in block:
            continue

        new_block = (block.replace(src_ar, ROBOT_AR)
                          .replace(src_en, ROBOT_EN)
                          .replace(src_act, "RobotStudioActivity"))
        new_block = re.sub(r"Icons\.(Filled|Default)\.[A-Za-z]+", "Icons.Filled.Build", new_block)

        line_start = text.rfind("\n", 0, start) + 1
        indent = re.match(r"[ \t]*", text[line_start:]).group(0)
        text = text[:end + 1] + "\n" + indent + new_block + text[end + 1:]

        if "Icons.Filled.Build" in new_block and "import androidx.compose.material.icons.filled.Build" not in text:
            m = re.search(r"^import .*$", text, re.M)
            if m:
                text = text[:m.start()] + "import androidx.compose.material.icons.filled.Build\n" + text[m.start():]

        write_file(MAIN_SCREEN, text)
        print("   + MainScreen.kt (تمت إضافة زر مختبر الروبوتات، استُنسخ من %s)" % src_ar)
        return

    print("   ! MainScreen.kt: لم أجد عنصراً قابلاً للاستنساخ (المختبر الميكانيكي / الإلكترونيات) - أضف الزر يدوياً")


def patch_manifest():
    if not os.path.isfile(MANIFEST):
        print("   ! AndroidManifest.xml غير موجود:", MANIFEST)
        return
    text = read_file(MANIFEST)
    if "RobotStudioActivity" in text:
        print("   = AndroidManifest.xml (النشاط مسجل مسبقاً)")
        return

    for _, _, src_act in SOURCES:
        anchor = text.find(src_act)
        if anchor < 0:
            continue
        tag_start = text.rfind("<activity", 0, anchor)
        tag_end = text.find(">", anchor)
        if tag_start < 0 or tag_end < 0:
            continue
        if text[tag_end - 1] == "/":
            block_end = tag_end + 1
        else:
            close = text.find("</activity>", tag_end)
            block_end = close + len("</activity>") if close >= 0 else -1
        if block_end > 0:
            block = text[tag_start:block_end]
            new_block = block.replace(src_act, "RobotStudioActivity")
            line_start = text.rfind("\n", 0, tag_start) + 1
            indent = re.match(r"[ \t]*", text[line_start:]).group(0)
            text = text[:block_end] + "\n" + indent + new_block + text[block_end:]
            write_file(MANIFEST, text)
            print("   + AndroidManifest.xml (تم تسجيل النشاط)")
            return

    close_app = text.find("</application>")
    if close_app >= 0:
        text = text[:close_app] + DEFAULT_ACTIVITY_BLOCK + "    " + text[close_app:]
        write_file(MANIFEST, text)
        print("   + AndroidManifest.xml (تم تسجيل النشاط قبل </application>)")
    else:
        print("   ! AndroidManifest.xml: لم أجد </application> - سجّل النشاط يدوياً")


def main():
    print(">> ROBOT LAB V21 applied: self-contained RobotStudioActivity (embedded assets)")
    os.makedirs(PKG_DIR, exist_ok=True)
    write_file(ROBOT_ACTIVITY_PATH, ROBOT_ACTIVITY_KT)
    print("   + RobotStudioActivity.kt")
    patch_main_screen()
    patch_manifest()


if __name__ == "__main__":
    main()

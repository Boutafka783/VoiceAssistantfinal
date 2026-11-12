#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
local_ai_patch.py
-----------------
Adds on-device AI (MediaPipe LLM Inference + Gemma2-2B) alongside the cloud AI.
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
MARK = "/*LOCAL_AI*/"
HTML_MARK = "<!--LOCAL_AI-->"

# ---- Configuration --------------------------------------------------------
MEDIAPIPE_DEP = 'implementation("com.google.mediapipe:tasks-genai:0.10.22")'

# اسم الملف والرابط المباشر؛ مستودع Hugging Face يعرض الملف فعلياً بامتداد .bin.
MODEL_NAME = "gemma2-2b-it-int8-web.task.bin"
MODEL_URL = "https://huggingface.co/litert-community/Gemma2-2B-IT/resolve/main/gemma2-2b-it-int8-web.task.bin"


DEFAULT_BRIDGE_NAME = "Android"
# نضيف نشاط الروبوت كي يُحقن الجسر عند التشغيل الثاني بعد توليده وتعديله.
ACTIVITY_FILES = [
    "CircuitSimulatorActivity.kt",
    "MechSimulatorActivity.kt",
    "RobotStudioActivity.kt",
    "ArchitectureActivity.kt",
    "FlightSimActivity.kt",
]
# نعدّل مصدر ورشة الروبوتات قبل ضغطه داخل RobotStudioActivity.kt.
HTML_FILES = [
    "circuit_sim.html",
    "mech_sim.html",
    "robot_lab.html",
    "architecture_lab.html",
    "flight_sim.html",
]
SKIP_DIRS = {".git", "build", ".gradle", "node_modules", ".idea"}

LOG = []
FAILED = []

def log(status, msg):
    LOG.append((status, msg))
    print("[%s] %s" % (status, msg))

def find_files(name):
    out = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        if name in files:
            out.append(os.path.join(d, name))
    return out

def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def write(p, s):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)

def rel(p):
    return os.path.relpath(p, ROOT)

def _matching_brace(text, open_pos):
    """إيجاد قوس الإغلاق لكتلة Gradle مع تجاهل الأقواس داخل السلاسل."""
    depth = 0
    quote = None
    escaped = False
    for i in range(open_pos, len(text)):
        c = text[i]
        if quote:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == quote:
                quote = None
            continue
        if c in ("'", '"'):
            quote = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _ensure_gradle_block(text, block_name, body):
    """إضافة كتلة Gradle داخل android أو إنشاءها إن كانت غائبة."""
    m = re.search(r"\b" + re.escape(block_name) + r"\s*\{", text)
    if not m:
        return text + "\n\n" + block_name + " {\n" + body + "\n}\n"
    open_pos = text.find("{", m.start())
    close_pos = _matching_brace(text, open_pos)
    if close_pos < 0:
        raise ValueError("كتلة Gradle غير مكتملة: " + block_name)
    return text[:close_pos] + "\n" + body + "\n" + text[close_pos:]


def patch_gradle():
    # نضيف MediaPipe ونحذف أي أثر قديم لـ HF_TOKEN من نسخ سابقة.
    # لا نلمس buildFeatures لأنه خاص بمشروع المستخدم ويحتاجه BuildConfig.VIDEO_SERVER_URL.
    app_dir = os.path.join(ROOT, "app")
    targets = [os.path.join(app_dir, n) for n in ("build.gradle.kts", "build.gradle")
               if os.path.isfile(os.path.join(app_dir, n))]
    if not targets:
        FAILED.append("gradle")
        log("FAIL", "app/build.gradle.kts not found!")
        return

    for p in targets:
        s = read(p)
        if "com.google.mediapipe:tasks-genai" not in s:
            m = re.search(r"^dependencies\s*\{", s, re.M)
            if m:
                s = s[:m.end()] + "\n    " + MARK + " " + MEDIAPIPE_DEP + "\n" + s[m.end():]
            else:
                s += "\n\ndependencies {\n    " + MARK + " " + MEDIAPIPE_DEP + "\n}\n"

        # تنظيف إعدادات التوكن التي أضافتها الإصدارات السابقة من هذا السكربت.
        s = re.sub(
            r"(?m)^[ \t]*// LOCAL_AI_HF_TOKEN[ \t]*\n"
            r"[ \t]*buildConfigField\s*(?:\(\s*)?[\"']String[\"']\s*,\s*[\"']HF_TOKEN[\"'][^\n]*\n?",
            "", s,
        )
        write(p, s)
        log("OK", "MediaPipe configured; app token configuration removed in %s" % rel(p))

def patch_manifest():
    for p in find_files("AndroidManifest.xml"):
        s = read(p)
        if "</application>" in s and HTML_MARK not in s:
            tag = ('    %s<uses-native-library android:name="libOpenCL.so" android:required="false"/>\n' % HTML_MARK)
            s = s.replace("</application>", tag + "</application>", 1)
            write(p, s)
            log("OK", "OpenCL native-library declared in %s" % rel(p))

KT_MANAGER = r'''package __PKG__

__MARK__
import android.content.Context
import com.google.mediapipe.tasks.genai.llminference.LlmInference
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL

object LocalAiManager {
    const val MODEL_NAME = "__MODEL_NAME__"
    @Volatile var modelUrl: String = "__MODEL_URL__"
    private var appContext: Context? = null
    @Volatile private var llm: LlmInference? = null

    fun init(context: Context) { if (appContext == null) appContext = context.applicationContext }
    private fun ctx(): Context = appContext ?: throw IllegalStateException("LocalAiManager.init(context) was not called")
    fun modelFile(): File = File(ctx().filesDir, MODEL_NAME)
    fun isModelReady(): Boolean = modelFile().let { it.exists() && it.length() > 100_000_000L }

    @Synchronized
    fun downloadModel(onProgress: ((Int) -> Unit)? = null): Boolean {
        if (isModelReady()) return true
        val target = modelFile()
        val part = File(target.parentFile, "$MODEL_NAME.part")
        var conn: HttpURLConnection? = null
        try {
            var url = URL(modelUrl)
            var redirects = 0
            while (true) {
                conn = (url.openConnection() as HttpURLConnection).apply {
                    connectTimeout = 30_000; readTimeout = 60_000; instanceFollowRedirects = false
                }
                val code = conn.responseCode
                if (code in 300..399 && redirects < 8) {
                    val loc = conn.getHeaderField("Location") ?: break
                    url = URL(url, loc); conn.disconnect(); redirects++; continue
                }
                if (code != HttpURLConnection.HTTP_OK) throw RuntimeException("Model download failed: HTTP $code")
                break
            }
            val total = conn!!.contentLengthLong
            var done = 0L; var lastPct = -1
            conn.inputStream.use { input ->
                FileOutputStream(part).use { out ->
                    val buf = ByteArray(256 * 1024)
                    while (true) {
                        val n = input.read(buf); if (n < 0) break
                        out.write(buf, 0, n); done += n
                        if (total > 0) {
                            val pct = (done * 100 / total).toInt()
                            if (pct != lastPct) { lastPct = pct; onProgress?.invoke(pct) }
                        }
                    }
                }
            }
            if (target.exists()) target.delete()
            if (!part.renameTo(target)) throw RuntimeException("Could not move model into place")
            return true
        } catch (e: Throwable) { part.delete(); throw e } finally { conn?.disconnect() }
    }

    @Synchronized
    private fun engine(): LlmInference {
        llm?.let { return it }
        if (!isModelReady()) throw IllegalStateException("Model file is missing.")
        val options = LlmInference.LlmInferenceOptions.builder()
            .setModelPath(modelFile().absolutePath).setMaxTokens(1024).build()
        val created = LlmInference.createFromOptions(ctx(), options)
        llm = created; return created
    }

    fun generateResponse(prompt: String): String {
        val formatted = "<start_of_turn>user\n$prompt<end_of_turn>\n<start_of_turn>model\n"
        return engine().generateResponse(formatted)
    }
}
'''

def package_of(kt_text):
    m = re.search(r"^\s*package\s+([\w.]+)", kt_text, re.M)
    return m.group(1) if m else None

def create_manager(pkg, directory):
    path = os.path.join(directory, "LocalAiManager.kt")
    if os.path.exists(path) and MARK in read(path):
        # ترقية الملف القديم: حذف أي اعتماد سابق على التوكن أو ترويسة Authorization.
        existing = read(path)
        migrated = re.sub(
            r"(?m)^\s*@Volatile\s+var\s+authToken:\s*String\s*=.*\n", "", existing
        )
        migrated = re.sub(
            r"(?m)^\s*if\s*\(authToken\.isNotEmpty\(\)\)\s*setRequestProperty\(.*\n", "", migrated
        )
        if migrated != existing:
            write(path, migrated)
            log("OK", "removed embedded token handling from %s" % rel(path))
        return path

    code = (KT_MANAGER.replace("__PKG__", pkg)
            .replace("__MARK__", MARK)
            .replace("__MODEL_NAME__", MODEL_NAME)
            .replace("__MODEL_URL__", MODEL_URL))

    write(path, code)
    log("OK", "created %s" % rel(path))
    return path

KT_BRIDGE = '''
    __MARK__
    @JavascriptInterface
    fun askLocalAi(requestId: String, prompt: String) {
        Thread {
            var ok = true
            val text: String = try {
                LocalAiManager.init(applicationContext)
                if (!LocalAiManager.isModelReady()) LocalAiManager.downloadModel()
                LocalAiManager.generateResponse(prompt)
            } catch (e: Throwable) {
                ok = false
                "Local AI error: " + (e.message ?: e.javaClass.simpleName)
            }
            val js = "window.onAiResult(" + org.json.JSONObject.quote(requestId) + "," + ok + "," + org.json.JSONObject.quote(text) + ")"
            runOnUiThread { __WV__?.evaluateJavascript(js, null) }
        }.start()
    }
'''

def detect_webview_name(s):
    m = re.search(r"(?:var|val)\s+(\w+)\s*(?::\s*WebView\??|=\s*WebView\(|=\s*findViewById<WebView>)", s)
    return m.group(1) if m else "webView"

def patch_activities(manager_pkg):
    for name in ACTIVITY_FILES:
        paths = find_files(name)
        for p in paths:
            s = read(p)
            if "askLocalAi" in s or MARK in s: continue
            m = re.search(r"inner\s+class\s+Bridge\b[^{]*\{", s)
            if not m:
                FAILED.append(name)
                continue
            wv = detect_webview_name(s)
            block = KT_BRIDGE.replace("__MARK__", MARK).replace("__WV__", wv)
            s = s[:m.end()] + block + s[m.end():]
            pkg = package_of(s)
            if pkg and manager_pkg and pkg != manager_pkg:
                imp = "import %s.LocalAiManager" % manager_pkg
                if imp not in s:
                    pm = re.search(r"^\s*package\s+[\w.]+\s*$", s, re.M)
                    s = s[:pm.end()] + "\n\n" + imp + s[pm.end():]
            if "import android.webkit.JavascriptInterface" not in s:
                pm = re.search(r"^\s*package\s+[\w.]+\s*$", s, re.M)
                if pm: s = s[:pm.end()] + "\n\nimport android.webkit.JavascriptInterface" + s[pm.end():]
            write(p, s)
            log("OK", "askLocalAi injected into %s" % rel(p))

HTML_BUTTON = ('<button id="btnAiMode" type="button" onclick="window.__aiToggle&&window.__aiToggle()" '
               'title="Local / Cloud" style="margin:0 4px;padding:6px 10px;border-radius:8px;'
               'border:1px solid #888;background:#222;color:#fff;font-size:13px;cursor:pointer">'
               '☁️ سحابي</button>' + HTML_MARK)

JS_BLOCK = r'''
<script>
__MARK__
(function () {
  var BR = '__BRIDGE__';
  var originalOnAiResult = window.onAiResult;
  var mode = 'cloud';
  try { mode = localStorage.getItem('ai_mode') || 'cloud'; } catch (e) {}

  function refresh() {
    var b = document.getElementById('btnAiMode');
    if (!b) return;
    b.textContent = mode === 'local' ? '📱 محلي' : '☁️ سحابي';
    b.setAttribute('aria-pressed', mode === 'local' ? 'true' : 'false');
  }
  
  window.__aiToggle = function () {
    mode = (mode === 'local') ? 'cloud' : 'local';
    try { localStorage.setItem('ai_mode', mode); } catch (e) {}
    refresh();
  };

  window.__aiRoute = function () {
    var a = Array.prototype.slice.call(arguments);
    var b = window[BR];
    if (mode === 'local' && b && typeof b.askLocalAi !== 'undefined') {
      var strs = a.map(function (x) { return String(x); });
      var prompt = strs.reduce(function (x, y) { return y.length > x.length ? y : x; }, '');
      var id = (a.length > 1 && strs[0] !== prompt) ? strs[0] : ('local_' + Date.now());
      return b.askLocalAi(id, prompt);
    }
    return b.askAi.apply(b, a);
  };

  window.onAiResult = function (id, ok, text) {
    if (originalOnAiResult) originalOnAiResult(id, ok, text);
    try { window.dispatchEvent(new CustomEvent('localai', { detail: { id: id, text: text, ok: ok } })); } catch (e) {}
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', refresh);
  else refresh();
})();
</script>
'''

def patch_html():
    for name in HTML_FILES:
        paths = find_files(name)
        for p in paths:
            s = read(p)
            if MARK in s or HTML_MARK in s: continue
            bridge = DEFAULT_BRIDGE_NAME
            mb = re.search(r"\b([A-Za-z_]\w*)\.askAi\s*\(", s)
            if mb: bridge = mb.group(1)
            # قبول Android.askAi و window.Android.askAi دون إنتاج window.window.__aiRoute.
            s, n_calls = re.subn(r"(?:window\.)?\b%s\.askAi\s*\(" % re.escape(bridge), "window.__aiRoute(", s)
            
            placed = False
            # نضع زر التبديل بجانب أحد أزرار كل مختبر، بما فيها أزرار ورشة الروبوتات.
            for bid in ("btnAskAi", "btnGen", "bAsk", "bAi", "aiGo", "ai-btn"):

                m = re.search(r"<button\b[^>]*\bid=[\"']%s[\"'][^>]*>.*?</button>" % bid, s, re.S | re.I)
                if m:
                    s = s[:m.end()] + HTML_BUTTON + s[m.end():]
                    placed = True
                    break
            if not placed:
                s = s.replace("</body>", HTML_BUTTON + "\n</body>", 1) if "</body>" in s else s + HTML_BUTTON
                
            js = (JS_BLOCK.replace("__MARK__", MARK).replace("__BRIDGE__", bridge))
            s = s.replace("</body>", js + "</body>", 1) if "</body>" in s else s + js
            write(p, s)
            log("OK", "%s patched" % rel(p))

def main():
    print("Project root:", ROOT)
    patch_gradle()
    patch_manifest()
    manager_pkg = None
    for name in ACTIVITY_FILES:
        ps = find_files(name)
        if ps:
            manager_pkg = package_of(read(ps[0]))
            if manager_pkg:
                create_manager(manager_pkg, os.path.dirname(ps[0]))
                break
    if manager_pkg:
        patch_activities(manager_pkg)
    patch_html()
    
    print("\n==== SUMMARY ====")
    if FAILED:
        print("Required patches failed:", ", ".join(sorted(set(FAILED))))
        sys.exit(1)

if __name__ == "__main__":
    main()
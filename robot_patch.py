#!/usr/bin/env python3
"""يقرأ robot_lab.html، يضغطه (zip) ويشفّره (base64)، ثم يولّد RobotStudioActivity.kt
ويسجّل الـ Activity في AndroidManifest.xml إن لم تكن مسجّلة."""
import base64, io, os, re, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "robot_lab.html")
CHUNK = 8000  # حد ثابت النص في JVM هو 65535 بايت، فنقسم البيانات إلى قطع

# ---------- 1) قراءة HTML وضغطه وتشفيره ----------
if not os.path.isfile(HTML):
    sys.exit("ERROR: robot_lab.html غير موجود بجانب robot_patch.py")
raw = open(HTML, "rb").read()
if b"<html" not in raw.lower():
    sys.exit("ERROR: الملف لا يبدو صفحة HTML صالحة")

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr("robot_lab.html", raw)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")

# تحقق ذاتي: فك التشفير والضغط ويجب أن يطابق الأصل بايتاً ببايت
with zipfile.ZipFile(io.BytesIO(base64.b64decode(b64))) as z:
    assert z.read("robot_lab.html") == raw, "فشل التحقق من الضغط/التشفير"
print(f"HTML {len(raw):,} B -> zip+b64 {len(b64):,} chars (تحقق ناجح)")

chunks = [b64[i:i + CHUNK] for i in range(0, len(b64), CHUNK)]
data_kt = ",\n".join('            "%s"' % c for c in chunks)

# ---------- 2) اكتشاف الحزمة (package) ----------
def detect_package():
    p = os.environ.get("APP_PACKAGE")
    if p:
        return p
    for g in ("app/build.gradle.kts", "app/build.gradle"):
        gp = os.path.join(HERE, g)
        if os.path.isfile(gp):
            t = open(gp, encoding="utf-8").read()
            m = re.search(r'namespace\s*=?\s*["\']([\w.]+)["\']', t) or \
                re.search(r'applicationId\s*=?\s*["\']([\w.]+)["\']', t)
            if m:
                return m.group(1)
    mf = os.path.join(HERE, "app/src/main/AndroidManifest.xml")
    if os.path.isfile(mf):
        m = re.search(r'package\s*=\s*"([\w.]+)"', open(mf, encoding="utf-8").read())
        if m:
            return m.group(1)
    sys.exit("ERROR: تعذّر اكتشاف الحزمة. عيّن المتغير APP_PACKAGE")

PKG = detect_package()

# ---------- 3) قالب Kotlin ----------
KT = r'''package __PKG__

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.speech.RecognizerIntent
import android.util.Base64
import android.view.ViewGroup
import android.view.WindowManager
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
import android.widget.Toast
import org.json.JSONObject
import java.io.ByteArrayInputStream
import java.util.Locale
import java.util.zip.ZipInputStream
import java.util.concurrent.TimeUnit
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import com.example.voiceassistant.data.LicenseManager

class RobotStudioActivity : Activity() {

    companion object {
        private const val REQ_VOICE = 7001

        // robot_lab.html مضغوط (zip) ومشفّر (base64)، وقد وُلّد تلقائياً أثناء البناء
        private val DATA = arrayOf(
__DATA__
        )

        private fun loadHtml(): String {
            val bytes = Base64.decode(DATA.joinToString(""), Base64.DEFAULT)
            ZipInputStream(ByteArrayInputStream(bytes)).use { zin ->
                zin.nextEntry ?: error("zip فارغ")
                return zin.readBytes().toString(Charsets.UTF_8)
            }
        }
    }

    private lateinit var web: WebView
    private var voiceId = ""
    private val client: OkHttpClient by lazy {
        OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(70, TimeUnit.SECONDS)
            .build()
    }

    @SuppressLint("SetJavaScriptEnabled", "AddJavascriptInterface")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        val rootView = FrameLayout(this).apply {
            setBackgroundColor(Color.parseColor("#0A0F18"))
            fitsSystemWindows = true
        }
        web = WebView(this).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
            setBackgroundColor(Color.parseColor("#0A0F18"))
            overScrollMode = WebView.OVER_SCROLL_NEVER
            isVerticalScrollBarEnabled = false
            isHorizontalScrollBarEnabled = false
        }
        rootView.addView(web)
        setContentView(rootView)

        web.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            allowFileAccess = false
            allowContentAccess = false
            mediaPlaybackRequiresUserGesture = false
            mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
            useWideViewPort = true
            loadWithOverviewMode = true
            setSupportZoom(false)
        }
        web.webChromeClient = WebChromeClient()
        web.webViewClient = WebViewClient()
        web.addJavascriptInterface(Bridge(), "Android")

        web.loadDataWithBaseURL("https://appassets.local/", loadHtml(),
            "text/html", "UTF-8", null)
    }

    // ---- Bridge ----
    inner class Bridge {
        @JavascriptInterface
        fun askAi(id: String, tutor: String, prompt: String) {
            Thread {
                try {
                    val base = BuildConfig.VIDEO_SERVER_URL.trim()
                        .replace("/api/generate-video", "")
                        .removeSuffix("/api")
                        .trimEnd('/')
                    val key = LicenseManager.getBackendKey()
                    val body = JSONObject()
                        .put("licenseKey", key)
                        .put("mode", tutor)
                        .put("prompt", prompt)
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
                            reply(id, true, text)
                        } else {
                            reply(id, false, "")
                        }
                    }
                } catch (e: Exception) {
                    reply(id, false, "")
                }
            }.start()
        }

        @JavascriptInterface
        fun startVoice(id: String) {
            runOnUiThread {
                voiceId = id
                try {
                    val i = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                        putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ar-SA")
                        putExtra(RecognizerIntent.EXTRA_PROMPT, "تحدّث الآن")
                    }
                    startActivityForResult(i, REQ_VOICE)
                } catch (e: Exception) {
                    Toast.makeText(this@RobotStudioActivity,
                        "التعرف على الصوت غير متاح", Toast.LENGTH_SHORT).show()
                    voiceResult(id, false, "")
                }
            }
        }
    }

    private fun js(code: String) = runOnUiThread { web.evaluateJavascript(code, null) }

    private fun reply(id: String, ok: Boolean, text: String) =
        js("window.onAiResult && window.onAiResult(${JSONObject.quote(id)},$ok,${JSONObject.quote(text)})")

    private fun voiceResult(id: String, ok: Boolean, text: String) =
        js("window.onVoiceResult && window.onVoiceResult(${JSONObject.quote(id)},$ok,${JSONObject.quote(text)})")

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQ_VOICE) return
        val t = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)?.firstOrNull()
        voiceResult(voiceId, resultCode == RESULT_OK && !t.isNullOrBlank(), t ?: "")
    }

    override fun onPause() { web.onPause(); super.onPause() }
    override fun onResume() { super.onResume(); web.onResume() }
    override fun onDestroy() {
        (web.parent as? ViewGroup)?.removeView(web)
        web.destroy()
        super.onDestroy()
    }
}
'''

kt = KT.replace("__PKG__", PKG).replace("__DATA__", data_kt)

out_dir = os.path.join(HERE, "app/src/main/java", *PKG.split("."))
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "RobotStudioActivity.kt")
open(out, "w", encoding="utf-8").write(kt)
print("كُتب:", out)

# ---------- 4) تسجيل الـ Activity في المانيفست ----------
mf = os.path.join(HERE, "app/src/main/AndroidManifest.xml")
if os.path.isfile(mf):
    t = open(mf, encoding="utf-8").read()
    if "RobotStudioActivity" not in t:
        act = ('    <activity android:name=".RobotStudioActivity" android:exported="false"\n'
               '        android:configChanges="orientation|screenSize|keyboardHidden|smallestScreenSize|screenLayout"\n'
               '        android:windowSoftInputMode="adjustResize" />\n')
        t = t.replace("</application>", act + "</application>", 1)
        open(mf, "w", encoding="utf-8").write(t)
        print("سُجّلت RobotStudioActivity في AndroidManifest.xml")
else:
    print("تنبيه: AndroidManifest.xml غير موجود، سجّل الـ Activity يدوياً")
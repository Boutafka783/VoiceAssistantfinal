import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
SCANNER = PKG_DIR + "/SecurityScanner.kt"
ACTIVITY = PKG_DIR + "/SecurityActivity.kt"
HTML_PATH = "app/src/main/assets/security_lab.html"
ARCH_ACTIVITY = PKG_DIR + "/ArchitectureActivity.kt"

print(">> Applying Security Center Patch v1.0 ...")

# ---------------------------------------------------------------- 1) Scanner
scanner_content = r'''package com.zevorix.assistant

import android.app.KeyguardManager
import android.app.admin.DevicePolicyManager
import android.content.Context
import android.content.pm.ApplicationInfo
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import android.provider.Settings
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.InetSocketAddress
import java.net.Socket
import java.net.URL
import java.security.KeyStore
import java.security.MessageDigest
import java.text.SimpleDateFormat
import java.util.Locale

object SecurityScanner {

    private val STORES = setOf(
        "com.android.vending", "com.huawei.appmarket", "com.sec.android.app.samsungapps",
        "com.xiaomi.mipicks", "com.xiaomi.market", "com.heytap.market", "com.oppo.market",
        "com.vivo.appstore", "com.amazon.venezia"
    )

    private const val P = "android.permission."

    private val PERM_SCORES: Map<String, Pair<Int, String>> = mapOf(
        P + "READ_SMS" to Pair(20, "يقرأ الرسائل النصية"),
        P + "RECEIVE_SMS" to Pair(15, "يستقبل الرسائل النصية (قد يسرق رموز التحقق)"),
        P + "SEND_SMS" to Pair(10, "يرسل رسائل نصية"),
        P + "READ_CALL_LOG" to Pair(15, "يقرأ سجل المكالمات"),
        P + "RECORD_AUDIO" to Pair(10, "يستخدم الميكروفون"),
        P + "CAMERA" to Pair(5, "يستخدم الكاميرا"),
        P + "ACCESS_BACKGROUND_LOCATION" to Pair(10, "يتتبع الموقع في الخلفية"),
        P + "READ_CONTACTS" to Pair(8, "يقرأ جهات الاتصال"),
        P + "SYSTEM_ALERT_WINDOW" to Pair(15, "يظهر فوق التطبيقات الأخرى (قد يُستخدم للتصيّد)"),
        P + "REQUEST_INSTALL_PACKAGES" to Pair(15, "يستطيع تثبيت تطبيقات أخرى"),
        P + "MANAGE_EXTERNAL_STORAGE" to Pair(10, "وصول كامل لكل الملفات"),
        P + "QUERY_ALL_PACKAGES" to Pair(4, "يرى قائمة كل التطبيقات")
    )

    @Suppress("DEPRECATION")
    private fun allApps(pm: PackageManager): List<ApplicationInfo> {
        return if (Build.VERSION.SDK_INT >= 33) {
            pm.getInstalledApplications(PackageManager.ApplicationInfoFlags.of(0L))
        } else {
            pm.getInstalledApplications(0)
        }
    }

    @Suppress("DEPRECATION")
    private fun pkgInfo(pm: PackageManager, name: String): PackageInfo? {
        val flags = PackageManager.GET_PERMISSIONS or PackageManager.GET_SERVICES or PackageManager.GET_RECEIVERS
        return try {
            if (Build.VERSION.SDK_INT >= 33) {
                pm.getPackageInfo(name, PackageManager.PackageInfoFlags.of(flags.toLong()))
            } else {
                pm.getPackageInfo(name, flags)
            }
        } catch (e: Exception) {
            null
        }
    }

    @Suppress("DEPRECATION")
    private fun installer(pm: PackageManager, pkg: String): String? {
        return try {
            if (Build.VERSION.SDK_INT >= 30) pm.getInstallSourceInfo(pkg).installingPackageName
            else pm.getInstallerPackageName(pkg)
        } catch (e: Exception) {
            null
        }
    }

    private fun enabledPkgs(ctx: Context, key: String): Set<String> {
        val raw: String? = try {
            Settings.Secure.getString(ctx.contentResolver, key)
        } catch (e: Exception) {
            null
        }
        if (raw.isNullOrBlank()) return emptySet()
        return raw.split(":").map { it.substringBefore("/") }.filter { it.isNotBlank() }.toSet()
    }

    private fun adminPkgs(ctx: Context): Set<String> {
        return try {
            val dpm = ctx.getSystemService(Context.DEVICE_POLICY_SERVICE) as DevicePolicyManager
            val admins = dpm.activeAdmins ?: emptyList()
            admins.map { it.packageName }.toSet()
        } catch (e: Exception) {
            emptySet()
        }
    }

    private fun portOpen(port: Int): Boolean {
        return try {
            Socket().use { s ->
                s.connect(InetSocketAddress("127.0.0.1", port), 150)
                true
            }
        } catch (e: Exception) {
            false
        }
    }

    // ------------------------------------------------------------ apps
    fun scanApps(ctx: Context): JSONObject {
        val pm = ctx.packageManager
        val acc = enabledPkgs(ctx, "enabled_accessibility_services")
        val nl = enabledPkgs(ctx, "enabled_notification_listeners")
        val adm = adminPkgs(ctx)
        var total = 0
        val found = ArrayList<JSONObject>()

        for (ai in allApps(pm)) {
            if ((ai.flags and ApplicationInfo.FLAG_SYSTEM) != 0) continue
            total++
            val pkg = ai.packageName
            val pi = pkgInfo(pm, pkg) ?: continue
            val perms = (pi.requestedPermissions ?: emptyArray<String>()).toSet()
            val svcPerms = (pi.services ?: emptyArray()).mapNotNull { it.permission }.toSet()
            var score = 0
            val reasons = ArrayList<String>()
            fun add(points: Int, text: String) {
                score += points
                reasons.add(text)
            }

            val accOn = acc.contains(pkg)
            if (accOn) add(50, "خدمة إمكانية الوصول مفعّلة (تستطيع قراءة الشاشة والتحكم بها)")
            else if (svcPerms.contains(P + "BIND_ACCESSIBILITY_SERVICE")) add(8, "يعرّف خدمة إمكانية وصول (غير مفعّلة)")
            if (nl.contains(pkg)) add(35, "يقرأ كل الإشعارات (بما فيها رموز التحقق)")
            else if (svcPerms.contains(P + "BIND_NOTIFICATION_LISTENER_SERVICE")) add(5, "يعرّف مستمع إشعارات (غير مفعّل)")
            if (adm.contains(pkg)) add(35, "مدير جهاز مفعّل (صعب الإزالة)")

            for (p in perms) {
                val e = PERM_SCORES[p]
                if (e != null) add(e.first, e.second)
            }

            val hasSms = perms.contains(P + "READ_SMS") || perms.contains(P + "RECEIVE_SMS")
            val hasOverlay = perms.contains(P + "SYSTEM_ALERT_WINDOW")
            if (accOn && hasOverlay) add(20, "تركيبة خطرة: إمكانية وصول + ظهور فوق التطبيقات")
            if (hasSms && hasOverlay) add(20, "تركيبة خطرة: الرسائل + ظهور فوق التطبيقات")

            val inst = installer(pm, pkg)
            val sideload = inst == null || !STORES.contains(inst)
            if (sideload) add(15, "مثبّت من خارج متجر معروف")
            if ((ai.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0) add(15, "نسخة قابلة للتصحيح (debuggable)")
            if (ai.targetSdkVersion < 26) add(8, "تطبيق قديم يتجاهل حمايات أندرويد الحديثة")
            if (score >= 20 && pm.getLaunchIntentForPackage(pkg) == null) add(10, "لا يملك أيقونة تشغيل (قد يكون مخفياً)")

            if (score >= 15) {
                val level = if (score >= 60) "high" else if (score >= 30) "medium" else "low"
                val o = JSONObject()
                o.put("pkg", pkg)
                o.put("name", pm.getApplicationLabel(ai).toString())
                o.put("score", score)
                o.put("level", level)
                o.put("sideload", sideload)
                o.put("installer", inst ?: "")
                o.put("reasons", JSONArray(reasons))
                found.add(o)
            }
        }
        found.sortByDescending { it.getInt("score") }
        val arr = JSONArray()
        for (o in found) arr.put(o)
        return JSONObject().put("total", total).put("apps", arr)
    }

    // ------------------------------------------------------------ device
    fun scanDevice(ctx: Context): JSONArray {
        val out = JSONArray()
        fun add(sev: String, title: String, detail: String, action: String = "") {
            out.put(JSONObject().put("sev", sev).put("title", title).put("detail", detail).put("action", action))
        }
        val cr = ctx.contentResolver

        try {
            val km = ctx.getSystemService(Context.KEYGUARD_SERVICE) as KeyguardManager
            if (km.isDeviceSecure) add("ok", "قفل الشاشة مفعّل", "الجهاز محمي بنمط أو رمز أو بصمة.")
            else add("high", "لا يوجد قفل شاشة", "أي شخص يمسك هاتفك يصل لكل بياناتك.", "security")
        } catch (e: Exception) { }

        try {
            val patch = Build.VERSION.SECURITY_PATCH
            val d = SimpleDateFormat("yyyy-MM-dd", Locale.US).parse(patch)
            if (d != null) {
                val age = ((System.currentTimeMillis() - d.time) / 86400000L).toInt()
                if (age > 365) add("high", "تحديثات الأمان قديمة جداً", "آخر تصحيح أمني: " + patch + " (منذ " + age + " يوماً). الثغرات المعروفة غير مسدودة.", "security")
                else if (age > 150) add("medium", "تحديثات الأمان متأخرة", "آخر تصحيح أمني: " + patch + " (منذ " + age + " يوماً).", "security")
                else add("ok", "تحديثات الأمان حديثة", "آخر تصحيح أمني: " + patch)
            }
        } catch (e: Exception) { }

        try {
            if (Settings.Global.getInt(cr, Settings.Global.ADB_ENABLED, 0) == 1)
                add("high", "تصحيح USB (ADB) مفعّل", "يسمح لأي حاسوب موصول بالتحكم بالهاتف وسحب البيانات. عطّله إن لم تكن مطوراً.", "developer")
            else add("ok", "تصحيح USB معطّل", "")
            if (Settings.Global.getInt(cr, Settings.Global.DEVELOPMENT_SETTINGS_ENABLED, 0) == 1)
                add("low", "خيارات المطور مفعّلة", "الأفضل إيقافها إن لم تحتجها.", "developer")
        } catch (e: Exception) { }

        try {
            val ks = KeyStore.getInstance("AndroidCAStore")
            ks.load(null)
            var n = 0
            val en = ks.aliases()
            while (en.hasMoreElements()) {
                if (en.nextElement().startsWith("user:")) n++
            }
            if (n > 0) add("high", "شهادات جذر مثبّتة يدوياً (" + n + ")", "تسمح لجهة ما باعتراض وقراءة حركة HTTPS. تحقق منها وأزلها إن لم تعرفها.", "security")
            else add("ok", "لا توجد شهادات جذر مضافة يدوياً", "")
        } catch (e: Exception) { }

        try {
            val cm = ctx.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
            val caps = cm.getNetworkCapabilities(cm.activeNetwork)
            if (caps != null && caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))
                add("medium", "اتصال VPN نشط", "تأكد أنك أنت من فعّله وأنه من مزوّد موثوق، فالـVPN يرى كل حركة بياناتك.", "vpn")
            val proxy = System.getProperty("http.proxyHost")
            if (!proxy.isNullOrBlank())
                add("high", "بروكسي مفعّل على الشبكة", "الخادم " + proxy + " يمرّ عبره اتصالك وقد يراقبه.", "wifi")
        } catch (e: Exception) { }

        try {
            val mode = Settings.Global.getString(cr, "private_dns_mode")
            if (mode == "hostname" || mode == "opportunistic") add("ok", "DNS الخاص مفعّل", "")
            else add("low", "DNS الخاص غير مفعّل", "تفعيله يحمي استعلامات المواقع من التلصص على شبكات الواي فاي.", "wifi")
        } catch (e: Exception) { }

        try {
            if (Settings.Global.getInt(cr, "package_verifier_enable", 1) == 0)
                add("medium", "فحص التطبيقات (Play Protect) معطّل", "فعّله من إعدادات متجر Google Play.", "security")
        } catch (e: Exception) { }

        try {
            val t = Settings.System.getInt(cr, Settings.System.SCREEN_OFF_TIMEOUT, 60000)
            if (t > 300000) add("low", "مهلة إطفاء الشاشة طويلة", "الشاشة تبقى مفتوحة أكثر من 5 دقائق.", "security")
        } catch (e: Exception) { }

        val rootPaths = listOf(
            "/system/bin/su", "/system/xbin/su", "/sbin/su", "/system/app/Superuser.apk",
            "/data/local/bin/su", "/data/local/xbin/su", "/su/bin/su"
        )
        val rooted = rootPaths.any { File(it).exists() } || (Build.TAGS ?: "").contains("test-keys")
        if (rooted) add("high", "مؤشرات على روت أو نظام معدّل", "الروت يلغي عزل التطبيقات ويسهّل التجسس.")
        else add("ok", "لا مؤشرات على روت", "")

        val frida = File("/data/local/tmp/frida-server").exists() || portOpen(27042)
        if (frida) add("high", "أداة حقن (Frida) قيد العمل", "تُستخدم لاعتراض التطبيقات والتلاعب بها.")

        val acc = enabledPkgs(ctx, "enabled_accessibility_services")
        if (acc.isNotEmpty()) add("medium", "خدمات إمكانية وصول مفعّلة (" + acc.size + ")", acc.joinToString("، "), "accessibility")
        val nl = enabledPkgs(ctx, "enabled_notification_listeners")
        if (nl.isNotEmpty()) add("medium", "تطبيقات تقرأ الإشعارات (" + nl.size + ")", nl.joinToString("، "), "notifications")
        val adm = adminPkgs(ctx)
        if (adm.isNotEmpty()) add("medium", "مديرو جهاز مفعّلون (" + adm.size + ")", adm.joinToString("، "), "security")

        return out
    }

    // ------------------------------------------------------------ VirusTotal
    private fun sha256(path: String): String {
        val md = MessageDigest.getInstance("SHA-256")
        File(path).inputStream().use { ins ->
            val buf = ByteArray(65536)
            while (true) {
                val n = ins.read(buf)
                if (n <= 0) break
                md.update(buf, 0, n)
            }
        }
        return md.digest().joinToString("") { "%02x".format(it) }
    }

    @Suppress("DEPRECATION")
    fun vtLookup(ctx: Context, pkg: String, key: String): JSONObject {
        val res = JSONObject()
        try {
            val ai = ctx.packageManager.getApplicationInfo(pkg, 0)
            val h = sha256(ai.sourceDir)
            res.put("sha256", h)
            val c = URL("https://www.virustotal.com/api/v3/files/" + h).openConnection() as HttpURLConnection
            c.connectTimeout = 10000
            c.readTimeout = 15000
            c.setRequestProperty("x-apikey", key)
            val code = c.responseCode
            if (code == 200) {
                val body = c.inputStream.bufferedReader().use { it.readText() }
                val st = JSONObject(body).getJSONObject("data").getJSONObject("attributes").getJSONObject("last_analysis_stats")
                res.put("status", "found")
                res.put("malicious", st.optInt("malicious"))
                res.put("suspicious", st.optInt("suspicious"))
                res.put("harmless", st.optInt("harmless"))
                res.put("undetected", st.optInt("undetected"))
            } else if (code == 404) {
                res.put("status", "unknown")
            } else if (code == 401 || code == 403) {
                res.put("status", "badkey")
            } else if (code == 429) {
                res.put("status", "ratelimit")
            } else {
                res.put("status", "error").put("detail", "HTTP " + code)
            }
            c.disconnect()
        } catch (e: Exception) {
            res.put("status", "error").put("detail", e.message ?: "")
        }
        return res
    }
}
'''

# --------------------------------------------------------------- 2) Activity
activity_content = r'''package com.zevorix.assistant

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.zevorix.assistant.ui.theme.VoiceAssistantTheme
import kotlinx.coroutines.*
import org.json.JSONObject

class SecurityActivity : ComponentActivity() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            VoiceAssistantTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    AndroidView(
                        modifier = Modifier.fillMaxSize(),
                        factory = { context ->
                            WebView(context).apply {
                                settings.javaScriptEnabled = true
                                settings.allowFileAccess = false
                                settings.allowContentAccess = false
                                settings.javaScriptCanOpenWindowsAutomatically = false
                                webViewClient = WebViewClient()
                                addJavascriptInterface(Bridge(this@SecurityActivity, this, scope), "Android")
                                loadUrl("file:///android_asset/security_lab.html")
                            }
                        }
                    )
                }
            }
        }
    }

    override fun onDestroy() {
        scope.cancel()
        super.onDestroy()
    }

    class Bridge(
        private val activity: ComponentActivity,
        private val webView: WebView,
        private val scope: CoroutineScope
    ) {
        private val prefs = activity.getSharedPreferences("zevorix_security", Context.MODE_PRIVATE)
        private val pkgRegex = Regex("^[A-Za-z0-9_.]+$")

        private suspend fun push(id: String, json: String) {
            withContext(Dispatchers.Main) {
                webView.evaluateJavascript(
                    "window.onSecResult(" + JSONObject.quote(id) + ", " + JSONObject.quote(json) + ");", null
                )
            }
        }

        @JavascriptInterface
        fun scanDevice() {
            scope.launch {
                try {
                    push("device", SecurityScanner.scanDevice(activity).toString())
                } catch (e: Exception) {
                    push("device", "[]")
                }
            }
        }

        @JavascriptInterface
        fun scanApps() {
            scope.launch {
                try {
                    push("apps", SecurityScanner.scanApps(activity).toString())
                } catch (e: Exception) {
                    push("apps", "{\"total\":0,\"apps\":[]}")
                }
            }
        }

        @JavascriptInterface
        fun hasKey(): Boolean = !prefs.getString("vt", "").isNullOrBlank()

        @JavascriptInterface
        fun saveKey(key: String): Boolean {
            val k = key.trim()
            if (k.length < 20 || k.length > 100 || !k.all { it.isLetterOrDigit() }) return false
            prefs.edit().putString("vt", k).apply()
            return true
        }

        @JavascriptInterface
        fun clearKey() {
            prefs.edit().remove("vt").apply()
        }

        @JavascriptInterface
        fun vtCheck(pkg: String) {
            if (!pkgRegex.matches(pkg)) return
            scope.launch {
                val key = prefs.getString("vt", "") ?: ""
                if (key.isBlank()) {
                    push("vt:" + pkg, "{\"status\":\"nokey\"}")
                } else {
                    push("vt:" + pkg, SecurityScanner.vtLookup(activity, pkg, key).toString())
                }
            }
        }

        private fun launch(intent: Intent) {
            activity.runOnUiThread {
                try {
                    activity.startActivity(intent)
                } catch (e: Exception) { }
            }
        }

        @JavascriptInterface
        fun openSetting(name: String) {
            val action = when (name) {
                "accessibility" -> Settings.ACTION_ACCESSIBILITY_SETTINGS
                "notifications" -> "android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"
                "developer" -> Settings.ACTION_APPLICATION_DEVELOPMENT_SETTINGS
                "vpn" -> Settings.ACTION_VPN_SETTINGS
                "wifi" -> Settings.ACTION_WIFI_SETTINGS
                else -> Settings.ACTION_SECURITY_SETTINGS
            }
            launch(Intent(action))
        }

        @JavascriptInterface
        fun openApp(pkg: String) {
            if (!pkgRegex.matches(pkg)) return
            launch(Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + pkg)))
        }

        @JavascriptInterface
        fun uninstall(pkg: String) {
            if (!pkgRegex.matches(pkg)) return
            launch(Intent(Intent.ACTION_DELETE, Uri.parse("package:" + pkg)))
        }
    }
}
'''

# ------------------------------------------------------------------- 3) HTML
html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>مركز الأمان</title>
<style>
:root{--bg:#0a192f;--panel:#112240;--border:#233554;--text:#ccd6f6;--muted:#8892b0;--accent:#64ffda;--hi:#ef4444;--md:#f59e0b;--lo:#38bdf8;--ok:#22c55e}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;min-height:100%;background:var(--bg);color:var(--text);font-family:system-ui,sans-serif}
#app{padding:12px 12px 40px;max-width:720px;margin:0 auto}
h1{margin:4px 0 12px;font-size:1.1rem;color:var(--accent)}
h2{margin:18px 0 8px;font-size:.95rem;color:var(--accent)}
.card{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:8px}
#score{display:flex;align-items:center;gap:14px}
#ring{width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:700;border:6px solid var(--border);flex:0 0 auto}
#scoretxt{font-size:.85rem;color:var(--muted);line-height:1.7}
button{font-family:inherit;cursor:pointer}
.btn{background:var(--accent);color:#0a192f;border:0;border-radius:8px;padding:10px 14px;font-weight:700;font-size:.9rem}
.btn:disabled{opacity:.5}
.sbtn{background:transparent;border:1px solid var(--border);color:var(--text);border-radius:6px;padding:6px 10px;font-size:.78rem;margin:6px 0 0 6px}
.sbtn.danger{border-color:var(--hi);color:var(--hi)}
.item{border-right:4px solid var(--border)}
.item.high{border-right-color:var(--hi)}.item.medium{border-right-color:var(--md)}.item.low{border-right-color:var(--lo)}.item.ok{border-right-color:var(--ok)}
.item .t{font-weight:700;font-size:.9rem}
.item .d{color:var(--muted);font-size:.8rem;margin-top:4px;line-height:1.6;word-break:break-word}
.item ul{margin:6px 0 0;padding-right:18px;font-size:.8rem;color:var(--muted);line-height:1.7}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:.72rem;margin-right:6px;color:#0a192f}
.badge.high{background:var(--hi)}.badge.medium{background:var(--md)}.badge.low{background:var(--lo)}
.pkg{font-size:.72rem;color:var(--muted);direction:ltr;text-align:right;word-break:break-all}
.vt{margin-top:6px;font-size:.8rem}
input{width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:var(--text);margin:6px 0;direction:ltr}
.note{font-size:.75rem;color:var(--muted);line-height:1.7}
#toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--accent);color:#0a192f;padding:10px 18px;border-radius:18px;font-weight:700;font-size:.85rem;opacity:0;transition:opacity .3s;pointer-events:none;max-width:92%;text-align:center}
</style>
</head>
<body>
<div id="app">
  <h1>🛡️ مركز الأمان</h1>

  <div class="card" id="score">
    <div id="ring">--</div>
    <div>
      <div id="scoretxt">اضغط «افحص الآن» لتدقيق الجهاز والتطبيقات.</div>
      <button class="btn" id="scan-btn" style="margin-top:8px">🔍 افحص الآن</button>
    </div>
  </div>

  <h2>إعدادات الجهاز والبيئة</h2>
  <div id="dev"></div>

  <h2>التطبيقات المشبوهة <span id="appcount" class="note"></span></h2>
  <div id="apps"></div>

  <h2>فحص VirusTotal</h2>
  <div class="card">
    <div class="note">أدخل مفتاح API مجاني من virustotal.com لفحص بصمة أي تطبيق (لا يُرفع التطبيق نفسه، تُرسل بصمته فقط). الحد المجاني: 4 طلبات في الدقيقة.</div>
    <input id="key" type="password" placeholder="VirusTotal API key" autocomplete="off">
    <button class="sbtn" id="key-save">حفظ المفتاح</button>
    <button class="sbtn" id="key-clear">حذف المفتاح</button>
    <span id="key-state" class="note"></span>
  </div>

  <div class="note" style="margin-top:14px">⚠️ هذه أداة تدقيق وكشف مؤشرات، وليست بديلاً عن مضاد فيروسات متكامل. لا يمكنها كشف برامج التجسس المتقدمة على مستوى النظام. عند الشك الجدي، أعد ضبط المصنع بعد نسخ بياناتك المهمة.</div>
</div>
<div id="toast"></div>

<script>
(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
var dev=null,apps=null,toastTimer=null,waiting=0;
var LV={high:'خطر',medium:'متوسط',low:'منخفض'};
var ACT={security:'فتح الإعدادات',accessibility:'إدارة إمكانية الوصول',notifications:'إدارة الإشعارات',developer:'خيارات المطور',vpn:'إعدادات VPN',wifi:'إعدادات الشبكة'};

function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
function toast(m){var t=$('toast');t.textContent=m;t.style.opacity=1;clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.style.opacity=0},3500)}
function A(fn){
  try{var a=Array.prototype.slice.call(arguments,1);return window.Android[fn].apply(window.Android,a)}
  catch(e){toast('هذه الميزة تعمل داخل التطبيق فقط');return null}
}

function updateScore(){
  if(!dev&&!apps)return;
  var s=100,i;
  if(dev)for(i=0;i<dev.length;i++){if(dev[i].sev==='high')s-=15;else if(dev[i].sev==='medium')s-=6;else if(dev[i].sev==='low')s-=2}
  if(apps)for(i=0;i<apps.apps.length;i++){var l=apps.apps[i].level;if(l==='high')s-=8;else if(l==='medium')s-=3}
  s=Math.max(0,Math.min(100,s));
  var c=s>=80?'var(--ok)':(s>=55?'var(--md)':'var(--hi)');
  var ring=$('ring');ring.textContent=s;ring.style.borderColor=c;ring.style.color=c;
  $('scoretxt').textContent=s>=80?'وضعك الأمني جيد. راجع الملاحظات أدناه.':(s>=55?'هناك نقاط تحتاج معالجة.':'وضعك الأمني ضعيف. عالج البنود الحمراء أولاً.');
}

function renderDev(){
  var box=$('dev');box.textContent='';
  var order={high:0,medium:1,low:2,ok:3};
  dev.sort(function(a,b){return order[a.sev]-order[b.sev]});
  dev.forEach(function(f){
    var c=el('div','card item '+f.sev);
    c.appendChild(el('div','t',(f.sev==='ok'?'✅ ':'')+f.title));
    if(f.detail)c.appendChild(el('div','d',f.detail));
    if(f.action&&f.sev!=='ok'){
      var b=el('button','sbtn',ACT[f.action]||'فتح الإعدادات');
      b.onclick=function(){A('openSetting',f.action)};
      c.appendChild(b);
    }
    box.appendChild(c);
  });
}

function renderApps(){
  var box=$('apps');box.textContent='';
  $('appcount').textContent='(فُحص '+apps.total+' تطبيقاً)';
  if(!apps.apps.length){box.appendChild(el('div','card note','لم يُعثر على تطبيقات ذات مؤشرات خطرة ✅'));return}
  apps.apps.forEach(function(a){
    var c=el('div','card item '+a.level);
    var t=el('div','t',a.name);
    t.appendChild(el('span','badge '+a.level,LV[a.level]+' · '+a.score));
    c.appendChild(t);
    c.appendChild(el('div','pkg',a.pkg));
    var ul=el('ul');a.reasons.forEach(function(r){ul.appendChild(el('li',null,r))});
    c.appendChild(ul);
    var vt=el('div','vt');vt.id='vt-'+a.pkg;
    c.appendChild(vt);
    var b1=el('button','sbtn','تفاصيل');b1.onclick=function(){A('openApp',a.pkg)};
    var b2=el('button','sbtn','فحص VirusTotal');b2.onclick=function(){vt.textContent='جاري الفحص...';A('vtCheck',a.pkg)};
    var b3=el('button','sbtn danger','إزالة');b3.onclick=function(){A('uninstall',a.pkg)};
    c.appendChild(b1);c.appendChild(b2);c.appendChild(b3);
    box.appendChild(c);
  });
}

function renderVt(pkg,d){
  var e=document.getElementById('vt-'+pkg);if(!e)return;
  var m={nokey:'أدخل مفتاح VirusTotal أولاً.',unknown:'البصمة غير معروفة لدى VirusTotal (تطبيق نادر أو جديد).',badkey:'المفتاح مرفوض.',ratelimit:'تجاوزت الحد المجاني، انتظر دقيقة.',error:'تعذر الفحص: '+(d.detail||'')};
  if(d.status==='found'){
    var bad=d.malicious+d.suspicious;
    e.textContent=(bad>0?'🚨 ':'✅ ')+'خبيث: '+d.malicious+' · مشبوه: '+d.suspicious+' · سليم: '+d.harmless;
    e.style.color=bad>0?'var(--hi)':'var(--ok)';
  }else{e.textContent=m[d.status]||'خطأ';e.style.color='var(--muted)'}
}

window.onSecResult=function(id,json){
  var d;try{d=JSON.parse(json)}catch(e){return}
  if(id==='device'){dev=d;renderDev();waiting--}
  else if(id==='apps'){apps=d;renderApps();waiting--}
  else if(id.indexOf('vt:')===0){renderVt(id.slice(3),d)}
  if(waiting<=0){$('scan-btn').disabled=false;$('scan-btn').textContent='🔍 افحص مجدداً'}
  updateScore();
};

$('scan-btn').onclick=function(){
  waiting=2;this.disabled=true;this.textContent='جاري الفحص...';
  $('scoretxt').textContent='جاري تدقيق الجهاز والتطبيقات...';
  A('scanDevice');A('scanApps');
};

function keyState(){var h=A('hasKey');$('key-state').textContent=h?'المفتاح محفوظ ✔':'لا يوجد مفتاح'}
$('key-save').onclick=function(){
  var v=$('key').value;
  if(A('saveKey',v)){$('key').value='';toast('تم حفظ المفتاح')}else toast('مفتاح غير صالح');
  keyState();
};
$('key-clear').onclick=function(){A('clearKey');keyState();toast('تم حذف المفتاح')};
keyState();
})();
</script>
</body>
</html>
'''

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(">> Wrote " + path)

write(SCANNER, scanner_content)
write(ACTIVITY, activity_content)
write(HTML_PATH, html_content)

# ------------------------------------------------------------ 4) Manifest
if not os.path.exists(MANIFEST):
    raise FileNotFoundError("File not found: " + MANIFEST)
with open(MANIFEST, "r", encoding="utf-8") as f:
    m = f.read()
body = re.sub(r"<!--.*?-->", "", m, flags=re.S)

perms = [
    "android.permission.QUERY_ALL_PACKAGES",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.INTERNET",
    "android.permission.REQUEST_DELETE_PACKAGES",
]
missing = [p for p in perms if not re.search(r'<uses-permission\b[^>]*android:name\s*=\s*"' + re.escape(p) + r'"', body)]
if missing:
    idx = m.find("<application")
    if idx < 0:
        raise RuntimeError("<application not found in manifest")
    lines = "".join('    <uses-permission android:name="%s" />\n' % p for p in missing)
    m = m[:idx] + lines + "\n    " + m[idx:]
    print(">> Added permissions: " + ", ".join(p.split(".")[-1] for p in missing))

if not re.search(r'<activity\b[^>]*android:name\s*=\s*"[^"]*\bSecurityActivity"', body, re.S):
    block = (
        '    <activity\n'
        '        android:name=".SecurityActivity"\n'
        '        android:exported="false"\n'
        '        android:configChanges="orientation|screenSize|keyboardHidden|screenLayout|smallestScreenSize|uiMode"\n'
        '        android:theme="@style/Theme.VoiceAssistant" />\n\n'
    )
    idx = m.rfind("</application>")
    if idx < 0:
        raise RuntimeError("</application> not found in manifest")
    m = m[:idx] + block + m[idx:]
    print(">> Registered SecurityActivity")
else:
    print(">> SecurityActivity already declared")
write(MANIFEST, m)

# ------------------------------------------- 5) Harden ArchitectureActivity
if os.path.exists(ARCH_ACTIVITY):
    with open(ARCH_ACTIVITY, "r", encoding="utf-8") as f:
        a = f.read()
    if "settings.allowFileAccess = true" in a:
        a = a.replace("settings.allowFileAccess = true", "settings.allowFileAccess = false", 1)
        write(ARCH_ACTIVITY, a)
        print(">> Hardened ArchitectureActivity WebView (allowFileAccess=false)")

print(">> Security Center Patch applied.")
print(">> Open it from anywhere with: startActivity(Intent(context, SecurityActivity::class.java))")

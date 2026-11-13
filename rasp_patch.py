import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
SECURITY_DIR = PKG_DIR + "/security"

print(">> Applying RASP (Runtime Self-Protection) Patch...")

# 1) إنشاء محرك الحماية الذاتية
os.makedirs(SECURITY_DIR, exist_ok=True)
monitor_code = r'''package com.zevorix.assistant.security

import android.content.Context
import android.os.Debug
import android.widget.Toast
import android.os.Build
import java.io.File
import java.net.Proxy
import java.net.ProxySelector

object SecurityMonitor {
    
    fun startMonitoring(context: Context) {
        var threatDetected = false
        val threats = mutableListOf<String>()

        if (isEmulator()) {
            threats.add("محاكي (Emulator)")
            threatDetected = true
        }
        if (isRooted()) {
            threats.add("صلاحيات روت (Root)")
            threatDetected = true
        }
        if (isDebuggerConnected()) {
            threats.add("أداة تصحيح (Debugger)")
            threatDetected = true
        }
        if (isProxySet()) {
            threats.add("اتصال غير آمن أو اعتراض شبكة (Proxy/VPN)")
            threatDetected = true
        }

        if (threatDetected) {
            val msg = "⚠️ تحذير أمني: تم كشف بيئة غير آمنة!\n" + threats.joinToString("\n")
            android.os.Handler(android.os.Looper.getMainLooper()).post {
                Toast.makeText(context, msg, Toast.LENGTH_LONG).show()
            }
            // يمكنك هنا إيقاف ميزات الذكاء الاصطناعي أو إغلاق التطبيق برمجياً
        }
    }

    private fun isEmulator(): Boolean {
        return (Build.FINGERPRINT.startsWith("generic")
                || Build.FINGERPRINT.startsWith("unknown")
                || Build.MODEL.contains("google_sdk")
                || Build.MODEL.contains("Emulator")
                || Build.MODEL.contains("Android SDK built for x86")
                || Build.MANUFACTURER.contains("Genymotion")
                || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
                || "google_sdk" == Build.PRODUCT)
    }

    private fun isRooted(): Boolean {
        val paths = arrayOf(
            "/system/app/Superuser.apk", "/sbin/su", "/system/bin/su", "/system/xbin/su",
            "/data/local/xbin/su", "/data/local/bin/su", "/system/sd/xbin/su",
            "/system/bin/failsafe/su", "/data/local/su", "/su/bin/su"
        )
        for (path in paths) {
            if (File(path).exists()) return true
        }
        return false
    }

    private fun isDebuggerConnected(): Boolean {
        return Debug.isDebuggerConnected() || Debug.waitingForDebugger()
    }

    private fun isProxySet(): Boolean {
        val proxyAddress = System.getProperty("http.proxyHost")
        val proxyPort = System.getProperty("http.proxyPort")
        if (proxyAddress != null && proxyPort != null) return true
        val proxy = ProxySelector.getDefault()?.select(java.net.URI("https://www.google.com"))
        if (proxy != null && proxy.isNotEmpty() && proxy[0].type() != Proxy.Type.DIRECT) {
            return true
        }
        return false
    }
}
'''
with open(os.path.join(SECURITY_DIR, "SecurityMonitor.kt"), "w", encoding="utf-8") as f:
    f.write(monitor_code)
print(">> Created SecurityMonitor.kt")

# 2) حقن الحماية في MainActivity
main_activity_path = PKG_DIR + "/MainActivity.kt"
if os.path.exists(main_activity_path):
    with open(main_activity_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    if "SecurityMonitor.startMonitoring" not in code:
        # إضافة منع تصوير الشاشة + تفعيل المراقب
        injection = """
        // 🛡️ RASP Protection & Anti-Screen Capture
        window.setFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE, android.view.WindowManager.LayoutParams.FLAG_SECURE)
        com.zevorix.assistant.security.SecurityMonitor.startMonitoring(this)
        """
        # حقن الكود بعد super.onCreate
        code = re.sub(r'(super\.onCreate\(savedInstanceState\))', r'\1\n' + injection, code, count=1)
        with open(main_activity_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
        print(">> Injected RASP into MainActivity (FLAG_SECURE enabled)")
    else:
        print("== MainActivity already protected")
else:
    print("!! WARNING: MainActivity.kt not found")

# 3) إضافة صلاحيات الشبكة للمانيفست
if os.path.exists(MANIFEST):
    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest = f.read()
    
    if "android.permission.ACCESS_NETWORK_STATE" not in manifest:
        manifest = manifest.replace("</manifest>", '    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />\n</manifest>')
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
            f.write(manifest)
        print(">> Added ACCESS_NETWORK_STATE permission")

print(">> RASP Patch applied successfully!")
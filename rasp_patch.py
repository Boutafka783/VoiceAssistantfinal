import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
SECURITY_DIR = PKG_DIR + "/security"

print(">> Applying RASP v2 (Anti-Spyware UI + Security Page)...")

# 1) إنشاء محرك الحماية الذاتية (يتحقق ويفتح شاشة التنبيه)
os.makedirs(SECURITY_DIR, exist_ok=True)
monitor_code = r'''package com.zevorix.assistant.security

import android.content.Context
import android.content.Intent
import android.os.Debug
import android.os.Build
import java.io.File
import java.net.Proxy
import java.net.ProxySelector

object SecurityMonitor {
    
    fun startMonitoring(context: Context) {
        val threats = mutableListOf<String>()

        if (isEmulator()) threats.add("تشغيل على محاكي (Emulator)")
        if (isRooted()) threats.add("الهاتف مروت (Root) - يمكن التجسس على البيانات")
        if (isDebuggerConnected()) threats.add("محاولة ربط أداة تصحيح (Debugger)")
        if (isProxySet()) threats.add("شبكة غير آمنة أو برنامج تجسس (Proxy/VPN)")

        // إذا وجد أي خطر، نفتح صفحة التنبيه الأمني فوراً
        if (threats.isNotEmpty()) {
            val intent = Intent(context, SecurityAlertActivity::class.java).apply {
                putStringArrayListExtra("threats", ArrayList(threats))
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
            }
            context.startActivity(intent)
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
        for (path in paths) { if (File(path).exists()) return true }
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

# 2) إنشاء شاشة التنبيه الأمني (SecurityAlertActivity)
alert_code = r'''package com.zevorix.assistant.security

import android.app.Activity
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast

class SecurityAlertActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // منع تصوير الشاشة في صفحة التنبيه
        window.setFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE, android.view.WindowManager.LayoutParams.FLAG_SECURE)

        val threats = intent.getStringArrayListExtra("threats") ?: arrayListOf("تهديد غير معروف")

        val scroll = ScrollView(this)
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(50, 150, 50, 50)
            setBackgroundColor(Color.parseColor("#B71C1C")) // لون أحمر داكن
            gravity = Gravity.CENTER_HORIZONTAL
        }

        val title = TextView(this).apply {
            text = "⚠️ تحذير أمني خطير!"
            textSize = 28f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 40)
        }

        val desc = TextView(this).apply {
            text = "لقد اكتشف النظام محاولة تجسس أو بيئة غير آمنة. لحماية بياناتك ومحادثاتك، قد يتم إيقاف بعض الميزات:"
            textSize = 18f
            setTextColor(Color.parseColor("#FFCDD2"))
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 30)
        }

        layout.addView(title)
        layout.addView(desc)

        threats.forEach { threat ->
            val tView = TextView(this).apply {
                text = "• $threat"
                textSize = 20f
                setTextColor(Color.WHITE)
                setPadding(0, 10, 0, 10)
                gravity = Gravity.RIGHT
            }
            layout.addView(tView)
        }

        val btn = Button(this).apply {
            text = "أوافق على المخاطرة والمتابعة"
            textSize = 16f
            setBackgroundColor(Color.WHITE)
            setTextColor(Color.parseColor("#B71C1C"))
            setPadding(30, 20, 30, 20)
            setOnClickListener { finish() }
        }
        
        val btnLayout = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply { setMargins(0, 60, 0, 0) }
        
        layout.addView(btn, btnLayout)
        scroll.addView(layout)
        setContentView(scroll)
    }
}
'''
with open(os.path.join(SECURITY_DIR, "SecurityAlertActivity.kt"), "w", encoding="utf-8") as f:
    f.write(alert_code)
print(">> Created SecurityAlertActivity.kt")

# 3) حقن الحماية في MainActivity
main_activity_path = PKG_DIR + "/MainActivity.kt"
if os.path.exists(main_activity_path):
    with open(main_activity_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    if "SecurityMonitor.startMonitoring" not in code:
        injection = """
        // 🛡️ RASP Protection & Anti-Screen Capture
        window.setFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE, android.view.WindowManager.LayoutParams.FLAG_SECURE)
        com.zevorix.assistant.security.SecurityMonitor.startMonitoring(this)
        """
        code = re.sub(r'(super\.onCreate\(savedInstanceState\))', r'\1\n' + injection, code, count=1)
        with open(main_activity_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
        print(">> Injected RASP into MainActivity (FLAG_SECURE enabled)")
else:
    print("!! WARNING: MainActivity.kt not found")

# 4) تسجيل شاشة التنبيه في المانيفست
if os.path.exists(MANIFEST):
    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest = f.read()
    
    if "SecurityAlertActivity" not in manifest:
        block = (
            '    <!-- Security Alert Screen -->\n'
            '    <activity\n'
            '        android:name=".security.SecurityAlertActivity"\n'
            '        android:exported="false"\n'
            '        android:theme="@android:style/Theme.Material.NoActionBar" />\n\n'
            '</application>'
        )
        manifest = manifest.replace("</application>", block)
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
            f.write(manifest)
        print(">> Registered SecurityAlertActivity in Manifest")

    if "ACCESS_NETWORK_STATE" not in manifest:
        manifest = manifest.replace("</manifest>", '    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />\n</manifest>')
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
            f.write(manifest)
        print(">> Added ACCESS_NETWORK_STATE permission")

print(">> RASP v2 applied successfully!")
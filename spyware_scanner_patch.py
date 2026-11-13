import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
SECURITY_DIR = PKG_DIR + "/security"

print(">> Applying Anti-Spyware Scanner Patch...")

# 1) محرك فحص التطبيقات الخارجية
scanner_code = r'''package com.zevorix.assistant.security

import android.content.Context
import android.content.pm.PackageManager
import android.view.accessibility.AccessibilityManager
import android.accessibilityservice.AccessibilityServiceInfo
import android.app.admin.DevicePolicyManager
import android.provider.Settings

object SpywareScanner {
    data class Threat(val appName: String, val packageName: String, val reason: String)

    fun scan(context: Context): List<Threat> {
        val threats = mutableListOf<Threat>()
        val pm = context.packageManager

        // فحص 1: صلاحية إمكانية الوصول (Accessibility)
        val am = context.getSystemService(Context.ACCESSIBILITY_SERVICE) as AccessibilityManager
        val enabledServices = am.getEnabledAccessibilityServiceList(AccessibilityServiceInfo.FEEDBACK_ALL_MASK)
        for (service in enabledServices) {
            val pkg = service.resolveInfo.serviceInfo.packageName
            if (pkg != context.packageName) {
                val appName = getAppName(pm, pkg)
                if (!isKnownSafeApp(pkg)) {
                    threats.add(Threat(appName, pkg, "لديه صلاحية قراءة الشاشة (Accessibility) - يمكنه قراءة رسائل واتساب و فيسبوك"))
                }
            }
        }

        // فحص 2: صلاحية مدير الجهاز (Device Admin)
        val dpm = context.getSystemService(Context.DEVICE_POLICY_SERVICE) as DevicePolicyManager
        for (admin in dpm.activeAdmins) {
            val pkg = admin.packageName
            if (pkg != context.packageName && !isKnownSafeApp(pkg)) {
                val appName = getAppName(pm, pkg)
                threats.add(Threat(appName, pkg, "لديه صلاحية التحكم بالهاتف (Device Admin) - قد يمنع حذفه"))
            }
        }

        // فحص 3: صلاحية الرسم فوق التطبيقات (Overlays)
        if (Settings.canDrawOverlays(context)) {
            val installedApps = pm.getInstalledPackages(PackageManager.GET_PERMISSIONS)
            for (app in installedApps) {
                if (app.packageName == context.packageName) continue
                if (app.requestedPermissions?.contains(android.Manifest.permission.SYSTEM_ALERT_WINDOW) == true) {
                     if (!isKnownSafeApp(app.packageName)) {
                         threats.add(Threat(getAppName(pm, app.packageName), app.packageName, "لديه صلاحية الرسم فوق التطبيقات (Overlay) - قد يسرق كلمات المرور"))
                     }
                }
            }
        }

        return threats.distinctBy { it.packageName }
    }

    private fun getAppName(pm: PackageManager, pkg: String): String {
        return try {
            pm.getApplicationLabel(pm.getApplicationInfo(pkg, 0)).toString()
        } catch (e: Exception) { pkg }
    }

    private fun isKnownSafeApp(pkg: String): Boolean {
        val safeApps = listOf(
            "com.whatsapp", "com.facebook.katana", "com.instagram.android", 
            "com.google.android", "com.android", "com.samsung", "com.miui",
            "com.zevorix.assistant", "com.microsoft", "com.linkedin.android"
        )
        return safeApps.any { pkg.startsWith(it) }
    }
}
'''
os.makedirs(SECURITY_DIR, exist_ok=True)
with open(os.path.join(SECURITY_DIR, "SpywareScanner.kt"), "w", encoding="utf-8") as f:
    f.write(scanner_code)

# 2) واجهة مركز الأمان (SecurityCenterActivity)
ui_code = r'''package com.zevorix.assistant.security

import android.app.Activity
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

class SecurityCenterActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.setFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE, android.view.WindowManager.LayoutParams.FLAG_SECURE)

        val scroll = ScrollView(this)
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(40, 100, 40, 40)
            setBackgroundColor(Color.parseColor("#0a192f"))
            gravity = Gravity.CENTER_HORIZONTAL
        }

        val title = TextView(this).apply {
            text = "🛡️ مركز الأمان (Security Center)"
            textSize = 24f
            setTextColor(Color.parseColor("#64ffda"))
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 30)
        }

        val resultText = TextView(this).apply {
            text = "اضغط على الزر أدناه لفحص هاتفك بحثاً عن برامج تجسس تتجسس على واتساب أو الفيسبوك."
            textSize = 18f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 40)
        }

        val btn = Button(this).apply {
            text = "🔍 ابدأ الفحص الشامل"
            textSize = 18f
            setBackgroundColor(Color.parseColor("#64ffda"))
            setTextColor(Color.parseColor("#0a192f"))
            setPadding(30, 20, 30, 20)
            setOnClickListener {
                val threats = SpywareScanner.scan(this@SecurityCenterActivity)
                if (threats.isEmpty()) {
                    resultText.text = "✅ هاتفك آمن! لم يتم اكتشاف أي تطبيقات مشبوهة تتجسس على التطبيقات الأخرى."
                } else {
                    var res = "⚠️ تم اكتشاف ${threats.size} تطبيق مشبوه:\n\n"
                    threats.forEach {
                        res += "❌ ${it.appName}\nالسبب: ${it.reason}\n\n"
                    }
                    res += "ننصح بحذف هذه التطبيقات فوراً لحماية خصوصيتك."
                    resultText.text = res
                    resultText.setTextColor(Color.parseColor("#ff5555"))
                }
            }
        }

        layout.addView(title)
        layout.addView(resultText)
        layout.addView(btn)
        scroll.addView(layout)
        setContentView(scroll)
    }
}
'''
with open(os.path.join(SECURITY_DIR, "SecurityCenterActivity.kt"), "w", encoding="utf-8") as f:
    f.write(ui_code)

# 3) تسجيل الشاشة في المانيفست
if os.path.exists(MANIFEST):
    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest = f.read()
    
    if "SecurityCenterActivity" not in manifest:
        block = (
            '    <!-- Security Center Screen -->\n'
            '    <activity\n'
            '        android:name=".security.SecurityCenterActivity"\n'
            '        android:exported="false"\n'
            '        android:theme="@android:style/Theme.Material.NoActionBar" />\n\n'
            '</application>'
        )
        manifest = manifest.replace("</application>", block)
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
            f.write(manifest)

    if "QUERY_ALL_PACKAGES" not in manifest:
        manifest = manifest.replace("</manifest>", '    <uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" />\n</manifest>')
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
            f.write(manifest)

print(">> Anti-Spyware Scanner Patch applied successfully!")
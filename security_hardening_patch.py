import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
BUILD_GRADLE = "app/build.gradle"
PROGUARD = "app/proguard-rules.pro"

def read(p):
    if not os.path.exists(p): return ""
    with open(p, "r", encoding="utf-8") as f: return f.read()

def write(p, c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f: f.write(c)

print(">> Applying Security Hardening Patch (WebView & Manifest)...")

# 1) تأمين المانيفست
if os.path.exists(MANIFEST):
    m = read(MANIFEST)
    # منع النسخ الاحتياطي واستخراج البيانات
    if 'android:allowBackup="false"' not in m:
        m = m.replace('<application', '<application android:allowBackup="false" android:fullBackupContent="false"', 1)
    # تعطيل الاتصالات غير المشفرة
    if 'android:usesCleartextTraffic="false"' not in m:
        m = m.replace('<application', '<application android:usesCleartextTraffic="false"', 1)
    
    # تأمين جميع الأنشطة بمنع التصدير (exported="false") عدا الشاشة الرئيسية
    m = re.sub(r'(<activity[^>]*android:name="(?!"\.MainActivity")[^>]*)android:exported="true"', r'\1android:exported="false"', m)
    write(MANIFEST, m)
    print(">> Manifest secured (allowBackup=false, cleartext=false, activities locked)")

# 2) تفعيل تشفير الكود (Obfuscation) في Gradle
if os.path.exists(BUILD_GRADLE):
    bg = read(BUILD_GRADLE)
    if "minifyEnabled true" not in bg:
        bg = re.sub(r'minifyEnabled\s+false', 'minifyEnabled true', bg)
        bg = re.sub(r'shrinkResources\s+false', 'shrinkResources true', bg)
        write(BUILD_GRADLE, bg)
        print(">> Enabled R8 code obfuscation in build.gradle")
    
    # حماية دوال JavascriptInterface من المسح بواسطة R8
    if os.path.exists(PROGUARD):
        pg = read(PROGUARD)
        if "javascriptinterface" not in pg:
            pg += "\n# Keep JavascriptInterfaces for WebView\n-keepclassmembers class * {\n    @android.webkit.JavascriptInterface <methods>;\n}\n"
            write(PROGUARD, pg)
            print(">> Added ProGuard rules to protect JavascriptInterface")

# 3) تحصين ملفات الـ WebView (حقن درع الحماية)
html_files = [
    "app/src/main/assets/architecture_lab.html",
    "app/src/main/assets/flight_sim.html",
    "app/src/main/assets/circuit_sim.html",
    "app/src/main/assets/mech_sim.html"
]

# درع الحماية (Sanitizer)
sanitizer_js = """
// 🛡️ Security Sanitizer (Anti-XSS for AI Output)
function secureAIResponse(html) {
    if (!html) return "";
    return html
        .replace(/<script\\b[^<]*(?:(?!<\\/script>)<[^<]*)*<\\/script>/gi, "")
        .replace(/<iframe\\b[^<]*(?:(?!<\\/iframe>)<[^<]*)*<\\/iframe>/gi, "")
        .replace(/<object\\b[^<]*(?:(?!<\\/object>)<[^<]*)*<\\/object>/gi, "")
        .replace(/<embed\\b[^>]*>/gi, "")
        .replace(/javascript:/gi, "")
        .replace(/on\\w+\\s*=/gi, "");
}
"""

for hf in html_files:
    if os.path.exists(hf):
        h = read(hf)
        if "secureAIResponse" not in h:
            # حقن الدرع في بداية السكربت
            h = h.replace("<script>", "<script>\n" + sanitizer_js, 1)
            
            # استبدال الدوال التي تقوم بحقن كود الـ AI (innerHTML) لتمر عبر الفلتر
            # في العمارة: container.innerHTML = a
            h = re.sub(r'container\.innerHTML\s*=\s*([a-zA-Z0-9_]+);', r'container.innerHTML = secureAIResponse(\1);', h)
            h = re.sub(r'stage\.innerHTML\s*=\s*([a-zA-Z0-9_]+);', r'stage.innerHTML = secureAIResponse(\1);', h)
            
            write(hf, h)
            print(f">> Injected AI Anti-XSS Sanitizer into {hf}")

print(">> Security Hardening Patch applied successfully!")
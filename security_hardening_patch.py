import os
import re
import xml.etree.ElementTree as ET

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

print(">> Applying Security Hardening Patch (Safe XML)...")

# 1) تأمين المانيفست باستخدام ElementTree
if os.path.exists(MANIFEST):
    # تعريف مساحات الأسماء
    ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
    ET.register_namespace('tools', 'http://schemas.android.com/tools')
    
    tree = ET.parse(MANIFEST)
    root = tree.getroot()
    app_node = root.find('application')
    
    if app_node is not None:
        # إضافة سمات الأمان
        app_node.set('{http://schemas.android.com/apk/res/android}allowBackup', 'false')
        app_node.set('{http://schemas.android.com/apk/res/android}usesCleartextTraffic', 'false')
        # إضافة tools:replace لتجنب تعارض المكتبات
        app_node.set('{http://schemas.android.com/tools}replace', 'android:allowBackup,android:usesCleartextTraffic')
        
        # حفظ الملف
        tree.write(MANIFEST, encoding='utf-8', xml_declaration=True)
        print(">> Manifest secured safely with tools:replace")
    else:
        print("!! ERROR: <application> tag not found in manifest")

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
            h = h.replace("<script>", "<script>\n" + sanitizer_js, 1)
            h = re.sub(r'container\.innerHTML\s*=\s*([a-zA-Z0-9_]+);', r'container.innerHTML = secureAIResponse(\1);', h)
            h = re.sub(r'stage\.innerHTML\s*=\s*([a-zA-Z0-9_]+);', r'stage.innerHTML = secureAIResponse(\1);', h)
            write(hf, h)
            print(f">> Injected AI Anti-XSS Sanitizer into {hf}")

print(">> Security Hardening Patch applied successfully!")
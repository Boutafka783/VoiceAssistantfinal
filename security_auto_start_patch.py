#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security_auto_start_patch.py — تفعيل المراقبة الأمنية تلقائياً (Option C)
يشغّل بعد security_patch.py.
- يفعل SecurityMonitor عند فتح التطبيق (لا يكرر إن كان مفعّلاً)
- يطلب إذن الإشعارات (Android 13+) بأدب
- يشغّل فحصاً أولياً لبناء خط الأساس (صامت)
- لا يفشل البناء إن لم يجد نشاطاً — يحذّر فقط
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("PROJECT_DIR", ".")).resolve()
PKG_DIR = ROOT / "app" / "src" / "main" / "java" / "com" / "zevorix" / "assistant"

MARKER = "// SECURITY_AUTO_START_V1"

# كود التفعيل التلقائي — مضاف داخل onCreate()
AUTO_START_CODE = '''
        // SECURITY_AUTO_START_V1: تفعيل المراقبة الأمنية تلقائياً (Option C)
        try {
            val notifGranted = if (android.os.Build.VERSION.SDK_INT >= 33) {
                checkSelfPermission("android.permission.POST_NOTIFICATIONS") ==
                    android.content.pm.PackageManager.PERMISSION_GRANTED
            } else true
            if (!notifGranted) {
                try {
                    requestPermissions(arrayOf("android.permission.POST_NOTIFICATIONS"), 1001)
                } catch (e: Exception) { }
            }
            if (!com.zevorix.assistant.SecurityMonitor.isOn(this)) {
                com.zevorix.assistant.SecurityMonitor.enable(this)
                Thread {
                    try {
                        com.zevorix.assistant.SecurityMonitor.run(applicationContext)
                    } catch (e: Exception) { }
                }.start()
            }
        } catch (e: Exception) { }
'''


def die(msg):
    print("security_auto_start_patch.py: " + msg, file=sys.stderr)
    sys.exit(1)


def find_application_class():
    """يبحث عن Application class (أفضل موضع: يعمل مرة واحدة لكل عملية)"""
    for pattern in ("*App.kt", "*Application.kt"):
        for f in PKG_DIR.glob(pattern):
            try:
                text = f.read_text(encoding="utf-8")
                if re.search(r':\s*Application\s*\(\s*\)', text):
                    return f
            except Exception:
                pass
    return None


def find_main_activity():
    """يبحث عن نشاط launcher (يحتوي setContent أو setContentView)"""
    candidates = [
        PKG_DIR / "MainActivity.kt",
        PKG_DIR / "ui" / "MainActivity.kt",
    ]
    for c in candidates:
        if c.is_file():
            return c
    for f in PKG_DIR.rglob("*.kt"):
        try:
            text = f.read_text(encoding="utf-8")
            if ("setContent {" in text or "setContentView(" in text) and \
               re.search(r':\s*(ComponentActivity|AppCompatActivity|Activity)\s*\(\s*\)', text):
                return f
        except Exception:
            pass
    return None


def patch_file(file_path):
    """يدخل كود التفعيل بعد super.onCreate()"""
    text = file_path.read_text(encoding="utf-8")

    if MARKER in text:
        print(f">> {file_path.name}: التفعيل التلقائي موجود مسبقاً. لا تعديل.")
        return True

    # ابحث عن onCreate + super.onCreate
    m = re.search(
        r'override\s+fun\s+onCreate\s*\([^)]*\)\s*\{[^}]*?super\.onCreate\([^)]*\)',
        text
    )
    if not m:
        print(f"⚠️  {file_path.name}: لم أجد onCreate/super.onCreate — تخطّي")
        return False

    insert_pos = m.end()
    new_text = text[:insert_pos] + "\n" + AUTO_START_CODE + text[insert_pos:]

    file_path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f">> ✅ {file_path.name}: أُضيف التفعيل التلقائي")
    return True


def verify_prerequisites():
    """يتحقق من أن security_patch.py أنجز مهامه"""
    errors = []
    if not (PKG_DIR / "SecurityActivity.kt").is_file():
        errors.append("SecurityActivity.kt مفقود — شغّل security_patch.py أولاً")
    if not (PKG_DIR / "SecurityMonitorService.kt").is_file():
        errors.append("SecurityMonitorService.kt مفقود")

    manifest_path = ROOT / "app" / "src" / "main" / "AndroidManifest.xml"
    if manifest_path.is_file():
        manifest = manifest_path.read_text(encoding="utf-8")
        for perm in ("POST_NOTIFICATIONS", "RECEIVE_BOOT_COMPLETED"):
            if perm not in manifest:
                errors.append(f"{perm} مفقود من المانيفست")
    return errors


def main():
    if not PKG_DIR.is_dir():
        die(f"لم أجد الحزمة في {PKG_DIR}")

    errors = verify_prerequisites()
    if errors:
        print("❌ متطلبات ناقصة:")
        for e in errors:
            print(f"   - {e}")
        sys.exit(1)

    # جرّب Application class أولاً (يعمل مرة واحدة لكل عملية — أفضل)
    app_class = find_application_class()
    main_activity = find_main_activity()

    patched = False
    if app_class:
        print(f">> سأستخدم Application class: {app_class.relative_to(ROOT)}")
        patched = patch_file(app_class)
    elif main_activity:
        print(f">> سأستخدم Main Activity: {main_activity.relative_to(ROOT)}")
        patched = patch_file(main_activity)
    else:
        die("لم أجد لا Application class ولا Main Activity — لا يمكن التفعيل التلقائي")

    if not patched:
        die("فشل إدخال كود التفعيل")

    print(">> security_auto_start_patch.py: اكتمل بنجاح.")
    print(">> النتيجة: المراقبة تبدأ تلقائياً عند أول فتح للتطبيق.")


if __name__ == "__main__":
    main()
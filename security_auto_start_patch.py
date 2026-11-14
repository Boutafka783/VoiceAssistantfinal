import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MARKER = "SECURITY_AUTO_START_V1"

INJECT = '''
        // ''' + MARKER + '''
        // تفعيل مراقبة الأمان تلقائياً مرة واحدة فقط (إن عطّلها المستخدم لاحقاً لا تُفعَّل من جديد)
        try {
            val secPrefs = com.zevorix.assistant.SecurityStore.prefs(this)
            if (!secPrefs.getBoolean("auto_started", false)) {
                secPrefs.edit().putBoolean("auto_started", true).apply()
                com.zevorix.assistant.SecurityMonitor.enable(this)
                if (android.os.Build.VERSION.SDK_INT >= 33 &&
                    checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 7302)
                }
            }
        } catch (e: Exception) { }
'''

ONCREATE_RE = re.compile(r"override\s+fun\s+onCreate\s*\(\s*(\w+)\s*:\s*Bundle\?\s*\)\s*\{")


def find_main_activity():
    for root, _, files in os.walk(PKG_DIR):
        for fn in files:
            if not fn.endswith(".kt"):
                continue
            p = os.path.join(root, fn)
            with open(p, "r", encoding="utf-8") as f:
                s = f.read()
            if re.search(r"class\s+MainActivity\b", s) and ONCREATE_RE.search(s):
                return p, s
    return None, None


# إن كان الوسم موجوداً مسبقاً فلا شيء نفعله
for root, _, files in os.walk(PKG_DIR):
    for fn in files:
        if fn.endswith(".kt"):
            with open(os.path.join(root, fn), "r", encoding="utf-8") as f:
                if MARKER in f.read():
                    print("== auto-start already present in " + fn)
                    sys.exit(0)

path, s = find_main_activity()
if path is None:
    print("ERROR: MainActivity.kt with onCreate(Bundle?) not found under " + PKG_DIR)
    sys.exit(1)

m = ONCREATE_RE.search(s)
bundle = m.group(1)
pos = m.end()
sup = re.compile(r"super\.onCreate\s*\(\s*" + re.escape(bundle) + r"\s*\)").search(s, m.end())
if sup:
    nl = s.find("\n", sup.end())
    pos = len(s) if nl == -1 else nl

s = s[:pos] + "\n" + INJECT + s[pos:]
with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
print("OK auto-start injected into " + path)

import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"
MANIFEST = "app/src/main/AndroidManifest.xml"

# (marker, label_ar, label_en, emoji, activity, manifest_required)
ITEMS = [
    ("FlightSimActivity",    "مختبر هندسة الطيران", "Aerospace Engineering Lab", "✈️", "FlightSimActivity",     True),
    ("ArchitectureActivity", "هندسة المباني",        "Architecture Lab",          "🏛️", "ArchitectureActivity",  True),
    ("SecurityActivity",     "مركز الأمان",          "Security Center",           "🛡️", "SecurityActivity",     False),
]

def item_code(ar, en, emoji, act, reset_var):
    # إصلاح 1: استخدام setClassName بدلاً من ::class.java لتجنب أخطاء الترجمة
    # إصلاح 2: إضافة فاصلة (,) في نهاية العنصر لمنع أخطاء Syntax
    return (
        "\n                DropdownMenuItem(\n"
        f'                    text = {{ Text(state.language.tr("{ar}", "{en}")) }},\n'
        f'                    leadingIcon = {{ Text("{emoji}", style = androidx.compose.ui.text.TextStyle(fontSize = androidx.compose.ui.unit.TextUnit(20f, androidx.compose.ui.unit.TextUnitType.Sp))) }},\n'
        "                    onClick = {\n"
        f"                        {reset_var} = false\n"
        f"                        val intent = android.content.Intent()\n"
        f"                        intent.setClassName(context, \"com.zevorix.assistant.{act}\")\n"
        f"                        context.startActivity(intent)\n"
        "                    }\n"
        "                ),\n"
    )

def matching_paren(s, open_idx):
    depth, i, in_str = 0, open_idx, False
    while i < len(s):
        c = s[i]
        if in_str:
            if c == "\\": i += 1
            elif c == '"': in_str = False
        else:
            if c == '"': in_str = True
            elif c == "(": depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0: return i
        i += 1
    return -1

def detect_reset_var(s):
    m = re.search(r"onDismissRequest\s*=\s*\{\s*(\w+)\s*=\s*false", s)
    if m: return m.group(1)
    m = re.search(r"(\w+)\s*=\s*false\s*\n\s*\}\s*\)\s*\{", s)
    if m: return m.group(1)
    return "showSettingsMenu"

def find_insert_point(s):
    for marker in ("Robot Lab", "Mechanical Lab", "Electronics Lab", "مختبر الإلكترونيات"):
        m = s.find(marker)
        if m != -1:
            start = s.rfind("DropdownMenuItem(", 0, m)
            if start != -1:
                end = matching_paren(s, start + len("DropdownMenuItem"))
                if end != -1:
                    return end + 1, f"after '{marker}' item"
    m = re.search(r"onDismissRequest\s*=\s*\{\s*\w+\s*=\s*false\s*\}\s*\)\s*\{", s)
    if m:
        return m.end(), "start of settings menu (regex)"
    return None, None

if not os.path.exists(MAIN_SCREEN):
    print("ERROR: MainScreen.kt not found"); sys.exit(1)

with open(MAIN_SCREEN, "r", encoding="utf-8") as f:
    s = f.read()

reset_var = detect_reset_var(s)
print(f">> detected menu reset variable: {reset_var}")

added = []
for marker, ar, en, emoji, act, mreq in ITEMS:
    # البحث عن اسم الكلاس فقط لتجنب التكرار
    if f'com.zevorix.assistant.{act}"' in s or f'{act}::class.java' in s:
        print(f"== {act}: menu item already present"); continue
    
    pos, how = find_insert_point(s)
    if pos is None:
        print("ERROR: no insertion point found in MainScreen.kt.")
        sys.exit(1)
    
    s = s[:pos] + item_code(ar, en, emoji, act, reset_var) + s[pos:]
    added.append(f"{act} -> {how}")

# إصلاح 3: طريقة مضمونة 100% لإضافة متغير context داخل Composable
if "val context" not in s:
    idx = s.find("fun MainScreen(")
    if idx != -1:
        brace = s.find("{", idx)
        if brace != -1:
            s = s[:brace+1] + "\n    val context = androidx.compose.ui.platform.LocalContext.current\n" + s[brace+1:]
            print(">> Added 'context' variable inside MainScreen")
    else:
        print("WARNING: Could not auto-add context. Check MainScreen.kt manually.")

with open(MAIN_SCREEN, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)

for a in added: print("OK menu item:", a)

# فحص نهائي
manifest = open(MANIFEST, encoding="utf-8").read() if os.path.exists(MANIFEST) else ""
missing = []
for _, _, _, _, act, mreq in ITEMS:
    ok_menu = (f'com.zevorix.assistant.{act}"' in s) or (f"{act}::class.java" in s)
    ok_man = f".{act}" in manifest
    print(f"CHECK {act}: menu={ok_menu} manifest={ok_man}{' (required)' if mreq else ' (deferred)'}")
    if not ok_menu:
        missing.append(f"{act} (menu)")
    if mreq and not ok_man:
        missing.append(f"{act} (manifest)")

if missing:
    print("ERROR missing:", ", ".join(missing))
    sys.exit(1)
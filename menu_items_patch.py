import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"
MANIFEST = "app/src/main/AndroidManifest.xml"

# (marker, label_ar, label_en, emoji, activity, manifest_required)
# manifest_required=False → لا يفشل لو كان النشاط غير مسجّل بعد
ITEMS = [
    ("FlightSimActivity",    "مختبر هندسة الطيران", "Aerospace Engineering Lab", "✈️", "FlightSimActivity",     True),
    ("ArchitectureActivity", "هندسة المباني",        "Architecture Lab",          "🏛️", "ArchitectureActivity",  True),
    ("SecurityActivity",     "مركز الأمان",          "Security Center",           "🛡️", "SecurityActivity",     False),
]


def item_code(ar, en, emoji, act, reset_var):
    return (
        "\n                DropdownMenuItem(\n"
        f'                    text = {{ Text(state.language.tr("{ar}", "{en}")) }},\n'
        f'                    leadingIcon = {{ Text("{emoji}", style = androidx.compose.ui.text.TextStyle(fontSize = androidx.compose.ui.unit.TextUnit(20f, androidx.compose.ui.unit.TextUnitType.Sp))) }},\n'
        "                    onClick = {\n"
        f"                        {reset_var} = false\n"
        f"                        context.startActivity(android.content.Intent(context, com.zevorix.assistant.{act}::class.java))\n"
        "                    }\n"
        "                )\n"
    )


def matching_paren(s, open_idx):
    """index of ')' matching the '(' at open_idx (skips string literals)."""
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
    """يستخرج اسم متغيّر إغلاق القائمة بدل افتراض showSettingsMenu."""
    m = re.search(r"onDismissRequest\s*=\s*\{\s*(\w+)\s*=\s*false", s)
    if m: return m.group(1)
    m = re.search(r"(\w+)\s*=\s*false\s*\n\s*\}\s*\)\s*\{", s)
    if m: return m.group(1)
    return "showSettingsMenu"  # fallback


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
    m = s.find("Scan apps")
    if m != -1:
        start = s.rfind("DropdownMenuItem(", 0, m)
        if start != -1:
            return start, "before 'Scan apps' item"
    return None, None


if not os.path.exists(MAIN_SCREEN):
    print("ERROR: MainScreen.kt not found"); sys.exit(1)

with open(MAIN_SCREEN, "r", encoding="utf-8") as f:
    s = f.read()

reset_var = detect_reset_var(s)
print(f">> detected menu reset variable: {reset_var}")

added = []
for marker, ar, en, emoji, act, mreq in ITEMS:
    if f"{act}::class.java" in s:
        print(f"== {act}: menu item already present"); continue
    pos, how = find_insert_point(s)
    if pos is None:
        print("ERROR: no insertion point found in MainScreen.kt. Region around reset var:")
        i = s.find(reset_var)
        print(s[max(0, i-300): i+700] if i != -1 else f"({reset_var} not found)")
        sys.exit(1)
    s = s[:pos] + item_code(ar, en, emoji, act, reset_var) + s[pos:]
    added.append(f"{act} -> {how}")

if "val context" not in s:
    s2 = re.sub(r"(val state by viewModel\.uiState\.collectAsStateWithLifecycle\(\)\n)",
                r"\1    val context = androidx.compose.ui.platform.LocalContext.current\n", s, count=1)
    if s2 == s:
        print("WARNING: 'context' variable not found and could not be added — Security/Architecture buttons may crash at runtime")
    s = s2

with open(MAIN_SCREEN, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)

for a in added: print("OK menu item:", a)

# فحص نهائي: القائمة والمانيفست (مع مرونة للأنشطة التي تُسجَّل لاحقاً)
manifest = open(MANIFEST, encoding="utf-8").read() if os.path.exists(MANIFEST) else ""
missing = []
for _, _, _, _, act, mreq in ITEMS:
    ok_menu = f"{act}::class.java" in s
    ok_man = f".{act}" in manifest
    print(f"CHECK {act}: menu={ok_menu} manifest={ok_man}{' (required)' if mreq else ' (deferred)'}")
    if not ok_menu:
        missing.append(f"{act} (menu)")
    if mreq and not ok_man:
        missing.append(f"{act} (manifest)")
if missing:
    print("ERROR missing:", ", ".join(missing))
    sys.exit(1)
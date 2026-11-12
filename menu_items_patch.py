import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"

# (marker, label_ar, label_en, icon, activity)
ITEMS = [
    ("FlightSimActivity",     "مختبر هندسة الطيران", "Aerospace Engineering Lab", "FlightTakeoff", "FlightSimActivity"),
    ("ArchitectureActivity",  "هندسة المباني",       "Architecture Lab",          "Apartment",     "ArchitectureActivity"),
]

def item_code(ar, en, icon, act):
    return (
        "\n                DropdownMenuItem(\n"
        f'                    text = {{ Text(state.language.tr("{ar}", "{en}")) }},\n'
        f"                    leadingIcon = {{ Icon(androidx.compose.material.icons.Icons.Filled.{icon}, contentDescription = null) }},\n"
        "                    onClick = {\n"
        "                        showSettingsMenu = false\n"
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

def find_insert_point(s):
    # 1) بعد عنصر "Robot Lab" مباشرة
    for marker in ("Robot Lab", "Mechanical Lab"):
        m = s.find(marker)
        if m != -1:
            start = s.rfind("DropdownMenuItem(", 0, m)
            if start != -1:
                end = matching_paren(s, start + len("DropdownMenuItem"))
                if end != -1:
                    return end + 1, f"after '{marker}' item"
    # 2) بداية القائمة (مرساة مرنة بالمسافات)
    m = re.search(r"onDismissRequest\s*=\s*\{\s*showSettingsMenu\s*=\s*false\s*\}\s*\)\s*\{", s)
    if m:
        return m.end(), "start of settings menu (regex)"
    # 3) قبل أول عنصر "Scan apps"
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

added = []
for marker, ar, en, icon, act in ITEMS:
    if f"{act}::class.java" in s:
        print(f"== {act}: menu item already present"); continue
    pos, how = find_insert_point(s)
    if pos is None:
        print("ERROR: no insertion point found in MainScreen.kt. Region around 'showSettingsMenu':")
        i = s.find("showSettingsMenu")
        print(s[max(0, i-300): i+700] if i != -1 else "(showSettingsMenu not found)")
        sys.exit(1)
    s = s[:pos] + item_code(ar, en, icon, act) + s[pos:]
    added.append(f"{act} -> {how}")

if "val context" not in s:
    s2 = re.sub(r"(val state by viewModel\.uiState\.collectAsStateWithLifecycle\(\)\n)",
                r"\1    val context = androidx.compose.ui.platform.LocalContext.current\n", s, count=1)
    if s2 == s:
        print("WARNING: 'context' variable not found and could not be added")
    s = s2

with open(MAIN_SCREEN, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)

for a in added: print("OK menu item:", a)

# تحقق نهائي: يجب أن تكون الأنشطة موجودة في القائمة وفي المانيفست
manifest = open("app/src/main/AndroidManifest.xml", encoding="utf-8").read()
for _, _, _, _, act in ITEMS:
    ok_menu = f"{act}::class.java" in s
    ok_man = f".{act}" in manifest
    print(f"CHECK {act}: menu={ok_menu} manifest={ok_man}")
    if not (ok_menu and ok_man): sys.exit(1)

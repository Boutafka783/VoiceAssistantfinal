import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"
MANIFEST = "app/src/main/AndroidManifest.xml"

ACT = "SecurityActivity"
LABEL_AR = "مركز الأمان"
LABEL_EN = "Security Center"
EMOJI = "🛡️"
MARKER = "SECURITY_MENU_ITEM_V1"


def item_code():
    # استدعاء مباشر ::class.java (بدون Class.forName) كي لا يتأثر بتشويه R8
    return (
        "\n                // " + MARKER + "\n"
        "                DropdownMenuItem(\n"
        f'                    text = {{ Text(state.language.tr("{LABEL_AR}", "{LABEL_EN}")) }},\n'
        f'                    leadingIcon = {{ Text("{EMOJI}", style = androidx.compose.ui.text.TextStyle(fontSize = androidx.compose.ui.unit.TextUnit(20f, androidx.compose.ui.unit.TextUnitType.Sp))) }},\n'
        "                    onClick = {\n"
        "                        showSettingsMenu = false\n"
        f"                        context.startActivity(android.content.Intent(context, com.zevorix.assistant.{ACT}::class.java))\n"
        "                    }\n"
        "                )\n"
    )


def matching_paren(s, open_idx):
    """index of ')' matching the '(' at open_idx (skips string literals)."""
    depth, i, in_str = 0, open_idx, False
    while i < len(s):
        c = s[i]
        if in_str:
            if c == "\\":
                i += 1
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def find_insert_point(s):
    # 1) بعد عنصر Robot/Mechanical Lab
    for marker in ("Robot Lab", "Mechanical Lab"):
        m = s.find(marker)
        if m != -1:
            start = s.rfind("DropdownMenuItem(", 0, m)
            if start != -1:
                end = matching_paren(s, start + len("DropdownMenuItem"))
                if end != -1:
                    return end + 1, "after '" + marker + "' item"
    # 2) بداية قائمة الإعدادات
    m = re.search(r"onDismissRequest\s*=\s*\{\s*showSettingsMenu\s*=\s*false\s*\}\s*\)\s*\{", s)
    if m:
        return m.end(), "start of settings menu"
    # 3) قبل أول عنصر Scan apps
    m = s.find("Scan apps")
    if m != -1:
        start = s.rfind("DropdownMenuItem(", 0, m)
        if start != -1:
            return start, "before 'Scan apps' item"
    return None, None


if not os.path.exists(MAIN_SCREEN):
    print("ERROR: MainScreen.kt not found:", MAIN_SCREEN)
    sys.exit(1)

with open(MAIN_SCREEN, "r", encoding="utf-8") as f:
    s = f.read()

if MARKER in s or (ACT + "::class.java") in s:
    print("== " + ACT + ": menu item already present")
else:
    pos, how = find_insert_point(s)
    if pos is None:
        print("ERROR: no insertion point found. Region around 'showSettingsMenu':")
        i = s.find("showSettingsMenu")
        print(s[max(0, i - 300): i + 700] if i != -1 else "(showSettingsMenu not found)")
        sys.exit(1)
    s = s[:pos] + item_code() + s[pos:]
    print("OK menu item: " + ACT + " -> " + how)

# متغير context مطلوب لـ startActivity
if not re.search(r"\bval\s+context\b", s):
    s2 = re.sub(
        r"(val state by viewModel\.uiState\.collectAsStateWithLifecycle\(\)\n)",
        r"\1    val context = androidx.compose.ui.platform.LocalContext.current\n",
        s, count=1)
    if s2 == s:
        print("ERROR: 'context' variable not found and could not be added")
        sys.exit(1)
    s = s2
    print("OK added: val context")

with open(MAIN_SCREEN, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)

# تحقق نهائي: القائمة + المانيفست
manifest = open(MANIFEST, encoding="utf-8").read() if os.path.exists(MANIFEST) else ""
ok_menu = (ACT + "::class.java") in s
ok_man = ("." + ACT) in manifest
print("CHECK " + ACT + ": menu=" + str(ok_menu) + " manifest=" + str(ok_man))
if not (ok_menu and ok_man):
    sys.exit(1)
print("Security Center menu item injected.")

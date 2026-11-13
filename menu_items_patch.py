import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"
MANIFEST = "app/src/main/AndroidManifest.xml"

# (label_ar, label_en, icon, activity)
ITEMS = [
    ("مختبر هندسة الطيران", "Aerospace Engineering Lab", "FlightTakeoff", "FlightSimActivity"),
    ("هندسة المباني",       "Architecture Lab",          "Apartment",     "ArchitectureActivity"),
]

# ---------------------------------------------------------------------------
# Kotlin-aware scanner: skips "..." / """...""" (with ${...} templates), '.' chars,
# // line comments and (nested) /* */ block comments while matching brackets.
# ---------------------------------------------------------------------------
def skip_literal(s, i):
    """If a string/char/comment starts at s[i], return the index just after it; otherwise return i."""
    n = len(s)
    if s.startswith("//", i):
        j = s.find("\n", i)
        return n if j == -1 else j
    if s.startswith("/*", i):
        depth, j = 1, i + 2
        while j < n and depth:
            if s.startswith("/*", j): depth += 1; j += 2
            elif s.startswith("*/", j): depth -= 1; j += 2
            else: j += 1
        return j
    if s.startswith('"""', i):
        j = i + 3
        while j < n:
            if s.startswith("${", j):
                j = match_close(s, j + 1) + 1
                if j <= 0: return n
            elif s.startswith('"""', j):
                j += 3
                while j < n and s[j] == '"': j += 1   # \"\"\"\" edge case
                return j
            else: j += 1
        return n
    if s[i] == '"':
        j = i + 1
        while j < n:
            c = s[j]
            if c == "\\": j += 2
            elif s.startswith("${", j):
                j = match_close(s, j + 1) + 1
                if j <= 0: return n
            elif c == '"': return j + 1
            elif c == "\n": return j          # unterminated: bail out at EOL
            else: j += 1
        return n
    if s[i] == "'":
        if s.startswith("'\\", i):
            j = s.find("'", i + 3)
            return i + 3 if j == -1 else j + 1
        if i + 2 < n and s[i + 2] == "'":
            return i + 3
    return i


def match_close(s, open_idx):
    """Index of the bracket closing the one at open_idx ('(' or '{' or '['); -1 if unbalanced."""
    open_c = s[open_idx]
    close_c = {"(": ")", "{": "}", "[": "]"}[open_c]
    depth, i, n = 0, open_idx, len(s)
    while i < n:
        j = skip_literal(s, i)
        if j != i:
            i = j
            continue
        c = s[i]
        if c == open_c: depth += 1
        elif c == close_c:
            depth -= 1
            if depth == 0: return i
        i += 1
    return -1


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


def item_span_containing(s, idx):
    """(start, end_exclusive) of the DropdownMenuItem( ... ) call that contains idx, or None."""
    pos = idx
    while True:
        start = s.rfind("DropdownMenuItem(", 0, pos)
        if start == -1: return None
        end = match_close(s, start + len("DropdownMenuItem"))
        if end != -1 and start < idx < end:
            return start, end + 1
        pos = start


def find_insert_point(s):
    # 1) right after the Robot Lab (or Mechanical Lab) item
    for marker in ("Robot Lab", "Mechanical Lab"):
        for m in re.finditer(re.escape(marker), s):
            span = item_span_containing(s, m.start())
            if span: return span[1], f"after '{marker}' item"
    # 2) start of the settings DropdownMenu content (whitespace tolerant)
    m = re.search(r"onDismissRequest\s*=\s*\{\s*showSettingsMenu\s*=\s*false\s*\}\s*\)\s*\{", s)
    if m: return m.end(), "start of settings menu (regex)"
    # 3) before the 'Scan apps' item
    i = s.find("Scan apps")
    if i != -1:
        span = item_span_containing(s, i)
        if span: return span[0], "before 'Scan apps' item"
    return None, None


def enclosing_function(s, pos):
    """(params_open, params_close, body_open, body_close) of the innermost fun whose block body contains pos."""
    best = None
    for m in re.finditer(r"\bfun\s+(?:<[^>]*>\s*)?(?:[\w.]+\.)?\w+\s*\(", s):
        p_open = m.end() - 1
        p_close = match_close(s, p_open)
        if p_close == -1: continue
        t = re.compile(r"\s*(?::\s*[^={\n]+)?\s*\{").match(s, p_close + 1)
        if not t: continue                      # expression-bodied fun
        b_open = t.end() - 1
        b_close = match_close(s, b_open)
        if b_close != -1 and b_open < pos < b_close:
            if best is None or b_open > best[2]:
                best = (p_open, p_close, b_open, b_close)
    return best


def ensure_icon_imports(s):
    """Icons.Filled.<Name> are extension properties: they need an explicit import even when Icons is fully qualified."""
    for _, _, icon, _ in ITEMS:
        imp = f"import androidx.compose.material.icons.filled.{icon}"
        if re.search(r"(?m)^" + re.escape(imp) + r"\s*$", s):
            continue
        first = re.search(r"(?m)^import ", s)
        if first:
            s = s[:first.start()] + imp + "\n" + s[first.start():]
        else:
            pk = re.search(r"(?m)^package\s+[^\n]+\n", s)
            if not pk:
                raise RuntimeError("Cannot place icon import: no package line / imports in MainScreen.kt")
            s = s[:pk.end()] + "\n" + imp + "\n" + s[pk.end():]
        print("INFO: added", imp)
    return s


if not os.path.exists(MAIN_SCREEN):
    raise RuntimeError("MainScreen.kt not found")

with open(MAIN_SCREEN, "r", encoding="utf-8") as f:
    s = f.read()

# ---- preconditions: fail with a clear message instead of a confusing compile error ----
if "state.language.tr(" not in s:
    raise RuntimeError("state.language.tr(...) signature not found - menu labels will not compile. Verify uiState API.")
if "showSettingsMenu" not in s:
    raise RuntimeError("showSettingsMenu not found in MainScreen.kt - menu items would not compile. Verify the menu state variable name.")

first_pos = None
added = []
for ar, en, icon, act in ITEMS:
    if f"{act}::class.java" in s:
        print(f"== {act}: menu item already present"); continue
    pos, how = find_insert_point(s)
    if pos is None:
        i = s.find("showSettingsMenu")
        raise RuntimeError("No insertion point found in MainScreen.kt. Context:\n" + s[max(0, i - 300): i + 700])
    code = item_code(ar, en, icon, act)
    s = s[:pos] + code + s[pos:]
    if first_pos is None: first_pos = pos + 1
    added.append(f"{act} -> {how}")

# ---- `context` must be in scope INSIDE the function that holds the menu ----
if first_pos is not None:
    fn = enclosing_function(s, first_pos)
    if fn is None:
        raise RuntimeError("Could not determine the composable that contains the menu (needed to check `context`).")
    p_open, p_close, b_open, b_close = fn
    params = s[p_open:p_close + 1]
    body_before = s[b_open:first_pos]
    has_param = re.search(r"\bcontext\s*:", params)
    has_val = re.search(r"\b(?:private\s+|internal\s+)?val\s+context\b\s*(?::[^=\n]+)?(?:=|by\b)", body_before)
    if not (has_param or has_val):
        s = s[:b_open + 1] + "\n    val context = androidx.compose.ui.platform.LocalContext.current" + s[b_open + 1:]
        print("INFO: injected `val context = LocalContext.current` at the top of the menu's composable")
    if "state.language.tr(" not in s[fn[2]:fn[3]]:
        print("WARNING: state.language.tr( not seen inside the menu's composable - check that `state` is in scope there")

s = ensure_icon_imports(s)

with open(MAIN_SCREEN, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
for a in added: print("OK menu item:", a)

# ---- final verification ----
manifest = open(MANIFEST, encoding="utf-8").read()
bad = False
for _, _, _, act in ITEMS:
    ok_menu = f"{act}::class.java" in s
    ok_man = re.search(r'android:name\s*=\s*"(?:com\.zevorix\.assistant)?\.?' + act + '"', manifest) is not None
    print(f"CHECK {act}: menu={ok_menu} manifest={bool(ok_man)}")
    ok_imp = any(f"import androidx.compose.material.icons.filled.{i}" in s for _, _, i, a2 in ITEMS if a2 == act)
    print(f"CHECK {act}: icon import={ok_imp}")
    bad |= not (ok_menu and ok_man and ok_imp)
if bad: sys.exit(1)

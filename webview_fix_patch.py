import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"

# (activity file, class, fallback html, background color)
TARGETS = [
    ("ArchitectureActivity.kt", "ArchitectureActivity", "architecture_lab.html", "#0a192f"),
    ("FlightSimActivity.kt",    "FlightSimActivity",    "flight_sim.html",       "#0a0f18"),
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


ONCREATE_RE = re.compile(r"override\s+fun\s+onCreate\s*\(\s*(\w+)\s*:\s*Bundle\?\s*\)\s*\{")


def bridge_args(src):
    """Build the Bridge(...) argument list from its actual constructor, so both Bridge shapes work."""
    m = re.search(r"class\s+Bridge\s*\(([^)]*)\)", src)
    if not m:
        raise RuntimeError("class Bridge(...) not found")
    args = []
    for p in [x.strip() for x in m.group(1).split(",") if x.strip()]:
        t = p.split(":", 1)[1].strip()
        if "Activity" in t: args.append("this")
        elif t.endswith("WebView"): args.append("webView")
        elif t.endswith("AiChatService"): args.append("aiService")
        else: raise RuntimeError(f"Unknown Bridge parameter type: {t}")
    return ", ".join(args)


def build_body(bundle_param, cls, html, bg, bridge_call):
    return f"""
        super.onCreate({bundle_param})
        val webView = android.webkit.WebView(this)
        webView.setBackgroundColor(android.graphics.Color.parseColor("{bg}"))
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        // NOTE: WebView is hardware-accelerated by default. This only takes effect while the window itself is
        // hardware-accelerated, so the manifest must keep android:hardwareAccelerated="true" for this Activity.
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {{
            webView.setLayerType(android.view.View.LAYER_TYPE_HARDWARE, null)
        }}
        webView.webChromeClient = object : android.webkit.WebChromeClient() {{
            override fun onConsoleMessage(m: android.webkit.ConsoleMessage): Boolean {{
                android.util.Log.e("ZevorixLab", "JS: ${{m.message()}} @${{m.lineNumber()}}")
                return true
            }}
        }}
        webView.webViewClient = object : android.webkit.WebViewClient() {{
            override fun onReceivedError(
                view: android.webkit.WebView?,
                request: android.webkit.WebResourceRequest?,
                error: android.webkit.WebResourceError?
            ) {{
                android.widget.Toast.makeText(
                    this@{cls},
                    "Load error: ${{request?.url}} ${{error?.description}}",
                    android.widget.Toast.LENGTH_LONG
                ).show()
            }}
        }}
        webView.addJavascriptInterface(Bridge({bridge_call}), "Android")
        setContentView(webView)
        webView.loadUrl("file:///android_asset/{html}")
    """


failed = False
for fname, cls, fallback_html, bg in TARGETS:
    path = os.path.join(PKG_DIR, fname)
    if not os.path.exists(path):
        print(f"ERROR: {path} not found"); failed = True; continue
    s = open(path, encoding="utf-8").read()
    if "setContentView(webView)" in s:
        print(f"== {cls}: already uses plain WebView"); continue
    m = ONCREATE_RE.search(s)
    if not m:
        raise RuntimeError(f"{fname}: onCreate(Bundle?) not found")
    b_open = m.end() - 1
    b_close = match_close(s, b_open)
    if b_close == -1:
        raise RuntimeError(f"{fname}: unbalanced braces in onCreate")
    old_body = s[b_open + 1:b_close]
    h = re.search(r'file:///android_asset/([\w.\-]+)', old_body)
    html = h.group(1) if h else fallback_html
    new_body = build_body(m.group(1), cls, html, bg, bridge_args(s))
    s = s[:b_open + 1] + new_body + s[b_close:]
    # sanity: the whole file must still be brace-balanced and the class must close
    c = re.search(r"class\s+" + cls + r"\b[^{]*\{", s)
    if not c or match_close(s, c.end() - 1) == -1:
        raise RuntimeError(f"{fname}: class braces unbalanced after patch")
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print(f"OK {cls}: plain WebView ({html}), Bridge({bridge_args(s)})")

if failed: sys.exit(1)

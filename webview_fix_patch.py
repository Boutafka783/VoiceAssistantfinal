import os, re, sys

PKG_DIR = "app/src/main/java/com/zevorix/assistant"

# (ملف النشاط, اسم الصنف, ملف HTML, لون الخلفية)
TARGETS = [
    ("ArchitectureActivity.kt", "ArchitectureActivity", "architecture_lab.html", "#0a192f"),
    ("FlightSimActivity.kt",    "FlightSimActivity",    "flight_sim.html",       "#0a0f18"),
]

BODY = '''super.onCreate(savedInstanceState)
        val webView = WebView(this)
        webView.setBackgroundColor(android.graphics.Color.parseColor("%(bg)s"))
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.webChromeClient = object : android.webkit.WebChromeClient() {
            override fun onConsoleMessage(m: android.webkit.ConsoleMessage): Boolean {
                android.util.Log.e("ZevorixLab", "JS: ${m.message()} @${m.lineNumber()}")
                return true
            }
        }
        webView.webViewClient = object : WebViewClient() {
            override fun onReceivedError(
                view: WebView?,
                request: android.webkit.WebResourceRequest?,
                error: android.webkit.WebResourceError?
            ) {
                android.widget.Toast.makeText(
                    this@%(cls)s,
                    "Load error: ${request?.url} ${error?.description}",
                    android.widget.Toast.LENGTH_LONG
                ).show()
            }
        }
        webView.addJavascriptInterface(Bridge(this, webView, aiService), "Android")
        setContentView(webView)
        webView.loadUrl("file:///android_asset/%(html)s")
    }

    '''

ok = True
for fname, cls, html, bg in TARGETS:
    path = os.path.join(PKG_DIR, fname)
    if not os.path.exists(path):
        print(f"ERROR: {path} not found"); ok = False; continue
    s = open(path, encoding="utf-8").read()
    if "setContentView(webView)" in s:
        print(f"== {cls}: already uses plain WebView"); continue
    pat = re.compile(r"super\.onCreate\(savedInstanceState\)\n.*?\n    \}\n\s*(?=class Bridge)", re.S)
    if not pat.search(s):
        print(f"ERROR: onCreate pattern not found in {fname}"); ok = False; continue
    s = pat.sub(lambda m: BODY % {"bg": bg, "cls": cls, "html": html}, s, count=1)
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print(f"OK {cls}: replaced Compose AndroidView with plain WebView + error toast + JS console log")

if not ok: sys.exit(1)

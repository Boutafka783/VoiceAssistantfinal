import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"

def replace_once(file_path, old, new):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.count(old) != 1:
        raise RuntimeError(f"Anchor not found exactly once in {file_path}: {old[:60]}")
    content = content.replace(old, new, 1)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

print(">> Applying Blueprint Generator Patch...")

# 1) إنشاء ملف blueprint_lab.html في مجلد assets
html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>مولد مخططات البناء</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  :root { --bg: #0a0f18; --panel: #0d1522; --border: rgba(53, 208, 255, 0.4); --text: #e8edf5; --accent: #35d0ff; --btn-bg: #ff9f1c; --btn-text: #1a1100; }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  body, html { margin: 0; height: 100%; background: var(--bg); color: var(--text); font-family: system-ui, -apple-system, sans-serif; overflow: hidden; }
  #app { display: flex; flex-direction: column; height: 100vh; }
  #header { display: flex; align-items: center; justify-content: space-between; padding: 10px 15px; background: var(--panel); border-bottom: 1px solid var(--border); }
  #header h1 { margin: 0; font-size: 1.2rem; color: var(--accent); }
  #tabs { display: flex; gap: 5px; overflow-x: auto; }
  .tab { background: transparent; border: 1px solid var(--border); color: var(--text); padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 0.9rem; white-space: nowrap; }
  .tab.active { background: rgba(53, 208, 255, 0.15); border-color: var(--accent); color: var(--accent); }
  #workspace { flex: 1; position: relative; background-image: radial-gradient(circle, #1a2538 1px, transparent 1px); background-size: 20px 20px; overflow: hidden; display: flex; justify-content: center; align-items: center; padding: 10px; }
  #canvas-container { width: 100%; height: 100%; background: #fff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); overflow: auto; display: flex; justify-content: center; align-items: center; position: relative; }
  #canvas-container svg { max-width: 100%; max-height: 100%; }
  #canvas-container pre.mermaid { background: transparent; border: none; font-family: inherit; text-align: center; }
  #loading { position: absolute; inset: 0; background: rgba(10, 15, 24, 0.8); display: none; justify-content: center; align-items: center; z-index: 10; color: var(--accent); font-size: 1.2rem; flex-direction: column; gap: 10px; backdrop-filter: blur(4px); }
  .spinner { width: 40px; height: 40px; border: 4px solid rgba(53,208,255,0.2); border-top-color: var(--accent); border-radius: 50%; animation: spin 1s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  #footer { padding: 15px; background: var(--panel); border-top: 1px solid var(--border); display: flex; gap: 10px; align-items: center; }
  #prompt { flex: 1; padding: 12px 15px; border-radius: 8px; border: 1px solid var(--border); background: #060a12; color: var(--text); font-size: 1rem; outline: none; }
  #prompt:focus { border-color: var(--accent); }
  #generate-btn { padding: 12px 24px; background: var(--btn-bg); color: var(--btn-text); border: none; border-radius: 8px; font-size: 1rem; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 8px; }
  #generate-btn:disabled { opacity: 0.5; cursor: not-allowed; }
  #save-btn { padding: 12px; background: transparent; border: 1px solid var(--border); color: var(--text); border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
  #toast { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(53, 208, 255, 0.9); color: #000; padding: 10px 20px; border-radius: 20px; font-weight: bold; opacity: 0; transition: opacity 0.3s; pointer-events: none; z-index: 100; }
</style>
</head>
<body>
<div id="app">
  <div id="header">
    <h1>🏗️ مخططات البناء</h1>
    <div id="tabs">
      <button class="tab active" data-type="circuit">إلكترونيات</button>
      <button class="tab" data-type="mechanical">ميكانيكا</button>
      <button class="tab" data-type="robot">روبوت</button>
      <button class="tab" data-type="flowchart">تدفق</button>
    </div>
  </div>
  <div id="workspace">
    <div id="canvas-container">
      <div id="placeholder" style="color:#888; font-size:1.1rem; text-align:center; padding:20px;">اكتب وصف المخطط في الأسفل واضغط "توليد"</div>
    </div>
    <div id="loading"><div class="spinner"></div><div>جاري تصميم المخطط...</div></div>
    <div id="toast"></div>
  </div>
  <div id="footer">
    <button id="save-btn" title="حفظ كصورة HTML">💾</button>
    <input type="text" id="prompt" placeholder="مثال: دائرة إضاءة LED مع بطارية 9V..." />
    <button id="generate-btn">✨ توليد</button>
  </div>
</div>
<script>
  mermaid.initialize({ startOnLoad: false, theme: 'default' });
  let currentType = 'circuit', currentCode = '', currentFormat = 'svg';
  const container = document.getElementById('canvas-container'), placeholder = document.getElementById('placeholder'),
        loading = document.getElementById('loading'), promptInput = document.getElementById('prompt'),
        generateBtn = document.getElementById('generate-btn'), saveBtn = document.getElementById('save-btn'), toast = document.getElementById('toast');
  
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentType = tab.getAttribute('data-type');
    });
  });
  
  function showToast(msg) { toast.textContent = msg; toast.style.opacity = 1; setTimeout(() => { toast.style.opacity = 0; }, 3000); }
  function setLoading(show) { loading.style.display = show ? 'flex' : 'none'; generateBtn.disabled = show; }
  
  generateBtn.addEventListener('click', () => {
    const text = promptInput.value.trim();
    if (!text) return;
    if (!window.Android || !window.Android.askAi) { showToast('Android bridge not available'); return; }
    setLoading(true); placeholder.style.display = 'none'; container.innerHTML = '';
    let sysPrompt = currentType === 'flowchart' 
      ? `أنت خبير في رسم مخططات التدفق. أنشئ كود Mermaid فقط (يبدأ بـ graph TD) بناءً على: "${text}". بدون أي كلام إضافي أو علامات markdown.`
      : `أنت مهندس محترف. أنشئ كود SVG فقط لمخطط ${currentType === 'circuit' ? 'دائرة إلكترونية' : currentType === 'mechanical' ? 'قطعة ميكانيكية' : 'روبوت'} بناءً على: "${text}". استخدم viewBox="0 0 800 600" وألواناً واضحة. أعد كود SVG فقط بدون أي كلام إضافي أو markdown.`;
    window.Android.askAi('blueprint_gen', currentType, sysPrompt);
  });
  
  window.onAiResult = function(id, ok, text) {
    if (id !== 'blueprint_gen') return;
    setLoading(false);
    if (!ok || !text) { showToast('فشل التوليد: ' + text); placeholder.style.display = 'block'; return; }
    let code = text.trim();
    if (code.startsWith('```')) code = code.replace(/^```[a-z]*\n/, '').replace(/\n```$/, '');
    currentCode = code;
    if (currentType === 'flowchart') {
      currentFormat = 'mermaid';
      container.innerHTML = '<pre class="mermaid">' + code + '</pre>';
      try { mermaid.run({ nodes: container.querySelectorAll('.mermaid') }); } catch(e) { showToast('خطأ في Mermaid'); }
    } else {
      currentFormat = 'svg';
      if (!code.includes('<svg')) { container.innerHTML = '<div style="color:red; padding:20px; font-weight:bold;">الرد لا يحتوي على كود SVG صالح.</div>'; return; }
      container.innerHTML = code;
    }
    showToast('تم التوليد بنجاح!');
  };
  
  saveBtn.addEventListener('click', () => {
    if (!currentCode) { showToast('لا يوجد مخطط لحفظه'); return; }
    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>Blueprint</title><script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"><\/script><script>mermaid.initialize({startOnLoad:true});<\/script><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fafafa;}</style></head><body>${currentFormat === 'mermaid' ? '<pre class="mermaid">' + currentCode + '</pre>' : currentCode}</body></html>`;
    if (window.Android && window.Android.saveBlueprint) {
      window.Android.saveBlueprint(html, currentType);
      showToast('تم الحفظ في Downloads/ZevorixDiagrams');
    } else { showToast('Save bridge not available'); }
  });
</script>
</body>
</html>
'''

os.makedirs("app/src/main/assets", exist_ok=True)
with open("app/src/main/assets/blueprint_lab.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# 2) إنشاء BlueprintActivity.kt
activity_content = r'''package com.zevorix.assistant

import android.annotation.SuppressLint
import android.content.ContentValues
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.material3.Surface
import androidx.compose.material3.MaterialTheme
import com.zevorix.assistant.data.AiChatService
import com.zevorix.assistant.data.AiResult
import com.zevorix.assistant.ui.theme.VoiceAssistantTheme
import kotlinx.coroutines.*
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class BlueprintActivity : ComponentActivity() {
    private val aiService = AiChatService()
    
    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            VoiceAssistantTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    AndroidView(
                        modifier = Modifier.fillMaxSize(),
                        factory = { context ->
                            WebView(context).apply {
                                settings.javaScriptEnabled = true
                                settings.domStorageEnabled = true
                                settings.allowFileAccess = true
                                webViewClient = WebViewClient()
                                addJavascriptInterface(Bridge(this@BlueprintActivity, this, aiService), "Android")
                                loadUrl("file:///android_asset/blueprint_lab.html")
                            }
                        }
                    )
                }
            }
        }
    }
    
    class Bridge(private val activity: ComponentActivity, private val webView: WebView, private val aiService: AiChatService) {
        @JavascriptInterface
        fun askAi(id: String, type: String, prompt: String) {
            CoroutineScope(Dispatchers.IO).launch {
                val lang = if (prompt.any { it in '\u0600'..'\u06FF' }) com.zevorix.assistant.viewmodel.AppLanguage.ARABIC else com.zevorix.assistant.viewmodel.AppLanguage.ENGLISH
                val result = aiService.ask(prompt, lang)
                withContext(Dispatchers.Main) {
                    when (result) {
                        is AiResult.Success -> {
                            val safeText = result.text.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "")
                            webView.evaluateJavascript("window.onAiResult(\"$id\", true, \"$safeText\");", null)
                        }
                        is AiResult.Error -> {
                            val msg = "Error: ${result.kind} ${result.detail}"
                            val safeText = msg.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                            webView.evaluateJavascript("window.onAiResult(\"$id\", false, \"$safeText\");", null)
                        }
                    }
                }
            }
        }
        
        @JavascriptInterface
        fun saveBlueprint(html: String, type: String) {
            try {
                val stamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
                val filename = "blueprint_${type}_$stamp.html"
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    val resolver = activity.contentResolver
                    val values = ContentValues().apply {
                        put(MediaStore.MediaColumns.DISPLAY_NAME, filename)
                        put(MediaStore.MediaColumns.MIME_TYPE, "text/html")
                        put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/ZevorixDiagrams")
                    }
                    val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
                    if (uri != null) {
                        resolver.openOutputStream(uri)?.use { it.write(html.toByteArray()) }
                        CoroutineScope(Dispatchers.Main).launch { Toast.makeText(activity, "تم الحفظ في Downloads/ZevorixDiagrams", Toast.LENGTH_LONG).show() }
                    }
                } else {
                    val dir = File(activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), "ZevorixDiagrams")
                    dir.mkdirs()
                    val file = File(dir, filename)
                    file.writeText(html)
                    CoroutineScope(Dispatchers.Main).launch { Toast.makeText(activity, "تم الحفظ في ${file.absolutePath}", Toast.LENGTH_LONG).show() }
                }
            } catch (e: Exception) {
                CoroutineScope(Dispatchers.Main).launch { Toast.makeText(activity, "فشل الحفظ: ${e.message}", Toast.LENGTH_LONG).show() }
            }
        }
    }
}
'''

with open(PKG_DIR + "/BlueprintActivity.kt", "w", encoding="utf-8") as f:
    f.write(activity_content)

# 3) تسجيل النشاط في AndroidManifest.xml
replace_once(
    MANIFEST,
    '        <!-- Live Vision: live camera preview + spoken questions about what the camera sees -->\n',
    '        <!-- Blueprint Generator -->\n'
    '        <activity\n'
    '            android:name=".BlueprintActivity"\n'
    '            android:exported="false"\n'
    '            android:theme="@style/Theme.VoiceAssistant" />\n\n'
    '        <!-- Live Vision: live camera preview + spoken questions about what the camera sees -->\n'
)

# 4) إضافة الزر في واجهة التطبيق (MainScreen.kt)
replace_once(
    MAIN_SCREEN,
    "import com.zevorix.assistant.ui.components.AiSettingsSheet\n",
    "import com.zevorix.assistant.ui.components.AiSettingsSheet\n"
    "import com.zevorix.assistant.BlueprintActivity\n"
    "import androidx.compose.material.icons.filled.AccountTree\n"
)

replace_once(
    MAIN_SCREEN,
    "                                DropdownMenuItem(\n"
    "                                    text = { Text(state.language.tr(\"الرؤية الحية (كاميرا)\", \"Live Vision (Camera)\")) },\n",
    "                                DropdownMenuItem(\n"
    "                                    text = { Text(state.language.tr(\"مولد مخططات البناء\", \"Blueprint Generator\")) },\n"
    "                                    leadingIcon = { Icon(Icons.Filled.AccountTree, contentDescription = null) },\n"
    "                                    onClick = {\n"
    "                                        showSettingsMenu = false\n"
    "                                        context.startActivity(android.content.Intent(context, BlueprintActivity::class.java))\n"
    "                                    }\n"
    "                                )\n"
    "                                DropdownMenuItem(\n"
    "                                    text = { Text(state.language.tr(\"الرؤية الحية (كاميرا)\", \"Live Vision (Camera)\")) },\n"
)

print(">> Blueprint Generator Patch applied successfully!")
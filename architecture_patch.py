import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"

def replace_once(file_path, old, new, silent_if_exists=False, required=True):
    """Replace exactly one occurrence of `old`. Fails loudly instead of silently skipping.

    - silent_if_exists: if `new` is already in the file, do nothing (idempotent re-runs).
    - required: raise if the anchor is missing; with required=False a missing anchor returns False.
    - An anchor that appears more than once always raises (ambiguous).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if silent_if_exists and new in content:
        return True
    count = content.count(old)
    if count == 0:
        if required:
            raise RuntimeError(f"Anchor not found in {file_path}: {old!r}")
        return False
    if count > 1:
        raise RuntimeError(f"Anchor appears {count} times in {file_path}: {old!r}")
    content = content.replace(old, new, 1)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return True


def register_activity(name):
    """Register .<name> in AndroidManifest.xml (skips if already declared; raises if </application> is missing/ambiguous)."""
    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest = f.read()
    if re.search(r'android:name\s*=\s*"(?:com\.zevorix\.assistant)?\.?' + re.escape(name) + r'"', manifest):
        print(f">> {name} already declared in manifest - skipping")
        return
    block = (
        f'    <!-- {name} -->\n'
        f'    <activity\n'
        f'        android:name=".{name}"\n'
        f'        android:exported="false"\n'
        f'        android:hardwareAccelerated="true"\n'
        f'        android:configChanges="orientation|screenSize|keyboardHidden|screenLayout|smallestScreenSize|uiMode"\n'
        f'        android:theme="@style/Theme.VoiceAssistant" />\n\n'
        f'</application>'
    )
    replace_once(MANIFEST, "</application>", block, silent_if_exists=True, required=True)
    print(f">> Registered {name} in AndroidManifest.xml")

print(">> Applying Architecture Lab Patch...")

# 1) إنشاء ملف architecture_lab.html
# (نفس الكود السابق) ...
html_content = r'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>مختبر الهندسة المعمارية</title><style>:root{--bg:#0a192f;--panel:#112240;--border:#233554;--text:#ccd6f6;--accent:#64ffda;--btn-bg:#f59e0b;--btn-text:#000}*{box-sizing:border-box}body,html{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;overflow:hidden}#app{display:flex;flex-direction:column;height:100vh}#header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:var(--panel);border-bottom:1px solid var(--border);box-shadow:0 4px 6px rgba(0,0,0,.3)}#header h1{margin:0;font-size:1.2rem;color:var(--accent)}#workspace{flex:1;position:relative;background-color:#0a192f;background-image:linear-gradient(#233554 1px,transparent 1px),linear-gradient(90deg,#233554 1px,transparent 1px);background-size:20px 20px;display:flex;justify-content:center;align-items:center;padding:10px;overflow:hidden}#canvas-container{width:100%;height:100%;background:#fff;border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.5);overflow:hidden;display:flex;justify-content:center;align-items:center}#canvas-container svg{max-width:100%;max-height:100%}#loading{position:absolute;inset:0;background:rgba(10,25,47,.85);display:none;justify-content:center;align-items:center;z-index:10;color:var(--accent);font-size:1.2rem;flex-direction:column;gap:10px;backdrop-filter:blur(4px)}.spinner{width:50px;height:50px;border:4px solid rgba(100,255,218,.2);border-top-color:var(--accent);border-radius:50%;animation:spin 1s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}#footer{padding:15px;background:var(--panel);border-top:1px solid var(--border);display:flex;gap:10px;align-items:center}#prompt{flex:1;padding:14px;border-radius:8px;border:1px solid var(--border);background:#0a192f;color:var(--text);font-size:1rem;outline:none;resize:none;height:50px}#prompt:focus{border-color:var(--accent)}#generate-btn{padding:0 20px;height:50px;background:var(--accent);color:#0a192f;border:none;border-radius:8px;font-size:1rem;font-weight:bold;cursor:pointer;display:flex;align-items:center;gap:8px}#save-btn{height:50px;width:50px;background:transparent;border:1px solid var(--accent);color:var(--accent);border-radius:8px;cursor:pointer;display:flex;justify-content:center;align-items:center;font-size:1.2rem}#toast{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);background:var(--accent);color:#0a192f;padding:10px 20px;border-radius:20px;font-weight:bold;opacity:0;transition:opacity .3s;pointer-events:none;z-index:100}</style></head><body><div id="app"><div id="header"><h1>🏛️ الهندسة المعمارية</h1><span style="font-size:.8rem;color:#8892b0">Blueprint Architect</span></div><div id="workspace"><div id="canvas-container"><div id="placeholder" style="color:#8892b0;font-size:1.1rem;text-align:center;padding:20px">اكتب وصف المبنى في الأسفل، مثلاً:<br>"شقة بمساحة 120 متر، غرفتين نوم، صالة كبيرة، مطبخ، وحمامين"</div></div><div id="loading"><div class="spinner"></div><div>جاري رسم المخطط الهندسي...</div></div><div id="toast"></div></div><div id="footer"><button id="save-btn" title="حفظ المخطط">💾</button><textarea id="prompt" placeholder="وصف المبنى (مثال: فيلا دور واحد، 3 غرف، صالة، مطبخ، حديقة...)"></textarea><button id="generate-btn">✨ ارسم</button></div></div><script>let currentCode='';const container=document.getElementById('canvas-container'),placeholder=document.getElementById('placeholder'),loading=document.getElementById('loading'),promptInput=document.getElementById('prompt'),generateBtn=document.getElementById('generate-btn'),saveBtn=document.getElementById('save-btn'),toast=document.getElementById('toast');function showToast(e){toast.textContent=e,toast.style.opacity=1,setTimeout(()=>{toast.style.opacity=0},3e3)}function setLoading(e){loading.style.display=e?'flex':'none',generateBtn.disabled=e}generateBtn.addEventListener('click',()=>{const e=promptInput.value.trim();if(!e)return;if(!window.Android||!window.Android.askAi)return void showToast('Android bridge not available');setLoading(!0),placeholder.style.display='none',container.innerHTML='';let t=`أنت مهندس معماري خبير. قم بتصميم مخطط طابقي (Floor Plan) احترافي بصيغة SVG بناءً على هذا الطلب: "${e}". القواعد: 1. استخدم viewBox="0 0 1000 800". 2. ارسم الجدران بخطوط سميكة (stroke-width: 8). 3. أضف الأبواب كأقواس والنوافذ كخطوط مزدوجة. 4. ضع اسم كل غرفة وأبعادها التقريبية (مثلاً "غرفة نوم 4x4") في منتصفها. 5. استخدم ألواناً هندسية (خلفية بيضاء، جدران سوداء، الأرضيات رمادية فاتحة). 6. أعد كود SVG فقط بدون أي كلام إضافي أو علامات markdown.`;window.Android.askAi('architecture_gen','architecture',t)}),window.onAiResult=function(e,t,n){if('architecture_gen'===e){if(setLoading(!1),!t||!n)return showToast('فشل التوليد: '+n),void(placeholder.style.display='block');let a=n.trim();a.startsWith('```')&&(a=a.replace(/^```[a-z]*\n/,'').replace(/\n```$/,'')),currentCode=a,a.includes('<svg')?(container.innerHTML=a,showToast('تم رسم المخطط بنجاح!')):container.innerHTML='<div style="color:red;padding:20px;font-weight:bold">الرد لا يحتوي على كود SVG صالح.</div>'}},saveBtn.addEventListener('click',()=>{if(!currentCode)return void showToast('لا يوجد مخطط لحفظه');const e=`<!DOCTYPE html><html><head><meta charset="utf-8"><title>Architecture Blueprint</title><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fafafa;}</style></head><body>${currentCode}</body></html>`;window.Android&&window.Android.saveBlueprint&&(window.Android.saveBlueprint(e,'architecture'),showToast('تم الحفظ في Downloads/ZevorixDiagrams'))});</script></body></html>'''

os.makedirs("app/src/main/assets", exist_ok=True)
with open("app/src/main/assets/architecture_lab.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# 2) إنشاء ArchitectureActivity.kt
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

class ArchitectureActivity : ComponentActivity() {
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
                                addJavascriptInterface(Bridge(this@ArchitectureActivity, this, aiService), "Android")
                                loadUrl("file:///android_asset/architecture_lab.html")
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
                val filename = "architecture_${stamp}.html"
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

with open(PKG_DIR + "/ArchitectureActivity.kt", "w", encoding="utf-8") as f:
    f.write(activity_content)

# 3) تسجيل النشاط في AndroidManifest.xml
register_activity("ArchitectureActivity")

# 4) القائمة الجانبية: لا يتم تعديل MainScreen.kt هنا.
#    menu_items_patch.py هو المصدر الوحيد لإدراج عنصر القائمة (بأسماء كاملة، دون الحاجة لأي import).

print(">> Architecture Lab Patch applied (activity + html + manifest). Menu item: menu_items_patch.py")
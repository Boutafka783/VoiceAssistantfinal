import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
ACTIVITY = PKG_DIR + "/ArchitectureActivity.kt"
HTML_PATH = "app/src/main/assets/architecture_lab.html"

def replace_once(file_path, old, new, silent_if_exists=False, required=True):
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

print(">> Applying Architecture Lab Patch v3 (Smart SVG Renderer + JSON AI)...")

# 1) إنشاء ArchitectureActivity.kt المحدث (يدعم PNG, SVG, HTML)
activity_content = r'''package com.zevorix.assistant

import android.annotation.SuppressLint
import android.content.ContentValues
import android.graphics.BitmapFactory
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Base64
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
import org.json.JSONObject
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ArchitectureActivity : ComponentActivity() {
    private val aiService = AiChatService()
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

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
                                addJavascriptInterface(Bridge(this@ArchitectureActivity, this, aiService, scope), "Android")
                                loadUrl("file:///android_asset/architecture_lab.html")
                            }
                        }
                    )
                }
            }
        }
    }

    override fun onDestroy() {
        scope.cancel()
        super.onDestroy()
    }

    class Bridge(
        private val activity: ComponentActivity,
        private val webView: WebView,
        private val aiService: AiChatService,
        private val scope: CoroutineScope
    ) {
        @JavascriptInterface
        fun askAi(id: String, type: String, prompt: String) {
            scope.launch {
                val lang = if (prompt.any { it in '\u0600'..'\u06FF' }) com.zevorix.assistant.viewmodel.AppLanguage.ARABIC else com.zevorix.assistant.viewmodel.AppLanguage.ENGLISH
                val result = aiService.ask(prompt, lang)
                withContext(Dispatchers.Main) {
                    val idJs = JSONObject.quote(id)
                    when (result) {
                        is AiResult.Success -> webView.evaluateJavascript("window.onAiResult($idJs, true, ${JSONObject.quote(result.text)});", null)
                        is AiResult.Error -> {
                            val msg = "Error: ${result.kind} ${result.detail}"
                            webView.evaluateJavascript("window.onAiResult($idJs, false, ${JSONObject.quote(msg)});", null)
                        }
                    }
                }
            }
        }

        @JavascriptInterface
        fun saveBlueprint(html: String, type: String) {
            saveToFile(html.toByteArray(), "architecture_${getStamp()}.html", "text/html")
        }

        @JavascriptInterface
        fun saveSvg(svgContent: String) {
            saveToFile(svgContent.toByteArray(), "blueprint_${getStamp()}.svg", "image/svg+xml")
        }

        @JavascriptInterface
        fun savePng(base64Data: String) {
            try {
                val imageBytes = Base64.decode(base64Data, Base64.DEFAULT)
                saveToFile(imageBytes, "blueprint_${getStamp()}.png", "image/png")
            } catch (e: Exception) {
                showToast("فشل حفظ الصورة: ${e.message}")
            }
        }

        private fun getStamp(): String = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())

        private fun saveToFile(bytes: ByteArray, filename: String, mimeType: String) {
            try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    val resolver = activity.contentResolver
                    val values = ContentValues().apply {
                        put(MediaStore.MediaColumns.DISPLAY_NAME, filename)
                        put(MediaStore.MediaColumns.MIME_TYPE, mimeType)
                        put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/ZevorixDiagrams")
                    }
                    val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
                    if (uri != null) {
                        resolver.openOutputStream(uri)?.use { it.write(bytes) }
                        showToast("تم الحفظ في Downloads/ZevorixDiagrams")
                    }
                } else {
                    val dir = File(activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), "ZevorixDiagrams")
                    dir.mkdirs()
                    val file = File(dir, filename)
                    file.writeBytes(bytes)
                    showToast("تم الحفظ في ${file.absolutePath}")
                }
            } catch (e: Exception) {
                showToast("فشل الحفظ: ${e.message}")
            }
        }

        private fun showToast(msg: String) {
            CoroutineScope(Dispatchers.Main).launch {
                Toast.makeText(activity, msg, Toast.LENGTH_LONG).show()
            }
        }
    }
}
'''

with open(ACTIVITY, "w", encoding="utf-8", newline="\n") as f:
    f.write(activity_content)
print(">> Wrote " + ACTIVITY)

# 2) إنشاء ملف الـ HTML الجديد (Smart JSON Renderer)
html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>مختبر الهندسة المعمارية</title>
<style>
:root{--bg:#0a192f;--panel:#112240;--border:#233554;--text:#ccd6f6;--muted:#8892b0;--accent:#64ffda;--warn:#f59e0b}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;overflow:hidden}
#app{display:flex;flex-direction:column;height:100vh}
#header,#options,#chips,#footer{flex:0 0 auto}
#header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--panel);border-bottom:1px solid var(--border)}
#header h1{margin:0;font-size:1.05rem;color:var(--accent)}
.hbtns{display:flex;gap:8px}
.ibtn{height:38px;min-width:38px;padding:0 10px;background:transparent;border:1px solid var(--border);color:var(--text);border-radius:8px;cursor:pointer;font-size:1rem}
.ibtn:active{background:var(--border)}
#options{background:var(--panel);border-bottom:1px solid var(--border);padding:0 14px}
#options summary{padding:8px 0;color:var(--accent);cursor:pointer;font-size:.9rem}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;padding-bottom:10px;max-height:40vh;overflow:auto}
.grid label{display:flex;flex-direction:column;gap:4px;font-size:.78rem;color:var(--muted)}
.grid select,.grid input[type=number]{padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:.9rem}
.checks{grid-column:1/-1;display:flex;gap:14px;flex-wrap:wrap;font-size:.85rem}
.checks label{flex-direction:row;align-items:center;color:var(--text)}
#chips{display:flex;gap:8px;overflow-x:auto;padding:8px 14px;background:var(--bg);scrollbar-width:none}
.chip{flex:0 0 auto;white-space:nowrap;padding:6px 12px;border:1px solid var(--border);border-radius:16px;background:var(--panel);color:var(--text);font-size:.8rem;cursor:pointer}
#workspace{flex:1 1 auto;min-height:240px;position:relative;background-color:#0a192f;background-image:linear-gradient(#233554 1px,transparent 1px),linear-gradient(90deg,#233554 1px,transparent 1px);background-size:20px 20px;padding:8px;overflow:hidden}
#viewport{width:100%;height:100%;background:#fff;border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.5);overflow:hidden;position:relative;touch-action:none}
#stage{position:absolute;inset:0;transform-origin:0 0}
#stage svg{width:100%;height:100%;display:block}
#placeholder{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#64748b;text-align:center;padding:20px;line-height:1.8;pointer-events:none}
#zoom{position:absolute;bottom:14px;left:14px;display:flex;flex-direction:column;gap:6px;z-index:5}
#zoom button{width:38px;height:38px;border-radius:8px;border:1px solid var(--border);background:rgba(17,34,64,.92);color:var(--accent);font-size:1.1rem;cursor:pointer}
#loading{position:absolute;inset:0;background:rgba(10,25,47,.85);display:none;justify-content:center;align-items:center;z-index:10;color:var(--accent);flex-direction:column;gap:10px;backdrop-filter:blur(4px)}
.spinner{width:46px;height:46px;border:4px solid rgba(100,255,218,.2);border-top-color:var(--accent);border-radius:50%;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#footer{padding:10px;background:var(--panel);border-top:1px solid var(--border);display:flex;flex-direction:column;gap:8px}
#modebar{display:none;font-size:.8rem;color:var(--warn)}
#row{display:flex;gap:8px;align-items:center}
#prompt{flex:1;min-width:0;padding:12px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:.95rem;outline:none;resize:none;height:50px;font-family:inherit}
#prompt:focus{border-color:var(--accent)}
#generate-btn{padding:0 16px;height:50px;background:var(--accent);color:#0a192f;border:none;border-radius:8px;font-size:1rem;font-weight:bold;cursor:pointer;white-space:nowrap}
#generate-btn:disabled{opacity:.5}
#save-btn{height:50px;width:50px;flex:0 0 auto;background:transparent;border:1px solid var(--accent);color:var(--accent);border-radius:8px;cursor:pointer;font-size:1.2rem}
.menu{position:absolute;background:var(--panel);border:1px solid var(--border);border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.5);z-index:50;display:none;min-width:200px;overflow:hidden}
.menu button{display:block;width:100%;text-align:right;padding:12px 14px;background:transparent;border:0;border-bottom:1px solid var(--border);color:var(--text);font-size:.95rem;cursor:pointer}
.menu button:last-child{border-bottom:0}
.menu button:active{background:var(--border)}
#savemenu{bottom:76px;left:10px}
#histmenu{top:56px;left:10px;max-height:55vh;overflow:auto;min-width:250px}
#toast{position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:var(--accent);color:#0a192f;padding:10px 20px;border-radius:20px;font-weight:bold;opacity:0;transition:opacity .3s;pointer-events:none;z-index:100;max-width:92%;text-align:center;font-size:.9rem}
</style>
</head>
<body>
<div id="app">
  <div id="header">
    <h1>🏛️ مختبر الهندسة المعمارية</h1>
    <div class="hbtns">
      <button class="ibtn" id="hist-btn" title="السجل">🕘</button>
      <button class="ibtn" id="new-btn" title="مخطط جديد">＋</button>
    </div>
  </div>

  <details id="options">
    <summary>⚙️ خيارات المشروع</summary>
    <div class="grid">
      <label>نوع المبنى
        <select id="o-type">
          <option value="شقة سكنية">شقة سكنية</option>
          <option value="فيلا دور واحد">فيلا دور واحد</option>
          <option value="دوبلكس">دوبلكس</option>
          <option value="مكتب">مكتب</option>
          <option value="محل تجاري">محل تجاري</option>
          <option value="مطعم / مقهى">مطعم / مقهى</option>
          <option value="عيادة">عيادة</option>
        </select>
      </label>
      <label>المساحة الكلية (م²)
        <input type="number" id="o-area" min="15" max="1500" placeholder="مثال: 120">
      </label>
      <label>غرف النوم / المكاتب
        <input type="number" id="o-beds" min="0" max="8" placeholder="مثال: 2">
      </label>
      <label>الحمامات
        <input type="number" id="o-baths" min="0" max="6" placeholder="مثال: 2">
      </label>
      <label>اتجاه المدخل
        <select id="o-door">
          <option value="">جنوب (افتراضي)</option>
          <option value="الشمال">شمال</option>
          <option value="الشرق">شرق</option>
          <option value="الغرب">غرب</option>
        </select>
      </label>
      <label>مستوى التفصيل
        <select id="o-detail">
          <option value="standard">قياسي</option>
          <option value="high">عالي (أثاث + أبعاد)</option>
          <option value="simple">مبسّط</option>
        </select>
      </label>
      <div class="checks">
        <label><input type="checkbox" id="o-furn" checked> أثاث</label>
        <label><input type="checkbox" id="o-dims" checked> خطوط الأبعاد</label>
        <label><input type="checkbox" id="o-north" checked> سهم الشمال والمقياس</label>
        <label><input type="checkbox" id="o-local"> رسم سريع بدون ذكاء اصطناعي</label>
      </div>
    </div>
  </details>

  <div id="chips"></div>

  <div id="workspace">
    <div id="viewport">
      <div id="stage"></div>
      <div id="placeholder">اختر نموذجاً سريعاً من الأعلى<br>أو اكتب وصف المبنى ثم اضغط «ارسم»</div>
      <div id="zoom">
        <button id="z-in">＋</button>
        <button id="z-out">－</button>
        <button id="z-reset" title="إعادة الضبط">⤾</button>
      </div>
    </div>
    <div id="loading"><div class="spinner"></div><div id="loading-text">جاري توزيع الغرف...</div></div>
  </div>

  <div id="footer">
    <div id="modebar">✏️ وضع التعديل: سيتم تعديل المخطط الحالي — <a href="#" id="exit-edit" style="color:var(--accent)">رسم جديد بدلاً من ذلك</a></div>
    <div id="row">
      <button id="save-btn" title="حفظ / مشاركة">💾</button>
      <textarea id="prompt" placeholder="وصف المبنى (اختياري)..."></textarea>
      <button id="generate-btn">✨ ارسم</button>
    </div>
  </div>
</div>

<div class="menu" id="savemenu">
  <button data-fmt="png">🖼️ حفظ كصورة PNG</button>
  <button data-fmt="svg">📐 حفظ كملف SVG</button>
  <button data-fmt="html">🌐 حفظ كصفحة HTML</button>
</div>
<div class="menu" id="histmenu"></div>
<div id="toast"></div>

<script>
(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
var stage=$('stage'),viewport=$('viewport'),placeholder=$('placeholder'),loading=$('loading'),
    promptEl=$('prompt'),genBtn=$('generate-btn'),toastEl=$('toast');
var plan=null,currentSvg='',editMode=false,busy=false,pending=null,toastTimer=null,aiTimer=null;
var view={x:0,y:0,s:1};
var KEY={'الجنوب':'S','الشمال':'N','الشرق':'E','الغرب':'W','':'S'};
var INSIDE={N:1,S:-1,W:1,E:-1};
var TYPES={living:1,hall:1,dining:1,bed:1,master:1,bath:1,kitchen:1,corridor:1,store:1,office:1,stairs:1,other:1};
var EPS=0.05;
var DEF={'شقة سكنية':{a:100,b:2},'فيلا دور واحد':{a:200,b:3},'دوبلكس':{a:180,b:3},'مكتب':{a:90,b:3},'محل تجاري':{a:60,b:0},'مطعم / مقهى':{a:120,b:0},'عيادة':{a:80,b:2}};

function r1(v){return Math.round(v*10)/10}
function r2(v){return Math.round(v*100)/100}
function f1(v){return String(r1(v))}
function near(a,b){return Math.abs(a-b)<EPS}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function numOrNull(v){return (v===''||v==null||isNaN(+v))?null:+v}
function ar2en(s){return String(s).replace(/[٠-٩]/g,function(d){return String(d.charCodeAt(0)-1632)}).replace(/[۰-۹]/g,function(d){return String(d.charCodeAt(0)-1776)})}

function toast(msg){
  toastEl.textContent=msg;toastEl.style.opacity=1;
  clearTimeout(toastTimer);toastTimer=setTimeout(function(){toastEl.style.opacity=0},4200);
}
function setLoading(on,txt){
  busy=on;loading.style.display=on?'flex':'none';genBtn.disabled=on;
  if(txt)$('loading-text').textContent=txt;
}
function setEdit(on){
  editMode=!!(on&&plan);
  $('modebar').style.display=editMode?'block':'none';
  promptEl.placeholder=editMode?'ما التعديل المطلوب؟ (مثال: كبّر المطبخ وأضف غرفة غسيل)':'وصف المبنى (اختياري)...';
  genBtn.textContent=editMode?'✏️ عدّل':'✨ ارسم';
}
$('exit-edit').onclick=function(e){e.preventDefault();setEdit(false)};

var TEMPLATES=[
  {l:'🏢 شقة 120م²',type:'شقة سكنية',area:120,beds:2,baths:2,d:'شقة بمساحة 120 متر مربع: غرفتان نوم، صالة كبيرة، مطبخ، حمامان'},
  {l:'🏡 فيلا',type:'فيلا دور واحد',area:220,beds:3,baths:3,d:'فيلا من طابق واحد مع مجلس ضيوف ومكتب'},
  {l:'🏘️ استوديو 45م²',type:'شقة سكنية',area:45,beds:1,baths:1,d:'استوديو صغير بغرفة نوم واحدة ومطبخ وحمام'},
  {l:'🏪 محل 80م²',type:'محل تجاري',area:80,beds:0,baths:1,d:'محل تجاري بصالة عرض ومخزن وحمام'},
  {l:'☕ مقهى 100م²',type:'مطعم / مقهى',area:100,beds:0,baths:2,d:'مقهى بمنطقة جلوس ومطبخ ومخزن'},
  {l:'🏥 عيادة',type:'عيادة',area:80,beds:2,baths:1,d:'عيادة بغرفتي كشف واستقبال وانتظار'}
];
TEMPLATES.forEach(function(t){
  var b=document.createElement('button');b.className='chip';b.textContent=t.l;
  b.onclick=function(){
    $('o-type').value=t.type;$('o-area').value=t.area;$('o-beds').value=t.beds;$('o-baths').value=t.baths;
    promptEl.value=t.d;setEdit(false);
  };
  $('chips').appendChild(b);
});

function readOpts(desc){
  var d=ar2en(desc||''),m,type=$('o-type').value;
  var o={type:type,area:numOrNull($('o-area').value)||0,beds:numOrNull($('o-beds').value),baths:numOrNull($('o-baths').value),door:$('o-door').value};
  if(!o.area&&(m=d.match(/(\d{2,4})\s*(?:متر|م²|م2|م(?![؀-ۿ])|m)/i)))o.area=+m[1];
  if(o.beds===null){if(/غرفتين|غرفتان/.test(d))o.beds=2;else if((m=d.match(/(\d+)\s*غرف/)))o.beds=+m[1];}
  if(o.baths===null){if(/حمامين|حمامان/.test(d))o.baths=2;else if((m=d.match(/(\d+)\s*حمام/)))o.baths=+m[1];}
  o.extra={majlis:/مجلس/.test(d),office:/مكتب/.test(d)&&type!=='مكتب',laundry:/غسيل/.test(d),dining:/سفرة/.test(d)};
  return o;
}

function R(n,t,wt,min,entry){var r={n:n,t:t,wt:wt,min:min};if(entry)r.entry=true;return r}
function sumMin(a){var s=0;a.forEach(function(r){s+=r.min});return s}
function place(rooms,y,d,W){
  var wts=0,cum=0,x=0,out=[];
  rooms.forEach(function(r){wts+=r.wt});
  var extra=Math.max(0,W-sumMin(rooms));
  rooms.forEach(function(r,i){
    cum+=r.min+extra*r.wt/wts;
    var x2=(i===rooms.length-1)?W:Math.min(W,Math.round(cum*2)/2);
    var q={n:r.n,t:r.t,x:r1(x),y:r1(y),w:r1(x2-x),h:r1(d)};
    if(r.entry)q.entry=true;
    out.push(q);x=x2;
  });
  return out;
}
function generateLocal(o){
  var type=o.type,def=DEF[type]||DEF['شقة سكنية'];
  var A=Math.max(15,Math.min(1500,o.area||def.a)),beds=(o.beds==null)?def.b:o.beds,baths=o.baths;
  var ex=o.extra||{},north=[],south=[],cd=0,nf=0.5,minH=6,ratio=1.3,i;
  if(type==='شقة سكنية'||type==='فيلا دور واحد'||type==='دوبلكس'){
    beds=Math.max(1,Math.min(8,beds));
    if(baths==null)baths=beds>2?2:1;
    baths=Math.max(1,Math.min(6,baths));
    north.push(R(beds>1?'غرفة نوم رئيسية':'غرفة نوم',beds>1?'master':'bed',1.3,3.4));
    for(i=2;i<=beds;i++)north.push(R('غرفة نوم '+i,'bed',1,3));
    for(i=1;i<=baths;i++)north.push(R(baths>1?'حمام '+i:'حمام','bath',.55,1.8));
    if(ex.office)north.push(R('مكتب','office',.9,2.6));
    if(ex.laundry)north.push(R('غسيل','store',.5,1.6));
    south.push(R('صالة معيشة','living',2,4,true));
    if(ex.majlis||type==='فيلا دور واحد')south.push(R('مجلس ضيوف','living',1.2,3.2));
    if(ex.dining)south.push(R('سفرة','dining',1,2.8));
    south.push(R('مطبخ','kitchen',1.1,2.8));
    if(type==='دوبلكس')south.push(R('درج','stairs',.5,1.8));
    if(A>=70){cd=1.2;minH=7.6}
    while(sumMin(north)>sumMin(south)+3){
      var mv=-1;for(i=north.length-1;i>0;i--)if(north[i].t==='bed'){mv=i;break}
      if(mv<0)break;
      south.push(north.splice(mv,1)[0]);
    }
  }else if(type==='مكتب'){
    var k=Math.max(1,Math.min(8,beds||3));baths=Math.max(1,Math.min(4,baths==null?1:baths));
    for(i=1;i<=k;i++)north.push(R('مكتب '+i,'office',1,3));
    south.push(R('استقبال','hall',1.8,3.5,true),R('قاعة اجتماعات','office',1.5,3.2),R('مطبخ صغير','kitchen',.8,2));
    for(i=1;i<=baths;i++)south.push(R(baths>1?'حمام '+i:'حمام','bath',.6,1.6));
    cd=1.2;minH=7.6;
  }else if(type==='عيادة'){
    var k2=Math.max(1,Math.min(6,beds||2));baths=Math.max(1,Math.min(3,baths==null?1:baths));
    for(i=1;i<=k2;i++)north.push(R('غرفة كشف '+i,'office',1,3));
    for(i=1;i<=baths;i++)north.push(R(baths>1?'حمام '+i:'حمام','bath',.55,1.6));
    south.push(R('استقبال وانتظار','hall',2,4,true),R('مكتب إداري','office',1,3));
    cd=1.2;minH=7.6;
  }else if(type==='محل تجاري'){
    baths=Math.max(0,Math.min(3,baths==null?1:baths));
    north.push(R('مخزن','store',1.4,2));
    for(i=1;i<=baths;i++)north.push(R(baths>1?'حمام '+i:'حمام','bath',.6,1.6));
    south.push(R('صالة العرض','hall',1,3,true));
    nf=0.3;minH=5;ratio=1.6;
  }else{
    baths=Math.max(1,Math.min(4,baths==null?2:baths));
    north.push(R('مطبخ','kitchen',2,3.2),R('مخزن','store',1,2));
    for(i=1;i<=baths;i++)north.push(R(baths>1?'حمام '+i:'حمام','bath',.7,1.6));
    south.push(R('صالة الطعام','hall',1,4,true));
    nf=0.34;minH=5.5;ratio=1.6;
  }
  var W=Math.ceil(Math.max(Math.sqrt(A*ratio),sumMin(north),sumMin(south))*2)/2;
  var H=Math.max(A/W,minH),rem=H-cd;
  var dn=Math.max(2.5,Math.round(rem*nf*2)/2),ds=rem-dn;
  if(ds<2.8){ds=2.8}
  H=r1(dn+cd+ds);
  var rooms=place(north,0,dn,W);
  if(cd)rooms.push({n:'ممر',t:'corridor',x:0,y:r1(dn),w:W,h:cd});
  rooms=rooms.concat(place(south,r1(dn+cd),r1(ds),W));
  return {w:W,h:H,rooms:rooms};
}

function extractJson(t){
  t=String(t||'').replace(/```[a-z]*/gi,'');
  var a=t.indexOf('{'),b=t.lastIndexOf('}');
  if(a<0||b<=a)return null;
  try{return JSON.parse(t.slice(a,b+1))}catch(e){return null}
}
function guessType(n){
  n=String(n);
  if(/حمام|دورة|مرحاض/.test(n))return 'bath';
  if(/مطبخ/.test(n))return 'kitchen';
  if(/رئيسية|ماستر/.test(n))return 'master';
  if(/نوم/.test(n))return 'bed';
  if(/ممر|رواق/.test(n))return 'corridor';
  if(/مخزن|غسيل|مستودع/.test(n))return 'store';
  if(/مكتب|كشف|اجتماع/.test(n))return 'office';
  if(/سفرة|طعام/.test(n))return 'dining';
  if(/درج|سلم/.test(n))return 'stairs';
  if(/صالة|معيشة|مجلس|استقبال|جلوس|انتظار/.test(n))return 'living';
  return 'other';
}
function normalizeLayout(obj){
  if(!obj||!Array.isArray(obj.rooms)||obj.rooms.length<2||obj.rooms.length>24)return null;
  var rooms=[],i,j,q;
  for(i=0;i<obj.rooms.length;i++){
    q=obj.rooms[i]||{};
    var x=+q.x,y=+q.y,w=+q.w,h=+q.h;
    if(!isFinite(x)||!isFinite(y)||!isFinite(w)||!isFinite(h)||w<0.9||h<0.9)return null;
    var nm=String(q.n||q.name||'غرفة').slice(0,24);
    rooms.push({n:nm,t:TYPES[q.t]?q.t:guessType(nm),x:r1(x),y:r1(y),w:r1(w),h:r1(h),entry:!!q.entry});
  }
  var minX=1e9,minY=1e9,maxX=0,maxY=0;
  rooms.forEach(function(r){minX=Math.min(minX,r.x);minY=Math.min(minY,r.y)});
  rooms.forEach(function(r){r.x=r1(r.x-minX);r.y=r1(r.y-minY);maxX=Math.max(maxX,r.x+r.w);maxY=Math.max(maxY,r.y+r.h)});
  if(maxX>80||maxY>80)return null;
  var area=0;
  for(i=0;i<rooms.length;i++){
    area+=rooms[i].w*rooms[i].h;
    for(j=i+1;j<rooms.length;j++){
      var a=rooms[i],b=rooms[j];
      var ox=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x),oy=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y);
      if(ox>0.15&&oy>0.15)return null;
    }
  }
  if(area/(maxX*maxY)<0.88)return null;
  return {w:r1(maxX),h:r1(maxY),rooms:rooms};
}
function aiPrompt(desc,o,edit){
  var schema='{"w":12,"h":10,"rooms":[{"n":"صالة معيشة","t":"living","x":0,"y":5,"w":6,"h":5,"entry":true},{"n":"مطبخ","t":"kitchen","x":6,"y":5,"w":6,"h":5},{"n":"ممر","t":"corridor","x":0,"y":4,"w":12,"h":1}]}';
  var rules='القواعد:\n1. الوحدات بالمتر، نقطة الأصل أعلى اليسار، المحور y يتجه للأسفل.\n'+
    '2. الغرف مستطيلات متجاورة تملأ مستطيلاً كاملاً w×h بالتمام، بلا تداخل وبلا فراغات.\n'+
    '3. كل القيم من مضاعفات 0.5.\n'+
    '4. النوع t من: living, hall, dining, bed, master, bath, kitchen, corridor, store, office, stairs, other.\n'+
    '5. غرفة المدخل (entry:true) ملاصقة للحد السفلي y=h.\n'+
    '6. اربط الغرف بممر أو بصالة مركزية، وضع الحمامات قرب غرف النوم والمطبخ.\n'+
    '7. غرفة النوم لا تقل عن 9م²، الحمام بين 3 و6م²، ولا يقل أي بعد عن 1.5م.\n'+
    '8. أعد كائن JSON واحداً فقط بهذا الشكل، بدون شرح وبدون markdown:\n'+schema;
  if(edit&&plan){
    var cur={w:plan.layout.w,h:plan.layout.h,rooms:plan.layout.rooms.map(function(r){var q={n:r.n,t:r.t,x:r.x,y:r.y,w:r.w,h:r.h};if(r.entry)q.entry=true;return q})};
    return 'أنت مهندس معماري. هذا توزيع الغرف الحالي (JSON):\n'+JSON.stringify(cur)+'\n\nعدّله حسب الطلب: "'+desc+'" مع الحفاظ على بقية التوزيع قدر الإمكان.\n'+rules;
  }
  var parts=['نوع المبنى: '+o.type];
  if(o.area)parts.push('المساحة التقريبية: '+o.area+' م²');
  if(o.beds!=null)parts.push('عدد غرف النوم/المكاتب: '+o.beds);
  if(o.baths!=null)parts.push('عدد الحمامات: '+o.baths);
  return 'أنت مهندس معماري. صمّم توزيع غرف مخطط طابقي لهذه المعطيات: '+parts.join('، ')+'.\n'+(desc?('وصف إضافي: "'+desc+'"\n'):'')+rules;
}

function rotate(L,key){
  if(key==='S'||!key)return L;
  var W=L.w,H=L.h;
  var rooms=L.rooms.map(function(r){
    var q={n:r.n,t:r.t,x:r.x,y:r.y,w:r.w,h:r.h,entry:r.entry};
    if(key==='N'){q.x=r1(W-r.x-r.w);q.y=r1(H-r.y-r.h)}
    else if(key==='E'){q.x=r.y;q.y=r1(W-r.x-r.w);q.w=r.h;q.h=r.w}
    else if(key==='W'){q.x=r1(H-r.y-r.h);q.y=r.x;q.w=r.h;q.h=r.w}
    return q;
  });
  return key==='N'?{w:W,h:H,rooms:rooms}:{w:H,h:W,rooms:rooms};
}
function shared(a,b){
  var ya=Math.max(a.y,b.y),yb=Math.min(a.y+a.h,b.y+b.h),xa=Math.max(a.x,b.x),xb=Math.min(a.x+a.w,b.x+b.w);
  if(yb-ya>0.5&&(near(a.x+a.w,b.x)||near(b.x+b.w,a.x)))return {o:'v',pos:near(a.x+a.w,b.x)?b.x:a.x,a:ya,b:yb};
  if(xb-xa>0.5&&(near(a.y+a.h,b.y)||near(b.y+b.h,a.y)))return {o:'h',pos:near(a.y+a.h,b.y)?b.y:a.y,a:xa,b:xb};
  return null;
}
function extEdges(r,W,H){
  var e=[];
  if(near(r.y,0))e.push({s:'N',o:'h',pos:0,a:r.x,b:r.x+r.w});
  if(near(r.y+r.h,H))e.push({s:'S',o:'h',pos:H,a:r.x,b:r.x+r.w});
  if(near(r.x,0))e.push({s:'W',o:'v',pos:0,a:r.y,b:r.y+r.h});
  if(near(r.x+r.w,W))e.push({s:'E',o:'v',pos:W,a:r.y,b:r.y+r.h});
  return e;
}
function openings(L,key){
  var rooms=L.rooms,W=L.w,H=L.h,doors=[],wins=[],i,j,k;
  if(!rooms.length)return {doors:doors,wins:wins,entry:-1};
  var cands=rooms.filter(function(r){return r.entry});
  if(!cands.length)cands=rooms.filter(function(r){return r.t==='living'||r.t==='hall'});
  if(!cands.length)cands=rooms.slice();
  var entry=null,eEdge=null;
  function edgeOn(r){var es=extEdges(r,W,H);for(var q=0;q<es.length;q++)if(es[q].s===key&&es[q].b-es[q].a>=1.2)return es[q];return null}
  for(i=0;i<cands.length&&!entry;i++){var e1=edgeOn(cands[i]);if(e1){entry=cands[i];eEdge=e1}}
  if(!entry){
    var all=rooms.slice().sort(function(a,b){return b.w*b.h-a.w*a.h});
    for(i=0;i<all.length&&!entry;i++){var e2=edgeOn(all[i]);if(e2){entry=all[i];eEdge=e2}}
  }
  if(!entry){entry=cands[0];eEdge=extEdges(entry,W,H)[0]||null}
  if(eEdge){
    var elen=eEdge.b-eEdge.a;
    doors.push({o:eEdge.o,pos:eEdge.pos,c:(eEdge.a+eEdge.b)/2,w:Math.max(0.7,Math.min(1.1,elen-0.4)),side:INSIDE[eEdge.s],main:true,ri:rooms.indexOf(entry),rj:-1});
  }
  var conn=[entry],pend=rooms.filter(function(r){return r!==entry}),progress=true;
  while(pend.length&&progress){
    progress=false;
    var best=null;
    for(i=0;i<pend.length;i++)for(j=0;j<conn.length;j++){
      var s=shared(pend[i],conn[j]);if(!s)continue;
      var len=s.b-s.a;if(len<0.9)continue;
      var sc=conn[j].t==='corridor'?0:((conn[j].t==='living'||conn[j].t==='hall')?1:2);
      if(!best||sc<best.sc||(sc===best.sc&&len>best.len))best={p:pend[i],c:conn[j],s:s,sc:sc,len:len};
    }
    if(best){
      var dw=(best.p.t==='bath'||best.p.t==='store')?0.8:0.9;dw=Math.max(0.6,Math.min(dw,best.len-0.3));
      var side=(best.s.o==='v')?(near(best.p.x,best.s.pos)?1:-1):(near(best.p.y,best.s.pos)?1:-1);
      doors.push({o:best.s.o,pos:best.s.pos,c:(best.s.a+best.s.b)/2,w:dw,side:side,main:false,ri:rooms.indexOf(best.p),rj:rooms.indexOf(best.c)});
      conn.push(best.p);pend.splice(pend.indexOf(best.p),1);progress=true;
    }
  }
  rooms.forEach(function(r){
    if(r.t==='corridor'||r.t==='store'||r.t==='stairs')return;
    var es=extEdges(r,W,H).sort(function(a,b){return (b.b-b.a)-(a.b-a.a)}),count=0;
    es.forEach(function(e){
      var len=e.b-e.a;if(len<1.4||count>=2)return;
      var isEntryEdge=(r===entry&&eEdge&&e.s===eEdge.s&&near(e.pos,eEdge.pos));
      if(isEntryEdge){
        if(len>=5){var ww=Math.min(1.6,len*0.22);[0.2,0.8].forEach(function(f){wins.push({o:e.o,pos:e.pos,c:e.a+len*f,w:ww})});count++}
        return;
      }
      wins.push({o:e.o,pos:e.pos,c:(e.a+e.b)/2,w:r.t==='bath'?0.6:Math.min(1.6,len*0.5)});count++;
    });
  });
  return {doors:doors,wins:wins,entry:rooms.indexOf(entry)};
}

var COL={living:'#f3efe6',hall:'#f3efe6',dining:'#f5eddc',bed:'#e8eef5',master:'#e1eaf6',bath:'#dff1f5',kitchen:'#f6ecd9',corridor:'#f4f4f4',store:'#ececec',office:'#eef2e6',stairs:'#e9e9e9',other:'#f1f1f1'};
function buildSvg(L,op){
  var W=L.w,H=L.h,mL=105,mR=60,mT=115,mB=95;
  var S=Math.min((1000-mL-mR)/W,(800-mT-mB)/H);
  var ox=mL+((1000-mL-mR)-W*S)/2,oy=mT+((800-mT-mB)-H*S)/2;
  var X=function(x){return r2(ox+x*S)},Y=function(y){return r2(oy+y*S)};
  var wi=Math.max(4,0.12*S),we=Math.max(7,0.24*S);
  var simple=op.detail==='simple',high=(op.detail==='high'),showFurn=op.furn&&!simple,showDims=op.dims&&!simple;
  var o=openings(L,op.key),s=[];

  function furn(r){
    var a=[],t=r.t,x=r.x,y=r.y,w=r.w,h=r.h,i,j;
    function rc(px,py,pw,ph,rx){if(pw<=0.05||ph<=0.05)return;a.push('<rect x="'+X(px)+'" y="'+Y(py)+'" width="'+r2(pw*S)+'" height="'+r2(ph*S)+'" rx="'+r2((rx==null?0.05:rx)*S)+'"/>')}
    function ci(px,py,rad){if(rad<=0)return;a.push('<circle cx="'+X(px)+'" cy="'+Y(py)+'" r="'+r2(rad*S)+'"/>')}
    function el(px,py,rx,ry){a.push('<ellipse cx="'+X(px)+'" cy="'+Y(py)+'" rx="'+r2(rx*S)+'" ry="'+r2(ry*S)+'"/>')}
    function ln(x1,y1,x2,y2){a.push('<line x1="'+X(x1)+'" y1="'+Y(y1)+'" x2="'+X(x2)+'" y2="'+Y(y2)+'"/>')}
    if(t==='bed'||t==='master'){
      var bw=t==='master'?1.8:1.4,bl=2.0;
      if(w<bw+1||h<bl+1){var k=Math.min((w-0.8)/bw,(h-0.8)/bl);if(k<0.5)return '';bw*=k;bl*=k}
      var bx=x+(w-bw)/2,by=y+0.3;
      rc(bx,by,bw,bl);rc(bx+0.1,by+0.1,bw/2-0.15,0.4,0.1);rc(bx+bw/2+0.05,by+0.1,bw/2-0.15,0.4,0.1);
      if(w>=bw+1.8){rc(bx-0.5,by,0.4,0.4);rc(bx+bw+0.1,by,0.4,0.4)}
    }else if(t==='living'){
      if(w>=3&&h>=3){rc(x+0.3,y+h/2-1.1,0.9,2.2);rc(x+1.5,y+h/2-0.5,0.6,1.0);if(w>=4.5)rc(x+w-0.7,y+h/2-0.8,0.4,1.6)}
    }else if(t==='hall'){
      if(r.n.indexOf('طعام')>-1){
        var cols=Math.max(1,Math.floor((w-1)/2.4)),rows=Math.max(1,Math.floor((h-1)/2.0));
        for(i=0;i<cols;i++)for(j=0;j<rows;j++){
          var tx=x+0.5+(w-1)*(i+0.5)/cols-0.5,ty=y+0.5+(h-1)*(j+0.5)/rows-0.4;
          rc(tx,ty,1.0,0.8);ci(tx-0.3,ty+0.4,0.2);ci(tx+1.3,ty+0.4,0.2);
        }
      }else if(w>=3.5&&h>=3){
        rc(x+w-2.6,y+0.5,2.1,0.7);rc(x+0.1,y+0.8,0.45,Math.max(0.5,h-2.2));
      }
    }else if(t==='kitchen'){
      if(w>=2.2&&h>=2.2){
        rc(x+0.1,y+h-0.7,w-0.2,0.6);
        rc(x+w/2-0.3,y+h-0.63,0.6,0.46,0.1);
        ci(x+w*0.22,y+h-0.4,0.1);ci(x+w*0.22+0.3,y+h-0.4,0.1);
        rc(x+0.1,y+h-0.7-Math.min(2.2,h-1.6),0.6,Math.min(2.2,h-1.6));
      }
    }else if(t==='bath'){
      if(w>=1.6&&h>=1.8){
        rc(x+0.1,y+0.1,0.9,0.9);ln(x+0.1,y+0.1,x+1.0,y+1.0);ln(x+1.0,y+0.1,x+0.1,y+1.0);
        if(w>=1.7){rc(x+w-0.65,y+0.12,0.5,0.22);el(x+w-0.4,y+0.65,0.22,0.3)}
        if(h>=2.4)rc(x+0.1,y+1.25,0.45,0.6,0.1);
      }
    }else if(t==='dining'){
      if(w>=2.4&&h>=2.4){
        rc(x+w/2-0.8,y+h/2-0.45,1.6,0.9);
        [-0.5,0,0.5].forEach(function(d){ci(x+w/2+d*1.1,y+h/2-0.7,0.18);ci(x+w/2+d*1.1,y+h/2+0.7,0.18)});
      }
    }else if(t==='office'){
      if(w>=2.4&&h>=2.4){rc(x+0.3,y+0.3,Math.min(1.6,w-0.6),0.7);ci(x+0.3+Math.min(1.6,w-0.6)/2,y+1.4,0.22)}
    }else if(t==='store'){
      if(w>=1.2&&h>=1.2)rc(x+0.1,y+0.1,w-0.2,0.4);
    }else if(t==='stairs'){
      if(w>=1.2&&h>=1.8){
        rc(x+0.3,y+0.3,w-0.6,h-0.6);
        var n=Math.floor((h-0.6)/0.3);for(i=1;i<n;i++)ln(x+0.3,y+0.3+i*0.3,x+w-0.3,y+0.3+i*0.3);
      }
    }
    return a.join('');
  }

  s.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 800" preserveAspectRatio="xMidYMid meet" font-family="system-ui,sans-serif">');
  s.push('<rect width="1000" height="800" fill="#fff"/><rect x="8" y="8" width="984" height="784" fill="none" stroke="#222" stroke-width="1.5"/>');
  s.push('<text x="500" y="42" text-anchor="middle" font-size="24" font-weight="700" fill="#111">'+esc('مخطط طابقي — '+(op.title||''))+'</text>');

  s.push('<g id="floors">');
  L.rooms.forEach(function(r){s.push('<rect x="'+X(r.x)+'" y="'+Y(r.y)+'" width="'+r2(r.w*S)+'" height="'+r2(r.h*S)+'" fill="'+(COL[r.t]||COL.other)+'"/>')});
  s.push('</g>');

  if(showFurn){
    s.push('<g id="furniture" fill="#fff" fill-opacity=".75" stroke="#7b8794" stroke-width="1.1">');
    L.rooms.forEach(function(r){s.push(furn(r))});
    s.push('</g>');
  }

  s.push('<g id="walls" fill="none" stroke="#111" stroke-linejoin="miter">');
  L.rooms.forEach(function(r){s.push('<rect x="'+X(r.x)+'" y="'+Y(r.y)+'" width="'+r2(r.w*S)+'" height="'+r2(r.h*S)+'" stroke-width="'+r2(wi)+'"/>')});
  s.push('<rect x="'+X(0)+'" y="'+Y(0)+'" width="'+r2(W*S)+'" height="'+r2(H*S)+'" stroke-width="'+r2(we)+'"/>');
  s.push('</g>');

  s.push('<g id="openings">');
  o.wins.forEach(function(w){
    var len=r2(w.w*S);
    if(w.o==='h'){var x0=X(w.c-w.w/2),yy=Y(w.pos);
      s.push('<rect x="'+x0+'" y="'+r2(yy-we/2)+'" width="'+len+'" height="'+r2(we)+'" fill="#fff" stroke="#222" stroke-width="1.2"/><line x1="'+x0+'" y1="'+yy+'" x2="'+r2(x0+len)+'" y2="'+yy+'" stroke="#38bdf8" stroke-width="2"/>');
    }else{var xx=X(w.pos),y0=Y(w.c-w.w/2);
      s.push('<rect x="'+r2(xx-we/2)+'" y="'+y0+'" width="'+r2(we)+'" height="'+len+'" fill="#fff" stroke="#222" stroke-width="1.2"/><line x1="'+xx+'" y1="'+y0+'" x2="'+xx+'" y2="'+r2(y0+len)+'" stroke="#38bdf8" stroke-width="2"/>');
    }
  });
  o.doors.forEach(function(d){
    var dw=r2(d.w*S),t=r2((d.main?we:wi)+2.5),sd=d.side;
    if(d.o==='h'){
      var yy=Y(d.pos),x0=X(d.c-d.w/2),x1=r2(x0+dw),ye=r2(yy+sd*dw);
      s.push('<line x1="'+x0+'" y1="'+yy+'" x2="'+x1+'" y2="'+yy+'" stroke="#fff" stroke-width="'+t+'"/>');
      s.push('<line x1="'+x0+'" y1="'+yy+'" x2="'+x0+'" y2="'+ye+'" stroke="#111" stroke-width="2.5"/>');
      s.push('<path d="M'+x1+','+yy+' A'+dw+','+dw+' 0 0 '+(sd>0?1:0)+' '+x0+','+ye+'" fill="none" stroke="#666" stroke-width="1.2"/>');
    }else{
      var xx=X(d.pos),y0=Y(d.c-d.w/2),y1=r2(y0+dw),xe=r2(xx+sd*dw);
      s.push('<line x1="'+xx+'" y1="'+y0+'" x2="'+xx+'" y2="'+y1+'" stroke="#fff" stroke-width="'+t+'"/>');
      s.push('<line x1="'+xx+'" y1="'+y0+'" x2="'+xe+'" y2="'+y0+'" stroke="#111" stroke-width="2.5"/>');
      s.push('<path d="M'+xx+','+y1+' A'+dw+','+dw+' 0 0 '+(sd>0?0:1)+' '+xe+','+y0+'" fill="none" stroke="#666" stroke-width="1.2"/>');
    }
  });
  s.push('</g>');

  s.push('<g id="labels" text-anchor="middle" fill="#111" stroke="#fff" stroke-width="3" paint-order="stroke">');
  L.rooms.forEach(function(r){
    var pw=r.w*S,ph=r.h*S,cx=X(r.x+r.w/2),cy=Y(r.y+r.h/2);
    var fs=Math.max(9,Math.min(22,pw*0.9/(Math.max(r.n.length,5)*0.7)));fs=Math.min(fs,ph/3.2);
    var lines=[{t:r.n,f:fs,b:true}];
    if(!simple&&ph>fs*3.2)lines.push({t:f1(r.w*r.h)+' م²',f:fs*0.8});
    if(high&&showDims&&ph>fs*4.6&&pw>fs*5)lines.push({t:f1(r.w)+'×'+f1(r.h),f:fs*0.7});
    var lh=fs*1.25,y0=cy-(lines.length-1)*lh/2;
    lines.forEach(function(l,i){
      s.push('<text x="'+cx+'" y="'+r2(y0+i*lh)+'" dominant-baseline="central" font-size="'+r2(l.f)+'"'+(l.b?' font-weight="700"':'')+'>'+esc(l.t)+'</text>');
    });
  });
  s.push('</g>');

  if(showDims){
    s.push('<g id="dimensions" stroke="#555" stroke-width="1" fill="#333" font-size="13" text-anchor="middle">');
    var yo=r2(oy-40),xo=r2(ox-48);
    function dimH(a,b,y,label,fsz){
      return '<line x1="'+a+'" y1="'+y+'" x2="'+b+'" y2="'+y+'"/><line x1="'+r2(a-4)+'" y1="'+r2(y+4)+'" x2="'+r2(a+4)+'" y2="'+r2(y-4)+'"/><line x1="'+r2(b-4)+'" y1="'+r2(y+4)+'" x2="'+r2(b+4)+'" y2="'+r2(y-4)+'"/>'+
        '<text x="'+r2((a+b)/2)+'" y="'+r2(y-6)+'" font-size="'+fsz+'" stroke="none">'+label+'</text>';
    }
    function dimV(a,b,x,label,fsz){
      var cy=r2((a+b)/2),tx=r2(x-7);
      return '<line x1="'+x+'" y1="'+a+'" x2="'+x+'" y2="'+b+'"/><line x1="'+r2(x-4)+'" y1="'+r2(a+4)+'" x2="'+r2(x+4)+'" y2="'+r2(a-4)+'"/><line x1="'+r2(x-4)+'" y1="'+r2(b+4)+'" x2="'+r2(x+4)+'" y2="'+r2(b-4)+'"/>'+
        '<text x="'+tx+'" y="'+cy+'" transform="rotate(-90 '+tx+' '+cy+')" font-size="'+fsz+'" stroke="none">'+label+'</text>';
    }
    s.push(dimH(X(0),X(W),yo,f1(W)+' م',15));
    s.push(dimV(Y(0),Y(H),xo,f1(H)+' م',15));
    var top=L.rooms.filter(function(r){return near(r.y,0)}).sort(function(a,b){return a.x-b.x});
    if(top.length>1)top.forEach(function(r){s.push(dimH(X(r.x),X(r.x+r.w),r2(oy-20),f1(r.w),top.length>8?10:12))});
    var left=L.rooms.filter(function(r){return near(r.x,0)}).sort(function(a,b){return a.y-b.y});
    if(left.length>1)left.forEach(function(r){s.push(dimV(Y(r.y),Y(r.y+r.h),r2(ox-22),f1(r.h),left.length>8?10:12))});
    s.push('</g>');
  }

  if(op.north){
    s.push('<g id="north" transform="translate(935,78)"><circle r="24" fill="#fff" stroke="#333" stroke-width="1.5"/><polygon points="0,-19 8,10 0,4 -8,10" fill="#111"/><text y="-32" text-anchor="middle" font-size="16" font-weight="700" fill="#111">N</text></g>');
    var nb=(W*1>=10)?5:2,bl=nb*S;
    if(bl>300){nb=2;bl=nb*S}
    var bx=mL,by=800-52;
    s.push('<g id="scale" font-size="13" fill="#333" text-anchor="middle">');
    for(var q=0;q<nb;q++)s.push('<rect x="'+r2(bx+q*S)+'" y="'+by+'" width="'+r2(S)+'" height="8" fill="'+(q%2?'#fff':'#111')+'" stroke="#111" stroke-width="1"/>');
    s.push('<text x="'+bx+'" y="'+(by+24)+'">0</text><text x="'+r2(bx+bl)+'" y="'+(by+24)+'">'+nb+' م</text></g>');
  }
  s.push('<text x="960" y="765" text-anchor="end" font-size="16" fill="#444">'+esc('المساحة الإجمالية: '+f1(W*H)+' م²')+'</text>');
  s.push('</svg>');
  return s.join('');
}

function redraw(keepView){
  if(!plan)return;
  var key=KEY[$('o-door').value]||'S';
  var L=rotate(plan.layout,key);
  currentSvg=buildSvg(L,{key:key,detail:$('o-detail').value,furn:$('o-furn').checked,dims:$('o-dims').checked,north:$('o-north').checked,title:plan.type});
  stage.innerHTML=currentSvg;placeholder.style.display='none';
  if(!keepView)resetView();
}
['o-door','o-detail','o-furn','o-dims','o-north'].forEach(function(id){$(id).addEventListener('change',function(){redraw(true)})});

var HK='arch_lab_history_v3';
function loadHist(){try{return JSON.parse(localStorage.getItem(HK)||'[]')}catch(e){return []}}
function saveHist(title,L,ty){
  try{
    var h=loadHist();h.unshift({t:String(title).slice(0,60),L:L,ty:ty});
    localStorage.setItem(HK,JSON.stringify(h.slice(0,12)));
  }catch(e){}
}
function showHist(){
  var m=$('histmenu'),h=loadHist();m.innerHTML='';
  if(!h.length){var e=document.createElement('button');e.textContent='لا توجد مخططات محفوظة';e.disabled=true;m.appendChild(e)}
  h.forEach(function(it){
    var b=document.createElement('button');b.textContent='📄 '+it.t;
    b.onclick=function(){plan={layout:it.L,type:it.ty};redraw();setEdit(true);m.style.display='none'};
    m.appendChild(b);
  });
  m.style.display='block';
}
$('hist-btn').onclick=function(e){e.stopPropagation();$('savemenu').style.display='none';var m=$('histmenu');m.style.display==='block'?m.style.display='none':showHist()};
$('new-btn').onclick=function(){
  plan=null;currentSvg='';stage.innerHTML='';placeholder.style.display='flex';promptEl.value='';setEdit(false);resetView();
};

function setPlan(L,type,desc){
  plan={layout:L,type:type};redraw();saveHist(desc||type,L,type);setEdit(true);
}
function drawLocal(desc,o,note){
  setPlan(generateLocal(o),o.type,desc);
  toast(note||'تم رسم المخطط ✔');
}

genBtn.addEventListener('click',function(){
  if(busy)return;
  var desc=promptEl.value.trim(),o=readOpts(desc);
  var useAi=!$('o-local').checked&&window.Android&&window.Android.askAi;
  if(editMode){
    if(!desc){toast('اكتب التعديل المطلوب');return}
    if(!useAi){toast('التعديل يحتاج الذكاء الاصطناعي: ألغِ «رسم سريع»');return}
  }
  if(!useAi){drawLocal(desc,o,window.Android?'تم الرسم بالقالب السريع ✔':'تم الرسم بالقالب المحلي (لا يوجد اتصال بالذكاء الاصطناعي)');return}
  pending={desc:desc,o:o,edit:editMode};
  setLoading(true,editMode?'جاري تعديل المخطط...':'جاري توزيع الغرف...');
  clearTimeout(aiTimer);
  aiTimer=setTimeout(function(){if(pending)window.onAiResult('architecture_gen',false,'انتهت المهلة')},75000);
  try{window.Android.askAi('architecture_gen','architecture',aiPrompt(desc,o,editMode))}
  catch(e){window.onAiResult('architecture_gen',false,String(e))}
});

window.onAiResult=function(id,ok,text){
  if(id!=='architecture_gen'||!pending)return;
  clearTimeout(aiTimer);
  var p=pending;pending=null;setLoading(false);
  var L=ok?normalizeLayout(extractJson(text)):null;
  if(L){
    setPlan(L,(p.edit&&plan)?plan.type:p.o.type,p.desc);
    promptEl.value='';toast('تم رسم المخطط ✔ يمكنك الآن طلب تعديلات');
    return;
  }
  var why=ok?'رد الذكاء الاصطناعي غير صالح':('فشل الاتصال: '+String(text||'').slice(0,60));
  if(p.edit){toast(why+' — لم يتغير المخطط');return}
  drawLocal(p.desc,p.o,why+' — رُسم بالقالب المحلي');
};

function applyView(){stage.style.transform='translate('+view.x+'px,'+view.y+'px) scale('+view.s+')'}
function resetView(){view={x:0,y:0,s:1};applyView()}
function zoomAt(f,cx,cy){
  var ns=Math.min(8,Math.max(.5,view.s*f));f=ns/view.s;
  view.x=cx-(cx-view.x)*f;view.y=cy-(cy-view.y)*f;view.s=ns;applyView();
}
function center(){var r=viewport.getBoundingClientRect();return [r.width/2,r.height/2]}
$('z-in').onclick=function(){var c=center();zoomAt(1.3,c[0],c[1])};
$('z-out').onclick=function(){var c=center();zoomAt(1/1.3,c[0],c[1])};
$('z-reset').onclick=resetView;
viewport.addEventListener('wheel',function(e){
  e.preventDefault();var r=viewport.getBoundingClientRect();
  zoomAt(e.deltaY<0?1.12:1/1.12,e.clientX-r.left,e.clientY-r.top);
},{passive:false});
var ptrs={},lastDist=0;
viewport.addEventListener('pointerdown',function(e){
  if(e.target&&e.target.closest&&e.target.closest('#zoom'))return;
  ptrs[e.pointerId]={x:e.clientX,y:e.clientY};
  try{viewport.setPointerCapture(e.pointerId)}catch(x){}
  lastDist=0;
});
viewport.addEventListener('pointermove',function(e){
  var p=ptrs[e.pointerId];if(!p)return;
  var ids=Object.keys(ptrs);
  if(ids.length===1){view.x+=e.clientX-p.x;view.y+=e.clientY-p.y;p.x=e.clientX;p.y=e.clientY;applyView()}
  else if(ids.length===2){
    p.x=e.clientX;p.y=e.clientY;
    var a=ptrs[ids[0]],b=ptrs[ids[1]],d=Math.hypot(a.x-b.x,a.y-b.y);
    if(lastDist){var r=viewport.getBoundingClientRect();zoomAt(d/lastDist,(a.x+b.x)/2-r.left,(a.y+b.y)/2-r.top)}
    lastDist=d;
  }
});
function endPtr(e){delete ptrs[e.pointerId];lastDist=0}
viewport.addEventListener('pointerup',endPtr);
viewport.addEventListener('pointercancel',endPtr);
viewport.addEventListener('dblclick',resetView);

function exportSvgString(){return currentSvg.replace('<svg ','<svg width="1000" height="800" ')}
function exportPng(){
  var blob=new Blob([exportSvgString()],{type:'image/svg+xml;charset=utf-8'});
  var url=URL.createObjectURL(blob),img=new Image();
  img.onload=function(){
    var c=document.createElement('canvas');c.width=2000;c.height=1600;
    var g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,2000,1600);g.drawImage(img,0,0,2000,1600);
    URL.revokeObjectURL(url);
    try{window.Android.savePng(c.toDataURL('image/png').split(',')[1])}catch(e){toast('تعذر إنشاء الصورة')}
  };
  img.onerror=function(){URL.revokeObjectURL(url);toast('تعذر إنشاء الصورة')};
  img.src=url;
}
$('save-btn').addEventListener('click',function(e){
  e.stopPropagation();$('histmenu').style.display='none';
  if(!currentSvg){toast('لا يوجد مخطط لحفظه');return}
  var m=$('savemenu');m.style.display=m.style.display==='block'?'none':'block';
});
$('savemenu').addEventListener('click',function(e){
  var f=e.target.getAttribute&&e.target.getAttribute('data-fmt');if(!f)return;
  $('savemenu').style.display='none';
  if(!window.Android){toast('الحفظ متاح داخل التطبيق فقط');return}
  if(f==='png'&&window.Android.savePng)exportPng();
  else if(f==='svg'&&window.Android.saveSvg)window.Android.saveSvg(exportSvgString());
  else if(f==='html'&&window.Android.saveBlueprint){
    window.Android.saveBlueprint('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Architecture Blueprint</title><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fafafa}svg{max-width:100%;max-height:100%}</style></head><body>'+currentSvg+'</body></html>','architecture');
  }else toast('هذه الصيغة غير مدعومة في هذه النسخة');
});
document.addEventListener('click',function(){$('savemenu').style.display='none';$('histmenu').style.display='none'});

var h0=loadHist();
if(h0.length&&h0[0].L&&h0[0].L.rooms){plan={layout:h0[0].L,type:h0[0].ty};redraw();setEdit(true)}
})();
</script>
</body>
</html>
'''

os.makedirs("app/src/main/assets", exist_ok=True)
with open(HTML_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(html_content)
print(">> Wrote " + HTML_PATH)

# 3) تسجيل النشاط
register_activity("ArchitectureActivity")

print(">> Architecture Lab Patch v3 applied successfully!")
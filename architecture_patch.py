import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"


def replace_once(file_path, old, new, silent_if_exists=False, required=True):
    """Replace exactly one occurrence of `old`. Fails loudly instead of silently skipping."""
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
    """Register .<name> in AndroidManifest.xml (skips if already declared)."""
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


print(">> Applying Architecture Lab Patch v2...")

# ---------------------------------------------------------------------------
# 1) architecture_lab.html
# ---------------------------------------------------------------------------
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
#header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--panel);border-bottom:1px solid var(--border)}
#header h1{margin:0;font-size:1.1rem;color:var(--accent)}
.hbtns{display:flex;gap:8px}
.ibtn{height:38px;min-width:38px;padding:0 10px;background:transparent;border:1px solid var(--border);color:var(--text);border-radius:8px;cursor:pointer;font-size:1rem}
.ibtn:active{background:var(--border)}
#options{background:var(--panel);border-bottom:1px solid var(--border);padding:0 14px}
#options summary{padding:8px 0;color:var(--accent);cursor:pointer;font-size:.9rem}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;padding-bottom:10px}
.grid label{display:flex;flex-direction:column;gap:4px;font-size:.78rem;color:var(--muted)}
.grid select,.grid input[type=number]{padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:.9rem}
.checks{grid-column:1/-1;display:flex;gap:14px;flex-wrap:wrap;font-size:.85rem}
.checks label{flex-direction:row;align-items:center;color:var(--text)}
#chips{display:flex;gap:8px;overflow-x:auto;padding:8px 14px;background:var(--bg);scrollbar-width:none}
.chip{white-space:nowrap;padding:6px 12px;border:1px solid var(--border);border-radius:16px;background:var(--panel);color:var(--text);font-size:.8rem;cursor:pointer}
#workspace{flex:1;position:relative;background-color:#0a192f;background-image:linear-gradient(#233554 1px,transparent 1px),linear-gradient(90deg,#233554 1px,transparent 1px);background-size:20px 20px;padding:8px;overflow:hidden}
#viewport{width:100%;height:100%;background:#fff;border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.5);overflow:hidden;position:relative;touch-action:none}
#stage{position:absolute;inset:0;display:flex;justify-content:center;align-items:center;transform-origin:0 0}
#stage svg{width:100%;height:100%;display:block}
#placeholder{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#64748b;text-align:center;padding:20px;line-height:1.8;pointer-events:none}
#zoom{position:absolute;bottom:18px;left:18px;display:flex;flex-direction:column;gap:6px;z-index:5}
#zoom button{width:38px;height:38px;border-radius:8px;border:1px solid var(--border);background:rgba(17,34,64,.92);color:var(--accent);font-size:1.1rem;cursor:pointer}
#loading{position:absolute;inset:0;background:rgba(10,25,47,.85);display:none;justify-content:center;align-items:center;z-index:10;color:var(--accent);flex-direction:column;gap:10px;backdrop-filter:blur(4px)}
.spinner{width:46px;height:46px;border:4px solid rgba(100,255,218,.2);border-top-color:var(--accent);border-radius:50%;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#footer{padding:10px;background:var(--panel);border-top:1px solid var(--border);display:flex;flex-direction:column;gap:8px}
#modebar{display:none;font-size:.8rem;color:var(--warn)}
#row{display:flex;gap:8px;align-items:center}
#prompt{flex:1;padding:12px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:1rem;outline:none;resize:none;height:50px;font-family:inherit}
#prompt:focus{border-color:var(--accent)}
#generate-btn{padding:0 18px;height:50px;background:var(--accent);color:#0a192f;border:none;border-radius:8px;font-size:1rem;font-weight:bold;cursor:pointer}
#generate-btn:disabled{opacity:.5}
#save-btn{height:50px;width:50px;background:transparent;border:1px solid var(--accent);color:var(--accent);border-radius:8px;cursor:pointer;font-size:1.2rem}
.menu{position:absolute;background:var(--panel);border:1px solid var(--border);border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.5);z-index:50;display:none;min-width:200px;overflow:hidden}
.menu button{display:block;width:100%;text-align:right;padding:12px 14px;background:transparent;border:0;border-bottom:1px solid var(--border);color:var(--text);font-size:.95rem;cursor:pointer}
.menu button:last-child{border-bottom:0}
.menu button:active{background:var(--border)}
#savemenu{bottom:76px;left:10px}
#histmenu{top:56px;left:10px;max-height:55vh;overflow:auto;min-width:250px}
#toast{position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:var(--accent);color:#0a192f;padding:10px 20px;border-radius:20px;font-weight:bold;opacity:0;transition:opacity .3s;pointer-events:none;z-index:100;max-width:90%;text-align:center}
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
          <option value="دوبلكس">دوبلكس (طابقان)</option>
          <option value="مكتب">مكتب</option>
          <option value="محل تجاري">محل تجاري</option>
          <option value="مطعم / مقهى">مطعم / مقهى</option>
          <option value="عيادة">عيادة</option>
        </select>
      </label>
      <label>المساحة الكلية (م²)
        <input type="number" id="o-area" min="20" max="2000" placeholder="مثال: 120">
      </label>
      <label>غرف النوم
        <input type="number" id="o-beds" min="0" max="12" placeholder="مثال: 2">
      </label>
      <label>الحمامات
        <input type="number" id="o-baths" min="0" max="10" placeholder="مثال: 2">
      </label>
      <label>اتجاه المدخل
        <select id="o-door">
          <option value="">تلقائي</option>
          <option value="الجنوب">جنوب</option>
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
      </div>
    </div>
  </details>

  <div id="chips"></div>

  <div id="workspace">
    <div id="viewport">
      <div id="stage"></div>
      <div id="placeholder">اكتب وصف المبنى في الأسفل<br>أو اختر نموذجاً سريعاً من الأعلى</div>
      <div id="zoom">
        <button id="z-in">＋</button>
        <button id="z-out">－</button>
        <button id="z-reset" title="إعادة الضبط">⤾</button>
      </div>
    </div>
    <div id="loading"><div class="spinner"></div><div id="loading-text">جاري رسم المخطط الهندسي...</div></div>
  </div>

  <div id="footer">
    <div id="modebar">✏️ وضع التعديل: سيتم تعديل المخطط الحالي — <a href="#" id="exit-edit" style="color:var(--accent)">رسم جديد بدلاً من ذلك</a></div>
    <div id="row">
      <button id="save-btn" title="حفظ / مشاركة">💾</button>
      <textarea id="prompt" placeholder="وصف المبنى (مثال: فيلا دور واحد، 3 غرف، صالة، مطبخ، حديقة...)"></textarea>
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
var currentSvg='',lastRequest='',editMode=false,busy=false,retried=false,toastTimer=null;
var view={x:0,y:0,s:1};

var TEMPLATES=[
  ['🏢 شقة 120م²','شقة بمساحة 120 متر مربع: غرفتان نوم، صالة كبيرة، مطبخ مفتوح، حمامان، شرفة'],
  ['🏡 فيلا دور واحد','فيلا من طابق واحد: 3 غرف نوم (واحدة ماستر مع حمام)، صالة معيشة، مجلس ضيوف، مطبخ، حمامان، مدخل سيارة، حديقة أمامية'],
  ['🏘️ استوديو 45م²','استوديو صغير 45 متر مربع بغرفة معيشة ونوم مدمجة، مطبخ أمريكي، حمام، مساحة تخزين'],
  ['🏪 محل تجاري','محل تجاري 80 متر مربع: صالة عرض، كاونتر، مخزن، حمام، واجهة زجاجية'],
  ['☕ مقهى','مقهى بمساحة 100 متر مربع: منطقة جلوس، بار تحضير، مطبخ صغير، حمامان، مدخل واسع'],
  ['🏥 عيادة','عيادة طبية: استقبال، صالة انتظار، غرفتا كشف، حمام، مكتب إداري']
];
var chipsEl=$('chips');
TEMPLATES.forEach(function(t){
  var b=document.createElement('button');b.className='chip';b.textContent=t[0];
  b.onclick=function(){promptEl.value=t[1];setEdit(false);promptEl.focus()};
  chipsEl.appendChild(b);
});

function toast(msg){
  toastEl.textContent=msg;toastEl.style.opacity=1;
  clearTimeout(toastTimer);toastTimer=setTimeout(function(){toastEl.style.opacity=0},3000);
}
function setLoading(on,txt){
  busy=on;loading.style.display=on?'flex':'none';genBtn.disabled=on;
  if(txt)$('loading-text').textContent=txt;
}
function setEdit(on){
  editMode=on&&!!currentSvg;
  $('modebar').style.display=editMode?'block':'none';
  promptEl.placeholder=editMode?'ما التعديل المطلوب؟ (مثال: كبّر المطبخ وأضف غرفة غسيل)':'وصف المبنى (مثال: فيلا دور واحد، 3 غرف، صالة، مطبخ، حديقة...)';
  genBtn.textContent=editMode?'✏️ عدّل':'✨ ارسم';
}
$('exit-edit').onclick=function(e){e.preventDefault();setEdit(false)};

/* ---------- Prompt building ---------- */
function optionsText(){
  var parts=[];
  parts.push('نوع المبنى: '+$('o-type').value);
  if($('o-area').value)parts.push('المساحة الكلية التقريبية: '+$('o-area').value+' م²');
  if($('o-beds').value)parts.push('عدد غرف النوم: '+$('o-beds').value);
  if($('o-baths').value)parts.push('عدد الحمامات: '+$('o-baths').value);
  if($('o-door').value)parts.push('اتجاه المدخل الرئيسي: '+$('o-door').value);
  return parts.join('، ');
}
var RULES=function(){
  var detail=$('o-detail').value,furn=$('o-furn').checked&&detail!=='simple',
      dims=$('o-dims').checked&&detail!=='simple',north=$('o-north').checked;
  var r=[
    'استخدم viewBox="0 0 1000 800" وxmlns="http://www.w3.org/2000/svg" بدون width/height.',
    'رتّب الرسم في مجموعات <g> بالأسماء: id="floors" (أرضيات الغرف بألوان فاتحة مختلفة قليلاً حسب الوظيفة)، id="walls" (جدران سوداء stroke-width 8 إلى 10، والجدران الخارجية أسمك)، id="openings"، id="labels"'+(furn?'، id="furniture"':'')+(dims?'، id="dimensions"':'')+'.',
    'الأبواب: فتحة في الجدار + خط الضلفة + قوس ربع دائرة (path) يبيّن اتجاه الفتح. النوافذ: خطان متوازيان رفيعان داخل سُمك الجدار مع فتحة بيضاء.',
    'لكل غرفة اسمها بالعربية ومساحتها التقريبية بالمتر المربع (مثل "غرفة نوم 14م²") في وسطها بخط واضح font-size بين 14 و 20 وبـ text-anchor="middle".',
    'الغرف متجاورة دون تداخل ولا فراغات غير مبررة، والمجموع قريب من المساحة المطلوبة، مع ممر أو صالة تربط الغرف منطقياً، والحمامات قرب بعضها أو قرب المطبخ لتوفير شبكة السباكة.',
    'الألوان: خلفية بيضاء، جدران #111، أرضيات رمادية/بيج فاتحة، حمامات بلون مائل للأزرق الفاتح.',
    'أضف إطاراً رفيعاً حول الرسم وعنواناً صغيراً أعلى اليسار.'
  ];
  if(furn)r.push('ارسم رموز أثاث مبسطة بخطوط رفيعة رمادية: سرير مع وسادتين، أريكة وطاولة، طاولة طعام وكراسي، مطبخ (حوض + موقد + كاونتر L)، مرحاض وحوض ودش في الحمامات.');
  if(dims)r.push('أضف خطوط أبعاد خارجية مع أسهم صغيرة وقيم بالمتر على الجهتين الأفقية والعمودية.');
  if(north)r.push('أضف سهم الشمال (N) في زاوية، ومقياس رسم بسيط (شريط 0-5 م) في الأسفل.');
  var out='';r.forEach(function(x,i){out+=(i+1)+'. '+x+'\n'});
  return out;
};
function buildPrompt(userText){
  var base='أنت مهندس معماري خبير في إعداد المخططات الطابقية (Floor Plans).\n';
  if(editMode){
    return base+'هذا هو المخطط الحالي بصيغة SVG:\n'+currentSvg+'\n\nعدّله حسب الطلب التالي مع الحفاظ على بقية التصميم كما هو قدر الإمكان: "'+userText+'".\n'+
      'التزم بنفس القواعد التالية:\n'+RULES()+'أعد كود SVG الكامل المعدّل فقط، بدون أي شرح وبدون علامات markdown.';
  }
  return base+'صمّم مخططاً طابقياً احترافياً بصيغة SVG وفق المعطيات:\n'+optionsText()+'\nوصف العميل: "'+userText+'"\n\nالقواعد:\n'+RULES()+
    'ممنوع استخدام <script> أو <foreignObject> أو صور خارجية. أعد كود SVG فقط، بدون أي شرح وبدون علامات markdown.';
}

/* ---------- SVG extraction / sanitizing ---------- */
function extractSvg(text){
  if(!text)return '';
  var m=String(text).match(/<svg[\s\S]*<\/svg>/i);
  return m?m[0]:'';
}
function sanitizeSvg(src){
  var doc=new DOMParser().parseFromString(src,'image/svg+xml');
  if(doc.getElementsByTagName('parsererror').length)return '';
  var svg=doc.documentElement;
  if(!svg||svg.nodeName.toLowerCase()!=='svg')return '';
  var bad=['script','foreignObject','iframe','object','embed','audio','video','image','use'];
  bad.forEach(function(t){
    var els=Array.prototype.slice.call(doc.getElementsByTagName(t));
    els.forEach(function(e){e.parentNode&&e.parentNode.removeChild(e)});
  });
  var all=doc.getElementsByTagName('*');
  for(var i=0;i<all.length;i++){
    var el=all[i],attrs=Array.prototype.slice.call(el.attributes);
    attrs.forEach(function(a){
      var n=a.name.toLowerCase(),v=(a.value||'').trim().toLowerCase();
      if(n.indexOf('on')===0||((n==='href'||n==='xlink:href')&&v.indexOf('javascript:')===0)||v.indexOf('javascript:')>-1)el.removeAttribute(a.name);
    });
  }
  svg.setAttribute('xmlns','http://www.w3.org/2000/svg');
  if(!svg.getAttribute('viewBox'))svg.setAttribute('viewBox','0 0 1000 800');
  svg.removeAttribute('width');svg.removeAttribute('height');
  svg.setAttribute('preserveAspectRatio','xMidYMid meet');
  return new XMLSerializer().serializeToString(svg);
}

/* ---------- Rendering / zoom ---------- */
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
viewport.addEventListener('pointerdown',function(e){ptrs[e.pointerId]={x:e.clientX,y:e.clientY};viewport.setPointerCapture(e.pointerId);lastDist=0});
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

function render(svg){
  currentSvg=svg;stage.innerHTML=svg;placeholder.style.display='none';resetView();
}

/* ---------- History ---------- */
var HK='arch_lab_history_v2';
function loadHist(){try{return JSON.parse(localStorage.getItem(HK)||'[]')}catch(e){return []}}
function saveHist(title,svg){
  try{
    var h=loadHist();h.unshift({t:title.slice(0,60),s:svg,d:Date.now()});
    h=h.slice(0,8);
    while(h.length>1&&JSON.stringify(h).length>1800000)h.pop();
    localStorage.setItem(HK,JSON.stringify(h));
  }catch(e){}
}
function showHist(){
  var m=$('histmenu'),h=loadHist();m.innerHTML='';
  if(!h.length){m.innerHTML='<button disabled>لا توجد مخططات محفوظة</button>'}
  h.forEach(function(it){
    var b=document.createElement('button');
    b.textContent='📄 '+it.t;
    b.onclick=function(){render(it.s);setEdit(false);m.style.display='none'};
    m.appendChild(b);
  });
  m.style.display='block';
}
$('hist-btn').onclick=function(e){e.stopPropagation();$('savemenu').style.display='none';var m=$('histmenu');m.style.display==='block'?m.style.display='none':showHist()};
$('new-btn').onclick=function(){
  currentSvg='';stage.innerHTML='';placeholder.style.display='flex';promptEl.value='';setEdit(false);resetView();
};

/* ---------- Generate ---------- */
function send(promptText){
  if(!window.Android||!window.Android.askAi){toast('Android bridge not available');return}
  setLoading(true,editMode?'جاري تعديل المخطط...':'جاري رسم المخطط الهندسي...');
  window.Android.askAi('architecture_gen','architecture',promptText);
}
genBtn.addEventListener('click',function(){
  if(busy)return;
  var t=promptEl.value.trim();
  if(!t){toast('اكتب وصفاً أو التعديل المطلوب');return}
  lastRequest=t;retried=false;
  send(buildPrompt(t));
});

window.onAiResult=function(id,ok,text){
  if(id!=='architecture_gen')return;
  if(!ok||!text){setLoading(false);toast('فشل التوليد: '+(text||''));return}
  var svg=sanitizeSvg(extractSvg(text));
  if(!svg){
    if(!retried){
      retried=true;
      send('الرد السابق لم يكن SVG صالحاً. أعد إنتاج المخطط كاملاً بصيغة SVG صحيحة ومغلقة الوسوم فقط (بدون markdown وبدون شرح) للطلب التالي:\n'+buildPrompt(lastRequest));
      return;
    }
    setLoading(false);toast('الرد لا يحتوي على SVG صالح، حاول مرة أخرى');return;
  }
  setLoading(false);
  render(svg);saveHist(lastRequest,svg);
  setEdit(true);promptEl.value='';
  toast('تم رسم المخطط! يمكنك الآن طلب تعديلات عليه');
};

/* ---------- Save / export ---------- */
function exportSvgString(){
  return currentSvg.replace('<svg ','<svg width="1000" height="800" ');
}
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
  if(!window.Android){toast('Android bridge not available');return}
  if(f==='png')exportPng();
  else if(f==='svg'&&window.Android.saveSvg)window.Android.saveSvg(exportSvgString());
  else if(f==='html'&&window.Android.saveBlueprint){
    window.Android.saveBlueprint('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Architecture Blueprint</title><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fafafa}svg{max-width:100%;max-height:100%}</style></head><body>'+currentSvg+'</body></html>','architecture');
  }
});
document.addEventListener('click',function(){$('savemenu').style.display='none';$('histmenu').style.display='none'});

/* restore last plan */
var h0=loadHist();if(h0.length){render(h0[0].s);setEdit(true)}
})();
</script>
</body>
</html>'''

os.makedirs("app/src/main/assets", exist_ok=True)
with open("app/src/main/assets/architecture_lab.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# ---------------------------------------------------------------------------
# 2) ArchitectureActivity.kt
# ---------------------------------------------------------------------------
activity_content = r'''package com.zevorix.assistant

import android.annotation.SuppressLint
import android.content.ContentValues
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
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.zevorix.assistant.data.AiChatService
import com.zevorix.assistant.data.AiResult
import com.zevorix.assistant.ui.theme.VoiceAssistantTheme
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ArchitectureActivity : ComponentActivity() {
    private val aiService = AiChatService()
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    private var webViewRef: WebView? = null

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
                                // assets are served via file:///android_asset regardless of this flag
                                settings.allowFileAccess = false
                                settings.allowContentAccess = false
                                webViewClient = WebViewClient()
                                addJavascriptInterface(Bridge(this@ArchitectureActivity, this, aiService, scope), "Android")
                                loadUrl("file:///android_asset/architecture_lab.html")
                                webViewRef = this
                            }
                        }
                    )
                }
            }
        }
    }

    override fun onDestroy() {
        scope.cancel()
        webViewRef?.apply {
            removeJavascriptInterface("Android")
            stopLoading()
            destroy()
        }
        webViewRef = null
        super.onDestroy()
    }

    class Bridge(
        private val activity: ComponentActivity,
        private val webView: WebView,
        private val aiService: AiChatService,
        private val scope: CoroutineScope
    ) {
        private fun q(s: String): String = JSONObject.quote(s)

        private fun toast(msg: String) {
            scope.launch(Dispatchers.Main) { Toast.makeText(activity, msg, Toast.LENGTH_LONG).show() }
        }

        private fun callJs(id: String, ok: Boolean, text: String) {
            webView.evaluateJavascript("window.onAiResult(${q(id)}, $ok, ${q(text)});", null)
        }

        @JavascriptInterface
        fun askAi(id: String, type: String, prompt: String) {
            scope.launch(Dispatchers.IO) {
                val lang = if (prompt.any { it in '\u0600'..'\u06FF' })
                    com.zevorix.assistant.viewmodel.AppLanguage.ARABIC
                else
                    com.zevorix.assistant.viewmodel.AppLanguage.ENGLISH
                val result = try {
                    aiService.ask(prompt, lang)
                } catch (e: Exception) {
                    null
                }
                withContext(Dispatchers.Main) {
                    when (result) {
                        is AiResult.Success -> callJs(id, true, result.text)
                        is AiResult.Error -> callJs(id, false, "Error: ${result.kind} ${result.detail}")
                        null -> callJs(id, false, "Error: request failed")
                    }
                }
            }
        }

        @JavascriptInterface
        fun saveBlueprint(html: String, type: String) {
            saveBytes("architecture", "html", "text/html", html.toByteArray(Charsets.UTF_8))
        }

        @JavascriptInterface
        fun saveSvg(svg: String) {
            saveBytes("architecture", "svg", "image/svg+xml", svg.toByteArray(Charsets.UTF_8))
        }

        @JavascriptInterface
        fun savePng(base64: String) {
            try {
                saveBytes("architecture", "png", "image/png", Base64.decode(base64, Base64.DEFAULT))
            } catch (e: Exception) {
                toast("فشل الحفظ: ${e.message}")
            }
        }

        private fun saveBytes(prefix: String, ext: String, mime: String, bytes: ByteArray) {
            scope.launch(Dispatchers.IO) {
                try {
                    val stamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
                    val filename = "${prefix}_$stamp.$ext"
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                        val resolver = activity.contentResolver
                        val values = ContentValues().apply {
                            put(MediaStore.MediaColumns.DISPLAY_NAME, filename)
                            put(MediaStore.MediaColumns.MIME_TYPE, mime)
                            put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/ZevorixDiagrams")
                        }
                        val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
                        if (uri != null) {
                            resolver.openOutputStream(uri)?.use { it.write(bytes) }
                            toast("تم الحفظ في Downloads/ZevorixDiagrams")
                        } else {
                            toast("فشل الحفظ")
                        }
                    } else {
                        val dir = File(activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), "ZevorixDiagrams")
                        dir.mkdirs()
                        val file = File(dir, filename)
                        file.writeBytes(bytes)
                        toast("تم الحفظ في ${file.absolutePath}")
                    }
                } catch (e: Exception) {
                    toast("فشل الحفظ: ${e.message}")
                }
            }
        }
    }
}
'''

with open(PKG_DIR + "/ArchitectureActivity.kt", "w", encoding="utf-8") as f:
    f.write(activity_content)

# ---------------------------------------------------------------------------
# 3) Manifest
# ---------------------------------------------------------------------------
register_activity("ArchitectureActivity")

# 4) Menu item: still handled by menu_items_patch.py (MainScreen.kt is not touched here).
print(">> Architecture Lab Patch v2 applied (activity + html + manifest). Menu item: menu_items_patch.py")

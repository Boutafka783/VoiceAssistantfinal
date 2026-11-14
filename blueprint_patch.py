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

print(">> Applying Flight Lab v3 patch (select parts -> assemble (manual/auto) -> flight test)...")

# ---------------------------------------------------------------------------
# 1) flight_sim.html  (v2)
#    - 11 component categories (frame, wing, tail, battery, motor, prop, ESC,
#      servos, flight controller, radio link, camera)
#    - live engineering checks (TWR, wing loading, stall speed, ESC/battery limits...)
#    - bill of materials with weight + cost
#    - offline build guide generated from the chosen parts (+ AI guide on top)
#    - real throttle control, lift/drag/stall physics, quadcopter mode, crash + failsafe
# ---------------------------------------------------------------------------
html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>مختبر هندسة الطيران</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
:root{--bg:#0a0f18;--panel:rgba(13,21,34,.95);--border:rgba(53,208,255,.4);--text:#e8edf5;--accent:#35d0ff;--orange:#ff9f1c;--warn:#ff5555;--good:#00ff88}
*{box-sizing:border-box}
body,html{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;overflow:hidden;-webkit-user-select:none;user-select:none}
#canvas-container{position:absolute;inset:0;z-index:1}
.panel{background:var(--panel);border:1px solid var(--border);border-radius:8px}
#hud{position:absolute;top:84px;right:8px;z-index:2;padding:6px 10px;font-family:monospace;font-size:.78rem;text-align:right;pointer-events:none;line-height:1.35;max-width:46vw}
#hud .val{color:var(--accent);font-weight:bold}.warn{color:var(--warn);font-weight:bold}.good{color:var(--good);font-weight:bold}
#hud hr{border:0;border-top:1px solid #333;margin:4px 0}
#toolbar{position:absolute;top:6px;left:6px;right:6px;z-index:3;display:flex;gap:6px;justify-content:center}
.tbtn{padding:7px 10px;background:var(--panel);border:1px solid var(--border);color:var(--text);border-radius:8px;font-size:.8rem;cursor:pointer}
#builder-panel{position:fixed;top:88px;left:0;z-index:6;padding:10px;display:flex;flex-direction:column;gap:6px;width:min(250px,78vw);max-height:calc(100% - 190px);overflow-y:auto;border-radius:0 12px 12px 0;border-left:0;transform:translateX(-104%);transition:transform .25s ease;visibility:hidden}
body.drawer-open #builder-panel{transform:translateX(0);visibility:visible}
#side-btn{position:fixed;top:94px;left:0;z-index:7;width:42px;height:58px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;background:var(--panel);border:1px solid var(--border);border-left:0;border-radius:0 12px 12px 0;color:var(--text);font-size:1.25rem;cursor:pointer;transition:left .25s ease;touch-action:manipulation}
#side-btn small{font-size:.6rem;color:var(--accent)}
body.drawer-open #side-btn{left:min(250px,78vw)}
.row{display:flex;flex-direction:column;gap:2px}
.row label{font-size:.72rem;color:#9fb0c5}
.row select{padding:4px;border-radius:4px;border:1px solid var(--border);background:#060a12;color:#fff;font-size:.75rem}
.row select:disabled{opacity:.35}
#part-info{font-size:.72rem;line-height:1.4;color:#cfe;background:#0c1a28;border-radius:6px;padding:6px;display:none}
#checks{position:absolute;bottom:92px;right:8px;z-index:2;max-width:52vw;font-size:.7rem;line-height:1.35;padding:6px 8px;max-height:30vh;overflow-y:auto}
#checks div{margin-bottom:3px}
#ai-panel{position:absolute;bottom:92px;left:8px;z-index:2;width:210px;display:flex;flex-direction:column;gap:5px}
#ai-input{width:100%;padding:7px;border-radius:6px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:.8rem;outline:none}
#ai-btn{padding:7px;background:var(--accent);color:#000;border:0;border-radius:6px;font-weight:bold;cursor:pointer;font-size:.82rem}
#ai-result{font-size:.72rem;color:var(--orange);background:var(--panel);padding:5px;border-radius:6px;display:none;border:1px solid var(--orange)}
#msg{position:absolute;top:38%;left:0;right:0;text-align:center;z-index:5;font-size:1.3rem;font-weight:bold;color:var(--warn);text-shadow:0 0 8px #000;pointer-events:none;display:none}
.modal{position:absolute;inset:0;background:rgba(0,0,0,.82);z-index:100;display:none;justify-content:center;align-items:center;padding:14px;backdrop-filter:blur(4px)}
.modal-box{background:var(--panel);border:2px solid var(--accent);border-radius:12px;padding:16px;max-width:560px;width:100%;max-height:86vh;overflow-y:auto}
.modal-box h2{margin:0 0 8px;color:var(--accent);text-align:center;border-bottom:1px solid #333;padding-bottom:8px;font-size:1.1rem}
.modal-box h3{color:var(--orange);font-size:.95rem;margin:14px 0 6px}
.modal-box p,.modal-box li{line-height:1.7;font-size:.88rem;color:#d5deea}
.modal-box ol,.modal-box ul{padding-right:20px;margin:0}
.modal-box li{margin-bottom:6px;border-bottom:1px dashed #2a3442;padding-bottom:6px}
table{width:100%;border-collapse:collapse;font-size:.8rem}
td,th{padding:4px 6px;border-bottom:1px solid #2a3442;text-align:right}
th{color:var(--accent)}
.closebtn{width:100%;padding:11px;background:var(--accent);color:#000;border:0;border-radius:8px;font-weight:bold;font-size:1rem;margin-top:14px;cursor:pointer}
#controls{position:absolute;bottom:12px;left:12px;right:12px;z-index:2;display:flex;justify-content:space-between;align-items:flex-end;pointer-events:none}
.cg{display:flex;gap:8px;pointer-events:auto;align-items:flex-end}
.bc{width:50px;height:50px;border-radius:50%;border:2px solid var(--border);background:var(--panel);color:var(--text);font-size:1.15rem;display:flex;justify-content:center;align-items:center;cursor:pointer;touch-action:none}
#thr-wrap{display:flex;flex-direction:column;align-items:center;gap:4px}
#throttle-bar{width:26px;height:90px;background:var(--panel);border:2px solid var(--border);border-radius:8px;position:relative;overflow:hidden;touch-action:none}
#throttle-fill{position:absolute;bottom:0;left:0;right:0;background:var(--accent);height:0}
#throttle-text{font-family:monospace;font-size:.85rem}

#canvas-container{touch-action:none}
#toolbar{flex-direction:column;align-items:center;gap:4px}
#stepper,#tools{display:flex;gap:6px;justify-content:center}
#tools{flex-wrap:wrap}
#tools .tbtn{padding:4px 9px;font-size:.72rem}
.hbtn{display:none}
body.human.stage-fly .hbtn{display:block}
.hbtn.on{background:var(--warn);color:#000;font-weight:bold}
body.human.stage-fly #checks{display:none}
body.human.stage-fly #hud{background:rgba(13,21,34,.55);font-size:.68rem}
.st.on{background:var(--accent);color:#000;font-weight:bold}
#banner{display:none;position:absolute;top:84px;left:8px;right:8px;z-index:4;padding:8px 10px;font-size:.8rem;line-height:1.5;border-color:var(--orange);pointer-events:none}
#tray{display:none;position:absolute;bottom:10px;left:8px;right:8px;z-index:4;padding:8px}
body.stage-build #banner,body.stage-build #tray{display:block}
body.stage-build #hud,body.stage-build #checks,body.stage-build #ai-panel,body.stage-build #side-btn,body.stage-build #controls,body.stage-select #controls,body.stage-fly #ai-panel,body.stage-fly #side-btn{display:none}
#chips{display:flex;gap:6px;overflow-x:auto;padding-bottom:6px}
.chip{flex:0 0 auto;min-width:78px;padding:5px 8px;border:1px solid var(--border);border-radius:8px;background:#0c1a28;text-align:center;font-size:.72rem;cursor:pointer}
.chip small{color:#9fb0c5}
.chip.sel{border-color:var(--good);background:#0b3a2a}.chip.done{opacity:.35}.chip.hint{border-color:var(--orange);background:#3a2a0b}
#tray-actions{display:flex;gap:8px;align-items:center}
.abtn{padding:7px 10px;border:0;border-radius:6px;background:var(--accent);color:#000;font-weight:bold;font-size:.8rem;cursor:pointer}
#prog{margin-right:auto;font-family:monospace;color:var(--accent)}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="toolbar">
  <div id="stepper">
    <div class="tbtn st" id="st-select">① اختيار القطع</div>
    <div class="tbtn st" id="st-build">② التركيب</div>
    <div class="tbtn st" id="st-fly">③ الاختبار</div>
  </div>
  <div id="tools">
    <div class="tbtn" id="t-guide">📘 الدليل</div>
    <div class="tbtn" id="t-bom">📋 القائمة</div>
    <div class="tbtn" id="t-reset">↺ إعادة</div>
    <div class="tbtn hbtn" id="t-launch">🏃 ركض</div>
    <div class="tbtn hbtn" id="t-chute">🪂 مظلة</div>
    <div class="tbtn hbtn" id="t-fail">⛔ تعطل المحرك</div>
    <div class="tbtn hbtn" id="t-cam">🎥 كاميرا</div>
  </div>
</div>
<div id="banner" class="panel"></div>
<div id="tray" class="panel">
  <div id="chips"></div>
  <div id="tray-actions"><button class="abtn" id="auto-btn">🤖 تركيب آلي</button><button class="abtn" id="build-reset" style="background:#9fb0c5">↺ فك الكل</button><span id="prog"></span></div>
</div>

<div id="side-btn" title="القطع"><span id="side-ico">🧩</span><small>القطع</small></div>

<div id="hud" class="panel">
  السرعة: <span class="val" id="hud-speed">0</span> km/h<br>
  الارتفاع: <span class="val" id="hud-alt">0</span> m<br>
  البعد: <span class="val" id="hud-dist">0</span> m<br>
  <hr>
  الوزن: <span class="val" id="hud-weight">0</span> <span id="u-w">g</span><br>
  الدفع: <span class="val" id="hud-thrust">0</span> <span id="u-t">g</span><br>
  TWR: <span id="hud-twr">0</span><br>
  <span id="row-wl">تحميل الجناح: <span class="val" id="hud-wl">0</span> g/dm²<br>
  سرعة الانهيار: <span class="val" id="hud-stall">0</span> km/h<br></span>
  <span id="row-h" style="display:none">باع الجناح: <span class="val" id="hud-span">0</span> m<br>
  انزلاق L/D: <span class="val" id="hud-ld">0</span><br>
  قدرة الذروة: <span class="val" id="hud-pw">0</span> kW<br>
  معدل الصعود: <span class="val" id="hud-roc">0</span> m/s<br></span>
  البطارية: <span class="val" id="hud-bat">100</span>%<br>
  زمن الطيران: <span class="val" id="hud-time">0</span> د<br>
  المدى: <span class="val" id="hud-range">0</span> كم<br>
  التكلفة: <span class="val" id="hud-cost">0</span>$
</div>

<div id="builder-panel" class="panel"></div>
<div id="checks" class="panel"></div>

<div id="ai-panel">
  <input type="text" id="ai-input" placeholder="مثال: طائرة للمبتدئين تطير 15 دقيقة">
  <button id="ai-btn">✨ مهندس الطيران AI</button>
  <div id="ai-result"></div>
</div>

<div id="msg"></div>

<div id="guide-modal" class="modal"><div class="modal-box">
  <h2>📘 دليل تصنيع الطائرة</h2>
  <div id="guide-body"></div>
  <button class="closebtn" onclick="document.getElementById('guide-modal').style.display='none'">فهمت!</button>
</div></div>

<div id="bom-modal" class="modal"><div class="modal-box">
  <h2>📋 قائمة القطع والتكلفة</h2>
  <div id="bom-body"></div>
  <button class="closebtn" onclick="document.getElementById('bom-modal').style.display='none'">إغلاق</button>
</div></div>

<div id="controls">
  <div class="cg"><div class="bc" id="btn-pitch-down">⬇️</div><div class="bc" id="btn-pitch-up">⬆️</div></div>
  <div class="cg" id="thr-wrap">
    <div class="bc" id="btn-thr-up" style="width:40px;height:40px">＋</div>
    <div id="throttle-bar"><div id="throttle-fill"></div></div>
    <div id="throttle-text">0%</div>
    <div class="bc" id="btn-thr-down" style="width:40px;height:40px">－</div>
  </div>
  <div class="cg"><div class="bc" id="btn-roll-left">⬅️</div><div class="bc" id="btn-roll-right">➡️</div></div>
</div>

<script>
const $ = id => document.getElementById(id);

/* ======================= كتالوج القطع ======================= */
// w = الوزن بالغرام، c = السعر التقريبي بالدولار
const PARTS = {
  frame: {
    plane: {n:'طائرة تدريب', w:350, c:35, type:'plane', cd:.035, d:'هيكل من الفوم أو البلسا. أسهل نوع للمبتدئين: مستقرة وتسامح الأخطاء.'},
    wing:  {n:'جناح طائر (Flying Wing)', w:250, c:30, type:'wing', cd:.03, d:'بدون ذيل؛ التحكم بالـ Elevons (سيرفوهان على الجناح). سريعة وقليلة السحب لكن تحتاج متحكم طيران أو خبرة.'},
    cargo: {n:'طائرة شحن ثقيلة', w:900, c:90, type:'plane', cd:.05, d:'هيكل كبير يحمل أوزاناً أكثر. تحتاج محركاً قوياً وجناحاً كبيراً.'},
    quad:  {n:'كوادكوبتر (درون)', w:300, c:40, type:'quad', cd:.08, d:'4 محركات ومراوح، بلا جناح ولا ذيل. تحلق وتحوم في مكانها لكنها تحتاج متحكم طيران إلزامياً في الواقع.'},
    human: {n:'إنسان بجناح على الظهر (Wingpack)', w:3500, c:180, type:'human', cd:.03, d:'طيار بشري يطير مستلقياً: جناح قابل للطي داخل حقيبة الظهر مع محرك ومروحة خلفية وبطارية داخل الحقيبة. اختر وزنك من القائمة وسيُحسب باع الجناح ومساحته من وزنك الكلي. للمحاكاة والتعلم فقط.'}
  },
  wing: {
    trainer:{n:'جناح تدريب مستوٍ', w:120, c:20, S:.28, clmax:1.4, k:.06, d:'مقطع Clark-Y مسطح من الأسفل: رفع عالي وسرعة انهيار منخفضة. مثالي للتعلم.'},
    glider: {n:'جناح شراعي طويل', w:160, c:30, S:.30, clmax:1.3, k:.03, d:'نسبة باع/وتر عالية = سحب مستحث قليل = طيران طويل بطاقة أقل، لكنه هش.'},
    sport:  {n:'جناح رياضي صغير', w:110, c:22, S:.18, clmax:1.1, k:.07, d:'مساحة صغيرة = سرعة عالية لكن سرعة الانهيار عالية والهبوط أصعب.'},
    big:    {n:'جناح كبير للشحن', w:350, c:55, S:.60, clmax:1.4, k:.05, d:'مساحة كبيرة تحمل وزناً أكبر. يحتاج عارضة كربون (spar) لتقويته.'}
  },
  tail: {
    conv: {n:'ذيل تقليدي', w:40, c:8, stab:1, d:'مثبت أفقي + زعنفة عمودية: أفضل ثبات في الاتجاه والميلان.'},
    vtail:{n:'ذيل V', w:35, c:10, stab:.85, d:'سطحان مائلان يعملان كمصعد ودفة معاً: أخف وسحب أقل لكن خلط الإشارات (mixing) مطلوب.'},
    none: {n:'بدون ذيل', w:0, c:0, stab:0, d:'مناسب للجناح الطائر فقط. مع هيكل عادي ستكون الطائرة غير مستقرة.'}
  },
  battery: {
    '1s':    {n:'1S 500mAh LiPo',        w:14,   c:5,   mah:500,   cmax:20, s:1, chem:'LiPo',   d:'3.7V: للطائرات والدرونات الصغيرة جداً (Micro) مع المحركات الصغيرة.'},
    '2s':    {n:'2S 1000mAh LiPo',       w:70,   c:10,  mah:1000,  cmax:20, s:2, chem:'LiPo',   d:'7.4V: خفيفة للطائرات الصغيرة.'},
    '2s22':  {n:'2S 2200mAh LiPo',       w:120,  c:14,  mah:2200,  cmax:25, s:2, chem:'LiPo',   d:'7.4V: سعة أكبر لزمن طيران أطول مع محركات صغيرة.'},
    '3s':    {n:'3S 1500mAh LiPo',       w:130,  c:18,  mah:1500,  cmax:25, s:3, chem:'LiPo',   d:'11.1V: التوازن الأفضل للمبتدئين.'},
    '3s22':  {n:'3S 2200mAh LiPo',       w:185,  c:24,  mah:2200,  cmax:30, s:3, chem:'LiPo',   d:'11.1V: اختيار شائع للطائرات المتوسطة.'},
    '3s30':  {n:'3S 3000mAh LiPo',       w:250,  c:32,  mah:3000,  cmax:25, s:3, chem:'LiPo',   d:'11.1V: سعة كبيرة لزمن طيران جيد.'},
    '3sli':  {n:'3S 3000mAh Li-ion',     w:150,  c:22,  mah:3000,  cmax:3,  s:3, chem:'Li-ion', vmin:3.0, d:'خلايا 18650 خفيفة وطويلة المدى، لكنها لا تعطي تياراً عالياً (حد ~9A). للطائرات الشراعية والمستكشفة.'},
    '4s':    {n:'4S 2200mAh LiPo',       w:250,  c:32,  mah:2200,  cmax:30, s:4, chem:'LiPo',   d:'14.8V: قدرة أعلى وزمن أطول، وزنها أكبر.'},
    '4s15r': {n:'4S 1500mAh سباق (75C)', w:175,  c:22,  mah:1500,  cmax:75, s:4, chem:'LiPo',   d:'تفريغ عالٍ جداً للدرونات السريعة؛ سعتها صغيرة فزمن الطيران قصير.'},
    '4s33':  {n:'4S 3300mAh LiPo',       w:340,  c:42,  mah:3300,  cmax:30, s:4, chem:'LiPo',   d:'14.8V: للطائرات الأثقل أو الدرونات التي تحمل كاميرا.'},
    '4s50':  {n:'4S 5000mAh LiPo',       w:520,  c:65,  mah:5000,  cmax:25, s:4, chem:'LiPo',   d:'سعة كبيرة للمدى الطويل مع وزن كبير.'},
    '4sli':  {n:'4S 6000mAh Li-ion',     w:400,  c:50,  mah:6000,  cmax:5,  s:4, chem:'Li-ion', vmin:3.0, d:'أطول زمن طيران لكل غرام، بتيار محدود (~30A). مثالية للطيران الطويل بطاقة منخفضة.'},
    '6s':    {n:'6S 5000mAh LiPo',       w:650,  c:80,  mah:5000,  cmax:25, s:6, chem:'LiPo',   d:'22.2V: للطائرات الثقيلة والمحركات الكبيرة.'},
    '6s80':  {n:'6S 8000mAh LiPo',       w:1050, c:130, mah:8000,  cmax:20, s:6, chem:'LiPo',   d:'للشحن الثقيل والرحلات الطويلة؛ ثقيلة جداً على الهياكل الصغيرة.'},
    '3s13r': {n:'3S 1300mAh سباق (75C)', w:115,  c:16,  mah:1300,  cmax:75, s:3, chem:'LiPo',   d:'11.1V بتفريغ عالٍ (~97A): خفيفة للدرونات الصغيرة مع محركات 3S.'},
    '4s13r': {n:'4S 1300mAh سباق (100C)', w:160, c:24,  mah:1300,  cmax:100, s:4, chem:'LiPo',  d:'14.8V بتفريغ عالٍ جداً (~130A): للكوادكوبتر الخفيف السريع. زمن الطيران قصير.'},
    '4s22r': {n:'4S 2200mAh LiPo (50C)', w:250,  c:34,  mah:2200,  cmax:50, s:4, chem:'LiPo',   d:'14.8V: توازن جيد بين التيار (~110A) وزمن الطيران للكوادكوبتر.'},
    '4s40':  {n:'4S 4000mAh LiPo (40C)', w:420,  c:50,  mah:4000,  cmax:40, s:4, chem:'LiPo',   d:'14.8V: زمن طيران أطول للدرونات ذات الكاميرا، تتحمل ~160A.'},
    '6s13r': {n:'6S 1300mAh سباق (100C)', w:230, c:36,  mah:1300,  cmax:100, s:6, chem:'LiPo',  d:'22.2V بتفريغ عالٍ: للدرونات السريعة بمحركات 6S.'},
    '6s30':  {n:'6S 3000mAh LiPo (50C)', w:450,  c:70,  mah:3000,  cmax:50, s:6, chem:'LiPo',   d:'22.2V: للكوادكوبتر القوي والثقيل، تتحمل ~150A.'},
    '6s10k': {n:'6S 10000mAh LiPo (25C)', w:1350, c:160, mah:10000, cmax:25, s:6, chem:'LiPo',  d:'للكوادكوبتر الثقيل الحامل للأوزان وللطيران الطويل؛ ثقيلة جداً (~250A).'}
  },
  motor: {
    micro:  {n:'محرك مايكرو (100g)',    w:12,  c:7,   t:100,  a:6,  cells:[1,2], d:'Brushless صغير جداً (1103-1306). للطائرات والدرونات الصغيرة حتى ~150g.'},
    small:  {n:'محرك صغير (200g)',      w:30,  c:10,  t:200,  a:10, cells:[2,3], d:'Brushless outrunner صغير. مناسب لطائرات حتى ~400g.'},
    sport:  {n:'محرك رياضي (450g)',     w:38,  c:14,  t:450,  a:18, cells:[3,4], d:'قدرة جيدة بوزن خفيف. للطائرات الرياضية 500-900g والدرونات الصغيرة.'},
    medium: {n:'محرك متوسط (800g)',     w:60,  c:22,  t:800,  a:25, cells:[3,4], d:'الخيار العام: يرفع طائرات ~1.2-1.6kg.'},
    high:   {n:'محرك قوي (1200g)',      w:85,  c:30,  t:1200, a:35, cells:[3,5], d:'يرفع طائرات ~2kg أو درونات متوسطة بهامش جيد.'},
    large:  {n:'محرك كبير (2000g)',     w:120, c:45,  t:2000, a:50, cells:[4,6], d:'قدرة كبيرة للشحن أو الكوادكوبتر الثقيل. يستهلك تياراً عالياً.'},
    xl:     {n:'محرك ضخم (3200g)',      w:190, c:70,  t:3200, a:70, cells:[5,6], d:'للطائرات الثقيلة جداً. يحتاج بطارية 5-6S وESC قوياً.'},
    xxl:    {n:'محرك صناعي (5000g)',    w:320, c:110, t:5000, a:95, cells:[6,6], d:'أقوى المحركات المتاحة: للشحن الثقيل جداً. يتطلب بطارية 6S كبيرة وESC بحد 100A.'},
    q1806:  {n:'محرك درون 1806 (600g)',  w:22,  c:11,  t:600,  a:14, cells:[3,4], d:'محرك خفيف للدرونات الصغيرة (3-4 إنش). مثالي مع بطارية 3S-4S وESC 20A.'},
    q2205:  {n:'محرك درون 2205 (900g)',  w:28,  c:14,  t:900,  a:22, cells:[3,4], d:'الخيار الأمثل لكوادكوبتر 5 إنش: دفع جيد وتيار معتدل. ESC 30A كافٍ.'},
    q2306:  {n:'محرك درون 2306 (1200g)', w:34,  c:18,  t:1200, a:28, cells:[4,6], d:'قوة أكبر للدرون السريع أو الحامل لكاميرا HD. يحتاج ESC 40A.'},
    q2810:  {n:'محرك درون 2810 (1800g)', w:55,  c:28,  t:1800, a:30, cells:[4,6], d:'للدرونات القوية بحمولة إضافية. يحتاج ESC 40A وبطارية 6S عالية التفريغ (مثل 6S 3000mAh).'},
    q4108:  {n:'محرك رفع ثقيل 4108 (3500g)', w:140, c:60, t:3500, a:45, cells:[4,6], d:'للدرونات الكبيرة الحاملة للأوزان. يحتاج ESC 60A وبطارية 6S كبيرة (مثل 6S 10000mAh) مع مروحة متوسطة.'}
  },
  prop: {
    small: {n:'مروحة صغيرة',      w:10, c:3,  tm:.8,  am:.7,  d:'تيار أقل وسرعة أعلى، دفع ثابت أقل.'},
    medium:{n:'مروحة متوسطة',     w:15, c:4,  tm:1.0, am:1.0, d:'توازن بين الدفع والتيار.'},
    large: {n:'مروحة كبيرة',      w:25, c:6,  tm:1.2, am:1.3, d:'دفع أعلى عند الإقلاع، تستهلك تياراً أكبر.'},
    xl:    {n:'مروحة ضخمة (كفاءة)', w:45, c:12, tm:1.45, am:1.7, d:'أعلى دفع عند الإقلاع للشحن الثقيل، لكنها تستهلك أعلى تيار.'},
    q5:    {n:'مروحة درون 5 إنش',  w:5,  c:4,  tm:1.1, am:1.1, d:'خفيفة جداً ومناسبة للكوادكوبتر: دفع جيد وتيار معتدل.'},
    q7:    {n:'مروحة درون 7 إنش',  w:9,  c:7,  tm:1.3, am:1.4, d:'دفع أكبر وكفاءة أعلى لزمن طيران أطول، تحتاج محركاً أقوى.'},
    q10:   {n:'مروحة درون 10 إنش', w:18, c:12, tm:1.6, am:2.0, d:'للرفع الثقيل: أعلى دفع للكوادكوبتر لكن بتيار كبير.'}
  },
  esc: {
    e6:  {n:'ESC 6A',   w:4,  c:5,  a:6,   d:'للمحركات المايكرو فقط.'},
    e10: {n:'ESC 12A',  w:8,  c:8,  a:12,  d:'متحكم السرعة: يحول البطارية إلى 3 أطوار للمحرك. اختره دائماً أكبر من تيار المحرك بـ 20% على الأقل.'},
    e20: {n:'ESC 20A',  w:15, c:11, a:20,  d:'للمحركات الصغيرة والرياضية.'},
    e30: {n:'ESC 30A',  w:25, c:15, a:30,  d:'مناسب للمحرك المتوسط.'},
    e40: {n:'ESC 40A',  w:32, c:19, a:40,  d:'للمحركات القوية (1200g).'},
    e60: {n:'ESC 60A',  w:45, c:28, a:60,  d:'للمحركات الكبيرة. يفضل تبريده بتيار الهواء.'},
    e80: {n:'ESC 80A',  w:70, c:38, a:80,  d:'للمحركات الضخمة. يحتاج تبريداً جيداً.'},
    e100:{n:'ESC 100A', w:95, c:55, a:100, d:'للمحركات الضخمة جداً. يحتاج تبريداً قوياً وأسلاكاً سميكة.'},
    e120:{n:'ESC 120A', w:120, c:75, a:120, d:'للمحرك الصناعي (5000g). يحتاج تبريداً قوياً وأسلاكاً سميكة.'},
    e35: {n:'ESC 35A خفيف',  w:8,  c:12, a:35, d:'ESC خفيف بنمط BLHeli للدرونات؛ يكفي لمحركات 2205/2306 الخفيفة.'},
    e50: {n:'ESC 50A خفيف',  w:14, c:20, a:50, d:'ESC خفيف للدرونات القوية (2810)؛ أخف بكثير من ESC 60A العادي.'}
  },
  servo: {
    s9: {n:'سيرفو 9g بلاستيك', w:9,  c:4,  d:'يحرك الأسطح المتحركة. يكفي للطائرات الخفيفة.'},
    s17:{n:'سيرفو 17g معدني',  w:17, c:10, d:'تروس معدنية: أقوى وأدق للطائرات الأثقل والأسرع.'}
  },
  fc: {
    none:{n:'بدون متحكم طيران', w:0,  c:0,  stabil:0,  d:'تحكم مباشر من اليد فقط. للخبراء.'},
    gyro:{n:'متحكم طيران + جيروسكوب', w:10, c:25, stabil:.6, d:'يثبّت الطائرة تلقائياً ويخفف الاهتزاز. يوصى به كثيراً للمبتدئين.'},
    gps: {n:'متحكم طيران + GPS',   w:25, c:60, stabil:.75, gps:1, d:'يضيف العودة التلقائية للمنزل (RTH) والتحويم في المكان.'}
  },
  rc: {
    r24:{n:'راديو 2.4GHz', w:15, c:30, km:1,   d:'جهاز تحكم ومستقبل قياسي. المدى العملي ~1كم.'},
    r58:{n:'راديو 5.8GHz / طويل المدى', w:20, c:60, km:3, d:'مدى أطول مع هوائيات أفضل.'},
    r4g:{n:'4G / WiFi', w:40, c:90, km:999, d:'مدى مفتوح، لكن يعتمد على تغطية الشبكة وله تأخير زمني.'}
  },
  cam: {
    none:{n:'بدون كاميرا', w:0,  c:0,  d:''},
    fpv: {n:'كاميرا FPV', w:25, c:25, d:'بث مباشر لرؤية الطيار.'},
    hd:  {n:'كاميرا HD', w:80, c:90, d:'تصوير عالي الجودة، وزن إضافي يؤثر على التوازن.'}
  },
  chute: {
    none:{n:'—', w:0, c:0, d:''}
  }
};

/* ===== كتالوج الإنسان بجناح الحقيبة (الأوزان بالغرام، التكلفة بالدولار) =====
   wing: b = الباع (م)، S = المساحة (م²)، clmax، fold = طول الجناح مطوياً داخل الحقيبة (م)
   motor: P = القدرة الكهربائية القصوى (kW)، cells = عدد خلايا البطارية المسموح
   prop: D = القطر (م)  |  esc: a = التيار (A)  |  battery: s خلايا، mah، cmax = معدل التفريغ C
   chute: open = زمن الانفتاح (ث)، minAlt = أقل ارتفاع آمن للفتح (م) */
const PARTS_H = {
  wing: {
    auto:{n:'جناح تلقائي حسب وزنك', auto:1, clmax:1.3, w:0, c:0, d:'يحسب البرنامج مساحة الجناح وباعه من وزنك الكلي (جسمك + المعدات) لسرعة انهيار مستهدفة 12 م/ث (~43 كم/س): S = 2·M·g / (ρ·V²·CLmax)، والباع b = √(AR·S) مع AR = 6. يتغيّر الحجم تلقائياً عند تغيير وزنك أو أي قطعة.'},
    flap:{n:'جناح مرفرف حسب وزنك (Ornithopter)', auto:1, flap:1, clmax:1.2, w:0, c:0, d:'نفس حساب الجناح التلقائي، لكن بمفصل عند الكتف وذراعي رفرفة تحرّكهما علبة تروس من المحرك. الرفع الأساسي يأتي من تقدّم الجسم في الهواء، والرفرفة تضيف حركة ودفعاً بسيطاً وتستهلك ~8% طاقة زائدة. الميكانيزم أثقل (≈ +35% من وزن الجناح +1.5 كغ) ومعقّد، وكفاءته أقل من الجناح الثابت.'},
    hw3: {n:'جناح قصير 3.0 م (سريع)',  b:3.0, S:2.7,  clmax:1.0,  fold:.85, w:3200,  c:520,  d:'مساحة صغيرة: سرعة انهيار عالية جداً (أكثر من 20 م/ث لشخص عادي). للمحترفين مع إقلاع من ارتفاع.'},
    hw4: {n:'جناح 4.0 م',               b:4.0, S:4.4,  clmax:1.1,  fold:.95, w:4800,  c:780,  d:'مناسب للأوزان الخفيفة (50-60 كغ) مع سرعة طيران عالية نسبياً.'},
    hw5: {n:'جناح 5.0 م',               b:5.0, S:6.0,  clmax:1.2,  fold:1.0, w:6200,  c:1050, d:'جناح متوسط للأوزان 55-70 كغ، سرعة انهيار ~15 م/ث.'},
    hw6: {n:'جناح 6.0 م',               b:6.0, S:7.8,  clmax:1.25, fold:1.05, w:7800, c:1400, d:'جناح متوازن للأوزان 65-85 كغ، يحتاج عارضة كربون مزدوجة.'},
    hw8: {n:'جناح كبير 8.0 م (انزلاق)', b:8.0, S:12.0, clmax:1.3,  fold:1.2, w:11600, c:2100, d:'سرعة انهيار منخفضة وانزلاق جيد، للأوزان الكبيرة (90-120 كغ) لكن الحقيبة طويلة وثقيلة.'}
  },
  motor: {
    hm6:  {n:'محرك 6 kW',  w:1900, c:320,  P:6,  cells:[8,12],  d:'محرك صغير لأشخاص خفاف مع جناح كبير. دفع محدود.'},
    hm12: {n:'محرك 12 kW', w:3300, c:650,  P:12, cells:[12,14], d:'الخيار العام: دفع ~50 كغ مع مروحة 1.2 م. يعمل مع بطارية 12S-14S.'},
    hm20: {n:'محرك 20 kW', w:5200, c:1100, P:20, cells:[12,16], d:'قدرة أعلى للأوزان الكبيرة أو الصعود السريع. يحتاج ESC 500A مع 12S أو بطارية 14S.'},
    hm30: {n:'محرك 30 kW', w:7800, c:1900, P:30, cells:[14,18], d:'أقوى محرك: دفع كبير مع استهلاك عالٍ. يحتاج بطارية 18S وESC 500A.'}
  },
  prop: {
    hp08:{n:'مروحة 0.8 م', D:.8,  w:600,  c:140, d:'قرص صغير: دفع أقل لنفس القدرة وضجيج أعلى.'},
    hp10:{n:'مروحة 1.0 م', D:1.0, w:900,  c:220, d:'توازن بين الحجم والكفاءة.'},
    hp12:{n:'مروحة 1.2 م', D:1.2, w:1400, c:360, d:'كفاءة جيدة: دفع أكبر لنفس القدرة (T ∝ (P·√A)^(2/3)).'},
    hp15:{n:'مروحة 1.5 م', D:1.5, w:2200, c:620, d:'أعلى كفاءة وأقل استهلاكاً، لكنها كبيرة وتحتاج عمود تثبيت أطول.'}
  },
  esc: {
    he150:{n:'ESC 150A', w:330,  c:280,  a:150, d:'للمحركات الصغيرة (6 kW).'},
    he200:{n:'ESC 200A', w:450,  c:380,  a:200, d:'يكفي محرك 6-9 kW.'},
    he300:{n:'ESC 300A', w:700,  c:600,  a:300, d:'للمحرك 12 kW مع 14S.'},
    he400:{n:'ESC 400A', w:900,  c:800,  a:400, d:'للمحرك 12 kW مع 12S (تيار ~280A).'},
    he500:{n:'ESC 500A', w:1200, c:1100, a:500, d:'للمحركات 20-30 kW. يحتاج تبريداً قوياً.'}
  },
  battery: {
    hb1:{n:'12S 10Ah LiPo (25C)',  w:2500, c:380,  s:12, mah:10000, cmax:25, chem:'LiPo',   d:'444Wh: خفيفة، زمن طيران قصير.'},
    hb2:{n:'12S 16Ah LiPo (25C)',  w:4000, c:600,  s:12, mah:16000, cmax:25, chem:'LiPo',   d:'710Wh: الخيار العام مع محرك 12 kW.'},
    hb3:{n:'14S 16Ah LiPo (25C)',  w:4700, c:700,  s:14, mah:16000, cmax:25, chem:'LiPo',   d:'829Wh بجهد أعلى = تيار أقل لنفس القدرة.'},
    hb4:{n:'14S 22Ah LiPo (20C)',  w:6400, c:980,  s:14, mah:22000, cmax:20, chem:'LiPo',   d:'1140Wh: زمن طيران أطول بوزن أكبر.'},
    hb5:{n:'18S 16Ah LiPo (25C)',  w:6000, c:950,  s:18, mah:16000, cmax:25, chem:'LiPo',   d:'1066Wh بجهد عالٍ للمحركات 30 kW.'},
    hb6:{n:'12S 30Ah Li-ion (5C)', w:5200, c:900,  s:12, mah:30000, cmax:5,  chem:'Li-ion', vmin:3.0, d:'1332Wh بوزن منخفض، لكن التيار محدود (~150A): للمحركات الصغيرة أو الطيران الطويل.'},
    hb7:{n:'18S 22Ah LiPo (20C)',  w:8000, c:1300, s:18, mah:22000, cmax:20, chem:'LiPo',   d:'1465Wh: أكبر طاقة، ثقيلة جداً.'}
  },
  chute: {
    none:     {n:'بدون مظلة (خطر!)',         w:0,    c:0,    open:0,  minAlt:0,   d:'⚠️ لا وسيلة نجاة عند تعطل المحرك أو الجناح. غير مقبول للتصميم الآمن.'},
    basic:    {n:'مظلة احتياطية يدوية',      w:2500, c:450,  open:2.2, minAlt:100, d:'مظلة طوارئ مطوية في الحقيبة، تُفتح بمقبض. تحتاج ~100 م ارتفاع على الأقل لتنفتح بالكامل.'},
    ballistic:{n:'مظلة صاروخية (Ballistic)', w:3800, c:1100, open:.8,  minAlt:50,  d:'تُطلق بشحنة صغيرة فتنفتح خلال أقل من ثانية: ارتفاع آمن أقل (~50 م).'}
  }
};
const SLOTS = [['frame','الهيكل'],['wing','الجناح'],['tail','الذيل'],['battery','البطارية'],['motor','المحرك'],
  ['prop','المروحة'],['esc','متحكم السرعة ESC'],['servo','السيرفو'],['fc','متحكم الطيران'],['rc','التحكم عن بعد'],['cam','الكاميرا'],['chute','المظلة الاحتياطية']];

/* ======================= واجهة البناء ======================= */
const bp = $('builder-panel');
const STD_DEFAULT = {battery:'3s', motor:'medium', esc:'e30', prop:'small', wing:'trainer', fc:'gyro'};
const HUMAN_DEFAULT = {wing:'auto', motor:'hm12', prop:'hp12', esc:'he400', battery:'hb2', servo:'s17', fc:'gyro', rc:'r24', cam:'none', chute:'basic'};
let curMode = 'std';
const saved = {std:{}, human:{}};
// في وضع الإنسان تُستبدل كتالوجات الجناح والمحرك والمروحة والـ ESC والبطارية والمظلة بكتالوجات خاصة
const partsFor = k => (curMode === 'human' && PARTS_H[k]) ? PARTS_H[k] : PARTS[k];
function wlab(w){ return w >= 1000 ? (w / 1000).toFixed(1) + 'kg' : w + 'g'; }
function fillSel(k){
  const sel = $('sel-' + k); if (!sel) return;
  const cat = partsFor(k); sel.innerHTML = '';
  Object.keys(cat).forEach(key => {
    const p = cat[key], o = document.createElement('option');
    o.value = key; o.textContent = p.n + (p.w ? ' (' + wlab(p.w) + ' · $' + p.c + ')' : '');
    sel.appendChild(o);
  });
  const want = saved[curMode][k] || (curMode === 'human' ? HUMAN_DEFAULT : STD_DEFAULT)[k];
  if (want && cat[want]) sel.value = want;
}
SLOTS.forEach(([k,label]) => {
  const row = document.createElement('div'); row.className = 'row'; row.id = 'row-' + k;
  const lab = document.createElement('label'); lab.textContent = label;
  const sel = document.createElement('select'); sel.id = 'sel-' + k;
  sel.addEventListener('change', () => { saved[curMode][k] = sel.value; updatePlane(k); });
  row.appendChild(lab); row.appendChild(sel); bp.appendChild(row);
  if (k === 'frame'){
    const br = document.createElement('div'); br.className = 'row'; br.id = 'row-body'; br.style.display = 'none';
    const bl = document.createElement('label'); bl.textContent = 'وزن الشخص (كغ)';
    const bs = document.createElement('select'); bs.id = 'sel-body';
    [45,50,55,60,65,70,75,80,85,90,95,100,110,120,130].forEach(v => { const o = document.createElement('option'); o.value = v; o.textContent = v + ' كغ'; bs.appendChild(o); });
    bs.value = '75'; bs.addEventListener('change', () => updatePlane('body'));
    br.appendChild(bl); br.appendChild(bs); bp.appendChild(br);
  }
});
SLOTS.forEach(([k]) => fillSel(k));
function syncMode(){
  const m = PARTS.frame[$('sel-frame').value].type === 'human' ? 'human' : 'std';
  if (m !== curMode){ curMode = m; SLOTS.forEach(([k]) => { if (k !== 'frame') fillSel(k); }); }
  document.body.classList.toggle('human', curMode === 'human');
  $('row-body').style.display = curMode === 'human' ? '' : 'none';
  $('row-chute').style.display = curMode === 'human' ? '' : 'none';
}
const info = document.createElement('div'); info.id = 'part-info'; bp.appendChild(info);
function setDrawer(open){
  document.body.classList.toggle('drawer-open', open);
  const ico = $('side-ico'); if (ico) ico.textContent = open ? '✕' : '🧩';
}
function toggleDrawer(){ setDrawer(!document.body.classList.contains('drawer-open')); }
$('side-btn').addEventListener('click', toggleDrawer);
$('canvas-container').addEventListener('pointerdown', () => setDrawer(false));
setDrawer(false);
syncMode();

function showInfo(slot){
  const cat = partsFor(slot), p = cat && cat[$('sel-' + slot).value];
  if (p && p.d){ info.style.display = 'block'; info.textContent = 'ℹ️ ' + p.d; } else info.style.display = 'none';
}

/* ======================= حسابات التصميم ======================= */
let cfg = null;
function compute(){
  const sel = {}; SLOTS.forEach(([k]) => sel[k] = partsFor(k)[$('sel-' + k).value]);
  const fr = sel.frame, type = fr.type, isQuad = type === 'quad';
  if (type === 'human') return computeHuman(sel, fr);
  const nMot = isQuad ? 4 : 1, nServo = isQuad ? 0 : (type === 'wing' ? 2 : 4);
  const bom = [];
  const add = (cat, p, qty) => { if (qty > 0 && (p.w || p.c)) bom.push({cat, n:p.n, qty, w:p.w * qty, c:p.c * qty}); };
  add('الهيكل', fr, 1);
  if (!isQuad) add('الجناح', sel.wing, 1);
  if (type === 'plane') add('الذيل', sel.tail, 1);
  add('البطارية', sel.battery, 1);
  add('المحرك', sel.motor, nMot);
  add('المروحة', sel.prop, nMot);
  add('متحكم السرعة', sel.esc, nMot);
  add('السيرفو', sel.servo, nServo);
  add('متحكم الطيران', sel.fc, 1);
  add('التحكم عن بعد', sel.rc, 1);
  add('الكاميرا', sel.cam, 1);
  bom.push({cat:'أسلاك ومواصلات وغراء', n:'أسلاك، XT60، ارتباطات، غراء', qty:1, w:40, c:10});
  const mass = bom.reduce((s, b) => s + b.w, 0), cost = bom.reduce((s, b) => s + b.c, 0);
  const cellsN = sel.battery.s, [cLo, cHi] = sel.motor.cells;
  const vFactor = cellsN < cLo ? Math.max(.5, cellsN / cLo) : 1;
  const thrust = sel.motor.t * sel.prop.tm * nMot * vFactor;
  const ampsMotor = sel.motor.a * sel.prop.am;
  const amps = ampsMotor * nMot;
  const twr = thrust / mass;
  const S = isQuad ? 0 : sel.wing.S;
  const g = 9.81, rho = 1.225;
  const stall = isQuad ? 0 : Math.sqrt(2 * (mass / 1000) * g / (rho * S * sel.wing.clmax));
  const wl = isQuad ? 0 : mass / (S * 100);
  const cruiseThr = isQuad ? Math.min(1, Math.max(.15, 1 / twr)) : .45;
  const timeMin = (sel.battery.mah / 1000 * .8) / (amps * cruiseThr) * 60;
  const cruiseSpeed = isQuad ? 10 : Math.max(stall * 1.6, 8);
  const rcKm = sel.rc.km;
  const range = Math.min(cruiseSpeed * timeMin * 60 / 1000 / (isQuad ? 1 : 1), rcKm * 2);
  const warnings = [];
  const bad = t => warnings.push({k:'bad', t}), ok = t => warnings.push({k:'ok', t}), meh = t => warnings.push({k:'meh', t});
  if (isQuad){ twr < 1.2 ? bad('TWR أقل من 1.2: الكوادكوبتر لن ترتفع بثبات.') : (twr < 2 ? meh('TWR مقبول للتحويم لكن بلا هامش مناورة.') : ok('TWR ممتاز للتحويم والمناورة.')); }
  else { twr < .35 ? bad('الدفع ضعيف جداً: لن تقلع.') : (twr < .5 ? meh('الدفع ضعيف: إقلاع صعب وصعود بطيء.') : ok('دفع كافٍ للإقلاع والصعود.')); }
  if (!isQuad){
    wl > 90 ? bad('تحميل الجناح عالٍ جداً (' + wl.toFixed(0) + ' g/dm²): هبوط خطير وسرعة انهيار عالية.') :
    (wl > 60 ? meh('تحميل الجناح مرتفع للمبتدئ.') : ok('تحميل الجناح مناسب.'));
    if (type === 'plane' && sel.tail.stab === 0 && sel.fc.stabil === 0) bad('طائرة بلا ذيل ولا متحكم طيران: ستكون غير مستقرة.');
    else if (type === 'plane' && sel.tail.stab === 0) meh('بلا ذيل: يعتمد الثبات كلياً على متحكم الطيران.');
    if (type === 'wing' && sel.fc.stabil === 0) meh('الجناح الطائر أسهل بكثير مع جيروسكوب.');
  }
  if (cellsN > cHi) bad('جهد البطارية (' + cellsN + 'S) أعلى من الحد الآمن للمحرك (' + cHi + 'S): سيحترق المحرك.');
  else if (cellsN < cLo) meh('بطارية ' + cellsN + 'S أقل من المطلوب للمحرك (' + cLo + 'S على الأقل): الدفع سينقص كثيراً.');
  else ok('جهد البطارية (' + cellsN + 'S) مناسب للمحرك.');
  if (sel.esc.a < ampsMotor * 1.2) bad('الـ ESC (' + sel.esc.a + 'A) أصغر من اللازم لتيار المحرك (' + ampsMotor.toFixed(0) + 'A): سيحترق.');
  else ok('الـ ESC مناسب لتيار المحرك.');
  const maxA = sel.battery.mah / 1000 * sel.battery.cmax;
  if (amps > maxA) bad('البطارية لا تتحمل التيار (' + amps.toFixed(0) + 'A مطلوب، حدها ~' + maxA.toFixed(0) + 'A): ستسخن وتنتفخ.');
  const batShare = sel.battery.w / mass;
  if (batShare > .45) meh('البطارية تشكل ' + (batShare * 100).toFixed(0) + '% من الوزن.');
  if (timeMin < 4) meh('زمن الطيران قصير (' + timeMin.toFixed(1) + ' د).');
  if (sel.cam.w >= 80 && mass < 500) meh('كاميرا HD ثقيلة على طائرة صغيرة: انتبه لمركز الثقل.');
  return {sel, fr, type, isQuad, nMot, nServo, bom, mass, cost, thrust, ampsMotor, amps, twr, S, stall, wl, cruiseThr, timeMin, cruiseSpeed, rcKm, range, warnings, clmax: isQuad ? 0 : sel.wing.clmax, k: isQuad ? 0 : sel.wing.k, cd: fr.cd};
}

/* ======================= حسابات الإنسان بجناح الحقيبة ======================= */
const RHO = 1.225, GRAV = 9.81;
const ETA_S = .62;                 // معامل الجودة الكلي للمروحة+المحرك+ESC عند الثبات
const ETA_P = .72, ETA_M = .88;    // كفاءة المروحة أثناء الطيران وكفاءة المحرك+ESC
const AUTO_STALL = 12, AUTO_AR = 6, E_OSW = .85;   // سرعة الانهيار المستهدفة (م/ث)، نسبة الباع/الوتر، معامل أوزوالد
const BAT_SCALE = 10;              // تسريع استهلاك البطارية في المحاكاة (نفس المعامل المستخدم للطائرات)
// وزن جناح كربون/فوم قابل للطي ≈ 0.9 كغ/م² + 0.8 كغ للمفصلات؛ الجناح المرفرف +35% و+1.5 كغ للميكانيزم
const wingMassKg = (S, flap) => flap ? (.9 * S + .8) * 1.35 + 1.5 : .9 * S + .8;
function recWing(M, clmax){
  clmax = clmax || 1.3;
  const S = Math.max(2.5, Math.min(16, 2 * M * GRAV / (RHO * clmax * AUTO_STALL * AUTO_STALL)));
  return {S, b: Math.sqrt(AUTO_AR * S)};
}
// القدرة الكهربائية اللازمة لدفع T (نيوتن) عند سرعة v (م/ث) بمروحة مساحة قرصها A (م²)
function powerElec(T, v, A){
  if (T <= 0) return 0;
  const vh = Math.sqrt(T / (2 * RHO * A));
  const Ps = Math.pow(T, 1.5) / (Math.sqrt(2 * RHO * A) * ETA_S);   // نظرية الزخم عند الثبات
  const Pd = T * v / (ETA_P * ETA_M);                              // قدرة الدفع أثناء الطيران
  return Math.max(Pd, Ps * (1 - .5 * Math.min(1, v / (3 * vh + .01))));
}
function computeHuman(sel, fr){
  const bodyKg = +$('sel-body').value || 75, nServo = 2;
  const W = sel.wing, mot = sel.motor, prop = sel.prop, esc = sel.esc, bat = sel.battery, chute = sel.chute;
  const A = Math.PI * prop.D * prop.D / 4;
  const fixedKg = (fr.w + mot.w + prop.w + esc.w + bat.w + sel.servo.w * nServo + sel.fc.w + sel.rc.w + sel.cam.w + chute.w + 600) / 1000;
  let S, b, wKg, clmax = W.clmax;
  if (W.auto){
    wKg = 6;
    for (let i = 0; i < 8; i++){ const r = recWing(bodyKg + fixedKg + wKg, clmax); S = r.S; b = r.b; wKg = wingMassKg(S, W.flap); }
  } else { S = W.S; b = W.b; wKg = W.w / 1000; }
  const wingPart = W.auto ? {n:W.n + ' (باع ' + b.toFixed(1) + ' م · ' + S.toFixed(1) + ' م²)', w:Math.round(wKg * 1000), c:Math.round((W.flap ? 1200 + 160 * S : 400 + 120 * S))} : W;
  const fold = W.auto ? Math.max(.8, b / 6.5) : W.fold;

  const bom = [];
  const add = (cat, p, qty) => { if (qty > 0 && (p.w || p.c)) bom.push({cat, n:p.n, qty, w:p.w * qty, c:p.c * qty}); };
  bom.push({cat:'الطيار', n:'وزن الجسم (' + bodyKg + ' كغ)', qty:1, w:bodyKg * 1000, c:0});
  add('الحقيبة والحزام', fr, 1);
  add('الجناح المطوي', wingPart, 1);
  add('المحرك', mot, 1);
  add('المروحة', prop, 1);
  add('متحكم السرعة', esc, 1);
  add('البطارية (داخل الحقيبة)', bat, 1);
  add('السيرفو', sel.servo, nServo);
  add('متحكم الطيران', sel.fc, 1);
  add('التحكم باليد', sel.rc, 1);
  add('الكاميرا', sel.cam, 1);
  add('المظلة الاحتياطية', chute, 1);
  bom.push({cat:'أسلاك وفيوز ومفتاح طوارئ', n:'موصلات QS8/XT90 وفيوز وحبل قطع الطوارئ', qty:1, w:600, c:80});
  const mass = bom.reduce((s, x) => s + x.w, 0), cost = bom.reduce((s, x) => s + x.c, 0);
  const M = mass / 1000, Wn = M * GRAV, gearKg = M - bodyKg;

  // الكهرباء والدفع (نظرية الزخم): T = (η·P·√(2ρA))^(2/3)
  const cellsN = bat.s, cLo = mot.cells[0], cHi = mot.cells[1];
  const vF = cellsN < cLo ? Math.pow(cellsN / cLo, 2) : 1;
  const Pmax = mot.P * 1000 * vF;
  const Tn = Math.pow(ETA_S * Pmax * Math.sqrt(2 * RHO * A), 2 / 3);
  const Imax = Pmax / (cellsN * 3.6);
  const twr = Tn / Wn;

  // الأيروديناميكا: سحب مستحث k = 1/(π·e·AR)
  const AR = b * b / S, k = 1 / (Math.PI * E_OSW * AR);
  const CdA = .17 + .012 * S, cd = CdA / S;
  const stall = Math.sqrt(2 * Wn / (RHO * S * clmax));
  const vc = Math.max(1.3 * stall, 10);
  const qc = .5 * RHO * vc * vc, CLc = Wn / (qc * S);
  const Dc = qc * S * (cd + k * CLc * CLc);
  const ld = 1 / (2 * Math.sqrt(cd * k));
  const roc = Math.max(0, (Tn - Dc) * vc / Wn);
  const Pc = powerElec(Dc, vc, A);
  const whNom = cellsN * 3.7 * bat.mah / 1000, whUse = whNom * .8;
  const timeMin = whUse / Math.max(Pc, 1) * 60;
  const range = vc * timeMin * 60 / 1000;
  const rec = recWing(M, clmax);

  const warnings = [];
  const bad = t => warnings.push({k:'bad', t}), ok = t => warnings.push({k:'ok', t}), meh = t => warnings.push({k:'meh', t});
  ok('وزنك ' + bodyKg + ' كغ + المعدات ' + gearKg.toFixed(0) + ' كغ = ' + M.toFixed(0) + ' كغ. الجناح الموصى به لوزنك: باع ~' + rec.b.toFixed(1) + ' م ومساحة ~' + rec.S.toFixed(1) + ' م².');
  if (!chute.w) bad('لا توجد مظلة احتياطية: أي تعطل للمحرك أو الجناح قاتل. أضف مظلة قبل الاختبار.');
  else ok('المظلة الاحتياطية موجودة (أقل ارتفاع آمن للفتح ' + chute.minAlt + ' م).');
  twr < .2 ? bad('الدفع/الوزن ' + twr.toFixed(2) + ': ضعيف جداً للإقلاع والصعود.') :
    (twr < .35 ? meh('الدفع/الوزن ' + twr.toFixed(2) + ': صعود بطيء وهامش أمان صغير.') : ok('دفع كافٍ (' + (Tn / GRAV).toFixed(0) + ' كغ دفع، نسبة ' + twr.toFixed(2) + ' من الوزن).'));
  roc < .5 ? bad('معدل الصعود شبه معدوم (' + roc.toFixed(1) + ' م/ث): لن تحافظ على الارتفاع.') :
    (roc < 2 ? meh('معدل الصعود ضعيف (' + roc.toFixed(1) + ' م/ث).') : ok('معدل الصعود ~' + roc.toFixed(1) + ' م/ث.'));
  stall > 17 ? bad('سرعة الانهيار ' + stall.toFixed(0) + ' م/ث (' + (stall * 3.6).toFixed(0) + ' كم/س): الهبوط على القدمين خطير. كبّر الجناح.') :
    (stall > 13 ? meh('سرعة انهيار عالية (' + (stall * 3.6).toFixed(0) + ' كم/س): هبوط صعب ويحتاج مضمار طويلاً.') : ok('سرعة الانهيار ' + (stall * 3.6).toFixed(0) + ' كم/س مقبولة.'));
  if (stall > 9) meh('أسرع من سرعة الركض (~9 م/ث): الإقلاع يتم من منحدر أو بمساعدة (زر ⛰️ داخل الاختبار).');
  if (cellsN > cHi) bad('جهد البطارية (' + cellsN + 'S) أعلى من الحد الآمن للمحرك (' + cHi + 'S): سيحترق.');
  else if (cellsN < cLo) meh('بطارية ' + cellsN + 'S أقل من المطلوب (' + cLo + 'S): تقل القدرة والدفع كثيراً.');
  else ok('جهد البطارية (' + cellsN + 'S) مناسب للمحرك.');
  if (esc.a < Imax * 1.15) bad('الـ ESC (' + esc.a + 'A) أصغر من التيار الأقصى (' + Imax.toFixed(0) + 'A): سيحترق.');
  else ok('الـ ESC مناسب (التيار الأقصى ~' + Imax.toFixed(0) + 'A).');
  const maxA = bat.mah / 1000 * bat.cmax;
  if (Imax > maxA) bad('البطارية لا تتحمل التيار (' + Imax.toFixed(0) + 'A مطلوب، حدها ~' + maxA.toFixed(0) + 'A): ستسخن وتنتفخ.');
  gearKg > 35 ? bad('الحقيبة ثقيلة جداً (' + gearKg.toFixed(0) + ' كغ): خطر إصابة العمود الفقري.') :
    (gearKg > 28 ? meh('الحقيبة ثقيلة (' + gearKg.toFixed(0) + ' كغ).') : ok('وزن المعدات ' + gearKg.toFixed(0) + ' كغ مقبول.'));
  if (fold > 1.15) meh('الجناح مطوياً طوله ' + fold.toFixed(2) + ' م: الحقيبة تتجاوز ارتفاع الظهر.');
  if (b > 7.5) meh('باع كبير (' + b.toFixed(1) + ' م): يحتاج عارضة كربون مضاعفة ومفاصل مقواة.');
  if (timeMin < 6) meh('زمن الطيران قصير (' + timeMin.toFixed(1) + ' د).');
  if (!sel.fc.stabil) meh('بلا متحكم طيران: التحكم بميل الجسم متعب وغير مستقر.');
  if (W.flap) meh('جناح مرفرف: ميكانيزم إضافي ثقيل ومعقد؛ الرفع الأساسي من التقدم والرفرفة تزيد الاستهلاك ~8% فقط.');
  return {flap:!!W.flap, sel, fr, type:'human', isHuman:true, isQuad:false, nMot:1, nServo, bom, mass, cost, thrust:Tn / GRAV * 1000,
    ampsMotor:Imax, amps:Imax, twr, S, stall, wl:mass / (S * 100), cruiseThr:Math.min(1, Dc / Tn), timeMin, cruiseSpeed:vc,
    rcKm:999, range, warnings, clmax, k, cd, bodyKg, b, AR, ld, kw:Pmax / 1000, roc, whNom, whUse, vc, Dc, Pc, A, D:prop.D, fold,
    gearKg, wingKg:wKg, Tn, Wn, M, CLc, CdA, chuteOpen:chute.open, rec, mot, prop};
}

/* ======================= المشهد ثلاثي الأبعاد ======================= */
const container = $('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB);
scene.fog = new THREE.Fog(0x87CEEB, 150, 1200);
const camera = new THREE.PerspectiveCamera(70, innerWidth / innerHeight, .1, 3000);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
container.appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff, .65));
const sun = new THREE.DirectionalLight(0xffffff, .8); sun.position.set(100, 200, 50); scene.add(sun);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000), new THREE.MeshStandardMaterial({color:0x3d7a3a}));
ground.rotation.x = -Math.PI / 2; ground.position.y = -.01; scene.add(ground);
const runway = new THREE.Mesh(new THREE.PlaneGeometry(12, 500), new THREE.MeshStandardMaterial({color:0x444a52}));
runway.rotation.x = -Math.PI / 2; runway.position.set(0, 0, 200); scene.add(runway);
for (let i = 0; i < 90; i++){
  const t = new THREE.Mesh(new THREE.ConeGeometry(2, 8, 6), new THREE.MeshStandardMaterial({color:0x1f5a2a}));
  const a = Math.random() * 6.283, r = 60 + Math.random() * 900;
  t.position.set(Math.cos(a) * r, 4, Math.sin(a) * r); scene.add(t);
}
const planeGroup = new THREE.Group(); planeGroup.rotation.order = 'YXZ'; scene.add(planeGroup);
let spinners = [];

function M(col){ return new THREE.MeshStandardMaterial({color:col}); }
function box(w, h, d, col, x, y, z){ const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), M(col)); m.position.set(x || 0, y || 0, z || 0); planeGroup.add(m); return m; }

/* ======================= نموذج القطع القابل للتركيب ======================= */
let stage = 'select', built = false, held = null, autoRun = false;
let MP = [], fuseMat = null;
const orb = {yaw:.8, pitch:.35, dist:11};
const LBL = {wing:'الجناح', tail:'الذيل', servo:'السيرفو', motor:'المحرك', esc:'متحكم السرعة ESC', battery:'البطارية', fc:'متحكم الطيران', rc:'جهاز الاستقبال', cam:'الكاميرا', prop:'المروحة', chute:'المظلة الاحتياطية'};
const MT = {
  wing:'يُثبَّت فوق الهيكل بزاوية سقوط موجبة ~2° مع تماثل تام بين الجهتين.',
  tail:'في مؤخرة الهيكل: المثبت الأفقي مستوٍ وعمودي على الزعنفة ليعطي ثباتاً.',
  servo:'يحرك الأسطح المتحركة (الجنيحات/المصعد/الدفة) عبر قضبان دفع قصيرة.',
  motor:'في مقدمة الهيكل مع زاوية دفع ~2° لأسفل ولليمين لمقاومة عزم الدوران.',
  esc:'داخل الهيكل في مجرى هواء للتبريد؛ يربط البطارية بأسلاك المحرك الثلاثة.',
  battery:'تحت الهيكل على منزلق: حرّكها أماماً أو خلفاً لضبط مركز الثقل.',
  fc:'قرب مركز الثقل وبعيداً عن المحرك والـ ESC، والسهم نحو الأمام.',
  rc:'داخل الهيكل بعيداً عن الكربون والمعادن، والهوائيات بزاوية 90° بينهما.',
  cam:'في المقدمة، ثابتة ومعزولة عن الاهتزاز.',
  prop:'تُركَّب أخيراً بعد التأكد من اتجاه المحرك؛ الجهة المنحنية للأمام.',
  chute:'في أعلى الحقيبة بمقبض سهل الوصول، مطوية بإتقان وبمنع التشابك مع الجناح.'
};
const V = (x, y, z) => new THREE.Vector3(x, y, z);
function bx(g, w, h, d, col, x, y, z){ const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), M(col)); m.position.set(x || 0, y || 0, z || 0); g.add(m); return m; }

function buildModel(c){
  while (planeGroup.children.length) planeGroup.remove(planeGroup.children[0]);
  spinners = []; MP = []; fuseMat = null;
  const S = c.sel, hasFc = !!(S.fc.w || S.fc.c), big = S.prop.tm >= 1.2;
  function mk(o, fill){
    const g = new THREE.Group(); planeGroup.add(g); fill(g);
    const gh = new THREE.Mesh(new THREE.SphereGeometry(.2, 12, 10), new THREE.MeshBasicMaterial({color:0xff9f1c, transparent:true, opacity:.4, depthTest:false}));
    gh.position.copy(o.pos); gh.renderOrder = 10; gh.visible = false; planeGroup.add(gh);
    const i = o.i || 0, cnt = o.cnt || 1;
    const m = {slot:o.slot, id:o.slot + i, label:LBL[o.slot] + (cnt > 1 ? ' ' + (i + 1) : ''), part:S[o.slot], g, ghost:gh, out:o.out || V(0, 3, 0), needs:o.needs || [], hint:o.hint || MT[o.slot], mounted:true, anim:1};
    g.traverse(x => { if (x.isMesh) x.userData.mp = m; }); gh.userData.mp = m;
    MP.push(m); return m;
  }
  if (c.isQuad){
    const fr = new THREE.Group(); planeGroup.add(fr);
    bx(fr, 1.2, .4, 1.2, 0x333333);
    [Math.PI / 4, -Math.PI / 4].forEach(a => { bx(fr, 5.2, .14, .28, 0x666666).rotation.y = a; });
    const P = [[1.85,1.85],[-1.85,1.85],[1.85,-1.85],[-1.85,-1.85]];
    P.forEach(([x, z], i) => mk({slot:'motor', i, cnt:4, pos:V(x, .2, z), hint:'على طرف كل ذراع؛ اثنان CW واثنان CCW بالتبادل القطري.'}, g => {
      const mo = new THREE.Mesh(new THREE.CylinderGeometry(.22, .22, .3, 10), M(0x222222)); mo.position.set(x, .2, z); g.add(mo); }));
    P.forEach(([x, z], i) => mk({slot:'esc', i, cnt:4, pos:V(x * .55, .18, z * .55), needs:['motor' + i]}, g => bx(g, .3, .1, .3, 0xcc3333, x * .55, .15, z * .55)));
    mk({slot:'battery', pos:V(0, -.3, 0), out:V(0, -3, 0), needs:['esc0','esc1','esc2','esc3']}, g => bx(g, .7, .25, .5, 0xffcc00, 0, -.3, 0));
    if (hasFc) mk({slot:'fc', pos:V(0, .28, 0), needs:['battery0']}, g => bx(g, .4, .08, .4, 0x22aa55, 0, .28, 0));
    mk({slot:'rc', pos:V(-.35, .28, -.35), needs:[hasFc ? 'fc0' : 'battery0']}, g => bx(g, .2, .1, .3, 0x333355, -.35, .28, -.35));
    if (S.cam.w) mk({slot:'cam', pos:V(0, -.1, .7), out:V(0, -3, 0)}, g => bx(g, .25, .25, .25, 0x111111, 0, -.1, .7));
    P.forEach(([x, z], i) => mk({slot:'prop', i, cnt:4, pos:V(x, .75, z), needs:['motor' + i, 'esc' + i]}, g => {
      const pr = bx(g, 1.5, .03, .12, i % 2 ? 0xff5533 : 0x35d0ff, x, .4, z); spinners.push({m:pr, axis:'y', dir:i % 2 ? 1 : -1}); }));
    return;
  }
  if (c.isHuman){
    // طيار مستلقٍ: الرأس نحو +z، الظهر نحو +y، الجناح يخرج من حقيبة الظهر، والمروحة خلف القدمين على عمود
    const sc = Math.cbrt(c.bodyKg / 75), wb = c.b, ch = c.S / c.b, zc = .08 * sc;
    const fr = new THREE.Group(); planeGroup.add(fr);
    bx(fr, .42 * sc, .24 * sc, .7 * sc, 0xff4d1a, 0, 0, .1 * sc);
    const hd = new THREE.Mesh(new THREE.SphereGeometry(.14 * sc, 12, 10), M(0xe0b090)); hd.position.set(0, .03, .62 * sc); fr.add(hd);
    const hm = new THREE.Mesh(new THREE.SphereGeometry(.165 * sc, 12, 10), M(0xffd400)); hm.position.set(0, .07 * sc, .6 * sc); fr.add(hm);
    [-1, 1].forEach(sx => {
      bx(fr, .13 * sc, .13 * sc, .85 * sc, 0x1c3a6b, sx * .1 * sc, -.02, -.72 * sc);
      bx(fr, .1 * sc, .1 * sc, .62 * sc, 0xff4d1a, sx * .3 * sc, 0, .5 * sc);
    });
    fuseMat = M(0x444a55);
    const pack = new THREE.Mesh(new THREE.BoxGeometry(.5 * sc, .22, .75 * sc), fuseMat); pack.position.set(0, .2 * sc + .05, zc); fr.add(pack);
    const yP = Math.max(.45, c.D / 2 + .15), zM = -1.35 * sc, zP = zM - .23;
    bx(fr, .07, .07, -zM - .25, 0x555555, 0, yP, (zM - .25) / 2);
    bx(fr, .07, yP - .25, .07, 0x555555, 0, (yP + .25) / 2, -.3 * sc);
    const yi = .26 * sc;
    const whalf = wb / 2, WN = 6, wseg = whalf / WN, WDIH = .12;
    const chAt = x => ch * (1.3 - .8 * Math.abs(x) / whalf), yAt = x => .46 + Math.abs(x) * WDIH, zAt = x => .05 - Math.abs(x) * .12;
    // الجناح يكون مطوياً (ضيقاً) داخل الحقيبة أثناء التركيب ثم ينفرد عند تركيبه. كل نصف جناح مجموعة بمفصل عند الكتف ليمكنه الرفرفة
    let wingHalves = null;
    const wingM = mk({slot:'wing', pos:V(0, .5, .05), out:V(0, 0, 0), hint:'ينفرد من الحقيبة ويُقفل في المنتصف فوق الكتفين؛ باعه ' + wb.toFixed(1) + ' م وطوله مطوياً ~' + c.fold.toFixed(1) + ' م. الجهتان متماثلتان تماماً.' + (c.flap ? ' ذراعا الرفرفة تتصلان بعلبة تروس من المحرك.' : '')}, g => {
      wingHalves = [];
      [-1, 1].forEach(sx => {
        const hg = new THREE.Group(); hg.position.set(0, .46, .05); g.add(hg); wingHalves.push(hg);
        for (let i = 0; i < WN; i++){
          const xc = sx * (i + .5) * wseg;
          const sg = bx(hg, wseg * 1.04, .045, chAt(xc), i % 2 ? 0xe8dcc8 : 0xf4ecda, xc, yAt(xc) - .46, zAt(xc) - .05);
          sg.rotation.z = sx * Math.atan(WDIH);
        }
        for (let j = 0; j < 5; j++){
          const fe = bx(hg, .45, .025, .11, j % 2 ? 0x5a4632 : 0x7a6244, sx * (whalf + .2), yAt(whalf) + .05 + j * .015 - .46, zAt(whalf) + (j - 2) * .11 - .05);
          fe.rotation.y = sx * (j - 2) * .14; fe.rotation.z = sx * .28;
        }
      });
      bx(g, .5, .07, ch * 1.3, 0xc9bda4, 0, .47, .05);
    });
    wingM.flap = wingHalves;
    [-1, 1].forEach((sx, i) => mk({slot:'servo', i, cnt:2, pos:V(sx * wb * .3, yAt(wb * .3) + .05, zAt(wb * .3) - chAt(wb * .3) / 2 + .1), needs:['wing0'], hint:'في الحافة الخلفية للجناح لتحريك الجنيحات (Flaperons) للتحكم بالميلان والارتفاع.'},
      g => bx(g, .16, .08, .2, 0x2a6fd6, sx * wb * .3, yAt(wb * .3) + .05, zAt(wb * .3) - chAt(wb * .3) / 2 + .1)));
    mk({slot:'motor', pos:V(0, yP, zM), out:V(0, 0, -4), needs:['wing0'], hint:'على عمود خلف القدمين وبمحاذاة مركز الثقل قدر الإمكان؛ يدفع للأمام وبعيداً عن الجسم.'}, g => {
      const n = new THREE.Mesh(new THREE.CylinderGeometry(.14, .14, .3, 12), M(0xaaaaaa)); n.rotation.x = Math.PI / 2; n.position.set(0, yP, zM); g.add(n); });
    mk({slot:'esc', pos:V(0, yi, zc - .25 * sc), needs:['motor0'], hint:'داخل الحقيبة قرب المحرك مع تبريد وسلك ثلاثي سميك إلى العمود.'}, g => bx(g, .2, .1, .14, 0xcc3333, 0, yi, zc - .25 * sc));
    if (S.fc.w || S.fc.c) mk({slot:'fc', pos:V(0, yi, zc - .08 * sc), needs:['battery0'], hint:'قرب مركز الثقل، بعيداً عن الـ ESC والمحرك، والسهم نحو الأمام.'}, g => bx(g, .14, .06, .14, 0x22aa55, 0, yi, zc - .08 * sc));
    if (S.chute.w) mk({slot:'chute', pos:V(0, yi, zc + .08 * sc), out:V(0, 3, 0), needs:['battery0']}, g => bx(g, .26, .1, .18, 0xff5533, 0, yi, zc + .08 * sc));
    mk({slot:'battery', pos:V(0, yi, zc + .26 * sc), out:V(0, 3, 0), needs:['esc0'], hint:'في الجيب العلوي للحقيبة مع فيوز رئيسي ومفتاح قطع طوارئ بحبل بمتناول اليد، ومعزولة حرارياً عن ظهرك.'}, g => bx(g, .3, .12, .2, 0xffcc00, 0, yi, zc + .26 * sc));
    if (S.cam.w) mk({slot:'cam', pos:V(0, .2, .78 * sc), out:V(0, 3, 0)}, g => bx(g, .1, .1, .12, 0x111111, 0, .2, .78 * sc));
    mk({slot:'prop', pos:V(0, yP, zP), out:V(0, 0, -5), needs:['motor0', 'esc0']}, g => {
      const pr = bx(g, c.D, .05, .12, 0x222222, 0, yP, zP); spinners.push({m:pr, axis:'z', dir:1}); });
    return;
  }
  const isWing = c.type === 'wing', cargo = c.fr === PARTS.frame.cargo;
  const L = isWing ? 2.4 : (cargo ? 7 : 5.2), R = cargo ? .8 : (isWing ? .35 : .4);
  const fr = new THREE.Group(); planeGroup.add(fr);
  fuseMat = M(isWing ? 0xdddddd : (cargo ? 0x7a7a7a : 0xd0d4dc));
  const fus = new THREE.Mesh(new THREE.CylinderGeometry(R, R * .6, L, 10), fuseMat); fus.rotation.x = Math.PI / 2; fr.add(fus);
  const span = Math.max(3, c.S * 18), chord = isWing ? 1.9 : 1.1, wz = isWing ? -.3 : .4, tz = -L / 2 + .3;
  mk({slot:'wing', pos:V(0, .45, wz), out:V(0, 4, 0)}, g => {
    bx(g, span, .12, chord, isWing ? 0xe8e8ee : 0xeeeeee, 0, .05, wz);
    if (isWing){ bx(g, .1, .8, .8, 0xff9f1c, span / 2 - .1, .4, -.9); bx(g, .1, .8, .8, 0xff9f1c, -span / 2 + .1, .4, -.9); }
  });
  let tl = null;
  if (c.type === 'plane' && (S.tail.w || S.tail.c)) tl = mk({slot:'tail', pos:V(0, .65, tz), out:V(0, 0, -4)}, g => {
    if (S.tail === PARTS.tail.conv){ bx(g, span * .38, .1, .7, 0xeeeeee, 0, .1, tz); bx(g, .1, 1.1, .8, 0xff9f1c, 0, .6, tz); }
    else { bx(g, .1, 1.3, .7, 0xff9f1c, .55, .55, tz).rotation.z = -.6; bx(g, .1, 1.3, .7, 0xff9f1c, -.55, .55, tz).rotation.z = .6; }
  });
  const sv = (i, x, y, z, needs) => mk({slot:'servo', i, cnt:c.nServo, pos:V(x, y, z), needs}, g => bx(g, .22, .16, .3, 0x2a6fd6, x, y, z));
  if (c.nServo === 2){ sv(0, span * .3, .2, wz - .2, ['wing0']); sv(1, -span * .3, .2, wz - .2, ['wing0']); }
  else if (c.nServo === 4){
    sv(0, span * .3, .2, wz + .2, ['wing0']); sv(1, -span * .3, .2, wz + .2, ['wing0']);
    sv(2, .3, .25, tz + .6, tl ? ['tail0'] : []); sv(3, -.3, .25, tz + .6, tl ? ['tail0'] : []);
  }
  mk({slot:'motor', pos:V(0, 0, L / 2 + .1), out:V(0, 0, 4)}, g => {
    const n = new THREE.Mesh(new THREE.CylinderGeometry(.2, .2, .45, 10), M(0xaaaaaa)); n.rotation.x = Math.PI / 2; n.position.set(0, 0, L / 2 + .1); g.add(n); });
  mk({slot:'esc', pos:V(0, 0, -L * .08), needs:['motor0']}, g => bx(g, .3, .15, .5, 0xcc3333, 0, 0, -L * .08));
  mk({slot:'battery', pos:V(0, -R - .12, .2), out:V(0, -3, 0), needs:['esc0']}, g => bx(g, .5, .25, 1, 0xffcc00, 0, -R - .12, .2));
  if (hasFc) mk({slot:'fc', pos:V(0, .05, L * .06), needs:['battery0']}, g => bx(g, .3, .08, .3, 0x22aa55, 0, .05, L * .06));
  mk({slot:'rc', pos:V(0, .08, -L * .2), needs:[hasFc ? 'fc0' : 'battery0']}, g => bx(g, .2, .1, .3, 0x333355, 0, .08, -L * .2));
  if (S.cam.w) mk({slot:'cam', pos:V(0, -R - .1, L / 2 - .6), out:V(0, -3, 0)}, g => bx(g, .25, .25, .3, 0x111111, 0, -R - .1, L / 2 - .6));
  mk({slot:'prop', pos:V(0, 0, L / 2 + .7), out:V(0, 0, 5), needs:['motor0', 'esc0']}, g => {
    const pr = bx(g, big ? 2.4 : 1.7, .08, .14, 0x222222, 0, 0, L / 2 + .4); spinners.push({m:pr, axis:'z', dir:1}); });
}

/* ======================= ورشة التركيب ======================= */
const byId = id => MP.find(x => x.id === id);
const ready = m => m.needs.every(id => { const o = byId(id); return !o || o.mounted; });
const nextMP = () => MP.find(m => !m.mounted && ready(m));
function setXray(on){ if (fuseMat){ fuseMat.transparent = on; fuseMat.opacity = on ? .3 : 1; fuseMat.depthWrite = !on; fuseMat.needsUpdate = true; } }
function fitCam(){ orb.dist = cfg.isHuman ? 8 + cfg.b * .9 : (cfg.fr === PARTS.frame.cargo ? 15 : (cfg.isQuad ? 9 : 11)); }
function say(t){ $('banner').textContent = t; clearTimeout(say.t); say.t = setTimeout(refreshBuildUI, 5000); }

function refreshBuildUI(){
  const ch = $('chips'); ch.innerHTML = ''; const G = {};
  MP.forEach(m => { const g = G[m.slot] = G[m.slot] || {m, left:0}; if (!m.mounted) g.left++; });
  Object.keys(G).forEach(k => {
    const g = G[k], d = document.createElement('div');
    d.className = 'chip' + (held === k ? ' sel' : '') + (g.left ? '' : ' done'); d.id = 'chip-' + k;
    const s = document.createElement('small'); s.textContent = LBL[k];
    const b = document.createElement('b'); b.textContent = (g.left ? '' : '✓ ') + g.m.part.n + (g.left > 1 ? ' ×' + g.left : '');
    d.appendChild(s); d.appendChild(document.createElement('br')); d.appendChild(b);
    d.addEventListener('click', () => pickChip(k)); ch.appendChild(d);
  });
  const done = MP.filter(m => m.mounted).length; $('prog').textContent = done + '/' + MP.length;
  const nx = nextMP();
  $('banner').textContent = stage !== 'build' ? '' : (!nx
    ? '✅ اكتمل التركيب! اضغط «③ الاختبار» لتجربة الطيران.'
    : 'الخطوة ' + (done + 1) + '/' + MP.length + ': اختر «' + nx.part.n + '» من الصندوق ثم المس مكانها المتوهج على الطائرة. ' + nx.hint);
}
function pickChip(k){
  if (autoRun) return;
  held = held === k ? null : k;
  const m = MP.find(x => x.slot === k); refreshBuildUI();
  if (held) say('🧩 ' + m.part.n + ': ' + m.part.d + ' — ' + m.hint);
}
function mount(m){
  m.mounted = true;
  if (!MP.some(x => x.slot === m.slot && !x.mounted) && held === m.slot) held = null;
  if (MP.every(x => x.mounted)){ built = true; flash('✅ اكتمل التركيب! انتقل إلى ③ الاختبار', 2600); }
  refreshBuildUI();
}
function tryMount(m){
  if (held !== m.slot){
    say('⚠️ هذا مكان «' + m.label + '». اختر القطعة الصحيحة من الصندوق بالأسفل.');
    const c = $('chip-' + m.slot); if (c){ c.classList.add('hint'); setTimeout(() => c.classList.remove('hint'), 1500); }
    return;
  }
  const miss = m.needs.map(byId).filter(o => o && !o.mounted)[0];
  if (miss){ say('⛔ لا يمكن تركيب «' + m.label + '» الآن؛ ركّب أولاً: ' + miss.label); return; }
  mount(m);
}
function tryUnmount(m){
  if (held){ say('هذا المكان مشغول. المس القطعة بدون اختيار شيء من الصندوق لفكّها.'); return; }
  const dep = MP.find(x => x.mounted && x.needs.includes(m.id));
  if (dep){ say('⛔ فكّ «' + dep.label + '» أولاً قبل فكّ «' + m.label + '».'); return; }
  m.mounted = false; built = false; refreshBuildUI(); say('تم فك «' + m.label + '».');
}
const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
function tapAt(x, y){
  if (autoRun) return;
  ndc.set(x / innerWidth * 2 - 1, -(y / innerHeight) * 2 + 1); ray.setFromCamera(ndc, camera);
  const objs = [];
  MP.forEach(m => { if (m.ghost.visible) objs.push(m.ghost); if (m.mounted) m.g.traverse(o => { if (o.isMesh) objs.push(o); }); });
  const hs = ray.intersectObjects(objs, false);
  const h = hs.find(q => !q.object.userData.mp.mounted) || hs[0]; if (!h) return;
  const m = h.object.userData.mp; m.mounted ? tryUnmount(m) : tryMount(m);
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function autoBuild(){
  if (autoRun){ autoRun = false; return; }
  autoRun = true; held = null; $('auto-btn').textContent = '⏹ إيقاف';
  while (autoRun && stage === 'build'){
    const m = nextMP(); if (!m) break;
    held = m.slot; refreshBuildUI();
    $('banner').textContent = '🤖 الآلة تُركّب «' + m.part.n + '» في «' + m.label + '». ' + m.hint;
    await sleep(600); if (!autoRun || stage !== 'build') break;
    mount(m); await sleep(1000);
  }
  autoRun = false; held = null; $('auto-btn').textContent = '🤖 تركيب آلي'; refreshBuildUI();
}
function setStage(s){
  autoRun = false; $('auto-btn').textContent = '🤖 تركيب آلي';
  if (s === 'fly' && !built){ flash('🔧 ركّب الطائرة أولاً: يدوياً أو بالتركيب الآلي', 2800); s = 'build'; }
  stage = s; held = null;
  ['select', 'build', 'fly'].forEach(k => { document.body.classList.toggle('stage-' + k, k === s); $('st-' + k).classList.toggle('on', k === s); });
  if (s !== 'select') setDrawer(false);
  if (s === 'build') built = false;
  MP.forEach(m => { m.mounted = s !== 'build'; m.anim = m.mounted ? 1 : 0; });
  setXray(s === 'build');
  if (s === 'fly') resetState();
  if (s === 'build' && cfg.warnings.some(w => w.k === 'bad')) flash('⚠️ في تصميمك أخطاء هندسية (راجع الفحوصات في ①): يمكنك التركيب لكن الاختبار قد يفشل', 3500);
  refreshBuildUI();
}
function animMounts(dt){
  const tm = performance.now() / 1000;
  MP.forEach(m => {
    const to = m.mounted ? 1 : 0; m.anim += Math.sign(to - m.anim) * Math.min(Math.abs(to - m.anim), dt * 1.8);
    const e = m.anim * m.anim * (3 - 2 * m.anim);
    m.g.position.copy(m.out).multiplyScalar(1 - e);
    const folded = cfg.isHuman && m.slot === 'wing';           // جناح الإنسان يبقى ظاهراً مطوياً ثم ينفرد
    m.g.visible = folded || m.anim > .01;
    if (folded) m.g.scale.x = .1 + .9 * e;
    const sg = stage === 'build' && !m.mounted; m.ghost.visible = sg;
    if (sg){
      const hit = held === m.slot && ready(m), ok = ready(m), p = Math.sin(tm * 6);
      m.ghost.material.color.setHex(hit ? 0x00ff88 : (ok ? 0xff9f1c : 0x555555));
      m.ghost.material.opacity = hit ? .55 + .3 * p : (ok ? .4 : .18); m.ghost.scale.setScalar(hit ? 1.2 + .25 * p : 1);
    }
  });
  // رفرفة الجناح (للجناح المرفرف فقط): التردد والسعة يتبعان الثروتل، وتهدأ عند تعطل المحرك أو فتح المظلة
  const wm = cfg.isHuman && MP.find(x => x.slot === 'wing');
  if (wm && wm.flap){
    let amp = 0, pw = 0;
    if (cfg.flap && wm.mounted){
      if (stage === 'fly'){
        pw = (state.battery > 0 && !state.engineOut && !state.chute) ? state.throttle : 0;
        amp = (state.engineOut || state.battery <= 0 || state.chute) ? .05 : .12 + .3 * pw;
      } else amp = .22;
    }
    flapPh += dt * 6.283 * (.9 + 2.4 * pw);
    const an = amp * Math.sin(flapPh);
    wm.flap[0].rotation.z = -an; wm.flap[1].rotation.z = an;
  }
}
function orbitCam(){
  const d = orb.dist, cp = Math.cos(orb.pitch);
  camera.position.lerp(V(Math.sin(orb.yaw) * cp * d, .5 + Math.sin(orb.pitch) * d, Math.cos(orb.yaw) * cp * d), .2);
  camera.lookAt(0, .6, 0);
}
const ptrs = new Map(); let moved = 0, pinch0 = 0;
const pdist = () => { const a = [...ptrs.values()]; return Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y); };
const cv = $('canvas-container');
cv.addEventListener('pointerdown', e => { ptrs.set(e.pointerId, {x:e.clientX, y:e.clientY}); if (ptrs.size === 1) moved = 0; if (ptrs.size === 2) pinch0 = pdist(); });
cv.addEventListener('pointermove', e => {
  const p = ptrs.get(e.pointerId); if (!p || stage === 'fly') return;
  const dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY; moved += Math.abs(dx) + Math.abs(dy);
  if (ptrs.size === 2){ const d = pdist(); if (pinch0) orb.dist = Math.max(5, Math.min(26, orb.dist * pinch0 / d)); pinch0 = d; }
  else { orb.yaw -= dx * .008; orb.pitch = Math.max(.05, Math.min(1.4, orb.pitch + dy * .008)); }
});
cv.addEventListener('pointerup', e => { const had = ptrs.delete(e.pointerId); if (had && ptrs.size === 0 && moved < 8 && stage === 'build') tapAt(e.clientX, e.clientY); });
cv.addEventListener('pointercancel', e => ptrs.delete(e.pointerId));
cv.addEventListener('wheel', e => { if (stage !== 'fly') orb.dist = Math.max(5, Math.min(26, orb.dist + e.deltaY * .01)); }, {passive:true});
$('st-select').addEventListener('click', () => { setStage('select'); setDrawer(true); });
$('st-build').addEventListener('click', () => setStage('build'));
$('st-fly').addEventListener('click', () => setStage('fly'));
$('auto-btn').addEventListener('click', autoBuild);
$('build-reset').addEventListener('click', () => setStage('build'));

/* ======================= الحالة والتحكم ======================= */
let state = {};
let launchMode = 'ground';
let flapPh = 0, camView = 0;
const IDLE = {x:0, z:0, alt:0, heading:0, pitch:0, roll:0};   // وضعية النموذج خارج الاختبار (في المركز دائماً)
const CAM_NAMES = ['خلفية بعيدة', 'قريبة', 'أمامية'];
const canopy = new THREE.Mesh(new THREE.SphereGeometry(3.4, 18, 10, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({color:0xff5533, side:THREE.DoubleSide}));
canopy.scale.y = .55; canopy.visible = false; scene.add(canopy);
function setLaunch(m){
  launchMode = m;
  $('t-launch').textContent = m === 'slope' ? '⛰️ منحدر 25م' : '🏃 ركض';
}
function resetState(){
  state = {speed:0, vz:0, alt:0, x:0, z:0, heading:0, throttle:0, pitch:0, roll:0, pitchIn:0, rollIn:0, battery:100, crashed:0, t:0, drift:0, chute:0, chuteT:0, engineOut:0};
  if (cfg && cfg.isHuman && launchMode === 'slope'){ state.alt = 25; state.speed = Math.max(cfg.stall * 1.25, 8); state.throttle = .55; }
  planeGroup.position.set(0, .5, 0);
  $('t-fail').classList.remove('on');
  updateThrottleUI();
}
function updateThrottleUI(){
  $('throttle-fill').style.height = Math.round(state.throttle * 100) + '%';
  $('throttle-text').textContent = Math.round(state.throttle * 100) + '%';
}
function setThrottle(v){ state.throttle = Math.max(0, Math.min(1, v)); updateThrottleUI(); }

$('btn-pitch-up').addEventListener('pointerdown', () => state.pitchIn = 1);
$('btn-pitch-down').addEventListener('pointerdown', () => state.pitchIn = -1);
$('btn-roll-left').addEventListener('pointerdown', () => state.rollIn = -1);
$('btn-roll-right').addEventListener('pointerdown', () => state.rollIn = 1);
addEventListener('pointerup', () => { state.pitchIn = 0; state.rollIn = 0; });
$('btn-thr-up').addEventListener('pointerdown', () => setThrottle(state.throttle + .1));
$('btn-thr-down').addEventListener('pointerdown', () => setThrottle(state.throttle - .1));
function barSet(e){ const r = $('throttle-bar').getBoundingClientRect(); setThrottle(1 - (e.clientY - r.top) / r.height); }
$('throttle-bar').addEventListener('pointerdown', barSet);
$('throttle-bar').addEventListener('pointermove', e => { if (e.buttons) barSet(e); });
addEventListener('keydown', e => {
  const k = e.key;
  if (k === 'ArrowUp') state.pitchIn = 1; else if (k === 'ArrowDown') state.pitchIn = -1;
  else if (k === 'ArrowLeft') state.rollIn = -1; else if (k === 'ArrowRight') state.rollIn = 1;
  else if (k === 'w' || k === 'W') setThrottle(state.throttle + .1); else if (k === 's' || k === 'S') setThrottle(state.throttle - .1);
  else if (k === 'r' || k === 'R') resetState();
});
addEventListener('keyup', () => { state.pitchIn = 0; state.rollIn = 0; });

function flash(text, ms){ const m = $('msg'); m.textContent = text; m.style.display = 'block'; clearTimeout(flash.t); flash.t = setTimeout(() => m.style.display = 'none', ms || 2000); }

/* ======================= الفيزياء ======================= */
function step(dt){
  const c = cfg, g = 9.81, rho = 1.225, m = c.mass / 1000, W = m * g, s = state;
  s.t += dt;
  if (s.crashed){ s.crashed -= dt; if (s.crashed <= 0) resetState(); return; }
  if (s.battery <= 0 && s.throttle > 0){ setThrottle(0); flash('🔋 نفدت البطارية', 2500); }
  const dist = Math.hypot(s.x, s.z);
  const linked = dist / 1000 <= c.rcKm;
  if (!linked && !s.linkWarn){ s.linkWarn = 1; flash('📡 فقدان الاتصال!', 2500); }
  if (linked) s.linkWarn = 0;
  const thr = (linked && !s.engineOut && !s.chute) ? s.throttle : 0;
  const T = c.thrust * thr * g / 1000 * (.8 + .2 * s.battery / 100);
  const stabil = c.sel.fc.stabil;

  if (c.isHuman && s.chute){
    // المظلة: انفتاح تدريجي ثم هبوط ثابت ~5.5 م/ث؛ الفتح من ارتفاع منخفض يعني اصطداماً بسرعة عالية
    s.chuteT += dt;
    const f = Math.min(1, s.chuteT / Math.max(.1, c.chuteOpen));
    s.vz += (-g * (1 - f) + ((s.chuteVT || -5.5) - s.vz) * 3 * f) * dt;
    s.speed *= Math.exp(-.8 * dt);
    s.pitch += (85 - s.pitch) * 1.5 * dt; s.roll *= Math.exp(-2 * dt);
    const impactC = s.vz;
    s.alt += s.vz * dt;
    if (s.alt <= 0){
      s.alt = 0; s.vz = 0;
      if (impactC < -8){ s.crashed = 2.2; flash('💥 فُتحت المظلة متأخراً: الارتفاع غير كافٍ!', 2400); }
      else flash('🪂 هبوط ناجح بالمظلة', 2200);
      s.chute = 0; s.speed = 0; s.pitch = 3; s.roll = 0;
    }
    s.x += Math.sin(s.heading) * s.speed * dt; s.z += Math.cos(s.heading) * s.speed * dt;
    return;
  }

  if (c.isQuad){
    s.pitch += 60 * s.pitchIn * dt; s.roll += 60 * s.rollIn * dt;
    if (!s.pitchIn) s.pitch *= Math.exp(-(2 + 4 * stabil) * dt);
    if (!s.rollIn) s.roll *= Math.exp(-(2 + 4 * stabil) * dt);
    s.pitch = Math.max(-30, Math.min(30, s.pitch)); s.roll = Math.max(-30, Math.min(30, s.roll));
    const tilt = Math.cos(s.pitch * Math.PI / 180) * Math.cos(s.roll * Math.PI / 180);
    const az = (T * tilt - W) / m;
    s.vz += az * dt; s.vz *= Math.exp(-1.5 * dt);
    const target = (s.pitch / 30) * 14;
    s.speed += (target - s.speed) * 2 * dt;
    s.heading -= s.rollIn * 1.1 * dt;
    if (s.alt <= 0 && s.vz < 0) s.vz = 0;
    s.alt += s.vz * dt; if (s.alt < 0) s.alt = 0;
    if (s.alt <= 0 && thr < .05){ s.speed *= .9; }
  } else {
    const grounded = s.alt <= .01;
    s.pitch += 40 * s.pitchIn * dt; s.roll += 90 * s.rollIn * dt;
    if (!s.pitchIn) s.pitch += (3 - s.pitch) * (1.2 + 3 * stabil) * dt;
    if (!s.rollIn) s.roll *= Math.exp(-(1 + 4 * stabil) * dt);
    const instab = (c.type === 'plane' && c.sel.tail.stab === 0 ? 1 : 0) * (1 - stabil) + (c.type === 'wing' ? .35 * (1 - stabil) : 0) + (c.isHuman ? .15 * (1 - stabil) : 0);
    if (!grounded && instab > 0){ s.drift += (Math.random() - .5) * 200 * instab * dt; s.drift *= .96; s.pitch += s.drift * dt; s.roll += s.drift * .6 * dt; }
    s.pitch = Math.max(-30, Math.min(30, s.pitch)); s.roll = Math.max(-60, Math.min(60, s.roll));
    if (grounded){ s.roll = 0; if (s.pitch < 0) s.pitch = 0; }
    const q = .5 * rho * s.speed * s.speed;
    const clRaw = .35 + .09 * s.pitch;
    let CL = Math.max(0, Math.min(c.clmax, clRaw));
    const stalled = clRaw > c.clmax && s.speed > 3 && !grounded;
    if (stalled) CL = c.clmax * .5;
    if (stalled && !s.stallWarn){ s.stallWarn = 1; flash('⚠️ انهيار الجناح (Stall)! اخفض الأنف وزد الدفع', 1800); }
    if (!stalled) s.stallWarn = 0;
    const L = q * c.S * CL;
    const D = q * c.S * (c.cd + c.k * CL * CL) + (grounded ? .04 * W : 0);
    const gamma = s.vz / Math.max(s.speed, 1);
    s.speed += ((T - D) / m - g * gamma * .3) * dt; if (s.speed < 0) s.speed = 0;
    if (c.isHuman && grounded && launchMode !== 'slope' && s.speed > 9) s.speed = 9;   // أقصى سرعة ركض
    const az = (L * Math.cos(s.roll * Math.PI / 180) - W + (c.isHuman ? T * Math.sin(s.pitch * Math.PI / 180) : 0)) / m;
    if (grounded && az < 0) s.vz = 0; else { s.vz += az * dt; }
    s.vz *= Math.exp(-.8 * dt);
    const impact = s.vz;
    s.alt += s.vz * dt;
    if (s.alt < 0){
      if (impact < (c.isHuman ? -3.5 : -4) || (s.speed > c.stall * 2.2 && impact < -2.5)){ s.crashed = 2.2; flash(c.isHuman ? '💥 سقوط خطير! ← اهبط بنعومة (أقل من 3 م/ث رأسياً) أو افتح المظلة مبكراً' : '💥 تحطمت الطائرة! ← اهبط بنعومة وبسرعة منخفضة', 2200); }
      s.alt = 0; s.vz = 0;
    }
    if (s.alt > .5) s.heading -= g * Math.tan(s.roll * Math.PI / 180) / Math.max(s.speed, 5) * dt;
  }
  s.x += Math.sin(s.heading) * s.speed * dt; s.z += Math.cos(s.heading) * s.speed * dt;
  if (thr > 0){
    if (c.isHuman){
      // القدرة الفعلية من نظرية الزخم (تتناسب مع T^1.5 عند الثبات)
      const Pw = powerElec(T, s.speed, c.A) * (c.flap ? 1.08 : 1);
      s.battery = Math.max(0, s.battery - (Pw * dt / 3600) / c.whUse * 100 * BAT_SCALE);
    } else {
      const used = c.amps * thr * dt / 3600 * 1000;
      s.battery = Math.max(0, s.battery - used / c.sel.battery.mah * 100 * 10);
    }
  }
}

function render(dt){
  const s = state, p = stage === 'fly' ? s : IDLE;
  planeGroup.position.set(p.x, p.alt + .5, p.z);
  animMounts(dt);
  planeGroup.rotation.y = p.heading;
  planeGroup.rotation.x = cfg.isQuad ? p.pitch * Math.PI / 180 : -p.pitch * Math.PI / 180;
  planeGroup.rotation.z = p.roll * Math.PI / 180;
  canopy.visible = !!s.chute && stage === 'fly'; canopy.position.set(s.x, s.alt + 5.2, s.z);
  const spin = (s.battery > 0 && !s.engineOut && !s.chute ? s.throttle : 0) * 60 * dt;
  spinners.forEach(p => { if (p.axis === 'z') p.m.rotation.z += spin; else p.m.rotation.y += spin * p.dir; });
  if (stage === 'fly'){
    const sh = Math.sin(s.heading), ch = Math.cos(s.heading);
    if (cfg.isHuman){
      // كاميرا الإنسان: بعيدة لترى الجناح كاملاً، أو قريبة للجسم، أو أمامية؛ ويُزاح الطيار لليسار بعيداً عن لوح المعلومات
      const bb = cfg.b, V3 = [[7 + bb * 1.3, 2.5 + bb * .4, 2.4, 2.2], [4.5, 1.6, 1.2, 1.0], [-(5 + bb * .8), 2.2, 1.6, 1.0]][camView];
      const target = new THREE.Vector3(s.x - sh * V3[0], s.alt + V3[1], s.z - ch * V3[0]);
      camera.position.lerp(target, .12);
      camera.lookAt(s.x - ch * V3[2], s.alt + V3[3], s.z + sh * V3[2]);
    } else {
      const target = new THREE.Vector3(s.x - sh * 11, s.alt + 4.5, s.z - ch * 11);
      camera.position.lerp(target, .12);
      camera.lookAt(s.x, s.alt + 1, s.z);
    }
  } else orbitCam();
  renderer.render(scene, camera);
  $('hud-speed').textContent = Math.round(s.speed * 3.6);
  $('hud-alt').textContent = Math.round(s.alt);
  $('hud-dist').textContent = Math.round(Math.hypot(s.x, s.z));
  $('hud-bat').textContent = Math.round(s.battery);
  $('hud-bat').className = s.battery < 20 ? 'warn' : 'val';
}

/* ======================= الإحصاءات والفحوصات ======================= */
function renderStats(){
  const c = cfg;
  const hu = !!c.isHuman;
  $('hud-weight').textContent = hu ? (c.mass / 1000).toFixed(0) : Math.round(c.mass); $('u-w').textContent = hu ? 'kg' : 'g';
  $('hud-thrust').textContent = hu ? (c.thrust / 1000).toFixed(0) : Math.round(c.thrust); $('u-t').textContent = hu ? 'kgf' : 'g';
  const t = $('hud-twr'); t.textContent = c.twr.toFixed(2);
  t.className = c.twr < (c.isQuad ? 1.2 : .35) ? 'warn' : (c.twr > 2 ? 'good' : 'val');
  $('row-wl').style.display = c.isQuad ? 'none' : 'inline';
  $('row-h').style.display = hu ? 'inline' : 'none';
  if (hu){
    $('hud-span').textContent = c.b.toFixed(1); $('hud-ld').textContent = c.ld.toFixed(1);
    $('hud-pw').textContent = c.kw.toFixed(0); $('hud-roc').textContent = c.roc.toFixed(1);
  }
  $('hud-wl').textContent = c.wl.toFixed(0); $('hud-stall').textContent = Math.round(c.stall * 3.6);
  $('hud-time').textContent = c.timeMin.toFixed(1);
  $('hud-range').textContent = (c.rcKm >= 999 && !hu) ? c.range.toFixed(1) + '+' : c.range.toFixed(1);
  $('hud-cost').textContent = Math.round(c.cost);
  const box = $('checks'); box.innerHTML = '';
  c.warnings.forEach(w => {
    const d = document.createElement('div');
    d.className = w.k === 'bad' ? 'warn' : (w.k === 'ok' ? 'good' : '');
    d.style.color = w.k === 'meh' ? '#ffcc66' : '';
    d.textContent = (w.k === 'bad' ? '⛔ ' : w.k === 'ok' ? '✅ ' : '⚠️ ') + w.t;
    box.appendChild(d);
  });
}

function updatePlane(changed){
  syncMode();
  const q = PARTS.frame[$('sel-frame').value].type;
  $('sel-wing').disabled = q === 'quad'; $('sel-servo').disabled = q === 'quad';
  $('sel-tail').disabled = q !== 'plane';
  cfg = compute();
  if (cfg.isHuman) setLaunch(cfg.stall > 9 ? 'slope' : 'ground');
  buildModel(cfg); built = false; fitCam(); setStage('select'); resetState(); renderStats();
  if (changed) showInfo(changed);
}

/* ======================= قائمة القطع ======================= */
function showBom(){
  const c = cfg; let h = '<table><tr><th>القطعة</th><th>العدد</th><th>الوزن</th><th>السعر</th></tr>';
  c.bom.forEach(b => { h += '<tr><td>' + b.cat + '<br><small style="color:#889">' + b.n + '</small></td><td>' + b.qty + '</td><td>' + wlab(b.w) + '</td><td>$' + b.c + '</td></tr>'; });
  h += '<tr><th>الإجمالي</th><th></th><th>' + wlab(Math.round(c.mass)) + '</th><th>$' + Math.round(c.cost) + '</th></tr></table>';
  h += '<p style="font-size:.75rem;color:#889">الأسعار تقريبية وتختلف حسب المتجر والبلد. أضف أدوات التصنيع وشاحن LiPo إن لم تكن تملكهما.</p>';
  $('bom-body').innerHTML = h; $('bom-modal').style.display = 'flex';
}

/* ======================= دليل التصنيع (محلي) ======================= */
function humanGuide(c){
  const S = c.sel, f1 = x => x.toFixed(1), f0 = x => x.toFixed(0);
  const explain = 'طيار بوزن ' + c.bodyKg + ' كغ يطير مستلقياً بجناح قابل للطي داخل حقيبة الظهر، ومحرك ومروحة خلفية وبطارية داخل الحقيبة. الوزن الكلي ' + f0(c.M) + ' كغ، باع الجناح ' + f1(c.b) + ' م ومساحته ' + f1(c.S) + ' م²، وسرعة الانهيار ' + f0(c.stall * 3.6) + ' كم/س، وزمن الطيران المقدّر ~' + f1(c.timeMin) + ' دقيقة. هذا نموذج تعليمي للمحاكاة: الطيران الحقيقي بمثل هذه المعدات يتطلب مدرباً وتراخيص وسنوات تدريب.';
  const math = [
    'الوزن الكلي: M = جسم ' + c.bodyKg + ' + معدات ' + f1(c.gearKg) + ' = ' + f1(c.M) + ' كغ، ومنه الوزن W = M·g = ' + f0(c.Wn) + ' نيوتن.',
    'مساحة الجناح من سرعة الانهيار: S = 2W / (ρ·V²·CLmax) = 2×' + f0(c.Wn) + ' / (1.225×' + AUTO_STALL + '²×' + c.clmax + ') ≈ ' + f1(c.rec.S) + ' م²، والباع b = √(AR·S) = √(' + AUTO_AR + '×' + f1(c.rec.S) + ') ≈ ' + f1(c.rec.b) + ' م.',
    'جناحك الحالي: S = ' + f1(c.S) + ' م²، b = ' + f1(c.b) + ' م، AR = b²/S = ' + f1(c.AR) + '، تحميل الجناح = M/S = ' + f1(c.M / c.S) + ' كغ/م².',
    'سرعة الانهيار: Vs = √(2W / (ρ·S·CLmax)) = ' + f1(c.stall) + ' م/ث (' + f0(c.stall * 3.6) + ' كم/س). سرعة الطيران المريحة = 1.3×Vs = ' + f1(c.vc) + ' م/ث.',
    'السحب: D = ½ρV²·S·(CD0 + k·CL²) مع k = 1/(π·e·AR) = ' + c.k.toFixed(3) + ' و CD0·S = CdA = ' + c.CdA.toFixed(2) + ' م² (جسم + حقيبة + جناح). عند ' + f1(c.vc) + ' م/ث: CL = ' + c.CLc.toFixed(2) + ' والسحب D ≈ ' + f0(c.Dc) + ' نيوتن.',
    'أفضل نسبة انزلاق: L/D = 1/(2√(CD0·k)) = ' + f1(c.ld) + '. عند توقف المحرك من ارتفاع 100 م تنزلق ≈ ' + f0(c.ld * 100) + ' م أفقياً.',
    'الدفع الأقصى (نظرية الزخم): T = (η·P·√(2ρA))^(2/3) = ' + f0(c.Tn) + ' نيوتن (' + f0(c.Tn / GRAV) + ' كغ دفع) لقدرة ' + f0(c.kw) + ' kW ومروحة قطرها ' + c.D + ' م (A = ' + c.A.toFixed(2) + ' م²). نسبة الدفع/الوزن = ' + c.twr.toFixed(2) + '.',
    'قدرة الطيران الأفقي: P = D·V/(ηp·ηm) = ' + f0(c.Dc) + '×' + f1(c.vc) + '/0.63 ≈ ' + f1(c.Pc / 1000) + ' kW.',
    'الطاقة: E = ' + S.battery.s + 'S × 3.7 فولت × ' + (S.battery.mah / 1000) + ' أمبير·ساعة = ' + f0(c.whNom) + ' واط·ساعة (المستخدم 80% = ' + f0(c.whUse) + '). زمن الطيران = E/P ≈ ' + f1(c.timeMin) + ' دقيقة، والمدى ≈ ' + f1(c.range) + ' كم.',
    'معدل الصعود = (T − D)·V / W = (' + f0(c.Tn) + ' − ' + f0(c.Dc) + ')×' + f1(c.vc) + ' / ' + f0(c.Wn) + ' ≈ ' + f1(c.roc) + ' م/ث. التيار الأقصى = P/V = ' + f0(c.amps) + ' أمبير.'
  ];
  const table = [];
  const gearNoWing = c.gearKg - c.wingKg;
  [50, 60, 70, 80, 90, 100, 120].forEach(bk => {
    let wk = 6, r = null, M = 0;
    for (let i = 0; i < 8; i++){ M = bk + gearNoWing + wk; r = recWing(M, 1.3); wk = wingMassKg(r.S); }
    table.push(bk + ' كغ ← كتلة كلية ' + f0(M) + ' كغ ← باع ' + f1(r.b) + ' م ومساحة ' + f1(r.S) + ' م² (سرعة انهيار ' + AUTO_STALL + ' م/ث)');
  });
  const steps = [
    'التحضير: اطبع مخطط الحقيبة والجناح بالمقاس الحقيقي، وزّن كل قطعة وقارنها بالقائمة. اختبر المحرك والـ ESC والبطارية على طاولة اختبار مثبّتة بدون مروحة.',
    'الحقيبة والحزام: هيكل كربون/ألمنيوم خفيف بمبطّن ظهر وحزام صدر وخصر وساقين (Harness) مصمم لتحمل أحمال أكبر من 6 أضعاف وزنك. ضع الأثقال قرب مركز الثقل.',
    'الجناح (' + f1(c.b) + ' م): هيكل عارضة كربون مزدوجة مع أضلاع فوم وغلاف خفيف، ينقسم لنصفين يُطويان داخل الحقيبة (طول مطوي ~' + c.fold.toFixed(1) + ' م). اضبط زاوية سقوط ~3° وارتفاع نهايات الجناحين (Dihedral) ~3° للثبات، ثم قفل مركزي مزدوج.',
    (S.wing.flap ? 'ميكانيزم الرفرفة: ثبّت مفصلاً عند كل كتف وذراع رفرفة (كرنك) متصلاً بعلبة تروس بنسبة ~1:25 يحركها المحرك أو محرك مساعد، بتردد 1-3 هرتز وسعة ±20°. افحص التوازن الديناميكي واهتزاز الحقيبة قبل أي طيران، وأضف حداً ميكانيكياً لمنع تجاوز زاوية الرفرفة.' : 'قفل الجناح: استخدم قفلاً مركزياً مزدوجاً بمقبض طوارئ لفكّ الجناح بسرعة عند الحاجة.'),
    'الجنيحات: ركّب ' + 2 + ' سيرفو عالي العزم (' + S.servo.n + ') على الحافة الخلفية للتحكم بالميلان والارتفاع (Flaperons).',
    'المحرك والمروحة: ثبّت المحرك على عمود كربون خلف القدمين بحيث يكون محور الدفع قريباً من مركز الثقل. بين المروحة والقدمين مسافة آمنة (>0.3 م) ومروحة محاطة بحلقة حماية إن أمكن.',
    'الكهرباء: وصّل البطارية (' + S.battery.n + ') بالـ ESC عبر فيوز رئيسي وموصل QS8/XT90 ومفتاح قطع طوارئ بحبل يُسحب بالقبضة. ثبّت البطارية في جيب معزول حرارياً بعيداً عن ظهرك.',
    'متحكم الطيران: ثبّته قرب مركز الثقل والسهم نحو الأمام، عاير الجيروسكوب، وفعّل وضع الثبات (Angle) وعتبة أمان للقدرة المنخفضة.',
    'المظلة الاحتياطية: اطوِ المظلة في جيبها العلوي مع مقبض سهل المنال. اختبر آلية الفتح على الأرض مراراً قبل أي طيران.',
    'مركز الثقل: اضبط توزيع الأحمال بحيث تكون الحقيبة متوازنة عند التعليق من الحزام (انزلاق البطارية أماماً/خلفاً).',
    'الاختبارات: أرضية بدون مروحة، ثم اختبار دفع مربوط بحبل مع قياس التيار، ثم انزلاق بدون محرك من تل منخفض مع مدرب، ثم القدرة تدريجياً.'
  ];
  const tools = ['مكواة لحام قوية ولاحم بالقصدير للأسلاك السميكة', 'كمّاشة ضغط موصلات وقاطع أسلاك ثقيل', 'ميزان رقمي ومقياس دفع (Thrust stand)', 'ملتيميتر وأمبيرمتر بكماشة (Clamp meter)', 'مفاتيح سداسية ولوكتايت', 'ماكينة خياطة صناعية لتصنيع الحزام والجيوب', 'شاحن بطاريات بالتوازن + حقيبة LiPo مقاومة للنار', 'طفاية حريق مناسبة للبطاريات بجوار منطقة الشحن'];
  const safety = [
    'هذا تصميم تعليمي ومحاكاة. لا تبنِ ولا تطر بمعدات حقيقية دون مدرب مرخّص وتدريب كافٍ وتصاريح الطيران المحلية.',
    'المظلة الاحتياطية إلزامية: ارتفاع الفتح الآمن ' + (S.chute.minAlt || 100) + ' م على الأقل. تدرّب على فتحها قبل الطيران.',
    'مفتاح قطع الطوارئ بمتناول اليد دائماً، وحماية للمروحة حتى لا تقترب منها الأطراف أو الأحزمة.',
    'بطاريات ' + S.battery.chem + ' عالية السعة خطرة: اشحنها داخل كيس/صندوق مقاوم للنار ولا تتركها دون مراقبة، ولا تنزل عن ' + (S.battery.vmin || 3.5).toFixed(1) + ' فولت لكل خلية (' + (S.battery.s * (S.battery.vmin || 3.5)).toFixed(0) + ' فولت للحزمة).',
    'ارتدِ خوذة ودرعاً للظهر وملابس واقية، وتدرّب فوق أرض عشبية أو ماء بوجود فريق إنقاذ.'
  ];
  const tests = [
    'وزن المعدات النهائي يطابق القائمة (±5%) والحقيبة متزنة عند التعليق.',
    'اتجاه دوران المروحة صحيح والدفع باتجاه الأمام، واختبار مفتاح القطع.',
    'اختبار الدفع المربوط: الدفع ≥ ' + f0(c.Tn / GRAV * .9) + ' كغ والتيار ≤ ' + f0(c.amps) + ' أمبير.',
    'اختبار انفتاح المظلة وآلية فك الجناح بسهولة عند الطوارئ.',
    'أول طيران بالمحاكاة: ركض أو منحدر، ثم ثروتل 60-70% وارفع الأنف تدريجياً، وتدرب على تعطل المحرك وفتح المظلة.'
  ];
  return {explain, steps, tools, safety, tests, math, table};
}
function localGuide(c){
  if (c.isHuman) return humanGuide(c);
  const t = c.type, S = c.sel, quad = c.isQuad;
  const cells = c.sel.battery.s, vmin = c.sel.battery.vmin || 3.5, chem = c.sel.battery.chem;
  const explain = quad
    ? 'كوادكوبتر بأربع محركات: ترتفع بقوة الدفع فقط (TWR = ' + c.twr.toFixed(2) + ') ويتولى متحكم الطيران الثبات. الوزن ' + Math.round(c.mass) + 'g وزمن الطيران المقدر ~' + c.timeMin.toFixed(0) + ' دقيقة.'
    : (t === 'wing' ? 'جناح طائر بلا ذيل: التحكم بسيرفوهين (Elevons). ' : 'طائرة بجناح وذيل: ') + 'الوزن ' + Math.round(c.mass) + 'g، سرعة الانهيار ~' + Math.round(c.stall * 3.6) + ' km/h، وزمن الطيران ~' + c.timeMin.toFixed(0) + ' دقيقة.';
  const tools = ['مكواة لحام + قصدير + فلكس', 'مسدس غراء حراري وغراء سيانو (CA) ومنشط', 'سكين هوايات (X-Acto) وقاعدة قص', 'مفكات سداسية وفيليبس', 'ملتيميتر لفحص التوصيلات', 'ميزان رقمي دقيق (0.1g)', 'شاحن LiPo متوازن + كيس أمان للبطاريات', 'أنبوب انكماش حراري وأربطة كيبل', 'شريط لاصق قوي (تيسا/فيلامنت) للمفصلات'];
  const steps = [];
  steps.push('التحضير: اطبع/ارسم المخطط بالمقاس الحقيقي، ووزّن كل قطعة وسجّل الأوزان وقارنها بالقائمة. اختبر المحرك والـ ESC والمستقبل على الطاولة قبل أي تركيب.');
  if (quad){
    steps.push('الإطار: اربط الأذرع الأربعة بالصفيحة المركزية بمسامير مع Loctite أزرق. تأكد أن المسافة بين المحركات متساوية والإطار مستوٍ بلا التواء.');
    steps.push('المحركات: ثبّت 4 محركات على أطراف الأذرع بمسامير قصيرة (لا تلمس اللفائف الداخلية). حدد اتجاه الدوران: اثنان CW واثنان CCW بالتبادل القطري.');
    steps.push('اللحام: لحّم أسلاك كل محرك بالـ ESC (3 أسلاك، ويمكن تبديل أي سلكين لعكس الاتجاه). لحّم مدخل البطارية XT60 بلوحة التوزيع. غلّف كل وصلة بأنبوب انكماش.');
    steps.push('متحكم الطيران: ثبّته في مركز الإطار على وسائد اهتزاز (foam) والسهم نحو الأمام. وصّل إشارات الـ ESC الأربعة بالترتيب الصحيح حسب مخطط البرنامج (Betaflight/ArduPilot).');
  } else {
    steps.push(t === 'wing'
      ? 'الهيكل والجناح: قص الجناح من الفوم (EPP أو EPS) بالمقطع المطلوب وقوّه بعارضة كربون طولية بقطر 6مم داخل الجناح، ثم الصق الهيكل المركزي. الجناح الطائر يحتاج انحناء/تواء خفيف (washout) عند الأطراف للثبات.'
      : 'الهيكل: قص الأجزاء من الفوم أو البلسا ثم اغراء أجزاء الهيكل. اترك مكاناً للبطارية في المقدمة لضبط التوازن، وغطّ الحواف بشريط لتقوية الصدمات.');
    steps.push('الجناح: ثبّته بزاوية سقوط (incidence) موجبة ~2° وزاوية ميل للأعلى (dihedral) ~2-3° لثبات الميلان. للجناح الكبير ركّب عارضة كربون (spar) طولية وأعد التحقق من التماثل بين الجهتين.');
    if (t === 'plane') steps.push('الذيل: ثبّت المثبت الأفقي (Stabilizer) مستوياً وعمودياً على الزعنفة. اربط المصعد والدفة بمفصلات شريط لاصق على الجهة العليا والسفلى ثم تحقق من الحركة الحرة بلا احتكاك.');
    steps.push('المحرك: ثبّت الحامل (motor mount) على مقدمة الهيكل مع زاوية دفع لأسفل ~2° ولليمين ~2° لمقاومة عزم الدوران. استخدم Loctite وراقب أن لا تلمس البراغي لفائف المحرك.');
    steps.push('الـ ESC والبطارية: لحّم موصلات bullet 3.5mm بين المحرك والـ ESC، وXT60 بين الـ ESC والبطارية. ثبّت الـ ESC في مجرى هواء للتبريد. صل سلك BEC/الإشارة بقناة الثروتل في المستقبل.');
    steps.push('السيرفو: ركّب ' + c.nServo + ' سيرفو ووصّل كل منها بسطح التحكم بقضيب (pushrod) مع clevis. اجعل الذراع عند الحياد 90° والسطح مستوياً، ثم اضبط التقييد (end points) وعكس الاتجاه في جهاز التحكم.');
  }
  if (S.fc.stabil > 0) steps.push('متحكم الطيران (' + S.fc.n + '): ثبّته بعيداً عن المحرك والـ ESC (مصدر ضجيج)، السهم نحو الأمام. أجرِ معايرة الجيروسكوب على سطح مستوٍ، واضبط أوضاع الطيران (Stabilize/Angle)' + (S.fc.gps ? '، وفعّل RTH بعد انتظار تثبيت أقمار GPS 8+.' : '.'));
  steps.push('المستقبل والتحكم: اربط (Bind) المستقبل بالجهاز، واضبط الـ Failsafe بحيث يقطع الثروتل أو يعيد للمنزل عند فقدان الإشارة. ثبّت الهوائيات بعيداً عن الكربون والمعادن وبزاوية 90° بينهما.' + (S.cam.w ? ' ثبّت الكاميرا في المقدمة وتأكد أنها لا تغيّر التوازن.' : ''));
  if (!quad) steps.push('مركز الثقل (CG): اضبط البطارية أمامية/خلفية حتى تتوازن الطائرة بإصبعين على ~25-33% من وتر الجناح (قياس من الحافة الأمامية). الطائرة المائلة للأنف قليلاً أسلم من الذيلية الثقل.');
  steps.push('المراوح: وازن المروحة (Prop balancer) وركّبها في الآخر فقط، بعد اختبار الدوران. تأكد أن الجهة المنحنية متجهة للأمام ومحكمة الشد.');
  steps.push('الاختبارات الأرضية (انظر القائمة بالأسفل) ثم أول طيران في طقس هادئ.');
  const safety = [
    'لا توصّل البطارية والمروحة مركّبة أثناء التجارب على الطاولة.',
    'بطاريات ' + chem + ': اشحنها داخل كيس أمان، لا تتركها تُشحن دون مراقبة، ولا تفرغها أقل من ' + vmin.toFixed(1) + 'V لكل خلية (' + cells + 'S: لا تنزل عن ~' + (cells * vmin).toFixed(1) + 'V).',
    'ارتدِ نظارات واقية عند اللحام واختبار المحرك، وابعد الأيدي عن مستوى المروحة.',
    'تحقق من قوانين الطيران المحلية ومتطلبات التسجيل، وطِر بعيداً عن المطارات والتجمعات والمباني.'
  ];
  const tests = [
    'وزن الطائرة النهائي يطابق الحساب (±5%) ومركز الثقل في موضعه.',
    'اتجاه كل سطح تحكم صحيح (ميل العصا يميناً = الجناح الأيمن لأسفل).',
    'المحرك يدور بالاتجاه الصحيح وبلا اهتزاز.',
    'اختبار المدى: سر 30 خطوة والهوائي منخفض والإشارة ثابتة.',
    'اختبار الـ Failsafe: أطفئ جهاز التحكم وتأكد من استجابة الطائرة كما تم ضبطها.',
    'أول طيران: ' + (quad ? 'تحويم على ارتفاع 1م لدقيقة، ثم زد تدريجياً.' : 'إقلاع بالتوجه عكس الريح، ثروتل 70%، صعود تدريجي، واضبط الـ trim ثم اهبط بعد 2-3 دقائق.')
  ];
  return {explain, steps, tools, safety, tests};
}

function listHtml(tag, arr){ return '<' + tag + '>' + arr.map(x => '<li></li>').join('') + '</' + tag + '>'; }
function fillList(tag, arr){
  const el = document.createElement(tag);
  arr.forEach(x => { const li = document.createElement('li'); li.textContent = x; el.appendChild(li); });
  return el;
}
function showGuide(ai){
  const local = localGuide(cfg), body = $('guide-body'); body.innerHTML = '';
  const add = (title, node) => { const h = document.createElement('h3'); h.textContent = title; body.appendChild(h); body.appendChild(node); };
  const p = document.createElement('p'); p.textContent = (ai && ai.explanation) ? ai.explanation : local.explain; body.appendChild(p);
  if (ai && ai.explanation){ const p2 = document.createElement('p'); p2.textContent = local.explain; body.appendChild(p2); }
  add('🔧 خطوات التصنيع', fillList('ol', (ai && Array.isArray(ai.steps) && ai.steps.length) ? ai.steps.map(String) : local.steps));
  if (local.math) add('📐 الحسابات الرياضية', fillList('ul', local.math));
  if (local.table) add('📏 باع الجناح الموصى به حسب الوزن', fillList('ul', local.table));
  if (ai && Array.isArray(ai.tips) && ai.tips.length) add('💡 نصائح المهندس', fillList('ul', ai.tips.map(String)));
  add('🧰 الأدوات المطلوبة', fillList('ul', local.tools));
  add('🦺 السلامة', fillList('ul', local.safety));
  add('✅ قائمة الفحص قبل الطيران', fillList('ul', local.tests));
  $('guide-modal').style.display = 'flex';
}

/* ======================= شريط الأدوات ======================= */
$('t-guide').addEventListener('click', () => showGuide(null));
$('t-bom').addEventListener('click', showBom);
$('t-reset').addEventListener('click', resetState);
$('t-launch').addEventListener('click', () => {
  setLaunch(launchMode === 'slope' ? 'ground' : 'slope'); resetState();
  flash(launchMode === 'slope' ? '⛰️ إقلاع من منحدر ارتفاعه 25 م' : '🏃 إقلاع بالركض (حتى 9 م/ث)', 1800);
});
$('t-chute').addEventListener('click', () => {
  if (!cfg.isHuman || stage !== 'fly' || state.chute || state.crashed) return;
  if (!cfg.sel.chute.w){ flash('⛔ لا توجد مظلة احتياطية في تصميمك!', 2200); return; }
  if (state.alt < 3){ flash('أنت على الأرض بالفعل', 1200); return; }
  state.chute = 1; state.chuteT = 0; setThrottle(0);
  const lo = cfg.sel.chute.minAlt;
  // الفتح تحت الارتفاع الآمن: المظلة لا تنفتح بالكامل فيزداد معدل الهبوط (5.5 م/ث عادةً)
  state.chuteVT = -5.5 - 6 * Math.max(0, 1 - state.alt / lo);
  flash(state.alt < lo ? '⚠️ ارتفاع منخفض: الحد الآمن لفتح هذه المظلة ' + lo + ' م، قد لا تنفتح بالكامل' : '🪂 فُتحت المظلة', 2200);
});
$('t-cam').addEventListener('click', () => {
  camView = (camView + 1) % 3; flash('🎥 كاميرا ' + CAM_NAMES[camView], 1200);
});
$('t-fail').addEventListener('click', () => {
  if (!cfg.isHuman || stage !== 'fly') return;
  state.engineOut = state.engineOut ? 0 : 1;
  $('t-fail').classList.toggle('on', !!state.engineOut);
  flash(state.engineOut ? '⛔ تعطل المحرك! انزلق نحو منطقة هبوط أو افتح المظلة' : '✅ عاد المحرك للعمل', 2200);
});

/* ======================= مهندس الطيران AI ======================= */
const aiBtn = $('ai-btn'), aiResult = $('ai-result');
aiBtn.addEventListener('click', () => {
  const q = $('ai-input').value.trim(); if (!q) return;
  aiResult.style.display = 'block';
  if (!(window.Android && window.Android.askAi)){ aiResult.textContent = 'خاصية AI تعمل داخل التطبيق فقط. يمكنك استخدام زر الدليل المحلي.'; return; }
  aiResult.textContent = 'جاري التصميم وكتابة دليل التصنيع...';
  const prompt = 'أنت مهندس طيران ومعلم للمبتدئين. المستخدم يطلب: "' + q + '". اختر أفضل قطع للطائرة، واشرح لماذا، واكتب خطوات تصنيع واقعية ونصائح.\n' +
    'الخيارات المتاحة (استخدم المفاتيح الإنجليزية فقط):\n' +
    '- frame: plane, wing, cargo, quad, human\n- wing: trainer, glider, sport, big (تُهمل للكوادكوبتر)\n- tail: conv, vtail, none\n' +
    '- battery (عدد الخلايا S بين قوسين): 1s(1), 2s(2), 2s22(2), 3s(3), 3s22(3), 3s30(3), 3sli(3 Li-ion تيار ضعيف), 4s(4), 4s15r(4 سباق), 4s33(4), 4s50(4), 4sli(4 Li-ion تيار ضعيف), 6s(6), 6s80(6), 3s13r(3 سباق), 4s13r(4 سباق 100C), 4s22r(4), 4s40(4), 6s13r(6 سباق), 6s30(6), 6s10k(6 ثقيلة)\n- motor (الخلايا المسموحة): micro(1-2), small(2-3), sport(3-4), medium(3-4), high(3-5), large(4-6), xl(5-6), xxl(6), q1806(3-4), q2205(3-4), q2306(4-6), q2810(4-6), q4108(4-6) [الأخيرة 5 مخصصة للدرونات]\n- prop: small, medium, large, xl, q5, q7, q10\n- esc: e6, e10, e20, e30, e35, e40, e50, e60, e80, e100, e120\n- servo: s9, s17\n' +
    '- fc: none, gyro, gps\n- rc: r24, r58, r4g\n- cam: none, fpv, hd\n' +
    '- لو اخترت frame=human (إنسان بجناح بالحقيبة) استخدم هذه المفاتيح بدل القوائم السابقة للجناح والمحرك والمروحة وESC والبطارية، وأضف حقل body على مستوى JSON بوزن الشخص بالكغ كرقم: wing: auto (ثابت),flap (مرفرف, أثقل وأقل كفاءة),hw3,hw4,hw5,hw6,hw8 | motor: hm6,hm12,hm20,hm30 | prop: hp08,hp10,hp12,hp15 | esc: he150,he200,he300,he400,he500 | battery: hb1,hb2,hb3,hb4,hb5,hb6,hb7 | chute: basic,ballistic (إلزامية) | servo,fc,rc,cam كما هي. يجب أن تكون سرعة الانهيار أقل من 13 م/ث، والدفع أكبر من 0.35 من الوزن الكلي، والـ ESC أكبر من التيار الأقصى بـ 15%.\n' +
    'قواعد: ESC أكبر من تيار المحرك بـ20%، والبطارية تتحمل التيار، وعدد خلايا البطارية ضمن المسموح للمحرك، وTWR للطائرة ≥ 0.5 وللكوادكوبتر ≥ 1.5.\n' +
    'أعد JSON فقط بدون markdown أو أي كلام إضافي بهذا الشكل:\n' +
    '{"parts":{"frame":"plane","wing":"trainer","tail":"conv","battery":"3s","motor":"medium","prop":"small","esc":"e30","servo":"s9","fc":"gyro","rc":"r24","cam":"none"},' +
    '"explanation":"شرح بسيط لسطرين","steps":["الخطوة 1...","الخطوة 2..."],"tips":["نصيحة 1","نصيحة 2"]}';
  window.Android.askAi('flight_engineer', prompt);
});

window.onAiResult = function(id, ok, text){
  if (id !== 'flight_engineer') return;
  if (!ok){ aiResult.textContent = 'خطأ: ' + text; return; }
  let data = null;
  try {
    const a = text.indexOf('{'), b = text.lastIndexOf('}');
    data = JSON.parse(text.slice(a, b + 1));
  } catch (e) { data = null; }
  if (data && data.parts){
    const fv = data.parts.frame;
    if (fv && PARTS.frame[fv]) $('sel-frame').value = fv;
    syncMode();
    const bd = +(data.body || data.parts.body);
    if (bd >= 40 && bd <= 150){
      const bs = $('sel-body'); let best = bs.options[0].value, dmin = 1e9;
      Array.from(bs.options).forEach(o => { const d = Math.abs(+o.value - bd); if (d < dmin){ dmin = d; best = o.value; } });
      bs.value = best;
    }
    SLOTS.forEach(([k]) => {
      const v = data.parts[k], cat = partsFor(k);
      if (k !== 'frame' && v && cat[v]){ $('sel-' + k).value = v; saved[curMode][k] = v; }
    });
    updatePlane();
    aiResult.textContent = 'تم تجهيز الطائرة ودليل التصنيع!';
    showGuide(data);
  } else {
    aiResult.textContent = 'تعذّر فهم رد AI، عرضنا الدليل المحلي.';
    showGuide(null);
  }
};

/* ======================= الحلقة الرئيسية ======================= */
updatePlane('frame');
info.style.display = 'none';
let last = performance.now();
function loop(){
  requestAnimationFrame(loop);
  let dt = (performance.now() - last) / 1000; last = performance.now();
  if (dt > .05) dt = .05;
  if (stage === 'fly') step(dt); render(dt);
}
addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });
loop();
</script>
</body>
</html>'''

os.makedirs("app/src/main/assets", exist_ok=True)
with open("app/src/main/assets/flight_sim.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# ---------------------------------------------------------------------------
# 2) FlightSimActivity.kt
#    - JSONObject.quote for safe JS escaping (quotes, newlines, unicode separators)
#    - coroutine scope cancelled in onDestroy
#    - back button goes back inside the WebView first
# ---------------------------------------------------------------------------
activity_content = r'''package com.zevorix.assistant

import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
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

class FlightSimActivity : ComponentActivity() {
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
                                addJavascriptInterface(Bridge(this, aiService, scope), "Android")
                                loadUrl("file:///android_asset/flight_sim.html")
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
        private val webView: WebView,
        private val aiService: AiChatService,
        private val scope: CoroutineScope
    ) {
        @JavascriptInterface
        fun askAi(id: String, prompt: String) {
            scope.launch {
                val lang = if (prompt.any { it in '\u0600'..'\u06FF' })
                    com.zevorix.assistant.viewmodel.AppLanguage.ARABIC
                else com.zevorix.assistant.viewmodel.AppLanguage.ENGLISH
                val result = aiService.ask(prompt, lang)
                withContext(Dispatchers.Main) {
                    val idJs = JSONObject.quote(id)
                    when (result) {
                        is AiResult.Success -> {
                            webView.evaluateJavascript(
                                "window.onAiResult($idJs, true, ${JSONObject.quote(result.text)});", null)
                        }
                        is AiResult.Error -> {
                            val msg = "Error: ${result.kind} ${result.detail}"
                            webView.evaluateJavascript(
                                "window.onAiResult($idJs, false, ${JSONObject.quote(msg)});", null)
                        }
                    }
                }
            }
        }
    }
}
'''

with open(PKG_DIR + "/FlightSimActivity.kt", "w", encoding="utf-8") as f:
    f.write(activity_content)

# 3) تسجيل النشاط في AndroidManifest.xml
register_activity("FlightSimActivity")

# 4) القائمة الجانبية: لا يتم تعديل MainScreen.kt هنا.
#    menu_items_patch.py هو المصدر الوحيد لإدراج عنصر القائمة.

print(">> Flight Lab v2 + side drawer + extended parts + human wingpack applied (activity + html + manifest). Menu item: menu_items_patch.py")

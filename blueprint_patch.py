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

print(">> Applying Flight Lab v2 patch (parts catalog + build guide + flight physics)...")

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
#hud{position:absolute;top:44px;right:8px;z-index:2;padding:6px 10px;font-family:monospace;font-size:.78rem;text-align:right;pointer-events:none;line-height:1.35;max-width:46vw}
#hud .val{color:var(--accent);font-weight:bold}.warn{color:var(--warn);font-weight:bold}.good{color:var(--good);font-weight:bold}
#hud hr{border:0;border-top:1px solid #333;margin:4px 0}
#toolbar{position:absolute;top:6px;left:6px;right:6px;z-index:3;display:flex;gap:6px;justify-content:center}
.tbtn{padding:7px 10px;background:var(--panel);border:1px solid var(--border);color:var(--text);border-radius:8px;font-size:.8rem;cursor:pointer}
#builder-panel{position:absolute;top:44px;left:8px;z-index:2;padding:8px;display:flex;flex-direction:column;gap:5px;width:200px;max-height:58vh;overflow-y:auto}
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
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="toolbar">
  <div class="tbtn" id="t-parts">🧩 القطع</div>
  <div class="tbtn" id="t-guide">📘 دليل التصنيع</div>
  <div class="tbtn" id="t-bom">📋 القائمة والتكلفة</div>
  <div class="tbtn" id="t-reset">↺ إعادة</div>
</div>

<div id="hud" class="panel">
  السرعة: <span class="val" id="hud-speed">0</span> km/h<br>
  الارتفاع: <span class="val" id="hud-alt">0</span> m<br>
  البعد: <span class="val" id="hud-dist">0</span> m<br>
  <hr>
  الوزن: <span class="val" id="hud-weight">0</span> g<br>
  الدفع: <span class="val" id="hud-thrust">0</span> g<br>
  TWR: <span id="hud-twr">0</span><br>
  <span id="row-wl">تحميل الجناح: <span class="val" id="hud-wl">0</span> g/dm²<br>
  سرعة الانهيار: <span class="val" id="hud-stall">0</span> km/h<br></span>
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
    quad:  {n:'كوادكوبتر (درون)', w:300, c:40, type:'quad', cd:.08, d:'4 محركات ومراوح، بلا جناح ولا ذيل. تحلق وتحوم في مكانها لكنها تحتاج متحكم طيران إلزامياً في الواقع.'}
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
    '2s':{n:'2S 1000mAh', w:70,  c:10, mah:1000, cmax:20, d:'7.4V: خفيفة للطائرات الصغيرة جداً.'},
    '3s':{n:'3S 1500mAh', w:130, c:18, mah:1500, cmax:25, d:'11.1V: التوازن الأفضل للمبتدئين.'},
    '4s':{n:'4S 2200mAh', w:250, c:32, mah:2200, cmax:30, d:'14.8V: قدرة أعلى وزمن أطول، وزنها أكبر.'},
    '6s':{n:'6S 5000mAh', w:650, c:80, mah:5000, cmax:25, d:'22.2V: للطائرات الثقيلة والمحركات الكبيرة.'}
  },
  motor: {
    small: {n:'محرك صغير (200g)',  w:30,  c:10, t:200,  a:10, d:'Brushless outrunner صغير. مناسب لطائرات حتى ~400g.'},
    medium:{n:'محرك متوسط (800g)', w:60,  c:22, t:800,  a:25, d:'الخيار العام: يرفع طائرات ~1.2-1.6kg.'},
    large: {n:'محرك كبير (2000g)', w:120, c:45, t:2000, a:50, d:'قدرة كبيرة للشحن أو الكوادكوبتر الثقيل. يستهلك تياراً عالياً.'}
  },
  prop: {
    small:{n:'مروحة صغيرة', w:10, c:3, tm:.8,  am:.7,  d:'تيار أقل وسرعة أعلى، دفع ثابت أقل.'},
    large:{n:'مروحة كبيرة', w:25, c:6, tm:1.2, am:1.3, d:'دفع أعلى عند الإقلاع، تستهلك تياراً أكبر.'}
  },
  esc: {
    e10:{n:'ESC 12A', w:8,  c:8,  a:12, d:'متحكم السرعة: يحول البطارية إلى 3 أطوار للمحرك. اختره دائماً أكبر من تيار المحرك بـ 20% على الأقل.'},
    e30:{n:'ESC 30A', w:25, c:15, a:30, d:'مناسب للمحرك المتوسط.'},
    e60:{n:'ESC 60A', w:45, c:28, a:60, d:'للمحركات الكبيرة. يفضل تبريده بتيار الهواء.'}
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
  }
};
const SLOTS = [['frame','الهيكل'],['wing','الجناح'],['tail','الذيل'],['battery','البطارية'],['motor','المحرك'],
  ['prop','المروحة'],['esc','متحكم السرعة ESC'],['servo','السيرفو'],['fc','متحكم الطيران'],['rc','التحكم عن بعد'],['cam','الكاميرا']];

/* ======================= واجهة البناء ======================= */
const bp = $('builder-panel');
SLOTS.forEach(([k,label]) => {
  const row = document.createElement('div'); row.className = 'row';
  const lab = document.createElement('label'); lab.textContent = label;
  const sel = document.createElement('select'); sel.id = 'sel-' + k;
  Object.keys(PARTS[k]).forEach(key => {
    const p = PARTS[k][key], o = document.createElement('option');
    o.value = key; o.textContent = p.n + (p.w ? ' (' + p.w + 'g · $' + p.c + ')' : '');
    sel.appendChild(o);
  });
  sel.addEventListener('change', () => updatePlane(k));
  row.appendChild(lab); row.appendChild(sel); bp.appendChild(row);
});
const info = document.createElement('div'); info.id = 'part-info'; bp.appendChild(info);
$('sel-battery').value = '3s'; $('sel-motor').value = 'medium'; $('sel-esc').value = 'e30';
$('sel-prop').value = 'small'; $('sel-wing').value = 'trainer'; $('sel-fc').value = 'gyro';

function showInfo(slot){
  const p = PARTS[slot][$('sel-' + slot).value];
  if (p && p.d){ info.style.display = 'block'; info.textContent = 'ℹ️ ' + p.d; } else info.style.display = 'none';
}

/* ======================= حسابات التصميم ======================= */
let cfg = null;
function compute(){
  const sel = {}; SLOTS.forEach(([k]) => sel[k] = PARTS[k][$('sel-' + k).value]);
  const fr = sel.frame, type = fr.type, isQuad = type === 'quad';
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
  const thrust = sel.motor.t * sel.prop.tm * nMot;
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

function buildModel(c){
  while (planeGroup.children.length) planeGroup.remove(planeGroup.children[0]);
  spinners = [];
  const big = c.sel.prop === PARTS.prop.large;
  if (c.isQuad){
    box(1.2, .4, 1.2, 0x333333, 0, 0, 0);
    const a1 = box(5.2, .14, .28, 0x666666, 0, 0, 0); a1.rotation.y = Math.PI / 4;
    const a2 = box(5.2, .14, .28, 0x666666, 0, 0, 0); a2.rotation.y = -Math.PI / 4;
    [[1.85,1.85],[-1.85,1.85],[1.85,-1.85],[-1.85,-1.85]].forEach(([x,z], i) => {
      const mo = new THREE.Mesh(new THREE.CylinderGeometry(.22, .22, .3, 10), M(0x222222)); mo.position.set(x, .2, z); planeGroup.add(mo);
      const pr = box(1.5, .03, .12, i % 2 ? 0xff5533 : 0x35d0ff, x, .4, z); spinners.push({m:pr, axis:'y', dir:i % 2 ? 1 : -1});
    });
    box(.7, .25, .5, 0xffcc00, 0, -.3, 0);
    if (c.sel.cam.w) box(.25, .25, .25, 0x111111, 0, -.1, .7);
    return;
  }
  const isWing = c.type === 'wing', cargo = c.fr === PARTS.frame.cargo;
  const L = isWing ? 2.4 : (cargo ? 7 : 5.2), R = cargo ? .8 : (isWing ? .35 : .4);
  const fus = new THREE.Mesh(new THREE.CylinderGeometry(R, R * .6, L, 10), M(isWing ? 0xdddddd : (cargo ? 0x7a7a7a : 0xd0d4dc)));
  fus.rotation.x = Math.PI / 2; planeGroup.add(fus);
  const span = Math.max(3, c.S * 18), chord = isWing ? 1.9 : 1.1;
  const wing = box(span, .12, chord, isWing ? 0xe8e8ee : 0xeeeeee, 0, .05, isWing ? -.3 : .4);
  if (isWing){ box(.1, .8, .8, 0xff9f1c, span / 2 - .1, .4, -.9); box(.1, .8, .8, 0xff9f1c, -span / 2 + .1, .4, -.9); }
  if (c.type === 'plane'){
    const tz = -L / 2 + .3;
    if (c.sel.tail === PARTS.tail.conv){
      box(span * .38, .1, .7, 0xeeeeee, 0, .1, tz);
      box(.1, 1.1, .8, 0xff9f1c, 0, .6, tz);
    } else if (c.sel.tail === PARTS.tail.vtail){
      const a = box(.1, 1.3, .7, 0xff9f1c, .55, .55, tz); a.rotation.z = -.6;
      const b = box(.1, 1.3, .7, 0xff9f1c, -.55, .55, tz); b.rotation.z = .6;
    }
  }
  if (c.sel.battery.w >= 250) box(.5, .3, 1, 0xffcc00, 0, -R, .2);
  if (c.sel.cam.w) box(.25, .25, .3, 0x111111, 0, -R - .1, L / 2 - .6);
  const pr = box(big ? 2.4 : 1.7, .08, .14, 0x222222, 0, 0, L / 2 + .15); spinners.push({m:pr, axis:'z', dir:1});
  const nose = new THREE.Mesh(new THREE.CylinderGeometry(.12, .12, .25, 8), M(0xaaaaaa)); nose.rotation.x = Math.PI / 2; nose.position.set(0, 0, L / 2 + .05); planeGroup.add(nose);
}

/* ======================= الحالة والتحكم ======================= */
let state = {};
function resetState(){
  state = {speed:0, vz:0, alt:0, x:0, z:0, heading:0, throttle:0, pitch:0, roll:0, pitchIn:0, rollIn:0, battery:100, crashed:0, t:0, drift:0};
  planeGroup.position.set(0, .5, 0);
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
  const thr = linked ? s.throttle : 0;
  const T = c.thrust * thr * g / 1000 * (.8 + .2 * s.battery / 100);
  const stabil = c.sel.fc.stabil;

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
    const instab = (c.type === 'plane' && c.sel.tail.stab === 0 ? 1 : 0) * (1 - stabil) + (c.type === 'wing' ? .35 * (1 - stabil) : 0);
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
    const az = (L * Math.cos(s.roll * Math.PI / 180) - W) / m;
    if (grounded && az < 0) s.vz = 0; else { s.vz += az * dt; }
    s.vz *= Math.exp(-.8 * dt);
    const impact = s.vz;
    s.alt += s.vz * dt;
    if (s.alt < 0){
      if (impact < -4 || (s.speed > c.stall * 2.2 && impact < -2.5)){ s.crashed = 2.2; flash('💥 تحطمت الطائرة! ← اهبط بنعومة وبسرعة منخفضة', 2200); }
      s.alt = 0; s.vz = 0;
    }
    if (s.alt > .5) s.heading -= g * Math.tan(s.roll * Math.PI / 180) / Math.max(s.speed, 5) * dt;
  }
  s.x += Math.sin(s.heading) * s.speed * dt; s.z += Math.cos(s.heading) * s.speed * dt;
  if (thr > 0){
    const used = c.amps * thr * dt / 3600 * 1000;
    s.battery = Math.max(0, s.battery - used / c.sel.battery.mah * 100 * 10);
  }
}

function render(dt){
  const s = state;
  planeGroup.position.set(s.x, s.alt + .5, s.z);
  planeGroup.rotation.y = s.heading;
  planeGroup.rotation.x = cfg.isQuad ? s.pitch * Math.PI / 180 : -s.pitch * Math.PI / 180;
  planeGroup.rotation.z = s.roll * Math.PI / 180;
  const spin = (s.battery > 0 ? s.throttle : 0) * 60 * dt;
  spinners.forEach(p => { if (p.axis === 'z') p.m.rotation.z += spin; else p.m.rotation.y += spin * p.dir; });
  const sh = Math.sin(s.heading), ch = Math.cos(s.heading);
  const target = new THREE.Vector3(s.x - sh * 11, s.alt + 4.5, s.z - ch * 11);
  camera.position.lerp(target, .12);
  camera.lookAt(s.x, s.alt + 1, s.z);
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
  $('hud-weight').textContent = Math.round(c.mass);
  $('hud-thrust').textContent = Math.round(c.thrust);
  const t = $('hud-twr'); t.textContent = c.twr.toFixed(2);
  t.className = c.twr < (c.isQuad ? 1.2 : .35) ? 'warn' : (c.twr > 2 ? 'good' : 'val');
  $('row-wl').style.display = c.isQuad ? 'none' : 'inline';
  $('hud-wl').textContent = c.wl.toFixed(0); $('hud-stall').textContent = Math.round(c.stall * 3.6);
  $('hud-time').textContent = c.timeMin.toFixed(1);
  $('hud-range').textContent = c.rcKm >= 999 ? c.range.toFixed(1) + '+' : c.range.toFixed(1);
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
  const q = PARTS.frame[$('sel-frame').value].type;
  $('sel-wing').disabled = q === 'quad'; $('sel-servo').disabled = q === 'quad';
  $('sel-tail').disabled = q !== 'plane';
  cfg = compute();
  buildModel(cfg); resetState(); renderStats();
  if (changed) showInfo(changed);
}

/* ======================= قائمة القطع ======================= */
function showBom(){
  const c = cfg; let h = '<table><tr><th>القطعة</th><th>العدد</th><th>الوزن</th><th>السعر</th></tr>';
  c.bom.forEach(b => { h += '<tr><td>' + b.cat + '<br><small style="color:#889">' + b.n + '</small></td><td>' + b.qty + '</td><td>' + b.w + 'g</td><td>$' + b.c + '</td></tr>'; });
  h += '<tr><th>الإجمالي</th><th></th><th>' + Math.round(c.mass) + 'g</th><th>$' + Math.round(c.cost) + '</th></tr></table>';
  h += '<p style="font-size:.75rem;color:#889">الأسعار تقريبية وتختلف حسب المتجر والبلد. أضف أدوات التصنيع وشاحن LiPo إن لم تكن تملكهما.</p>';
  $('bom-body').innerHTML = h; $('bom-modal').style.display = 'flex';
}

/* ======================= دليل التصنيع (محلي) ======================= */
function localGuide(c){
  const t = c.type, S = c.sel, quad = c.isQuad;
  const cells = c.sel.battery === PARTS.battery['2s'] ? 2 : c.sel.battery === PARTS.battery['3s'] ? 3 : c.sel.battery === PARTS.battery['4s'] ? 4 : 6;
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
    'بطاريات LiPo: اشحنها داخل كيس أمان، لا تتركها تُشحن دون مراقبة، ولا تفرغها أقل من 3.5V لكل خلية (' + cells + 'S: لا تنزل عن ~' + (cells * 3.5).toFixed(1) + 'V).',
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
  if (ai && Array.isArray(ai.tips) && ai.tips.length) add('💡 نصائح المهندس', fillList('ul', ai.tips.map(String)));
  add('🧰 الأدوات المطلوبة', fillList('ul', local.tools));
  add('🦺 السلامة', fillList('ul', local.safety));
  add('✅ قائمة الفحص قبل الطيران', fillList('ul', local.tests));
  $('guide-modal').style.display = 'flex';
}

/* ======================= شريط الأدوات ======================= */
$('t-parts').addEventListener('click', () => { const d = bp.style.display; bp.style.display = d === 'none' ? 'flex' : 'none'; });
$('t-guide').addEventListener('click', () => showGuide(null));
$('t-bom').addEventListener('click', showBom);
$('t-reset').addEventListener('click', resetState);

/* ======================= مهندس الطيران AI ======================= */
const aiBtn = $('ai-btn'), aiResult = $('ai-result');
aiBtn.addEventListener('click', () => {
  const q = $('ai-input').value.trim(); if (!q) return;
  aiResult.style.display = 'block';
  if (!(window.Android && window.Android.askAi)){ aiResult.textContent = 'خاصية AI تعمل داخل التطبيق فقط. يمكنك استخدام زر الدليل المحلي.'; return; }
  aiResult.textContent = 'جاري التصميم وكتابة دليل التصنيع...';
  const prompt = 'أنت مهندس طيران ومعلم للمبتدئين. المستخدم يطلب: "' + q + '". اختر أفضل قطع للطائرة، واشرح لماذا، واكتب خطوات تصنيع واقعية ونصائح.\n' +
    'الخيارات المتاحة (استخدم المفاتيح الإنجليزية فقط):\n' +
    '- frame: plane, wing, cargo, quad\n- wing: trainer, glider, sport, big (تُهمل للكوادكوبتر)\n- tail: conv, vtail, none\n' +
    '- battery: 2s, 3s, 4s, 6s\n- motor: small, medium, large\n- prop: small, large\n- esc: e10, e30, e60\n- servo: s9, s17\n' +
    '- fc: none, gyro, gps\n- rc: r24, r58, r4g\n- cam: none, fpv, hd\n' +
    'قواعد: ESC أكبر من تيار المحرك بـ20%، والبطارية تتحمل التيار، وTWR للطائرة ≥ 0.5 وللكوادكوبتر ≥ 1.5.\n' +
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
    SLOTS.forEach(([k]) => {
      const v = data.parts[k];
      if (v && PARTS[k][v]) $('sel-' + k).value = v;
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
  step(dt); render(dt);
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

print(">> Flight Lab v2 applied (activity + html + manifest). Menu item: menu_items_patch.py")

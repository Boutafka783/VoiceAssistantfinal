import os
import re

ROOT = os.environ.get("PROJECT_DIR", ".")
PKG_DIR = os.path.join(ROOT, "app", "src", "main", "java", "com", "example", "voiceassistant")
ASSETS_DIR = os.path.join(ROOT, "app", "src", "main", "assets")
MAIN_SCREEN = os.path.join(PKG_DIR, "ui", "MainScreen.kt")
MANIFEST = os.path.join(ROOT, "app", "src", "main", "AndroidManifest.xml")
MECH_HTML_PATH = os.path.join(ASSETS_DIR, "mech_sim.html")
MECH_ACTIVITY_PATH = os.path.join(PKG_DIR, "MechSimulatorActivity.kt")

# ==============================================================================
# 1. mech_sim.html  (واجهة المختبر الميكانيكي)
# ==============================================================================
MECH_HTML = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Mechanical Lab</title>
<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--accent:#38bdf8}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}
html,body{margin:0;height:100%}
body{background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;overflow:hidden;display:flex;flex-direction:column}
header{padding:8px;background:var(--panel);border-bottom:1px solid var(--line);display:flex;gap:8px;align-items:center}
header h1{flex:1;margin:0;font-size:15px;white-space:nowrap}
header label{font-size:12px;display:flex;align-items:center;gap:4px;direction:ltr}
header input[type=range]{width:80px}
button{background:#334155;color:#fff;border:1px solid #475569;border-radius:8px;padding:6px 12px;font-size:13px;cursor:pointer;white-space:nowrap}
button:disabled{opacity:.5}
button.primary{background:#0284c7;border-color:#0ea5e9}
button.danger{background:#7f1d1d;border-color:#991b1b}
#tools{padding:8px;background:var(--panel);border-bottom:1px solid var(--line);display:flex;gap:6px;overflow-x:auto}
#tools3{padding:8px;background:var(--panel);border-bottom:1px solid var(--line);display:flex;gap:6px;overflow-x:auto}
#stage{flex:1;position:relative;background:#0b1220;min-height:0}
canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none}
#out{display:none;position:absolute;left:8px;right:8px;bottom:8px;max-height:45%;overflow:auto;background:rgba(15,23,42,.94);border:1px solid var(--line);border-radius:10px;padding:10px;font-size:13px;line-height:1.6;white-space:pre-wrap;-webkit-user-select:text;user-select:text}
#props{display:none;position:absolute;left:8px;right:8px;bottom:8px;background:rgba(15,23,42,.96);border:1px solid var(--accent);border-radius:10px;padding:8px 10px}
#props .ph{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;font-size:14px}
#pFields{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center}
#pFields label{font-size:12px;display:flex;align-items:center;gap:6px}
#pFields input[type=number]{width:72px;padding:5px;border-radius:6px;border:1px solid #475569;background:#0b1220;color:#fff;-webkit-user-select:text;user-select:text}
#pFields input[type=checkbox]{width:18px;height:18px}
#tools2{padding:6px 8px;background:var(--panel);border-bottom:1px solid var(--line);display:flex;gap:6px;overflow-x:auto;align-items:center}
#tools2 select{background:#334155;color:#fff;border:1px solid #475569;border-radius:8px;padding:6px;font-size:13px}
#ai{display:flex;gap:6px;padding:8px;background:var(--panel);border-top:1px solid var(--line)}
#ai input{flex:1;min-width:0;padding:8px;border-radius:8px;border:1px solid #475569;background:#0b1220;color:#fff;-webkit-user-select:text;user-select:text}
</style>
</head>
<body>
<header>
  <h1>المختبر الميكانيكي ⚙️</h1>
  <label>g <input id="gs" type="range" min="0" max="20" step="0.1" value="9.8" oninput="setG(this.value)"><span id="gv">9.8</span></label>
  <button id="btnPause" onclick="togglePause()">⏸</button>
  <button id="btnClose" onclick="if(window.Android&&Android.close){Android.close();}else{history.back();}">✕</button>
</header>
<div id="tools">
  <button onclick="addBody('motor')">+ محرك</button>
  <button onclick="addBody('dc_motor')">+ محرك DC</button>
  <button onclick="addBody('gear')">+ ترس</button>
  <button onclick="addBody('worm')">+ ترس دودي</button>
  <button onclick="addBody('bevel')">+ ترس مخروطي</button>
  <button onclick="addBody('flywheel')">+ حدافة</button>
  <button onclick="addBody('pulley')">+ بكرة</button>
  <button onclick="addBody('spring')">+ نابض</button>
  <button onclick="addBody('ball')">+ كرة</button>
  <button onclick="addBody('weight')">+ ثقل</button>
  <button onclick="addBody('pendulum')">+ بندول</button>
  <button onclick="addBody('wheel')">+ عجلة</button>
  <button onclick="addBody('rod')">+ ذراع</button>
  <button onclick="addBody('rack')">+ جريدة</button>
  <button onclick="addBody('belt')">+ حزام</button>
  <button onclick="addBody('chain')">+ سلسلة</button>
  <button onclick="addBody('pump')">+ مضخة</button>
  <button onclick="addBody('piston')">+ مكبس</button>
  <button onclick="addBody('valve')">+ صمام</button>
  <button onclick="addBody('reservoir')">+ خزان</button>
  <button onclick="addBody('actuator')">+ مشغل خطي</button>
  <button onclick="addBody('cam')">+ كامة</button>
  <button onclick="addBody('crank')">+ عمود مرفق</button>
  <button onclick="addBody('slider')">+ منزلق</button>
  <button onclick="addBody('anchor')">+ مسمار تثبيت</button>
  <button onclick="addBody('beam')">+ عارضة</button>
  <button onclick="addBody('limit_switch')">+ مفتاح حدي</button>
  <button class="danger" onclick="delSel()">حذف المحدد</button>
  <button class="danger" onclick="clearAll()">مسح</button>
</div>
<div id="tools3">
  <button onclick="addBody('gripper')">+ قابض</button>
  <button onclick="addBody('robot_arm')">+ ذراع روبوت</button>
  <button onclick="addBody('conveyor')">+ سير ناقل</button>
  <button onclick="addBody('lead_screw')">+ مسمار حركة</button>
  <button onclick="addBody('differential')">+ ترس تفاضلي</button>
  <button onclick="addBody('shock_absorber')">+ ممتص صدمات</button>
  <button onclick="addBody('steering')">+ توجيه</button>
  <button onclick="addBody('universal_joint')">+ مفصل عام</button>
  <button onclick="addBody('clutch')">+ قابض احتكاكي</button>
  <button onclick="addBody('ratchet')">+ سقاطة</button>
  <button onclick="addBody('pawl')">+ لسان سقاطة</button>
  <button onclick="addBody('geneva')">+ آلية جنيف</button>
  <button onclick="addBody('escapement')">+ ميزان ساعة</button>
  <button onclick="addBody('flyball_governor')">+ منظم طرد مركزي</button>
  <button onclick="addBody('propeller')">+ مروحة</button>
  <button onclick="addBody('turbine')">+ توربين</button>
  <button onclick="addBody('windmill')">+ طاحونة</button>
  <button onclick="addBody('encoder')">+ مشفّر</button>
  <button onclick="addBody('pressure_gauge')">+ مقياس ضغط</button>
  <button onclick="addBody('dynamometer')">+ مقياس قوة</button>
</div>
<div id="tools2">
  <select id="slot"><option value="1">خانة 1</option><option value="2">خانة 2</option><option value="3">خانة 3</option></select>
  <button onclick="saveScene()">💾 حفظ</button>
  <button onclick="loadSaved()">📂 تحميل</button>
  <button onclick="exportImage()">🖼 صورة</button>
  <button onclick="undo()">↩ تراجع</button>
</div>
<div id="stage">
  <canvas id="cv"></canvas>
  <div id="props"><div class="ph"><b id="pTitle"></b><button onclick="hideProps()">إغلاق</button></div><div id="pFields"></div></div>
  <div id="out" onclick="this.style.display='none'"></div>
</div>
<div id="ai">
  <input id="aiText" placeholder="مثال: صمم نظام تروس مع محرك وجريدة">
  <button id="btnGen" class="primary" onclick="askGenerate()">ارسم</button>
  <button id="btnExp" onclick="askExplain()">اشرح</button>
  <button id="btnFix" onclick="askFix()">أصلح</button>
</div>
<script>
var TYPES = ["motor", "gear", "pulley", "spring", "ball", "pendulum", "wheel", "rod", "rack", "belt",
             "pump", "piston", "valve", "reservoir", "cam", "crank",
             "actuator", "slider", "worm", "bevel", "flywheel", "anchor", "beam", "weight", "chain",
             "limit_switch", "dc_motor",
             "gripper", "robot_arm", "conveyor", "lead_screw", "differential", "shock_absorber", "steering",
             "universal_joint", "clutch", "ratchet", "geneva", "escapement", "pawl", "flyball_governor",
             "propeller", "turbine", "windmill", "encoder", "pressure_gauge", "dynamometer"];
var NEW_TYPES = ["pump", "piston", "valve", "reservoir", "cam", "crank",
                 "actuator", "slider", "anchor", "beam", "limit_switch",
                 "gripper", "robot_arm", "conveyor", "lead_screw", "shock_absorber", "pawl",
                 "propeller", "pressure_gauge", "dynamometer"];   // عناصر بدون زر تثبيت
var ROT_TYPES = ["motor", "dc_motor", "gear", "pulley", "worm", "bevel", "flywheel", "differential", "steering",
                 "universal_joint", "clutch", "ratchet", "geneva", "escapement", "flyball_governor",
                 "windmill", "turbine", "encoder"];
var LINK_R = 220;              // أقصى مسافة بين المضخة والمكبس ليرتبطا هيدروليكياً
var NAMES = { motor: "محرك", gear: "ترس", pulley: "بكرة", spring: "نابض", ball: "كرة",
              pendulum: "بندول", wheel: "عجلة", rod: "ذراع توصيل", rack: "جريدة مسننة", belt: "حزام",
              pump: "مضخة", piston: "مكبس", valve: "صمام", reservoir: "خزان", cam: "كامة", crank: "عمود مرفق",
              actuator: "مشغل خطي", slider: "منزلق", worm: "ترس دودي", bevel: "ترس مخروطي", flywheel: "حدافة",
              anchor: "مسمار تثبيت", beam: "عارضة", weight: "ثقل", chain: "سلسلة", limit_switch: "مفتاح حدي",
              dc_motor: "محرك DC",
              gripper: "قابض (كلابة)", robot_arm: "ذراع روبوت", conveyor: "سير ناقل", lead_screw: "مسمار حركة",
              differential: "ترس تفاضلي", shock_absorber: "ممتص صدمات", steering: "نظام توجيه",
              universal_joint: "مفصل عام", clutch: "قابض احتكاكي", ratchet: "سقاطة", geneva: "آلية جنيف",
              escapement: "ميزان الساعة", pawl: "لسان سقاطة", flyball_governor: "منظم طرد مركزي",
              propeller: "مروحة", turbine: "توربين", windmill: "طاحونة هوائية", encoder: "مشفّر دوّار",
              pressure_gauge: "مقياس ضغط", dynamometer: "مقياس قوة" };
var HINTS = {
  piston: "يتحرك المكبس دورياً، وإذا وُجدت مضخة ضمن 220 بكسل يتبع سرعتها؛ صمام مغلق على الخط بينهما يوقفه. يدفع منزلقاً أفقياً بطرف قضيبه.",
  crank: "اسحب طرف ذراع (rod) فوق مسمار المرفق ليتحرك معه. اربط طرفه الآخر بمركز منزلق للحصول على آلية مرفق-منزلق.",
  belt: "اسحب طرفي الحزام فوق بكرتين/ترسين/محرك ليدورا معاً بنفس الاتجاه.",
  chain: "اسحب طرفي السلسلة فوق ترسين ليدورا معاً بنفس الاتجاه وبنسبة نصفي القطر.",
  slider: "يتحرك أفقياً على سكته. يدفعه مشغل خطي أو مكبس أو كامة، وإذا ربطت ذراعاً بمركزه ومرفق يتحرك به. ثابت الإرجاع 0 = حر.",
  anchor: "نقطة ثابتة: اسحب طرف ذراع (rod) فوقها ليدور الذراع حولها.",
  worm: "يحرّك ترساً مجاوراً بنسبة 1 : عدد أسنانه، ولا يُدار إلا من محرك (ذاتي القفل).",
  bevel: "يتعشق مع ترس مخروطي آخر لنقل الحركة بزاوية 90° (الاتجاه اصطلاحي في الرسم ثنائي الأبعاد).",
  flywheel: "قرص ثقيل: يتسارع ببطء ولا يتوقف فجأة عند فصل المحرك. السرعة الابتدائية تُدخل من الخاصية rpm.",
  limit_switch: "يحمرّ ويضيء عند ملامسة أي جسم متحرك (كرة، ثقل، منزلق، ذراع...).",
  weight: "ثقل يسقط بالجاذبية ويقف على الأرض أو العارضة أو الجريدة. ألغِ التثبيت ليسقط.",
  beam: "عارضة ثابتة تقف عليها الكرات والعجلات والأثقال.",
  gripper: "فكّان يفتحان ويغلقان. انقر عليه لفتحه/إغلاقه يدوياً، أو اتركه يعمل تلقائياً.",
  robot_arm: "ذراع بثلاثة مفاصل تتحرك بسلاسة؛ طرفها يدفع منزلقاً أو يضغط مفتاحاً حدياً.",
  conveyor: "يسحب أي كرة أو عجلة أو ثقل فوق سطحه أفقياً بسرعة sv (سالبة = للخلف).",
  lead_screw: "يحوّل الدوران إلى حركة خطية بطيئة لصامولة تدفع المنزلق، وتعكس اتجاهها عند الحدّين.",
  differential: "يدير عجلتين (wheel) موضوعتين عند طرفيه. ثبّت إحداهما لترى الأخرى تتسارع. يُدار بتعشيقه مع ترس/محرك.",
  shock_absorber: "نابض مع أسطوانة تخميد؛ زد التخميد ليقل الاهتزاز. اسحب كرته لتجربته.",
  steering: "يدوّر العجلتين الأماميتين عند تدويره (بتعشيق محرك) أو يدوياً من حقل الزاوية.",
  universal_joint: "ينقل الحركة بزاوية انحناء deg مع تذبذب في السرعة مثل المفصل الحقيقي.",
  clutch: "انقر عليه: مغلق ينقل الحركة، مفتوح يقطعها. القيم بينهما = انزلاق.",
  ratchet: "يدور في اتجاه واحد فقط؛ الاتجاه يُعكس بالحقل ori.",
  pawl: "لسان يمنع الترس القريب منه من الدوران بعكس عقارب الساعة (يُعكس بالحقل ori).",
  geneva: "يحوّل دوران الدخل المستمر إلى دوران متقطع (ربع لفة لكل دورة) لما يتعشق به.",
  escapement: "ينظّم الدوران بنبضات tik-tok؛ السرعة بالحقل spd.",
  flyball_governor: "كرتان تتباعدان بزيادة سرعة الدوران (الطرد المركزي).",
  propeller: "تدفع الأجسام القريبة في اتجاه deg؛ تدير أيضاً التوربين والطاحونة أمامها.",
  turbine: "يدور بتدفق مضخة قريبة (ما لم يُغلق صمام بينهما) أو بمروحة، ويدير ما يتعشق به.",
  windmill: "تدور بسرعة الرياح (حقل rpm) وبمروحة أمامها، وتدير ما يتعشق بها.",
  encoder: "يقرأ زاوية الدوران والسرعة ويعرضهما؛ يمرّر الحركة لما يتعشق به.",
  pressure_gauge: "يقرأ ضغط المضخات القريبة (يهبط عند إغلاق صمام بينهما). ألغِ الوضع التلقائي لضبطه يدوياً.",
  dynamometer: "يقيس قوة السحب/الدفع بالنيوتن من استطالة نابضه. علّق ثقلاً أو ادفعه بجسم."
};
var TOGGLES = {
  actuator: ["⏸ إيقاف المشغل", "▶ تشغيل المشغل"],
  robot_arm: ["⏸ إيقاف الحركة", "▶ تشغيل الحركة"],
  gripper: ["⏸ إيقاف الحركة التلقائية", "▶ تشغيل الحركة التلقائية"],
  pressure_gauge: ["🔄 تلقائي (اضغط لليدوي)", "✋ يدوي (اضغط للتلقائي)"]
};
var cv = document.getElementById("cv"), ctx = cv.getContext("2d");
var props = document.getElementById("props"), pFields = document.getElementById("pFields");
var W = 300, H = 300, dpr = window.devicePixelRatio || 1;
var PX_PER_M = 100;            // 100 بكسل = 1 متر
var G = 9.8 * PX_PER_M;        // الجاذبية بالبكسل/ث²
var bodies = [], paused = false, sel = null, drag = null, uid = 1;
var busy = false, busyTimer = null, last = 0, acc = 0;
var GROUND = 10, E_BALL = 0.6, E_WHEEL = 0.3, BOB_R = 12, MESH_GAP = 14;
var MU = 0.8, ROLL_RES = 0.5;                 // احتكاك الأرض ومقاومة التدحرج
var PITCH = 2 * Math.PI * 3.3;                // خطوة الأسنان (تتوافق مع عدد أسنان الترس)

function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
function num(v, d, a, b) { v = parseFloat(v); return isFinite(v) ? clamp(v, a, b) : d; }
function isMotor(b) { return b.type === "motor" || b.type === "dc_motor"; }
function isRot(b) {
  return b.type === "motor" || b.type === "dc_motor" || b.type === "gear" || b.type === "pulley" ||
         b.type === "worm" || b.type === "bevel" || b.type === "flywheel";
}
function isCircBody(b) { return b.type === "ball" || b.type === "wheel" || isRot(b); }
function isRoll(b) { return b.type === "ball" || b.type === "wheel"; }
function isBelt(b) { return b.type === "belt" || b.type === "chain"; }
function isLinkT(t) { return t === "rod" || t === "belt" || t === "chain"; }
function isLink(b) { return isLinkT(b.type); }
function beltHost(h) { return isRot(h) && h.type !== "worm"; }
function teethOf(r) { return Math.max(6, Math.round(r / 3.3)); }

// أقرب مضخة ضمن LINK_R، وهل يوجد صمام مغلق على الخط بين المضخة والمكبس
function pistonLink(b) {
  var p = null, bd = LINK_R, i, o, d;
  for (i = 0; i < bodies.length; i++) {
    o = bodies[i];
    if (o.type !== "pump") continue;
    d = dist(b.x, b.y, o.x, o.y);
    if (d <= bd) { bd = d; p = o; }
  }
  if (!p) return { p: null, blocked: false };
  var blocked = false;
  for (i = 0; i < bodies.length; i++) {
    o = bodies[i];
    if (o.type === "valve" && !o.state && segDist(o.x, o.y, p.x, p.y, b.x, b.y) < o.size + 14) { blocked = true; break; }
  }
  return { p: p, blocked: blocked };
}

// الكامة (قطع ناقص يدور حول مركزه): تدفع أي طرف حر لذراع يلامس سطحها العلوي
function camPushPt(b, kx, ky, kox, koy) {
  for (var i = 0; i < bodies.length; i++) {
    var c = bodies[i];
    if (c.type !== "cam") continue;
    var dx = b[kx] - c.x, dy = b[ky] - c.y;
    var ca = c.size + c.ecc, cb = c.size;
    if (Math.abs(dx) > ca || Math.abs(dy) > ca) continue;
    var s = Math.sin(c.angle), co = Math.cos(c.angle);
    var qa = s * s / (ca * ca) + co * co / (cb * cb);
    var qb = 2 * dx * s * co * (1 / (ca * ca) - 1 / (cb * cb));
    var qc = dx * dx * (co * co / (ca * ca) + s * s / (cb * cb)) - 1;
    var D = qb * qb - 4 * qa * qc;
    if (D < 0) continue;
    var sq = Math.sqrt(D), top = (-qb - sq) / (2 * qa), bot = (-qb + sq) / (2 * qa);
    if (dy > top && dy <= (top + bot) / 2) { b[ky] = c.y + top - 0.5; b[koy] = b[ky]; }
  }
}
// الكامة تدفع المنزلق جانبياً: نحسب حافتي القطع الناقص على خط ارتفاع المنزلق
function camPushSlider(s) {
  for (var i = 0; i < bodies.length; i++) {
    var c = bodies[i];
    if (c.type !== "cam") continue;
    var dy = s.y - c.y, ca = c.size + c.ecc, cb = c.size;
    if (Math.abs(dy) >= ca) continue;
    var sn = Math.sin(c.angle), co = Math.cos(c.angle);
    var A = co * co / (ca * ca) + sn * sn / (cb * cb);
    var B = 2 * dy * sn * co * (1 / (ca * ca) - 1 / (cb * cb));
    var C = dy * dy * (sn * sn / (ca * ca) + co * co / (cb * cb)) - 1;
    var D = B * B - 4 * A * C;
    if (D <= 0) continue;
    var sq = Math.sqrt(D), xl = c.x + (-B - sq) / (2 * A), xr = c.x + (-B + sq) / (2 * A);
    if (s.x >= c.x) { if (s.x - s.size < xr) { s.x = xr + s.size; s.vx = 0; } }
    else { if (s.x + s.size > xl) { s.x = xl - s.size; s.vx = 0; } }
  }
}
function dist(x1, y1, x2, y2) { var dx = x2 - x1, dy = y2 - y1; return Math.sqrt(dx * dx + dy * dy); }

// أطراف المشغل الخطي والمكبس
function actLen(o) { return o.rest + (o.len - o.rest) * clamp(o.val, 0, 1); }
function actTip(o) {
  var a = o.deg * Math.PI / 180, L = actLen(o);
  return { x: o.x + Math.cos(a) * L, y: o.y + Math.sin(a) * L };
}
function pistonTip(o) {
  var pv = clamp(o.val, 0, 1), X = (-o.len / 2 + 6 + (o.len - 12) * pv) + o.len;
  return (o.ori >= 0.5) ? { x: o.x, y: o.y - X } : { x: o.x + X, y: o.y };
}

function resize() {
  var r = cv.getBoundingClientRect();
  W = Math.max(50, r.width); H = Math.max(50, r.height);
  cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
window.addEventListener("resize", resize);

function setG(v) {
  v = num(v, 9.8, 0, 20);
  G = v * PX_PER_M;
  document.getElementById("gv").textContent = v.toFixed(1);
}
function togglePause() {
  paused = !paused;
  document.getElementById("btnPause").textContent = paused ? "▶" : "⏸";
}

function mk(type, x, y, o) {
  var b = { id: uid++, type: type, x: x, y: y, vx: 0, vy: 0, angle: 0, w: 0, rpm: 0, size: 30,
            k: 60, rest: 90, bx: x, by: y, bvx: 0, bvy: 0, len: 120, th: 0, om: 0, seen: false,
            fixed: (type === "ball" || type === "wheel" || type === "rod" || type === "weight") ? false : true,
            ex: x, ey: y, ox: x, oy: y, eox: x, eoy: y, at: null, bt: null,
            state: true, val: 0, ecc: 12, spd: 1, ori: 0, ph: -Math.PI / 2,
            volt: 12, deg: 0, fw: 0, hit: false };
  if (type === "motor") { b.size = 28; b.rpm = 30; }
  else if (type === "dc_motor") { b.size = 28; b.rpm = 30; b.volt = 12; }
  else if (type === "gear") { b.size = 40; }
  else if (type === "worm") { b.size = 20; }
  else if (type === "bevel") { b.size = 30; }
  else if (type === "flywheel") { b.size = 45; }
  else if (type === "pulley") { b.size = 34; }
  else if (type === "ball") { b.size = 18; }
  else if (type === "wheel") { b.size = 22; }
  else if (type === "weight") { b.size = 18; }
  else if (type === "anchor") { b.size = 8; }
  else if (type === "beam") { b.len = 150; b.size = 14; }
  else if (type === "pendulum") { b.th = 0.9; }
  else if (type === "rack") { b.len = 160; }
  else if (type === "pump") { b.size = 24; b.rpm = 30; }
  else if (type === "piston") { b.len = 60; }
  else if (type === "valve") { b.size = 16; }
  else if (type === "reservoir") { b.size = 60; b.len = 90; b.val = 0.6; }
  else if (type === "cam") { b.size = 26; b.ecc = 12; b.rpm = 30; }
  else if (type === "crank") { b.size = 10; b.len = 45; b.rpm = 30; }
  else if (type === "actuator") { b.rest = 50; b.len = 110; b.deg = 0; }
  else if (type === "slider") { b.size = 16; b.len = 140; b.k = 40; }
  else if (type === "limit_switch") { b.size = 14; }
  o = o || {};
  for (var key in o) { if (o.hasOwnProperty(key)) b[key] = o[key]; }
  if (type === "spring") { b.bx = b.x; b.by = b.y + b.rest * 1.3; }
  if (isLinkT(type)) { b.ex = b.x + b.len; b.ey = b.y; b.ox = b.x; b.oy = b.y; b.eox = b.ex; b.eoy = b.ey; }
  return b;
}

function addBody(t) {
  var x = clamp(W / 2 + (Math.random() - 0.5) * 80, 40, W - 40), y;
  if (t === "ball") y = 50;
  else if (t === "wheel") y = 60;
  else if (t === "weight") y = 50;
  else if (t === "spring" || t === "pendulum") y = 40;
  else if (t === "anchor") y = H * 0.3;
  else if (isLinkT(t)) { y = H * 0.3; x = clamp(W / 2 - 60, 10, Math.max(10, W - 140)); }
  else if (t === "rack") y = H * 0.7;
  else if (t === "pump") { x = clamp(W * 0.2, 40, W - 40); y = H * 0.65; }
  else if (t === "valve") { x = clamp(W * 0.4, 40, W - 40); y = H * 0.65; }
  else if (t === "piston") { x = clamp(W * 0.62, 60, Math.max(60, W - 60)); y = H * 0.65; }
  else if (t === "reservoir") { x = clamp(W * 0.5, 60, W - 60); y = H * 0.75; }
  else if (t === "cam") { x = clamp(W * 0.5, 50, W - 50); y = H * 0.7; }
  else if (t === "crank") { x = clamp(W * 0.5, 60, W - 60); y = H * 0.5; }
  else if (t === "actuator") { x = clamp(W * 0.2, 30, W - 30); y = H * 0.6; }
  else if (t === "slider") { x = clamp(W * 0.6, 60, Math.max(60, W - 60)); y = H * 0.6; }
  else if (t === "beam") { x = clamp(W * 0.5, 80, Math.max(80, W - 80)); y = H * 0.8; }
  else if (t === "limit_switch") { x = clamp(W * 0.8, 30, W - 30); y = H - GROUND - 14; }
  else y = H * 0.45;
  var b = mk(t, x, y, {});
  bodies.push(b); sel = b;
}
function delSel() {
  if (!sel) return;
  var i = bodies.indexOf(sel);
  if (i >= 0) bodies.splice(i, 1);
  sel = null; hideProps();
}
function clearAll() { if (bodies.length) pushUndo(); bodies = []; sel = null; hideProps(); document.getElementById("out").style.display = "none"; }

// ---------------------------------------------------------------- الفيزياء
function meshing(a, c) { return dist(a.x, a.y, c.x, c.y) < a.size + c.size + MESH_GAP; }

// الجريدة: أسنانها للأعلى، وخط الخطوة على ارتفاع (y - 11)
function rackMesh(g, r) {
  if (!isRot(g)) return false;
  var d = (r.y - 11) - g.y;
  return Math.abs(d - g.size) < MESH_GAP && Math.abs(g.x - r.x) <= r.len / 2;
}
function transfer(a, c) {
  if (a.type === "rack") {
    if (c.type === "rack" || !rackMesh(c, a)) return false;
    c.w = -a.vx / c.size; return true;
  }
  if (c.type === "rack") {
    if (!rackMesh(a, c)) return false;
    c.vx = -a.w * a.size; return true;
  }
  if (!meshing(a, c)) return false;
  if (c.type === "worm") {                       // الدودي ذاتي القفل: لا يُدار إلا من محرك
    if (!isMotor(a)) return false;
    c.w = -a.w * a.size / c.size; return true;
  }
  if (a.type === "worm") { c.w = -a.w / teethOf(c.size); return true; }     // نسبة 1 : عدد الأسنان
  if (a.type === "bevel" && c.type === "bevel") { c.w = a.w * a.size / c.size; return true; }   // محوران متعامدان
  c.w = -a.w * a.size / c.size; return true;
}

function circ(b) {
  if (b.type === "spring") return { o: b, x: "bx", y: "by", vx: "bvx", vy: "bvy", r: BOB_R, im: isDragging(b, "bob") ? 0 : 1 };
  return { o: b, x: "x", y: "y", vx: "vx", vy: "vy", r: b.size, im: (b.fixed || isDragging(b, "main")) ? 0 : 1 };
}
function isDragging(b, part) { return drag && drag.b === b && drag.part === part; }

// كرة / عجلة / عنصر دوّار غير مثبّت: جاذبية + ارتداد + احتكاك الأرض
function stepCircle(b, dt) {
  var roll = isRoll(b);
  var e = b.type === "wheel" ? E_WHEEL : (b.type === "ball" ? E_BALL : 0.2);
  b.vy += G * dt;
  b.vx *= (1 - 0.1 * dt);
  b.x += b.vx * dt; b.y += b.vy * dt;
  var floorY = H - GROUND - b.size;
  if (b.y > floorY) {
    var vin = Math.abs(b.vy);
    b.y = floorY; b.vy = -b.vy * e;
    if (Math.abs(b.vy) < 25) b.vy = 0;
    var N = vin + Math.abs(b.vy);                  // الدفع العمودي
    if (roll) {
      // قيد التدحرج بدون انزلاق: slip = vx - w*r ، قرص متجانس (I = m r²/2)
      var slip = b.vx - b.w * b.size;
      var J = clamp(-slip / 3, -MU * N, MU * N);
      b.vx += J; b.w += -2 * J / b.size;
      var damp = 1 - ROLL_RES * dt;                // مقاومة تدحرج تجعلها تستقر
      b.vx *= damp; b.w *= damp;
      if (Math.abs(b.vx) < 2 && Math.abs(b.w * b.size) < 2) { b.vx = 0; b.w = 0; }
    } else {
      b.vx *= (1 - 6 * dt);                        // انزلاق
    }
  }
  if (b.x - b.size < 0) { b.x = b.size; b.vx = -b.vx * e; }
  if (b.x + b.size > W) { b.x = W - b.size; b.vx = -b.vx * e; }
  beamHit(b, e, roll, dt);
  if (roll) b.angle += b.w * dt;
}

// تصادم دائرة مع العوارض الثابتة (مستطيلات محاذية للمحاور)
function beamHit(b, e, roll, dt) {
  for (var i = 0; i < bodies.length; i++) {
    var m = bodies[i];
    if (m.type !== "beam") continue;
    var hw = m.len / 2, hh = m.size / 2;
    var cx = clamp(b.x, m.x - hw, m.x + hw), cy = clamp(b.y, m.y - hh, m.y + hh);
    var dx = b.x - cx, dy = b.y - cy, d = Math.sqrt(dx * dx + dy * dy);
    if (d >= b.size) continue;
    var nx, ny;
    if (d < 0.001) { nx = 0; ny = -1; b.y = m.y - hh - b.size; }      // المركز داخل العارضة: ادفعها للأعلى
    else { nx = dx / d; ny = dy / d; b.x += nx * (b.size - d); b.y += ny * (b.size - d); }
    var vn = b.vx * nx + b.vy * ny;
    if (vn < 0) {
      b.vx -= (1 + e) * vn * nx; b.vy -= (1 + e) * vn * ny;
      if (ny < -0.5 && Math.abs(b.vy) < 25) b.vy = 0;
      if (ny < -0.5) {
        if (roll) {
          var N = -vn * (1 + e), slip = b.vx - b.w * b.size;
          var J = clamp(-slip / 3, -MU * N, MU * N);
          b.vx += J; b.w += -2 * J / b.size;
          var damp = 1 - ROLL_RES * dt;
          b.vx *= damp; b.w *= damp;
          if (Math.abs(b.vx) < 2 && Math.abs(b.w * b.size) < 2) { b.vx = 0; b.w = 0; }
        } else {
          b.vx *= (1 - 6 * dt);
        }
      }
    }
  }
}

// الثقل: مربع ثقيل يسقط ولا يرتد، ويقف على الأرض والعوارض والجريدة والأثقال الأخرى
function stepWeight(b, dt) {
  var s = b.size;
  if (b.fixed || isDragging(b, "main")) { b.vx = 0; b.vy = 0; return; }
  b.vy += G * dt;
  b.vx *= (1 - 4 * dt);
  b.x += b.vx * dt; b.y += b.vy * dt;
  var fy = H - GROUND - s;
  if (b.y > fy) { b.y = fy; b.vy = 0; b.vx *= (1 - 8 * dt); }
  b.x = clamp(b.x, s, W - s);
  for (var i = 0; i < bodies.length; i++) {
    var m = bodies[i], hw, hh;
    if (m === b) continue;
    if (m.type === "beam") { hw = m.len / 2; hh = m.size / 2; }
    else if (m.type === "rack") { hw = m.len / 2; hh = 7; }
    else if (m.type === "weight") { hw = m.size; hh = m.size; }
    else continue;
    var ox = hw + s - Math.abs(b.x - m.x), oy = hh + s - Math.abs(b.y - m.y);
    if (ox <= 0 || oy <= 0) continue;
    if (oy < ox) {
      if (b.y < m.y) { b.y -= oy; if (b.vy > 0) b.vy = 0; }
      else { b.y += oy; if (b.vy < 0) b.vy = 0; }
    } else {
      b.x += (b.x < m.x) ? -ox : ox; b.vx = 0;
    }
  }
}

// المنزلق: كتلة تتحرك أفقياً على سكة؛ نابض إرجاع اختياري، ويدفعها مشغل أو مكبس أو كامة
function drivenByRod(s) {
  for (var i = 0; i < bodies.length; i++) {
    var r = bodies[i];
    if (r.type === "rod" && ((r.at && r.at.id === s.id) || (r.bt && r.bt.id === s.id))) return true;
  }
  return false;
}
function pusherTips() {
  var tips = [];
  for (var i = 0; i < bodies.length; i++) {
    var o = bodies[i];
    if (o.type === "actuator") tips.push(actTip(o));
    else if (o.type === "piston" && o.ori < 0.5) tips.push(pistonTip(o));
  }
  return tips;
}
function stepSlider(b, dt) {
  var lo = b.bx - b.len / 2 + b.size, hi = b.bx + b.len / 2 - b.size;
  if (lo > hi) { lo = b.bx; hi = b.bx; }
  if (isDragging(b, "main")) { b.vx = 0; return; }
  if (drivenByRod(b)) { b.vx = 0; }
  else {
    if (b.k > 0) b.vx += -b.k * (b.x - b.ox) * dt;
    b.vx *= (1 - 4 * dt);
    b.x += b.vx * dt;
  }
  var tips = pusherTips(), i, p;
  for (i = 0; i < tips.length; i++) {
    p = tips[i];
    if (Math.abs(p.y - b.y) > 11) continue;
    if (p.x > b.x - b.size && p.x < b.x) { b.x = p.x + b.size; b.vx = 0; }
    else if (p.x >= b.x && p.x < b.x + b.size) { b.x = p.x - b.size; b.vx = 0; }
  }
  camPushSlider(b);
  b.x = clamp(b.x, lo, hi);
}

// ---- المفتاح الحدي: هل يلامس أي جسم؟
function boxHit(sx, sy, sr, mx, my, hw, hh) {
  var cx = clamp(sx, mx - hw, mx + hw), cy = clamp(sy, my - hh, my + hh);
  return dist(sx, sy, cx, cy) < sr;
}
function touches(sw, o) {
  var sx = sw.x, sy = sw.y, sr = sw.size, t = o.type, tp;
  if (isCircBody(o)) return dist(sx, sy, o.x, o.y) < o.size + sr;
  if (t === "weight") return boxHit(sx, sy, sr, o.x, o.y, o.size, o.size);
  if (t === "rack") return boxHit(sx, sy, sr, o.x, o.y - 4, o.len / 2, 11);
  if (t === "slider") return boxHit(sx, sy, sr, o.x, o.y, o.size, 11);
  if (t === "spring") return dist(sx, sy, o.bx, o.by) < BOB_R + sr;
  if (t === "pendulum") return dist(sx, sy, o.x + Math.sin(o.th) * o.len, o.y + Math.cos(o.th) * o.len) < 15 + sr;
  if (t === "rod") return segDist(sx, sy, o.x, o.y, o.ex, o.ey) < sr + 5;
  if (t === "actuator") { tp = actTip(o); return dist(sx, sy, tp.x, tp.y) < sr + 5; }
  if (t === "piston") { tp = pistonTip(o); return dist(sx, sy, tp.x, tp.y) < sr + 4; }
  if (t === "crank") return dist(sx, sy, o.x + Math.cos(o.angle) * o.len, o.y + Math.sin(o.angle) * o.len) < sr + 6;
  if (t === "cam") {
    var dx = sx - o.x, dy = sy - o.y, cs = Math.cos(o.angle), sn = Math.sin(o.angle);
    var lx = dx * cs + dy * sn, ly = -dx * sn + dy * cs;
    var ea = o.size + o.ecc + sr, eb = o.size + sr;
    return (lx * lx) / (ea * ea) + (ly * ly) / (eb * eb) < 1;
  }
  return false;
}

// ---- الذراع (قضيب فيرليه بنقطتين مع قيد الطول)
function findBody(id) {
  for (var i = 0; i < bodies.length; i++) { if (bodies[i].id === id) return bodies[i]; }
  return null;
}
function pinPos(b, end) {
  var at = (end === "a") ? b.at : b.bt;
  if (!at) return null;
  var h = findBody(at.id);
  if (!h) { if (end === "a") b.at = null; else b.bt = null; return null; }
  var ang = h.angle + at.a;
  var pd = (h.type === "crank") ? h.len : at.d;
  return { x: h.x + Math.cos(ang) * pd, y: h.y + Math.sin(ang) * pd };
}
function slHost(b, end) {
  var at = (end === "a") ? b.at : b.bt;
  if (!at) return null;
  var h = findBody(at.id);
  return (h && h.type === "slider") ? h : null;
}
// الطرف الآخر مثبّت عند p: المنزلق يتحرك على سكته بحيث يبقى طول الذراع ثابتاً (مرفق-منزلق)
function slideTo(s, p, L) {
  var dy = s.y - p.y;
  if (Math.abs(dy) >= L) return;
  var dx = Math.sqrt(L * L - dy * dy), x1 = p.x + dx, x2 = p.x - dx;
  var nx = (Math.abs(x1 - s.x) <= Math.abs(x2 - s.x)) ? x1 : x2;
  var lo = s.bx - s.len / 2 + s.size, hi = s.bx + s.len / 2 - s.size;
  if (lo > hi) { lo = s.bx; hi = s.bx; }
  s.x = clamp(nx, lo, hi); s.vx = 0;
}
function refreshLen(b) {
  if (b.type !== "rod" || !b.at || !b.bt) return;
  var pa = pinPos(b, "a"), pb = pinPos(b, "b");
  if (pa && pb) b.len = clamp(dist(pa.x, pa.y, pb.x, pb.y), 10, 500);
}
function stepRod(b, dt) {
  var pa = pinPos(b, "a"), pb = pinPos(b, "b");
  var sa = slHost(b, "a"), sb = slHost(b, "b"), drv = false;
  if (sb && !sa && pa) { slideTo(sb, pa, b.len); drv = true; }
  else if (sa && !sb && pb) { slideTo(sa, pb, b.len); drv = true; }
  if (drv) { pa = pinPos(b, "a"); pb = pinPos(b, "b"); }
  var dA = isDragging(b, "a") || isDragging(b, "mid"), dB = isDragging(b, "b") || isDragging(b, "mid");
  var free = b.fixed ? 0 : 1;
  var imA = (pa || dA) ? 0 : free, imB = (pb || dB) ? 0 : free;
  var g2 = G * dt * dt, vx, vy;
  if (pa) { b.ox = b.x; b.oy = b.y; b.x = pa.x; b.y = pa.y; }
  if (pb) { b.eox = b.ex; b.eoy = b.ey; b.ex = pb.x; b.ey = pb.y; }
  if (dA) { b.ox = b.x; b.oy = b.y; }
  if (dB) { b.eox = b.ex; b.eoy = b.ey; }
  if (imA) { vx = (b.x - b.ox) * 0.995; vy = (b.y - b.oy) * 0.995; b.ox = b.x; b.oy = b.y; b.x += vx; b.y += vy + g2; }
  if (imB) { vx = (b.ex - b.eox) * 0.995; vy = (b.ey - b.eoy) * 0.995; b.eox = b.ex; b.eoy = b.ey; b.ex += vx; b.ey += vy + g2; }
  if ((pa || dA) && (pb || dB)) {
    if (!drv) b.len = clamp(dist(b.x, b.y, b.ex, b.ey), 10, 500);   // طرفان مثبتان: الطول يتبع المسافة
    return;
  }
  var floorY = H - GROUND - 4;
  for (var k = 0; k < 6; k++) {
    var dx = b.ex - b.x, dy = b.ey - b.y, d = Math.sqrt(dx * dx + dy * dy) || 0.001;
    var diff = (d - b.len) / d, tot = imA + imB;
    if (!tot) break;
    b.x += dx * diff * imA / tot; b.y += dy * diff * imA / tot;
    b.ex -= dx * diff * imB / tot; b.ey -= dy * diff * imB / tot;
    if (imA) {
      if (b.y > floorY) { b.y = floorY; b.ox = b.x - (b.x - b.ox) * 0.9; b.oy = b.y; }
      b.x = clamp(b.x, 0, W);
      camPushPt(b, "x", "y", "ox", "oy");
    }
    if (imB) {
      if (b.ey > floorY) { b.ey = floorY; b.eox = b.ex - (b.ex - b.eox) * 0.9; b.eoy = b.ey; }
      b.ex = clamp(b.ex, 0, W);
      camPushPt(b, "ex", "ey", "eox", "eoy");
    }
  }
}
function stepBelt(b) {
  var pa = pinPos(b, "a"), pb = pinPos(b, "b");
  if (pa) { b.x = pa.x; b.y = pa.y; }
  if (pb) { b.ex = pb.x; b.ey = pb.y; }
}
function beltR(h) { return h.size + (h.type === "gear" ? 6 : 2); }
function setRodLen(b, v) {
  var dx = b.ex - b.x, dy = b.ey - b.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
  b.len = v;
  if (!b.bt) { b.ex = b.x + dx / d * v; b.ey = b.y + dy / d * v; b.eox = b.ex; b.eoy = b.ey; }
  else if (!b.at) { b.x = b.ex - dx / d * v; b.y = b.ey - dy / d * v; b.ox = b.x; b.oy = b.y; }
}
function tryAttach(b, end) {
  var px = (end === "a") ? b.x : b.ex, py = (end === "a") ? b.y : b.ey;
  var best = null, bd = 1e9, belt = isBelt(b);
  for (var i = 0; i < bodies.length; i++) {
    var h = bodies[i];
    if (belt ? !beltHost(h) : !(isRot(h) || h.type === "wheel" || h.type === "crank" || h.type === "anchor" || h.type === "slider")) continue;
    var d, reach;
    if (h.type === "crank") { d = dist(px, py, h.x + Math.cos(h.angle) * h.len, h.y + Math.sin(h.angle) * h.len); reach = 16; }
    else { d = dist(px, py, h.x, h.y); reach = h.size + 10; }
    if (d <= reach && d < bd) { bd = d; best = h; }
  }
  if (!best) return;
  if (best.type === "crank") {                       // يُربط الذراع بمسمار المرفق
    var cat = { id: best.id, d: best.len, a: 0 };
    if (end === "a") b.at = cat; else b.bt = cat;
    return;
  }
  if (best.type === "anchor" || best.type === "slider") {   // يُربط بمركز المسمار/المنزلق
    var sat = { id: best.id, d: 0, a: 0 };
    if (end === "a") b.at = sat; else b.bt = sat;
    return;
  }
  var at = belt ? { id: best.id, d: 0, a: 0 }          // الحزام/السلسلة يُربط بمركز العنصر
                : { id: best.id, d: bd, a: Math.atan2(py - best.y, px - best.x) - best.angle };
  if (end === "a") b.at = at; else b.bt = at;
}

function step(dt) {
  var i, j, b, a, c, q = [], nodes = [];

  // 1) انتقال الحركة: المحرك → تروس/بكرات → جريدة
  for (i = 0; i < bodies.length; i++) {
    b = bodies[i];
    if (isRot(b) || b.type === "rack") { b.seen = false; nodes.push(b); }
  }
  for (i = 0; i < nodes.length; i++) {
    if (isMotor(nodes[i])) { nodes[i].seen = true; nodes[i].w = nodes[i].rpm * 2 * Math.PI / 60; q.push(nodes[i]); }
  }
  var belts = [];
  for (i = 0; i < bodies.length; i++) {
    b = bodies[i];
    if (isBelt(b) && b.at && b.bt) {
      a = findBody(b.at.id); c = findBody(b.bt.id);
      if (a && c && a !== c && isRot(a) && isRot(c)) belts.push([a, c]);
    }
  }
  while (q.length) {
    a = q.shift();
    // الحدافة: تتسارع ببطء نحو سرعة المحرك (قصور ذاتي)
    if (a.type === "flywheel") { a.fw += (a.w - a.fw) * (1 - Math.exp(-dt / 1.5)); a.w = a.fw; }
    for (j = 0; j < nodes.length; j++) {
      c = nodes[j];
      if (!c.seen && transfer(a, c)) { c.seen = true; q.push(c); }
    }
    // الحزام/السلسلة: نفس اتجاه الدوران ونسبة السرعة = نسبة نصفي القطر
    for (j = 0; j < belts.length; j++) {
      var pA = belts[j][0], pB = belts[j][1];
      if (a === pA && !pB.seen) { pB.w = a.w * a.size / pB.size; pB.seen = true; q.push(pB); }
      else if (a === pB && !pA.seen) { pA.w = a.w * a.size / pA.size; pA.seen = true; q.push(pA); }
    }
  }
  for (i = 0; i < nodes.length; i++) {
    b = nodes[i];
    if (b.type === "rack") {
      var dr = isDragging(b, "main");
      if (dr) { b.vx = 0; b.vy = 0; continue; }
      if (!b.seen) b.vx *= Math.pow(0.2, dt);
      b.x += b.vx * dt;
      var hw = Math.min(b.len / 2, W / 2);
      b.x = clamp(b.x, hw, W - hw);
      if (b.fixed) { b.vy = 0; }
      else {
        b.vy += G * dt; b.y += b.vy * dt;
        var fy = H - GROUND - 7;
        if (b.y > fy) { b.y = fy; b.vy = 0; }
      }
    } else {
      if (!b.seen) {
        // عنصر غير متصل يتوقف تدريجياً؛ الحدافة تحتفظ بطاقتها وتتباطأ ببطء شديد
        b.w *= Math.pow(b.type === "flywheel" ? 0.9 : 0.2, dt);
        if (b.type === "flywheel") b.fw = b.w;
      }
      b.angle += b.w * dt;
    }
  }

  // 1.5) المضخة والكامة والمرفق تدور مثل المحرك، والمكبس والمشغل يتحركان دورياً
  for (i = 0; i < bodies.length; i++) {
    b = bodies[i];
    if (b.type === "pump" || b.type === "cam" || b.type === "crank") {
      b.w = b.rpm * 2 * Math.PI / 60;
      b.angle += b.w * dt;
    } else if (b.type === "piston") {
      var lk = pistonLink(b);
      var rate = lk.p ? Math.abs(lk.p.rpm) / 60 * b.spd : 0.5 * b.spd;   // دورة/ث
      if (!lk.blocked) b.ph += 2 * Math.PI * rate * dt;
      b.val = 0.5 + 0.5 * Math.sin(b.ph);
    } else if (b.type === "actuator") {
      if (b.state) b.ph += 2 * Math.PI * 0.5 * b.spd * dt;
      b.val = 0.5 + 0.5 * Math.sin(b.ph);
    }
  }

  // 2) الأجسام الحرة
  var cs = [];
  for (i = 0; i < bodies.length; i++) {
    b = bodies[i];
    if (isCircBody(b)) {
      if (b.fixed) {
        b.vx = 0; b.vy = 0;
        if (isRoll(b)) { b.angle += b.w * dt; b.w *= Math.pow(0.5, dt); }
      } else if (!isDragging(b, "main")) {
        stepCircle(b, dt);
      }
      cs.push(circ(b));
    } else if (b.type === "spring") {
      // قانون هوك: F = -k (L - L0)  (الكتلة = 1)
      if (!isDragging(b, "bob")) {
        var dx = b.bx - b.x, dy = b.by - b.y;
        var L = Math.sqrt(dx * dx + dy * dy); if (L < 1) L = 1;
        var f = -b.k * (L - b.rest);
        b.bvx += (f * dx / L) * dt;
        b.bvy += (f * dy / L + G) * dt;
        b.bvx *= (1 - 0.6 * dt); b.bvy *= (1 - 0.6 * dt);
        b.bx += b.bvx * dt; b.by += b.bvy * dt;
        if (b.by + BOB_R > H - GROUND) { b.by = H - GROUND - BOB_R; b.bvy = -b.bvy * 0.5; }
        if (b.bx - BOB_R < 0) { b.bx = BOB_R; b.bvx = -b.bvx * 0.5; }
        if (b.bx + BOB_R > W) { b.bx = W - BOB_R; b.bvx = -b.bvx * 0.5; }
      }
      cs.push(circ(b));
    } else if (b.type === "pendulum") {
      if (!isDragging(b, "bob")) {
        var al = -(G / b.len) * Math.sin(b.th) - 0.15 * b.om;
        b.om += al * dt; b.th += b.om * dt;
      }
    } else if (b.type === "weight") {
      stepWeight(b, dt);
    } else if (b.type === "slider") {
      stepSlider(b, dt);
    } else if (b.type === "rod") {
      stepRod(b, dt);
    } else if (isBelt(b)) {
      stepBelt(b);
    }
  }

  // 3) تصادم الدوائر (كتل غير متساوية؛ المثبّت كتلته لانهائية)
  for (i = 0; i < cs.length; i++) {
    for (j = i + 1; j < cs.length; j++) {
      var A = cs[i], B = cs[j], oa = A.o, ob = B.o, tot = A.im + B.im;
      if (!tot) continue;
      var ddx = ob[B.x] - oa[A.x], ddy = ob[B.y] - oa[A.y];
      var d = Math.sqrt(ddx * ddx + ddy * ddy), mr = A.r + B.r;
      if (d < mr && d > 0.001) {
        var nx = ddx / d, ny = ddy / d, ov = mr - d;
        oa[A.x] -= nx * ov * A.im / tot; oa[A.y] -= ny * ov * A.im / tot;
        ob[B.x] += nx * ov * B.im / tot; ob[B.y] += ny * ov * B.im / tot;
        var rv = (ob[B.vx] - oa[A.vx]) * nx + (ob[B.vy] - oa[A.vy]) * ny;
        if (rv < 0) {
          var imp = -1.7 * rv / tot;
          oa[A.vx] -= imp * A.im * nx; oa[A.vy] -= imp * A.im * ny;
          ob[B.vx] += imp * B.im * nx; ob[B.vy] += imp * B.im * ny;
        }
      }
    }
  }

  // 4) المفاتيح الحدية: تتفعل إذا لامسها أي جسم آخر
  for (i = 0; i < bodies.length; i++) {
    b = bodies[i];
    if (b.type !== "limit_switch") continue;
    b.hit = false;
    for (j = 0; j < bodies.length; j++) {
      if (bodies[j] !== b && touches(b, bodies[j])) { b.hit = true; break; }
    }
  }
}

// ---------------------------------------------------------------- الرسم
function gearPath(r, n) {
  var ri = r - 3, ro = r + 8, s = 2 * Math.PI / n;
  ctx.beginPath();
  for (var i = 0; i < n; i++) {
    var a0 = i * s;
    var pts = [[ri, a0], [ro, a0 + s * 0.15], [ro, a0 + s * 0.45], [ri, a0 + s * 0.6]];
    for (var k = 0; k < pts.length; k++) {
      var px = Math.cos(pts[k][1]) * pts[k][0], py = Math.sin(pts[k][1]) * pts[k][0];
      if (i === 0 && k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
  }
  ctx.closePath();
}

function drawSpring(x1, y1, x2, y2) {
  var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy) || 1;
  var ux = dx / L, uy = dy / L, px = -uy, py = ux;
  var lead = Math.min(14, L * 0.2), n = 10, coil = L - 2 * lead;
  ctx.beginPath(); ctx.moveTo(x1, y1);
  ctx.lineTo(x1 + ux * lead, y1 + uy * lead);
  for (var i = 1; i <= n; i++) {
    var t = lead + coil * (i - 0.5) / n, s = (i % 2 === 0) ? -9 : 9;
    ctx.lineTo(x1 + ux * t + px * s, y1 + uy * t + py * s);
  }
  ctx.lineTo(x2 - ux * lead, y2 - uy * lead);
  ctx.lineTo(x2, y2);
  ctx.stroke();
}

function ring(x, y, r) {
  ctx.save();
  ctx.setLineDash([4, 4]); ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.stroke();
  ctx.restore();
}
function rectRing(x, y, hw, hh) {
  ctx.save();
  ctx.setLineDash([4, 4]); ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1;
  ctx.strokeRect(x - hw, y - hh, hw * 2, hh * 2);
  ctx.restore();
}

function draw() {
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = "#334155"; ctx.fillRect(0, H - GROUND, W, GROUND);
  ctx.font = "11px system-ui"; ctx.textAlign = "center";

  for (var hi = 0; hi < bodies.length; hi++) {          // خراطيم المضخة → المكبس
    var hb = bodies[hi];
    if (hb.type !== "piston") continue;
    var hl = pistonLink(hb);
    if (!hl.p) continue;
    ctx.save();
    ctx.lineWidth = 3; ctx.strokeStyle = hl.blocked ? "#ef4444" : "#38bdf8";
    ctx.setLineDash([8, 6]); ctx.lineDashOffset = hl.blocked ? 0 : -(performance.now() / 50) % 14;
    ctx.beginPath(); ctx.moveTo(hl.p.x, hl.p.y); ctx.lineTo(hb.x, hb.y); ctx.stroke();
    ctx.restore();
  }

  for (var i = 0; i < bodies.length; i++) {
    var b = bodies[i];
    ctx.save();
    if (b.type === "ball") {
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      ctx.fillStyle = "#f87171"; ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = "rgba(127,29,29,.8)"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(b.size, 0); ctx.stroke();
      ctx.fillStyle = "rgba(255,255,255,.35)"; ctx.beginPath(); ctx.arc(-b.size * 0.3, -b.size * 0.3, b.size * 0.25, 0, Math.PI * 2); ctx.fill();
    } else if (b.type === "wheel") {
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      ctx.fillStyle = "#0a0a0a"; ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.lineWidth = 1.5; ctx.strokeStyle = "#64748b";
      ctx.beginPath(); ctx.arc(0, 0, b.size * 0.55, 0, Math.PI * 2); ctx.stroke();
      for (var sp = 0; sp < 4; sp++) {
        var sa = sp * Math.PI / 2;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(sa) * b.size * 0.55, Math.sin(sa) * b.size * 0.55); ctx.stroke();
      }
      ctx.fillStyle = "#94a3b8"; ctx.beginPath(); ctx.arc(0, 0, 3, 0, Math.PI * 2); ctx.fill();
    } else if (b.type === "motor") {
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "#0c4a6e"; ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.rotate(b.angle);
      ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(b.size - 4, 0); ctx.stroke();
      ctx.rotate(-b.angle);
      ctx.fillStyle = "#e2e8f0"; ctx.fillText("M " + Math.round(b.rpm) + "rpm", 0, b.size + 16);
    } else if (b.type === "dc_motor") {
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "#431407"; ctx.strokeStyle = "#f97316"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.rotate(b.angle);
      ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(b.size - 4, 0); ctx.stroke();
      ctx.rotate(-b.angle);
      // نقطتا التوصيل (+) و (−) للربط الكهربائي لاحقاً
      ctx.fillStyle = "#ef4444"; ctx.beginPath(); ctx.arc(-b.size * 0.45, -b.size - 5, 4, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#1e293b"; ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(b.size * 0.45, -b.size - 5, 4, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = "#e2e8f0"; ctx.fillText("DC " + Math.round(b.volt) + "V " + Math.round(b.rpm) + "rpm", 0, b.size + 16);
    } else if (b.type === "gear") {
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      gearPath(b.size, teethOf(b.size));
      ctx.fillStyle = "rgba(251,191,36,.25)"; ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2;
      ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(0, 0, 5, 0, Math.PI * 2); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(b.size * 0.6, 0); ctx.stroke();
    } else if (b.type === "bevel") {
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      gearPath(b.size, teethOf(b.size));
      ctx.fillStyle = "rgba(52,211,153,.22)"; ctx.strokeStyle = "#34d399"; ctx.lineWidth = 2;
      ctx.fill(); ctx.stroke();
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(0, 0, b.size * 0.62, 0, Math.PI * 2); ctx.stroke();
      ctx.beginPath(); ctx.arc(0, 0, b.size * 0.25, 0, Math.PI * 2); ctx.stroke();
      for (var bv = 0; bv < 8; bv++) {
        var bva = bv * Math.PI / 4;
        ctx.beginPath(); ctx.moveTo(Math.cos(bva) * b.size * 0.25, Math.sin(bva) * b.size * 0.25);
        ctx.lineTo(Math.cos(bva) * b.size * 0.9, Math.sin(bva) * b.size * 0.9); ctx.stroke();
      }
    } else if (b.type === "worm") {
      var wl = b.size, wh = b.size * 0.55, wph = ((b.angle * 2.5) % 8 + 8) % 8;
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "rgba(244,114,182,.18)"; ctx.fillRect(-wl, -wh, wl * 2, wh * 2);
      ctx.save();
      ctx.beginPath(); ctx.rect(-wl, -wh, wl * 2, wh * 2); ctx.clip();
      ctx.strokeStyle = "#f472b6"; ctx.lineWidth = 2;
      for (var wx = -wl - 16 + wph; wx < wl + 8; wx += 8) {      // خطوط حلزونية تتحرك مع الدوران
        ctx.beginPath(); ctx.moveTo(wx, wh); ctx.lineTo(wx + wh * 0.9, -wh); ctx.stroke();
      }
      ctx.restore();
      ctx.strokeStyle = "#f472b6"; ctx.lineWidth = 2.5;
      ctx.strokeRect(-wl, -wh, wl * 2, wh * 2);
      ctx.beginPath(); ctx.moveTo(-wl - 8, 0); ctx.lineTo(-wl, 0); ctx.moveTo(wl, 0); ctx.lineTo(wl + 8, 0); ctx.stroke();
    } else if (b.type === "flywheel") {
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      ctx.fillStyle = "#1e293b"; ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 7;
      ctx.beginPath(); ctx.arc(0, 0, b.size - 3, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.lineWidth = 3; ctx.strokeStyle = "#64748b";
      for (var fs = 0; fs < 6; fs++) {
        var fa = fs * Math.PI / 3;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(fa) * (b.size - 8), Math.sin(fa) * (b.size - 8)); ctx.stroke();
      }
      ctx.fillStyle = "#94a3b8"; ctx.beginPath(); ctx.arc(0, 0, b.size * 0.18, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#fbbf24"; ctx.beginPath(); ctx.arc(b.size - 3, 0, 4, 0, Math.PI * 2); ctx.fill();
    } else if (b.type === "pulley") {
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      ctx.strokeStyle = "#c084fc"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.stroke();
      ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(0, 0, b.size - 6, 0, Math.PI * 2); ctx.stroke();
      for (var s = 0; s < 3; s++) {
        var a = s * Math.PI * 2 / 3;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * (b.size - 6), Math.sin(a) * (b.size - 6)); ctx.stroke();
      }
    } else if (b.type === "spring") {
      ctx.strokeStyle = "#4ade80"; ctx.lineWidth = 2.5; ctx.lineJoin = "round";
      drawSpring(b.x, b.y, b.bx, b.by);
      ctx.fillStyle = "#94a3b8"; ctx.fillRect(b.x - 8, b.y - 6, 16, 6);
      ctx.fillStyle = "#4ade80"; ctx.beginPath(); ctx.arc(b.bx, b.by, BOB_R, 0, Math.PI * 2); ctx.fill();
    } else if (b.type === "pendulum") {
      var tx = b.x + Math.sin(b.th) * b.len, ty = b.y + Math.cos(b.th) * b.len;
      ctx.strokeStyle = "#a855f7"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(b.x, b.y); ctx.lineTo(tx, ty); ctx.stroke();
      ctx.fillStyle = "#94a3b8"; ctx.beginPath(); ctx.arc(b.x, b.y, 4, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#a855f7"; ctx.beginPath(); ctx.arc(tx, ty, 15, 0, Math.PI * 2); ctx.fill();
    } else if (b.type === "weight") {
      var ws = b.size;
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "#64748b"; ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 2.5;
      ctx.fillRect(-ws, -ws, ws * 2, ws * 2); ctx.strokeRect(-ws, -ws, ws * 2, ws * 2);
      ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(0, -ws - 4, 4, 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = "#e2e8f0"; ctx.fillText("W", 0, 4);
    } else if (b.type === "anchor") {
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "#fbbf24"; ctx.strokeStyle = "#78350f"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(-b.size * 0.5, -b.size * 0.5); ctx.lineTo(b.size * 0.5, b.size * 0.5);
      ctx.moveTo(b.size * 0.5, -b.size * 0.5); ctx.lineTo(-b.size * 0.5, b.size * 0.5); ctx.stroke();
    } else if (b.type === "beam") {
      var bhw = b.len / 2, bhh = b.size / 2;
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "#475569"; ctx.fillRect(-bhw, -bhh, b.len, b.size);
      ctx.save();
      ctx.beginPath(); ctx.rect(-bhw, -bhh, b.len, b.size); ctx.clip();
      ctx.strokeStyle = "#64748b"; ctx.lineWidth = 1.5;
      for (var bx2 = -bhw - b.size; bx2 < bhw; bx2 += 12) {
        ctx.beginPath(); ctx.moveTo(bx2, bhh); ctx.lineTo(bx2 + b.size, -bhh); ctx.stroke();
      }
      ctx.restore();
      ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 2; ctx.strokeRect(-bhw, -bhh, b.len, b.size);
    } else if (b.type === "rod") {
      var rl = dist(b.x, b.y, b.ex, b.ey), ra = Math.atan2(b.ey - b.y, b.ex - b.x);
      ctx.translate(b.x, b.y); ctx.rotate(ra);
      ctx.fillStyle = "#64748b"; ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 1.5;
      ctx.fillRect(-6, -5, rl + 12, 10); ctx.strokeRect(-6, -5, rl + 12, 10);
      ctx.fillStyle = "#0f172a"; ctx.strokeStyle = b.at ? "#fbbf24" : "#cbd5e1";
      ctx.beginPath(); ctx.arc(0, 0, 3.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = b.bt ? "#fbbf24" : "#cbd5e1";
      ctx.beginPath(); ctx.arc(rl, 0, 3.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    } else if (isBelt(b)) {
      var chn = (b.type === "chain");
      var bA = b.at ? findBody(b.at.id) : null, bB = b.bt ? findBody(b.bt.id) : null;
      ctx.lineWidth = chn ? 5 : 3; ctx.strokeStyle = chn ? "#fbbf24" : "#d4d4d8"; ctx.lineJoin = "round";
      if (bA && bB && bA !== bB) {
        var r1 = beltR(bA), r2 = beltR(bB), dd = dist(bA.x, bA.y, bB.x, bB.y);
        if (dd > Math.abs(r1 - r2) + 1) {
          var ph = Math.atan2(bB.y - bA.y, bB.x - bA.x), al = Math.acos((r1 - r2) / dd);
          if (chn) { ctx.setLineDash([7, 4]); ctx.lineDashOffset = -(bA.angle * r1); }
          ctx.beginPath();
          ctx.moveTo(bA.x + r1 * Math.cos(ph + al), bA.y + r1 * Math.sin(ph + al));
          ctx.lineTo(bB.x + r2 * Math.cos(ph + al), bB.y + r2 * Math.sin(ph + al));
          ctx.arc(bB.x, bB.y, r2, ph + al, ph - al, true);
          ctx.lineTo(bA.x + r1 * Math.cos(ph - al), bA.y + r1 * Math.sin(ph - al));
          ctx.arc(bA.x, bA.y, r1, ph - al, ph + al, true);
          ctx.closePath(); ctx.stroke();
        }
      } else {
        ctx.setLineDash([6, 4]);
        ctx.beginPath(); ctx.moveTo(b.x, b.y); ctx.lineTo(b.ex, b.ey); ctx.stroke();
      }
      ctx.setLineDash([]);
      ctx.fillStyle = "#0f172a"; ctx.lineWidth = 2;
      ctx.strokeStyle = b.at ? "#fbbf24" : (chn ? "#fcd34d" : "#d4d4d8");
      ctx.beginPath(); ctx.arc(b.x, b.y, 5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = b.bt ? "#fbbf24" : (chn ? "#fcd34d" : "#d4d4d8");
      ctx.beginPath(); ctx.arc(b.ex, b.ey, 5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    } else if (b.type === "rack") {
      ctx.translate(b.x, b.y);
      var hw = b.len / 2;
      ctx.fillStyle = "#9a3412"; ctx.strokeStyle = "#fb923c"; ctx.lineWidth = 2;
      ctx.fillRect(-hw, -7, b.len, 14); ctx.strokeRect(-hw, -7, b.len, 14);
      var n = Math.floor(b.len / PITCH), x0 = -n * PITCH / 2;
      ctx.fillStyle = "#c2410c";
      for (var t = 0; t < n; t++) {
        var tx0 = x0 + t * PITCH;
        ctx.beginPath();
        ctx.moveTo(tx0 + PITCH * 0.1, -7); ctx.lineTo(tx0 + PITCH * 0.3, -15);
        ctx.lineTo(tx0 + PITCH * 0.7, -15); ctx.lineTo(tx0 + PITCH * 0.9, -7);
        ctx.closePath(); ctx.fill(); ctx.stroke();
      }
    } else if (b.type === "pump") {
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "rgba(37,99,235,.35)"; ctx.strokeStyle = "#60a5fa"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.rotate(b.angle);
      var pr = b.size * 0.6;
      ctx.strokeStyle = "#93c5fd"; ctx.fillStyle = "#93c5fd"; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.moveTo(-pr, 0); ctx.lineTo(pr, 0); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(pr, 0); ctx.lineTo(pr - 7, -5); ctx.lineTo(pr - 7, 5); ctx.closePath(); ctx.fill();
      ctx.rotate(-b.angle);
      ctx.fillStyle = "#e2e8f0"; ctx.fillText("P " + Math.round(b.rpm) + "rpm", 0, b.size + 16);
    } else if (b.type === "piston") {
      var pv = clamp(b.val, 0, 1), pl = b.len, pyH = 14;
      ctx.translate(b.x, b.y); ctx.rotate(b.ori >= 0.5 ? -Math.PI / 2 : 0);
      var hx = -pl / 2 + 6 + (pl - 12) * pv;
      ctx.fillStyle = "rgba(56,189,248,.28)"; ctx.fillRect(-pl / 2, -pyH, hx + pl / 2, pyH * 2);
      ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5; ctx.strokeRect(-pl / 2, -pyH, pl, pyH * 2);
      ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 5;
      ctx.beginPath(); ctx.moveTo(hx, 0); ctx.lineTo(hx + pl, 0); ctx.stroke();
      ctx.fillStyle = "#94a3b8"; ctx.fillRect(hx - 3, -pyH + 2, 6, pyH * 2 - 4);
    } else if (b.type === "valve") {
      var vs = b.size, vOpen = !!b.state;
      ctx.translate(b.x, b.y);
      ctx.fillStyle = vOpen ? "rgba(34,197,94,.35)" : "rgba(239,68,68,.35)";
      ctx.strokeStyle = vOpen ? "#22c55e" : "#ef4444"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(0, -vs); ctx.lineTo(vs, 0); ctx.lineTo(0, vs); ctx.lineTo(-vs, 0); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.beginPath();
      if (vOpen) { ctx.moveTo(-vs * 0.6, 0); ctx.lineTo(vs * 0.6, 0); } else { ctx.moveTo(0, -vs * 0.6); ctx.lineTo(0, vs * 0.6); }
      ctx.stroke();
      ctx.fillStyle = "#e2e8f0"; ctx.fillText(vOpen ? "مفتوح" : "مغلق", 0, vs + 14);
    } else if (b.type === "reservoir") {
      var rw = b.len, rh = b.size, lvl = clamp(b.val, 0, 1);
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "rgba(56,189,248,.4)"; ctx.fillRect(-rw / 2, rh / 2 - rh * lvl, rw, rh * lvl);
      ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 3; ctx.lineJoin = "round";
      ctx.beginPath(); ctx.moveTo(-rw / 2, -rh / 2); ctx.lineTo(-rw / 2, rh / 2); ctx.lineTo(rw / 2, rh / 2); ctx.lineTo(rw / 2, -rh / 2); ctx.stroke();
      ctx.fillStyle = "#e2e8f0"; ctx.fillText("خزان", 0, rh / 2 + 14);
    } else if (b.type === "cam") {
      var cma = b.size + b.ecc, cmb = b.size;
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      ctx.fillStyle = "rgba(45,212,191,.25)"; ctx.strokeStyle = "#2dd4bf"; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.ellipse(0, 0, cma, cmb, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(cma * 0.8, 0); ctx.stroke();
      ctx.fillStyle = "#2dd4bf"; ctx.beginPath(); ctx.arc(0, 0, 4, 0, Math.PI * 2); ctx.fill();
    } else if (b.type === "crank") {
      var kl = b.len, kx = Math.cos(b.angle) * kl, ky = Math.sin(b.angle) * kl;
      ctx.translate(b.x, b.y);
      ctx.save();
      ctx.setLineDash([3, 4]); ctx.strokeStyle = "#475569"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(-kl - 8, 0); ctx.lineTo(kl + 8, 0); ctx.stroke();
      ctx.restore();
      ctx.strokeStyle = "#f472b6"; ctx.lineWidth = 5; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(kx, ky); ctx.stroke();
      ctx.fillStyle = "#0f172a"; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.arc(0, 0, b.size * 0.6, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(kx, ky, 6, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = "#f472b6"; ctx.fillRect(kx - 5, -5, 10, 10);
    } else if (b.type === "actuator") {
      var aL = actLen(b), aHous = b.rest * 0.85;
      ctx.translate(b.x, b.y); ctx.rotate(b.deg * Math.PI / 180);
      ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 5; ctx.lineCap = "round";   // القضيب: خط متغير الطول
      ctx.beginPath(); ctx.moveTo(aHous, 0); ctx.lineTo(aL, 0); ctx.stroke();
      ctx.fillStyle = "rgba(251,146,60,.35)"; ctx.strokeStyle = "#fb923c"; ctx.lineWidth = 2.5;
      ctx.fillRect(-8, -8, aHous + 8, 16); ctx.strokeRect(-8, -8, aHous + 8, 16);
      ctx.fillStyle = "#0f172a"; ctx.beginPath(); ctx.arc(0, 0, 4, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = b.state ? "#fbbf24" : "#64748b";
      ctx.beginPath(); ctx.arc(aL, 0, 5, 0, Math.PI * 2); ctx.fill();
    } else if (b.type === "slider") {
      ctx.strokeStyle = "#64748b"; ctx.lineWidth = 4; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(b.bx - b.len / 2, b.y); ctx.lineTo(b.bx + b.len / 2, b.y); ctx.stroke();
      ctx.lineWidth = 2; ctx.strokeStyle = "#94a3b8";
      ctx.beginPath();
      ctx.moveTo(b.bx - b.len / 2, b.y - 8); ctx.lineTo(b.bx - b.len / 2, b.y + 8);
      ctx.moveTo(b.bx + b.len / 2, b.y - 8); ctx.lineTo(b.bx + b.len / 2, b.y + 8);
      ctx.stroke();
      ctx.fillStyle = "#0e7490"; ctx.strokeStyle = "#22d3ee"; ctx.lineWidth = 2.5;
      ctx.fillRect(b.x - b.size, b.y - 11, b.size * 2, 22); ctx.strokeRect(b.x - b.size, b.y - 11, b.size * 2, 22);
      ctx.fillStyle = "#0f172a"; ctx.beginPath(); ctx.arc(b.x, b.y, 3, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    } else if (b.type === "limit_switch") {
      var lh = !!b.hit;
      ctx.translate(b.x, b.y);
      if (lh) { ctx.shadowColor = "#ef4444"; ctx.shadowBlur = 16; }
      ctx.fillStyle = lh ? "rgba(239,68,68,.6)" : "rgba(51,65,85,.9)"; ctx.strokeStyle = lh ? "#ef4444" : "#64748b"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.shadowBlur = 0;
      ctx.fillStyle = lh ? "#fecaca" : "#22c55e";
      ctx.beginPath(); ctx.arc(0, 0, b.size * 0.4, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#e2e8f0"; ctx.fillText(lh ? "ON" : "LS", 0, b.size + 14);
    }
    ctx.restore();
  }

  if (sel && bodies.indexOf(sel) >= 0) {
    if (sel.type === "spring") ring(sel.bx, sel.by, BOB_R + 5);
    else if (sel.type === "pendulum") ring(sel.x + Math.sin(sel.th) * sel.len, sel.y + Math.cos(sel.th) * sel.len, 20);
    else if (isLink(sel)) { ring(sel.x, sel.y, 12); ring(sel.ex, sel.ey, 12); }
    else if (sel.type === "rack") {
      ctx.save(); ctx.setLineDash([4, 4]); ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1;
      ctx.strokeRect(sel.x - sel.len / 2 - 4, sel.y - 19, sel.len + 8, 34); ctx.restore();
    }
    else if (sel.type === "piston") ring(sel.x, sel.y, sel.len / 2 + 14);
    else if (sel.type === "reservoir") {
      ctx.save(); ctx.setLineDash([4, 4]); ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1;
      ctx.strokeRect(sel.x - sel.len / 2 - 6, sel.y - sel.size / 2 - 6, sel.len + 12, sel.size + 12); ctx.restore();
    }
    else if (sel.type === "cam") ring(sel.x, sel.y, sel.size + sel.ecc + 6);
    else if (sel.type === "crank") ring(sel.x, sel.y, sel.len + 10);
    else if (sel.type === "actuator") { var stp = actTip(sel); ring(sel.x, sel.y, 12); ring(stp.x, stp.y, 12); }
    else if (sel.type === "slider") rectRing(sel.x, sel.y, sel.size + 5, 16);
    else if (sel.type === "beam") rectRing(sel.x, sel.y, sel.len / 2 + 5, sel.size / 2 + 5);
    else if (sel.type === "weight") rectRing(sel.x, sel.y, sel.size + 5, sel.size + 5);
    else ring(sel.x, sel.y, (isRot(sel) ? sel.size + 12 : sel.size + 6));
    if (sel.fixed && hasFixed(sel)) {
      ctx.fillStyle = "#fbbf24"; ctx.textAlign = "left";
      ctx.fillText("📌", sel.x - 6, sel.y - 14 - ((isCircBody(sel) || sel.type === "weight") ? sel.size : 0));
      ctx.textAlign = "center";
    }
  }
  ctx.fillStyle = "#64748b"; ctx.textAlign = "left";
  ctx.fillText("g = " + (G / PX_PER_M).toFixed(1) + " m/s²", 8, 14);
}

function loop(t) {
  var dt = Math.min(0.05, ((t - last) / 1000) || 0);
  last = t;
  if (!paused) {
    acc += dt;
    var n = 0;
    while (acc >= 1 / 120 && n < 10) { step(1 / 120); acc -= 1 / 120; n++; }
  }
  draw();
  requestAnimationFrame(loop);
}

// ---------------------------------------------------------------- لوحة الخصائص
function hideProps() { props.style.display = "none"; }
function hasFixed(b) { return b.type !== "spring" && b.type !== "pendulum" && !isBelt(b) && NEW_TYPES.indexOf(b.type) < 0; }
function fieldsFor(b) {
  var f = [];
  if (isCircBody(b)) f.push({ k: "size", l: "نصف القطر", min: 8, max: 120, step: 1 });
  if (isMotor(b)) f.push({ k: "rpm", l: "السرعة rpm", min: -300, max: 300, step: 1 });
  if (b.type === "dc_motor") f.push({ k: "volt", l: "الجهد V", min: 1, max: 48, step: 1 });
  if (b.type === "flywheel") f.push({ k: "rpm", l: "سرعة ابتدائية rpm", min: -300, max: 300, step: 1 });
  if (b.type === "weight") f.push({ k: "size", l: "نصف الضلع", min: 8, max: 60, step: 1 });
  if (b.type === "beam") {
    f.push({ k: "len", l: "الطول", min: 40, max: 400, step: 1 });
    f.push({ k: "size", l: "السماكة", min: 6, max: 40, step: 1 });
  }
  if (b.type === "spring") {
    f.push({ k: "k", l: "ثابت النابض k", min: 5, max: 400, step: 1 });
    f.push({ k: "rest", l: "الطول الطبيعي", min: 30, max: 300, step: 1 });
  }
  if (b.type === "pendulum") f.push({ k: "len", l: "الطول", min: 40, max: 300, step: 1 });
  if (b.type === "rod") f.push({ k: "len", l: "الطول", min: 20, max: 300, step: 1 });
  if (b.type === "rack") f.push({ k: "len", l: "الطول", min: 60, max: 400, step: 1 });
  if (b.type === "pump") {
    f.push({ k: "size", l: "نصف القطر", min: 12, max: 60, step: 1 });
    f.push({ k: "rpm", l: "سرعة الضخ rpm", min: 0, max: 300, step: 1 });
  }
  if (b.type === "piston") {
    f.push({ k: "len", l: "الطول", min: 40, max: 200, step: 1 });
    f.push({ k: "spd", l: "السرعة", min: 0.1, max: 5, step: 0.1 });
    f.push({ k: "ori", l: "الاتجاه (0 أفقي، 1 رأسي)", min: 0, max: 1, step: 1 });
  }
  if (b.type === "valve") f.push({ k: "size", l: "الحجم", min: 10, max: 40, step: 1 });
  if (b.type === "reservoir") {
    f.push({ k: "len", l: "العرض", min: 40, max: 250, step: 1 });
    f.push({ k: "size", l: "الارتفاع", min: 30, max: 120, step: 1 });
    f.push({ k: "val", l: "مستوى السائل (0-1)", min: 0, max: 1, step: 0.05 });
  }
  if (b.type === "cam") {
    f.push({ k: "size", l: "نصف القطر", min: 10, max: 80, step: 1 });
    f.push({ k: "ecc", l: "الانحراف", min: 0, max: 40, step: 1 });
    f.push({ k: "rpm", l: "السرعة rpm", min: -300, max: 300, step: 1 });
  }
  if (b.type === "crank") {
    f.push({ k: "len", l: "طول الذراع", min: 15, max: 120, step: 1 });
    f.push({ k: "rpm", l: "السرعة rpm", min: -300, max: 300, step: 1 });
  }
  if (b.type === "actuator") {
    f.push({ k: "len", l: "أقصى طول", min: 40, max: 300, step: 1 });
    f.push({ k: "rest", l: "أدنى طول", min: 20, max: 250, step: 1 });
    f.push({ k: "deg", l: "الزاوية (0 يمين، 90 أسفل)", min: -180, max: 180, step: 1 });
    f.push({ k: "spd", l: "السرعة", min: 0.1, max: 5, step: 0.1 });
  }
  if (b.type === "slider") {
    f.push({ k: "len", l: "طول السكة", min: 60, max: 400, step: 1 });
    f.push({ k: "size", l: "نصف عرض الكتلة", min: 8, max: 60, step: 1 });
    f.push({ k: "k", l: "ثابت الإرجاع (0 = حر)", min: 0, max: 400, step: 1 });
  }
  if (b.type === "limit_switch") f.push({ k: "size", l: "الحجم", min: 8, max: 40, step: 1 });
  return f;
}
function applyProp(b, f, raw) {
  var v = parseFloat(raw);
  if (!isFinite(v)) return;
  v = clamp(v, f.min, f.max);
  if (f.k === "len" && b.type === "rod") setRodLen(b, v);
  else b[f.k] = v;
  if (b.type === "rack") { var hw = Math.min(b.len / 2, W / 2); b.x = clamp(b.x, hw, W - hw); }
  if (b.type === "actuator" && b.rest > b.len - 5) b.rest = b.len - 5;
  if (b.type === "flywheel" && f.k === "rpm") { b.w = b.rpm * 2 * Math.PI / 60; b.fw = b.w; }
  if ((isCircBody(b) || b.type === "weight") && b.y + b.size > H - GROUND && !b.fixed) b.y = H - GROUND - b.size;
}
function showProps(b) {
  document.getElementById("out").style.display = "none";
  document.getElementById("pTitle").textContent = NAMES[b.type] || b.type;
  pFields.innerHTML = "";
  var defs = fieldsFor(b);
  defs.forEach(function (f) {
    var lab = document.createElement("label");
    lab.appendChild(document.createTextNode(f.l));
    var inp = document.createElement("input");
    inp.type = "number"; inp.min = f.min; inp.max = f.max; inp.step = f.step;
    inp.value = Math.round(b[f.k] * 100) / 100;
    inp.addEventListener("input", function () { applyProp(b, f, inp.value); });
    inp.addEventListener("change", function () { applyProp(b, f, inp.value); inp.value = Math.round(b[f.k] * 100) / 100; });
    lab.appendChild(inp); pFields.appendChild(lab);
  });
  if (hasFixed(b)) {
    var fb = document.createElement("button");
    var paintFix = function () {
      fb.textContent = b.fixed ? "📌 إلغاء التثبيت" : "📌 تثبيت";
      fb.className = b.fixed ? "primary" : "";
    };
    fb.addEventListener("click", function () {
      b.fixed = !b.fixed;
      if (b.fixed) { b.vx = 0; b.vy = 0; b.ox = b.x; b.oy = b.y; b.eox = b.ex; b.eoy = b.ey; }
      paintFix();
    });
    paintFix();
    pFields.appendChild(fb);
  }
  if (b.type === "valve") {
    var vb = document.createElement("button");
    var paintV = function () {
      vb.textContent = b.state ? "🟢 مفتوح (اضغط للإغلاق)" : "🔴 مغلق (اضغط للفتح)";
      vb.className = b.state ? "primary" : "danger";
    };
    vb.addEventListener("click", function () { b.state = !b.state; paintV(); });
    paintV();
    pFields.appendChild(vb);
  }
  if (b.type === "actuator") {
    var ab = document.createElement("button");
    var paintA = function () {
      ab.textContent = b.state ? "⏸ إيقاف المشغل" : "▶ تشغيل المشغل";
      ab.className = b.state ? "primary" : "";
    };
    ab.addEventListener("click", function () { b.state = !b.state; paintA(); });
    paintA();
    pFields.appendChild(ab);
  }
  if (HINTS[b.type]) {
    var hint = document.createElement("span");
    hint.style.fontSize = "12px";
    hint.textContent = HINTS[b.type];
    pFields.appendChild(hint);
  }
  if (isLink(b) && (b.at || b.bt)) {
    var ub = document.createElement("button");
    ub.textContent = "فك الربط";
    ub.addEventListener("click", function () { b.at = null; b.bt = null; ub.style.display = "none"; });
    pFields.appendChild(ub);
  }
  props.style.display = "block";
}

// ---------------------------------------------------------------- السحب والإفلات
function pt(e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }

function segDist(px, py, x1, y1, x2, y2) {
  var dx = x2 - x1, dy = y2 - y1, l2 = dx * dx + dy * dy;
  var t = l2 ? clamp(((px - x1) * dx + (py - y1) * dy) / l2, 0, 1) : 0;
  return dist(px, py, x1 + t * dx, y1 + t * dy);
}

function pick(p) {
  var best = null, bd = 1e9;
  function test(b, part, d, r) {
    if (d <= r && d < bd) { bd = d; best = { b: b, part: part }; }
  }
  for (var i = bodies.length - 1; i >= 0; i--) {
    var b = bodies[i];
    if (b.type === "spring") {
      test(b, "bob", dist(p.x, p.y, b.bx, b.by), 24); test(b, "main", dist(p.x, p.y, b.x, b.y), 22);
    } else if (b.type === "pendulum") {
      test(b, "bob", dist(p.x, p.y, b.x + Math.sin(b.th) * b.len, b.y + Math.cos(b.th) * b.len), 26);
      test(b, "main", dist(p.x, p.y, b.x, b.y), 22);
    } else if (isLink(b)) {
      if (!isBelt(b) || !b.at) test(b, "a", dist(p.x, p.y, b.x, b.y), 22);
      if (!isBelt(b) || !b.bt) test(b, "b", dist(p.x, p.y, b.ex, b.ey), 22);
      test(b, "mid", segDist(p.x, p.y, b.x, b.y, b.ex, b.ey) + 6, 20);
    } else if (b.type === "rack") {
      if (Math.abs(p.x - b.x) <= b.len / 2 + 6 && p.y >= b.y - 20 && p.y <= b.y + 12) test(b, "main", 5, 6);
    } else if (b.type === "piston") {
      test(b, "main", dist(p.x, p.y, b.x, b.y), Math.max(26, b.len / 2 + 8));
    } else if (b.type === "reservoir") {
      if (Math.abs(p.x - b.x) <= b.len / 2 + 6 && Math.abs(p.y - b.y) <= b.size / 2 + 6) test(b, "main", dist(p.x, p.y, b.x, b.y), 1e9);
    } else if (b.type === "cam") {
      test(b, "main", dist(p.x, p.y, b.x, b.y), b.size + b.ecc + 10);
    } else if (b.type === "crank") {
      test(b, "main", dist(p.x, p.y, b.x, b.y), Math.max(b.len, 16) + 12);
    } else if (b.type === "actuator") {
      var pt2 = actTip(b);
      test(b, "main", Math.min(dist(p.x, p.y, b.x, b.y), segDist(p.x, p.y, b.x, b.y, pt2.x, pt2.y)), 22);
    } else if (b.type === "slider") {
      if (Math.abs(p.x - b.x) <= b.size + 8 && Math.abs(p.y - b.y) <= 20) test(b, "main", dist(p.x, p.y, b.x, b.y), 1e9);
    } else if (b.type === "beam") {
      if (Math.abs(p.x - b.x) <= b.len / 2 + 6 && Math.abs(p.y - b.y) <= b.size / 2 + 8) test(b, "main", dist(p.x, p.y, b.x, b.y), 1e9);
    } else if (b.type === "weight") {
      if (Math.abs(p.x - b.x) <= b.size + 8 && Math.abs(p.y - b.y) <= b.size + 8) test(b, "main", dist(p.x, p.y, b.x, b.y), 1e9);
    } else {
      test(b, "main", dist(p.x, p.y, b.x, b.y), isRot(b) ? b.size + 12 : b.size + 10);
    }
  }
  return best;
}

cv.addEventListener("pointerdown", function (e) {
  var p = pt(e);
  drag = pick(p);
  if (drag) {
    sel = drag.b;
    drag.sx = p.x; drag.sy = p.y; drag.lx = p.x; drag.ly = p.y; drag.lt = performance.now(); drag.moved = false;
    try { cv.setPointerCapture(e.pointerId); } catch (err) {}
  } else { sel = null; hideProps(); }
});
cv.addEventListener("pointermove", function (e) {
  if (!drag) return;
  var p = pt(e), b = drag.b;
  if (!drag.moved) {
    if (dist(p.x, p.y, drag.sx, drag.sy) < 6) return;
    drag.moved = true;
  }
  var x = clamp(p.x, 0, W), y = clamp(p.y, 0, H - GROUND);
  if (drag.part === "bob") {
    if (b.type === "spring") { b.bx = x; b.by = y; b.bvx = 0; b.bvy = 0; }
    else { b.th = Math.atan2(x - b.x, y - b.y); b.om = 0; }
  } else if (drag.part === "a") {
    b.at = null; b.x = x; b.y = y;
  } else if (drag.part === "b") {
    b.bt = null; b.ex = x; b.ey = y;
  } else if (drag.part === "mid") {
    if (isBelt(b) && (b.at || b.bt)) return;   // الحزام/السلسلة المربوطة لا تتحرك بالسحب (استخدم فك الربط)
    var mx = x - drag.lx, my = y - drag.ly;
    b.at = null; b.bt = null;
    b.x += mx; b.y += my; b.ex += mx; b.ey += my;
    drag.lx = x; drag.ly = y;
  } else if (b.type === "slider") {
    // سحب المنزلق ينقل السكة ونقطة الإرجاع معه
    var sdx = clamp(b.x + (x - drag.lx), 20, W - 20) - b.x;
    var sdy = clamp(b.y + (y - drag.ly), 10, H - GROUND - 10) - b.y;
    b.x += sdx; b.bx += sdx; b.ox += sdx; b.y += sdy;
    drag.lx = x; drag.ly = y;
  } else {
    var now = performance.now(), dtt = Math.max(1, now - drag.lt) / 1000;
    if (isRoll(b)) {
      b.vx = clamp((x - drag.lx) / dtt, -1500, 1500);
      b.vy = clamp((y - drag.ly) / dtt, -1500, 1500);
    }
    b.x = x; b.y = y;
    drag.lx = x; drag.ly = y; drag.lt = now;
  }
});
function endDrag() {
  if (drag) {
    var b = drag.b;
    if (b.type === "valve" && !drag.moved) b.state = !b.state;      // نقرة = فتح/غلق
    if (isLink(b) && drag.moved && (drag.part === "a" || drag.part === "b")) { tryAttach(b, drag.part); refreshLen(b); }
    if (!drag.moved || props.style.display === "block") showProps(b);
  }
  drag = null;
}
cv.addEventListener("pointerup", endDrag);
cv.addEventListener("pointercancel", function () { drag = null; });

// ---------------------------------------------------------------- حفظ / تحميل / تصدير / تراجع
var undoSnap = null;
function serialize() {
  var idx = {};
  bodies.forEach(function (b, i) { idx[b.id] = i; });
  return { v: 5, g: +(G / PX_PER_M).toFixed(2), bodies: bodies.map(function (b) {
    var o = { type: b.type, x: b.x, y: b.y, size: b.size, rpm: b.rpm, k: b.k, rest: b.rest,
              len: b.len, th: b.th, fixed: !!b.fixed,
              state: !!b.state, ecc: b.ecc, spd: b.spd, ori: b.ori, level: b.val,
              volt: b.volt, deg: b.deg };
    if (b.type === "slider") { o.rx = b.bx; o.ro = b.ox; }
    if (isLink(b)) {
      o.ex = b.ex; o.ey = b.ey;
      if (b.at && idx[b.at.id] !== undefined) o.at = { i: idx[b.at.id], d: b.at.d, a: b.at.a };
      if (b.bt && idx[b.bt.id] !== undefined) o.bt = { i: idx[b.bt.id], d: b.bt.d, a: b.bt.a };
    }
    return o;
  }) };
}
function pushUndo() { try { undoSnap = JSON.stringify(serialize()); } catch (e) { undoSnap = null; } }
function loadScene(s) {
  if (!s || !s.bodies || !s.bodies.length) return false;
  var nb = [], i, it, b, o, t;
  for (i = 0; i < s.bodies.length && i < 60; i++) {
    it = s.bodies[i]; t = it ? String(it.type) : "";
    if (TYPES.indexOf(t) < 0) { nb.push(null); continue; }
    o = { size: num(it.size, 30, 8, 120), rpm: num(it.rpm, 0, -300, 300), k: num(it.k, 60, 0, 400),
          rest: num(it.rest, 90, 10, 300), len: num(it.len, 120, 20, 500), th: num(it.th, 0, -3.2, 3.2), fixed: !!it.fixed,
          state: it.state === undefined ? true : !!it.state, ecc: num(it.ecc, 12, 0, 40),
          spd: num(it.spd, 1, 0.1, 5), ori: num(it.ori, 0, 0, 1),
          volt: num(it.volt, 12, 1, 48), deg: num(it.deg, 0, -180, 180) };
    if (t === "reservoir") o.val = num(it.level, 0.6, 0, 1);
    b = mk(t, num(it.x, W / 2, 0, W), num(it.y, H / 2, 0, H), o);
    if (t === "slider") { b.bx = num(it.rx, b.x, 0, W); b.ox = num(it.ro, b.x, 0, W); }
    if (isLinkT(t)) {
      b.ex = num(it.ex, b.x + b.len, 0, W); b.ey = num(it.ey, b.y, 0, H); b.eox = b.ex; b.eoy = b.ey;
    }
    nb.push(b);
  }
  for (i = 0; i < nb.length; i++) {
    it = s.bodies[i]; b = nb[i];
    if (!b || !isLink(b)) continue;
    if (it.at && nb[it.at.i]) b.at = { id: nb[it.at.i].id, d: num(it.at.d, 0, 0, 500), a: num(it.at.a, 0, -1e6, 1e6) };
    if (it.bt && nb[it.bt.i]) b.bt = { id: nb[it.bt.i].id, d: num(it.bt.d, 0, 0, 500), a: num(it.bt.a, 0, -1e6, 1e6) };
  }
  bodies = nb.filter(function (x) { return !!x; });
  sel = null; hideProps();
  if (isFinite(parseFloat(s.g))) { var gv = num(s.g, 9.8, 0, 20); document.getElementById("gs").value = gv; setG(gv); }
  return bodies.length > 0;
}
function slotKey() { return "mech_lab_slot_" + document.getElementById("slot").value; }
function saveScene() {
  if (!bodies.length) { showOut("لا يوجد شيء لحفظه."); return; }
  try {
    localStorage.setItem(slotKey(), JSON.stringify(serialize()));
    showOut("تم الحفظ في الخانة " + document.getElementById("slot").value + " ✔");
  } catch (e) { showOut("تعذّر الحفظ على هذا الجهاز."); }
}
function loadSaved() {
  var raw = null;
  try { raw = localStorage.getItem(slotKey()); } catch (e) { showOut("تعذّر الوصول إلى التخزين."); return; }
  if (!raw) { showOut("الخانة فارغة."); return; }
  var s = null;
  try { s = JSON.parse(raw); } catch (e2) { s = null; }
  pushUndo();
  if (loadScene(s)) showOut("تم التحميل ✔"); else showOut("بيانات الحفظ غير صالحة.");
}
function undo() {
  if (!undoSnap) { showOut("لا يوجد ما يمكن التراجع عنه."); return; }
  var s = null;
  try { s = JSON.parse(undoSnap); } catch (e) { s = null; }
  undoSnap = null;
  if (!s) return;
  if (!s.bodies || !s.bodies.length) { bodies = []; sel = null; hideProps(); }
  else loadScene(s);
  showOut("تم التراجع ✔");
}
function exportImage() {
  if (!bodies.length) { showOut("لا يوجد شيء لتصديره."); return; }
  draw();
  var oc = document.createElement("canvas");
  oc.width = cv.width; oc.height = cv.height;
  var c2 = oc.getContext("2d");
  c2.fillStyle = "#0b1220"; c2.fillRect(0, 0, oc.width, oc.height);
  c2.drawImage(cv, 0, 0);
  var url = oc.toDataURL("image/png"), name = "mech_lab_" + Date.now();
  if (window.Android && Android.saveImage) { Android.saveImage(url, name); return; }
  var a = document.createElement("a");
  a.href = url; a.download = name + ".png";
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  showOut("تم تصدير الصورة.");
}
window.onImageSaved = function (ok, msg) {
  showOut(ok ? "تم حفظ الصورة في المعرض ✔\n" + msg : "تعذّر حفظ الصورة: " + msg);
};

// ---------------------------------------------------------------- الذكاء الاصطناعي
// المشهد بنفس صيغة التوليد (للإصلاح بالذكاء الاصطناعي)
function aiScene() {
  return bodies.map(function (b) {
    var o = { type: b.type, x: Math.round(b.x), y: Math.round(b.y) };
    if (isCircBody(b)) o.size = b.size;
    if (isMotor(b)) o.rpm = b.rpm;
    if (b.type === "dc_motor") o.volt = b.volt;
    if (b.type === "spring") { o.k = b.k; o.len = Math.round(b.rest); }
    if (b.type === "pendulum" || b.type === "rack") o.len = Math.round(b.len);
    if (isLink(b)) { o.x2 = Math.round(b.ex); o.y2 = Math.round(b.ey); }
    if (b.type === "pump" || b.type === "cam" || b.type === "crank") o.rpm = b.rpm;
    if (b.type === "pump" || b.type === "cam" || b.type === "valve" || b.type === "reservoir" ||
        b.type === "weight" || b.type === "limit_switch" || b.type === "beam" || b.type === "slider") o.size = b.size;
    if (b.type === "cam") o.ecc = b.ecc;
    if (b.type === "piston") { o.len = Math.round(b.len); o.spd = b.spd; }
    if (b.type === "crank") o.len = Math.round(b.len);
    if (b.type === "reservoir") { o.len = Math.round(b.len); o.level = b.val; }
    if (b.type === "valve") o.state = !!b.state;
    if (b.type === "actuator") { o.len = Math.round(b.len); o.minlen = Math.round(b.rest); o.deg = b.deg; o.spd = b.spd; }
    if (b.type === "slider") { o.len = Math.round(b.len); o.k = b.k; }
    if (b.type === "beam") o.len = Math.round(b.len);
    if (hasFixed(b)) o.fixed = !!b.fixed;
    return o;
  });
}
function askFix() {
  if (!bodies.length) { showOut("أضف عناصر أولاً ثم اطلب الإصلاح."); return; }
  var txt = document.getElementById("aiText").value.trim();
  var p = "أصلح التصميم الميكانيكي التالي ليعمل بشكل صحيح: تعشيق التروس بمسافة مركزين ≈ مجموع نصفي القطر + 8، " +
    "ووضع الجريدة تحت ترس (y الجريدة ≈ y الترس + نصف قطر الترس + 11)، وربط الأذرع والأحزمة والسلاسل بمراكز العناصر الدوّارة، " +
    "وتثبيت المحرك والتروس، وتجنب التداخل والخروج من اللوحة. اللوحة " + Math.round(W) + "x" + Math.round(H) + " بكسل والإحداثيات بالبكسل. " +
    "أعد JSON فقط بنفس الصيغة {\"bodies\":[...],\"note\":\"ما الذي أصلحته\"} بدون markdown. " +
    (txt ? "ملاحظات المستخدم: " + txt + ". " : "") +
    "التصميم الحالي: " + JSON.stringify({ bodies: aiScene() });
  sendAI("mech_fix", "fix_mechanical", p);
}
function setBusy(v) {
  busy = v;
  document.getElementById("btnGen").disabled = v;
  document.getElementById("btnExp").disabled = v;
  document.getElementById("btnFix").disabled = v;
  if (busyTimer) { clearTimeout(busyTimer); busyTimer = null; }
  if (v) busyTimer = setTimeout(function () { busy = false; setBusy(false); }, 80000);
}
function showOut(t) {
  hideProps();
  var o = document.getElementById("out");
  o.textContent = t; o.style.display = "block";
}
function sendAI(id, mode, prompt) {
  if (!(window.Android && Android.askAi)) { showOut("الذكاء الاصطناعي يعمل داخل التطبيق فقط."); return; }
  if (busy) return;
  setBusy(true);
  showOut("جارٍ المعالجة...");
  Android.askAi(id, mode, prompt);
}
function askGenerate() {
  var txt = document.getElementById("aiText").value.trim();
  if (!txt) { showOut("اكتب وصف التصميم أولاً."); return; }
  var p = "أنت مساعد لمختبر ميكانيكي ثنائي الأبعاد. أعد JSON فقط بدون أي شرح خارجه وبدون markdown بالشكل: " +
    "{\"bodies\":[{\"type\":\"motor|dc_motor|gear|worm|bevel|flywheel|pulley|spring|ball|weight|pendulum|wheel|rod|rack|belt|chain|pump|piston|valve|reservoir|actuator|cam|crank|slider|anchor|beam|limit_switch\",\"x\":0,\"y\":0,\"size\":0,\"rpm\":0,\"k\":0,\"len\":0,\"x2\":0,\"y2\":0,\"fixed\":true}],\"note\":\"شرح قصير بالعربية\"}. " +
    "اللوحة بحجم " + Math.round(W) + "x" + Math.round(H) + " بكسل (x أفقي، y رأسي من الأعلى) وأعطِ x و y بالبكسل. " +
    "الأحجام الافتراضية (نصف القطر): المحرك 28 والترس 40 والبكرة 34 والكرة 18 والعجلة 22. لتعشيق تروس اجعل المسافة بين مركزيهما قريبة من مجموع نصفي القطرين + 8. " +
    "rpm للمحرك فقط. k ثابت النابض (20 إلى 200). len طول النابض أو البندول أو الجريدة بالبكسل. " +
    "الذراع rod يمتد من (x,y) إلى (x2,y2) وينربط طرفه تلقائياً بأي ترس أو عجلة أو بكرة أو محرك أو مسمار تثبيت anchor أو منزلق slider يقع الطرف داخله. " +
    "الحزام belt والسلسلة chain يمتدان من (x,y) إلى (x2,y2): ضع طرفيهما عند مركزي عنصرين دوّارين (بكرة/ترس/محرك) فيدور الثاني بنفس اتجاه الأول وبنسبة نصفي القطر. " +
    "الجريدة rack مركزها (x,y) وأسنانها للأعلى وتتحرك أفقياً عندما يلامسها ترس يقع فوقها (y الترس ≈ y الجريدة - 11 - نصف قطر الترس). " +
    "المضخة pump (rpm) تحرّك أي مكبس piston قريب منها (حتى 220 بكسل)، والصمام valve (state=true مفتوح أو false مغلق) إن وقع على الخط بينهما وكان مغلقاً أوقف المكبس. المكبس len طوله و spd معامل سرعته. الكامة cam (size نصف قطرها، ecc انحرافها، rpm) تدفع ذراع rod يقع طرفه فوقها أو منزلقاً بجانبها. المرفق crank (len طول الذراع، rpm) ويُربط طرف الذراع rod عند نهاية ذراعه، ويربط الطرف الآخر بمركز منزلق فيصبح مرفق-منزلق. الخزان reservoir (len العرض، size الارتفاع، level من 0 إلى 1). " +
    "المشغل الخطي actuator (x,y قاعدته، len أقصى طول، minlen أدنى طول، deg اتجاهه بالدرجات: 0 يمين و90 أسفل، spd) يتمدد ويتقلص ويدفع منزلقاً. المنزلق slider (x,y مركزه، len طول سكته الأفقية، size نصف عرضه، k ثابت إرجاع). " +
    "الترس الدودي worm (size) يحرّك ترساً مجاوراً بنسبة 1:عدد الأسنان ولا يُدار إلا من محرك. الترس المخروطي bevel يتعشق مع bevel آخر. الحدافة flywheel (size) قرص ثقيل يحتفظ بدورانه. مسمار التثبيت anchor نقطة ثابتة يُربط بها طرف ذراع. العارضة beam (len العرض، size السماكة) سطح ثابت تقف عليه الكرات والأثقال. الثقل weight (size نصف الضلع) يسقط بالجاذبية. المفتاح الحدي limit_switch (size) يحمرّ عند ملامسة أي جسم. المحرك dc_motor مثل المحرك مع volt الجهد. " +
    "fixed=true يثبّت العنصر في مكانه (الافتراضي true للمحرك والترس والبكرة والجريدة و false للكرة والعجلة والذراع والثقل). الطلب: " + txt;
  sendAI("mech_gen", "generate_mechanical", p);
}
function askExplain() {
  if (!bodies.length) { showOut("أضف عناصر أولاً ثم اطلب الشرح."); return; }
  var scene = bodies.map(function (b) {
    var o = { type: b.type, x: Math.round(b.x), y: Math.round(b.y), size: b.size, rpm: b.rpm,
              k: b.k, rest: b.rest, len: Math.round(b.len), fixed: !!b.fixed, w_rad_s: +(b.w || 0).toFixed(2) };
    if (isLink(b)) { o.x2 = Math.round(b.ex); o.y2 = Math.round(b.ey); o.attachedA = !!b.at; o.attachedB = !!b.bt; }
    if (b.type === "rack") o.vx = +(b.vx || 0).toFixed(1);
    if (b.type === "piston") { o.val = +(b.val || 0).toFixed(2); o.spd = b.spd; }
    if (b.type === "valve") o.open = !!b.state;
    if (b.type === "cam") o.ecc = b.ecc;
    if (b.type === "reservoir") o.level = b.val;
    if (b.type === "actuator") { o.extension = +(b.val || 0).toFixed(2); o.minlen = Math.round(b.rest); o.deg = b.deg; o.running = !!b.state; }
    if (b.type === "slider") { o.k = b.k; o.rail = Math.round(b.len); }
    if (b.type === "limit_switch") o.pressed = !!b.hit;
    if (b.type === "dc_motor") o.volt = b.volt;
    return o;
  });
  var p = "اشرح بإيجاز وبالعربية هذا التصميم الميكانيكي وفيزياءه (الجاذبية، الاحتكاك، قانون هوك، نسب التروس، الترس الدودي والمخروطي، الجريدة والترس، ذراع التوصيل، المرفق والمنزلق، الحدافة وعزم القصور، البندول، المضخة والمكبس والصمام الهيدروليكي، المشغل الخطي، الكامة، المفتاح الحدي) في بضع جمل. المشهد: " + JSON.stringify(scene);
  sendAI("mech_exp", "explain_mechanical", p);
}
function extractJSON(t) {
  t = String(t).replace(/```json|```/g, "");
  var a = t.indexOf("{"), b = t.lastIndexOf("}");
  if (a < 0 || b <= a) return null;
  try { return JSON.parse(t.substring(a, b + 1)); } catch (e) { return null; }
}
function fromAI(d) {
  if (!d || typeof d !== "object") return null;
  var t = String(d.type || "").toLowerCase();
  if (TYPES.indexOf(t) < 0) return null;
  var x = parseFloat(d.x), y = parseFloat(d.y);
  if (!isFinite(x) || !isFinite(y)) return null;
  if (x <= 1 && y <= 1) { x *= W; y *= H; }
  var o = {};
  if (d.size !== undefined) o.size = num(d.size, 30, 8, 120);
  if (d.rpm !== undefined) o.rpm = num(d.rpm, 30, -300, 300);
  if (d.k !== undefined) o.k = num(d.k, 60, 0, 400);
  var L = (d.rest !== undefined) ? d.rest : d.len;
  if (L !== undefined) { o.rest = num(L, 90, 30, 300); o.len = num(L, 120, 20, 400); }
  if (d.angle !== undefined) o.th = num(d.angle, 0.9, -3, 3);
  if (d.fixed !== undefined) o.fixed = (d.fixed === true || d.fixed === "true");
  if (d.ecc !== undefined) o.ecc = num(d.ecc, 12, 0, 40);
  if (d.spd !== undefined) o.spd = num(d.spd, 1, 0.1, 5);
  if (d.ori !== undefined) o.ori = num(d.ori, 0, 0, 1);
  if (d.level !== undefined) o.val = num(d.level, 0.6, 0, 1);
  if (d.deg !== undefined) o.deg = num(d.deg, 0, -180, 180);
  if (d.volt !== undefined) o.volt = num(d.volt, 12, 1, 48);
  if (d.state !== undefined) o.state = !(d.state === false || d.state === "false" || d.state === "closed");
  var b = mk(t, clamp(x, 10, W - 10), clamp(y, 10, H - GROUND - 10), o);
  if (t === "piston") b.len = clamp(b.len, 40, 200);
  if (t === "actuator") {
    b.len = num(d.len, 110, 30, 300);
    b.rest = num(d.minlen, Math.round(b.len * 0.45), 10, Math.max(10, b.len - 5));
  }
  if (isLinkT(t)) {
    var x2 = parseFloat(d.x2), y2 = parseFloat(d.y2);
    if (isFinite(x2) && isFinite(y2)) {
      if (x2 <= 1 && y2 <= 1) { x2 *= W; y2 *= H; }
      b.ex = clamp(x2, 10, W - 10); b.ey = clamp(y2, 10, H - GROUND - 10);
      b.len = clamp(dist(b.x, b.y, b.ex, b.ey), 20, 500);
      b.eox = b.ex; b.eoy = b.ey;
    }
  }
  return b;
}
window.onAiResult = function (id, ok, text) {
  setBusy(false);
  if (!ok) { showOut("خطأ: " + text); return; }
  if (id === "mech_gen" || id === "mech_fix") {
    var d = extractJSON(text);
    if (!d || !d.bodies || !d.bodies.length) { showOut("تعذّر فهم رد الذكاء الاصطناعي."); return; }
    var nb = [];
    for (var i = 0; i < d.bodies.length && i < 40; i++) { var b = fromAI(d.bodies[i]); if (b) nb.push(b); }
    if (!nb.length) { showOut("لم يتم إنشاء أي عنصر صالح."); return; }
    pushUndo();
    bodies = nb; sel = null; hideProps();
    for (var r = 0; r < bodies.length; r++) {
      if (isLink(bodies[r])) { tryAttach(bodies[r], "a"); tryAttach(bodies[r], "b"); refreshLen(bodies[r]); }
    }
    if (d.note) showOut(String(d.note)); else document.getElementById("out").style.display = "none";
  } else {
    showOut(String(text));
  }
};

resize();
bodies.push(mk("motor", W * 0.3, H * 0.45, {}));
bodies.push(mk("gear", W * 0.3 + 28 + 40 + 8, H * 0.45, {}));
requestAnimationFrame(loop);
</script>
</body>
</html>
'''

# ==============================================================================
# 2. MechSimulatorActivity.kt
# ==============================================================================
MECH_ACTIVITY_KT = r'''package com.example.voiceassistant

import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import com.example.voiceassistant.data.LicenseManager
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class MechSimulatorActivity : ComponentActivity() {
    private var web: WebView? = null

    private val client: OkHttpClient by lazy {
        OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(70, TimeUnit.SECONDS)
            .build()
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val wv = WebView(this)
        wv.settings.javaScriptEnabled = true
        wv.settings.domStorageEnabled = true
        wv.webViewClient = WebViewClient()
        wv.addJavascriptInterface(Bridge(), "Android")
        web = wv
        setContentView(wv)
        wv.loadUrl("file:///android_asset/mech_sim.html")

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() { finish() }
        })
    }

    override fun onDestroy() {
        web?.removeJavascriptInterface("Android")
        web?.destroy()
        web = null
        super.onDestroy()
    }

    private fun deliver(id: String, ok: Boolean, text: String) {
        runOnUiThread {
            web?.evaluateJavascript(
                "window.onAiResult(${JSONObject.quote(id)}, $ok, ${JSONObject.quote(text)})",
                null
            )
        }
    }

    private fun deliverSaved(ok: Boolean, msg: String) {
        runOnUiThread {
            web?.evaluateJavascript("window.onImageSaved($ok, ${JSONObject.quote(msg)})", null)
        }
    }

    inner class Bridge {
        @JavascriptInterface
        fun close() { runOnUiThread { finish() } }

        @JavascriptInterface
        fun saveImage(dataUrl: String, name: String) {
            Thread {
                try {
                    val bytes = android.util.Base64.decode(dataUrl.substringAfter("base64,"), android.util.Base64.DEFAULT)
                    val fileName = name.replace(Regex("[^A-Za-z0-9_]"), "_") + ".png"
                    val savedPath: String
                    if (android.os.Build.VERSION.SDK_INT >= 29) {
                        val values = android.content.ContentValues().apply {
                            put(android.provider.MediaStore.Images.Media.DISPLAY_NAME, fileName)
                            put(android.provider.MediaStore.Images.Media.MIME_TYPE, "image/png")
                            put(android.provider.MediaStore.Images.Media.RELATIVE_PATH, "Pictures/MechLab")
                        }
                        val uri = contentResolver.insert(android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)
                            ?: throw java.io.IOException("MediaStore insert failed")
                        contentResolver.openOutputStream(uri)?.use { it.write(bytes) }
                        savedPath = "Pictures/MechLab/$fileName"
                    } else {
                        val dir = getExternalFilesDir(android.os.Environment.DIRECTORY_PICTURES) ?: filesDir
                        val f = java.io.File(dir, fileName)
                        f.writeBytes(bytes)
                        savedPath = f.absolutePath
                    }
                    deliverSaved(true, savedPath)
                } catch (e: Exception) {
                    deliverSaved(false, e.message ?: "error")
                }
            }.start()
        }

        @JavascriptInterface
        fun askAi(id: String, mode: String, payload: String) {
            Thread {
                try {
                    val base = BuildConfig.VIDEO_SERVER_URL.trim()
                        .replace("/api/generate-video", "")
                        .removeSuffix("/api")
                        .trimEnd('/')
                    val key = LicenseManager.getBackendKey()
                    val body = JSONObject()
                        .put("licenseKey", key)
                        .put("mode", mode)
                        .put("prompt", payload)
                        .put("cost", 1)
                    val req = Request.Builder()
                        .url("$base/api/ai/circuit")
                        .post(body.toString().toRequestBody("application/json".toMediaType()))
                        .build()
                    client.newCall(req).execute().use { r ->
                        val raw = r.body?.string() ?: "{}"
                        val json = try { JSONObject(raw) } catch (e: Exception) { null }
                        val text = json?.optString("text", "") ?: ""
                        if (r.isSuccessful && text.isNotEmpty()) {
                            deliver(id, true, text)
                        } else {
                            val err = json?.optString("error", "") ?: ""
                            deliver(id, false, if (err.isNotEmpty()) err else "HTTP ${r.code}")
                        }
                    }
                } catch (e: Exception) {
                    deliver(id, false, "Network Error")
                }
            }.start()
        }
    }
}
'''

# ==============================================================================
# 3. تعديل MainScreen.kt و AndroidManifest.xml
#    الفكرة: نستنسخ عنصر "مختبر الإلكترونيات" الموجود فعلاً (بكل متغيراته)
#    ونستبدل الاسم والـ Activity، فلا نفترض أسماء متغيرات غير موجودة.
# ==============================================================================
ELEC_AR = "مختبر الإلكترونيات"
ELEC_EN = "Electronics Lab"
MECH_AR = "المختبر الميكانيكي"
MECH_EN = "Mechanical Lab"

DEFAULT_ACTIVITY_BLOCK = (
    '        <activity\n'
    '            android:name=".MechSimulatorActivity"\n'
    '            android:exported="false"\n'
    '            android:theme="@style/Theme.VoiceAssistant" />\n'
)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def find_matching_paren(s, i):
    """i = فهرس '(' ، يرجع فهرس ')' المقابل مع تجاهل النصوص بين علامتي اقتباس."""
    depth = 0
    in_str = False
    j = i
    n = len(s)
    while j < n:
        c = s[j]
        if in_str:
            if c == "\\":
                j += 2
                continue
            if c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return j
        j += 1
    return -1


def patch_main_screen():
    if not os.path.isfile(MAIN_SCREEN):
        print("   ! MainScreen.kt غير موجود:", MAIN_SCREEN)
        return
    text = read_file(MAIN_SCREEN)
    if "MechSimulatorActivity" in text:
        print("   = MainScreen.kt (الزر موجود مسبقاً)")
        return

    pos = text.find(ELEC_AR)
    if pos < 0:
        pos = text.find(ELEC_EN)
    if pos < 0:
        print("   ! MainScreen.kt: لم أجد عنصر 'مختبر الإلكترونيات' - أضف الزر يدوياً")
        return

    start = text.rfind("DropdownMenuItem(", 0, pos)
    if start < 0 or pos - start > 1000:
        print("   ! MainScreen.kt: لم أجد DropdownMenuItem حول عنصر الإلكترونيات - أضف الزر يدوياً")
        return

    end = find_matching_paren(text, start + len("DropdownMenuItem"))
    if end < 0:
        print("   ! MainScreen.kt: تعذر تحديد نهاية DropdownMenuItem - أضف الزر يدوياً")
        return

    block = text[start:end + 1]
    if "CircuitSimulatorActivity" not in block:
        print("   ! MainScreen.kt: عنصر الإلكترونيات لا يفتح CircuitSimulatorActivity مباشرة - أضف الزر يدوياً")
        return

    new_block = (block.replace(ELEC_AR, MECH_AR)
                      .replace(ELEC_EN, MECH_EN)
                      .replace("CircuitSimulatorActivity", "MechSimulatorActivity"))
    new_block = re.sub(r"Icons\.(Filled|Default)\.[A-Za-z]+", "Icons.Filled.Build", new_block)

    line_start = text.rfind("\n", 0, start) + 1
    indent = re.match(r"[ \t]*", text[line_start:]).group(0)
    text = text[:end + 1] + "\n" + indent + new_block + text[end + 1:]

    if "Icons.Filled.Build" in new_block and "import androidx.compose.material.icons.filled.Build" not in text:
        m = re.search(r"^import .*$", text, re.M)
        if m:
            text = text[:m.start()] + "import androidx.compose.material.icons.filled.Build\n" + text[m.start():]

    write_file(MAIN_SCREEN, text)
    print("   + MainScreen.kt (تمت إضافة زر المختبر الميكانيكي)")


def patch_manifest():
    if not os.path.isfile(MANIFEST):
        print("   ! AndroidManifest.xml غير موجود:", MANIFEST)
        return
    text = read_file(MANIFEST)
    if "MechSimulatorActivity" in text:
        print("   = AndroidManifest.xml (النشاط مسجل مسبقاً)")
        return

    anchor = text.find("CircuitSimulatorActivity")
    if anchor >= 0:
        tag_start = text.rfind("<activity", 0, anchor)
        tag_end = text.find(">", anchor)
        if tag_start >= 0 and tag_end >= 0:
            if text[tag_end - 1] == "/":
                block_end = tag_end + 1
            else:
                close = text.find("</activity>", tag_end)
                block_end = close + len("</activity>") if close >= 0 else -1
            if block_end > 0:
                block = text[tag_start:block_end]
                new_block = block.replace("CircuitSimulatorActivity", "MechSimulatorActivity")
                line_start = text.rfind("\n", 0, tag_start) + 1
                indent = re.match(r"[ \t]*", text[line_start:]).group(0)
                text = text[:block_end] + "\n" + indent + new_block + text[block_end:]
                write_file(MANIFEST, text)
                print("   + AndroidManifest.xml (تم تسجيل النشاط)")
                return

    close_app = text.find("</application>")
    if close_app >= 0:
        text = text[:close_app] + DEFAULT_ACTIVITY_BLOCK + "    " + text[close_app:]
        write_file(MANIFEST, text)
        print("   + AndroidManifest.xml (تم تسجيل النشاط قبل </application>)")
    else:
        print("   ! AndroidManifest.xml: لم أجد </application> - سجّل النشاط يدوياً")


def main():
    print(">> MECH LAB V4 applied:")
    os.makedirs(ASSETS_DIR, exist_ok=True)
    os.makedirs(PKG_DIR, exist_ok=True)
    write_file(MECH_HTML_PATH, MECH_HTML)
    write_file(MECH_ACTIVITY_PATH, MECH_ACTIVITY_KT)
    print("   + assets/mech_sim.html")
    print("   + MechSimulatorActivity.kt")
    patch_main_screen()
    patch_manifest()


if __name__ == "__main__":
    main()

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
<link rel="stylesheet" href="mech_style.css">
</head>
<body>
<header>
  <h1>المختبر الميكانيكي ⚙️</h1>
  <label>g <input id="gs" type="range" min="0" max="20" step="0.1" value="9.8" oninput="setG(this.value)"><span id="gv">9.8</span></label>
  <button id="btnPause" onclick="togglePause()">⏸</button>
  <button id="btnClose" onclick="if(window.Android&&Android.close){Android.close();}else{history.back();}">✕</button>
</header>

<!-- حاوية الأدوات الجديدة -->
<div class="toolbar-container">
  <div class="toolbar" id="tools">
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
  
  <div class="toolbar" id="tools3">
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

  <div class="toolbar" id="tools4">
    <button onclick="addBody('bearing')">+ محمل كروي</button>
    <button onclick="addBody('bearing_block')">+ بيت محمل</button>
    <button onclick="addBody('shaft')">+ عمود دوران</button>
    <button onclick="addBody('coupling')">+ وصلة عمود</button>
    <button onclick="addBody('brake')">+ فرامل</button>
    <button onclick="addBody('disc_brake')">+ قرص فرامل</button>
    <button onclick="addBody('gearbox')">+ علبة تروس</button>
    <button onclick="addBody('planetary_gear')">+ ترس كوكبي</button>
    <button onclick="addBody('chain_sprocket')">+ عجلة جنزير</button>
    <button onclick="addBody('idler')">+ ترس وسيط</button>
    <button onclick="addBody('tensioner')">+ شداد حزام</button>
    <button onclick="addBody('belt_tensioner')">+ بكرة شداد</button>
    <button onclick="addBody('hydraulic_cylinder')">+ أسطوانة هيدروليكية</button>
    <button onclick="addBody('hydraulic_motor')">+ محرك هيدروليكي</button>
    <button onclick="addBody('filter')">+ مرشح زيت</button>
    <button onclick="addBody('oil_cooler')">+ مبرد زيت</button>
    <button onclick="addBody('heat_exchanger')">+ مبادل حراري</button>
    <button onclick="addBody('fan')">+ مروحة تبريد</button>
    <button onclick="addBody('radiator')">+ مشعاع</button>
    <button onclick="addBody('compressor')">+ ضاغط هواء</button>
    <button onclick="addBody('air_tank')">+ خزان هواء</button>
    <button onclick="addBody('regulator')">+ منظم ضغط</button>
    <button onclick="addBody('lubricator')">+ مزيت</button>
    <button onclick="addBody('flow_meter')">+ مقياس تدفق</button>
    <button onclick="addBody('thermometer')">+ مقياس حرارة</button>
    <button onclick="addBody('spring_damper')">+ مخمّد نابضي</button>
    <button onclick="addBody('torsion_spring')">+ نابض لوي</button>
    <button onclick="addBody('counterweight')">+ ثقل موازن</button>
    <button onclick="addBody('hinge')">+ مفصلة</button>
    <button onclick="addBody('linear_rail')">+ سكة خطية</button>
    <button onclick="addBody('linear_bearing')">+ محمل خطي</button>
    <button onclick="addBody('shaft_support')">+ دعامة عمود</button>
    <button onclick="addBody('mechanical_seal')">+ مانع تسرب</button>
    <button onclick="addBody('gasket')">+ حشية</button>
    <button onclick="addBody('filter_screen')">+ شبكة ترشيح</button>
    <button onclick="addBody('exhaust')">+ مخرج عادم</button>
    <button onclick="addBody('intake')">+ مدخل هواء</button>
    <button onclick="addBody('combustion_chamber')">+ غرفة احتراق</button>
    <button onclick="addBody('cam_follower')">+ تابع كامة</button>
    <button onclick="addBody('eccentric')">+ لامركزي</button>
    <button onclick="addBody('vibration_motor')">+ محرك اهتزاز</button>
    <button onclick="addBody('load_cell')">+ خلية وزن</button>
    <button onclick="addBody('clamp')">+ ملزمة تثبيت</button>
    <button onclick="addBody('vise')">+ منجلة</button>
    <button onclick="addBody('drill')">+ مثقاب</button>
    <button onclick="addBody('saw')">+ منشار</button>
    <button onclick="addBody('lathe')">+ مخرطة</button>
    <button onclick="addBody('gear_sensor')">+ حساس ترس</button>
  </div>

  <div class="toolbar" id="tools5">
    <button onclick="addBody('servo_motor')">+ محرك سيرفو</button>
    <button onclick="addBody('stepper_motor')">+ محرك خطوي</button>
    <button onclick="addBody('generator')">+ مولد كهربائي</button>
    <button onclick="addBody('alternator')">+ مولد تيار متناوب</button>
    <button onclick="addBody('starter_motor')">+ محرك بادئ</button>
    <button onclick="addBody('solenoid')">+ ملف لولبي</button>
    <button onclick="addBody('electromagnet')">+ مغناطيس كهربائي</button>
    <button onclick="addBody('linear_actuator')">+ مشغل خطي كهربائي</button>
    <button onclick="addBody('ball_screw')">+ لولب كروي</button>
    <button onclick="addBody('telescopic_rail')">+ سكة تلسكوبية</button>
    <button onclick="addBody('guide_rail')">+ دليل خطي</button>
    <button onclick="addBody('linear_encoder')">+ مشفّر خطي</button>
    <button onclick="addBody('proximity_sensor')">+ حساس اقتراب</button>
    <button onclick="addBody('photo_sensor')">+ حساس ضوئي</button>
    <button onclick="addBody('temperature_sensor')">+ حساس حرارة</button>
    <button onclick="addBody('flow_control')">+ منظم تدفق</button>
    <button onclick="addBody('check_valve')">+ صمام عدم رجوع</button>
    <button onclick="addBody('relief_valve')">+ صمام تنفيس</button>
    <button onclick="addBody('directional_valve')">+ صمام اتجاهي</button>
    <button onclick="addBody('hydraulic_filter')">+ مرشح هيدروليكي</button>
    <button onclick="addBody('hydraulic_accumulator')">+ مراكم هيدروليكي</button>
    <button onclick="addBody('hydraulic_manifold')">+ مجمع هيدروليكي</button>
    <button onclick="addBody('pneumatic_cylinder')">+ أسطوانة هوائية</button>
    <button onclick="addBody('pneumatic_valve')">+ صمام هوائي</button>
    <button onclick="addBody('vacuum_pump')">+ مضخة تفريغ</button>
    <button onclick="addBody('silencer')">+ كاتم صوت</button>
    <button onclick="addBody('nozzle')">+ فوهة</button>
    <button onclick="addBody('spray_nozzle')">+ فوهة رش</button>
    <button onclick="addBody('sprocket')">+ مسنن سلسلة</button>
    <button onclick="addBody('gear_rack')">+ ترس وجريدة</button>
    <button onclick="addBody('helical_gear')">+ ترس حلزوني</button>
    <button onclick="addBody('internal_gear')">+ ترس داخلي</button>
    <button onclick="addBody('friction_wheel')">+ عجلة احتكاك</button>
    <button onclick="addBody('brake_caliper')">+ كاليبر فرامل</button>
    <button onclick="addBody('disc_coupling')">+ وصلة قرصية</button>
    <button onclick="addBody('flexible_coupling')">+ وصلة مرنة</button>
    <button onclick="addBody('flywheel_clutch')">+ قابض حدافة</button>
    <button onclick="addBody('oil_pump')">+ مضخة زيت</button>
    <button onclick="addBody('water_pump')">+ مضخة ماء</button>
    <button onclick="addBody('lubrication_unit')">+ وحدة تزييت</button>
    <button onclick="addBody('filter_dryer')">+ مجفف ومرشح هواء</button>
    <button onclick="addBody('pneumatic_regulator')">+ منظم هواء</button>
    <button onclick="addBody('pressure_switch')">+ مفتاح ضغط</button>
    <button onclick="addBody('flow_switch')">+ مفتاح تدفق</button>
    <button onclick="addBody('thermostat')">+ منظم حرارة</button>
    <button onclick="addBody('cooling_coil')">+ ملف تبريد</button>
    <button onclick="addBody('condenser')">+ مكثف</button>
    <button onclick="addBody('evaporator')">+ مبخر</button>
    <button onclick="addBody('combustion_engine')">+ محرك احتراق</button>
    <button onclick="addBody('crankshaft')">+ عمود مرفق</button>
    <button onclick="addBody('camshaft')">+ عمود كامات</button>
    <button onclick="addBody('connecting_rod')">+ ذراع توصيل</button>
    <button onclick="addBody('cylinder_head')">+ رأس أسطوانة</button>
    <button onclick="addBody('piston_ring')">+ حلقة مكبس</button>
    <button onclick="addBody('fuel_injector')">+ حاقن وقود</button>
    <button onclick="addBody('air_filter')">+ مرشح هواء</button>
    <button onclick="addBody('muffler')">+ كاتم عادم</button>
    <button onclick="addBody('exhaust_manifold')">+ مجمع عادم</button>
    <button onclick="addBody('differential_lock')">+ قفل تفاضلي</button>
    <button onclick="addBody('cv_joint')">+ مفصل سرعة ثابتة</button>
    <button onclick="addBody('torsion_bar')">+ قضيب التواء</button>
    <button onclick="addBody('leaf_spring')">+ نابض ورقي</button>
    <button onclick="addBody('coilover')">+ ممتص صدمات لولبي</button>
    <button onclick="addBody('rubber_mount')">+ قاعدة مطاطية</button>
    <button onclick="addBody('vibration_isolator')">+ عازل اهتزاز</button>
    <button onclick="addBody('load_hook')">+ خطاف حمولة</button>
    <button onclick="addBody('chain_block')">+ رافعة سلسلة</button>
    <button onclick="addBody('winch')">+ ونش</button>
    <button onclick="addBody('hoist')">+ رافعة</button>
    <button onclick="addBody('scissor_lift')">+ رافعة مقصية</button>
    <button onclick="addBody('hydraulic_jack')">+ رافعة هيدروليكية</button>
    <button onclick="addBody('clamp_cylinder')">+ أسطوانة تثبيت</button>
    <button onclick="addBody('robot_wrist')">+ معصم روبوت</button>
    <button onclick="addBody('linear_gripper')">+ قابض خطي</button>
    <button onclick="addBody('rotary_table')">+ منضدة دوارة</button>
    <button onclick="addBody('indexing_table')">+ منضدة تقسيم</button>
    <button onclick="addBody('turntable_bearing')">+ محمل منضدة دوارة</button>
    <button onclick="addBody('workpiece')">+ قطعة تشغيل</button>
    <button onclick="addBody('tool_holder')">+ حامل أداة</button>
    <button onclick="addBody('milling_cutter')">+ قاطع تفريز</button>
    <button onclick="addBody('grinding_wheel')">+ قرص تجليخ</button>
    <button onclick="addBody('drill_chuck')">+ ظرف مثقاب</button>
    <button onclick="addBody('gear_hob')">+ قاطع تروس</button>
    <button onclick="addBody('welding_torch')">+ شعلة لحام</button>
    <button onclick="addBody('cnc_spindle')">+ مغزل CNC</button>
    <button onclick="addBody('coolant_tank')">+ خزان سائل تبريد</button>
    <button onclick="addBody('chip_conveyor')">+ ناقل رايش</button>
    <button onclick="addBody('machine_guard')">+ حاجز آلة</button>
    <button onclick="addBody('safety_interlock')">+ قفل أمان</button>
    <button onclick="addBody('emergency_stop')">+ إيقاف طوارئ</button>
    <button onclick="addBody('control_panel')">+ لوحة تحكم</button>
  </div>

  <div class="toolbar" id="tools2">
    <select id="slot"><option value="1">خانة 1</option><option value="2">خانة 2</option><option value="3">خانة 3</option></select>
    <button onclick="saveScene()">💾 حفظ</button>
    <button onclick="loadSaved()">📂 تحميل</button>
    <button onclick="exportImage()">🖼 صورة</button>
    <button onclick="undo()">↩ تراجع</button>
  </div>

  <div class="toolbar" id="robotTools">
    <button class="primary" onclick="addRobotTemplate('diff')">🤖 روبوت بعجلتين</button>
    <button onclick="addRobotTemplate('rover')">🚙 روبوت استكشاف 4×4</button>
    <button onclick="addRobotTemplate('arm')">🦾 ذراع صناعي 6 محاور</button>
    <button onclick="addRobotTemplate('scara')">ذراع SCARA</button>
    <button onclick="addRobotTemplate('quadruped')">🐾 روبوت رباعي</button>
    <button onclick="addRobotTemplate('humanoid')">🧍 روبوت شبيه بالبشر</button>
    <button onclick="addRobotTemplate('drone')">🚁 مسيّرة رباعية</button>
    <button onclick="addRobotTemplate('line')">اتباع الخط</button>
    <button onclick="addRobotTemplate('delta')">روبوت دلتا</button>
    <button onclick="addBody('robot_base')">+ قاعدة روبوت</button>
    <button onclick="addBody('robot_joint')">+ مفصل ذكي</button>
    <button onclick="addBody('robot_wheel')">+ عجلة قيادة</button>
    <button onclick="addBody('lidar')">+ ليدار</button>
    <button onclick="addBody('ultrasonic')">+ حساس مسافة</button>
    <button onclick="addBody('robot_camera')">+ كاميرا</button>
    <button onclick="addBody('imu')">+ وحدة IMU</button>
    <button onclick="addBody('robot_battery')">+ بطارية</button>
    <button onclick="addBody('robot_controller')">+ متحكم</button>
    <button onclick="addBody('motor_driver')">+ مشغل محركات</button>
    <button onclick="addBody('robot_servo')">+ سيرفو مفصلي</button>
    <button onclick="addBody('robot_leg')">+ ساق روبوت</button>
    <button onclick="addBody('robot_track')">+ جنزير روبوت</button>
  </div>
</div> <!-- نهاية حاوية الأدوات -->

<div id="stage">
  <canvas id="cv"></canvas>
  <div id="props"><div class="ph"><b id="pTitle"></b><button onclick="hideProps()">إغلاق</button></div><div id="pFields"></div></div>
  <div id="out" onclick="this.style.display='none'"></div>
</div>
<div id="ai">
  <button id="btnMic" onclick="toggleVoice()" title="تحدث">🎤</button>
  <input id="aiText" placeholder="مثال: صمم نظام تروس مع محرك وجريدة">
  <button id="btnGen" class="primary" onclick="askGenerate()">ارسم</button>
  <button id="btnExp" onclick="askExplain()">اشرح</button>
  <button id="btnFix" onclick="askFix()">أصلح</button>
</div>
<script src="robot_parts.js"></script>
<script src="robot_physics.js"></script>
<script>
var W = 300, H = 300, dpr = window.devicePixelRatio || 1;
var PX_PER_M = 100;            // 100 بكسل = 1 متر
var G = 9.8 * PX_PER_M;        // الجاذبية بالبكسل/ث²
var bodies = [], paused = false, sel = null, drag = null, uid = 1;
var busy = false, busyTimer = null, last = 0, acc = 0;
var GROUND = 10, E_BALL = 0.6, E_WHEEL = 0.3, BOB_R = 12, MESH_GAP = 14;
var MU = 0.8, ROLL_RES = 0.5;                 // احتكاك الأرض ومقاومة التدحرج
var PITCH = 2 * Math.PI * 3.3;                // خطوة الأسنان (تتوافق مع عدد أسنان الترس)

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
  else if (type === "hydraulic_cylinder") { b.len = 110; b.size = 22; b.spd = 1; b.val = 0.15; }
  else if (type === "hydraulic_motor") { b.size = 24; b.rpm = 0; }
  else if (type === "air_tank") { b.len = 90; b.size = 55; b.pressure = 4; }
  else if (type === "compressor") { b.size = 26; b.rpm = 0; b.pressure = 0; }
  else if (type === "spring_damper") { b.len = 100; b.size = 20; b.k = 80; b.damp = 3; }
  else if (type === "torsion_spring") { b.size = 28; b.k = 45; }
  else if (type === "brake") { b.size = 24; b.state = true; }
  else if (type === "clutch") { b.size = 24; b.state = true; }
  else if (type === "robot_base") { b.size = 34; b.len = 92; b.fixed = false; b.cmdV = 0; b.cmdW = 0; b.heading = 0; b.battery = 100; b.autonomy = false; }
  else if (type === "robot_joint") { b.size = 14; b.angle = 0; b.minAngle = -90; b.maxAngle = 90; b.fixed = true; }
  else if (type === "robot_wheel") { b.size = 18; b.rpm = 0; b.fixed = true; }
  else if (type === "robot_servo") { b.size = 19; b.deg = 0; b.minAngle = -90; b.maxAngle = 90; }
  else if (type === "robot_battery") { b.size = 20; b.volt = 12; b.capacity = 2200; b.charge = 100; }
  else if (type === "robot_controller") { b.size = 23; b.state = true; }
  else if (type === "motor_driver") { b.size = 22; b.volt = 12; b.state = true; }
  else if (type === "lidar" || type === "ultrasonic" || type === "robot_camera" || type === "imu" || type === "line_sensor") { b.size = 15; b.range = type === "lidar" ? 150 : 90; }
  else if (type === "robot_leg" || type === "arm_link") { b.size = 12; b.len = 58; b.deg = 0; }
  else if (type === "robot_track") { b.size = 20; b.len = 95; }
  else if (type === "drone_rotor") { b.size = 20; b.rpm = 0; }
  else if (TYPES.indexOf(type) >= 0) { b.size = 24; b.len = 90; b.rpm = 0; }
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
var activeRobotBase = null;
function robotPart(type, x, y, extra) {
  var b = mk(type, clamp(x, 18, W-18), clamp(y, 18, H-24), extra || {});
  if (type === "robot_base") activeRobotBase = b;
  else if (activeRobotBase) { b.robotBaseId = activeRobotBase.id; b.localX = b.x - activeRobotBase.x; b.localY = b.y - activeRobotBase.y; }
  bodies.push(b); return b;
}
function addRobotTemplate(kind) {
  pushUndo(); activeRobotBase = null;
  var cx = W * 0.5, cy = H * 0.52, base, i;
  function part(t, dx, dy, o) { return robotPart(t, cx + dx, cy + dy, o); }
  if (kind === "diff" || kind === "rover" || kind === "line") {
    base = part("robot_base", 0, 0, {len: kind === "rover" ? 112 : 92, size: kind === "rover" ? 42 : 34, cmdV: 0, cmdW: 0});
    base.name = kind === "line" ? "روبوت تتبع خط" : (kind === "rover" ? "روبوت استكشاف" : "روبوت تفاضلي");
    part("robot_wheel", -base.len*0.34, 0, {size: 18, side: "left"});
    part("robot_wheel", base.len*0.34, 0, {size: 18, side: "right"});
    part("dc_motor", -base.len*0.34, 24, {rpm: 0, size: 15});
    part("dc_motor", base.len*0.34, 24, {rpm: 0, size: 15});
    part("ultrasonic", 0, -base.size-18, {range: 110}); part("robot_battery", -base.len*0.25, -base.size-18, {});
    part("robot_controller", base.len*0.25, -base.size-18, {});
    if (kind === "line") { part("line_sensor", -12, base.size+18, {}); part("line_sensor", 12, base.size+18, {}); }
    if (kind === "rover") { part("robot_camera", 0, -base.size-38, {}); part("lidar", 0, 0, {range: 145}); }
  } else if (kind === "arm" || kind === "scara") {
    base = part("robot_base", 0, 62, {len: 72, size: 28, fixed: true, name: "قاعدة الذراع"});
    var lengths = kind === "scara" ? [58,52,42] : [52,48,42,34,28,22];
    var px = cx, py = cy + 42;
    for (i=0;i<lengths.length;i++) {
      var j = part("robot_joint", px-cx, py-cy, {size: 12, minAngle: -150, maxAngle: 150, deg: i===0 ? -35 : 18});
      var a = (i===0 ? -0.65 : (i%2 ? 0.45 : -0.25));
      var nx = px + Math.cos(a)*lengths[i], ny = py + Math.sin(a)*lengths[i];
      robotPart("arm_link", (px+nx)/2, (py+ny)/2, {len:lengths[i],deg:a*180/Math.PI,size:9});
      px=nx; py=ny;
    }
    robotPart("gripper", px, py, {size:17}); robotPart("robot_controller", cx-42, cy+95, {}); robotPart("robot_battery", cx+42, cy+95, {});
  } else if (kind === "quadruped" || kind === "humanoid") {
    base = part("robot_base", 0, 0, {len: kind === "humanoid" ? 46 : 86, size: kind === "humanoid" ? 34 : 30, fixed: true, name: kind === "humanoid" ? "جذع روبوت" : "جسم رباعي الأرجل"});
    if (kind === "quadruped") {
      for (i=0;i<4;i++) { var dx=(i%2?1:-1)*30, dy=(i<2?-1:1)*18; robotPart("robot_joint",cx+dx,cy+dy,{size:11,deg:25}); robotPart("robot_leg",cx+dx*1.35,cy+dy*2.1,{len:42,deg:dy<0?-55:55,size:8}); }
      part("imu",0,-48,{}); part("robot_controller",0,48,{});
    } else {
      part("robot_joint",0,-42,{size:13}); part("robot_camera",0,-68,{});
      for(i=0;i<2;i++){var side=i?1:-1;part("robot_joint",side*34,-20,{size:10});part("robot_leg",side*48,8,{len:42,deg:side*45,size:8});part("robot_joint",side*12,42,{size:11});part("robot_leg",side*15,76,{len:45,deg:0,size:9});}
      part("robot_battery",-42,45,{});part("robot_controller",42,45,{});
    }
  } else if (kind === "drone" || kind === "delta") {
    base = part("robot_base",0,0,{len:70,size:25,fixed:true,name:kind==="drone"?"هيكل مسيّرة":"قاعدة دلتا"});
    if(kind === "drone") { for(i=0;i<4;i++){var a=i*Math.PI/2+Math.PI/4, dx=Math.cos(a)*48,dy=Math.sin(a)*48;part("arm_link",dx/2,dy/2,{len:66,deg:a*180/Math.PI,size:7});part("drone_rotor",dx,dy,{size:17,rpm:900});} part("imu",0,0,{});part("robot_battery",0,30,{});part("robot_camera",0,-32,{}); }
    else { for(i=0;i<3;i++){var a=i*2*Math.PI/3-Math.PI/2, dx=Math.cos(a)*55,dy=Math.sin(a)*45;part("robot_servo",dx,dy,{deg:0});part("arm_link",dx*.55,dy*.55,{len:62,deg:a*180/Math.PI,size:8});}part("gripper",0,35,{}); }
  }
  if (base) { sel=base; showProps(base); }
  activeRobotBase = null;
}
function delSel() {
  if (!sel) return;
  var i = bodies.indexOf(sel);
  if (i >= 0) bodies.splice(i, 1);
  sel = null; hideProps();
}
function clearAll() { if (bodies.length) pushUndo(); bodies = []; sel = null; hideProps(); document.getElementById("out").style.display = "none"; }

// ---------------------------------------------------------------- الفيزياء

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
    } else if (b.type === "robot_base") {
      ctx.translate(b.x,b.y); ctx.rotate(b.heading || 0);
      ctx.fillStyle="#164e63";ctx.strokeStyle="#67e8f9";ctx.lineWidth=2.5;
      ctx.beginPath();ctx.roundRect(-b.len/2,-b.size/2,b.len,b.size,10);ctx.fill();ctx.stroke();
      ctx.fillStyle="#e0f2fe";ctx.font="bold 11px system-ui";ctx.fillText("ROBOT",0,4);
      ctx.fillStyle="#fbbf24";ctx.beginPath();ctx.arc(b.len*.28,0,4,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle="#a5f3fc";ctx.beginPath();ctx.moveTo(0,-b.size/2);ctx.lineTo(0,-b.size/2-12);ctx.stroke();
    } else if (b.type === "robot_joint" || b.type === "robot_servo") {
      ctx.translate(b.x,b.y);ctx.rotate((b.deg||0)*Math.PI/180);
      ctx.fillStyle="#7c3aed";ctx.strokeStyle="#c4b5fd";ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,b.size,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(b.size+8,0);ctx.stroke();ctx.fillStyle="#fff";ctx.font="9px system-ui";ctx.fillText("J",0,3);
    } else if (b.type === "robot_wheel" || b.type === "drone_rotor") {
      ctx.translate(b.x,b.y);ctx.rotate(b.angle||0);ctx.fillStyle="#111827";ctx.strokeStyle="#94a3b8";ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,b.size,0,Math.PI*2);ctx.fill();ctx.stroke();
      for(var rw=0;rw<4;rw++){ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(rw*Math.PI/2)*b.size*.85,Math.sin(rw*Math.PI/2)*b.size*.85);ctx.stroke();}
    } else if (b.type === "lidar" || b.type === "ultrasonic" || b.type === "robot_camera" || b.type === "imu" || b.type === "line_sensor") {
      ctx.translate(b.x,b.y);ctx.fillStyle=b.type==="robot_camera"?"#1d4ed8":"#0f766e";ctx.strokeStyle="#99f6e4";ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,b.size,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.fillStyle="#f8fafc";ctx.font="9px system-ui";ctx.fillText(b.type==="lidar"?"L":b.type==="ultrasonic"?"US":b.type==="robot_camera"?"CAM":b.type==="imu"?"IMU":"IR",0,3);
      if(b.type==="lidar"||b.type==="ultrasonic"||b.type==="robot_camera"){ctx.globalAlpha=.16;ctx.fillStyle="#38bdf8";ctx.beginPath();ctx.moveTo(0,0);ctx.arc(0,0,b.range||90,-.55,.55);ctx.closePath();ctx.fill();}
    } else if (b.type === "robot_battery" || b.type === "robot_controller" || b.type === "motor_driver") {
      ctx.translate(b.x,b.y);ctx.fillStyle=b.type==="robot_battery"?"#854d0e":"#1e40af";ctx.strokeStyle="#fde68a";ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(-b.size,-b.size*.65,b.size*2,b.size*1.3,5);ctx.fill();ctx.stroke();ctx.fillStyle="#fff";ctx.font="9px system-ui";ctx.fillText(b.type==="robot_battery"?"BAT":b.type==="motor_driver"?"DRV":"CPU",0,3);
    } else if (b.type === "arm_link" || b.type === "robot_leg" || b.type === "robot_track") {
      ctx.translate(b.x,b.y);ctx.rotate((b.deg||0)*Math.PI/180);ctx.fillStyle=b.type==="robot_leg"?"#475569":"#334155";ctx.strokeStyle="#cbd5e1";ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(-b.len/2,-b.size/2,b.len,b.size,5);ctx.fill();ctx.stroke();
    } else {
      // رسم رمزي للمكونات الميكانيكية الموسعة
      ctx.translate(b.x, b.y);
      var label = NAMES[b.type] || b.type, radius = clamp(b.size || 24, 10, 60);
      var palette = ["#38bdf8","#34d399","#f59e0b","#c084fc","#fb7185"];
      var ci = Math.abs(b.type.length * 7 + b.type.charCodeAt(0)) % palette.length;
      ctx.strokeStyle = palette[ci]; ctx.fillStyle = "rgba(30,41,59,.92)"; ctx.lineWidth = 2.5;
      if (["shaft","linear_rail","hydraulic_cylinder","compressor","radiator","air_tank","gearbox","heat_exchanger","oil_cooler","lathe","drill","saw","servo_motor","stepper_motor","generator","alternator","starter_motor","solenoid","electromagnet","linear_actuator","ball_screw","pneumatic_cylinder","vacuum_pump","hydraulic_accumulator","hydraulic_manifold","combustion_engine","crankshaft","camshaft","cylinder_head","winch","hoist","hydraulic_jack","scissor_lift","control_panel","coolant_tank","chip_conveyor"].indexOf(b.type) >= 0) {
        ctx.beginPath(); ctx.rect(-radius*1.45,-radius*.55,radius*2.9,radius*1.1); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-radius,-radius*.25); ctx.lineTo(radius,radius*.25); ctx.stroke();
      } else if (["hinge","bearing","bearing_block","linear_bearing","shaft_support","coupling","idler","chain_sprocket","planetary_gear","disc_brake","fan","vibration_motor","sprocket","helical_gear","internal_gear","friction_wheel","brake_caliper","disc_coupling","flexible_coupling","rotary_table","indexing_table","turntable_bearing","grinding_wheel","drill_chuck","cnc_spindle","milling_cutter","gear_hob","robot_wrist"].indexOf(b.type) >= 0) {
        ctx.beginPath(); ctx.arc(0,0,radius,0,Math.PI*2); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.arc(0,0,radius*.38,0,Math.PI*2); ctx.stroke();
        for (var gi=0;gi<4;gi++){var ga=gi*Math.PI/2;ctx.beginPath();ctx.moveTo(Math.cos(ga)*radius*.4,Math.sin(ga)*radius*.4);ctx.lineTo(Math.cos(ga)*radius*.9,Math.sin(ga)*radius*.9);ctx.stroke();}
      } else if (["proximity_sensor","photo_sensor","temperature_sensor","pressure_switch","flow_switch","thermostat","safety_interlock","emergency_stop","check_valve","relief_valve","directional_valve","pneumatic_valve","flow_control","nozzle","spray_nozzle","fuel_injector"].indexOf(b.type) >= 0) {
        ctx.beginPath(); ctx.moveTo(0,-radius); ctx.lineTo(radius,radius*.75); ctx.lineTo(-radius,radius*.75); ctx.closePath(); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.arc(0,0,radius*.22,0,Math.PI*2); ctx.stroke();
      } else {
        ctx.beginPath(); ctx.rect(-radius,-radius*.7,radius*2,radius*1.4); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-radius*.6,0); ctx.lineTo(radius*.6,0); ctx.stroke();
      }
      ctx.fillStyle = "#e2e8f0"; ctx.font = "10px system-ui"; ctx.textAlign = "center";
      ctx.fillText(label, 0, radius + 14);
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
  if (TYPES.indexOf(b.type) >= 0 && !isCircBody(b) && !isLink(b) &&
      ["spring","pendulum","rod","rack","beam","weight","pump","piston","valve","reservoir","cam","crank","actuator","slider","limit_switch"].indexOf(b.type) < 0) {
    f.push({ k: "size", l: "الحجم", min: 8, max: 80, step: 1 });
    f.push({ k: "len", l: "الطول", min: 20, max: 300, step: 1 });
    if (["shaft","fan","compressor","hydraulic_motor","vibration_motor","drill","lathe"].indexOf(b.type) >= 0)
      f.push({ k: "rpm", l: "السرعة rpm", min: -500, max: 500, step: 1 });
  }

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
  if (b.type === "hydraulic_cylinder") {
    f.push({ k: "len", l: "طول الأسطوانة", min: 50, max: 220, step: 1 });
    f.push({ k: "spd", l: "معامل السرعة", min: 0.1, max: 4, step: 0.1 });
  }
  if (b.type === "hydraulic_motor") f.push({ k: "spd", l: "معامل السرعة", min: 0.1, max: 4, step: 0.1 });
  if (b.type === "compressor") f.push({ k: "pressure", l: "الضغط المتراكم bar", min: 0, max: 10, step: 0.1 });
  if (b.type === "air_tank") f.push({ k: "pressure", l: "ضغط الخزان bar", min: 0, max: 10, step: 0.1 });
  if (b.type === "spring_damper") {
    f.push({ k: "k", l: "صلابة النابض k", min: 5, max: 500, step: 1 });
    f.push({ k: "damp", l: "التخميد", min: 0, max: 20, step: 0.1 });
  }
  if (b.type === "torsion_spring") f.push({ k: "k", l: "ثابت الالتواء", min: 5, max: 300, step: 1 });
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
  if (b.type === "brake" || b.type === "clutch") {
    var mb = document.createElement("button");
    var paintM = function () {
      mb.textContent = b.type === "brake" ? (b.state ? "🟢 الفرامل محررة" : "🔴 تفعيل الفرامل") : (b.state ? "🟢 القابض موصول" : "🔴 القابض مفصول");
      mb.className = b.state ? "primary" : "danger";
    };
    mb.addEventListener("click", function () { b.state = !b.state; paintM(); });
    paintM(); pFields.appendChild(mb);
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
  if (["flow_meter","thermometer","air_tank","compressor","hydraulic_cylinder","hydraulic_motor"].indexOf(b.type) >= 0) {
    var meter = document.createElement("span"); meter.style.fontSize = "12px";
    if (b.type === "flow_meter") meter.textContent = "القراءة الحالية: " + (b.reading || 0).toFixed(2) + " وحدة تدفق";
    else if (b.type === "thermometer") meter.textContent = "الحرارة التقديرية: " + (b.reading || 20).toFixed(1) + " °C";
    else if (b.type === "air_tank" || b.type === "compressor") meter.textContent = "الضغط الحالي: " + (b.pressure || 0).toFixed(2) + " bar";
    else if (b.type === "hydraulic_cylinder") meter.textContent = "التدفق: " + (b.flow || 0).toFixed(2) + " دورة/ث";
    else meter.textContent = "سرعة المحرك الهيدروليكي: " + ((b.w || 0) * 60 / (2 * Math.PI)).toFixed(1) + " rpm";
    pFields.appendChild(meter);
  }
  if (b.type === "robot_base") {
    var drive = document.createElement("div"); drive.style.display="flex"; drive.style.flexWrap="wrap"; drive.style.gap="6px";
    function cmd(label,v,w){var bt=document.createElement("button");bt.textContent=label;bt.onclick=function(){b.autonomy=false;b.cmdV=v;b.cmdW=w;};drive.appendChild(bt);}
    cmd("⬆ أمام",45,0);cmd("⬇ خلف",-35,0);cmd("↶ يسار",0,-1.2);cmd("↷ يمين",0,1.2);
    var stop=document.createElement("button");stop.textContent="⏹ توقف";stop.className="danger";stop.onclick=function(){b.cmdV=0;b.cmdW=0;b.autonomy=false;};drive.appendChild(stop);
    var auto=document.createElement("button");auto.textContent=b.autonomy?"إيقاف الذاتي":"تشغيل تجوال ذاتي";auto.onclick=function(){b.autonomy=!b.autonomy;b.cmdV=0;b.cmdW=0;showProps(b);};drive.appendChild(auto);
    pFields.appendChild(drive);
    f.push({k:"cmdV",l:"السرعة",min:-100,max:100,step:1},{k:"cmdW",l:"الدوران",min:-2.5,max:2.5,step:0.1},{k:"battery",l:"شحن البطارية %",min:0,max:100,step:1});
  }
  if (b.type === "robot_joint" || b.type === "robot_servo") f.push({k:"deg",l:"زاوية المفصل °",min:-180,max:180,step:1},{k:"minAngle",l:"الحد الأدنى °",min:-180,max:0,step:1},{k:"maxAngle",l:"الحد الأعلى °",min:0,max:180,step:1});
  if (b.type === "robot_battery") f.push({k:"volt",l:"الجهد V",min:3,max:48,step:1},{k:"capacity",l:"السعة mAh",min:500,max:20000,step:100},{k:"charge",l:"الشحن %",min:0,max:100,step:1});
  if (b.type === "lidar" || b.type === "ultrasonic") f.push({k:"range",l:"مدى الاستشعار px",min:20,max:250,step:5});
  if (b.type === "arm_link" || b.type === "robot_leg" || b.type === "robot_track") f.push({k:"len",l:"الطول",min:20,max:180,step:1},{k:"deg",l:"زاوية الوصلة °",min:-180,max:180,step:1});
  if (HINTS[b.type] || TYPES.indexOf(b.type) >= 0) {
    var hint = document.createElement("span");
    hint.style.fontSize = "12px";
    hint.textContent = HINTS[b.type] || "عنصر ميكانيكي إضافي للتركيب والتوضيح البصري. يمكن تغيير موضعه وحجمه وخصائصه؛ لا تمثل وظيفته محاكاة هندسية كاملة.";
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
              volt: b.volt, deg: b.deg, cmdV: b.cmdV, cmdW: b.cmdW, heading: b.heading,
              autonomy: b.autonomy, battery: b.battery, capacity: b.capacity, charge: b.charge,
              range: b.range, minAngle: b.minAngle, maxAngle: b.maxAngle, name: b.name, side: b.side, robotBaseIndex: undefined };
    if (b.robotBaseId !== undefined && idx[b.robotBaseId] !== undefined) { o.robotBaseIndex = idx[b.robotBaseId]; o.localX = b.localX; o.localY = b.localY; }
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
          volt: num(it.volt, 12, 1, 48), deg: num(it.deg, 0, -180, 180),
          cmdV: num(it.cmdV, 0, -100, 100), cmdW: num(it.cmdW, 0, -2.5, 2.5),
          heading: num(it.heading, 0, -100000, 100000), autonomy: !!it.autonomy,
          battery: num(it.battery, 100, 0, 100), capacity: num(it.capacity, 2200, 500, 20000),
          charge: num(it.charge, 100, 0, 100), range: num(it.range, 90, 20, 250),
          minAngle: num(it.minAngle, -90, -180, 0), maxAngle: num(it.maxAngle, 90, 0, 180),
          name: it.name, side: it.side };
    if (t === "reservoir") o.val = num(it.level, 0.6, 0, 1);
    b = mk(t, num(it.x, W / 2, 0, W), num(it.y, H / 2, 0, H), o);
    if (t === "slider") { b.bx = num(it.rx, b.x, 0, W); b.ox = num(it.ro, b.x, 0, W); }
    if (isLinkT(t)) {
      b.ex = num(it.ex, b.x + b.len, 0, W); b.ey = num(it.ey, b.y, 0, H); b.eox = b.ex; b.eoy = b.ey;
    }
    if (it.robotBaseIndex !== undefined) { b._robotBaseIndex = it.robotBaseIndex; b.localX = num(it.localX,0,-1000,1000); b.localY = num(it.localY,0,-1000,1000); }
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
  if (d.angle !== undefined) o.th = num(d
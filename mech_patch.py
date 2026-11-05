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
#stage{flex:1;position:relative;background:#0b1220;min-height:0}
canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none}
#out{display:none;position:absolute;left:8px;right:8px;bottom:8px;max-height:45%;overflow:auto;background:rgba(15,23,42,.94);border:1px solid var(--line);border-radius:10px;padding:10px;font-size:13px;line-height:1.6;white-space:pre-wrap;-webkit-user-select:text;user-select:text}
#props{display:none;position:absolute;left:8px;right:8px;bottom:8px;background:rgba(15,23,42,.96);border:1px solid var(--accent);border-radius:10px;padding:8px 10px}
#props .ph{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;font-size:14px}
#pFields{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center}
#pFields label{font-size:12px;display:flex;align-items:center;gap:6px}
#pFields input[type=number]{width:72px;padding:5px;border-radius:6px;border:1px solid #475569;background:#0b1220;color:#fff;-webkit-user-select:text;user-select:text}
#pFields input[type=checkbox]{width:18px;height:18px}
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
  <button onclick="addBody('gear')">+ ترس</button>
  <button onclick="addBody('pulley')">+ بكرة</button>
  <button onclick="addBody('spring')">+ نابض</button>
  <button onclick="addBody('ball')">+ كرة</button>
  <button onclick="addBody('pendulum')">+ بندول</button>
  <button onclick="addBody('wheel')">+ عجلة</button>
  <button onclick="addBody('rod')">+ ذراع</button>
  <button onclick="addBody('rack')">+ جريدة</button>
  <button class="danger" onclick="delSel()">حذف المحدد</button>
  <button class="danger" onclick="clearAll()">مسح</button>
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
</div>
<script>
var TYPES = ["motor", "gear", "pulley", "spring", "ball", "pendulum", "wheel", "rod", "rack"];
var NAMES = { motor: "محرك", gear: "ترس", pulley: "بكرة", spring: "نابض", ball: "كرة",
              pendulum: "بندول", wheel: "عجلة", rod: "ذراع توصيل", rack: "جريدة مسننة" };
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
function isRot(b) { return b.type === "motor" || b.type === "gear" || b.type === "pulley"; }
function isCircBody(b) { return b.type === "ball" || b.type === "wheel" || isRot(b); }
function isRoll(b) { return b.type === "ball" || b.type === "wheel"; }
function dist(x1, y1, x2, y2) { var dx = x2 - x1, dy = y2 - y1; return Math.sqrt(dx * dx + dy * dy); }

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
            fixed: (type === "ball" || type === "wheel" || type === "rod") ? false : true,
            ex: x, ey: y, ox: x, oy: y, eox: x, eoy: y, at: null, bt: null };
  if (type === "motor") { b.size = 28; b.rpm = 30; }
  else if (type === "gear") { b.size = 40; }
  else if (type === "pulley") { b.size = 34; }
  else if (type === "ball") { b.size = 18; }
  else if (type === "wheel") { b.size = 22; }
  else if (type === "pendulum") { b.th = 0.9; }
  else if (type === "rack") { b.len = 160; }
  o = o || {};
  for (var key in o) { if (o.hasOwnProperty(key)) b[key] = o[key]; }
  if (type === "spring") { b.bx = b.x; b.by = b.y + b.rest * 1.3; }
  if (type === "rod") { b.ex = b.x + b.len; b.ey = b.y; b.ox = b.x; b.oy = b.y; b.eox = b.ex; b.eoy = b.ey; }
  return b;
}

function addBody(t) {
  var x = clamp(W / 2 + (Math.random() - 0.5) * 80, 40, W - 40), y;
  if (t === "ball") y = 50;
  else if (t === "wheel") y = 60;
  else if (t === "spring" || t === "pendulum") y = 40;
  else if (t === "rod") { y = H * 0.3; x = clamp(W / 2 - 60, 10, Math.max(10, W - 140)); }
  else if (t === "rack") y = H * 0.7;
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
function clearAll() { bodies = []; sel = null; hideProps(); document.getElementById("out").style.display = "none"; }

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
  if (roll) b.angle += b.w * dt;
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
  return { x: h.x + Math.cos(ang) * at.d, y: h.y + Math.sin(ang) * at.d };
}
function stepRod(b, dt) {
  var pa = pinPos(b, "a"), pb = pinPos(b, "b");
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
    b.len = clamp(dist(b.x, b.y, b.ex, b.ey), 10, 500);   // طرفان مثبتان: الطول يتبع المسافة
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
    }
    if (imB) {
      if (b.ey > floorY) { b.ey = floorY; b.eox = b.ex - (b.ex - b.eox) * 0.9; b.eoy = b.ey; }
      b.ex = clamp(b.ex, 0, W);
    }
  }
}
function setRodLen(b, v) {
  var dx = b.ex - b.x, dy = b.ey - b.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
  b.len = v;
  if (!b.bt) { b.ex = b.x + dx / d * v; b.ey = b.y + dy / d * v; b.eox = b.ex; b.eoy = b.ey; }
  else if (!b.at) { b.x = b.ex - dx / d * v; b.y = b.ey - dy / d * v; b.ox = b.x; b.oy = b.y; }
}
function tryAttach(b, end) {
  var px = (end === "a") ? b.x : b.ex, py = (end === "a") ? b.y : b.ey;
  var best = null, bd = 1e9;
  for (var i = 0; i < bodies.length; i++) {
    var h = bodies[i];
    if (!(isRot(h) || h.type === "wheel")) continue;
    var d = dist(px, py, h.x, h.y);
    if (d <= h.size + 10 && d < bd) { bd = d; best = h; }
  }
  if (!best) return;
  var at = { id: best.id, d: bd, a: Math.atan2(py - best.y, px - best.x) - best.angle };
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
    if (nodes[i].type === "motor") { nodes[i].seen = true; nodes[i].w = nodes[i].rpm * 2 * Math.PI / 60; q.push(nodes[i]); }
  }
  while (q.length) {
    a = q.shift();
    for (j = 0; j < nodes.length; j++) {
      c = nodes[j];
      if (!c.seen && transfer(a, c)) { c.seen = true; q.push(c); }
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
      if (!b.seen) b.w *= Math.pow(0.2, dt);   // عنصر غير متصل يتوقف تدريجياً
      b.angle += b.w * dt;
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
    } else if (b.type === "rod") {
      stepRod(b, dt);
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

function draw() {
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = "#334155"; ctx.fillRect(0, H - GROUND, W, GROUND);
  ctx.font = "11px system-ui"; ctx.textAlign = "center";

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
    } else if (b.type === "gear") {
      ctx.translate(b.x, b.y); ctx.rotate(b.angle);
      gearPath(b.size, Math.max(6, Math.round(b.size / 3.3)));
      ctx.fillStyle = "rgba(251,191,36,.25)"; ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2;
      ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(0, 0, 5, 0, Math.PI * 2); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(b.size * 0.6, 0); ctx.stroke();
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
    } else if (b.type === "rod") {
      var rl = dist(b.x, b.y, b.ex, b.ey), ra = Math.atan2(b.ey - b.y, b.ex - b.x);
      ctx.translate(b.x, b.y); ctx.rotate(ra);
      ctx.fillStyle = "#64748b"; ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 1.5;
      ctx.fillRect(-6, -5, rl + 12, 10); ctx.strokeRect(-6, -5, rl + 12, 10);
      ctx.fillStyle = "#0f172a"; ctx.strokeStyle = b.at ? "#fbbf24" : "#cbd5e1";
      ctx.beginPath(); ctx.arc(0, 0, 3.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = b.bt ? "#fbbf24" : "#cbd5e1";
      ctx.beginPath(); ctx.arc(rl, 0, 3.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
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
    }
    ctx.restore();
  }

  if (sel && bodies.indexOf(sel) >= 0) {
    if (sel.type === "spring") ring(sel.bx, sel.by, BOB_R + 5);
    else if (sel.type === "pendulum") ring(sel.x + Math.sin(sel.th) * sel.len, sel.y + Math.cos(sel.th) * sel.len, 20);
    else if (sel.type === "rod") { ring(sel.x, sel.y, 12); ring(sel.ex, sel.ey, 12); }
    else if (sel.type === "rack") {
      ctx.save(); ctx.setLineDash([4, 4]); ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1;
      ctx.strokeRect(sel.x - sel.len / 2 - 4, sel.y - 19, sel.len + 8, 34); ctx.restore();
    }
    else ring(sel.x, sel.y, (isRot(sel) ? sel.size + 12 : sel.size + 6));
    if (sel.fixed && sel.type !== "spring" && sel.type !== "pendulum") {
      ctx.fillStyle = "#fbbf24"; ctx.textAlign = "left";
      ctx.fillText("📌", (sel.type === "rod" ? sel.x : sel.x) - 6, sel.y - 14 - (isCircBody(sel) ? sel.size : 0));
    }
  }
  ctx.fillStyle = "#64748b"; ctx.textAlign = "left";
  ctx.fillText("g = " + (G / PX_PER_M).toFixed(1) + " m/s\u00B2", 8, 14);
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
function hasFixed(b) { return b.type !== "spring" && b.type !== "pendulum"; }
function fieldsFor(b) {
  var f = [];
  if (isCircBody(b)) f.push({ k: "size", l: "نصف القطر", min: 8, max: 120, step: 1 });
  if (b.type === "motor") f.push({ k: "rpm", l: "السرعة rpm", min: -300, max: 300, step: 1 });
  if (b.type === "spring") {
    f.push({ k: "k", l: "ثابت النابض k", min: 5, max: 400, step: 1 });
    f.push({ k: "rest", l: "الطول الطبيعي", min: 30, max: 300, step: 1 });
  }
  if (b.type === "pendulum") f.push({ k: "len", l: "الطول", min: 40, max: 300, step: 1 });
  if (b.type === "rod") f.push({ k: "len", l: "الطول", min: 20, max: 300, step: 1 });
  if (b.type === "rack") f.push({ k: "len", l: "الطول", min: 60, max: 400, step: 1 });
  return f;
}
function applyProp(b, f, raw) {
  var v = parseFloat(raw);
  if (!isFinite(v)) return;
  v = clamp(v, f.min, f.max);
  if (f.k === "len" && b.type === "rod") setRodLen(b, v);
  else b[f.k] = v;
  if (b.type === "rack") { var hw = Math.min(b.len / 2, W / 2); b.x = clamp(b.x, hw, W - hw); }
  if (isCircBody(b) && b.y + b.size > H - GROUND && !b.fixed) b.y = H - GROUND - b.size;
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
    } else if (b.type === "rod") {
      test(b, "a", dist(p.x, p.y, b.x, b.y), 22);
      test(b, "b", dist(p.x, p.y, b.ex, b.ey), 22);
      test(b, "mid", segDist(p.x, p.y, b.x, b.y, b.ex, b.ey) + 6, 20);
    } else if (b.type === "rack") {
      if (Math.abs(p.x - b.x) <= b.len / 2 + 6 && p.y >= b.y - 20 && p.y <= b.y + 12) test(b, "main", 5, 6);
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
    var mx = x - drag.lx, my = y - drag.ly;
    b.at = null; b.bt = null;
    b.x += mx; b.y += my; b.ex += mx; b.ey += my;
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
    if (b.type === "rod" && drag.moved && (drag.part === "a" || drag.part === "b")) tryAttach(b, drag.part);
    if (!drag.moved || props.style.display === "block") showProps(b);
  }
  drag = null;
}
cv.addEventListener("pointerup", endDrag);
cv.addEventListener("pointercancel", function () { drag = null; });

// ---------------------------------------------------------------- الذكاء الاصطناعي
function setBusy(v) {
  busy = v;
  document.getElementById("btnGen").disabled = v;
  document.getElementById("btnExp").disabled = v;
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
    "{\"bodies\":[{\"type\":\"motor|gear|pulley|spring|ball|pendulum|wheel|rod|rack\",\"x\":0,\"y\":0,\"size\":0,\"rpm\":0,\"k\":0,\"len\":0,\"x2\":0,\"y2\":0,\"fixed\":true}],\"note\":\"شرح قصير بالعربية\"}. " +
    "اللوحة بحجم " + Math.round(W) + "x" + Math.round(H) + " بكسل (x أفقي، y رأسي من الأعلى) وأعطِ x و y بالبكسل. " +
    "الأحجام الافتراضية (نصف القطر): المحرك 28 والترس 40 والبكرة 34 والكرة 18 والعجلة 22. لتعشيق تروس اجعل المسافة بين مركزيهما قريبة من مجموع نصفي القطرين + 8. " +
    "rpm للمحرك فقط. k ثابت النابض (20 إلى 200). len طول النابض أو البندول أو الجريدة بالبكسل. " +
    "الذراع rod يمتد من (x,y) إلى (x2,y2) وينربط طرفه تلقائياً بأي ترس أو عجلة أو بكرة أو محرك يقع الطرف داخله. " +
    "الجريدة rack مركزها (x,y) وأسنانها للأعلى وتتحرك أفقياً عندما يلامسها ترس يقع فوقها (y الترس ≈ y الجريدة - 11 - نصف قطر الترس). " +
    "fixed=true يثبّت العنصر في مكانه (الافتراضي true للمحرك والترس والبكرة والجريدة و false للكرة والعجلة والذراع). الطلب: " + txt;
  sendAI("mech_gen", "generate_mechanical", p);
}
function askExplain() {
  if (!bodies.length) { showOut("أضف عناصر أولاً ثم اطلب الشرح."); return; }
  var scene = bodies.map(function (b) {
    var o = { type: b.type, x: Math.round(b.x), y: Math.round(b.y), size: b.size, rpm: b.rpm,
              k: b.k, rest: b.rest, len: Math.round(b.len), fixed: !!b.fixed, w_rad_s: +(b.w || 0).toFixed(2) };
    if (b.type === "rod") { o.x2 = Math.round(b.ex); o.y2 = Math.round(b.ey); o.attachedA = !!b.at; o.attachedB = !!b.bt; }
    if (b.type === "rack") o.vx = +(b.vx || 0).toFixed(1);
    return o;
  });
  var p = "اشرح بإيجاز وبالعربية هذا التصميم الميكانيكي وفيزياءه (الجاذبية، الاحتكاك، قانون هوك، نسب التروس، الجريدة والترس، ذراع التوصيل، البندول) في بضع جمل. المشهد: " + JSON.stringify(scene);
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
  if (d.k !== undefined) o.k = num(d.k, 60, 5, 400);
  var L = (d.rest !== undefined) ? d.rest : d.len;
  if (L !== undefined) { o.rest = num(L, 90, 30, 300); o.len = num(L, 120, 20, 400); }
  if (d.angle !== undefined) o.th = num(d.angle, 0.9, -3, 3);
  if (d.fixed !== undefined) o.fixed = (d.fixed === true || d.fixed === "true");
  var b = mk(t, clamp(x, 10, W - 10), clamp(y, 10, H - GROUND - 10), o);
  if (t === "rod") {
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
  if (id === "mech_gen") {
    var d = extractJSON(text);
    if (!d || !d.bodies || !d.bodies.length) { showOut("تعذّر فهم رد الذكاء الاصطناعي."); return; }
    var nb = [];
    for (var i = 0; i < d.bodies.length && i < 40; i++) { var b = fromAI(d.bodies[i]); if (b) nb.push(b); }
    if (!nb.length) { showOut("لم يتم إنشاء أي عنصر صالح."); return; }
    bodies = nb; sel = null; hideProps();
    for (var r = 0; r < bodies.length; r++) {
      if (bodies[r].type === "rod") { tryAttach(bodies[r], "a"); tryAttach(bodies[r], "b"); }
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

    inner class Bridge {
        @JavascriptInterface
        fun close() { runOnUiThread { finish() } }

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
    print(">> MECH LAB V2 applied:")
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

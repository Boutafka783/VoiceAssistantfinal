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
  <button class="danger" onclick="delSel()">حذف المحدد</button>
  <button class="danger" onclick="clearAll()">مسح</button>
</div>
<div id="stage"><canvas id="cv"></canvas><div id="out" onclick="this.style.display='none'"></div></div>
<div id="ai">
  <input id="aiText" placeholder="مثال: صمم نظام تروس مع محرك وكرة">
  <button id="btnGen" class="primary" onclick="askGenerate()">ارسم</button>
  <button id="btnExp" onclick="askExplain()">اشرح</button>
</div>
<script>
var TYPES = ["motor", "gear", "pulley", "spring", "ball", "pendulum"];
var cv = document.getElementById("cv"), ctx = cv.getContext("2d");
var W = 300, H = 300, dpr = window.devicePixelRatio || 1;
var PX_PER_M = 100;            // 100 بكسل = 1 متر
var G = 9.8 * PX_PER_M;        // الجاذبية بالبكسل/ث²
var bodies = [], paused = false, sel = null, drag = null, uid = 1;
var busy = false, busyTimer = null, last = 0, acc = 0;
var GROUND = 10, E_BALL = 0.6, BOB_R = 12, MESH_GAP = 14;

function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
function num(v, d, a, b) { v = parseFloat(v); return isFinite(v) ? clamp(v, a, b) : d; }

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
            k: 60, rest: 90, bx: x, by: y, bvx: 0, bvy: 0, len: 120, th: 0, om: 0, seen: false };
  if (type === "motor") { b.size = 28; b.rpm = 30; }
  else if (type === "gear") { b.size = 40; }
  else if (type === "pulley") { b.size = 34; }
  else if (type === "ball") { b.size = 18; }
  else if (type === "pendulum") { b.th = 0.9; }
  o = o || {};
  for (var key in o) { if (o.hasOwnProperty(key)) b[key] = o[key]; }
  if (type === "spring") { b.bx = b.x; b.by = b.y + b.rest * 1.3; }
  return b;
}

function addBody(t) {
  var x = clamp(W / 2 + (Math.random() - 0.5) * 80, 40, W - 40);
  var y = (t === "ball") ? 50 : (t === "spring" || t === "pendulum") ? 40 : H * 0.45;
  var b = mk(t, x, y, {});
  bodies.push(b); sel = b;
}
function delSel() {
  if (!sel) return;
  var i = bodies.indexOf(sel);
  if (i >= 0) bodies.splice(i, 1);
  sel = null;
}
function clearAll() { bodies = []; sel = null; document.getElementById("out").style.display = "none"; }

// ---------------------------------------------------------------- الفيزياء
function isRot(b) { return b.type === "motor" || b.type === "gear" || b.type === "pulley"; }
function meshing(a, c) {
  var dx = a.x - c.x, dy = a.y - c.y;
  return Math.sqrt(dx * dx + dy * dy) < a.size + c.size + MESH_GAP;
}
function circ(b) {
  if (b.type === "ball") return { o: b, x: "x", y: "y", vx: "vx", vy: "vy", r: b.size };
  return { o: b, x: "bx", y: "by", vx: "bvx", vy: "bvy", r: BOB_R };
}
function isDragging(b, part) { return drag && drag.b === b && drag.part === part; }

function step(dt) {
  var i, j, b, a, c, q = [], rot = [];

  // 1) انتقال الحركة بين المحرك والتروس والبكرات (نسبة السرعة = عكس نسبة الأقطار)
  for (i = 0; i < bodies.length; i++) { if (isRot(bodies[i])) { bodies[i].seen = false; rot.push(bodies[i]); } }
  for (i = 0; i < rot.length; i++) {
    if (rot[i].type === "motor") { rot[i].seen = true; rot[i].w = rot[i].rpm * 2 * Math.PI / 60; q.push(rot[i]); }
  }
  while (q.length) {
    a = q.shift();
    for (j = 0; j < rot.length; j++) {
      c = rot[j];
      if (!c.seen && meshing(a, c)) { c.seen = true; c.w = -a.w * a.size / c.size; q.push(c); }
    }
  }
  for (i = 0; i < rot.length; i++) {
    b = rot[i];
    if (!b.seen) b.w *= Math.pow(0.2, dt);   // ترس غير متصل يتوقف تدريجياً
    b.angle += b.w * dt;
  }

  // 2) الأجسام الحرة
  var cs = [];
  for (i = 0; i < bodies.length; i++) {
    b = bodies[i];
    if (b.type === "ball") {
      if (!isDragging(b, "main")) {
        b.vy += G * dt;
        b.vx *= (1 - 0.1 * dt);
        b.x += b.vx * dt; b.y += b.vy * dt;
        if (b.y + b.size > H - GROUND) {
          b.y = H - GROUND - b.size;
          b.vy = -b.vy * E_BALL; b.vx *= 0.99;
          if (Math.abs(b.vy) < 25) b.vy = 0;
        }
        if (b.x - b.size < 0) { b.x = b.size; b.vx = -b.vx * E_BALL; }
        if (b.x + b.size > W) { b.x = W - b.size; b.vx = -b.vx * E_BALL; }
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
    }
  }

  // 3) تصادم الكرات / ثقل النوابض فيما بينها
  for (i = 0; i < cs.length; i++) {
    for (j = i + 1; j < cs.length; j++) {
      var A = cs[i], B = cs[j], oa = A.o, ob = B.o;
      var ddx = ob[B.x] - oa[A.x], ddy = ob[B.y] - oa[A.y];
      var d = Math.sqrt(ddx * ddx + ddy * ddy), mr = A.r + B.r;
      if (d < mr && d > 0.001) {
        var nx = ddx / d, ny = ddy / d, ov = (mr - d) / 2;
        oa[A.x] -= nx * ov; oa[A.y] -= ny * ov;
        ob[B.x] += nx * ov; ob[B.y] += ny * ov;
        var rv = (ob[B.vx] - oa[A.vx]) * nx + (ob[B.vy] - oa[A.vy]) * ny;
        if (rv < 0) {
          var imp = -(1 + 0.7) * rv / 2;
          oa[A.vx] -= imp * nx; oa[A.vy] -= imp * ny;
          ob[B.vx] += imp * nx; ob[B.vy] += imp * ny;
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
      ctx.translate(b.x, b.y);
      ctx.fillStyle = "#f87171"; ctx.beginPath(); ctx.arc(0, 0, b.size, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "rgba(255,255,255,.35)"; ctx.beginPath(); ctx.arc(-b.size * 0.3, -b.size * 0.3, b.size * 0.25, 0, Math.PI * 2); ctx.fill();
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
    }
    ctx.restore();
  }

  if (sel && bodies.indexOf(sel) >= 0) {
    if (sel.type === "spring") ring(sel.bx, sel.by, BOB_R + 5);
    else if (sel.type === "pendulum") ring(sel.x + Math.sin(sel.th) * sel.len, sel.y + Math.cos(sel.th) * sel.len, 20);
    else ring(sel.x, sel.y, (isRot(sel) ? sel.size + 12 : sel.size + 6));
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

// ---------------------------------------------------------------- السحب والإفلات
function pt(e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }

function pick(p) {
  var best = null, bd = 1e9;
  function test(b, part, x, y, r) {
    var d = Math.sqrt((p.x - x) * (p.x - x) + (p.y - y) * (p.y - y));
    if (d <= r && d < bd) { bd = d; best = { b: b, part: part }; }
  }
  for (var i = bodies.length - 1; i >= 0; i--) {
    var b = bodies[i];
    if (b.type === "spring") { test(b, "bob", b.bx, b.by, 24); test(b, "main", b.x, b.y, 22); }
    else if (b.type === "pendulum") { test(b, "bob", b.x + Math.sin(b.th) * b.len, b.y + Math.cos(b.th) * b.len, 26); test(b, "main", b.x, b.y, 22); }
    else if (b.type === "ball") test(b, "main", b.x, b.y, b.size + 10);
    else test(b, "main", b.x, b.y, b.size + 12);
  }
  return best;
}

cv.addEventListener("pointerdown", function (e) {
  var p = pt(e);
  drag = pick(p);
  if (drag) {
    sel = drag.b;
    drag.lx = p.x; drag.ly = p.y; drag.lt = performance.now();
    try { cv.setPointerCapture(e.pointerId); } catch (err) {}
  } else { sel = null; }
});
cv.addEventListener("pointermove", function (e) {
  if (!drag) return;
  var p = pt(e), b = drag.b, x = clamp(p.x, 0, W), y = clamp(p.y, 0, H - GROUND);
  if (drag.part === "bob") {
    if (b.type === "spring") { b.bx = x; b.by = y; b.bvx = 0; b.bvy = 0; }
    else { b.th = Math.atan2(x - b.x, y - b.y); b.om = 0; }
  } else {
    var now = performance.now(), dtt = Math.max(1, now - drag.lt) / 1000;
    if (b.type === "ball") {
      b.vx = clamp((x - drag.lx) / dtt, -1500, 1500);
      b.vy = clamp((y - drag.ly) / dtt, -1500, 1500);
    }
    b.x = x; b.y = y;
    if (b.type === "spring") { /* الثقل يتبع النابض تلقائياً */ }
    drag.lx = x; drag.ly = y; drag.lt = now;
  }
});
function endDrag() { drag = null; }
cv.addEventListener("pointerup", endDrag);
cv.addEventListener("pointercancel", endDrag);

// ---------------------------------------------------------------- الذكاء الاصطناعي
function setBusy(v) {
  busy = v;
  document.getElementById("btnGen").disabled = v;
  document.getElementById("btnExp").disabled = v;
  if (busyTimer) { clearTimeout(busyTimer); busyTimer = null; }
  if (v) busyTimer = setTimeout(function () { busy = false; setBusy(false); }, 80000);
}
function showOut(t) {
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
    "{\"bodies\":[{\"type\":\"motor|gear|pulley|spring|ball|pendulum\",\"x\":0,\"y\":0,\"size\":0,\"rpm\":0,\"k\":0,\"len\":0}],\"note\":\"شرح قصير بالعربية\"}. " +
    "اللوحة بحجم " + Math.round(W) + "x" + Math.round(H) + " بكسل (x أفقي، y رأسي من الأعلى) وأعطِ x و y بالبكسل. " +
    "نصف قطر المحرك الافتراضي 28 والترس 40 والبكرة 34 والكرة 18. لتعشيق تروس اجعل المسافة بين مركزيهما قريبة من مجموع نصفي القطرين + 8. " +
    "rpm للمحرك فقط. k ثابت النابض (20 إلى 200). len طول النابض أو البندول بالبكسل. الطلب: " + txt;
  sendAI("mech_gen", "generate_mechanical", p);
}
function askExplain() {
  if (!bodies.length) { showOut("أضف عناصر أولاً ثم اطلب الشرح."); return; }
  var scene = bodies.map(function (b) {
    return { type: b.type, x: Math.round(b.x), y: Math.round(b.y), size: b.size, rpm: b.rpm,
             k: b.k, rest: b.rest, len: b.len, w_rad_s: +(b.w || 0).toFixed(2) };
  });
  var p = "اشرح بإيجاز وبالعربية هذا التصميم الميكانيكي وفيزياءه (الجاذبية، قانون هوك، نسب التروس، الدوران، البندول) في بضع جمل. المشهد: " + JSON.stringify(scene);
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
  if (L !== undefined) { o.rest = num(L, 90, 30, 300); o.len = num(L, 120, 40, 300); }
  if (d.angle !== undefined) o.th = num(d.angle, 0.9, -3, 3);
  return mk(t, clamp(x, 10, W - 10), clamp(y, 10, H - GROUND - 10), o);
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
    bodies = nb; sel = null;
    if (d.note) showOut(String(d.note)); else document.getElementById("out").style.display = "none";
  } else {
    showOut(String(text));
  }
};

resize();
addBody("motor"); bodies[0].x = W * 0.3; bodies[0].y = H * 0.5;
addBody("gear");  bodies[1].x = W * 0.3 + 28 + 40 + 8; bodies[1].y = H * 0.5;
sel = null;
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
    print(">> MECH LAB V1 applied:")
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
circuit_patch.py
يضيف ميزة «مختبر الإلكترونيات» (Circuit Lab) إلى المشروع الذي ولّده setup.py.
- الإصدار 3: يضيف الحفظ السحابي (Cloud Save/Load) والإصلاح الذكي (Smart AI Fix) بجانب العناصر والأفوميتر.
"""
import os

ROOT = os.environ.get("PROJECT_DIR", ".")
PKG_DIR = os.path.join(ROOT, "app", "src", "main", "java", "com", "example", "voiceassistant")
ASSETS_DIR = os.path.join(ROOT, "app", "src", "main", "assets")
MAIN_SCREEN = os.path.join(PKG_DIR, "ui", "MainScreen.kt")
MANIFEST = os.path.join(ROOT, "app", "src", "main", "AndroidManifest.xml")
HTML_PATH = os.path.join(ASSETS_DIR, "circuit_sim.html")
ACTIVITY_PATH = os.path.join(PKG_DIR, "CircuitSimulatorActivity.kt")

# ==============================================================================
# 1) ملف الواجهة: assets/circuit_sim.html
# ==============================================================================
CIRCUIT_HTML = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Electronics Lab</title>
<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--accent:#38bdf8;--bad:#f87171;--good:#4ade80;--warn:#fbbf24;--purple:#a855f7}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;overflow:hidden;touch-action:manipulation}
#app{display:flex;flex-direction:column;height:100%}
header{display:flex;align-items:center;gap:6px;padding:8px 10px;background:var(--panel);border-bottom:1px solid var(--line)}
header h1{flex:1;margin:0;font-size:15px;font-weight:700}
button{font:inherit;color:var(--text);background:#334155;border:1px solid #475569;border-radius:10px;padding:7px 11px;font-size:13px;cursor:pointer;white-space:nowrap}
button:active{background:#475569}
button.primary{background:#0284c7;border-color:#0ea5e9}
button.danger{background:#7f1d1d;border-color:#b91c1c}
button.fix{background:var(--purple);border-color:#c084fc}
button.save{background:#10b981;border-color:#34d399}
button:disabled{opacity:.5}
#palette{display:flex;gap:6px;padding:6px 8px;overflow-x:auto;background:#162033;border-bottom:1px solid var(--line)}
#palette button{flex:0 0 auto}
#stage{flex:1;position:relative;min-height:120px}
canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none;display:block}
#status{padding:6px 10px;font-size:12.5px;line-height:1.5;min-height:30px;background:#162033;border-top:1px solid var(--line);color:var(--muted)}
#status.ok{color:var(--good)}#status.warn{color:var(--warn)}#status.bad{color:var(--bad)}
#tools{display:none;gap:6px;align-items:center;flex-wrap:wrap;padding:6px 8px;background:var(--panel);border-top:1px solid var(--line)}
#tools.show{display:flex}
#tools .lbl{flex:1;min-width:90px;font-size:13px;font-weight:600}
#ai{display:flex;gap:6px;padding:8px;background:var(--panel);border-top:1px solid var(--line)}
#ai input{flex:1;min-width:0;font:inherit;font-size:14px;color:var(--text);background:#0b1220;border:1px solid #475569;border-radius:10px;padding:8px 10px}
#answer{display:none;position:absolute;inset:8px;background:rgba(15,23,42,.96);border:1px solid var(--accent);border-radius:14px;padding:12px;overflow:auto;z-index:5}
#answer.show{display:block}
#answer pre{white-space:pre-wrap;word-wrap:break-word;font:inherit;font-size:14px;line-height:1.7;margin:0 0 10px}
#busy{display:none;position:absolute;inset:0;background:rgba(15,23,42,.55);z-index:6;align-items:center;justify-content:center;font-size:15px}
#busy.show{display:flex}
</style>
</head>
<body>
<div id="app">
  <header>
    <h1 data-ar="مختبر الإلكترونيات ⚡" data-en="Electronics Lab ⚡"></h1>
    <button id="btnDemo" data-ar="مثال" data-en="Example"></button>
    <button id="btnSave" class="save" data-ar="حفظ ☁" data-en="Save ☁"></button>
    <button id="btnLoad" class="save" data-ar="تحميل ☁" data-en="Load ☁"></button>
    <button id="btnClear" class="danger" data-ar="مسح" data-en="Clear"></button>
    <button id="btnClose" data-ar="✕" data-en="✕"></button>
  </header>
  <div id="palette"></div>
  <div id="stage">
    <canvas id="cv"></canvas>
    <div id="answer"><pre id="answerText"></pre><button id="btnAnswerClose" class="primary" data-ar="إغلاق" data-en="Close"></button></div>
    <div id="busy"><span data-ar="جارٍ المعالجة…" data-en="Processing…"></span></div>
  </div>
  <div id="status"></div>
  <div id="tools">
    <span class="lbl" id="toolLbl"></span>
    <button id="btnMinus">−</button>
    <button id="btnPlus">+</button>
    <button id="btnToggle" data-ar="فتح/إغلاق" data-en="Open/Close"></button>
    <button id="btnRot" data-ar="تدوير" data-en="Rotate"></button>
    <button id="btnDel" class="danger" data-ar="حذف" data-en="Delete"></button>
  </div>
  <div id="ai">
    <input id="aiText" type="text" maxlength="300" data-ph-ar="مثال: دائرة LED أخضر مع مقاومة" data-ph-en="e.g. green LED with a resistor">
    <button id="btnGen" class="primary" data-ar="ارسم" data-en="Draw"></button>
    <button id="btnExplain" data-ar="اشرح" data-en="Explain"></button>
    <button id="btnFix" class="fix" data-ar="إصلاح ذكي 🪄" data-en="Smart Fix 🪄"></button>
  </div>
</div>
<script>
"use strict";
/* ===================================================== اللغة ===================================================== */
var AR = true;
try { AR = (window.Android && Android.isArabic) ? !!Android.isArabic() : /^ar/i.test(navigator.language || "ar"); } catch (e) { AR = true; }
function t(ar, en) { return AR ? ar : en; }
function applyLang() {
  document.documentElement.lang = AR ? "ar" : "en";
  document.documentElement.dir = AR ? "rtl" : "ltr";
  var els = document.querySelectorAll("[data-ar]");
  for (var i = 0; i < els.length; i++) els[i].textContent = AR ? els[i].getAttribute("data-ar") : els[i].getAttribute("data-en");
  var ph = document.querySelectorAll("[data-ph-ar]");
  for (var j = 0; j < ph.length; j++) ph[j].setAttribute("placeholder", AR ? ph[j].getAttribute("data-ph-ar") : ph[j].getAttribute("data-ph-en"));
}

/* ================================================= أنواع العناصر ================================================= */
var HL = 40;
var LED_COLORS = {
  red:    { vf: 1.9, col: "#ff3b30", ar: "أحمر",  en: "red" },
  green:  { vf: 2.2, col: "#34d399", ar: "أخضر",  en: "green" },
  yellow: { vf: 2.1, col: "#facc15", ar: "أصفر",  en: "yellow" },
  blue:   { vf: 3.0, col: "#3b82f6", ar: "أزرق",  en: "blue" },
  white:  { vf: 3.1, col: "#f8fafc", ar: "أبيض",  en: "white" }
};
var TYPES = {
  battery:   { prefix: "B", ar: "بطارية", en: "Battery", vals: [1.5, 3, 4.5, 5, 9, 12], def: 9 },
  resistor:  { prefix: "R", ar: "مقاومة", en: "Resistor", vals: [10, 47, 100, 220, 330, 470, 1000, 2200, 4700, 10000], def: 330 },
  capacitor: { prefix: "C", ar: "مكثف", en: "Capacitor", vals: [10, 47, 100, 470, 1000], def: 100 },
  diode:     { prefix: "E", ar: "دايود", en: "Diode", vals: ["silicon", "germanium"], def: "silicon" },
  fuse:      { prefix: "F", ar: "فيوز", en: "Fuse", vals: [0.5, 1, 2, 5], def: 1 },
  led:       { prefix: "D", ar: "LED", en: "LED", vals: ["red", "green", "yellow", "blue", "white"], def: "red" },
  bulb:      { prefix: "L", ar: "مصباح", en: "Bulb", vals: [25, 50, 100], def: 50 },
  "switch":  { prefix: "S", ar: "مفتاح", en: "Switch", vals: [], def: 0 }
};
var MAX_COMPS = 30, MAX_WIRES = 70;

/* =================================================== الحالة ====================================================== */
var comps = [];
var wires = [];
var sel = null;
var pending = null;
var sim = null;

var meter = {
  visible: false, x: 20, y: 60, w: 180, h: 100,
  mode: "V",
  probeA: { x: 0, y: 0, key: null },
  probeB: { x: 0, y: 0, key: null },
  reading: "---"
};
function probePos(pr) {
  var p = pr.key ? keyPos(pr.key) : null;
  return p || { x: pr.x, y: pr.y };
}

function findComp(id) { for (var i = 0; i < comps.length; i++) if (comps[i].id === id) return comps[i]; return null; }
function newId(type) {
  var p = TYPES[type].prefix, n = 1;
  while (findComp(p + n)) n++;
  return p + n;
}
function termPos(c, which) {
  var s = which === "a" ? -1 : 1;
  return c.rot ? { x: c.x, y: c.y + s * HL } : { x: c.x + s * HL, y: c.y };
}
function keyPos(key) {
  var p = key.split("."), c = findComp(p[0]);
  return c ? termPos(c, p[1]) : null;
}

/* ===================================================================================================================
   المحاكي
   =================================================================================================================== */
/*SOLVER_START*/
var R_BATT = 0.1, R_SW_ON = 0.01, R_LED = 5, G_MIN = 1e-9;

function solveLinear(A, z) {
  var n = z.length, i, j, k;
  for (i = 0; i < n; i++) A[i] = A[i].slice();
  z = z.slice();
  for (i = 0; i < n; i++) {
    var piv = i, best = Math.abs(A[i][i]);
    for (j = i + 1; j < n; j++) if (Math.abs(A[j][i]) > best) { best = Math.abs(A[j][i]); piv = j; }
    if (best < 1e-18) return null;
    if (piv !== i) { var tr = A[i]; A[i] = A[piv]; A[piv] = tr; var tz = z[i]; z[i] = z[piv]; z[piv] = tz; }
    for (j = i + 1; j < n; j++) {
      var f = A[j][i] / A[i][i];
      if (f === 0) continue;
      for (k = i; k < n; k++) A[j][k] -= f * A[i][k];
      z[j] -= f * z[i];
    }
  }
  var x = new Array(n);
  for (i = n - 1; i >= 0; i--) {
    var s = z[i];
    for (k = i + 1; k < n; k++) s -= A[i][k] * x[k];
    x[i] = s / A[i][i];
  }
  return x;
}

function nodeMap(comps, wires) {
  var parent = {};
  function find(x) { while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; } return x; }
  comps.forEach(function (c) { parent[c.id + ".a"] = c.id + ".a"; parent[c.id + ".b"] = c.id + ".b"; });
  wires.forEach(function (w) {
    if (parent.hasOwnProperty(w.a) && parent.hasOwnProperty(w.b)) {
      var ra = find(w.a), rb = find(w.b);
      if (ra !== rb) parent[ra] = rb;
    }
  });
  var keys = Object.keys(parent), root = {}, idx = {}, n = 0;
  keys.forEach(function (k) { var r = find(k); if (!idx.hasOwnProperty(r)) idx[r] = n++; root[k] = idx[r]; });
  return { node: root, count: n };
}

function simulate(comps, wires) {
  var out = { ok: false, reason: "", V: {}, I: {}, P: {}, ledOn: {}, diodeOn: {}, nodeOf: {}, warnings: [] };
  var bat = null;
  for (var i = 0; i < comps.length; i++) if (comps[i].type === "battery") { bat = comps[i]; break; }
  if (!bat) { out.reason = "nobattery"; return out; }
  var nm = nodeMap(comps, wires);
  out.nodeOf = nm.node;
  var gnd = nm.node[bat.id + ".b"];
  var map = new Array(nm.count), n = 0, k;
  for (k = 0; k < nm.count; k++) map[k] = (k === gnd) ? -1 : n++;
  function mi(c, t) { return map[nm.node[c.id + "." + t]]; }

  var ledOn = {}, diodeOn = {};
  comps.forEach(function (c) {
    if (c.type === "led") ledOn[c.id] = false;
    if (c.type === "diode") diodeOn[c.id] = false;
  });
  function diodeVf(c) { return c.val === "germanium" ? 0.3 : 0.7; }
  var volt = null;

  for (var iter = 0; iter < 60; iter++) {
    var A = [], z = [], r, q;
    for (r = 0; r < n; r++) { A.push(new Array(n).fill(0)); z.push(0); A[r][r] += G_MIN; }
    var stampG = function (a, b, g) {
      if (a >= 0) A[a][a] += g;
      if (b >= 0) A[b][b] += g;
      if (a >= 0 && b >= 0) { A[a][b] -= g; A[b][a] -= g; }
    };
    var stampI = function (a, b, i) { if (a >= 0) z[a] += i; if (b >= 0) z[b] -= i; };
    comps.forEach(function (c) {
      var a = mi(c, "a"), b = mi(c, "b");
      if (c.type === "battery") { var g = 1 / R_BATT; stampG(a, b, g); stampI(a, b, c.val * g); }
      else if (c.type === "resistor" || c.type === "bulb") { stampG(a, b, 1 / c.val); }
      else if (c.type === "fuse") { stampG(a, b, 1 / 0.01); }
      else if (c.type === "capacitor") { stampG(a, b, 1e-9); }
      else if (c.type === "switch") { if (c.closed) stampG(a, b, 1 / R_SW_ON); }
      else if (c.type === "led" && ledOn[c.id]) {
        var gl = 1 / R_LED, vf = LED_COLORS[c.val] ? LED_COLORS[c.val].vf : 2;
        stampG(a, b, gl); stampI(a, b, gl * vf);
      }
      else if (c.type === "diode" && diodeOn[c.id]) {
        stampG(a, b, 1.0); stampI(a, b, diodeVf(c));
      }
    });
    var x = n > 0 ? solveLinear(A, z) : [];
    if (!x) { out.reason = "singular"; return out; }
    volt = x;
    var changed = false;
    comps.forEach(function (c) {
      if (c.type !== "led" && c.type !== "diode") return;
      var va = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, vb = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
      var vf = c.type === "led" ? (LED_COLORS[c.val] ? LED_COLORS[c.val].vf : 2) : diodeVf(c);
      var on = (va - vb) > vf;
      var st = c.type === "led" ? ledOn : diodeOn;
      if (on !== st[c.id]) { st[c.id] = on; changed = true; }
    });
    if (!changed) break;
  }

  function vOf(c, t) { var m = mi(c, t); return m >= 0 ? volt[m] : 0; }
  comps.forEach(function (c) {
    var va = vOf(c, "a"), vb = vOf(c, "b"), vd = va - vb, cur = 0;
    if (c.type === "battery") cur = (c.val - vd) / R_BATT;
    else if (c.type === "resistor" || c.type === "bulb") cur = vd / c.val;
    else if (c.type === "fuse") cur = vd / 0.01;
    else if (c.type === "capacitor") cur = 0;
    else if (c.type === "switch") cur = c.closed ? vd / R_SW_ON : 0;
    else if (c.type === "led") { var vf = LED_COLORS[c.val] ? LED_COLORS[c.val].vf : 2; cur = ledOn[c.id] ? Math.max(0, (vd - vf) / R_LED) : 0; }
    else if (c.type === "diode") { cur = diodeOn[c.id] ? Math.max(0, (vd - diodeVf(c)) / 1.0) : 0; }
    out.V[c.id] = vd; out.I[c.id] = cur; out.P[c.id] = Math.abs(vd * cur);
    if (Math.abs(cur) < 1e-12) out.I[c.id] = 0;
  });
  out.ledOn = ledOn; out.diodeOn = diodeOn;
  out.nodeV = function (key) { var node = nm.node[key]; if (node === undefined) return 0; var m = map[node]; return m >= 0 ? volt[m] : 0; };
  out.ok = true;

  var anyCurrent = false;
  comps.forEach(function (c) {
    var i = Math.abs(out.I[c.id]);
    if (c.type === "battery" && i > 0.01) anyCurrent = true;
    if (c.type === "battery" && i > 2) out.warnings.push({ k: "short", id: c.id });
    if (c.type === "led" && i > 0.030) out.warnings.push({ k: "ledburn", id: c.id });
    if (c.type === "resistor" && out.P[c.id] > 0.25) out.warnings.push({ k: "hot", id: c.id });
    if (c.type === "fuse" && i > c.val) out.warnings.push({ k: "fuse_blow", id: c.id, val: c.val });
  });
  out.anyCurrent = anyCurrent;
  return out;
}

function measureResistance(keyA, keyB) {
  if (!keyA || !keyB || keyA === keyB) return 0;
  var testComps = comps.map(function (c) { return { id: c.id, type: c.type, x: c.x, y: c.y, rot: c.rot, val: c.val, closed: c.closed }; });
  var seen = {}; testComps.forEach(function (c) { seen[c.id] = true; });
  var bid = "M1", n = 1;
  while (seen[bid]) { n++; bid = "M" + n; }
  testComps.push({ id: bid, type: "battery", val: 1, x: 0, y: 0, rot: 0, closed: true });
  var testWires = wires.map(function (w) { return { a: w.a, b: w.b }; });
  testWires.push({ a: bid + ".a", b: keyA });
  testWires.push({ a: bid + ".b", b: keyB });
  var s = simulate(testComps, testWires);
  if (!s.ok) return 0;
  var cur = Math.abs(s.I[bid]);
  if (cur < 1e-6) return 999999;
  return 1 / cur;
}
/*SOLVER_END*/

/* ================================================ التنسيق والعرض ================================================= */
function fmtR(v) { return v >= 1000 ? (v / 1000) + "kΩ" : v + "Ω"; }
function fmtC(v) { return v >= 1000 ? (v / 1000) + "mF" : v + "µF"; }
function fmtI(a) {
  var m = Math.abs(a);
  if (m >= 1) return a.toFixed(2) + "A";
  if (m >= 0.001) return (a * 1000).toFixed(1) + "mA";
  if (m > 0) return (a * 1e6).toFixed(0) + "µA";
  return "0";
}
function valText(c) {
  if (c.type === "battery") return c.val + "V";
  if (c.type === "resistor" || c.type === "bulb") return fmtR(c.val);
  if (c.type === "capacitor") return fmtC(c.val);
  if (c.type === "fuse") return c.val + "A";
  if (c.type === "diode") return AR ? (c.val === "silicon" ? "سيليكون" : "جرمانيوم") : c.val;
  if (c.type === "led") { var lc = LED_COLORS[c.val]; return lc ? (AR ? lc.ar : lc.en) : ""; }
  if (c.type === "switch") return c.closed ? t("مغلق", "closed") : t("مفتوح", "open");
  return "";
}

var cv = document.getElementById("cv"), ctx = cv.getContext("2d"), stage = document.getElementById("stage");
var cssW = 300, cssH = 300, dpr = 1;
function resize() {
  dpr = Math.max(1, window.devicePixelRatio || 1);
  cssW = Math.max(100, stage.clientWidth); cssH = Math.max(100, stage.clientHeight);
  cv.width = Math.round(cssW * dpr); cv.height = Math.round(cssH * dpr);
  draw();
}

function drawComp(c) {
  var s = sim && sim.ok ? sim : null;
  var cur = s ? s.I[c.id] : 0;
  ctx.save();
  ctx.translate(c.x, c.y);
  if (c.rot) ctx.rotate(Math.PI / 2);
  ctx.lineWidth = 2.5; ctx.lineCap = "round"; ctx.lineJoin = "round";
  var isSel = sel && sel.kind === "comp" && sel.id === c.id;
  ctx.strokeStyle = isSel ? "#38bdf8" : "#e2e8f0";
  ctx.fillStyle = ctx.strokeStyle;
  function line(x1, y1, x2, y2) { ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); }
  if (isSel) { ctx.save(); ctx.fillStyle = "rgba(56,189,248,.10)"; ctx.fillRect(-HL, -24, HL * 2, 48); ctx.restore(); }
  var k;
  
  if (c.type === "resistor") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-24, 0);
    for (k = 0; k < 6; k++) ctx.lineTo(-24 + 4 + k * 8, k % 2 === 0 ? -9 : 9);
    ctx.lineTo(24, 0); ctx.stroke();
  } else if (c.type === "battery") {
    line(-HL, 0, -6, 0); line(6, 0, HL, 0);
    line(-6, -15, -6, 15); line(6, -8, 6, 8);
    ctx.font = "bold 13px sans-serif"; ctx.textAlign = "center"; ctx.fillText("+", -20, -8);
  } else if (c.type === "capacitor") {
    line(-HL, 0, -8, 0); line(8, 0, HL, 0);
    line(-8, -15, -8, 15); line(8, -15, 8, 15);
  } else if (c.type === "diode") {
    line(-HL, 0, -10, 0); line(10, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-10, -14); ctx.lineTo(-10, 14); ctx.lineTo(10, 0); ctx.closePath(); ctx.stroke();
    line(10, -14, 10, 14);
  } else if (c.type === "fuse") {
    var blown = s && cur > c.val;
    line(-HL, 0, -16, 0); line(16, 0, HL, 0);
    ctx.beginPath(); ctx.rect(-16, -8, 32, 16); ctx.stroke();
    if (blown) { ctx.save(); ctx.strokeStyle = "#f87171"; line(-16, 0, -3, 0); line(3, 0, 16, 0); ctx.restore(); }
    else line(-16, 0, 16, 0);
  } else if (c.type === "led") {
    var lc = LED_COLORS[c.val] || LED_COLORS.red;
    var br = s && s.ledOn[c.id] ? Math.min(1, cur / 0.02) : 0;
    var burnt = s && cur > 0.030;
    if (br > 0) {
      var g = ctx.createRadialGradient(0, 0, 4, 0, 0, 14 + 34 * br);
      g.addColorStop(0, lc.col); g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.save(); ctx.globalAlpha = 0.25 + 0.7 * br; ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(0, 0, 14 + 34 * br, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    line(-HL, 0, -10, 0); line(10, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-10, -14); ctx.lineTo(-10, 14); ctx.lineTo(10, 0); ctx.closePath();
    ctx.save(); ctx.fillStyle = br > 0 ? lc.col : "rgba(148,163,184,.25)"; ctx.fill(); ctx.restore(); ctx.stroke();
    line(10, -14, 10, 14);
    ctx.save(); ctx.strokeStyle = lc.col; ctx.lineWidth = 1.8;
    line(2, -16, 10, -24); line(8, -14, 16, -22); ctx.restore();
    if (burnt) { ctx.save(); ctx.strokeStyle = "#f87171"; ctx.lineWidth = 3; line(-14, -14, 14, 14); line(14, -14, -14, 14); ctx.restore(); }
  } else if (c.type === "bulb") {
    var pr = s ? s.P[c.id] : 0, rated = 36 / c.val, bb = Math.min(1, pr / rated);
    if (bb > 0.02) {
      var g2 = ctx.createRadialGradient(0, 0, 4, 0, 0, 20 + 30 * bb);
      g2.addColorStop(0, "#fde68a"); g2.addColorStop(1, "rgba(0,0,0,0)");
      ctx.save(); ctx.globalAlpha = 0.25 + 0.7 * bb; ctx.fillStyle = g2;
      ctx.beginPath(); ctx.arc(0, 0, 20 + 30 * bb, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    line(-HL, 0, -16, 0); line(16, 0, HL, 0);
    ctx.beginPath(); ctx.arc(0, 0, 16, 0, Math.PI * 2);
    ctx.save(); ctx.fillStyle = bb > 0.02 ? "rgba(253,230,138," + (0.3 + 0.6 * bb) + ")" : "rgba(148,163,184,.15)"; ctx.fill(); ctx.restore(); ctx.stroke();
    line(-11, -11, 11, 11); line(11, -11, -11, 11);
  } else if (c.type === "switch") {
    line(-HL, 0, -16, 0); line(16, 0, HL, 0);
    ctx.beginPath(); ctx.arc(-16, 0, 3, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(16, 0, 3, 0, Math.PI * 2); ctx.fill();
    if (c.closed) line(-16, 0, 16, 0); else line(-16, 0, 12, -17);
  }
  
  ["a", "b"].forEach(function (w) {
    var key = c.id + "." + w, on = pending === key;
    var px = w === "a" ? -HL : HL;
    ctx.beginPath(); ctx.arc(px, 0, on ? 8 : 5.5, 0, Math.PI * 2);
    ctx.fillStyle = on ? "#fbbf24" : "#38bdf8"; ctx.fill();
    ctx.lineWidth = 1.5; ctx.strokeStyle = "#0f172a"; ctx.stroke();
  });
  ctx.restore();
  
  ctx.save();
  ctx.fillStyle = "#cbd5e1"; ctx.font = "11px sans-serif";
  ctx.textAlign = c.rot ? "left" : "center";
  var lx = c.rot ? c.x + 20 : c.x, ly = c.rot ? c.y - 4 : c.y - 30;
  ctx.fillText(c.id + " · " + valText(c), lx, ly);
  if (s && c.type !== "switch" && c.type !== "capacitor" && Math.abs(s.I[c.id]) > 0) {
    ctx.fillStyle = "#fbbf24";
    ctx.fillText(fmtI(s.I[c.id]), lx, ly + 13);
  }
  ctx.restore();
}

function drawMeter() {
  if (!meter.visible) return;
  ctx.save();
  ctx.fillStyle = "rgba(30,41,59,.95)"; ctx.strokeStyle = "#475569"; ctx.lineWidth = 2;
  ctx.fillRect(meter.x, meter.y, meter.w, meter.h); ctx.strokeRect(meter.x, meter.y, meter.w, meter.h);
  ctx.fillStyle = "#94a3b8"; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "left";
  ctx.fillText(AR ? "أفوميتر" : "Multimeter", meter.x + 10, meter.y + 20);
  ctx.fillStyle = meter.mode === "V" ? "#38bdf8" : "#334155";
  ctx.fillRect(meter.x + 10, meter.y + 30, 30, 22);
  ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.fillText("V", meter.x + 25, meter.y + 46);
  ctx.fillStyle = meter.mode === "R" ? "#38bdf8" : "#334155";
  ctx.fillRect(meter.x + 45, meter.y + 30, 30, 22);
  ctx.fillStyle = "white"; ctx.fillText("Ω", meter.x + 60, meter.y + 46);
  ctx.fillStyle = "#4ade80"; ctx.font = "bold 14px monospace"; ctx.textAlign = "left";
  ctx.fillText(meter.reading, meter.x + 82, meter.y + 46);
  ctx.fillStyle = "#cbd5e1"; ctx.font = "11px sans-serif";
  ctx.fillText("Red: " + (meter.probeA.key || "---"), meter.x + 10, meter.y + 72);
  ctx.fillText("Blk: " + (meter.probeB.key || "---"), meter.x + 10, meter.y + 88);
  ctx.restore();
  var posA = probePos(meter.probeA), posB = probePos(meter.probeB);
  ctx.save();
  ctx.lineWidth = 2; ctx.lineCap = "round";
  ctx.beginPath(); ctx.moveTo(meter.x, meter.y + 35); ctx.lineTo(posA.x, posA.y); ctx.strokeStyle = "#ef4444"; ctx.stroke();
  ctx.beginPath(); ctx.arc(posA.x, posA.y, 6, 0, Math.PI * 2); ctx.fillStyle = "#ef4444"; ctx.fill();
  ctx.beginPath(); ctx.moveTo(meter.x, meter.y + 65); ctx.lineTo(posB.x, posB.y); ctx.strokeStyle = "#94a3b8"; ctx.stroke();
  ctx.beginPath(); ctx.arc(posB.x, posB.y, 6, 0, Math.PI * 2); ctx.fillStyle = "#111827"; ctx.fill(); ctx.stroke();
  ctx.restore();
}

function distSeg(px, py, x1, y1, x2, y2) {
  var dx = x2 - x1, dy = y2 - y1, l2 = dx * dx + dy * dy;
  var u = l2 === 0 ? 0 : Math.max(0, Math.min(1, ((px - x1) * dx + (py - y1) * dy) / l2));
  var cx = x1 + u * dx, cy = y1 + u * dy;
  return Math.hypot(px - cx, py - cy);
}

function draw() {
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, cssW, cssH);
  ctx.fillStyle = "rgba(148,163,184,.18)";
  for (var gx = 10; gx < cssW; gx += 20) for (var gy = 10; gy < cssH; gy += 20) ctx.fillRect(gx, gy, 1.2, 1.2);
  wires.forEach(function (w, i) {
    var p1 = keyPos(w.a), p2 = keyPos(w.b);
    if (!p1 || !p2) return;
    var live = sim && sim.ok && Math.abs(sim.nodeV(w.a)) > 0.05;
    var isSel = sel && sel.kind === "wire" && sel.i === i;
    ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
    ctx.lineWidth = isSel ? 5 : 3; ctx.lineCap = "round";
    ctx.strokeStyle = isSel ? "#38bdf8" : (live ? "#fbbf24" : "#64748b");
    ctx.stroke();
  });
  comps.forEach(drawComp);
  drawMeter();
}

/* ================================================== الحالة والرسائل ============================================== */
var statusEl = document.getElementById("status");
function setStatus(cls, msg) { statusEl.className = cls; statusEl.textContent = msg; }

function recompute() {
  sim = simulate(comps, wires);
  var msg, cls = "";
  if (comps.length === 0) { msg = t("أضف عناصر من الشريط العلوي، ثم المس طرفَين لتوصيلهما بسلك.", "Add parts from the bar above, then tap two terminals to wire them."); }
  else if (pending) { msg = t("اختر الطرف الثاني لإكمال السلك (أو المس مكاناً فارغاً للإلغاء).", "Tap the second terminal to finish the wire (or tap empty space to cancel)."); }
  else if (!sim.ok && sim.reason === "nobattery") { cls = "warn"; msg = t("أضف بطارية لتشغيل الدائرة.", "Add a battery to power the circuit."); }
  else if (!sim.ok) { cls = "bad"; msg = t("تعذّر حل الدائرة، تحقق من التوصيلات.", "Could not solve the circuit — check the wiring."); }
  else if (sim.warnings.length) {
    var w = sim.warnings[0]; cls = "bad";
    if (w.k === "short") msg = t("⚠ قصر دائرة! البطارية " + w.id + " تعطي تياراً هائلاً.", "⚠ Short circuit! Battery " + w.id + " is driving a huge current.");
    else if (w.k === "ledburn") msg = t("⚠ " + w.id + " سيحترق: التيار أعلى من 30mA — أضف مقاومة على التوالي.", "⚠ " + w.id + " would burn out: over 30 mA — add a series resistor.");
    else if (w.k === "fuse_blow") msg = t("⚠ الفيوز " + w.id + " احترق: التيار أعلى من " + w.val + "A!", "⚠ Fuse " + w.id + " blew: current over " + w.val + "A!");
    else msg = t("⚠ " + w.id + " يسخن جداً (أكثر من ربع واط).", "⚠ " + w.id + " is overheating (over 0.25 W).");
  }
  else if (!sim.anyCurrent) { cls = "warn"; msg = t("الدائرة مفتوحة: لا يمر تيار. تأكد من إغلاق الحلقة ومن اتجاه الـ LED (الطرف a هو المصعد).", "Open circuit: no current. Close the loop and check LED polarity (terminal a is the anode)."); }
  else {
    var b = null; for (var i = 0; i < comps.length; i++) if (comps[i].type === "battery") { b = comps[i]; break; }
    cls = "ok"; msg = t("✔ الدائرة تعمل — تيار البطارية " + fmtI(sim.I[b.id]) + " عند " + b.val + "V", "✔ Circuit is live — battery current " + fmtI(sim.I[b.id]) + " at " + b.val + "V");
  }
  setStatus(cls, msg);

  if (meter.visible) {
    if (meter.mode === "V") {
      var va = sim.ok && meter.probeA.key ? sim.nodeV(meter.probeA.key) : 0;
      var vb = sim.ok && meter.probeB.key ? sim.nodeV(meter.probeB.key) : 0;
      meter.reading = (va - vb).toFixed(2) + " V";
    } else if (comps.some(function (c) { return c.type === "battery"; })) {
      meter.reading = t("أزل البطارية", "Remove battery");
    } else {
      var rr = measureResistance(meter.probeA.key, meter.probeB.key);
      meter.reading = rr > 900000 ? "OL" : rr.toFixed(1) + " Ω";
    }
  }
  updateTools();
  draw();
  scheduleSave();
}

/* =================================================== شريط الأدوات ================================================ */
var toolsEl = document.getElementById("tools"), toolLbl = document.getElementById("toolLbl");
var btnMinus = document.getElementById("btnMinus"), btnPlus = document.getElementById("btnPlus");
var btnToggle = document.getElementById("btnToggle"), btnRot = document.getElementById("btnRot");
function updateTools() {
  if (!sel) { toolsEl.className = ""; return; }
  toolsEl.className = "show";
  if (sel.kind === "wire") {
    toolLbl.textContent = t("سلك", "Wire");
    btnMinus.style.display = btnPlus.style.display = btnToggle.style.display = btnRot.style.display = "none";
    return;
  }
  var c = findComp(sel.id);
  if (!c) { sel = null; toolsEl.className = ""; return; }
  toolLbl.textContent = c.id + " · " + (AR ? TYPES[c.type].ar : TYPES[c.type].en) + " · " + valText(c);
  var hasVals = TYPES[c.type].vals.length > 0;
  btnMinus.style.display = btnPlus.style.display = hasVals ? "" : "none";
  btnToggle.style.display = c.type === "switch" ? "" : "none";
  btnRot.style.display = "";
}
function stepValue(dir) {
  if (!sel || sel.kind !== "comp") return;
  var c = findComp(sel.id); if (!c) return;
  var vals = TYPES[c.type].vals; if (!vals.length) return;
  var i = vals.indexOf(c.val); if (i < 0) i = 0;
  c.val = vals[Math.max(0, Math.min(vals.length - 1, i + dir))];
  recompute();
}
btnMinus.onclick = function () { stepValue(-1); };
btnPlus.onclick = function () { stepValue(1); };
btnToggle.onclick = function () { var c = sel && sel.kind === "comp" ? findComp(sel.id) : null; if (c && c.type === "switch") { c.closed = !c.closed; recompute(); } };
btnRot.onclick = function () { var c = sel && sel.kind === "comp" ? findComp(sel.id) : null; if (c) { c.rot = c.rot ? 0 : 1; recompute(); } };
document.getElementById("btnDel").onclick = function () {
  if (!sel) return;
  if (sel.kind === "wire") { wires.splice(sel.i, 1); }
  else {
    var id = sel.id;
    comps = comps.filter(function (c) { return c.id !== id; });
    wires = wires.filter(function (w) { return w.a.split(".")[0] !== id && w.b.split(".")[0] !== id; });
  }
  sel = null; pending = null; recompute();
};

/* ===================================================== الإضافة =================================================== */
function addComp(type, x, y, val, closed, id) {
  if (comps.length >= MAX_COMPS) { setStatus("warn", t("وصلت للحد الأقصى من العناصر.", "Part limit reached.")); return null; }
  var d = TYPES[type];
  var c = { id: id || newId(type), type: type, x: x, y: y, rot: 0, val: val === undefined ? d.def : val, closed: closed === undefined ? true : !!closed };
  comps.push(c);
  return c;
}
function freeSpot() {
  var cx = cssW / 2, cy = cssH / 2;
  for (var r = 0; r < 12; r++) {
    for (var a = 0; a < 8; a++) {
      var x = Math.round((cx + Math.cos(a * Math.PI / 4) * r * 45) / 10) * 10, y = Math.round((cy + Math.sin(a * Math.PI / 4) * r * 45) / 10) * 10;
      if (x < HL + 10 || x > cssW - HL - 10 || y < 40 || y > cssH - 30) continue;
      var clash = comps.some(function (c) { return Math.hypot(c.x - x, c.y - y) < 70; });
      if (!clash) return { x: x, y: y };
    }
  }
  return { x: cx, y: cy };
}
(function buildPalette() {
  var pal = document.getElementById("palette");
  Object.keys(TYPES).forEach(function (type) {
    var b = document.createElement("button");
    b.textContent = "+ " + (AR ? TYPES[type].ar : TYPES[type].en);
    b.onclick = function () {
      var p = freeSpot(), c = addComp(type, p.x, p.y);
      if (c) { sel = { kind: "comp", id: c.id }; pending = null; recompute(); }
    };
    pal.appendChild(b);
  });
  var mbtn = document.createElement("button");
  mbtn.textContent = "🔌 " + (AR ? "أفوميتر" : "Multimeter");
  mbtn.id = "btnMeter";
  mbtn.onclick = function () {
    meter.visible = !meter.visible;
    mbtn.style.background = meter.visible ? "#0284c7" : "";
    if (meter.visible && meter.probeA.x === 0 && meter.probeB.x === 0) {
      meter.probeA.x = meter.x + 20; meter.probeA.y = meter.y + 130;
      meter.probeB.x = meter.x + 60; meter.probeB.y = meter.y + 130;
    }
    recompute();
  };
  pal.appendChild(mbtn);
})();

/* ======================================================== اللمس ================================================== */
var drag = null;
function evPos(e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
function hitTerminal(p) {
  var best = null, bd = 20;
  comps.forEach(function (c) {
    ["a", "b"].forEach(function (w) {
      var tp = termPos(c, w), d = Math.hypot(tp.x - p.x, tp.y - p.y);
      if (d < bd) { bd = d; best = c.id + "." + w; }
    });
  });
  return best;
}
function hitComp(p) {
  for (var i = comps.length - 1; i >= 0; i--) {
    var c = comps[i], dx = p.x - c.x, dy = p.y - c.y;
    if (c.rot) { var tmp = dx; dx = dy; dy = -tmp; }
    if (Math.abs(dx) <= HL - 6 && Math.abs(dy) <= 24) return c;
  }
  return null;
}
function hitWire(p) {
  for (var i = wires.length - 1; i >= 0; i--) {
    var p1 = keyPos(wires[i].a), p2 = keyPos(wires[i].b);
    if (p1 && p2 && distSeg(p.x, p.y, p1.x, p1.y, p2.x, p2.y) < 12) return i;
  }
  return -1;
}
cv.addEventListener("pointerdown", function (e) {
  var p = evPos(e);
  try { cv.setPointerCapture(e.pointerId); } catch (err) {}
  if (meter.visible) {
    var pA = probePos(meter.probeA), pB = probePos(meter.probeB);
    if (Math.hypot(pA.x - p.x, pA.y - p.y) < 20) { drag = { mode: "probe", probe: "A", sx: p.x, sy: p.y }; return; }
    if (Math.hypot(pB.x - p.x, pB.y - p.y) < 20) { drag = { mode: "probe", probe: "B", sx: p.x, sy: p.y }; return; }
    if (p.x > meter.x + 10 && p.x < meter.x + 40 && p.y > meter.y + 30 && p.y < meter.y + 52) { meter.mode = "V"; recompute(); return; }
    if (p.x > meter.x + 45 && p.x < meter.x + 75 && p.y > meter.y + 30 && p.y < meter.y + 52) { meter.mode = "R"; recompute(); return; }
    if (p.x > meter.x && p.x < meter.x + meter.w && p.y > meter.y && p.y < meter.y + meter.h) { drag = { mode: "meter", ox: p.x - meter.x, oy: p.y - meter.y, sx: p.x, sy: p.y }; return; }
  }
  var tk = hitTerminal(p);
  if (tk) { drag = { mode: "term", key: tk, sx: p.x, sy: p.y }; return; }
  var c = hitComp(p);
  if (c) { drag = { mode: "comp", id: c.id, ox: p.x - c.x, oy: p.y - c.y, sx: p.x, sy: p.y, moved: false }; return; }
  drag = { mode: "bg", sx: p.x, sy: p.y };
});
cv.addEventListener("pointermove", function (e) {
  if (!drag) return;
  var p = evPos(e);
  if (drag.mode === "meter") { meter.x = p.x - drag.ox; meter.y = p.y - drag.oy; draw(); return; }
  if (drag.mode === "probe") {
    var pr = drag.probe === "A" ? meter.probeA : meter.probeB;
    pr.x = p.x; pr.y = p.y; pr.key = null; draw(); return;
  }
  if (drag.mode !== "comp") return;
  if (!drag.moved && Math.hypot(p.x - drag.sx, p.y - drag.sy) < 6) return;
  drag.moved = true;
  var c = findComp(drag.id); if (!c) return;
  c.x = Math.max(HL, Math.min(cssW - HL, Math.round((p.x - drag.ox) / 10) * 10));
  c.y = Math.max(30, Math.min(cssH - 20, Math.round((p.y - drag.oy) / 10) * 10));
  draw();
});
function onUp(e) {
  if (!drag) return;
  var d = drag; drag = null;
  var p = evPos(e);
  var moved = Math.hypot(p.x - d.sx, p.y - d.sy) >= 6;
  if (d.mode === "meter") { scheduleSave(); return; }
  if (d.mode === "probe") {
    var tkp = hitTerminal(p);
    if (d.probe === "A") meter.probeA.key = tkp; else meter.probeB.key = tkp;
    recompute(); return;
  }
  if (d.mode === "comp") {
    if (!moved && !d.moved) {
      var c = findComp(d.id);
      if (c) {
        if (c.type === "switch") c.closed = !c.closed;
        sel = { kind: "comp", id: c.id }; pending = null;
      }
    }
    recompute(); return;
  }
  if (moved) { return; }
  if (d.mode === "term") {
    if (!pending) { pending = d.key; sel = null; }
    else if (pending === d.key) { pending = null; }
    else {
      var dup = wires.some(function (w) { return (w.a === pending && w.b === d.key) || (w.a === d.key && w.b === pending); });
      if (!dup && wires.length < MAX_WIRES) wires.push({ a: pending, b: d.key });
      pending = null;
    }
    recompute(); return;
  }
  if (pending) { pending = null; recompute(); return; }
  var wi = hitWire(p);
  sel = wi >= 0 ? { kind: "wire", i: wi } : null;
  recompute();
}
cv.addEventListener("pointerup", onUp);
cv.addEventListener("pointercancel", function () { drag = null; });

/* ================================================= الحفظ والتحميل ================================================ */
var saveTimer = null;
function serialize() { return JSON.stringify({ comps: comps, wires: wires, meter: meter }); }
function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(function () {
    try { if (window.Android && Android.saveState) Android.saveState(serialize()); } catch (e) {}
  }, 500);
}
function sanitizeState(obj) {
  if (!obj || !Array.isArray(obj.comps)) return null;
  var outC = [], seen = {};
  obj.comps.slice(0, MAX_COMPS).forEach(function (c) {
    if (!c || !TYPES.hasOwnProperty(c.type)) return;
    var id = String(c.id || "");
    if (!/^[A-Za-z][A-Za-z0-9]{0,5}$/.test(id) || seen[id]) id = null;
    var d = TYPES[c.type], val = c.val;
    if (d.vals.length) {
      if (c.type === "led" || c.type === "diode") { if (d.vals.indexOf(val) < 0) val = d.def; }
      else { val = Number(val); if (d.vals.indexOf(val) < 0) { var best = d.vals[0]; d.vals.forEach(function (v) { if (Math.abs(v - val) < Math.abs(best - val)) best = v; }); val = isNaN(val) ? d.def : best; } }
    } else val = 0;
    var item = { id: id, type: c.type, x: Number(c.x), y: Number(c.y), rot: c.rot ? 1 : 0, val: val, closed: c.closed === undefined ? true : !!c.closed };
    outC.push(item);
    if (id) seen[id] = true;
  });
  outC.forEach(function (c) {
    if (c.id) return;
    var p = TYPES[c.type].prefix, n = 1;
    while (seen[p + n]) n++;
    c.id = p + n; seen[c.id] = true;
  });
  var outW = [];
  (Array.isArray(obj.wires) ? obj.wires : []).slice(0, MAX_WIRES).forEach(function (w) {
    var a, b;
    if (Array.isArray(w)) { a = w[0]; b = w[1]; } else if (w) { a = w.a; b = w.b; }
    var ok = function (k) { return typeof k === "string" && /^[A-Za-z][A-Za-z0-9]{0,5}\.[ab]$/.test(k) && seen[k.split(".")[0]]; };
    if (ok(a) && ok(b) && a !== b) outW.push({ a: a, b: b });
  });
  return { comps: outC, wires: outW };
}
function autoLayout(list) {
  var n = list.length, rows = Math.ceil(n / 2);
  var xs = [cssW * 0.27, cssW * 0.73];
  var top = 60, step = rows > 1 ? Math.min(100, (cssH - top - 40) / (rows - 1)) : 0;
  list.forEach(function (c, i) {
    if (isFinite(c.x) && isFinite(c.y) && c.x > 0 && c.y > 0) return;
    c.x = Math.round(xs[i % 2] / 10) * 10;
    c.y = Math.round((top + Math.floor(i / 2) * step) / 10) * 10;
  });
}
function loadState(obj, forceLayout) {
  var s = sanitizeState(obj); if (!s) return false;
  if (forceLayout) s.comps.forEach(function (c) { c.x = NaN; c.y = NaN; });
  autoLayout(s.comps);
  comps = s.comps; wires = s.wires; sel = null; pending = null;
  if (!forceLayout && obj.meter && typeof obj.meter === "object") {
    var m = obj.meter;
    meter.visible = !!m.visible;
    meter.mode = m.mode === "R" ? "R" : "V";
    meter.x = isFinite(m.x) ? Number(m.x) : 20; meter.y = isFinite(m.y) ? Number(m.y) : 60;
    ["probeA", "probeB"].forEach(function (k) {
      var pr = m[k] || {};
      meter[k].x = isFinite(pr.x) ? Number(pr.x) : 0; meter[k].y = isFinite(pr.y) ? Number(pr.y) : 0;
      meter[k].key = (typeof pr.key === "string" && keyPos(pr.key)) ? pr.key : null;
    });
  }
  ["probeA", "probeB"].forEach(function (k) { if (meter[k].key && !keyPos(meter[k].key)) meter[k].key = null; });
  var mb = document.getElementById("btnMeter");
  if (mb) mb.style.background = meter.visible ? "#0284c7" : "";
  recompute();
  return true;
}
function demo() {
  loadState({
    comps: [
      { id: "B1", type: "battery", val: 9 }, { id: "S1", type: "switch", closed: true },
      { id: "R1", type: "resistor", val: 330 }, { id: "D1", type: "led", val: "red" }
    ],
    wires: [["B1.a", "S1.a"], ["S1.b", "R1.a"], ["R1.b", "D1.a"], ["D1.b", "B1.b"]]
  }, true);
}

/* ===================================================== الذكاء الاصطناعي ========================================== */
var aiPending = {}, reqN = 0;
window.onAiResult = function (id, ok, text) {
  var p = aiPending[id]; if (!p) return;
  delete aiPending[id];
  if (ok) p.res(String(text)); else p.rej(new Error(String(text)));
};
function askAi(mode, payload) {
  return new Promise(function (res, rej) {
    if (!(window.Android && Android.askAi)) { rej(new Error(t("الذكاء الاصطناعي متاح داخل التطبيق فقط.", "AI is only available inside the app."))); return; }
    var id = "r" + (++reqN);
    aiPending[id] = { res: res, rej: rej };
    setTimeout(function () { if (aiPending[id]) { delete aiPending[id]; rej(new Error(t("انتهت المهلة.", "Timed out."))); } }, 135000);
    try { Android.askAi(id, mode, payload); } catch (e) { delete aiPending[id]; rej(e); }
  });
}
function extractJson(text) {
  var a = text.indexOf("{"), b = text.lastIndexOf("}");
  if (a < 0 || b <= a) return null;
  try { return JSON.parse(text.slice(a, b + 1)); } catch (e) { return null; }
}
var busyEl = document.getElementById("busy"), btnGen = document.getElementById("btnGen"), btnExplain = document.getElementById("btnExplain"), btnFix = document.getElementById("btnFix");
function setBusy(v) { busyEl.className = v ? "show" : ""; btnGen.disabled = btnExplain.disabled = btnFix.disabled = v; }

// ---- زر الرسم ----
btnGen.onclick = function () {
  var txt = document.getElementById("aiText").value.trim();
  if (!txt) { setStatus("warn", t("اكتب وصف الدائرة أولاً.", "Describe the circuit first.")); return; }
  setBusy(true);
  askAi("generate", txt).then(function (reply) {
    var obj = extractJson(reply);
    if (!obj || !loadState(obj, true)) throw new Error(t("لم أستطع فهم رد الذكاء الاصطناعي، جرّب وصفاً آخر.", "Could not understand the AI reply — try another description."));
  }).catch(function (e) { setStatus("bad", e.message || String(e)); }).then(function () { setBusy(false); });
};

// ---- زر الشرح ----
btnExplain.onclick = function () {
  if (comps.length === 0) { setStatus("warn", t("لا توجد دائرة لشرحها.", "There is no circuit to explain.")); return; }
  var desc = { components: comps.map(function (c) { var o = { id: c.id, type: c.type, value: c.val }; if (c.type === "switch") o.closed = c.closed; if (sim && sim.ok) { o.voltage_V = +sim.V[c.id].toFixed(3); o.current_A = +sim.I[c.id].toFixed(5); } return o; }),
                wires: wires.map(function (w) { return [w.a, w.b]; }) };
  setBusy(true);
  askAi("explain", JSON.stringify(desc)).then(function (reply) {
    document.getElementById("answerText").textContent = reply;
    document.getElementById("answer").className = "show";
  }).catch(function (e) { setStatus("bad", e.message || String(e)); }).then(function () { setBusy(false); });
};

// ---- زر الإصلاح الذكي ----
btnFix.onclick = function () {
  if (comps.length === 0) { setStatus("warn", t("لا توجد دائرة لإصلاحها.", "There is no circuit to fix.")); return; }
  var errs = sim && sim.ok ? (sim.warnings || []) : [{ k: sim.reason }];
  if (errs.length === 0 && sim && sim.anyCurrent) { 
    setStatus("warn", t("الدائرة تبدو سليمة وتعمل بالفعل!", "The circuit looks fine and is already working!")); 
    return; 
  }
  
  setBusy(true);
  var desc = { 
    error: errs.map(function(w) { return w.k; }).join(", "),
    components: comps.map(function (c) { var o = { id: c.id, type: c.type, value: c.val }; if (c.type === "switch") o.closed = c.closed; return o; }),
    wires: wires.map(function (w) { return [w.a, w.b]; }) 
  };
  
  askAi("fix", JSON.stringify(desc)).then(function (reply) {
    var obj = extractJson(reply);
    if (!obj || !loadState(obj, true)) throw new Error(t("لم أستطع إصلاح الدائرة، حاول تعديلها يدوياً.", "Could not fix the circuit, try editing it manually."));
    setStatus("ok", t("تم إصلاح الدائرة بنجاح! 🪄", "Circuit fixed successfully! 🪄"));
  }).catch(function (e) { setStatus("bad", e.message || String(e)); }).then(function () { setBusy(false); });
};

document.getElementById("btnAnswerClose").onclick = function () { document.getElementById("answer").className = ""; };

/* ================================================== الحفظ السحابي ============================================== */
window.onCloudSaved = function(code) {
  if (code && code.length > 0) {
    prompt(t("تم الحفظ بنجاح! انسخ هذا الكود لاستعادتها لاحقاً:", "Saved successfully! Copy this code to restore it later:"), code);
  } else {
    setStatus("bad", t("تعذّر الحفظ في السحابة.", "Could not save to cloud."));
  }
};
window.onCloudLoaded = function(json) {
  if (json && json.length > 0) {
    try {
      var obj = JSON.parse(json);
      if (loadState(obj, true)) {
        setStatus("ok", t("تم التحميل من السحابة بنجاح!", "Loaded from cloud successfully!"));
      } else {
        setStatus("bad", t("ملف غير صالح.", "Invalid file."));
      }
    } catch(e) { setStatus("bad", t("ملف تالف.", "Corrupted file.")); }
  } else {
    setStatus("bad", t("لم يتم العثور على دائرة بهذا الكود.", "No circuit found with this code."));
  }
};
document.getElementById("btnSave").onclick = function() {
  if (comps.length === 0) { setStatus("warn", t("لا توجد دائرة لحفظها.", "No circuit to save.")); return; }
  var state = JSON.stringify({ comps: comps, wires: wires, meter: meter });
  try { if (window.Android && Android.saveCloud) Android.saveCloud(state); else setStatus("warn", t("غير مدعوم هنا.", "Not supported here.")); } catch(e) {}
};
document.getElementById("btnLoad").onclick = function() {
  var code = prompt(t("أدخل كود التحميل المكون من 6 أحرف:", "Enter the 6-letter load code:"));
  if (code && code.trim().length > 0) {
    try { if (window.Android && Android.loadCloud) Android.loadCloud(code.trim().toUpperCase()); else setStatus("warn", t("غير مدعوم هنا.", "Not supported here.")); } catch(e) {}
  }
};

/* ====================================================== أزرار الرأس ============================================== */
var clearArmed = false, clearTimer = null, btnClear = document.getElementById("btnClear");
btnClear.onclick = function () {
  if (!clearArmed) {
    clearArmed = true; btnClear.textContent = t("تأكيد؟", "Sure?");
    clearTimer = setTimeout(function () { clearArmed = false; btnClear.textContent = t("مسح", "Clear"); }, 3000);
    return;
  }
  clearTimeout(clearTimer); clearArmed = false; btnClear.textContent = t("مسح", "Clear");
  comps = []; wires = []; sel = null; pending = null;
  meter.probeA.key = null; meter.probeB.key = null;
  recompute();
};
document.getElementById("btnDemo").onclick = demo;
document.getElementById("btnClose").onclick = function () { try { if (window.Android && Android.close) { Android.close(); return; } } catch (e) {} history.back(); };

/* ========================================================= البدء ================================================= */
applyLang();
if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener("resize", resize);
resize();
(function init() {
  var saved = "";
  try { if (window.Android && Android.loadState) saved = Android.loadState() || ""; } catch (e) { saved = ""; }
  var ok = false;
  if (saved) { try { ok = loadState(JSON.parse(saved), false); } catch (e) { ok = false; } }
  if (!ok) demo();
})();
</script>
</body>
</html>
'''

# ==============================================================================
# 2) CircuitSimulatorActivity.kt (مع دوال السحابة)
# ==============================================================================
CIRCUIT_ACTIVITY_KT = r'''package com.example.voiceassistant

import android.annotation.SuppressLint
import android.content.SharedPreferences
import android.graphics.Color
import android.os.Bundle
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.core.view.ViewCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import com.example.voiceassistant.data.AiProvider
import com.example.voiceassistant.data.AiSettings
import com.example.voiceassistant.data.CreditsManager
import com.example.voiceassistant.data.LicenseManager
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

class CircuitSimulatorActivity : ComponentActivity() {

    private var web: WebView? = null
    private var arabic: Boolean = true
    private val busy = AtomicBoolean(false)
    private lateinit var prefs: SharedPreferences

    private val http: OkHttpClient by lazy {
        OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(120, TimeUnit.SECONDS)
            .writeTimeout(60, TimeUnit.SECONDS)
            .callTimeout(130, TimeUnit.SECONDS)
            .build()
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arabic = intent.getBooleanExtra("ar", true)
        prefs = getSharedPreferences("circuit_lab", MODE_PRIVATE)

        val bg = Color.parseColor("#0F172A")
        val root = FrameLayout(this)
        root.setBackgroundColor(bg)

        val wv = WebView(this)
        wv.setBackgroundColor(bg)
        wv.layoutParams = FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        )
        val s = wv.settings
        s.javaScriptEnabled = true
        s.domStorageEnabled = false
        s.allowFileAccess = false
        s.allowContentAccess = false
        s.blockNetworkLoads = true
        s.setSupportZoom(false)
        wv.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
                return !request.url.toString().startsWith(PAGE_PREFIX)
            }
        }
        wv.addJavascriptInterface(Bridge(), "Android")
        root.addView(wv)
        web = wv
        setContentView(root)

        WindowCompat.getInsetsController(window, root).isAppearanceLightStatusBars = false
        ViewCompat.setOnApplyWindowInsetsListener(root) { v, insets ->
            val b = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(b.left, b.top, b.right, b.bottom)
            insets
        }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() { finish() }
        })

        wv.loadUrl(PAGE_URL)
    }

    override fun onDestroy() {
        web?.let {
            (it.parent as? ViewGroup)?.removeView(it)
            it.destroy()
        }
        web = null
        super.onDestroy()
    }

    inner class Bridge {
        @JavascriptInterface fun isArabic(): Boolean = arabic
        @JavascriptInterface fun close() { runOnUiThread { finish() } }
        @JavascriptInterface fun saveState(json: String) { if (json.length < 200_000) prefs.edit().putString("state", json).apply() }
        @JavascriptInterface fun loadState(): String = prefs.getString("state", "") ?: ""

        @JavascriptInterface
        fun saveCloud(json: String) {
            Thread {
                try {
                    val base = backendBase()
                    val key = LicenseManager.getBackendKey()
                    val did = CreditsManager.currentDeviceId()
                    if (base.isEmpty() || key.isEmpty() || did.isEmpty()) {
                        runOnUiThread { web?.evaluateJavascript("onCloudSaved('')", null) }
                        return@Thread
                    }
                    val body = JSONObject().put("licenseKey", key).put("deviceId", did).put("circuit", json)
                    val req = Request.Builder().url("$base/api/circuit/save").post(body.toString().toRequestBody("application/json".toMediaType())).build()
                    http.newCall(req).execute().use { r ->
                        val text = r.body?.string() ?: ""
                        val code = if (r.isSuccessful) JSONObject(text).optString("code", "") else ""
                        val safe = JSONObject.quote(code.filter { it.isLetterOrDigit() }.take(16))
                        runOnUiThread { web?.evaluateJavascript("onCloudSaved($safe)", null) }
                    }
                } catch (e: Exception) {
                    runOnUiThread { web?.evaluateJavascript("onCloudSaved('')", null) }
                }
            }.start()
        }

        @JavascriptInterface
        fun loadCloud(code: String) {
            Thread {
                try {
                    val base = backendBase()
                    if (base.isEmpty()) {
                        runOnUiThread { web?.evaluateJavascript("onCloudLoaded('')", null) }
                        return@Thread
                    }
                    val cleanCode = code.filter { it.isLetterOrDigit() }.take(16)
                    if (cleanCode.isEmpty()) {
                        runOnUiThread { web?.evaluateJavascript("onCloudLoaded('')", null) }
                        return@Thread
                    }
                    val req = Request.Builder().url("$base/api/circuit/load/$cleanCode").get().build()
                    http.newCall(req).execute().use { r ->
                        val text = r.body?.string() ?: ""
                        val jsonStr = if (r.isSuccessful) JSONObject(text).optString("circuit", "") else ""
                        val escaped = JSONObject.quote(jsonStr)
                        runOnUiThread { web?.evaluateJavascript("onCloudLoaded($escaped)", null) }
                    }
                } catch (e: Exception) {
                    runOnUiThread { web?.evaluateJavascript("onCloudLoaded('')", null) }
                }
            }.start()
        }

        @JavascriptInterface
        fun askAi(requestId: String, mode: String, payload: String) {
            if (mode != "generate" && mode != "explain" && mode != "fix") {
                deliver(requestId, false, msg("طلب غير صالح.", "Invalid request."))
                return
            }
            if (payload.isBlank() || payload.length > 20_000) {
                deliver(requestId, false, msg("النص فارغ أو طويل جداً.", "The text is empty or too long."))
                return
            }
            if (!busy.compareAndSet(false, true)) {
                deliver(requestId, false, msg("هناك طلب قيد التنفيذ، انتظر قليلاً.", "A request is already running."))
                return
            }
            Thread {
                try {
                    val r = callBackend(mode, payload)
                    deliver(requestId, r.first, r.second)
                } catch (e: Exception) {
                    deliver(requestId, false, msg("حدث خطأ غير متوقع.", "Unexpected error."))
                } finally {
                    busy.set(false)
                }
            }.start()
        }
    }

    private fun msg(ar: String, en: String): String = if (arabic) ar else en
    private fun deliver(requestId: String, ok: Boolean, text: String) {
        val js = "window.onAiResult(" + JSONObject.quote(requestId) + "," + ok + "," + JSONObject.quote(text) + ")"
        runOnUiThread { web?.evaluateJavascript(js, null) }
    }

    private class HttpRes(val code: Int, val text: String)
    private fun backendBase(): String {
        val raw = BuildConfig.VIDEO_SERVER_URL.trim()
        if (raw.isBlank()) return ""
        val withScheme = if (raw.startsWith("http://") || raw.startsWith("https://")) raw else "https://" + raw
        return withScheme.replace("/api/generate-video", "").removeSuffix("/api").trimEnd('/')
    }
    private fun post(url: String, body: JSONObject): HttpRes {
        val req = Request.Builder().url(url).post(body.toString().toRequestBody("application/json; charset=utf-8".toMediaType())).build()
        http.newCall(req).execute().use { r -> return HttpRes(r.code, r.body?.string().orEmpty()) }
    }

    private fun callBackend(mode: String, payload: String): Pair<Boolean, String> {
        val base = backendBase()
        if (base.isEmpty()) return false to msg("عنوان السيرفر غير مضبوط.", "Server URL is not configured.")
        val key = LicenseManager.getBackendKey()
        if (key.isEmpty()) return false to msg("لا يوجد ترخيص مفعّل.", "No active license.")
        val did = CreditsManager.currentDeviceId()
        if (did.isEmpty()) return false to msg("معرّف الجهاز غير جاهز بعد.", "Device id is not ready yet.")

        val selected = AiSettings.selectedProvider()
        val ordered = if (AiSettings.fallbackEnabled()) listOf(selected) + AiProvider.values().filter { it != selected } else listOf(selected)
        val names = ordered.map { it.name.lowercase() }
        val lang = if (arabic) "ar" else "en"

        return try {
            val dedicated = JSONObject().put("licenseKey", key).put("deviceId", did).put("provider", names.first()).put("providers", JSONArray(names)).put("mode", mode).put("prompt", payload).put("lang", lang).put("cost", 1)
            var res = post(base + "/api/ai/circuit", dedicated)

            if (res.code == 404) {
                val viaChat = JSONObject().put("licenseKey", key).put("deviceId", did).put("provider", names.first()).put("providers", JSONArray(names)).put("systemPrompt", systemPrompt(mode, lang)).put("cost", 1).put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", payload)))
                res = post(base + "/api/ai/chat", viaChat)
            }

            if (res.code !in 200..299) return false to httpError(res.code)
            val text = JSONObject(res.text).optString("text", "").trim()
            if (text.isEmpty()) false to msg("وصل رد فارغ من الذكاء الاصطناعي.", "The AI returned an empty reply.")
            else true to text
        } catch (e: IOException) {
            false to msg("تعذّر الاتصال بالسيرفر، تحقق من الإنترنت.", "Could not reach the server — check your connection.")
        } catch (e: Exception) {
            false to msg("رد غير مفهوم من السيرفر.", "Unreadable server reply.")
        }
    }

    private fun httpError(code: Int): String = when (code) {
        402 -> msg("رصيدك غير كافٍ.", "Not enough credits.")
        401, 403 -> msg("الترخيص غير صالح.", "License is not valid.")
        429 -> msg("طلبات كثيرة، حاول بعد قليل.", "Too many requests, try again shortly.")
        else -> msg("خطأ من السيرفر (", "Server error (") + code + ")"
    }

    private fun systemPrompt(mode: String, lang: String): String {
        val language = if (lang == "en") "English" else "Arabic"
        if (mode == "generate") {
            return "You design simple DC circuits for a circuit simulator. Reply with ONE JSON object and nothing else (no markdown). Schema: {\"comps\":[{\"id\":\"B1\",\"type\":\"battery\",\"val\":9},{\"id\":\"S1\",\"type\":\"switch\",\"closed\":true},{\"id\":\"R1\",\"type\":\"resistor\",\"val\":330},{\"id\":\"D1\",\"type\":\"led\",\"val\":\"red\"}],\"wires\":[[\"B1.a\",\"S1.a\"],[\"S1.b\",\"R1.a\"],[\"R1.b\",\"D1.a\"],[\"D1.b\",\"B1.b\"]]}. Allowed types: battery (1.5,3,4.5,5,9,12), resistor (10,47,100,220,330,470,1000,2200,4700,10000), capacitor (10,47,100,470,1000), diode (silicon, germanium), fuse (0.5,1,2,5), led (red,green,yellow,blue,white), bulb (25,50,100), switch. Every part has exactly two terminals a and b. Use ids B1,R1,D1. Always include exactly one battery, close the loop, protect every LED with a series resistor, use at most 12 parts."
        } else if (mode == "fix") {
            return "You are an electronics expert. The user sends a broken circuit as JSON. Fix it so it works perfectly. Return ONLY the fixed JSON object with the same schema (no markdown, no text). Ensure all LEDs have series resistors, there are no short circuits, and all loops are closed."
        } else {
            return "You are an electronics teacher. Explain the given circuit (JSON) in $language, in at most 8 short sentences: what it does, the current path, why each part is there, and any problem. Plain text only."
        }
    }

    companion object {
        private const val PAGE_PREFIX = "file:///android_asset/"
        private const val PAGE_URL = "file:///android_asset/circuit_sim.html"
    }
}
'''

# ==============================================================================
# 3) MainScreen.kt
# ==============================================================================
MAIN_OLD = r'''DropdownMenuItem(
    text = { Text(state.language.tr("السيناريوهات", "Routines")) },
    leadingIcon = { Icon(Icons.Filled.PlayArrow, contentDescription = null) },
    onClick = {
        showSettingsMenu = false
        showRoutines = true
    }
)'''

MAIN_NEW = r'''DropdownMenuItem(
    text = { Text(state.language.tr("مختبر الإلكترونيات", "Electronics Lab")) },
    leadingIcon = { Icon(Icons.Filled.Memory, contentDescription = null) },
    onClick = {
        showSettingsMenu = false
        context.startActivity(
            android.content.Intent(context, com.example.voiceassistant.CircuitSimulatorActivity::class.java)
                .putExtra("ar", state.language == AppLanguage.ARABIC)
        )
    }
)'''

MAIN_ANCHOR_LINE = r'''text = { Text(state.language.tr("السيناريوهات", "Routines")) },'''
MEMORY_IMPORT = "import androidx.compose.material.icons.filled.Memory\n"
IMPORT_ANCHORS = (
    "import androidx.compose.material.icons.filled.Psychology\n",
    "import androidx.compose.material.icons.Icons\n",
)

# ==============================================================================
# 4) AndroidManifest.xml
# ==============================================================================
MANIFEST_OLD = r'''<activity
    android:name=".LiveVisionActivity"
    android:exported="false"
    android:theme="@style/Theme.VoiceAssistant" />'''

MANIFEST_NEW = r'''<activity
    android:name=".CircuitSimulatorActivity"
    android:configChanges="orientation|screenSize|keyboardHidden"
    android:exported="false"
    android:theme="@style/Theme.VoiceAssistant"
    android:windowSoftInputMode="adjustResize" />'''

MANIFEST_ANCHOR_LINE = r'''android:name=".LiveVisionActivity"'''

# ------------------------------------------------------------------------------ أدوات
def die(message):
    raise SystemExit("circuit_patch.py: " + message)

def read(path):
    if not os.path.isfile(path):
        die("الملف غير موجود: %s\n  شغّل setup.py أولاً." % path)
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()

def write(path, text):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def indent_block(block, indent):
    return "\n".join((indent + line) if line.strip() else line for line in block.split("\n"))

def base_indent(text, anchor_line, what):
    pos = text.find(anchor_line)
    if pos < 0:
        die("لم أجد موضع التعديل في %s: %s" % (what, anchor_line))
    lead = text[text.rfind("\n", 0, pos) + 1:pos]
    if lead.strip():
        die("تنسيق غير متوقع في %s حول: %s" % (what, anchor_line))
    return lead[:-4] if len(lead) >= 4 else ""

def insert_after_block(text, old_block, new_block, anchor_line, what):
    base = base_indent(text, anchor_line, what)
    old = indent_block(old_block, base)
    found = text.count(old)
    if found != 1:
        die("الكتلة المتوقعة في %s وُجدت %d مرة." % (what, found))
    return text.replace(old, old + "\n" + indent_block(new_block, base), 1)

# ------------------------------------------------------------------------------ التنفيذ
def main():
    main_text = read(MAIN_SCREEN)
    manifest_text = read(MANIFEST)
    writes = {}
    done, skipped = [], []

    if "CircuitSimulatorActivity" in main_text:
        skipped.append("ui/MainScreen.kt (الزر موجود مسبقاً)")
    else:
        new_main = insert_after_block(main_text, MAIN_OLD, MAIN_NEW, MAIN_ANCHOR_LINE, "ui/MainScreen.kt")
        if MEMORY_IMPORT not in new_main:
            for anchor in IMPORT_ANCHORS:
                if anchor in new_main:
                    new_main = new_main.replace(anchor, anchor + MEMORY_IMPORT, 1)
                    break
            else:
                die("لم أجد موضعاً لإضافة استيراد أيقونة Memory في ui/MainScreen.kt")
        writes[MAIN_SCREEN] = new_main
        done.append("ui/MainScreen.kt (زر «مختبر الإلكترونيات» + استيراد الأيقونة)")

    if "CircuitSimulatorActivity" in manifest_text:
        skipped.append("AndroidManifest.xml (النشاط مسجّل مسبقاً)")
    else:
        writes[MANIFEST] = insert_after_block(
            manifest_text, MANIFEST_OLD, MANIFEST_NEW, MANIFEST_ANCHOR_LINE, "AndroidManifest.xml"
        )
        done.append("AndroidManifest.xml (تسجيل CircuitSimulatorActivity)")

    writes[HTML_PATH] = CIRCUIT_HTML
    writes[ACTIVITY_PATH] = CIRCUIT_ACTIVITY_KT
    done.append("assets/circuit_sim.html")
    done.append("CircuitSimulatorActivity.kt")

    for path, text in writes.items():
        write(path, text)

    print(">> CIRCUIT LAB V3 applied:")
    for item in done:
        print("   + " + item)
    for item in skipped:
        print("   = تخطّي: " + item)

main()
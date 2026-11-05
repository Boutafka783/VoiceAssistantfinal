#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
proteus_patch.py
Adds 4 Proteus-style features to app/src/main/assets/circuit_sim.html (JS/HTML only):
  1) Signal Generator  (type signal_gen: sine / square / triangle, frequency, amplitude + floating panel)
  2) Logic Analyzer    (digital 0/1 mode inside the existing oscilloscope, threshold 2.5 V)
  3) Voltage-colored wires (red > 3 V, blue < 0.5 V, green/yellow in between)
  4) Logic Probes      (draggable probes showing 1 / 0 / Z, saved + restored with the circuit state)

Properties:
  - Idempotent: every feature has a MARK; if the mark is already in the file the feature is skipped.
  - Atomic: all anchors are checked in memory first; if any anchor is missing the file is NOT written.
  - Does not touch CircuitSimulatorActivity.kt, the bridge, or the voice-control code.
Run order in CI:  circuit_patch -> ... -> mech_patch -> proteus_patch -> bridge_patch
"""
import os
import sys

ROOT = os.environ.get("PROJECT_DIR", ".")
HTML_PATH = os.path.join(ROOT, "app", "src", "main", "assets", "circuit_sim.html")

MARK_GEN = "/*PROTEUS_SIGGEN*/"
MARK_LOGIC = "/*PROTEUS_LOGIC*/"
MARK_WIRE = "/*PROTEUS_WIRECOLOR*/"
MARK_PROBE = "/*PROTEUS_PROBES*/"


def die(msg):
    sys.stderr.write("proteus_patch.py: ERROR: " + msg + "\n")
    sys.exit(1)


def read(path):
    if not os.path.isfile(path):
        die("file not found: %s (run the earlier patches first)" % path)
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def append_js(text, js, feature):
    """Insert a JS block right before the LAST </script> of the page."""
    pos = text.rfind("</script>")
    if pos < 0:
        die("[%s] no </script> found in circuit_sim.html" % feature)
    return text[:pos] + js + "\n" + text[pos:]


def apply_feature(text, feature):
    name, mark, edits, block = feature
    if mark in text:
        return text, False
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            die("[%s] anchor must appear exactly once (found %d):\n    %s" % (name, n, old[:110].replace("\n", "\\n")))
        text = text.replace(old, new, 1)
    if block:
        text = append_js(text, block, name)
    if mark not in text:
        die("[%s] internal error: mark not present after patching" % name)
    return text, True


# =====================================================================================================================
# Shared helper: put a new button in the top bar right after the oscilloscope button (and after earlier Proteus buttons)
# =====================================================================================================================
JS_BAR_HELPER = r'''
window.pxAddBar = window.pxAddBar || function (btn) {
  var bar = document.getElementById("paletteBar"), sb = document.getElementById("btnScope");
  if (!bar) return;
  btn.setAttribute("data-px", "1");
  var all = bar.querySelectorAll("[data-px]");
  var anchor = all.length ? all[all.length - 1] : sb;
  if (anchor && anchor.parentNode === bar) anchor.insertAdjacentElement("afterend", btn); else bar.appendChild(btn);
};
'''

# =====================================================================================================================
# Feature 2: Logic Analyzer mode inside the oscilloscope
# =====================================================================================================================
LOGIC_EDITS = [
    # persist the mode with the scope state
    ("return { visible: scope.visible, x: scope.x,",
     "return { visible: scope.visible, logic: !!scope.logic, x: scope.x,"),
    ("scope.visible = !!sc.visible;",
     "scope.visible = !!sc.visible; scope.logic = !!sc.logic;"),
    # trace drawing: digital lanes instead of the analog trace when scope.logic is on
    ("  [scope.probeA, scope.probeB].forEach(function (p) {\n    if (p.data.length < 2) return;",
     "  " + MARK_LOGIC + " if (scope.logic) pxDrawLogic(); else [scope.probeA, scope.probeB].forEach(function (p) {\n    if (p.data.length < 2) return;"),
    ('ctx.fillText("\u00b130V  slow-mo x" + TIME_SCALE,',
     'ctx.fillText((scope.logic ? "LOGIC 2.5V" : "\u00b130V") + "  slow-mo x" + TIME_SCALE,'),
]

LOGIC_JS = MARK_LOGIC + r'''
(function () {
  if (window.__pxLogic) return; window.__pxLogic = 1;
''' + JS_BAR_HELPER + r'''
  var TH = 2.5;
  // two lanes (CH1 on top, CH2 below); square 0/1 steps from the sampled voltages
  window.pxDrawLogic = function () {
    var chans = [scope.probeA, scope.probeB], laneH = scope.h / 2;
    ctx.save();
    chans.forEach(function (p, ci) {
      var top = scope.y + ci * laneH, hiY = top + laneH * 0.30, loY = top + laneH * 0.85;
      ctx.lineWidth = 1; ctx.strokeStyle = "rgba(148,163,184,.35)"; ctx.setLineDash([3, 4]);
      ctx.beginPath(); ctx.moveTo(scope.x, hiY); ctx.lineTo(scope.x + scope.w, hiY); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(scope.x, loY); ctx.lineTo(scope.x + scope.w, loY); ctx.stroke();
      ctx.setLineDash([]);
      if (ci === 1) {
        ctx.strokeStyle = "rgba(148,163,184,.6)";
        ctx.beginPath(); ctx.moveTo(scope.x, top); ctx.lineTo(scope.x + scope.w, top); ctx.stroke();
      }
      if (!p.data || p.data.length < 2) return;
      var dx = scope.w / scope.maxData, prev = null;
      ctx.beginPath(); ctx.strokeStyle = p.col; ctx.lineWidth = 2; ctx.lineJoin = "miter";
      for (var j = 0; j < p.data.length; j++) {
        var x = scope.x + j * dx, lvl = p.data[j] > TH ? 1 : 0, y = lvl ? hiY : loY;
        if (prev === null) ctx.moveTo(x, y);
        else { if (lvl !== prev) ctx.lineTo(x, prev ? hiY : loY); ctx.lineTo(x, y); }
        prev = lvl;
      }
      ctx.lineTo(scope.x + (p.data.length - 1) * dx, prev ? hiY : loY);
      ctx.stroke();
      ctx.fillStyle = prev ? "#4ade80" : "#f87171"; ctx.font = "bold 11px monospace"; ctx.textAlign = "right";
      ctx.fillText(String(prev), scope.x + scope.w - 4, top + 14);
    });
    ctx.restore();
  };

  var btn = document.createElement("button");
  btn.id = "btnLogicMode";
  btn.textContent = "\u{1F4CA} " + (AR ? "محلل منطق" : "Logic");
  function paint() { btn.style.background = scope.logic ? "#0284c7" : ""; }
  btn.onclick = function () {
    scope.logic = !scope.logic;
    if (scope.logic && !scope.visible) { var sb = document.getElementById("btnScope"); if (sb) sb.click(); }
    paint(); draw(); scheduleSave();
  };
  window.pxAddBar(btn);
  paint();

  // keep the button highlight in sync after a state load
  var _load = loadState;
  loadState = function () { var r = _load.apply(this, arguments); paint(); return r; };
})();
'''

# =====================================================================================================================
# Feature 1: Signal Generator
# =====================================================================================================================
GEN_EDITS = [
    # new part type (TYPES is an object, so we add a key)
    ('ac_source:  { prefix: "AC", ar: "تيار متردد", en: "AC Source", vals: [5, 12, 24], def: 12 },',
     'ac_source:  { prefix: "AC", ar: "تيار متردد", en: "AC Source", vals: [5, 12, 24], def: 12 },\n'
     '  ' + MARK_GEN + ' signal_gen: { prefix: "SG", ar: "مولد إشارات", en: "Signal Generator", vals: [1, 2, 3.3, 5, 9, 12, 24], def: 5 },'),
    # it is a voltage source
    ('function isSource(c) { c = aliasView(c); return c.type === "battery" || c.type === "ac_source" ||',
     'function isSource(c) { c = aliasView(c); return c.type === "battery" || c.type === "ac_source" || c.type === "signal_gen" ||'),
    # waveform maths: depends on time (timeSec) and wave type
    ('function srcV(c, t) { return c.type === "ac_source" ? c.val * Math.sin(2 * Math.PI * 50 * t) : c.val; }',
     'function srcV(c, t) {\n'
     '  if (c.type === "signal_gen") {\n'
     '    var A = (isFinite(c.amp) && c.amp > 0) ? Number(c.amp) : c.val;\n'
     '    var F = (isFinite(c.freq) && c.freq > 0) ? Number(c.freq) : 50;\n'
     '    var ph = 2 * Math.PI * F * t;\n'
     '    if (c.wave === "square") return A * (Math.sin(ph) >= 0 ? 1 : -1);\n'
     '    if (c.wave === "triangle") return A * (2 / Math.PI) * Math.asin(Math.sin(ph));\n'
     '    return A * Math.sin(ph);\n'
     '  }\n'
     '  return c.type === "ac_source" ? c.val * Math.sin(2 * Math.PI * 50 * t) : c.val;\n'
     '}'),
    ('vcc = bat.type === "ac_source" ? 5 : bat.val;',
     'vcc = (bat.type === "ac_source" || bat.type === "signal_gen") ? 5 : bat.val;'),
    # time-varying source: keep the animation clock + auto recompute running
    ('function hasAC() { return comps.some(function (c) { return c.type === "ac_source"; }); }',
     'function hasAC() { return comps.some(function (c) { return c.type === "ac_source" || c.type === "signal_gen"; }); }'),
    ('if (c.type === "ac_source") return c.val + "V AC";',
     'if (c.type === "ac_source") return c.val + "V AC";\n'
     '  if (c.type === "signal_gen") return ((isFinite(c.amp) && c.amp > 0) ? c.amp : c.val) + "V " + ((isFinite(c.freq) && c.freq > 0) ? c.freq : 50) + "Hz " + (c.wave === "square" ? "\u2293" : c.wave === "triangle" ? "\u25B3" : "\u223F");'),
    # palette ("Sources" tab)
    ('types: ["battery", "ac_source", "arduino"',
     'types: ["battery", "ac_source", "signal_gen", "arduino"'),
    # symbol on the canvas (new branch before the ac_source symbol)
    ('} else if (c.type === "ac_source") {',
     '} else if (c.type === "signal_gen") {\n'
     '    line(-HL, 0, -16, 0); line(16, 0, HL, 0);\n'
     '    ctx.beginPath(); ctx.arc(0, 0, 16, 0, Math.PI * 2); ctx.stroke();\n'
     '    ctx.beginPath();\n'
     '    if (c.wave === "square") { ctx.moveTo(-9, 4); ctx.lineTo(-9, -5); ctx.lineTo(0, -5); ctx.lineTo(0, 5); ctx.lineTo(9, 5); ctx.lineTo(9, -3); }\n'
     '    else if (c.wave === "triangle") { ctx.moveTo(-9, 0); ctx.lineTo(-4.5, -6); ctx.lineTo(4.5, 6); ctx.lineTo(9, 0); }\n'
     '    else { ctx.moveTo(-9, 0); ctx.quadraticCurveTo(-4.5, -12, 0, 0); ctx.quadraticCurveTo(4.5, 12, 9, 0); }\n'
     '    ctx.stroke();\n'
     '    ctx.save(); ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center"; ctx.fillText(((isFinite(c.freq) && c.freq > 0) ? c.freq : 50) + "Hz", 0, 29); ctx.restore();\n'
     '  } else if (c.type === "ac_source") {'),
    # PCB footprint = same as a battery/source
    ('if (type === "battery" || type === "ac_source" || type === "arduino" || type === "esp32")',
     'if (type === "battery" || type === "ac_source" || type === "signal_gen" || type === "arduino" || type === "esp32")'),
    # save/load: keep wave / freq / amp
    ('outC.push(item);',
     'if (c.type === "signal_gen") {\n'
     '      item.wave = (c.wave === "square" || c.wave === "triangle") ? c.wave : "sine";\n'
     '      var pxF = Number(c.freq); item.freq = (isFinite(pxF) && pxF > 0) ? Math.max(0.1, Math.min(1000, pxF)) : 50;\n'
     '      var pxA = Number(c.amp); item.amp = (isFinite(pxA) && pxA > 0) ? Math.min(50, pxA) : item.val;\n'
     '    }\n'
     '    outC.push(item);'),
]

GEN_JS = MARK_GEN + r'''
(function () {
  if (window.__pxGen) return; window.__pxGen = 1;
''' + JS_BAR_HELPER + r'''
  var panel = document.createElement("div");
  panel.id = "pxGenPanel";
  panel.style.cssText = "display:none;position:fixed;top:120px;left:8px;z-index:60;width:230px;background:var(--panel,#1e293b);color:var(--text,#e2e8f0);" +
    "border:1px solid var(--line,#334155);border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.45);font-size:13px;overflow:hidden";
  var inp = "width:100%;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:8px;padding:6px 8px;font-size:16px;margin-top:3px";
  panel.innerHTML =
    '<div id="pxGenHead" style="display:flex;align-items:center;gap:6px;padding:8px 10px;background:#0f172a;cursor:move;touch-action:none;user-select:none">' +
    '<b style="flex:1">\u{1F4E1} ' + t("مولد الإشارات", "Signal Generator") + '</b>' +
    '<button id="pxGenClose" style="padding:2px 8px">\u2715</button></div>' +
    '<div style="padding:10px;display:flex;flex-direction:column;gap:8px">' +
    '<div id="pxGenTarget" style="color:#94a3b8;font-size:12px"></div>' +
    '<label>' + t("نوع الموجة", "Waveform") + '<select id="pxWave" style="' + inp + '">' +
    '<option value="sine">Sine</option><option value="square">Square</option><option value="triangle">Triangle</option></select></label>' +
    '<label>' + t("التردد (Hz)", "Frequency (Hz)") + '<input id="pxFreq" type="number" min="0.1" max="1000" step="any" style="' + inp + '"></label>' +
    '<label>' + t("الجهد (V)", "Amplitude (V)") + '<input id="pxAmp" type="number" min="0.1" max="50" step="any" style="' + inp + '"></label>' +
    '<button id="pxGenAdd" class="primary">+ ' + t("إضافة مولد", "Add generator") + '</button>' +
    '<div style="color:#94a3b8;font-size:11px">' + t("المحاكاة بالحركة البطيئة ×", "Slow-motion simulation ×") + TIME_SCALE + '</div></div>';
  document.body.appendChild(panel);
  var elWave = panel.querySelector("#pxWave"), elFreq = panel.querySelector("#pxFreq"), elAmp = panel.querySelector("#pxAmp"), elTgt = panel.querySelector("#pxGenTarget");
  var lastId = null;

  function target() {
    if (sel && sel.kind === "comp") { var s = findComp(sel.id); if (s && s.type === "signal_gen") return s; }
    for (var i = 0; i < comps.length; i++) if (comps[i].type === "signal_gen") return comps[i];
    return null;
  }
  function fill() {
    var c = target();
    elTgt.textContent = c ? (t("العنصر: ", "Part: ") + c.id) : t("لا يوجد مولد — اضغط إضافة", "No generator — tap Add");
    [elWave, elFreq, elAmp].forEach(function (e) { e.disabled = !c; });
    if (!c) return;
    elWave.value = (c.wave === "square" || c.wave === "triangle") ? c.wave : "sine";
    elFreq.value = (isFinite(c.freq) && c.freq > 0) ? c.freq : 50;
    elAmp.value = (isFinite(c.amp) && c.amp > 0) ? c.amp : c.val;
  }
  function apply(commit) {
    var c = target(); if (!c) return;
    if (commit) snap();
    c.wave = (elWave.value === "square" || elWave.value === "triangle") ? elWave.value : "sine";
    var f = parseFloat(elFreq.value); c.freq = isFinite(f) ? Math.max(0.1, Math.min(1000, f)) : 50;
    var a = parseFloat(elAmp.value); c.amp = isFinite(a) ? Math.max(0.1, Math.min(50, a)) : 5;
    var vals = TYPES.signal_gen.vals, best = vals[0];
    vals.forEach(function (v) { if (Math.abs(v - c.amp) < Math.abs(best - c.amp)) best = v; });
    c.val = best;
    recompute();
  }
  elWave.addEventListener("change", function () { apply(true); });
  [elFreq, elAmp].forEach(function (e) {
    e.addEventListener("input", function () { apply(false); });
    e.addEventListener("change", function () { apply(true); });
  });
  panel.querySelector("#pxGenAdd").onclick = function () {
    snap();
    var s = freeSpot(), c = addComp("signal_gen", s.x, s.y);
    if (!c) return;
    c.wave = "sine"; c.freq = 50; c.amp = c.val; sel = { kind: "comp", id: c.id }; pending = null;
    lastId = null; recompute(); fill();
  };
  panel.querySelector("#pxGenClose").onclick = function () { panel.style.display = "none"; btn.style.background = ""; };

  // draggable floating panel
  (function () {
    var head = panel.querySelector("#pxGenHead"), dr = null;
    head.addEventListener("pointerdown", function (e) {
      if (e.target.tagName === "BUTTON") return;
      var r = panel.getBoundingClientRect(); dr = { ox: e.clientX - r.left, oy: e.clientY - r.top };
      try { head.setPointerCapture(e.pointerId); } catch (x) {}
    });
    head.addEventListener("pointermove", function (e) {
      if (!dr) return;
      panel.style.left = Math.max(0, Math.min(window.innerWidth - 60, e.clientX - dr.ox)) + "px";
      panel.style.top = Math.max(0, Math.min(window.innerHeight - 40, e.clientY - dr.oy)) + "px";
    });
    head.addEventListener("pointerup", function () { dr = null; });
    head.addEventListener("pointercancel", function () { dr = null; });
  })();

  var btn = document.createElement("button");
  btn.id = "btnSigGen";
  btn.textContent = "\u{1F4E1} " + t("مولد", "Sig Gen");
  btn.onclick = function () {
    var open = panel.style.display === "none";
    panel.style.display = open ? "block" : "none";
    btn.style.background = open ? "#0284c7" : "";
    if (open) { lastId = null; fill(); }
  };
  window.pxAddBar(btn);

  // follow the selection while the panel is open (does not overwrite what the user is typing)
  var _draw = draw;
  draw = function () {
    _draw();
    if (panel.style.display !== "none") {
      var c = target(), id = c ? c.id : "";
      if (id !== lastId) { lastId = id; fill(); }
    }
  };
  // the +/- tool buttons change c.val; keep the real amplitude in sync
  var _step = stepValue;
  stepValue = function () {
    _step.apply(this, arguments);
    var c = sel && sel.kind === "comp" ? findComp(sel.id) : null;
    if (c && c.type === "signal_gen") { c.amp = c.val; recompute(); if (panel.style.display !== "none") fill(); }
  };
})();
'''

# =====================================================================================================================
# Feature 3: voltage-colored wires
# =====================================================================================================================
WIRE_EDITS = [
    ('ctx.strokeStyle = isSel ? "#38bdf8" : (live ? "#fbbf24" : "#64748b");',
     'ctx.strokeStyle = isSel ? "#38bdf8" : pxWireColor(w, live);'),
]

WIRE_JS = MARK_WIRE + r'''
// wire colour from the node voltage: > 3 V red, < 0.5 V blue, otherwise green (low) / yellow (high)
function pxWireColor(w, live) {
  try {
    if (!(sim && sim.ok && sim.anyCurrent)) return "#64748b";
    var v = sim.nodeV(w.a);
    if (!isFinite(v)) return live ? "#fbbf24" : "#64748b";
    if (v > 3) return "#ef4444";
    if (v < 0.5) return "#3b82f6";
    return v > 1.75 ? "#fbbf24" : "#4ade80";
  } catch (e) { return live ? "#fbbf24" : "#64748b"; }
}
'''

# =====================================================================================================================
# Feature 4: Logic probes (1 / 0 / Z), saved with the circuit
# =====================================================================================================================
PROBE_EDITS = [
    ("scope: scopeState() }",
     "scope: scopeState(), probes: (window.proteusProbes || []).map(function (p) { return { x: p.x, y: p.y, key: p.key }; }) }"),
]

PROBE_JS = MARK_PROBE + r'''
(function () {
  if (window.__pxProbe) return; window.__pxProbe = 1;
''' + JS_BAR_HELPER + r'''
  var probes = window.proteusProbes = [];
  var mode = false, MAXP = 8, R = 11, pd = null, TH = 2.5;
  var COL = { "1": "#4ade80", "0": "#f87171", "Z": "#94a3b8" };

  function wired(key) { return wires.some(function (w) { return w.a === key || w.b === key; }); }
  function reading(p) {
    if (!p.key || !(sim && sim.ok) || !wired(p.key)) return "Z";
    var v = sim.nodeV(p.key);
    if (!isFinite(v)) return "Z";
    return v > TH ? "1" : "0";
  }
  function where(p) {
    var tp = p.key ? keyPos(p.key) : null;
    return tp ? { x: tp.x, y: tp.y - 22, tx: tp.x, ty: tp.y, snapped: true } : { x: p.x, y: p.y, snapped: false };
  }
  function hitProbe(pt) {
    for (var i = probes.length - 1; i >= 0; i--) { var q = where(probes[i]); if (Math.hypot(q.x - pt.x, q.y - pt.y) < R + 9) return i; }
    return -1;
  }
  function overTool(pt) {
    var hit = false;
    [meter, scope].forEach(function (T) {
      if (!T.visible) return;
      if (pt.x > T.x && pt.x < T.x + T.w && pt.y > T.y && pt.y < T.y + T.h) hit = true;
      [T.probeA, T.probeB].forEach(function (pr) { var q = probePos(pr); if (Math.hypot(q.x - pt.x, q.y - pt.y) < 20) hit = true; });
    });
    return hit;
  }

  function drawProbes() {
    if (!probes.length && !mode) return;
    ctx.save();
    probes.forEach(function (p) {
      if (p.key && !keyPos(p.key)) p.key = null;
      var q = where(p), r = reading(p), col = COL[r];
      if (q.snapped) {
        ctx.beginPath(); ctx.moveTo(q.tx, q.ty); ctx.lineTo(q.x, q.y + R); ctx.lineWidth = 2; ctx.strokeStyle = col; ctx.stroke();
        ctx.beginPath(); ctx.arc(q.tx, q.ty, 3.5, 0, Math.PI * 2); ctx.fillStyle = col; ctx.fill();
      }
      ctx.beginPath(); ctx.arc(q.x, q.y, R, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(15,23,42,.95)"; ctx.fill();
      ctx.lineWidth = 2.5; ctx.strokeStyle = col; ctx.stroke();
      ctx.fillStyle = col; ctx.font = "bold 14px monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText(r, q.x, q.y + 1);
    });
    if (pd && pd.hover) {
      var hp = keyPos(pd.hover);
      if (hp) { ctx.beginPath(); ctx.arc(hp.x, hp.y, 12, 0, Math.PI * 2); ctx.lineWidth = 2; ctx.strokeStyle = "#38bdf8"; ctx.stroke(); }
    }
    if (mode) {
      ctx.fillStyle = "#94a3b8"; ctx.font = "11px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
      ctx.fillText(t("وضع المجس: المس فراغاً لإضافة مجس · اسحبه إلى طرف · المس مجساً لحذفه",
                     "Probe mode: tap empty space to add · drag onto a terminal · tap a probe to delete"), cssW / 2, 14);
    }
    ctx.restore();
  }

  var _draw = draw;
  draw = function () { _draw(); drawProbes(); };

  // pointer handling in the capture phase on the parent of the canvas, so it runs before the original handlers
  var stage = cv.parentNode;
  stage.addEventListener("pointerdown", function (e) {
    if (!mode || e.target !== cv) return;
    var pt = evPos(e), i = hitProbe(pt);
    if (i < 0) {
      if (overTool(pt) || hitTerminal(pt) || hitComp(pt) || hitWire(pt) >= 0) return; // let the normal editor handle it
      if (probes.length >= MAXP) return;
      probes.push({ x: pt.x, y: pt.y, key: null });
      pd = { i: probes.length - 1, sx: pt.x, sy: pt.y, moved: false, isNew: true, hover: null };
    } else {
      pd = { i: i, sx: pt.x, sy: pt.y, moved: false, isNew: false, hover: null };
    }
    try { cv.setPointerCapture(e.pointerId); } catch (x) {}
    e.stopImmediatePropagation(); e.preventDefault();
  }, true);
  stage.addEventListener("pointermove", function (e) {
    if (!pd) return;
    var pt = evPos(e), p = probes[pd.i];
    if (!p) { pd = null; return; }
    if (!pd.moved && Math.hypot(pt.x - pd.sx, pt.y - pd.sy) < 6) return;
    pd.moved = true; p.x = pt.x; p.y = pt.y; p.key = null; pd.hover = hitTerminal(pt);
    draw();
  }, true);
  stage.addEventListener("pointerup", function (e) {
    if (!pd) return;
    var pt = evPos(e), p = probes[pd.i], d = pd; pd = null;
    if (p) {
      if (!d.moved && !d.isNew) probes.splice(d.i, 1);                 // tap = delete
      else if (d.moved) { var tk = hitTerminal(pt); p.key = tk || null; if (!tk) { p.x = pt.x; p.y = pt.y; } }
    }
    scheduleSave(); draw();
    e.stopImmediatePropagation();
  }, true);
  stage.addEventListener("pointercancel", function () { pd = null; }, true);

  var btn = document.createElement("button");
  btn.id = "btnLogicProbe";
  btn.textContent = "\u{1F50D} " + t("مجس", "Probe");
  btn.onclick = function () {
    mode = !mode;
    btn.style.background = mode ? "#0284c7" : "";
    if (mode && !probes.length) { probes.push({ x: Math.round(cssW / 2), y: 70, key: null }); scheduleSave(); }
    draw();
  };
  window.pxAddBar(btn);

  // restore the probes together with the rest of the saved circuit
  var _load = loadState;
  loadState = function (obj, forceLayout) {
    var ok = _load.apply(this, arguments);
    if (ok) {
      probes.length = 0;
      if (!forceLayout && obj && Array.isArray(obj.probes)) {
        obj.probes.slice(0, MAXP).forEach(function (q) {
          if (!q || !isFinite(q.x) || !isFinite(q.y)) return;
          var k = (typeof q.key === "string" && keyPos(q.key)) ? q.key : null;
          probes.push({ x: Number(q.x), y: Number(q.y), key: k });
        });
      }
      draw();
    }
    return ok;
  };
})();
'''

# Order matters only for the order of the top-bar buttons: [Scope][Logic][Sig Gen][Probe]
FEATURES = [
    ("Logic Analyzer", MARK_LOGIC, LOGIC_EDITS, LOGIC_JS),
    ("Signal Generator", MARK_GEN, GEN_EDITS, GEN_JS),
    ("Voltage-colored wires", MARK_WIRE, WIRE_EDITS, WIRE_JS),
    ("Logic Probes", MARK_PROBE, PROBE_EDITS, PROBE_JS),
]


def main():
    original = read(HTML_PATH)
    text = original
    done, skipped = [], []
    for feature in FEATURES:
        text, changed = apply_feature(text, feature)
        (done if changed else skipped).append(feature[0])
    if text != original:
        write(HTML_PATH, text)
    print(">> PROTEUS patch:")
    for n in done:
        print("   + " + n)
    for n in skipped:
        print("   = " + n + " (already applied)")


main()

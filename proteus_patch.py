#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
proteus_patch.py
Adds 15 Proteus-style features (v4 = v3's ten + five new ones) to app/src/main/assets/circuit_sim.html (JS/HTML only):
  1) Signal Generator  (type signal_gen: sine / square / triangle, frequency, amplitude + floating panel)
  2) Logic Analyzer    (digital 0/1 mode inside the existing oscilloscope, threshold 2.5 V)
  3) Voltage-colored wires (red > 3 V, blue < 0.5 V, green/yellow in between)
  4) Logic Probes      (draggable probes showing 1 / 0 / Z, saved + restored with the circuit state)
  5) Orthogonal wires  (wires drawn as 90-degree L-routes; hit-testing follows the drawn route)
  6) V/A probes        (top-bar "V/A" button: draggable voltage/current tags on wires, saved + restored)
  7) Properties editor (tap a part -> pencil icon, or long-press -> dialog to type c.val; recompute() runs at once)
  8) Interactive 7-seg / LCD (dynamic digit from the pin voltage; LCD shows READY + voltage; hooked at the end of the existing branch)
  9) Netlist export    (top-bar button, builds "R1 1 2 1000" lines from wires/comps and writes them with saveFile)
 10) Scope cursors     (draggable T1/T2 lines: dT, f, V1, V2; saved with the circuit)

New in v4:
 11) Component labels  (properties pencil gets a "Rename" pill: c.id + every wire / probe key follows the new name)
 12) Simulation speed  (top-bar 0.1x / 1x / 10x -> TIME_SCALE, scope traces cleared, recompute())
 13) Mirroring         (bottom-toolbar "Flip" -> c.flipX; drawComp mirrored with ctx.scale(-1, 1); saved with the circuit)
 14) Net highlighting  (select a wire -> the whole net glows cyan, its terminals are circled)
 15) Fault injection   (top-bar "Fault" -> w.cut = true: the solver ignores the wire; drawn red dashed with an X)

Properties:
  - Idempotent: every feature has a MARK; if the mark is already in the file the feature is skipped.
  - Atomic: all anchors are checked in memory first; if any anchor is missing the file is NOT written.
  - Does not touch CircuitSimulatorActivity.kt, the bridge, or the voice-control code.
Run order in CI:  circuit_patch -> ... -> mech_patch -> proteus_patch -> bridge_patch
"""
import os
import re
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
    for edit in edits:
        if callable(edit):                      # soft transform: never aborts, may append to WARNINGS
            text = edit(text)
            continue
        old, new = edit
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

# =====================================================================================================================
# Feature 5: Orthogonal wire routing (Proteus-style 90-degree wires)
#   - draw(): the straight p1->p2 segment becomes p1 -> elbow -> p2 (horizontal first, then vertical)
#   - hitWire(): hit-testing follows the drawn (orthogonal) path, not the invisible diagonal
# =====================================================================================================================
MARK_ORTHO = "/*PROTEUS_ORTHO*/"

ORTHO_EDITS = [
    ("ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);",
     "ctx.moveTo(p1.x, p1.y); " + MARK_ORTHO + " pxOrthoTo(p1, p2);"),
]

ORTHO_JS = MARK_ORTHO + r'''
// set to true for "vertical first, then horizontal"
var PX_ORTHO_V_FIRST = false;

// points of the orthogonal route between two terminals: [p1, elbow, p2] (or [p1, p2] when already aligned)
function pxOrthoPts(p1, p2) {
  if (Math.abs(p1.x - p2.x) < 0.5 || Math.abs(p1.y - p2.y) < 0.5) return [p1, p2];
  return [p1, PX_ORTHO_V_FIRST ? { x: p1.x, y: p2.y } : { x: p2.x, y: p1.y }, p2];
}
// continues the current canvas path (after moveTo(p1)) through the elbow to p2
function pxOrthoTo(p1, p2) {
  var P = pxOrthoPts(p1, p2);
  for (var i = 1; i < P.length; i++) ctx.lineTo(P[i].x, P[i].y);
}
// route of a wire object, or null when one of its terminals no longer exists
function pxWirePath(w) {
  var a = keyPos(w.a), b = keyPos(w.b);
  return (a && b) ? pxOrthoPts(a, b) : null;
}
function pxPathDist(P, pt) {
  var best = Infinity;
  for (var i = 1; i < P.length; i++) {
    var a = P[i - 1], b = P[i], dx = b.x - a.x, dy = b.y - a.y, l2 = dx * dx + dy * dy;
    var u = l2 ? ((pt.x - a.x) * dx + (pt.y - a.y) * dy) / l2 : 0;
    u = Math.max(0, Math.min(1, u));
    var d = Math.hypot(pt.x - (a.x + u * dx), pt.y - (a.y + u * dy));
    if (d < best) best = d;
  }
  return best;
}
(function () {
  if (window.__pxOrtho) return; window.__pxOrtho = 1;
  if (typeof hitWire !== "function") return;
  // the drawn wire is now an L-shape, so selecting / deleting it must test that shape
  hitWire = function (pt) {
    for (var i = wires.length - 1; i >= 0; i--) {
      var P = pxWirePath(wires[i]);
      if (P && pxPathDist(P, pt) < 9) return i;
    }
    return -1;
  };
})();
'''

# =====================================================================================================================
# Feature 6: V/A probes (voltmeter / ammeter tags that sit on a wire), saved with the circuit
#   - top-bar button "V/A": tap empty space (or the wire itself) to add a probe, drag it onto any wire
#   - tap a probe: V -> A -> delete.   V reads sim.nodeV(wire.a),  A reads sim.I (see pxReadWireCurrent)
# =====================================================================================================================
MARK_VAPROBE = "/*PROTEUS_VAPROBE*/"

VAPROBE_EDITS = [
    # scheduleSave payload: add "vaprobes" right after the logic "probes" array written by Feature 4
    ("probes: (window.proteusProbes || []).map(function (p) { return { x: p.x, y: p.y, key: p.key }; }) }",
     "probes: (window.proteusProbes || []).map(function (p) { return { x: p.x, y: p.y, key: p.key }; }), "
     + MARK_VAPROBE + " vaprobes: (window.proteusVAProbes || []).map(function (p) { "
     + 'return { kind: p.kind === "A" ? "A" : "V", a: p.a || null, b: p.b || null, s: p.s, x: p.x, y: p.y }; }) }'),
]

VAPROBE_JS = MARK_VAPROBE + r'''
(function () {
  if (window.__pxVA) return; window.__pxVA = 1;
''' + JS_BAR_HELPER + r'''
  var vps = window.proteusVAProbes = [];
  var mode = false, MAXP = 8, SNAP = 16, pd = null;
  var COL = { V: "#fbbf24", A: "#38bdf8" };
  var wirePath = (typeof pxWirePath === "function") ? pxWirePath : function (w) {
    var a = keyPos(w.a), b = keyPos(w.b); return (a && b) ? [a, b] : null;
  };

  // ---------- readings ----------
  function num(x) { return (typeof x === "number" && isFinite(x)) ? x : null; }
  function readV(w) {
    try { return (sim && sim.ok) ? num(sim.nodeV(w.a)) : null; } catch (e) { return null; }
  }
  // Current through a wire. Override window.pxReadWireCurrent if your sim exposes currents differently.
  window.pxReadWireCurrent = window.pxReadWireCurrent || function (w) {
    var I = sim.I, v = null;
    if (typeof I === "function") {
      v = num(I.call(sim, w));
      if (v === null) v = num(I.call(sim, w.a, w.b));
      if (v === null) v = num(I.call(sim, w.a));
    } else if (I && typeof I === "object") {
      var ks = [w.id, w.a, w.b, w.a + "|" + w.b, w.a + "-" + w.b];
      for (var k = 0; k < ks.length && v === null; k++) if (ks[k] !== undefined) v = num(I[ks[k]]);
    }
    return v;
  };
  function readI(w) {
    try { return (sim && sim.ok) ? window.pxReadWireCurrent(w) : null; } catch (e) { return null; }
  }
  function fmtV(v) {
    if (v === null) return "--";
    var a = Math.abs(v);
    if (a < 0.0005) return "0.0V";
    if (a < 1) return (v * 1000).toFixed(a * 1000 >= 100 ? 0 : 1) + "mV";
    return v.toFixed(a >= 100 ? 0 : 1) + "V";
  }
  function fmtI(i) {
    if (i === null) return "--";
    var a = Math.abs(i);                       // magnitude only: the sign has no meaning on a bare wire
    if (a < 1e-9) return "0mA";
    if (a >= 1) return a.toFixed(2) + "A";
    if (a >= 0.001) return (a * 1000).toFixed(a * 1000 >= 10 ? 0 : 1) + "mA";
    return (a * 1e6).toFixed(a * 1e6 >= 10 ? 0 : 1) + "\u00B5A";
  }

  // ---------- geometry along the orthogonal wire ----------
  function pathLen(P) { var L = 0; for (var i = 1; i < P.length; i++) L += Math.hypot(P[i].x - P[i - 1].x, P[i].y - P[i - 1].y); return L; }
  function pointAt(P, s) {
    var d = Math.max(0, Math.min(1, s)) * pathLen(P);
    for (var i = 1; i < P.length; i++) {
      var seg = Math.hypot(P[i].x - P[i - 1].x, P[i].y - P[i - 1].y);
      if (d <= seg || i === P.length - 1) {
        var f = seg ? Math.min(1, d / seg) : 0;
        return { x: P[i - 1].x + (P[i].x - P[i - 1].x) * f, y: P[i - 1].y + (P[i].y - P[i - 1].y) * f };
      }
      d -= seg;
    }
    return { x: P[0].x, y: P[0].y };
  }
  function project(P, pt) {
    var best = { d: Infinity, s: 0 }, L = pathLen(P) || 1, acc = 0;
    for (var i = 1; i < P.length; i++) {
      var a = P[i - 1], b = P[i], dx = b.x - a.x, dy = b.y - a.y, l2 = dx * dx + dy * dy, seg = Math.sqrt(l2);
      var u = l2 ? ((pt.x - a.x) * dx + (pt.y - a.y) * dy) / l2 : 0;
      u = Math.max(0, Math.min(1, u));
      var d = Math.hypot(pt.x - (a.x + u * dx), pt.y - (a.y + u * dy));
      if (d < best.d) best = { d: d, s: (acc + u * seg) / L };
      acc += seg;
    }
    return best;
  }
  // a probe is bound to a wire by its two terminal keys (+ position s along the route), so it survives moves/reloads
  function findWire(p) {
    if (!p.a || !p.b) return null;
    for (var i = 0; i < wires.length; i++) {
      var w = wires[i];
      if (w.a === p.a && w.b === p.b) return w;
      if (w.a === p.b && w.b === p.a) { p.a = w.a; p.b = w.b; p.s = 1 - p.s; return w; }
    }
    return null;
  }
  function attach(p, pt) {
    var bw = null, bd = SNAP, bs = 0;
    for (var i = wires.length - 1; i >= 0; i--) {
      var P = wirePath(wires[i]); if (!P) continue;
      var r = project(P, pt);
      if (r.d < bd) { bd = r.d; bw = wires[i]; bs = r.s; }
    }
    if (bw) { p.a = bw.a; p.b = bw.b; p.s = bs; } else { p.a = null; p.b = null; }
    return bw;
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
  function hitVP(pt) {
    for (var i = vps.length - 1; i >= 0; i--) {
      var r = vps[i]._r;
      if (r && pt.x >= r.x0 - 4 && pt.x <= r.x1 + 4 && pt.y >= r.y0 - 4 && pt.y <= r.y1 + 8) return i;
    }
    return -1;
  }

  // ---------- drawing ----------
  function rr(x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.arcTo(x + w, y, x + w, y + r, r);
    ctx.lineTo(x + w, y + h - r); ctx.arcTo(x + w, y + h, x + w - r, y + h, r); ctx.lineTo(x + r, y + h);
    ctx.arcTo(x, y + h, x, y + h - r, r); ctx.lineTo(x, y + r); ctx.arcTo(x, y, x + r, y, r); ctx.closePath();
  }
  function drawVA() {
    if (!vps.length && !mode) return;
    ctx.save();
    if (pd && pd.moved) {                                  // highlight the wire the probe will snap to
      var hw = findWire(vps[pd.i] || {}), HP = hw ? wirePath(hw) : null;
      if (HP) {
        ctx.beginPath(); ctx.moveTo(HP[0].x, HP[0].y);
        for (var k = 1; k < HP.length; k++) ctx.lineTo(HP[k].x, HP[k].y);
        ctx.lineWidth = 8; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = "rgba(56,189,248,.35)"; ctx.stroke();
      }
    }
    vps.forEach(function (p) {
      var w = findWire(p), P = w ? wirePath(w) : null, x = p.x, y = p.y, txt = "?";
      if (P) { var q = pointAt(P, p.s); x = p.x = q.x; y = p.y = q.y; txt = p.kind === "A" ? fmtI(readI(w)) : fmtV(readV(w)); }
      var col = COL[p.kind === "A" ? "A" : "V"];
      ctx.font = "bold 12px monospace";
      var tw = Math.ceil(ctx.measureText(txt).width) + 14, th = 20, bx = x - tw / 2, by = y - 14 - th;
      p._r = { x0: bx, y0: by, x1: bx + tw, y1: y };
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, by + th); ctx.lineWidth = 1.5; ctx.strokeStyle = col; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, 3.5, 0, Math.PI * 2); ctx.fillStyle = col; ctx.fill();
      rr(bx, by, tw, th, 6); ctx.fillStyle = "rgba(15,23,42,.95)"; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = col; ctx.stroke();
      ctx.fillStyle = col; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(txt, x, by + th / 2 + 1);
    });
    if (mode) {
      ctx.fillStyle = "#94a3b8"; ctx.font = "11px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
      ctx.fillText(t("مجس V/A: المس سلكاً لإضافة مجس · اسحبه فوق أي سلك · المسه للتبديل V ← A ← حذف",
                     "V/A probe: tap a wire to add · drag onto any wire · tap a probe: V → A → delete"), cssW / 2, 14);
    }
    ctx.restore();
  }
  var _draw = draw;
  draw = function () { _draw(); drawVA(); };

  // ---------- pointer handling (capture phase, runs before the normal editor) ----------
  var stage = cv.parentNode;
  stage.addEventListener("pointerdown", function (e) {
    if (!mode || e.target !== cv) return;
    var pt = evPos(e), i = hitVP(pt);
    if (i < 0) {
      if (overTool(pt) || hitTerminal(pt) || hitComp(pt)) return;     // let the normal editor handle it
      if (vps.length >= MAXP) return;
      var np = { kind: "V", a: null, b: null, s: 0.5, x: pt.x, y: pt.y };
      attach(np, pt); vps.push(np);
      pd = { i: vps.length - 1, sx: pt.x, sy: pt.y, moved: false, isNew: true };
    } else {
      pd = { i: i, sx: pt.x, sy: pt.y, moved: false, isNew: false };
    }
    try { cv.setPointerCapture(e.pointerId); } catch (x) {}
    e.stopImmediatePropagation(); e.preventDefault(); draw();
  }, true);
  stage.addEventListener("pointermove", function (e) {
    if (!pd) return;
    var pt = evPos(e), p = vps[pd.i];
    if (!p) { pd = null; return; }
    if (!pd.moved && Math.hypot(pt.x - pd.sx, pt.y - pd.sy) < 6) return;
    pd.moved = true; p.x = pt.x; p.y = pt.y; attach(p, pt);
    draw();
  }, true);
  stage.addEventListener("pointerup", function (e) {
    if (!pd) return;
    var pt = evPos(e), p = vps[pd.i], d = pd; pd = null;
    if (p) {
      if (d.moved) { attach(p, pt); if (!p.a) { p.x = pt.x; p.y = pt.y; } }
      else if (!d.isNew) { if (p.kind === "V") p.kind = "A"; else vps.splice(d.i, 1); }   // tap: V -> A -> delete
    }
    scheduleSave(); draw();
    e.stopImmediatePropagation();
  }, true);
  stage.addEventListener("pointercancel", function () { pd = null; }, true);

  // ---------- top-bar button ----------
  var btn = document.createElement("button");
  btn.id = "btnVAProbe";
  btn.textContent = "\u26A1 V/A";
  function paint() { btn.style.background = mode ? "#0284c7" : ""; }
  btn.onclick = function () {
    mode = !mode; paint();
    if (mode) { var lp = document.getElementById("btnLogicProbe"); if (lp && lp.style.background) lp.click(); }   // modes are exclusive
    if (mode && !vps.length) { vps.push({ kind: "V", a: null, b: null, s: 0.5, x: Math.round(cssW / 2) + 40, y: 110 }); scheduleSave(); }
    draw();
  };
  window.pxAddBar(btn);
  var lp0 = document.getElementById("btnLogicProbe");
  if (lp0) lp0.addEventListener("click", function () { if (lp0.style.background && mode) { mode = false; paint(); draw(); } });

  // restore the V/A probes together with the rest of the saved circuit
  var _load = loadState;
  loadState = function (obj, forceLayout) {
    var ok = _load.apply(this, arguments);
    if (ok) {
      vps.length = 0;
      if (!forceLayout && obj && Array.isArray(obj.vaprobes)) {
        obj.vaprobes.slice(0, MAXP).forEach(function (q) {
          if (!q || typeof q.x !== "number" || typeof q.y !== "number") return;
          vps.push({
            kind: q.kind === "A" ? "A" : "V",
            a: typeof q.a === "string" ? q.a : null, b: typeof q.b === "string" ? q.b : null,
            s: (typeof q.s === "number" && isFinite(q.s)) ? Math.max(0, Math.min(1, q.s)) : 0.5,
            x: q.x, y: q.y
          });
        });
      }
      draw();
    }
    return ok;
  };
})();
'''


# =====================================================================================================================
# v3 helpers: soft transforms (never abort the build) + shared UI helpers (toast / value dialog)
# =====================================================================================================================
WARNINGS = []


def _match_brace(text, open_idx):
    """Index of the '}' that closes the '{' at open_idx (skips strings and comments); -1 if not found."""
    depth, i, n = 0, open_idx, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'`":
            q = ch
            i += 1
            while i < n and text[i] != q:
                if text[i] == "\\":
                    i += 1
                i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            if j < 0:
                return -1
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            if j < 0:
                return -1
            i = j + 1
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _hook_branch(text, regex, call, label):
    """Insert `call(var)` as the LAST statement of every `if (X.type === "<name>") { ... }` branch found by regex."""
    matches = list(regex.finditer(text))
    if not matches:
        WARNINGS.append("[%s] drawing branch not found - left unchanged (static drawing stays)" % label)
        return text
    done = 0
    for m in reversed(matches):
        open_idx = m.end() - 1
        close = _match_brace(text, open_idx)
        if close < 0 or close - open_idx > 8000:
            WARNINGS.append("[%s] could not delimit the branch at offset %d - skipped" % (label, m.start()))
            continue
        text = text[:close] + "\n" + call % m.group(1) + "\n" + text[close:]
        done += 1
    if not done:
        return text
    return text


JS_UI_HELPER = r'''
window.pxToast = window.pxToast || function (msg) {
  var el = document.getElementById("pxToast");
  if (!el) {
    el = document.createElement("div"); el.id = "pxToast";
    el.style.cssText = "position:fixed;left:50%;bottom:70px;transform:translateX(-50%);z-index:120;max-width:84%;padding:8px 14px;border-radius:10px;" +
      "background:#0f172a;color:#e2e8f0;border:1px solid #334155;font-size:13px;box-shadow:0 6px 18px rgba(0,0,0,.45);display:none;text-align:center";
    document.body.appendChild(el);
  }
  el.textContent = msg; el.style.display = "block";
  clearTimeout(el.__t); el.__t = setTimeout(function () { el.style.display = "none"; }, 2400);
};
// our own modal (window.prompt is not available in every WebView): onSubmit(text) returns true to close
window.pxAskValue = window.pxAskValue || function (title, hint, initial, onSubmit) {
  var ov = document.getElementById("pxAskOv");
  if (!ov) {
    ov = document.createElement("div"); ov.id = "pxAskOv";
    ov.style.cssText = "display:none;position:fixed;left:0;top:0;right:0;bottom:0;z-index:110;background:rgba(0,0,0,.55);align-items:center;justify-content:center";
    ov.innerHTML =
      '<div style="width:260px;max-width:88%;background:var(--panel,#1e293b);color:var(--text,#e2e8f0);border:1px solid var(--line,#334155);border-radius:14px;padding:14px;box-shadow:0 10px 30px rgba(0,0,0,.5);font-size:13px">' +
      '<div id="pxAskT" style="font-weight:bold;margin-bottom:4px"></div><div id="pxAskH" style="color:#94a3b8;font-size:12px;margin-bottom:8px"></div>' +
      '<input id="pxAskI" type="text" inputmode="decimal" autocomplete="off" style="width:100%;box-sizing:border-box;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:8px;padding:8px;font-size:16px">' +
      '<div style="display:flex;gap:8px;margin-top:10px"><button id="pxAskC" style="flex:1">\u2715</button><button id="pxAskO" class="primary" style="flex:1">OK</button></div></div>';
    document.body.appendChild(ov);
  }
  var inp = ov.querySelector("#pxAskI");
  ov.querySelector("#pxAskT").textContent = title; ov.querySelector("#pxAskH").textContent = hint || "";
  inp.value = initial === undefined || initial === null ? "" : String(initial);
  function close() { ov.style.display = "none"; }
  function ok() { if (onSubmit(inp.value) !== false) close(); }
  ov.querySelector("#pxAskC").onclick = close;
  ov.querySelector("#pxAskO").onclick = ok;
  inp.onkeydown = function (e) { if (e.key === "Enter") { e.preventDefault(); ok(); } else if (e.key === "Escape") close(); };
  ov.style.display = "flex";
  setTimeout(function () { try { inp.focus(); inp.select(); } catch (x) {} }, 30);
};
// terminal keys of a component. Heuristic: wire-endpoint keys that start with the component id followed by a separator
// ("R1:0", "R1_a" ...). Override window.pxPinKeys(c) if your keys look different.
window.pxPinKeys = window.pxPinKeys || function (c) {
  var out = [], seen = {}, id = String(c.id);
  function mine(k) { return typeof k === "string" && k.indexOf(id) === 0 && (k.length === id.length || !/[A-Za-z0-9]/.test(k.charAt(id.length))); }
  wires.forEach(function (w) { [w.a, w.b].forEach(function (k) { if (mine(k) && !seen[k]) { seen[k] = 1; out.push(k); } }); });
  out.sort(function (p, q) { return p.localeCompare(q, undefined, { numeric: true }); });
  return out;
};
'''

# =====================================================================================================================
# Feature 7: Properties editor (tap a part -> small pencil icon, or long-press -> value dialog)
# =====================================================================================================================
MARK_PROPS = "/*PROTEUS_PROPS*/"

PROPS_JS = MARK_PROPS + r'''
(function () {
  if (window.__pxProps) return; window.__pxProps = 1;
''' + JS_UI_HELPER + r'''
  var LP_MS = 550, IR = 11, press = null;

  function compOf(r) {
    if (!r) return null;
    if (typeof r === "object") return r;
    if (typeof r === "string") return findComp(r);
    if (typeof r === "number" && r >= 0) return comps[r] || null;
    return null;
  }
  function editable(c) {
    var T = c && TYPES[c.type];
    return !!(T && Array.isArray(T.vals) && typeof c.val === "number");
  }
  function selComp() { return (sel && sel.kind === "comp") ? findComp(sel.id) : null; }
  function iconPos(c) { return (typeof c.x === "number" && typeof c.y === "number") ? { x: c.x + 30, y: c.y - 30 } : null; }

  // "4700", "4.7k", "2M", "1e-6", "5V", "100 ohm" -> number (NaN if invalid). Plain numbers are in the part's own unit.
  function parseVal(s) {
    var m = /^\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*(meg|[kKMG])?\s*(?:v|a|hz|ohm|\u03A9|f|h)?\s*$/i.exec(String(s).replace(",", "."));
    if (!m) return NaN;
    var n = parseFloat(m[1]), suf = m[2] || "", mult = 1;
    if (suf) {
      if (suf === "m") return NaN;                         // milli vs mega is ambiguous: write 1e-3 or use M / meg
      var low = suf.toLowerCase();
      mult = low === "k" ? 1e3 : low === "meg" ? 1e6 : low === "g" ? 1e9 : (suf === "M" ? 1e6 : 1);
    }
    return n * mult;
  }
  function openEditor(c) {
    if (!c || !editable(c)) return;
    var T = TYPES[c.type], nm = (AR ? T.ar : T.en) || c.type;
    window.pxAskValue(c.id + " \u2014 " + nm, t("القيمة الجديدة (نفس وحدة العنصر، يقبل k و M)", "New value (part's own unit; k and M accepted)"), c.val, function (txt) {
      var v = parseVal(txt);
      if (!isFinite(v) || v <= 0) { window.pxToast(t("قيمة غير صالحة", "Invalid value")); return false; }
      snap();
      c.val = v;
      if (c.type === "signal_gen") c.amp = Math.min(50, v);
      recompute(); scheduleSave(); draw();
      return true;
    });
  }
  window.pxEditProps = openEditor;

  var stage = cv.parentNode;
  stage.addEventListener("pointerdown", function (e) {
    if (e.target !== cv) return;
    var pt = evPos(e), sc = selComp();
    if (sc && editable(sc)) {                              // tap on the pencil icon
      var ip = iconPos(sc);
      if (ip && Math.hypot(ip.x - pt.x, ip.y - pt.y) < IR + 8) { e.stopImmediatePropagation(); e.preventDefault(); openEditor(sc); return; }
    }
    var c = null; try { c = compOf(hitComp(pt)); } catch (x) {}
    if (press) { clearTimeout(press.tm); press = null; }
    if (c && editable(c)) {                                // long press on a part (does not block the normal editor)
      press = { id: c.id, x: pt.x, y: pt.y, tm: setTimeout(function () {
        var p = press; press = null;
        if (p) { var cc = findComp(p.id); if (cc) openEditor(cc); }
      }, LP_MS) };
    }
  }, true);
  stage.addEventListener("pointermove", function (e) {
    if (!press) return;
    var pt = evPos(e);
    if (Math.hypot(pt.x - press.x, pt.y - press.y) > 6) { clearTimeout(press.tm); press = null; }
  }, true);
  function cancel() { if (press) { clearTimeout(press.tm); press = null; } }
  stage.addEventListener("pointerup", cancel, true);
  stage.addEventListener("pointercancel", cancel, true);

  var _draw = draw;
  draw = function () {
    _draw();
    var c = selComp(), ip = (c && editable(c)) ? iconPos(c) : null;
    if (!ip) return;
    ctx.save();
    ctx.beginPath(); ctx.arc(ip.x, ip.y, IR, 0, Math.PI * 2); ctx.fillStyle = "#0284c7"; ctx.fill();
    ctx.lineWidth = 1.5; ctx.strokeStyle = "#e0f2fe"; ctx.stroke();
    ctx.fillStyle = "#fff"; ctx.font = "bold 13px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("\u270E", ip.x, ip.y + 1);
    ctx.restore();
  };
})();
'''

# =====================================================================================================================
# Feature 8: interactive 7-segment + LCD (overlay drawn at the END of the existing seven_seg / lcd drawing branch)
# =====================================================================================================================
MARK_DISPLAYS = "/*PROTEUS_DISPLAYS*/"

SEG_RE = re.compile(r'(?:else\s+)?if\s*\(\s*([A-Za-z_$][\w$]*)\.type\s*===?\s*["\']seven_seg["\']\s*\)\s*\{')
LCD_RE = re.compile(r'(?:else\s+)?if\s*\(\s*([A-Za-z_$][\w$]*)\.type\s*===?\s*["\'][Ll][Cc][Dd][\w]*["\']\s*\)\s*\{')


def displays_edit(text):
    text = _hook_branch(text, SEG_RE, "window.pxSegOverlay && window.pxSegOverlay(%s); " + MARK_DISPLAYS, "7-segment")
    text = _hook_branch(text, LCD_RE, "window.pxLcdOverlay && window.pxLcdOverlay(%s); " + MARK_DISPLAYS, "LCD")
    return text


DISPLAYS_EDITS = [displays_edit]

DISPLAYS_JS = MARK_DISPLAYS + r'''
(function () {
  if (window.__pxDisp) return; window.__pxDisp = 1;
''' + JS_UI_HELPER + r'''
  var TH = 2.5, SW = 24, SH = 42;                          // SW / SH: size of the lit digit area (tune to your symbol)
  var MASK = { 0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg" };

  function V(k) { try { var v = sim.nodeV(k); return (typeof v === "number" && isFinite(v)) ? v : 0; } catch (e) { return 0; } }
  function pinMap(c) {
    var ks = window.pxPinKeys(c), by = {}, n = String(c.id).length + 1;
    ks.forEach(function (k) { by[k.slice(n).toLowerCase()] = k; });
    return { keys: ks, by: by };
  }
  // voltage that drives the digit: V(a) - V(b)  (falls back to V(c) / the 2nd wired pin / ground)
  window.pxSegVoltage = window.pxSegVoltage || function (c) {
    var pm = pinMap(c), ka = pm.by.a || pm.keys[0], kb = pm.by.b || pm.by.c || pm.keys[1];
    if (!ka) return null;
    if (kb === ka) kb = null;
    return Math.abs(V(ka) - (kb ? V(kb) : 0));
  };
  // highest pin voltage of an LCD (any powered pin wakes it up)
  window.pxLcdVoltage = window.pxLcdVoltage || function (c) {
    var ks = window.pxPinKeys(c), m = null;
    ks.forEach(function (k) { var v = Math.abs(V(k)); if (m === null || v > m) m = v; });
    return m;
  };
  function real(c) { return c && c.id !== undefined && !!findComp(c.id); }   // skip palette thumbnails etc.
  function live() { return !!(sim && sim.ok); }

  window.pxSegOverlay = function (c) {
    try {
      if (!real(c)) return;
      var v = live() ? window.pxSegVoltage(c) : null;
      var on = (v !== null && v > TH) ? MASK[Math.max(0, Math.min(9, Math.round(v)))] : "";
      ctx.save();
      ctx.fillStyle = "#0b1220"; ctx.fillRect(-SW / 2 - 7, -SH / 2 - 7, SW + 14, SH + 14);
      ctx.lineCap = "round"; ctx.lineWidth = 4;
      var x0 = -SW / 2 + 3, x1 = SW / 2 - 3, y0 = -SH / 2 + 2, ym = 0, y2 = SH / 2 - 2, xl = -SW / 2, xr = SW / 2;
      var S = {
        a: [x0, y0, x1, y0], b: [xr, y0 + 3, xr, ym - 2], c: [xr, ym + 2, xr, y2 - 3],
        d: [x0, y2, x1, y2], e: [xl, ym + 2, xl, y2 - 3], f: [xl, y0 + 3, xl, ym - 2], g: [x0, ym, x1, ym]
      };
      Object.keys(S).forEach(function (k) {
        var s = S[k], lit = on.indexOf(k) >= 0;
        ctx.strokeStyle = lit ? "#f87171" : "rgba(248,113,113,.13)";
        if (lit) { ctx.shadowColor = "#ef4444"; ctx.shadowBlur = 6; } else ctx.shadowBlur = 0;
        ctx.beginPath(); ctx.moveTo(s[0], s[1]); ctx.lineTo(s[2], s[3]); ctx.stroke();
      });
      ctx.restore();
    } catch (e) {}
  };

  window.pxLcdOverlay = function (c) {
    try {
      if (!real(c)) return;
      var v = live() ? window.pxLcdVoltage(c) : null, on = (v !== null && v > TH), W = 62, H = 30;
      ctx.save();
      ctx.fillStyle = on ? "#166534" : "#052e16"; ctx.fillRect(-W / 2, -H / 2, W, H);
      ctx.strokeStyle = "#0f172a"; ctx.lineWidth = 2; ctx.strokeRect(-W / 2, -H / 2, W, H);
      if (on) {
        ctx.fillStyle = "#dcfce7"; ctx.font = "bold 9px monospace"; ctx.textAlign = "left"; ctx.textBaseline = "middle";
        ctx.fillText("READY", -W / 2 + 5, -H / 2 + 9);
        ctx.fillText(v.toFixed(v >= 10 ? 1 : 2) + " V", -W / 2 + 5, -H / 2 + 21);
      }
      ctx.restore();
    } catch (e) {}
  };
})();
'''

# =====================================================================================================================
# Feature 9: Netlist export (top-bar button, uses the app's own saveFile)
# =====================================================================================================================
MARK_NETLIST = "/*PROTEUS_NETLIST*/"

NETLIST_JS = MARK_NETLIST + r'''
(function () {
  if (window.__pxNet) return; window.__pxNet = 1;
''' + JS_BAR_HELPER + JS_UI_HELPER + r'''
  // nets = connected groups of terminals (union-find over wires); the net of a ground part is "0"
  window.pxBuildNetlist = function () {
    var parent = {};
    function find(k) { if (parent[k] === undefined) parent[k] = k; while (parent[k] !== k) { parent[k] = parent[parent[k]]; k = parent[k]; } return k; }
    function union(a, b) { a = find(a); b = find(b); if (a !== b) parent[a] = b; }
    wires.forEach(function (w) { union(w.a, w.b); });
    var gnd = {}, isG = function (c) { return /^(gnd|ground)/i.test(String(c.type)); };
    comps.forEach(function (c) { if (isG(c)) window.pxPinKeys(c).forEach(function (k) { gnd[find(k)] = 1; }); });
    var num = {}, next = 1;
    function net(k) { var r = find(k); if (gnd[r]) return "0"; if (!num[r]) num[r] = next++; return String(num[r]); }
    var out = ["* Netlist exported from circuit_sim  " + new Date().toISOString().slice(0, 19).replace("T", " "),
               "* " + comps.length + " parts, " + wires.length + " wires"];
    if (!Object.keys(gnd).length) out.push("* (no ground part found: no net is numbered 0)");
    comps.forEach(function (c) {
      if (isG(c)) return;
      var ks = window.pxPinKeys(c);
      if (!ks.length) { out.push("* " + c.id + " (" + c.type + ") has no wired terminal"); return; }
      var nets = ks.map(net), line = c.id + " " + nets.join(" ");
      if (typeof c.val === "number" && isFinite(c.val)) line += " " + c.val;
      var extra = [];
      if (nets.length !== 2) extra.push(c.type);
      if (c.type === "signal_gen") extra.push((c.wave || "sine") + " " + (c.freq || 50) + "Hz " + (c.amp || c.val) + "V");
      if (c.type === "ac_source") extra.push("ac 50Hz");
      out.push(line + (extra.length ? " ; " + extra.join(", ") : ""));
    });
    out.push(".end");
    return out.join("\n") + "\n";
  };

  // call the app's saveFile whatever its parameter order is: look at the parameter NAMES, default (name, text, mime)
  function callSave(name, text) {
    if (typeof saveFile !== "function") return false;
    var args = [name, text, "text/plain"];
    try {
      var m = /^[^(]*\(([^)]*)\)/.exec(Function.prototype.toString.call(saveFile));
      var ps = m ? m[1].split(",").map(function (s) { return s.replace(/=.*$/, "").trim(); }).filter(Boolean) : [];
      var iN = -1, iT = -1, iM = -1;
      ps.forEach(function (p, i) {
        if (iN < 0 && /name|file|fn|path|title/i.test(p)) iN = i;
        else if (iM < 0 && /mime|type/i.test(p)) iM = i;
        else if (iT < 0 && /text|content|data|str|body|txt/i.test(p)) iT = i;
      });
      if (iN >= 0 && iT >= 0) {
        args = []; ps.forEach(function () { args.push(undefined); });
        args[iN] = name; args[iT] = text; if (iM >= 0) args[iM] = "text/plain";
      }
    } catch (e) {}
    saveFile.apply(window, args);
    return true;
  }

  function exportNetlist() {
    var text = window.pxBuildNetlist(), name = "netlist.txt";
    try {
      if (callSave(name, text)) { window.pxToast(t("تم تصدير الـ Netlist", "Netlist exported") + " (" + name + ")"); return; }
    } catch (e) {}
    // fallback: show the text so it can be copied by hand
    window.pxAskValue("Netlist", t("saveFile غير متاح — انسخ النص", "saveFile unavailable - copy the text"), text.replace(/\n/g, " | "), function () { return true; });
  }
  window.pxExportNetlist = exportNetlist;

  var btn = document.createElement("button");
  btn.id = "btnNetlist";
  btn.textContent = "\u{1F4C4} Netlist";
  btn.onclick = exportNetlist;
  window.pxAddBar(btn);
})();
'''

# =====================================================================================================================
# Feature 10: Oscilloscope cursors T1 / T2 (draggable vertical lines + dT, V1, V2 readout), saved with the circuit
# =====================================================================================================================
MARK_CURSORS = "/*PROTEUS_CURSORS*/"

CURSORS_EDITS = [
    # scheduleSave payload: append "pxcur" right after the V/A probes written by Feature 6
    ("a: p.a || null, b: p.b || null, s: p.s, x: p.x, y: p.y }; }) }",
     "a: p.a || null, b: p.b || null, s: p.s, x: p.x, y: p.y }; }), " + MARK_CURSORS
     + " pxcur: (window.pxCursorState ? window.pxCursorState() : null) }"),
]

CURSORS_JS = MARK_CURSORS + r'''
(function () {
  if (window.__pxCur) return; window.__pxCur = 1;
  var cur = { a: 0.25, b: 0.75 }, drag = null, GRAB = 14, dt = null, lastPush = null;
  window.pxCursorState = function () { return { a: cur.a, b: cur.b }; };
  function clamp(f) { return Math.max(0.02, Math.min(0.98, f)); }

  // sample period: window.PX_SCOPE_DT or scope.dt if you have it, otherwise estimated from the push rate of channel A
  function nowSim() {
    if (typeof timeSec === "number" && isFinite(timeSec)) return timeSec;
    return (performance.now() / 1000) / ((typeof TIME_SCALE === "number" && TIME_SCALE > 0) ? TIME_SCALE : 1);
  }
  function hook(p) {
    var d = p && p.data;
    if (!d || d.__pxw || typeof d.push !== "function") return;
    d.__pxw = 1;
    var orig = d.push;
    d.push = function () {
      var n = nowSim();
      if (lastPush !== null) { var g = n - lastPush; if (g > 0 && g < 1) dt = dt === null ? g : dt * 0.9 + g * 0.1; }
      lastPush = n;
      return orig.apply(d, arguments);
    };
  }
  function samplePeriod() {
    if (typeof window.PX_SCOPE_DT === "number" && window.PX_SCOPE_DT > 0) return { v: window.PX_SCOPE_DT, exact: true };
    if (typeof scope.dt === "number" && scope.dt > 0) return { v: scope.dt, exact: true };
    return dt ? { v: dt, exact: false } : null;
  }
  function fmtT(s) {
    var a = Math.abs(s);
    if (a >= 1) return s.toFixed(3) + "s";
    if (a >= 1e-3) return (s * 1e3).toFixed(2) + "ms";
    if (a >= 1e-6) return (s * 1e6).toFixed(2) + "\u00B5s";
    return (s * 1e9).toFixed(1) + "ns";
  }
  function fmtF(f) { return f >= 1e6 ? (f / 1e6).toFixed(2) + "MHz" : f >= 1e3 ? (f / 1e3).toFixed(2) + "kHz" : f.toFixed(1) + "Hz"; }
  function at(p, f) {
    var d = p && p.data;
    if (!d || d.length < 2) return null;
    var j = Math.round(f * (scope.maxData || d.length));
    return (j >= 0 && j < d.length && typeof d[j] === "number" && isFinite(d[j])) ? d[j] : null;
  }
  function fmtV(v) { return v === null ? "--" : (v >= 0 ? "" : "-") + Math.abs(v).toFixed(2) + "V"; }

  function drawCursors() {
    if (!scope || !scope.visible || !(scope.w > 0)) return;
    hook(scope.probeA);
    ctx.save();
    ctx.lineWidth = 1.5; ctx.setLineDash([5, 4]);
    [["T1", "#fde047", cur.a], ["T2", "#e879f9", cur.b]].forEach(function (c) {
      var x = scope.x + c[2] * scope.w;
      ctx.strokeStyle = c[1]; ctx.beginPath(); ctx.moveTo(x, scope.y); ctx.lineTo(x, scope.y + scope.h); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = c[1]; ctx.beginPath(); ctx.moveTo(x - 6, scope.y); ctx.lineTo(x + 6, scope.y); ctx.lineTo(x, scope.y + 8); ctx.closePath(); ctx.fill();
      ctx.font = "bold 10px monospace"; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
      ctx.fillText(c[0], x, scope.y + 20);
      ctx.setLineDash([5, 4]);
    });
    ctx.setLineDash([]);

    var lines = [], di = Math.abs(cur.b - cur.a) * (scope.maxData || 0), sp = samplePeriod();
    if (sp) {
      var T = di * sp.v;
      lines.push({ t: "\u0394T" + (sp.exact ? "=" : "\u2248") + fmtT(T) + (T > 0 ? "  f" + (sp.exact ? "=" : "\u2248") + fmtF(1 / T) : ""), c: "#e2e8f0" });
    } else {
      lines.push({ t: "\u0394T=" + Math.round(di) + " smp", c: "#e2e8f0" });
    }
    [["A", scope.probeA], ["B", scope.probeB]].forEach(function (ch) {
      var v1 = at(ch[1], cur.a), v2 = at(ch[1], cur.b);
      if (v1 === null && v2 === null) return;
      lines.push({ t: ch[0] + " V1=" + fmtV(v1) + " V2=" + fmtV(v2), c: (ch[1] && ch[1].col) || "#e2e8f0" });
    });
    ctx.font = "10px monospace"; ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    var w = 0; lines.forEach(function (l) { w = Math.max(w, ctx.measureText(l.t).width); });
    var bx = scope.x + 4, by = scope.y + scope.h - 6 - lines.length * 13;
    ctx.fillStyle = "rgba(2,6,23,.80)"; ctx.fillRect(bx - 2, by - 10, w + 8, lines.length * 13 + 4);
    lines.forEach(function (l, i) { ctx.fillStyle = l.c; ctx.fillText(l.t, bx + 2, by + i * 13 + 1); });
    ctx.restore();
  }
  var _draw = draw;
  draw = function () { _draw(); drawCursors(); };

  // dragging (capture phase: runs before the scope's own move / resize handlers)
  var stage = cv.parentNode;
  function nearProbe(pt) {
    var hit = false;
    [scope.probeA, scope.probeB].forEach(function (pr) { try { var q = probePos(pr); if (Math.hypot(q.x - pt.x, q.y - pt.y) < 20) hit = true; } catch (e) {} });
    return hit;
  }
  stage.addEventListener("pointerdown", function (e) {
    if (e.target !== cv || !scope.visible || !(scope.w > 0)) return;
    var pt = evPos(e);
    if (pt.y < scope.y || pt.y > scope.y + scope.h || nearProbe(pt)) return;
    var da = Math.abs(pt.x - (scope.x + cur.a * scope.w)), db = Math.abs(pt.x - (scope.x + cur.b * scope.w));
    if (Math.min(da, db) > GRAB) return;
    drag = da <= db ? "a" : "b";
    try { cv.setPointerCapture(e.pointerId); } catch (x) {}
    e.stopImmediatePropagation(); e.preventDefault();
  }, true);
  stage.addEventListener("pointermove", function (e) {
    if (!drag) return;
    cur[drag] = clamp((evPos(e).x - scope.x) / scope.w);
    draw(); e.stopImmediatePropagation();
  }, true);
  function stop(e) { if (!drag) return; drag = null; scheduleSave(); draw(); if (e && e.stopImmediatePropagation) e.stopImmediatePropagation(); }
  stage.addEventListener("pointerup", stop, true);
  stage.addEventListener("pointercancel", stop, true);

  // restore with the rest of the saved circuit
  var _load = loadState;
  loadState = function (obj, forceLayout) {
    var ok = _load.apply(this, arguments);
    if (ok && !forceLayout && obj && obj.pxcur && typeof obj.pxcur.a === "number" && typeof obj.pxcur.b === "number") {
      cur.a = clamp(obj.pxcur.a); cur.b = clamp(obj.pxcur.b);
    }
    if (ok) draw();
    return ok;
  };
})();
'''


# =====================================================================================================================
# =====================================================================================================================
#  v4  -  five new features (everything above is v3 and is kept byte-for-byte)
#    11) Component labels   (rename icon next to the properties pencil; c.id + every wire key / probe key follows)
#    12) Simulation speed   (top-bar 0.1x / 1x / 10x buttons -> TIME_SCALE, scope traces cleared, recompute())
#    13) Mirroring          (bottom-toolbar "Flip" button -> c.flipX, drawComp mirrored with ctx.scale(-1, 1))
#    14) Net highlighting   (select a wire -> every wire of the same net glows cyan, its terminals are circled)
#    15) Fault injection    (top-bar "Fault" button -> w.cut = true: wire is ignored by the solver, drawn red dashed + X)
#  Anchors that live in code this script has never seen (drawComp, nodeMap, simulate, TIME_SCALE, the bottom toolbar,
#  the wire selection object) are handled as SOFT transforms / run-time hooks: they never abort the build and never
#  corrupt the file; anything that could not be hooked is reported in WARNINGS and in the browser console.
# =====================================================================================================================
# =====================================================================================================================
MARK_V4CORE = "/*PROTEUS_V4CORE*/"
MARK_V4STATE = "/*PROTEUS_V4STATE*/"
MARK_RENAME = "/*PROTEUS_RENAME*/"
MARK_SPEED = "/*PROTEUS_SPEED*/"
MARK_FLIP = "/*PROTEUS_FLIP*/"
MARK_NETHL = "/*PROTEUS_NETHL*/"
MARK_FAULT = "/*PROTEUS_FAULT*/"

# ---------------------------------------------------------------------------------------------------------------------
# v4 core: shared helpers + persistence of the v4 flags (flipX, cut wires, speed) inside the saved circuit state
# ---------------------------------------------------------------------------------------------------------------------
V4_STATE_OLD = "pxcur: (window.pxCursorState ? window.pxCursorState() : null) }"
V4_STATE_NEW = ("pxcur: (window.pxCursorState ? window.pxCursorState() : null), " + MARK_V4STATE
                + " pxv4: (window.pxV4State ? window.pxV4State() : null) }")


def v4_state_edit(text):
    """Soft: add `pxv4` to the saved state, right after the `pxcur` field written by the v3 cursors feature."""
    if MARK_V4STATE in text:
        return text
    n = text.count(V4_STATE_OLD)
    if n != 1:
        WARNINGS.append("[v4 core] state anchor 'pxcur' found %d times - flip / cut wires / speed will NOT be saved with the circuit" % n)
        return text
    return text.replace(V4_STATE_OLD, V4_STATE_NEW, 1)


V4CORE_EDITS = [v4_state_edit]

V4CORE_JS = MARK_V4CORE + r'''
(function () {
  if (window.__pxV4Core) return; window.__pxV4Core = 1;
  var reg = window.pxV4Reg = window.pxV4Reg || { save: {}, load: {} };

  // what the v4 features want to keep inside the saved circuit (flipX list, cut wires, speed)
  window.pxV4State = function () {
    var o = {};
    Object.keys(reg.save).forEach(function (k) { try { var v = reg.save[k](); if (v !== undefined) o[k] = v; } catch (e) {} });
    return o;
  };

  function byEnds(a, b) {
    for (var i = 0; i < wires.length; i++) {
      var w = wires[i];
      if ((w.a === a && w.b === b) || (w.a === b && w.b === a)) return w;
    }
    return null;
  }
  window.pxWireByEnds = byEnds;

  // the wire object behind sel.kind === "wire" (the selection object's shape is not known, so try the usual ones)
  window.pxSelWire = function () {
    try {
      if (!sel || sel.kind !== "wire") return null;
      var i, k, v, objs = [sel.wire, sel.w, sel.obj, sel.ref, sel.item];
      for (i = 0; i < objs.length; i++) {
        v = objs[i];
        if (v && typeof v === "object" && typeof v.a === "string") {
          if (wires.indexOf(v) >= 0) return v;
          var m = byEnds(v.a, v.b); if (m) return m;
        }
      }
      var ik = ["index", "idx", "i", "wi", "n"];
      for (k = 0; k < ik.length; k++) { v = sel[ik[k]]; if (typeof v === "number" && wires[v]) return wires[v]; }
      if (sel.id !== undefined && sel.id !== null) {
        for (i = 0; i < wires.length; i++) if (wires[i].id !== undefined && wires[i].id === sel.id) return wires[i];
        if (typeof sel.id === "number" && wires[sel.id]) return wires[sel.id];
      }
      if (typeof sel.a === "string" && typeof sel.b === "string") return byEnds(sel.a, sel.b);
    } catch (e) {}
    return null;
  };

  // drawn route of a wire (orthogonal when Feature 5 is present)
  window.pxWirePts = function (w) {
    try {
      if (typeof pxWirePath === "function") { var P = pxWirePath(w); if (P) return P; }
      var a = keyPos(w.a), b = keyPos(w.b);
      return (a && b) ? [a, b] : null;
    } catch (e) { return null; }
  };

  window.pxPathMid = function (P) {
    var L = 0, i, seg;
    for (i = 1; i < P.length; i++) L += Math.hypot(P[i].x - P[i - 1].x, P[i].y - P[i - 1].y);
    var d = L / 2;
    for (i = 1; i < P.length; i++) {
      seg = Math.hypot(P[i].x - P[i - 1].x, P[i].y - P[i - 1].y);
      if (d <= seg || i === P.length - 1) {
        var f = seg ? Math.min(1, d / seg) : 0;
        return { x: P[i - 1].x + (P[i].x - P[i - 1].x) * f, y: P[i - 1].y + (P[i].y - P[i - 1].y) * f };
      }
      d -= seg;
    }
    return { x: P[0].x, y: P[0].y };
  };

  // the electrical net of a wire = every wire reachable through shared terminal keys; cut wires never connect anything
  window.pxNetOf = function (w0) {
    var parent = {};
    function find(k) { if (parent[k] === undefined) parent[k] = k; while (parent[k] !== k) { parent[k] = parent[parent[k]]; k = parent[k]; } return k; }
    wires.forEach(function (w) { if (!w.cut) { var ra = find(w.a), rb = find(w.b); if (ra !== rb) parent[ra] = rb; } });
    var root = find(w0.a), out = { wires: [], keys: {} };
    wires.forEach(function (w) {
      if (!w.cut && find(w.a) === root) { out.wires.push(w); out.keys[w.a] = 1; out.keys[w.b] = 1; }
    });
    return out;
  };

  // restore the v4 flags together with the rest of the saved circuit
  var _load = loadState;
  loadState = function (obj, forceLayout) {
    var ok = _load.apply(this, arguments);
    if (ok) {
      var st = (!forceLayout && obj && obj.pxv4 && typeof obj.pxv4 === "object") ? obj.pxv4 : {};
      Object.keys(reg.load).forEach(function (k) { try { reg.load[k](st[k]); } catch (e) {} });
      draw();
    }
    return ok;
  };
})();
'''

# ---------------------------------------------------------------------------------------------------------------------
# Feature 11: Custom component labels (rename)
# ---------------------------------------------------------------------------------------------------------------------
RENAME_JS = MARK_RENAME + r'''
(function () {
  if (window.__pxRename) return; window.__pxRename = 1;
''' + JS_UI_HELPER + r'''
  var PW = 36, PH = 22;

  // the shared value dialog opens a numeric keyboard; a name needs the text keyboard
  if (!window.__pxAskWrapped) {
    window.__pxAskWrapped = 1;
    var _ask = window.pxAskValue;
    window.pxAskValue = function () {
      var r = _ask.apply(this, arguments);
      var i = document.getElementById("pxAskI");
      if (i) { try { i.inputMode = window.__pxAskText ? "text" : "decimal"; } catch (e) {} }
      window.__pxAskText = false;
      return r;
    };
  }

  function selComp() { return (sel && sel.kind === "comp") ? findComp(sel.id) : null; }
  // terminal key of a part = its id followed by a non-alphanumeric separator ("R1.a", "R1:0", "R1_a" ...)
  function sepOk(k, id) {
    return typeof k === "string" && k.indexOf(id) === 0 && (k.length === id.length || !/[A-Za-z0-9]/.test(k.charAt(id.length)));
  }
  // owner of a key = the LONGEST part id that matches (so "R_LED.a" is never taken for part "R")
  function owner(k) {
    var best = null;
    comps.forEach(function (o) { var id = String(o.id); if (sepOk(k, id) && (best === null || id.length > best.length)) best = id; });
    return best;
  }
  function remap(k, oldId, newId) { return (typeof k === "string" && owner(k) === oldId) ? newId + k.slice(oldId.length) : k; }
  function fixObj(o, oldId, newId) {
    if (!o || typeof o !== "object") return;
    Object.keys(o).forEach(function (p) { if (typeof o[p] === "string") o[p] = remap(o[p], oldId, newId); });
  }

  function doRename(c, newId) {
    var oldId = String(c.id);
    if (newId === oldId) return true;
    var bad = null;
    comps.forEach(function (o) {
      if (o === c) return;
      var id = String(o.id);
      if (id === newId) bad = "dup";
      else if (!bad && (sepOk(newId, id) || sepOk(id, newId))) bad = "amb";
    });
    if (bad === "dup") { window.pxToast(t("الاسم مستخدم مسبقاً", "Name already in use")); return false; }
    if (bad === "amb") { window.pxToast(t("الاسم يتعارض مع مكوّن آخر (بادئة مشتركة)", "Name clashes with another part (shared prefix)")); return false; }
    snap();
    // 1) every reference to the old terminal keys (computed while the old id is still in place)
    wires.forEach(function (w) { w.a = remap(w.a, oldId, newId); w.b = remap(w.b, oldId, newId); });
    (window.proteusProbes || []).forEach(function (p) { p.key = remap(p.key, oldId, newId); });
    (window.proteusVAProbes || []).forEach(function (p) { p.a = remap(p.a, oldId, newId); p.b = remap(p.b, oldId, newId); });
    [scope, meter].forEach(function (T) { if (T) [T.probeA, T.probeB].forEach(function (pr) { fixObj(pr, oldId, newId); }); });
    try { if (typeof pending !== "undefined" && pending) fixObj(pending, oldId, newId); } catch (e) {}
    // 2) the part itself + the selection
    c.id = newId;
    if (sel && sel.kind === "comp" && String(sel.id) === oldId) sel.id = newId;
    recompute(); scheduleSave(); draw();
    window.pxToast(oldId + " \u2192 " + newId);
    return true;
  }

  function openRename(c) {
    if (!c) return;
    window.__pxAskText = true;
    window.pxAskValue(t("تغيير الاسم", "Rename") + " \u2014 " + c.id,
      t("اسم جديد (حروف إنجليزية / أرقام / _) مثال: R_LED", "New name (letters, digits, _) e.g. R_LED"), c.id, function (txt) {
        var n = String(txt).trim();
        if (!/^[A-Za-z][A-Za-z0-9_]{0,15}$/.test(n)) {
          window.pxToast(t("اسم غير صالح: ابدأ بحرف، حتى 16 خانة", "Invalid name: start with a letter, up to 16 chars"));
          return false;
        }
        return doRename(c, n);
      });
  }
  window.pxRenameComp = openRename;

  // the button sits to the right of the properties pencil (pencil = x + 30, rename pill = x + 68)
  function pillPos(c) { return (typeof c.x === "number" && typeof c.y === "number") ? { x: c.x + 68, y: c.y - 30 } : null; }

  // window + capture phase: runs before the editor's own handlers (and before the long-press timer of Feature 7)
  window.addEventListener("pointerdown", function (e) {
    if (e.target !== cv) return;
    var c = selComp(); if (!c) return;
    var ip = pillPos(c); if (!ip) return;
    var pt = evPos(e);
    if (Math.abs(pt.x - ip.x) <= PW / 2 + 3 && Math.abs(pt.y - ip.y) <= PH / 2 + 3) {
      e.stopImmediatePropagation(); e.preventDefault(); openRename(c);
    }
  }, true);

  var _draw = draw;
  draw = function () {
    _draw();
    var c = selComp(), ip = c ? pillPos(c) : null;
    if (!ip) return;
    var x = ip.x - PW / 2, y = ip.y - PH / 2, r = 7;
    ctx.save();
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.lineTo(x + PW - r, y); ctx.arcTo(x + PW, y, x + PW, y + r, r);
    ctx.lineTo(x + PW, y + PH - r); ctx.arcTo(x + PW, y + PH, x + PW - r, y + PH, r); ctx.lineTo(x + r, y + PH);
    ctx.arcTo(x, y + PH, x, y + PH - r, r); ctx.lineTo(x, y + r); ctx.arcTo(x, y, x + r, y, r); ctx.closePath();
    ctx.fillStyle = "#7c3aed"; ctx.fill(); ctx.lineWidth = 1.5; ctx.strokeStyle = "#ede9fe"; ctx.stroke();
    ctx.fillStyle = "#fff"; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("Aa", ip.x, ip.y + 1);
    ctx.fillStyle = "#94a3b8"; ctx.font = "9px sans-serif"; ctx.textBaseline = "alphabetic";
    ctx.fillText(t("تغيير الاسم", "Rename"), ip.x, y + PH + 10);
    ctx.restore();
  };
})();
'''

# ---------------------------------------------------------------------------------------------------------------------
# Feature 12: Simulation speed (0.1x / 1x / 10x)   TIME_SCALE = BASE * multiplier   (BASE = the value found in the file)
# ---------------------------------------------------------------------------------------------------------------------


def speed_edit(text):
    """Soft: TIME_SCALE must be re-assignable at run time, so a `const` / `let` declaration becomes `var`."""
    if "TIME_SCALE" not in text:
        WARNINGS.append("[Simulation speed] TIME_SCALE not found in the page - the speed buttons will report an error at run time")
        return text
    for kw in ("const", "let"):
        old = kw + " TIME_SCALE"
        if text.count(old) == 1:
            text = text.replace(old, "var TIME_SCALE", 1)
    if not re.search(r"\b(?:var|let|const)\s+TIME_SCALE\b", text):
        WARNINGS.append("[Simulation speed] no `TIME_SCALE` declaration found (e.g. declared inside a list) - make sure it is a plain `var`/`let`")
    return text


SPEED_EDITS = [speed_edit]

SPEED_JS = MARK_SPEED + r'''
(function () {
  if (window.__pxSpeed) return; window.__pxSpeed = 1;
  var reg = window.pxV4Reg = window.pxV4Reg || { save: {}, load: {} };
''' + JS_BAR_HELPER + JS_UI_HELPER + r'''
  var BASE = (typeof TIME_SCALE === "number" && TIME_SCALE > 0) ? TIME_SCALE : 0.05;
  var MULTS = [0.1, 1, 10], cur = 1, btns = {};

  function paint() {
    MULTS.forEach(function (m) { if (btns[m]) btns[m].style.background = (m === cur) ? "#0284c7" : ""; });
  }
  // changes TIME_SCALE, clears the scope traces (old samples were taken at another time base), re-solves and redraws
  function setSpeed(m, quiet) {
    m = Number(m);
    if (MULTS.indexOf(m) < 0) return false;
    try { TIME_SCALE = Number((BASE * m).toPrecision(6)); }
    catch (e) { if (!quiet) window.pxToast(t("تعذر تغيير TIME_SCALE (معرّف ثابت)", "Cannot change TIME_SCALE (constant binding)")); return false; }
    cur = m; paint();
    if (quiet) return true;
    try {
      [scope && scope.probeA, scope && scope.probeB].forEach(function (p) { if (p && Array.isArray(p.data)) p.data.length = 0; });
    } catch (e) {}
    recompute(); draw(); scheduleSave();
    window.pxToast(t("سرعة المحاكاة ", "Simulation speed ") + m + "x  (slow-mo x" + TIME_SCALE + ")");
    return true;
  }
  window.pxSetSpeed = setSpeed;

  MULTS.forEach(function (m) {
    var b = document.createElement("button");
    b.id = "btnSpeed" + String(m).replace(".", "_");
    b.textContent = m + "x";
    b.title = t("سرعة المحاكاة", "Simulation speed");
    b.style.cssText = "padding:4px 7px;font-size:12px;min-width:34px";
    b.onclick = function () { setSpeed(m); };
    btns[m] = b;
    window.pxAddBar(b);
  });
  paint();

  reg.save.speed = function () { return cur; };
  reg.load.speed = function (v) { if (typeof v === "number" && MULTS.indexOf(v) >= 0) setSpeed(v, true); };
})();
'''

# ---------------------------------------------------------------------------------------------------------------------
# Feature 13: Mirroring (Flip)
# ---------------------------------------------------------------------------------------------------------------------
FLIP_JS = MARK_FLIP + r'''
(function () {
  if (window.__pxFlip) return; window.__pxFlip = 1;
  var reg = window.pxV4Reg = window.pxV4Reg || { save: {}, load: {} };
''' + JS_UI_HELPER + r'''
  function selComp() { return (sel && sel.kind === "comp") ? findComp(sel.id) : null; }

  // drawComp: mirror the canvas around the part's centre (ctx.scale(-1, 1)) when c.flipX is on, then restore it.
  // Text drawn by the symbol is counter-mirrored so labels stay readable.
  if (typeof drawComp === "function") {
    var _dc = drawComp;
    drawComp = function (c) {
      if (!c || !c.flipX || typeof c.x !== "number") return _dc.apply(this, arguments);
      var ownF = Object.prototype.hasOwnProperty.call(ctx, "fillText"), ownS = Object.prototype.hasOwnProperty.call(ctx, "strokeText");
      var prevF = ctx.fillText, prevS = ctx.strokeText;
      ctx.save();
      try {
        ctx.translate(c.x, 0); ctx.scale(-1, 1); ctx.translate(-c.x, 0);
        ctx.fillText = function (s, x, y, mw) {
          ctx.save(); ctx.translate(x, y); ctx.scale(-1, 1);
          if (mw === undefined) prevF.call(ctx, s, 0, 0); else prevF.call(ctx, s, 0, 0, mw);
          ctx.restore();
        };
        ctx.strokeText = function (s, x, y, mw) {
          ctx.save(); ctx.translate(x, y); ctx.scale(-1, 1);
          if (mw === undefined) prevS.call(ctx, s, 0, 0); else prevS.call(ctx, s, 0, 0, mw);
          ctx.restore();
        };
        return _dc.apply(this, arguments);
      } finally {
        if (ownF) ctx.fillText = prevF; else delete ctx.fillText;
        if (ownS) ctx.strokeText = prevS; else delete ctx.strokeText;
        ctx.restore();
      }
    };
  } else {
    try { console.warn("proteus v4 Flip: drawComp() not found - c.flipX is toggled but nothing will be mirrored"); } catch (e) {}
  }

  function findBtn(rx) {
    var bs = document.querySelectorAll("button:not([data-px])");
    for (var i = 0; i < bs.length; i++) {
      var b = bs[i], s = (b.id || "") + " " + (b.textContent || "") + " " + (b.title || "") + " " + (b.getAttribute("aria-label") || "");
      if (rx.test(s)) return b;
    }
    return null;
  }

  var btn = document.createElement("button");
  btn.id = "btnFlip";
  btn.textContent = "\u2194 " + t("قلب", "Flip");
  btn.title = t("قلب المكوّن (مرآة)", "Mirror the selected part");
  btn.onclick = function () {
    var c = selComp();
    if (!c) { window.pxToast(t("حدد مكوناً أولاً", "Select a part first")); return; }
    snap();
    c.flipX = !c.flipX;
    scheduleSave(); draw();
  };
  // next to Rotate / Delete in the bottom toolbar; floating fallback if that toolbar is not found
  var rot = findBtn(/rotate|تدوير|دوّر|دوران|\u21BB|\u27F3|\u{1F504}/iu) || findBtn(/delete|حذف|\u{1F5D1}/iu);
  if (rot && rot.parentNode) { btn.className = rot.className; rot.insertAdjacentElement("afterend", btn); }
  else { btn.style.cssText = "position:fixed;left:8px;bottom:64px;z-index:55;padding:6px 10px"; document.body.appendChild(btn); }

  reg.save.flip = function () {
    var out = []; comps.forEach(function (c) { if (c.flipX) out.push(c.id); }); return out;
  };
  reg.load.flip = function (list) {
    comps.forEach(function (c) { c.flipX = !!(Array.isArray(list) && list.indexOf(c.id) >= 0); });
  };
})();
'''

# ---------------------------------------------------------------------------------------------------------------------
# Feature 14: Net highlighting
# ---------------------------------------------------------------------------------------------------------------------
NETHL_JS = MARK_NETHL + r'''
(function () {
  if (window.__pxNetHL) return; window.__pxNetHL = 1;

  function drawNet() {
    var sw = window.pxSelWire();
    if (!sw || sw.cut) return;
    var net = window.pxNetOf(sw), keys = Object.keys(net.keys), others = 0;
    ctx.save();
    ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.setLineDash([]);
    net.wires.forEach(function (w) {
      if (w === sw) return;
      var P = window.pxWirePts(w); if (!P) return;
      others++;
      ctx.beginPath(); ctx.moveTo(P[0].x, P[0].y);
      for (var i = 1; i < P.length; i++) ctx.lineTo(P[i].x, P[i].y);
      ctx.shadowColor = "#22d3ee"; ctx.shadowBlur = 16; ctx.lineWidth = 8; ctx.strokeStyle = "rgba(34,211,238,.30)"; ctx.stroke();
      ctx.shadowBlur = 10; ctx.lineWidth = 4.5; ctx.strokeStyle = "#22d3ee"; ctx.stroke();
    });
    ctx.shadowBlur = 0;
    var pins = 0;
    keys.forEach(function (k) {
      var p = keyPos(k); if (!p) return;
      pins++;
      ctx.beginPath(); ctx.arc(p.x, p.y, 7, 0, Math.PI * 2); ctx.fillStyle = "rgba(15,23,42,.92)"; ctx.fill();
      ctx.lineWidth = 2.5; ctx.strokeStyle = "#22d3ee"; ctx.stroke();
      ctx.beginPath(); ctx.arc(p.x, p.y, 2.5, 0, Math.PI * 2); ctx.fillStyle = "#22d3ee"; ctx.fill();
    });
    var txt = t("الشبكة: ", "NET: ") + (others + 1) + t(" سلك · ", " wires \u00B7 ") + pins + t(" طرف", " pins");
    try {
      if (sim && sim.ok) { var v = sim.nodeV(sw.a); if (typeof v === "number" && isFinite(v)) txt += "  \u00B7  " + v.toFixed(2) + " V"; }
    } catch (e) {}
    ctx.font = "bold 11px monospace"; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    var tw = ctx.measureText(txt).width + 14, bx = cssW / 2 - tw / 2;
    ctx.fillStyle = "rgba(2,6,23,.85)"; ctx.fillRect(bx, 20, tw, 18);
    ctx.fillStyle = "#22d3ee"; ctx.fillText(txt, cssW / 2, 33);
    ctx.restore();
  }

  var _draw = draw;
  draw = function () { _draw(); try { drawNet(); } catch (e) {} };
})();
'''

# ---------------------------------------------------------------------------------------------------------------------
# Feature 15: Fault injection (cut a wire)
#   The solver code (recompute / simulate / nodeMap ...) is not visible from here, so the wires array is filtered while
#   those functions run: a cut wire simply does not exist for the solver, but stays in `wires` for drawing / saving.
# ---------------------------------------------------------------------------------------------------------------------
FAULT_JS = MARK_FAULT + r'''
(function () {
  if (window.__pxFault) return; window.__pxFault = 1;
  var reg = window.pxV4Reg = window.pxV4Reg || { save: {}, load: {} };
''' + JS_BAR_HELPER + JS_UI_HELPER + r'''
  function hasCut() { for (var i = 0; i < wires.length; i++) if (wires[i] && wires[i].cut) return true; return false; }
  function anyCut() { return hasCut(); }

  // run fn with the cut wires removed from `wires` (restored in `finally`); re-entrant
  function wrapCut(fn) {
    if (typeof fn !== "function" || fn.__pxCut) return fn;
    var w = function () {
      if (window.__pxCutFull || !hasCut()) return fn.apply(this, arguments);
      var full = wires.slice();
      window.__pxCutFull = full;
      wires.length = 0; full.forEach(function (x) { if (!x.cut) wires.push(x); });
      try { return fn.apply(this, arguments); }
      finally { wires.length = 0; full.forEach(function (x) { wires.push(x); }); window.__pxCutFull = null; }
    };
    w.__pxCut = 1;
    return w;
  }

  var wrapped = [];
  try { if (typeof recompute === "function") { recompute = wrapCut(recompute); wrapped.push("recompute"); } } catch (e) {}
  try { if (typeof simulate === "function") { simulate = wrapCut(simulate); wrapped.push("simulate"); } } catch (e) {}
  try { if (typeof nodeMap === "function") { nodeMap = wrapCut(nodeMap); wrapped.push("nodeMap"); } } catch (e) {}
  try { if (typeof buildNodeMap === "function") { buildNodeMap = wrapCut(buildNodeMap); wrapped.push("buildNodeMap"); } } catch (e) {}
  try { if (typeof buildSim === "function") { buildSim = wrapCut(buildSim); wrapped.push("buildSim"); } } catch (e) {}
  try { if (typeof solveCircuit === "function") { solveCircuit = wrapCut(solveCircuit); wrapped.push("solveCircuit"); } } catch (e) {}
  try { if (typeof window.pxBuildNetlist === "function") { window.pxBuildNetlist = wrapCut(window.pxBuildNetlist); wrapped.push("pxBuildNetlist"); } } catch (e) {}
  window.pxFaultWrapped = wrapped;
  if (wrapped.indexOf("recompute") < 0) { try { console.warn("proteus v4 Fault: recompute() could not be wrapped - cut wires will not open the circuit"); } catch (e) {} }

  // a cut wire is invisible in the normal wire pass (transparent); the red dashed wire + X is drawn by this feature
  try {
    if (typeof pxWireColor === "function") {
      var _wc = pxWireColor;
      pxWireColor = function (w) { return (w && w.cut) ? "rgba(0,0,0,0)" : _wc.apply(this, arguments); };
    }
  } catch (e) {}

  function drawCut() {
    var any = false;
    ctx.save();
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    wires.forEach(function (w) {
      if (!w.cut) return;
      var P = window.pxWirePts(w); if (!P) return;
      any = true;
      ctx.beginPath(); ctx.moveTo(P[0].x, P[0].y);
      for (var i = 1; i < P.length; i++) ctx.lineTo(P[i].x, P[i].y);
      ctx.setLineDash([7, 5]); ctx.lineWidth = 3; ctx.strokeStyle = "#ef4444"; ctx.stroke();
      ctx.setLineDash([]);
      [P[0], P[P.length - 1]].forEach(function (p) {
        ctx.beginPath(); ctx.arc(p.x, p.y, 4, 0, Math.PI * 2); ctx.lineWidth = 2; ctx.strokeStyle = "#ef4444"; ctx.stroke();
      });
      var m = window.pxPathMid(P);
      ctx.beginPath(); ctx.arc(m.x, m.y, 10, 0, Math.PI * 2); ctx.fillStyle = "rgba(15,23,42,.95)"; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = "#ef4444"; ctx.stroke();
      ctx.lineWidth = 3; ctx.beginPath();
      ctx.moveTo(m.x - 5, m.y - 5); ctx.lineTo(m.x + 5, m.y + 5); ctx.moveTo(m.x + 5, m.y - 5); ctx.lineTo(m.x - 5, m.y + 5); ctx.stroke();
    });
    ctx.restore();
    return any;
  }

  var btn = document.createElement("button");
  btn.id = "btnFault";
  btn.textContent = "\u26A0 " + t("عطل", "Fault");
  btn.title = t("قطع السلك المحدد (اضغط مرة أخرى لإصلاحه)", "Cut the selected wire (tap again to repair it)");
  function paint() { btn.style.background = anyCut() ? "#b91c1c" : ""; }
  btn.onclick = function () {
    var w = window.pxSelWire();
    if (!w) {
      if (anyCut()) {                                   // nothing selected: repair every fault
        snap(); wires.forEach(function (x) { delete x.cut; });
        recompute(); scheduleSave(); draw(); paint();
        window.pxToast(t("تم إصلاح كل الأعطال", "All faults repaired"));
      } else window.pxToast(t("حدد سلكاً أولاً ثم اضغط عطل", "Select a wire first, then tap Fault"));
      return;
    }
    snap();
    if (w.cut) delete w.cut; else w.cut = true;
    recompute(); scheduleSave(); draw(); paint();
    window.pxToast(w.cut ? t("تم قطع السلك: الدائرة مفتوحة", "Wire cut: circuit opened") : t("تم إصلاح السلك", "Wire repaired"));
  };
  window.pxAddBar(btn);

  // while a wrapped solver runs (it may call draw() itself) the wires array is filtered: draw the full set, then put it back
  var _draw = draw;
  draw = function () {
    var full = window.__pxCutFull, kept = null;
    if (full) { kept = wires.slice(); wires.length = 0; full.forEach(function (x) { wires.push(x); }); }
    try { _draw(); try { drawCut(); } catch (e) {} }
    finally { if (kept) { wires.length = 0; kept.forEach(function (x) { wires.push(x); }); } }
    paint();
  };

  reg.save.cut = function () {
    var out = []; wires.forEach(function (w) { if (w.cut) out.push([w.a, w.b]); }); return out;
  };
  reg.load.cut = function (list) {
    wires.forEach(function (w) { delete w.cut; });
    var n = 0;
    if (Array.isArray(list)) list.forEach(function (p) {
      if (!Array.isArray(p) || p.length < 2) return;
      wires.forEach(function (w) { if ((w.a === p[0] && w.b === p[1]) || (w.a === p[1] && w.b === p[0])) { w.cut = true; n++; } });
    });
    if (n) { try { recompute(); } catch (e) {} }
    paint();
  };
  paint();
})();
'''


# Order matters only for the order of the top-bar buttons:
#   [Scope][Logic][Sig Gen][Probe][V/A][Netlist][0.1x][1x][10x][Fault]
# The v4 core must come after the v3 features (it wraps loadState last) and before the other v4 features.
FEATURES = [
    ("Logic Analyzer", MARK_LOGIC, LOGIC_EDITS, LOGIC_JS),
    ("Signal Generator", MARK_GEN, GEN_EDITS, GEN_JS),
    ("Voltage-colored wires", MARK_WIRE, WIRE_EDITS, WIRE_JS),
    ("Logic Probes", MARK_PROBE, PROBE_EDITS, PROBE_JS),
    ("Orthogonal wires", MARK_ORTHO, ORTHO_EDITS, ORTHO_JS),
    ("V/A probes", MARK_VAPROBE, VAPROBE_EDITS, VAPROBE_JS),
    ("Properties editor", MARK_PROPS, [], PROPS_JS),
    ("Interactive 7-seg / LCD", MARK_DISPLAYS, DISPLAYS_EDITS, DISPLAYS_JS),
    ("Netlist export", MARK_NETLIST, [], NETLIST_JS),
    ("Scope cursors", MARK_CURSORS, CURSORS_EDITS, CURSORS_JS),
    # ---- v4 ----
    ("v4 core (shared helpers + state)", MARK_V4CORE, V4CORE_EDITS, V4CORE_JS),
    ("Component labels (rename)", MARK_RENAME, [], RENAME_JS),
    ("Simulation speed", MARK_SPEED, SPEED_EDITS, SPEED_JS),
    ("Mirroring (flip)", MARK_FLIP, [], FLIP_JS),
    ("Net highlighting", MARK_NETHL, [], NETHL_JS),
    ("Fault injection", MARK_FAULT, [], FAULT_JS),
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
    for w in WARNINGS:
        print("   ! WARNING " + w)


main()

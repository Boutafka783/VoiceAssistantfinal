#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bridge_patch.py — الجسر (الميكاترونكس)
يربط مختبر الإلكترونيات بمختبر الميكانيكا عبر SharedPreferences.
آمن للتشغيل المتكرر. ينشئ نسخ احتياطية .bak
"""
import os, shutil, sys

ROOT = os.environ.get("PROJECT_DIR", ".")
PKG_DIR = os.path.join(ROOT, "app", "src", "main", "java", "com", "example", "voiceassistant")
ASSETS_DIR = os.path.join(ROOT, "app", "src", "main", "assets")
CIRCUIT_HTML = os.path.join(ASSETS_DIR, "circuit_sim.html")
MECH_HTML = os.path.join(ASSETS_DIR, "mech_sim.html")
CIRCUIT_KT = os.path.join(PKG_DIR, "CircuitSimulatorActivity.kt")
MECH_KT = os.path.join(PKG_DIR, "MechSimulatorActivity.kt")

def die(m): sys.exit("bridge_patch.py: " + m)
def read(p):
    if not os.path.isfile(p): die("لم أجد: " + p)
    with open(p, "r", encoding="utf-8", newline="") as f: return f.read()
def write(p, t):
    with open(p, "w", encoding="utf-8", newline="\n") as f: f.write(t)

def patch(text, old, new, mark, label, stats):
    if mark in text:
        print("   = تخطّي %s (مُطبَّق)" % label); stats["skip"] += 1; return text
    n = text.count(old)
    if n == 0:
        print("   ✗ فشل %s: لم أجد الكتلة" % label); stats["fail"] += 1; return text
    if n > 1:
        print("   ✗ فشل %s: وُجدت %d مرات" % (label, n)); stats["fail"] += 1; return text
    print("   + %s" % label); stats["ok"] += 1
    return text.replace(old, new, 1)

def main():
    stats = {"ok": 0, "skip": 0, "fail": 0}

    for p in [CIRCUIT_HTML, MECH_HTML, CIRCUIT_KT, MECH_KT]:
        if os.path.isfile(p): shutil.copy2(p, p + ".bak")
    print(">> نسخ احتياطية: *.bak"); print()

    # ═══ 1. Circuit HTML: publishBridge() ═══
    ch = read(CIRCUIT_HTML)
    old = "function measureResistance(keyA, keyB) {"
    new = """function publishBridge() {
  if (!(window.Android && Android.saveBridgeState)) return;
  try {
    if (!sim || !sim.ok) { Android.saveBridgeState('{}'); return; }
    var list = [];
    comps.forEach(function(c) {
      if (c.type === 'motor') {
        list.push({ id: c.id, on: Math.abs(sim.I[c.id]) > 0.001, v: Math.abs(sim.V[c.id]) });
      }
    });
    Android.saveBridgeState(JSON.stringify({ motors: list, ts: Date.now() }));
  } catch (e) {}
}

function measureResistance(keyA, keyB) {"""
    ch = patch(ch, old, new, "function publishBridge()",
               "circuit HTML: دالة publishBridge", stats)

    # ═══ 2. Circuit HTML: استدعاء من recompute ═══
    old2 = """  if (!fast) updateTools();
  updateSound();
  if (!fast) { draw(); scheduleSave(); }"""
    new2 = """  if (!fast) updateTools();
  updateSound();
  publishBridge();
  if (!fast) { draw(); scheduleSave(); }"""
    ch = patch(ch, old2, new2, "publishBridge();\n  if (!fast)",
               "circuit HTML: استدعاء publishBridge", stats)
    if stats["fail"] == 0: write(CIRCUIT_HTML, ch)

    # ═══ 3. Circuit Kotlin: saveBridgeState ═══
    ck = read(CIRCUIT_KT)
    old3 = '''        @JavascriptInterface fun loadState(): String = prefs.getString("state", "") ?: ""'''
    new3 = '''        @JavascriptInterface fun loadState(): String = prefs.getString("state", "") ?: ""

        @JavascriptInterface
        fun saveBridgeState(json: String) {
            if (json.length < 20000) {
                getSharedPreferences("mech_bridge", android.content.Context.MODE_PRIVATE).edit().putString("state", json).apply()
            }
        }'''
    ck = patch(ck, old3, new3, "fun saveBridgeState",
               "circuit Kotlin: saveBridgeState", stats)
    if stats["fail"] == 0: write(CIRCUIT_KT, ck)

    # ═══ 4. Mech Kotlin: loadBridgeState + saveState + loadState ═══
    mk = read(MECH_KT)
    old4 = """        @JavascriptInterface
        fun close() { runOnUiThread { finish() } }"""
    # 🚨 تم إصلاح هذا الجزء بتحويل الدوال إلى Block Body 🚨
    new4 = """        @JavascriptInterface
        fun close() { runOnUiThread { finish() } }

        @JavascriptInterface
        fun loadBridgeState(): String {
            return getSharedPreferences("mech_bridge", android.content.Context.MODE_PRIVATE).getString("state", "") ?: ""
        }

        @JavascriptInterface
        fun saveState(json: String) {
            if (json.length < 500000) {
                getSharedPreferences("mech_lab", android.content.Context.MODE_PRIVATE).edit().putString("state", json).apply()
            }
        }

        @JavascriptInterface
        fun loadState(): String {
            return getSharedPreferences("mech_lab", android.content.Context.MODE_PRIVATE).getString("state", "") ?: ""
        }"""
    mk = patch(mk, old4, new4, "fun loadBridgeState",
               "mech Kotlin: loadBridgeState + saveState + loadState", stats)
    if stats["fail"] == 0: write(MECH_KT, mk)

    # ═══ 5. Mech HTML: زر ربط ═══
    mh = read(MECH_HTML)
    old5 = """  <button id="btnPause" onclick="togglePause()">⏸</button>"""
    new5 = """  <button id="btnBridge" onclick="toggleBridge()">🔗 ربط</button>
  <button id="btnPause" onclick="togglePause()">⏸</button>"""
    mh = patch(mh, old5, new5, 'id="btnBridge"',
               "mech HTML: زر ربط", stats)

    # ═══ 6. Mech HTML: متغيرات ═══
    old6 = "var busy = false, busyTimer = null, last = 0, acc = 0;"
    new6 = """var busy = false, busyTimer = null, last = 0, acc = 0;
var bridgeOn = false, bridgeLastPoll = 0;"""
    mh = patch(mh, old6, new6, "var bridgeOn = false",
               "mech HTML: متغيرات bridge", stats)

    # ═══ 7. Mech HTML: toggleBridge + pollBridge ═══
    old7 = """function togglePause() {
  paused = !paused;
  document.getElementById("btnPause").textContent = paused ? "▶" : "⏸";
}"""
    new7 = """function togglePause() {
  paused = !paused;
  document.getElementById("btnPause").textContent = paused ? "▶" : "⏸";
}

function toggleBridge() {
  bridgeOn = !bridgeOn;
  var b = document.getElementById("btnBridge");
  if (b) { b.className = bridgeOn ? "primary" : ""; b.textContent = bridgeOn ? "🔗 متصل" : "🔗 ربط"; }
}

function pollBridge(now) {
  if (!bridgeOn) return;
  if (now - bridgeLastPoll < 200) return;
  bridgeLastPoll = now;
  if (!(window.Android && Android.loadBridgeState)) return;
  try {
    var raw = Android.loadBridgeState();
    if (!raw || raw === "{}") return;
    var data = JSON.parse(raw);
    var motors = data.motors || [];
    var anyOn = false, maxV = 0;
    for (var i = 0; i < motors.length; i++) {
      if (motors[i].on) { anyOn = true; if (motors[i].v > maxV) maxV = motors[i].v; }
    }
    var targetRpm = anyOn ? Math.min(300, Math.max(15, maxV * 15)) : 0;
    bodies.forEach(function(o) {
      if (o.type === "motor") {
        o.rpm = targetRpm;
        o.bridgeDriven = anyOn;
      }
    });
  } catch (e) {}
}"""
    mh = patch(mh, old7, new7, "function toggleBridge()",
               "mech HTML: toggleBridge + pollBridge", stats)

    # ═══ 8. Mech HTML: استدعاء pollBridge من loop ═══
    old8 = """function loop(t) {
  var dt = Math.min(0.05, ((t - last) / 1000) || 0);
  last = t;
  if (!paused) {"""
    new8 = """function loop(t) {
  var dt = Math.min(0.05, ((t - last) / 1000) || 0);
  last = t;
  pollBridge(t);
  if (!paused) {"""
    mh = patch(mh, old8, new8, "pollBridge(t);\n  if (!paused)",
               "mech HTML: استدعاء pollBridge في loop", stats)
    if stats["fail"] == 0: write(MECH_HTML, mh)

    print()
    print(">> النتيجة: %d مطبّق + %d متخطّى + %d فشل." % (stats["ok"], stats["skip"], stats["fail"]))
    if stats["fail"] > 0:
        print("   ⚠ لم يتم حفظ بعض الملفات. راجع الرسائل.")
        sys.exit(1)

if __name__ == "__main__":
    main()
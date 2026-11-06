#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bridge_patch.py — الجسر (الميكاترونكس)
يربط مختبر الإلكترونيات بمختبر الميكانيكا عبر SharedPreferences.
آمن للتشغيل المتكرر. ينشئ نسخ احتياطية .bak
"""
import os, re, shutil, sys

ROOT = os.environ.get("PROJECT_DIR", ".")


def discover_package():
    """اكتشاف الحزمة حسب إعدادات المشروع، مع إبقاء القيمة القديمة كخيار احتياطي."""
    # 1) متغير البيئة APP_PACKAGE
    value = os.environ.get("APP_PACKAGE", "").strip()
    if value:
        return value

    # 2) namespace أو applicationId من Gradle
    gradle_files = [
        os.path.join(ROOT, "app", "build.gradle.kts"),
        os.path.join(ROOT, "app", "build.gradle"),
        os.path.join(ROOT, "build.gradle.kts"),
        os.path.join(ROOT, "build.gradle"),
    ]
    for gradle_file in gradle_files:
        if not os.path.isfile(gradle_file):
            continue
        with open(gradle_file, "r", encoding="utf-8") as f:
            content = f.read()
        for key in ("namespace", "applicationId"):
            match = re.search(
                "\\b" + key + "\\s*(?:=\\s*)?[\\\"']([A-Za-z_][A-Za-z0-9_.]*)[\\\"']",
                content
            )
            if match:
                return match.group(1)

    # 3) package من AndroidManifest.xml
    manifest = os.path.join(ROOT, "app", "src", "main", "AndroidManifest.xml")
    if os.path.isfile(manifest):
        with open(manifest, "r", encoding="utf-8") as f:
            match = re.search("\\bpackage\\s*=\\s*[\\\"']([^\\\"']+)[\\\"']", f.read())
        if match:
            return match.group(1).strip()

    # 4) fallback
    return "com.example.voiceassistant"


PACKAGE_NAME = discover_package()
PKG_DIR = os.path.join(ROOT, "app", "src", "main", "java", *PACKAGE_NAME.split("."))
ASSETS_DIR = os.path.join(ROOT, "app", "src", "main", "assets")
CIRCUIT_HTML = os.path.join(ASSETS_DIR, "circuit_sim.html")
MECH_HTML = os.path.join(ASSETS_DIR, "mech_sim.html")
CIRCUIT_KT = os.path.join(PKG_DIR, "CircuitSimulatorActivity.kt")
MECH_KT = os.path.join(PKG_DIR, "MechSimulatorActivity.kt")
ROBOT_KT = os.path.join(PKG_DIR, "RobotStudioActivity.kt")

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
    stats = {"ok": 0, "skip": 0, "fail": 0, "warn": 0}

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


    # ═══ 9. Robot Kotlin: إضافة دوال الجسر والحفظ ═══
    if not os.path.isfile(ROBOT_KT):
        print("   = تخطّي robot Kotlin: الملف RobotStudioActivity.kt غير موجود")
        stats["skip"] += 1
    else:
        shutil.copy2(ROBOT_KT, ROBOT_KT + ".bak")
        rk = read(ROBOT_KT)
        robot_anchor = """    }

    private fun js(code: String) = runOnUiThread { web.evaluateJavascript(code, null) }"""
        robot_methods = """        // قراءة حالة المحركات القادمة من مختبر الإلكترونيات
        @JavascriptInterface
        fun loadBridgeState(): String {
            return getSharedPreferences("mech_bridge", android.content.Context.MODE_PRIVATE).getString("state", "") ?: ""
        }

        // حفظ واسترجاع حالة ورشة الروبوتات محلياً
        @JavascriptInterface
        fun saveState(json: String) {
            if (json.length < 500000) {
                getSharedPreferences("robot_lab", android.content.Context.MODE_PRIVATE).edit().putString("state", json).apply()
            }
        }

        @JavascriptInterface
        fun loadState(): String {
            return getSharedPreferences("robot_lab", android.content.Context.MODE_PRIVATE).getString("state", "") ?: ""
        }

    }

    private fun js(code: String) = runOnUiThread { web.evaluateJavascript(code, null) }"""
        if "fun loadBridgeState" in rk:
            print("   = تخطّي robot Kotlin: دوال الجسر موجودة مسبقاً")
            stats["skip"] += 1
        elif rk.count(robot_anchor) != 1:
            print("   ⚠ تحذير robot Kotlin: لم أجد موضع إدراج الدوال كما هو متوقع")
            stats["warn"] += 1
        else:
            rk = rk.replace(robot_anchor, robot_methods, 1)
            write(ROBOT_KT, rk)
            print("   + robot Kotlin: loadBridgeState + saveState + loadState")
            stats["ok"] += 1

        # ═══ 9b. Robot Kotlin: قبول استجابة JSON الخام من الخادم ═══
        # مهم: السطور هنا داخل Thread → try → use → askAi، فإزاحتها 24 مسافة
        old9b = """                        val text = json?.optString("text", "") ?: ""
                        if (r.isSuccessful && text.isNotEmpty()) {
                            reply(id, true, text)
                        } else {
                            reply(id, false, "")
                        }"""
        new9b = """                        val text = json?.optString("text", "") ?: ""
                        // الخادم قد يرجع JSON مباشراً (مثل {"action":"build",...}) بدون حقل text
                        val hasAction = try { json?.has("action") == true } catch (e: Exception) { false }
                        if (r.isSuccessful && hasAction) {
                            reply(id, true, raw)
                        } else if (r.isSuccessful && text.isNotEmpty()) {
                            reply(id, true, text)
                        } else if (r.isSuccessful && raw.trim().startsWith("{")) {
                            reply(id, true, raw)
                        } else {
                            reply(id, false, "")
                        }"""
        mark_9b = "hasAction"
        if mark_9b in rk:
            print("   = تخطّي robot Kotlin: معالجة JSON الخام موجودة مسبقاً")
            stats["skip"] += 1
        elif rk.count(old9b) != 1:
            print("   ⚠ تحذير robot Kotlin: لم أجد مقطع askAi المطلوب مطابقاً")
            stats["warn"] += 1
        else:
            rk = rk.replace(old9b, new9b, 1)
            write(ROBOT_KT, rk)
            print("   + robot Kotlin: إصلاح استجابة JSON الخام في askAi")
            stats["ok"] += 1

    print()
    print(">> النتيجة: %d مطبّق + %d متخطّى + %d تحذير + %d فشل." % (stats["ok"], stats["skip"], stats["warn"], stats["fail"]))
    if stats["fail"] > 0:
        print("   ⚠ لم يتم حفظ بعض الملفات. راجع الرسائل.")
        sys.exit(1)

if __name__ == "__main__":
    main()
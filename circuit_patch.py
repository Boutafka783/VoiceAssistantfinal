#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
circuit_patch.py
يضيف ميزة «مختبر الإلكترونيات» (Circuit Lab) إلى المشروع الذي ولّده setup.py.
- الإصدار 5: المقاومة المتغيرة، المقاومة الضوئية (LDR)، محرك DC، الجرس (Buzzer).
- الإصدار 9: مرحّل (Relay) بأربعة أطراف (ملف + نقطة مشتركة + تلامس مفتوح عادةً)، وتصدير الدائرة كصورة PNG إلى المعرض.
- الإصدار 8: مصدر تيار متردد (AC 50Hz بحركة بطيئة للعرض) وراسم إشارة بقناتين، ومثال مقوّم نصف موجة.
- الإصدار 7: بوابات المنطق (AND, OR, NOT) مع محاكاة صحيحة، وتوليد كود الأردوينو بالذكاء الاصطناعي،
             وتصحيح مواضع أطراف العناصر المُدارة.
- الإصدار 6: مقاومة متغيرة حقيقية بثلاثة أطراف (مؤشر)، تصحيح منطق المفتاح،
             محرك يدور، جرس بصوت، وانسياب التيار في الأسلاك.
- الإصدار 31: 666 عنصراً جديداً (الدفعة 21) — 106 مكوناً أساسياً بنماذج حقيقية (LED، مقاومات، مكثفات، دايودات، ترانزستورات، MOSFET، ملفات، أحمال، مفاتيح، مصادر) و560 شريحة/حساساً/وحدة — الإجمالي 1278 عنصراً.
- الإصدار 30: 245 عنصراً جديداً (الدفعة 20) — 51 مكوناً أساسياً يعمل بنموذج حقيقي (مكثفات، دايودات، ترانزستورات NPN/PNP، MOSFET، ملفات، أحمال، مفاتيح، بطاريات) في تاب «مكونات» جديد، و194 شريحة/حساساً/وحدة (حساسات، شاشات، تشغيل محركات، منظمات، اتصالات، منطق، ذاكرة، مضخمات) — الإجمالي 612 عنصراً في 10 تابات.
- الإصدار 29: 114 عنصراً جديداً (الدفعة 19) — الإجمالي 367 عنصراً في 9 تابات.
- الإصدار 28: 100 عنصر جديد (الدفعة 18) — الإجمالي 253 عنصراً في 9 تابات.
- الإصدار 27: تنظيم واجهة الاختيار إلى 9 تابات مصنّفة (153 عنصراً).
- الإصدار 26: 12 عنصراً جديداً (DS1302، MAX6675، MAX31855، SD_CARD، ENC28J60، ULN2803، TLC5940، MPU9250، AD9833، AMS1117، XL6009، VL6180X).
- الإصدار 25: 12 عنصراً جديداً (PCA9685، TCA9548A، L9110S، TMP36، AM2320، DS1307، PCF8563، ST7735، SSD1351، BMP180، SHT31، APDS-9960).
- الإصدار 24: 12 عنصراً جديداً (DRV8825، TB6612FNG، BTS7960، TCS34725، MLX90614، MAX30102، ADXL345، HX711، DHT22، SGP30، RC522، BME680).
- الإصدار 23: 12 عنصراً جديداً (A4988، PAM8403، MAX98357A، ADS1115، MCP4725، INA219، MQ-2، BH1750، VL53L0X، 74HC165، NRF24L01، SIM800L).
- الإصدار 22: 12 عنصراً جديداً (MPU6050، BMP280، ACS712، A3144، KY-038، YL-69، TTP223، KY-040، WS2812، TSOP، HC-05، L298N).
- الإصدار 21: 12 عنصراً (TDA7297، OPA2134، AD620، OPA548، LM337، CD4013، CD4015، 74HC273، 74HC373، AT24C32، MCP23017، 74HC00).
- الإصدار 20: LM741، NE5534، TDA2822، CD4051، PCF8574، CD4066 + إعادة هيكلة termList/nodeMap (hasThreePins).
- الإصدار 19: TDA2030، LM2596، TP4056، ADC0804، DAC0808، MAX7219.
- الإصدار 18: TL072، LM324، NE556، ULN2003، LM1117، LM3914.
- الإصدار 17: مضخمات LM386 / LM358 / NE5532 ومكاملات LM393 / CD4017 / 74HC138.
- الإصدار 16: شاشة OLED، 7-segment برقمين، L293D، 74HC595، DS3231، عازل ضوئي.
- الإصدار 15: شاشة LCD، حساس HC-SR04، DS18B20، محرك ستيبر، LED RGB، مقاومة حماية (MOV).
- الإصدار 14: بوابات NAND/XOR/XNOR، MOSFET-N، منظم LM317، محرك سيرفو.
- الإصدار 13: حساس PIR، حساس DHT11، شاشة 7-segment، مؤقت 555.
- الإصدار 12: منظما جهد 7805/7803، مكبر عمليات (مقارن)، ترانزستور PNP.
- الإصدار 11: 11 عنصراً جديداً (ملف حث، مقاومة حرارية، سماعة، زينر، شوتكي، نانو، ميجا، ESP8266، بيكو، خلية شمسية، مصدر خارجي).
- الإصدار 10: مصمم PCB (توجيه تلقائي، SVG، PNG، Gerber ZIP) + أكواد CNC (عزل المسارات، الثقب، القص) +
             تراجع/إعادة + حفظ الملفات في التنزيلات + نافذة إدخال للأكواد في WebView.
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
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--accent:#38bdf8;--bad:#f87171;--good:#4ade80;--warn:#fbbf24;--purple:#a855f7;--orange:#f97316}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;overflow:hidden;touch-action:manipulation}
#app{display:flex;flex-direction:column;height:100%}
header{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:8px 10px;background:var(--panel);border-bottom:1px solid var(--line)}
header h1{flex:1;margin:0;font-size:15px;font-weight:700}
button{font:inherit;color:var(--text);background:#334155;border:1px solid #475569;border-radius:10px;padding:7px 11px;font-size:13px;cursor:pointer;white-space:nowrap}
button:active{background:#475569}
button.primary{background:#0284c7;border-color:#0ea5e9}
button.danger{background:#7f1d1d;border-color:#b91c1c}
button.fix{background:var(--purple);border-color:#c084fc}
button.save{background:#10b981;border-color:#34d399}
button.code{background:var(--orange);border-color:#fb923c}
button.download{background:#6366f1;border-color:#818cf8}
button:disabled{opacity:.5}
#paletteBar{display:flex;gap:6px;padding:6px 8px;overflow-x:auto;background:#162033;border-bottom:1px solid var(--line);flex-wrap:wrap}
#paletteBar button{flex:0 0 auto}
#paletteTabs{display:flex;gap:4px;padding:6px 8px;overflow-x:auto;background:#0f172a;border-bottom:1px solid var(--line);flex-wrap:nowrap}
#paletteTabs button{padding:5px 11px;font-size:12px;border-radius:8px;background:#334155;border:1px solid #475569;color:#cbd5e1;white-space:nowrap;flex:0 0 auto}
#paletteTabs button.active{background:#0284c7;border-color:#0ea5e9;color:#fff;font-weight:600}
#paletteButtons{display:flex;gap:6px;padding:6px 8px;overflow-x:auto;background:#162033;border-bottom:1px solid var(--line);flex-wrap:nowrap}
#paletteButtons button{flex:0 0 auto}
#stage{flex:1;position:relative;min-height:120px}
canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none;display:block}
#status{padding:6px 10px;font-size:12.5px;line-height:1.5;min-height:30px;background:#162033;border-top:1px solid var(--line);color:var(--muted)}
#status.ok{color:var(--good)}#status.warn{color:var(--warn)}#status.bad{color:var(--bad)}
#tools{display:none;gap:6px;align-items:center;flex-wrap:wrap;padding:6px 8px;background:var(--panel);border-top:1px solid var(--line)}
#tools.show{display:flex}
#tools .lbl{flex:1;min-width:90px;font-size:13px;font-weight:600}
#ai{display:flex;flex-wrap:wrap;gap:6px;padding:8px;background:var(--panel);border-top:1px solid var(--line)}
#ai input{flex:1;min-width:140px;font:inherit;font-size:14px;color:var(--text);background:#0b1220;border:1px solid #475569;border-radius:10px;padding:8px 10px}
#answer{display:none;position:absolute;inset:8px;background:rgba(15,23,42,.96);border:1px solid var(--accent);border-radius:14px;padding:12px;overflow:auto;z-index:5}
#answer.show{display:block}
#answer pre{white-space:pre-wrap;word-wrap:break-word;font:inherit;font-size:14px;line-height:1.7;margin:0 0 10px;unicode-bidi:plaintext;text-align:start}
#busy{display:none;position:absolute;inset:0;background:rgba(15,23,42,.55);z-index:6;align-items:center;justify-content:center;font-size:15px}
#busy.show{display:flex}
#pcb{display:none;position:fixed;inset:0;z-index:30;background:var(--bg);flex-direction:column;overflow-y:auto}
#pcb.show{display:flex}
.pbar{display:flex;gap:6px;align-items:center;flex-wrap:wrap;padding:6px 8px;background:var(--panel);border-bottom:1px solid var(--line)}
#pcbCv{position:relative;inset:auto;width:100%;height:46vh;flex:0 0 46vh;background:#0b1220;touch-action:none}
#pcbStatus{padding:6px 10px;font-size:12px;line-height:1.5;min-height:34px;color:var(--muted)}
#pcbStatus.ok{color:var(--good)}#pcbStatus.warn{color:var(--warn)}#pcbStatus.bad{color:var(--bad)}
.pcnc{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;padding:8px;background:#162033;border-top:1px solid var(--line)}
.pcnc label{display:flex;align-items:center;justify-content:space-between;gap:6px;font-size:12px}
.pcnc input,.pcnc select,#pcbLayers{width:76px;font:inherit;font-size:13px;color:var(--text);background:#0b1220;border:1px solid #475569;border-radius:8px;padding:4px 6px}
.off{opacity:.45}
</style>
</head>
<body>
<div id="app">
  <header>
    <h1 data-ar="مختبر الإلكترونيات ⚡" data-en="Electronics Lab ⚡"></h1>
    <button id="btnDemo" data-ar="مثال" data-en="Example"></button>
    <button id="btnExport" class="download" data-ar="تصدير" data-en="Export"></button>
    <button id="btnImport" class="save" data-ar="استيراد" data-en="Import"></button>
    <button id="btnDownload" class="download" data-ar="صورة 📥" data-en="Image 📥"></button>
    <button id="btnSave" class="save" data-ar="حفظ ☁" data-en="Save ☁"></button>
    <button id="btnLoad" class="save" data-ar="تحميل ☁" data-en="Load ☁"></button>
    <button id="btnClear" class="danger" data-ar="مسح" data-en="Clear"></button>
    <button id="btnSound" data-ar="🔊" data-en="🔊"></button>
    <button id="btnScopeCsv" class="download" style="display:none" data-ar="CSV" data-en="CSV"></button>
    <button id="btnClose" data-ar="✕" data-en="✕"></button>
  </header>
  <input type="file" id="fileInput" accept=".json,application/json" style="display:none">
  <div id="paletteBar"></div>
  <div id="paletteTabs"></div>
  <div id="paletteButtons"></div>
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
    <button id="btnFix" class="fix" data-ar="إصلاح 🪄" data-en="Fix 🪄"></button>
    <button id="btnCode" class="code" data-ar="كود ⚙️" data-en="Code ⚙️"></button>
  </div>
</div>
<div id="pcb">
  <div class="pbar"><b data-ar="مصمم PCB 🟩" data-en="PCB Designer 🟩"></b><span style="flex:1"></span><button id="pcbClose">✕</button></div>
  <div class="pbar">
    <button id="pcbRoute" class="primary" data-ar="توجيه تلقائي" data-en="Auto-route"></button>
    <select id="pcbLayers"><option value="1">1 layer</option><option value="2" selected>2 layers</option></select>
    <button id="pcbTop">Top</button><button id="pcbBot">Bottom</button>
  </div>
  <canvas id="pcbCv"></canvas>
  <div id="pcbStatus"></div>
  <div class="pbar">
    <button id="pcbSvg" class="download">SVG</button>
    <button id="pcbPng" class="download">PNG</button>
    <button id="pcbGerber" class="save">Gerber ZIP</button>
  </div>
  <div class="pcnc">
    <label><span data-ar="وجه التشغيل" data-en="Side up"></span><select id="cSide"><option value="bottom">Bottom</option><option value="top">Top</option></select></label>
    <label><span data-ar="قُطر الأداة" data-en="Bit Ø mm"></span><input id="cTool" type="number" step="0.05" value="0.2"></label>
    <label><span data-ar="عمق الحفر" data-en="Depth mm"></span><input id="cDepth" type="number" step="0.01" value="0.1"></label>
    <label><span data-ar="سرعة القطع" data-en="Feed"></span><input id="cFeed" type="number" value="200"></label>
    <label><span data-ar="سرعة الغرز" data-en="Plunge"></span><input id="cPlunge" type="number" value="80"></label>
    <label><span data-ar="ارتفاع آمن" data-en="Safe Z"></span><input id="cSafe" type="number" step="0.5" value="2"></label>
    <label><span>RPM</span><input id="cRpm" type="number" value="12000"></label>
    <label><span data-ar="ثقب الأرجل" data-en="Pad drill"></span><input id="cDrill" type="number" step="0.05" value="0.9"></label>
    <label><span data-ar="ثقب الفيا" data-en="Via drill"></span><input id="cVia" type="number" step="0.05" value="0.6"></label>
    <label><span data-ar="سماكة اللوح" data-en="Thickness"></span><input id="cThick" type="number" step="0.1" value="1.6"></label>
    <label><span data-ar="أداة القص Ø" data-en="Mill Ø"></span><input id="cMill" type="number" step="0.1" value="2"></label>
    <label><span data-ar="عدد التمريرات" data-en="Iso passes"></span><input id="cPass" type="number" min="1" max="4" value="1"></label>
  </div>
  <div class="pbar">
    <button id="cncIso" class="code" data-ar="G-code عزل" data-en="G-code Isolation"></button>
    <button id="cncDrill" class="code" data-ar="G-code ثقب" data-en="G-code Drill"></button>
    <button id="cncOutline" class="code" data-ar="G-code قص" data-en="G-code Outline"></button>
    <button id="cncZip" class="save" data-ar="CNC ZIP (الكل)" data-en="CNC ZIP (all)"></button>
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
var RGB_COLORS = {
  red: "#ff0000", green: "#00ff00", blue: "#0000ff",
  yellow: "#ffff00", cyan: "#00ffff", magenta: "#ff00ff", white: "#ffffff"
};
var TYPES = {
  battery:    { prefix: "B", ar: "بطارية", en: "Battery", vals: [1.5, 3, 4.5, 5, 9, 12], def: 9 },
  ac_source:  { prefix: "AC", ar: "تيار متردد", en: "AC Source", vals: [5, 12, 24], def: 12 },
  arduino:    { prefix: "AR", ar: "اردوينو", en: "Arduino", vals: [5], def: 5 },
  esp32:      { prefix: "ES", ar: "ESP32", en: "ESP32", vals: [3.3], def: 3.3 },
  resistor:   { prefix: "R", ar: "مقاومة", en: "Resistor", vals: [10, 47, 100, 220, 330, 470, 1000, 2200, 4700, 10000], def: 330 },
  potentiometer: { prefix: "RV", ar: "مقاومة متغيرة", en: "Potentiometer", vals: [0, 100, 500, 1000, 5000, 10000], def: 1000, pins: 3 },
  ldr:        { prefix: "LDR", ar: "مقاومة ضوئية", en: "LDR", vals: [1000, 10000, 100000], def: 10000 },
  capacitor:  { prefix: "C", ar: "مكثف", en: "Capacitor", vals: [10, 47, 100, 470, 1000], def: 100 },
  diode:      { prefix: "E", ar: "دايود", en: "Diode", vals: ["silicon", "germanium"], def: "silicon" },
  transistor: { prefix: "Q", ar: "ترانزستور", en: "Transistor", vals: ["NPN"], def: "NPN", pins: 3 },
  relay:      { prefix: "K", ar: "مرحّل", en: "Relay", vals: [5, 12], def: 5 },
  fuse:       { prefix: "F", ar: "فيوز", en: "Fuse", vals: [0.5, 1, 2, 5], def: 1 },
  led:        { prefix: "D", ar: "LED", en: "LED", vals: ["red", "green", "yellow", "blue", "white"], def: "red" },
  bulb:       { prefix: "L", ar: "مصباح", en: "Bulb", vals: [25, 50, 100], def: 50 },
  motor:      { prefix: "M", ar: "محرك DC", en: "DC Motor", vals: [5, 10, 20], def: 10 },
  buzzer:     { prefix: "BZ", ar: "جرس", en: "Buzzer", vals: [50, 100, 200], def: 100 },
  gate_and:   { prefix: "U", ar: "AND", en: "AND Gate", vals: [], def: 0 },
  gate_or:    { prefix: "U", ar: "OR", en: "OR Gate", vals: [], def: 0 },
  gate_not:   { prefix: "U", ar: "NOT", en: "NOT Gate", vals: [], def: 0 },
  "switch":   { prefix: "S", ar: "مفتاح", en: "Switch", vals: [], def: 0 },
  inductor:   { prefix: "L", ar: "ملف حث", en: "Inductor", vals: [10, 100, 1000], def: 100 },
  thermistor: { prefix: "TH", ar: "مقاومة حرارية", en: "Thermistor", vals: [1000, 10000, 100000], def: 10000 },
  speaker:    { prefix: "SP", ar: "سماعة", en: "Speaker", vals: [4, 8, 16], def: 8 },
  zener:      { prefix: "DZ", ar: "دايود زينر", en: "Zener Diode", vals: [3.3, 5.1, 9.1, 12], def: 5.1 },
  schottky:   { prefix: "DS", ar: "دايود شوتكي", en: "Schottky Diode", vals: ["1N5819", "1N5822"], def: "1N5819" },
  nano:       { prefix: "NA", ar: "اردوينو نانو", en: "Arduino Nano", vals: [5], def: 5 },
  mega:       { prefix: "MG", ar: "اردوينو ميجا", en: "Arduino Mega", vals: [5], def: 5 },
  esp8266:    { prefix: "E8", ar: "ESP8266", en: "ESP8266", vals: [3.3], def: 3.3 },
  pico:       { prefix: "PI", ar: "باي بيكو", en: "Raspberry Pi Pico", vals: [3.3], def: 3.3 },
  solar:      { prefix: "SL", ar: "خلية شمسية", en: "Solar Cell", vals: [6, 9, 12], def: 9 },
  dc_jack:    { prefix: "DC", ar: "مصدر خارجي", en: "DC Jack", vals: [5, 9, 12, 24], def: 9 },
  reg7805:    { prefix: "VR", ar: "منظم 7805", en: "7805 Regulator", vals: [5], def: 5, pins: 3 },
  reg7803:    { prefix: "VR", ar: "منظم 7803", en: "7803 Regulator", vals: [3.3], def: 3.3, pins: 3 },
  opamp:      { prefix: "OP", ar: "مكبر عملياتي", en: "Op-Amp", vals: ["LM358", "LM741"], def: "LM358", pins: 3 },
  transistor_pnp: { prefix: "QP", ar: "ترانزستور PNP", en: "PNP Transistor", vals: ["PNP"], def: "PNP", pins: 3 },
  pir:        { prefix: "PIR", ar: "حساس حركة", en: "PIR Motion", vals: [], def: 0 },
  dht11:      { prefix: "DHT", ar: "حساس حرارة", en: "DHT11 Sensor", vals: [20, 25, 30, 35], def: 25 },
  seven_seg:  { prefix: "7S", ar: "شاشة 7-segment", en: "7-Segment", vals: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], def: 0, pins: 3 },
  timer555:   { prefix: "IC", ar: "مؤقت 555", en: "Timer 555", vals: [1, 2, 10, 50], def: 1, pins: 3 },
  gate_nand:  { prefix: "U", ar: "NAND", en: "NAND Gate", vals: [], def: 0 },
  gate_xor:   { prefix: "U", ar: "XOR", en: "XOR Gate", vals: [], def: 0 },
  gate_xnor:  { prefix: "U", ar: "XNOR", en: "XNOR Gate", vals: [], def: 0 },
  mosfet_n:   { prefix: "MN", ar: "MOSFET N", en: "N-MOSFET", vals: ["IRF540", "IRLZ44"], def: "IRF540", pins: 3 },
  lm317:      { prefix: "VR", ar: "LM317", en: "LM317", vals: [1.25, 3.3, 5, 9, 12], def: 5, pins: 3 },
  servo:      { prefix: "SV", ar: "سيرفو", en: "Servo", vals: [0, 45, 90, 135, 180], def: 90, pins: 3 },
  lcd_16x2:   { prefix: "LCD", ar: "شاشة LCD", en: "LCD 16×2", vals: ["Hello", "Ready", "OK", "Error", "Zone", "Alert"], def: "Hello", pins: 3 },
  hc_sr04:    { prefix: "SR", ar: "حساس مسافة", en: "HC-SR04", vals: [10, 25, 50, 100, 200, 400], def: 100, pins: 3 },
  ds18b20:    { prefix: "TMP", ar: "حساس حرارة دقيق", en: "DS18B20", vals: [20.0, 22.5, 25.0, 30.5, 37.0, 40.0], def: 25.0, pins: 3 },
  stepper_motor: { prefix: "STP", ar: "محرك ستيبر", en: "Stepper Motor", vals: [200, 400, 800], def: 200 },
  rgb_led:    { prefix: "RGB", ar: "LED RGB", en: "RGB LED", vals: ["red", "green", "blue", "yellow", "cyan", "magenta", "white"], def: "red" },
  varistor:   { prefix: "MOV", ar: "مقاومة حماية", en: "Varistor", vals: [5, 9, 12, 18, 24], def: 12 },
  oled_ssd1306: { prefix: "OLED", ar: "شاشة OLED", en: "OLED 0.96", vals: ["Hi", "Ready", "OK", "Alert", "Menu", "Temp"], def: "Hi", pins: 3 },
  seven_seg_4: { prefix: "7S4", ar: "شاشة رقمية", en: "7-Seg 2-digit", vals: [0, 12, 25, 42, 58, 73, 88, 99], def: 0, pins: 3 },
  l293d:      { prefix: "L293", ar: "مشغل محرك", en: "L293D", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  hc595:      { prefix: "595", ar: "سجل إزاحة", en: "74HC595", vals: [1, 2, 4, 8, 16, 32, 64, 128], def: 1, pins: 3 },
  ds3231:     { prefix: "RTC", ar: "ساعة RTC", en: "DS3231", vals: [0, 6, 12, 18, 24], def: 12, pins: 3 },
  optocoupler: { prefix: "OC", ar: "عازل ضوئي", en: "Optocoupler", vals: ["4N35", "PC817", "6N137"], def: "4N35" },
  lm386:      { prefix: "AUD", ar: "مضخم صوتي", en: "LM386 Amp", vals: [20, 50, 100, 200], def: 20, pins: 3 },
  lm358:      { prefix: "OP", ar: "مضخم عملياتي مزدوج", en: "LM358 Dual Op-Amp", vals: ["LM358"], def: "LM358", pins: 3 },
  ne5532:     { prefix: "OPA", ar: "مضخم صوتي", en: "NE5532 Audio Op-Amp", vals: ["NE5532"], def: "NE5532", pins: 3 },
  lm393:      { prefix: "CMP", ar: "مقارن مزدوج", en: "LM393 Comparator", vals: ["LM393"], def: "LM393", pins: 3 },
  cd4017:     { prefix: "CNT", ar: "عداد عشري", en: "CD4017 Counter", vals: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], def: 0, pins: 3 },
  ic_74hc138: { prefix: "DEC", ar: "مفكك 3→8", en: "74HC138 Decoder", vals: [0, 1, 2, 3, 4, 5, 6, 7], def: 0, pins: 3 },
  tl072:      { prefix: "OPJ", ar: "مضخم JFET", en: "TL072 JFET Op-Amp", vals: ["TL072"], def: "TL072", pins: 3 },
  lm324:      { prefix: "OPQ", ar: "مضخم رباعي", en: "LM324 Quad Op-Amp", vals: ["LM324"], def: "LM324", pins: 3 },
  ne556:      { prefix: "TMR", ar: "مؤقت مزدوج", en: "NE556 Dual Timer", vals: [1, 2, 5, 10], def: 1, pins: 3 },
  uln2003:    { prefix: "DRV", ar: "مصفوفة دارلينجتون", en: "ULN2003 Driver", vals: ["ULN2003"], def: "ULN2003", pins: 3 },
  lm1117:     { prefix: "LDO", ar: "منظم LDO", en: "LM1117 LDO", vals: [1.2, 1.8, 2.5, 3.3, 5.0], def: 3.3, pins: 3 },
  lm3914:     { prefix: "BAR", ar: "شريط LED", en: "LM3914 Bar Driver", vals: [5, 10, 12], def: 10, pins: 3 },
  tda2030:    { prefix: "AMP", ar: "مضخم 14W", en: "TDA2030 14W Amp", vals: [10, 20, 50], def: 20, pins: 3 },
  lm2596:     { prefix: "BUK", ar: "محول Buck", en: "LM2596 Buck", vals: [1.25, 3.3, 5, 9, 12], def: 5, pins: 3 },
  tp4056:     { prefix: "CHG", ar: "شاحن بطارية", en: "TP4056 Charger", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  adc0804:    { prefix: "ADC", ar: "محول رقمي", en: "ADC0804 8-bit", vals: [1, 2, 5], def: 5, pins: 3 },
  dac0808:    { prefix: "DAC", ar: "محول تناظري", en: "DAC0808 8-bit", vals: [0, 32, 64, 128, 192, 255], def: 128, pins: 3 },
  max7219:    { prefix: "MAX", ar: "مشغل شاشة", en: "MAX7219 Display Driver", vals: [0, 12, 42, 100, 888, 9999], def: 0, pins: 3 },
  lm741:      { prefix: "OP741", ar: "مضخم كلاسيكي", en: "LM741 Op-Amp", vals: ["LM741"], def: "LM741", pins: 3 },
  ne5534:     { prefix: "OP55", ar: "مضخم صوتي", en: "NE5534 Audio Op-Amp", vals: ["NE5534"], def: "NE5534", pins: 3 },
  tda2822:    { prefix: "STAMP", ar: "مضخم ستيريو", en: "TDA2822 Stereo Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  cd4051:     { prefix: "MUX", ar: "مضاعف 8 قنوات", en: "CD4051 MUX", vals: [0, 1, 2, 3, 4, 5, 6, 7], def: 0, pins: 3 },
  pcf8574:    { prefix: "I2C", ar: "موسع منافذ", en: "PCF8574 I2C", vals: [0, 1, 15, 85, 170, 255], def: 0, pins: 3 },
  cd4066:     { prefix: "SW", ar: "مفتاح تناظري", en: "CD4066 Quad Switch", vals: ["open", "closed"], def: "open", pins: 3 },
  tda7297:    { prefix: "AMP7", ar: "مضخم ستيريو 15W", en: "TDA7297 Stereo 15W", vals: [5, 10, 15], def: 10, pins: 3 },
  opa2134:    { prefix: "OPA2", ar: "مضخم استوديو", en: "OPA2134 Studio Op-Amp", vals: ["OPA2134"], def: "OPA2134", pins: 3 },
  ad620:      { prefix: "INST", ar: "مضخم قياس", en: "AD620 Instrumentation", vals: [1, 10, 100, 1000], def: 100, pins: 3 },
  opa548:     { prefix: "PWR", ar: "مضخم قدرة", en: "OPA548 Power Op-Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  lm337:      { prefix: "VRN", ar: "منظم سالب", en: "LM337 Negative Reg", vals: [-1.25, -3.3, -5, -9, -12], def: -5, pins: 3 },
  cd4013:     { prefix: "FF", ar: "D Flip-Flop", en: "CD4013 D Flip-Flop", vals: [0, 1], def: 0, pins: 3 },
  cd4015:     { prefix: "SHR", ar: "سجل إزاحة", en: "CD4015 Shift Register", vals: [0, 1, 3, 7, 15], def: 0, pins: 3 },
  ic_74hc273: { prefix: "LATCH", ar: "Octal FF", en: "74HC273 Octal FF", vals: [0, 1, 15, 85, 170, 255], def: 0, pins: 3 },
  ic_74hc373: { prefix: "TRL", ar: "Octal Latch", en: "74HC373 Transparent Latch", vals: [0, 1, 15, 85, 170, 255], def: 0, pins: 3 },
  at24c32:    { prefix: "EEP", ar: "EEPROM", en: "AT24C32 EEPROM", vals: [0, 16, 64, 128, 255], def: 0, pins: 3 },
  mcp23017:   { prefix: "EXP", ar: "موسع منافذ", en: "MCP23017 I2C Expander", vals: [0, 255, 65535], def: 0, pins: 3 },
  ic_74hc00:  { prefix: "NQ", ar: "NAND رباعي", en: "74HC00 Quad NAND", vals: ["74HC00"], def: "74HC00", pins: 3 },
  mpu6050:    { prefix: "IMU",  ar: "حساس حركة 6 محاور", en: "MPU6050 6-axis",      vals: ["flat", "tilt", "shake", "rotated"], def: "flat", pins: 3 },
  bmp280:     { prefix: "BARO", ar: "حساس ضغط جوي",       en: "BMP280 Pressure",    vals: [1013, 900, 800, 700, 500], def: 1013, pins: 3 },
  acs712:     { prefix: "CUR",  ar: "حساس تيار",          en: "ACS712 Current",     vals: [5, 10, 20, 30], def: 5, pins: 3 },
  a3144:      { prefix: "HALL", ar: "حساس هول مغناطيسي",  en: "A3144 Hall",         vals: [], def: 0, pins: 3 },
  ky038:      { prefix: "SND",  ar: "حساس صوت",           en: "KY-038 Sound",       vals: [0, 1, 2], def: 1, pins: 3 },
  yl69:       { prefix: "SOIL", ar: "حساس رطوبة تربة",    en: "YL-69 Soil",         vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  ttp223:     { prefix: "TCH",  ar: "حساس لمس سعوي",      en: "TTP223 Touch",       vals: [], def: 0, pins: 3 },
  ky040:      { prefix: "ENC",  ar: "مشفّر دوّار",        en: "KY-040 Encoder",     vals: [0, 45, 90, 180, 270], def: 0, pins: 3 },
  ws2812:     { prefix: "NEO",  ar: "LED عنواني RGB",     en: "WS2812 NeoPixel",    vals: ["red", "green", "blue", "yellow", "cyan", "magenta", "white"], def: "red", pins: 3 },
  tsop:       { prefix: "IR",   ar: "مستقبل IR",          en: "TSOP IR Receiver",   vals: [], def: 0, pins: 3 },
  hc05:       { prefix: "BT",   ar: "بلوتوث HC-05",       en: "HC-05 Bluetooth",    vals: ["ON", "OFF", "PAIR"], def: "ON", pins: 3 },
  l298n:      { prefix: "L298", ar: "مشغل محرك مزدوج",    en: "L298N Dual H-Bridge", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  a4988:      { prefix: "A498", ar: "مشغل ستيبر", en: "A4988 Stepper Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  pam8403:    { prefix: "PAM", ar: "مضخم صوتي 3W", en: "PAM8403 3W Stereo Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  max98357:   { prefix: "I2S", ar: "مضخم I2S", en: "MAX98357A I2S Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  ads1115:    { prefix: "AD16", ar: "محول رقمي 16-bit", en: "ADS1115 16-bit ADC", vals: [0, 1000, 2048, 3000, 4095], def: 2048, pins: 3 },
  mcp4725:    { prefix: "DA12", ar: "محول تناظري 12-bit", en: "MCP4725 12-bit DAC", vals: [0, 1000, 2048, 3000, 4095], def: 2048, pins: 3 },
  ina219:     { prefix: "INA", ar: "حساس تيار I2C", en: "INA219 I2C Current", vals: [0, 100, 500, 1000, 2000], def: 500, pins: 3 },
  mq2:        { prefix: "MQ2", ar: "حساس غاز", en: "MQ-2 Gas Sensor", vals: [0, 100, 300, 500, 1023], def: 200, pins: 3 },
  bh1750:     { prefix: "LUX", ar: "حساس إضاءة I2C", en: "BH1750 Light Sensor", vals: [0, 100, 1000, 10000, 65535], def: 1000, pins: 3 },
  vl53l0x:    { prefix: "TOF", ar: "حساس مسافة ليزر", en: "VL53L0X ToF Laser", vals: [50, 100, 200, 500, 1000, 2000], def: 200, pins: 3 },
  ic_74hc165: { prefix: "PISO", ar: "سجل إزاحة PISO", en: "74HC165 PISO Register", vals: [0, 1, 15, 85, 170, 255], def: 0, pins: 3 },
  nrf24l01:   { prefix: "RF24", ar: "لاسلكي 2.4GHz", en: "NRF24L01 Radio", vals: ["OFF", "RX", "TX", "SLEEP"], def: "RX", pins: 3 },
  sim800l:    { prefix: "GSM", ar: "وحدة GSM", en: "SIM800L GSM Module", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  drv8825:    { prefix: "DRV8", ar: "مشغل ستيبر قوي", en: "DRV8825 Stepper", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tb6612:     { prefix: "TB66", ar: "مشغل محرك مزدوج", en: "TB6612FNG Dual Motor", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  bts7960:    { prefix: "BTS", ar: "جسر H عالي القدرة", en: "BTS7960 High-Power Bridge", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tcs34725:   { prefix: "CLR", ar: "حساس لون RGB", en: "TCS34725 Color Sensor", vals: ["red", "green", "blue", "white", "clear"], def: "red", pins: 3 },
  mlx90614:   { prefix: "IRTH", ar: "ميزان حرارة IR", en: "MLX90614 IR Thermometer", vals: [20.0, 25.0, 30.0, 37.0, 40.0, 100.0], def: 25.0, pins: 3 },
  max30102:   { prefix: "HR", ar: "حساس نبض وأكسجين", en: "MAX30102 HR/SpO2", vals: [60, 75, 90, 120], def: 75, pins: 3 },
  adxl345:    { prefix: "ACC", ar: "مقياس تسارع 3 محاور", en: "ADXL345 3-axis Accel", vals: ["flat", "tilt", "shake", "freefall"], def: "flat", pins: 3 },
  hx711:      { prefix: "LOAD", ar: "مضخم خلية حمل", en: "HX711 Load Cell Amp", vals: [0, 100, 500, 1000, 5000, 20000], def: 500, pins: 3 },
  dht22:      { prefix: "DHT22", ar: "حساس حرارة ورطوبة دقيق", en: "DHT22 Temp/Humidity", vals: [20, 25, 30, 35, 40], def: 25, pins: 3 },
  sgp30:      { prefix: "AQ", ar: "حساس جودة هواء", en: "SGP30 Air Quality", vals: [400, 800, 1200, 2000, 5000], def: 800, pins: 3 },
  rc522:      { prefix: "RFID", ar: "قارئ RFID", en: "RC522 RFID Reader", vals: ["OFF", "IDLE", "CARD"], def: "IDLE", pins: 3 },
  bme680:     { prefix: "BME", ar: "حساس بيئي متكامل", en: "BME680 Environmental", vals: [25, 50, 100, 150, 250, 400], def: 100, pins: 3 },
  pca9685:    { prefix: "PWM", ar: "مشغل PWM 16 قناة", en: "PCA9685 16-ch PWM", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  tca9548a:   { prefix: "MUX8", ar: "مضاعف I2C", en: "TCA9548A I2C Mux", vals: [0, 1, 2, 3, 4, 5, 6, 7], def: 0, pins: 3 },
  l9110s:     { prefix: "L911", ar: "مشغل محرك صغير", en: "L9110S Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmp36:      { prefix: "T36", ar: "حساس حرارة تناظري", en: "TMP36 Analog Temp", vals: [0, 25, 50, 75, 100], def: 25, pins: 3 },
  am2320:     { prefix: "AM23", ar: "حساس حرارة ورطوبة", en: "AM2320 Temp/Humidity", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  ds1307:     { prefix: "RTC07", ar: "ساعة RTC كلاسيكية", en: "DS1307 RTC", vals: [0, 6, 12, 18, 24], def: 12, pins: 3 },
  pcf8563:    { prefix: "RTC56", ar: "ساعة RTC دقيقة", en: "PCF8563 RTC", vals: [0, 6, 12, 18, 24], def: 12, pins: 3 },
  st7735:     { prefix: "TFT", ar: "شاشة TFT ملونة", en: "ST7735 TFT 1.8\"", vals: ["Hello", "Ready", "OK", "Error", "Menu", "TFT"], def: "Ready", pins: 3 },
  ssd1351:    { prefix: "COLED", ar: "شاشة OLED ملونة", en: "SSD1351 Color OLED", vals: ["Hello", "Ready", "OK", "Error", "Menu", "OLED"], def: "Ready", pins: 3 },
  bmp180:     { prefix: "BARO18", ar: "حساس ضغط كلاسيكي", en: "BMP180 Pressure", vals: [1013, 900, 800, 700, 500], def: 1013, pins: 3 },
  sht31:      { prefix: "SHT", ar: "حساس حرارة ورطوبة دقيق", en: "SHT31 High-Precision", vals: [20, 25, 30, 35, 40, 50], def: 25, pins: 3 },
  apds9960:   { prefix: "GEST", ar: "حساس إيماءات ولون", en: "APDS-9960 Gesture", vals: ["UP", "DOWN", "LEFT", "RIGHT", "NEAR", "FAR", "NONE"], def: "NONE", pins: 3 },
  ds1302:     { prefix: "RTC02", ar: "ساعة RTC بسيطة", en: "DS1302 RTC", vals: [0, 6, 12, 18, 24], def: 12, pins: 3 },
  max6675:    { prefix: "THRM7", ar: "مضخم ثيرموكوبل", en: "MAX6675 Thermocouple", vals: [0, 100, 300, 500, 800, 1024], def: 300, pins: 3 },
  max31855:   { prefix: "THRM3", ar: "ثيرموكوبل دقيق", en: "MAX31855 Thermocouple", vals: [0, 100, 500, 1000, 1500, 2000], def: 500, pins: 3 },
  sd_card:    { prefix: "SD", ar: "قارئ بطاقة SD", en: "microSD Card Module", vals: ["OFF", "IDLE", "READ", "WRITE"], def: "IDLE", pins: 3 },
  enc28j60:   { prefix: "ETH", ar: "إيثرنت ENC28J60", en: "ENC28J60 Ethernet", vals: ["OFF", "IDLE", "RX", "TX"], def: "IDLE", pins: 3 },
  uln2803:    { prefix: "DRV8", ar: "مصفوفة دارلينجتون 8", en: "ULN2803 8-ch Driver", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  tlc5940:    { prefix: "LED16", ar: "مشغل LED 16 قناة", en: "TLC5940 16-ch LED", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  mpu9250:    { prefix: "IMU9", ar: "حساس 9 محاور", en: "MPU9250 9-axis IMU", vals: ["flat", "tilt", "shake", "rotated"], def: "flat", pins: 3 },
  ad9833:     { prefix: "DDS", ar: "مولد إشارة DDS", en: "AD9833 DDS Generator", vals: [100, 1000, 10000, 100000, 1000000], def: 1000, pins: 3 },
  ams1117:    { prefix: "LDO17", ar: "منظم LDO 3.3V", en: "AMS1117 LDO", vals: [1.8, 2.5, 3.3, 5.0], def: 3.3, pins: 3 },
  xl6009:     { prefix: "BOOST", ar: "محول رافع XL6009", en: "XL6009 Boost", vals: [5, 9, 12, 18, 24], def: 12, pins: 3 },
  vl6180x:    { prefix: "PROX", ar: "حساس اقتراب ليزر", en: "VL6180X Proximity", vals: [20, 50, 100, 200, 400], def: 100, pins: 3 },
  sht10: { prefix: "SHT10", ar: "SHT10 حرارة", en: "SHT10 Temp", vals: [20, 25, 30, 35, 40], def: 25, pins: 3 },
  sht75: { prefix: "SHT75", ar: "SHT75 حرارة", en: "SHT75 Temp", vals: [20, 25, 30, 35, 40], def: 25, pins: 3 },
  si7021: { prefix: "SI7021", ar: "Si7021 رطوبة", en: "Si7021 Humidity", vals: [20, 40, 60, 80, 100], def: 60, pins: 3 },
  bme280: { prefix: "BME280", ar: "BME280 بيئي", en: "BME280 Env", vals: [1013, 900, 800, 700, 500], def: 1013, pins: 3 },
  mpl3115a2: { prefix: "MPL3115", ar: "MPL3115A2 ارتفاع", en: "MPL3115A2 Alt", vals: [0, 100, 500, 1000, 2000], def: 100, pins: 3 },
  mq3: { prefix: "MQ3", ar: "MQ-3 كحول", en: "MQ-3 Alcohol", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  mq4: { prefix: "MQ4", ar: "MQ-4 ميثان", en: "MQ-4 Methane", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  mq5: { prefix: "MQ5", ar: "MQ-5 غاز بترول", en: "MQ-5 LPG", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  mq6: { prefix: "MQ6", ar: "MQ-6 بروبان", en: "MQ-6 Propane", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  mq7: { prefix: "MQ7", ar: "MQ-7 أول أكسيد", en: "MQ-7 CO", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  mq8: { prefix: "MQ8", ar: "MQ-8 هيدروجين", en: "MQ-8 Hydrogen", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  mq9: { prefix: "MQ9", ar: "MQ-9 غاز مشتعل", en: "MQ-9 Flammable", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  mq135: { prefix: "MQ135", ar: "MQ-135 جودة هواء", en: "MQ-135 Air Quality", vals: [0, 100, 200, 500, 1000], def: 200, pins: 3 },
  gp2y1010: { prefix: "DUST", ar: "GP2Y1010 غبار", en: "GP2Y1010 Dust", vals: [0, 50, 100, 200, 500, 1000], def: 100, pins: 3 },
  tsl2561: { prefix: "TSL", ar: "TSL2561 إضاءة", en: "TSL2561 Light", vals: [0, 100, 1000, 10000, 65535], def: 1000, pins: 3 },
  tcs3200: { prefix: "CLR2", ar: "TCS3200 لون", en: "TCS3200 Color", vals: ['red', 'green', 'blue', 'clear'], def: 'red', pins: 3 },
  reed_switch: { prefix: "REED", ar: "مفتاح مغناطيسي", en: "Reed Switch", vals: [], def: 0, pins: 3 },
  vibration_sensor: { prefix: "VIB", ar: "حساس اهتزاز", en: "Vibration", vals: [], def: 0, pins: 3 },
  water_level: { prefix: "WLVL", ar: "حساس مستوى ماء", en: "Water Level", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  flex_sensor: { prefix: "FLEX", ar: "حساس انثناء", en: "Flex Sensor", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  tilt_switch: { prefix: "TILT", ar: "مفتاح ميل", en: "Tilt Switch", vals: [], def: 0, pins: 3 },
  shock_sensor: { prefix: "SHOCK", ar: "حساس صدمة", en: "Shock Sensor", vals: [], def: 0, pins: 3 },
  flame_sensor: { prefix: "FLAME", ar: "حساس لهب", en: "Flame Sensor", vals: [0, 100, 300, 500, 1023], def: 300, pins: 3 },
  rain_sensor: { prefix: "RAIN", ar: "حساس مطر", en: "Rain Sensor", vals: [0, 25, 50, 75, 100], def: 25, pins: 3 },
  hall_linear: { prefix: "HALLL", ar: "حساس هول خطي", en: "Hall Linear", vals: [0, 100, 500, 1000, 4095], def: 500, pins: 3 },
  cd4071: { prefix: "OR4", ar: "CD4071 OR×4", en: "CD4071 Quad OR", vals: ['CD4071'], def: 'CD4071', pins: 3 },
  cd4081: { prefix: "AND4", ar: "CD4081 AND×4", en: "CD4081 Quad AND", vals: ['CD4081'], def: 'CD4081', pins: 3 },
  cd4030: { prefix: "XOR4", ar: "CD4030 XOR×4", en: "CD4030 Quad XOR", vals: ['CD4030'], def: 'CD4030', pins: 3 },
  cd4001: { prefix: "NOR4", ar: "CD4001 NOR×4", en: "CD4001 Quad NOR", vals: ['CD4001'], def: 'CD4001', pins: 3 },
  cd4023: { prefix: "NAND3", ar: "CD4023 NAND×3", en: "CD4023 Triple NAND", vals: ['CD4023'], def: 'CD4023', pins: 3 },
  cd4025: { prefix: "NOR3", ar: "CD4025 NOR×3", en: "CD4025 Triple NOR", vals: ['CD4025'], def: 'CD4025', pins: 3 },
  cd4070: { prefix: "XOR4B", ar: "CD4070 XOR×4", en: "CD4070 Quad XOR", vals: ['CD4070'], def: 'CD4070', pins: 3 },
  cd4075: { prefix: "OR3", ar: "CD4075 OR×3", en: "CD4075 Triple OR", vals: ['CD4075'], def: 'CD4075', pins: 3 },
  cd4077: { prefix: "XNOR4", ar: "CD4077 XNOR×4", en: "CD4077 Quad XNOR", vals: ['CD4077'], def: 'CD4077', pins: 3 },
  cd4093: { prefix: "NSCH", ar: "CD4093 NAND شميت", en: "CD4093 NAND Schmitt", vals: ['CD4093'], def: 'CD4093', pins: 3 },
  cd4538: { prefix: "MONO2", ar: "CD4538 أحادي×2", en: "CD4538 Dual Mono", vals: ['CD4538'], def: 'CD4538', pins: 3 },
  cd4047: { prefix: "ASTAB", ar: "CD4047 متعدد الاهتزاز", en: "CD4047 Astable", vals: ['CD4047'], def: 'CD4047', pins: 3 },
  cd4027: { prefix: "JK2", ar: "CD4027 JK×2", en: "CD4027 Dual JK", vals: ['CD4027'], def: 'CD4027', pins: 3 },
  cd4029: { prefix: "CNT29", ar: "CD4029 عداد صعود/هبوط", en: "CD4029 Up/Down", vals: ['CD4029'], def: 'CD4029', pins: 3 },
  cd4076: { prefix: "REG4", ar: "CD4076 سجل D×4", en: "CD4076 Quad D Reg", vals: ['CD4076'], def: 'CD4076', pins: 3 },
  cd4022: { prefix: "CNT22", ar: "CD4022 عداد ثماني", en: "CD4022 Octal Counter", vals: ['CD4022'], def: 'CD4022', pins: 3 },
  cd4060: { prefix: "CNT60", ar: "CD4060 عداد 14 مرحلة", en: "CD4060 14-stage", vals: ['CD4060'], def: 'CD4060', pins: 3 },
  cd4541: { prefix: "TIM41", ar: "CD4541 مؤقت مبرمج", en: "CD4541 Timer", vals: ['CD4541'], def: 'CD4541', pins: 3 },
  cd4511: { prefix: "BCD7S", ar: "CD4511 BCD→7seg", en: "CD4511 BCD→7seg", vals: ['CD4511'], def: 'CD4511', pins: 3 },
  cd4028: { prefix: "BCD10", ar: "CD4028 BCD→عشري", en: "CD4028 BCD→Decimal", vals: ['CD4028'], def: 'CD4028', pins: 3 },
  mcp3008: { prefix: "A10", ar: "MCP3008 ADC 8ch", en: "MCP3008 ADC", vals: [0, 512, 1023], def: 512, pins: 3 },
  mcp3208: { prefix: "A12", ar: "MCP3208 ADC 12b", en: "MCP3208 ADC", vals: [0, 2048, 4095], def: 2048, pins: 3 },
  ads1015: { prefix: "ADS1", ar: "ADS1015 ADC 4ch", en: "ADS1015 ADC", vals: [0, 2048, 4095], def: 2048, pins: 3 },
  pcf8591: { prefix: "PCF", ar: "PCF8591 ADC/DAC", en: "PCF8591 ADC/DAC", vals: [0, 128, 255], def: 128, pins: 3 },
  tlc5615: { prefix: "DA10", ar: "TLC5615 DAC 10b", en: "TLC5615 DAC", vals: [0, 512, 1023], def: 512, pins: 3 },
  mcp4921: { prefix: "DA4921", ar: "MCP4921 DAC 12b", en: "MCP4921 DAC", vals: [0, 2048, 4095], def: 2048, pins: 3 },
  at24c256: { prefix: "E256", ar: "AT24C256 EEPROM", en: "AT24C256 EEPROM", vals: [0, 128, 255], def: 128, pins: 3 },
  at24c512: { prefix: "E512", ar: "AT24C512 EEPROM", en: "AT24C512 EEPROM", vals: [0, 128, 255], def: 128, pins: 3 },
  w25q64: { prefix: "FLASH", ar: "W25Q64 SPI Flash", en: "W25Q64 SPI Flash", vals: [0, 64, 128, 255], def: 64, pins: 3 },
  mb85rc: { prefix: "FRAM", ar: "MB85RC FRAM", en: "MB85RC FRAM", vals: [0, 128, 255], def: 128, pins: 3 },
  ds3234: { prefix: "RTC34", ar: "DS3234 RTC SPI", en: "DS3234 RTC", vals: [0, 6, 12, 18, 24], def: 12, pins: 3 },
  rv3028: { prefix: "RTC28", ar: "RV-3028 RTC", en: "RV-3028 RTC", vals: [0, 6, 12, 18, 24], def: 12, pins: 3 },
  mcp7940: { prefix: "RTC40", ar: "MCP7940 RTC", en: "MCP7940 RTC", vals: [0, 6, 12, 18, 24], def: 12, pins: 3 },
  nokia5110: { prefix: "LCD51", ar: "Nokia 5110", en: "Nokia 5110 LCD", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  ssd1309: { prefix: "OL9", ar: "SSD1309 OLED", en: "SSD1309 OLED 128x64", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  st7565: { prefix: "LCD56", ar: "ST7565 LCD", en: "ST7565 LCD 128x64", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  st7920: { prefix: "LCD79", ar: "ST7920 LCD", en: "ST7920 LCD 128x64", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  ili9341: { prefix: "TFT93", ar: "ILI9341 TFT", en: "ILI9341 TFT 240x320", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  ili9486: { prefix: "TFT94", ar: "ILI9486 TFT", en: "ILI9486 TFT 320x480", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  max6954: { prefix: "LED69", ar: "MAX6954 LED", en: "MAX6954 LED Driver", vals: [0, 4, 8, 16], def: 8, pins: 3 },
  lcd_20x4: { prefix: "LCD20", ar: "LCD 20×4", en: "LCD 20x4", vals: ['Hello', 'Ready', 'OK', 'Menu'], def: 'Hello', pins: 3 },
  st7735_160: { prefix: "TFT160", ar: "ST7735 TFT 1.8\"", en: "ST7735 TFT 160x128", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  ssd1331: { prefix: "OL96", ar: "SSD1331 OLED", en: "SSD1331 OLED 96x64", vals: ['Hi', 'OK', 'Menu', 'Err'], def: 'Hi', pins: 3 },
  drv8833: { prefix: "DRV33", ar: "DRV8833 محرك", en: "DRV8833 Dual", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  drv8871: { prefix: "DRV71", ar: "DRV8871 محرك", en: "DRV8871 H-Bridge", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  l293e: { prefix: "L293E", ar: "L293E محرك", en: "L293E Quad", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  sn754410: { prefix: "SN41", ar: "SN754410 محرك", en: "SN754410 Quad", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  uln2004: { prefix: "ULN04", ar: "ULN2004 دارلينجتون", en: "ULN2004 Darlington", vals: [0, 1, 2, 4], def: 1, pins: 3 },
  mc33926: { prefix: "MC26", ar: "MC33926 محرك", en: "MC33926 H-Bridge", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  bd6221: { prefix: "BD62", ar: "BD6221 محرك 3A", en: "BD6221 3A Driver", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  tb67h420: { prefix: "TB67", ar: "TB67H420 محرك", en: "TB67H420 Dual", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  a3959: { prefix: "A3959", ar: "A3959 محرك", en: "A3959 H-Bridge", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  drv8824: { prefix: "DRV24", ar: "DRV8824 ستيبر", en: "DRV8824 Stepper", vals: ['FWD', 'REV', 'STOP'], def: 'FWD', pins: 3 },
  esp01: { prefix: "ESP1", ar: "ESP-01 واي فاي", en: "ESP-01 WiFi", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  rn2483: { prefix: "LORA", ar: "RN2483 LoRa", en: "RN2483 LoRa", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  rfm69: { prefix: "RF69", ar: "RFM69 لاسلكي", en: "RFM69 Radio", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  rfm95: { prefix: "RF95", ar: "RFM95 LoRa", en: "RFM95 LoRa", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  hc12: { prefix: "HC12", ar: "HC-12 بعيد المدى", en: "HC-12 Long Range", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  xbee: { prefix: "XBEE", ar: "XBee لاسلكي", en: "XBee Radio", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  sim900: { prefix: "GSM90", ar: "SIM900 GSM", en: "SIM900 GSM", vals: ['OFF', 'REG', 'ERR'], def: 'REG', pins: 3 },
  m95: { prefix: "M95", ar: "M95 GSM", en: "M95 GSM", vals: ['OFF', 'REG', 'ERR'], def: 'REG', pins: 3 },
  nrf905: { prefix: "RF905", ar: "NRF905 لاسلكي", en: "NRF905 Radio", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  cc1101: { prefix: "CC11", ar: "CC1101 sub-GHz", en: "CC1101 sub-GHz", vals: ['OFF', 'IDLE', 'TX', 'RX'], def: 'IDLE', pins: 3 },
  lm7809: { prefix: "VR09", ar: "منظم 7809", en: "7809 Regulator", vals: [9], def: 9, pins: 3 },
  lm7812: { prefix: "VR12", ar: "منظم 7812", en: "7812 Regulator", vals: [12], def: 12, pins: 3 },
  lm7905: { prefix: "VR-5", ar: "منظم 7905 سالب", en: "7905 -5V Reg", vals: [-5], def: -5, pins: 3 },
  lm7912: { prefix: "VR-12", ar: "منظم 7912 سالب", en: "7912 -12V Reg", vals: [-12], def: -12, pins: 3 },
  lm1084: { prefix: "LDO84", ar: "LM1084 LDO 5A", en: "LM1084 LDO 5A", vals: [1.5, 3.3, 5], def: 5, pins: 3 },
  lm2678: { prefix: "BUK78", ar: "LM2678 Buck 5A", en: "LM2678 Buck 5A", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm5007: { prefix: "BUK07", ar: "LM5007 Buck", en: "LM5007 Buck", vals: [5, 12, 24], def: 12, pins: 3 },
  mcp1700: { prefix: "LDO17", ar: "MCP1700 LDO", en: "MCP1700 LDO", vals: [1.8, 2.5, 3.3], def: 3.3, pins: 3 },
  mic5205: { prefix: "LDO05", ar: "MIC5205 LDO", en: "MIC5205 LDO", vals: [1.8, 3.0, 3.3, 5], def: 3.3, pins: 3 },
  lp2985: { prefix: "LDO85", ar: "LP2985 LDO", en: "LP2985 LDO", vals: [2.5, 3.0, 3.3, 5], def: 3.3, pins: 3 },
  lm4871: { prefix: "AUD81", ar: "LM4871 مضخم", en: "LM4871 Amp", vals: [1, 2, 3], def: 1, pins: 3 },
  tda2003: { prefix: "AMP03", ar: "TDA2003 مضخم 10W", en: "TDA2003 10W Amp", vals: [1, 5, 10], def: 5, pins: 3 },
  ds18s20: { prefix: "SNS20", ar: "DS18S20 حرارة", en: "DS18S20 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  lm35: { prefix: "SNS35", ar: "LM35 حرارة", en: "LM35 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  lm75: { prefix: "SNS75", ar: "LM75 حرارة I2C", en: "LM75 I2C Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  tmp102: { prefix: "SNS02", ar: "TMP102 حرارة", en: "TMP102 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  mcp9808: { prefix: "SNS08", ar: "MCP9808 حرارة", en: "MCP9808 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  max31865: { prefix: "SNS65", ar: "MAX31865 PT100", en: "MAX31865 PT100", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  ads1118: { prefix: "SNS18", ar: "ADS1118 حرارة", en: "ADS1118 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  hdc1080: { prefix: "HUM80", ar: "HDC1080 رطوبة", en: "HDC1080 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  htu21d: { prefix: "HUM21", ar: "HTU21D رطوبة", en: "HTU21D Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  sht21: { prefix: "HUM22", ar: "SHT21 رطوبة", en: "SHT21 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  sht35: { prefix: "HUM35", ar: "SHT35 رطوبة", en: "SHT35 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  aht10: { prefix: "HUM10", ar: "AHT10 رطوبة", en: "AHT10 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  aht20: { prefix: "HUM20", ar: "AHT20 رطوبة", en: "AHT20 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  ms5611: { prefix: "PRS61", ar: "MS5611 ضغط", en: "MS5611 Pressure", vals: [300, 700, 1000, 1100], def: 1000, pins: 3 },
  lps25h: { prefix: "PRS25", ar: "LPS25H ضغط", en: "LPS25H Pressure", vals: [300, 700, 1000, 1100], def: 1000, pins: 3 },
  bmp388: { prefix: "PRS88", ar: "BMP388 ضغط", en: "BMP388 Pressure", vals: [300, 700, 1000, 1100], def: 1000, pins: 3 },
  dps310: { prefix: "PRS31", ar: "DPS310 ضغط", en: "DPS310 Pressure", vals: [300, 700, 1000, 1100], def: 1000, pins: 3 },
  bmp085: { prefix: "PRS85", ar: "BMP085 ضغط", en: "BMP085 Pressure", vals: [300, 700, 1000, 1100], def: 1000, pins: 3 },
  lps22hb: { prefix: "PRS22", ar: "LPS22HB ضغط", en: "LPS22HB Pressure", vals: [300, 700, 1000, 1100], def: 1000, pins: 3 },
  mpx5700: { prefix: "PRS57", ar: "MPX5700 ضغط", en: "MPX5700 Pressure", vals: [300, 700, 1000, 1100], def: 1000, pins: 3 },
  mq131: { prefix: "GAS31", ar: "MQ131 أوزون", en: "MQ131 Ozone", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mq303: { prefix: "GAS03", ar: "MQ303 كحول", en: "MQ303 Alcohol", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mhz19: { prefix: "CO2_9", ar: "MH-Z19 CO2", en: "MH-Z19 CO2", vals: [400, 800, 1500, 3000, 5000], def: 800, pins: 3 },
  sds011: { prefix: "PM011", ar: "SDS011 غبار", en: "SDS011 Dust", vals: [0, 25, 50, 150, 500], def: 25, pins: 3 },
  pms5003: { prefix: "PM503", ar: "PMS5003 غبار", en: "PMS5003 Dust", vals: [0, 25, 50, 150, 500], def: 25, pins: 3 },
  ccs811: { prefix: "CCS11", ar: "CCS811 جودة هواء", en: "CCS811 Air Quality", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  ens160: { prefix: "ENS60", ar: "ENS160 جودة هواء", en: "ENS160 Air Quality", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  si1145: { prefix: "LUX45", ar: "Si1145 ضوء", en: "Si1145 Light", vals: [0, 100, 1000, 10000, 50000], def: 1000, pins: 3 },
  veml7700: { prefix: "LUX77", ar: "VEML7700 ضوء", en: "VEML7700 Light", vals: [0, 100, 1000, 10000, 50000], def: 1000, pins: 3 },
  opt3001: { prefix: "LUX01", ar: "OPT3001 ضوء", en: "OPT3001 Light", vals: [0, 100, 1000, 10000, 50000], def: 1000, pins: 3 },
  max44009: { prefix: "LUX09", ar: "MAX44009 ضوء", en: "MAX44009 Light", vals: [0, 100, 1000, 10000, 50000], def: 1000, pins: 3 },
  ltr329: { prefix: "LUX29", ar: "LTR-329 ضوء", en: "LTR-329 Light", vals: [0, 100, 1000, 10000, 50000], def: 1000, pins: 3 },
  ml8511: { prefix: "UV851", ar: "ML8511 أشعة UV", en: "ML8511 UV", vals: [0, 2, 5, 8, 11], def: 2, pins: 3 },
  veml6070: { prefix: "UV607", ar: "VEML6070 أشعة UV", en: "VEML6070 UV", vals: [0, 2, 5, 8, 11], def: 2, pins: 3 },
  ina226: { prefix: "PWR26", ar: "INA226 جهد/تيار", en: "INA226 Power Mon", vals: [0, 3.3, 5, 12, 24], def: 5, pins: 3 },
  ina260: { prefix: "PWR60", ar: "INA260 جهد/تيار", en: "INA260 Power Mon", vals: [0, 3.3, 5, 12, 24], def: 5, pins: 3 },
  ina3221: { prefix: "PWR21", ar: "INA3221 3 قنوات", en: "INA3221 3-Ch Mon", vals: [0, 3.3, 5, 12, 24], def: 5, pins: 3 },
  lis3dh: { prefix: "ACC3D", ar: "LIS3DH تسارع", en: "LIS3DH Accel", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  mma8452: { prefix: "ACC52", ar: "MMA8452 تسارع", en: "MMA8452 Accel", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  adxl335: { prefix: "ACC35", ar: "ADXL335 تسارع", en: "ADXL335 Accel", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  adxl362: { prefix: "ACC62", ar: "ADXL362 تسارع", en: "ADXL362 Accel", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  lsm6ds3: { prefix: "IMU63", ar: "LSM6DS3 IMU", en: "LSM6DS3 IMU", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  icm20948: { prefix: "IMU48", ar: "ICM-20948 IMU", en: "ICM-20948 IMU", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  bno055: { prefix: "IMU55", ar: "BNO055 اتجاه", en: "BNO055 Orientation", vals: [0, 1, 2, 4, 8], def: 1, pins: 3 },
  hmc5883l: { prefix: "MAG83", ar: "HMC5883L بوصلة", en: "HMC5883L Compass", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  qmc5883l: { prefix: "MAG88", ar: "QMC5883L بوصلة", en: "QMC5883L Compass", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  mlx90393: { prefix: "MAG93", ar: "MLX90393 مغناطيس", en: "MLX90393 Magnetometer", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  lm7815: { prefix: "LDO15", ar: "LM7815 منظم 15V", en: "LM7815 15V Reg", vals: [15], def: 15, pins: 3 },
  lm7824: { prefix: "LDO24", ar: "LM7824 منظم 24V", en: "LM7824 24V Reg", vals: [24], def: 24, pins: 3 },
  lm7808: { prefix: "LDO08", ar: "LM7808 منظم 8V", en: "LM7808 8V Reg", vals: [8], def: 8, pins: 3 },
  lm7806: { prefix: "LDO06", ar: "LM7806 منظم 6V", en: "LM7806 6V Reg", vals: [6], def: 6, pins: 3 },
  lm317hv: { prefix: "LDOHV", ar: "LM317HV منظم", en: "LM317HV Reg", vals: [5, 12, 24, 40], def: 12, pins: 3 },
  lm2940: { prefix: "LDO40", ar: "LM2940 LDO", en: "LM2940 LDO", vals: [5, 8, 10], def: 5, pins: 3 },
  tps7a47: { prefix: "LDO47", ar: "TPS7A47 LDO", en: "TPS7A47 LDO", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  lm2576: { prefix: "BUK76", ar: "LM2576 Buck 3A", en: "LM2576 Buck 3A", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm2574: { prefix: "BUK74", ar: "LM2574 Buck 0.5A", en: "LM2574 Buck 0.5A", vals: [3.3, 5, 12], def: 5, pins: 3 },
  mp1584: { prefix: "BUK84", ar: "MP1584 Buck 3A", en: "MP1584 Buck 3A", vals: [3.3, 5, 12], def: 5, pins: 3 },
  tps5430: { prefix: "BUK30", ar: "TPS5430 Buck 3A", en: "TPS5430 Buck 3A", vals: [3.3, 5, 12], def: 5, pins: 3 },
  mt3608: { prefix: "BST08", ar: "MT3608 Boost", en: "MT3608 Boost", vals: [5, 9, 12, 24], def: 12, pins: 3 },
  lm2577: { prefix: "BST77", ar: "LM2577 Boost", en: "LM2577 Boost", vals: [12, 15, 24], def: 12, pins: 3 },
  tps61023: { prefix: "BST23", ar: "TPS61023 Boost", en: "TPS61023 Boost", vals: [3.3, 5], def: 5, pins: 3 },
  max1771: { prefix: "BST71", ar: "MAX1771 Boost", en: "MAX1771 Boost", vals: [5, 12], def: 12, pins: 3 },
  lm3886: { prefix: "AUD86", ar: "LM3886 مضخم 68W", en: "LM3886 68W Amp", vals: [10, 30, 68], def: 30, pins: 3 },
  tda7294: { prefix: "AUD94", ar: "TDA7294 مضخم 100W", en: "TDA7294 100W Amp", vals: [10, 50, 100], def: 50, pins: 3 },
  tda2050: { prefix: "AUD50", ar: "TDA2050 مضخم 32W", en: "TDA2050 32W Amp", vals: [5, 15, 32], def: 15, pins: 3 },
  tda7377: { prefix: "AUD77", ar: "TDA7377 مضخم 2×30W", en: "TDA7377 2x30W Amp", vals: [5, 15, 30], def: 15, pins: 3 },
  tpa3116: { prefix: "AUD16", ar: "TPA3116 مضخم D", en: "TPA3116 Class-D", vals: [10, 50, 100], def: 50, pins: 3 },
  tpa2005: { prefix: "AUD05", ar: "TPA2005 مضخم D", en: "TPA2005 Class-D", vals: [1, 2, 3], def: 2, pins: 3 },
  lm4766: { prefix: "AUD66", ar: "LM4766 مضخم 2×40W", en: "LM4766 2x40W Amp", vals: [10, 20, 40], def: 20, pins: 3 },
  drv8434: { prefix: "DRV34", ar: "DRV8434 ستيبر", en: "DRV8434 Stepper", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2209: { prefix: "TMC09", ar: "TMC2209 ستيبر", en: "TMC2209 Stepper", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2130: { prefix: "TMC30", ar: "TMC2130 ستيبر", en: "TMC2130 Stepper", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  l6470: { prefix: "STP70", ar: "L6470 ستيبر", en: "L6470 Stepper", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  vnh5019: { prefix: "VNH19", ar: "VNH5019 محرك", en: "VNH5019 Motor Drv", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  drv8313: { prefix: "DRV13", ar: "DRV8313 BLDC", en: "DRV8313 BLDC", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  a4950: { prefix: "A4950", ar: "A4950 محرك DC", en: "A4950 DC Drv", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  mx1508: { prefix: "MX508", ar: "MX1508 محرك DC", en: "MX1508 DC Drv", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  esp32cam: { prefix: "CAM32", ar: "ESP32-CAM", en: "ESP32-CAM", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  sx1278: { prefix: "LOR78", ar: "SX1278 LoRa", en: "SX1278 LoRa", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  sx1276: { prefix: "LOR76", ar: "SX1276 LoRa", en: "SX1276 LoRa", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  nrf52832: { prefix: "BLE32", ar: "nRF52832 BLE", en: "nRF52832 BLE", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  hm10: { prefix: "BLE10", ar: "HM-10 BLE", en: "HM-10 BLE", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  jdy23: { prefix: "BLE23", ar: "JDY-23 BLE", en: "JDY-23 BLE", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  ublox_neo6m: { prefix: "GPS06", ar: "NEO-6M GPS", en: "NEO-6M GPS", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  ublox_neo7m: { prefix: "GPS07", ar: "NEO-7M GPS", en: "NEO-7M GPS", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  w5500: { prefix: "ETH55", ar: "W5500 إيثرنت", en: "W5500 Ethernet", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  cp2102: { prefix: "USB02", ar: "CP2102 USB-UART", en: "CP2102 USB-UART", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  ch340: { prefix: "USB40", ar: "CH340 USB-UART", en: "CH340 USB-UART", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  max485: { prefix: "RS485", ar: "MAX485 RS-485", en: "MAX485 RS-485", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  mcp2515: { prefix: "CAN15", ar: "MCP2515 CAN", en: "MCP2515 CAN", vals: ["TX", "RX", "IDLE"], def: "IDLE", pins: 3 },
  ssd1322: { prefix: "DSP22", ar: "SSD1322 OLED", en: "SSD1322 OLED", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  ssd1327: { prefix: "DSP27", ar: "SSD1327 OLED", en: "SSD1327 OLED", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  ssd1306_64: { prefix: "DSP64", ar: "OLED 128×64", en: "OLED 128x64", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  st7789: { prefix: "DSP89", ar: "ST7789 TFT", en: "ST7789 TFT", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  ili9488: { prefix: "DSP88", ar: "ILI9488 TFT", en: "ILI9488 TFT", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  hd44780: { prefix: "DSP44", ar: "HD44780 LCD", en: "HD44780 LCD", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  tm1637: { prefix: "DSP37", ar: "TM1637 4-digit", en: "TM1637 4-digit", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  ht16k33: { prefix: "DSP33", ar: "HT16K33 مصفوفة", en: "HT16K33 Matrix", vals: ["ON", "OFF"], def: "ON", pins: 3 },
  cd4017b: { prefix: "CNT17", ar: "CD4017B عداد", en: "CD4017B Counter", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc14: { prefix: "LGC14", ar: "74HC14 Schmitt", en: "74HC14 Schmitt", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc04: { prefix: "LGC04", ar: "74HC04 عاكس", en: "74HC04 Inverter", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc08: { prefix: "LGC08", ar: "74HC08 AND", en: "74HC08 AND", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc32: { prefix: "LGC32", ar: "74HC32 OR", en: "74HC32 OR", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc86: { prefix: "LGC86", ar: "74HC86 XOR", en: "74HC86 XOR", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc74: { prefix: "LGC74", ar: "74HC74 قلاب D", en: "74HC74 D Flip-Flop", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc590: { prefix: "LGC90", ar: "74HC590 عداد", en: "74HC590 Counter", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc4067: { prefix: "MUX67", ar: "74HC4067 مالتي", en: "74HC4067 Mux", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24c64: { prefix: "MEM64", ar: "AT24C64 ذاكرة", en: "AT24C64 EEPROM", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24c128: { prefix: "MEM28", ar: "AT24C128 ذاكرة", en: "AT24C128 EEPROM", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  w25q128: { prefix: "MEM12", ar: "W25Q128 فلاش", en: "W25Q128 Flash", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  fm25v02: { prefix: "MEM02", ar: "FM25V02 FRAM", en: "FM25V02 FRAM", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mcp23s17: { prefix: "IOX17", ar: "MCP23S17 توسعة", en: "MCP23S17 IO Exp", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  tca9534: { prefix: "IOX34", ar: "TCA9534 توسعة", en: "TCA9534 IO Exp", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  max7301: { prefix: "IOX01", ar: "MAX7301 توسعة", en: "MAX7301 IO Exp", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  elec_cap: { prefix: "CE", ar: "مكثف إلكتروليتي", en: "Electrolytic Cap", vals: [1, 4.7, 10, 47, 100, 220, 470, 1000, 2200, 4700], def: 100 },
  tantalum_cap: { prefix: "CT", ar: "مكثف تانتالوم", en: "Tantalum Cap", vals: [1, 4.7, 10, 22, 47, 100], def: 10 },
  ceramic_cap: { prefix: "CC", ar: "مكثف سيراميك", en: "Ceramic Cap", vals: [0.001, 0.01, 0.1, 1], def: 0.1 },
  supercap: { prefix: "CSC", ar: "مكثف فائق", en: "Supercapacitor", vals: [1000, 10000, 100000], def: 10000 },
  fast_diode: { prefix: "D4148", ar: "دايود سريع 1N4148", en: "1N4148 Fast Diode", vals: ["silicon"], def: "silicon" },
  rectifier_diode: { prefix: "D4007", ar: "دايود تقويم 1N4007", en: "1N4007 Rectifier", vals: ["silicon"], def: "silicon" },
  germanium_diode: { prefix: "DOA91", ar: "دايود جرمانيوم OA91", en: "OA91 Germanium Diode", vals: ["germanium"], def: "germanium" },
  zener_1w: { prefix: "DZ1W", ar: "زينر 1 واط", en: "1W Zener", vals: [3.3, 5.1, 6.2, 9.1, 12, 15, 18, 24], def: 5.1 },
  tvs_diode: { prefix: "TVS", ar: "دايود حماية TVS", en: "TVS Diode", vals: [5, 6.8, 12, 15, 24, 33], def: 12 },
  schottky_ss34: { prefix: "DSS", ar: "دايود شوتكي SS34", en: "SS34 Schottky", vals: ["SS14", "SS34", "SB560"], def: "SS34" },
  ntc: { prefix: "NTC", ar: "مقاومة NTC", en: "NTC Thermistor", vals: [1000, 10000, 100000], def: 10000 },
  polyfuse: { prefix: "PF", ar: "فيوز ذاتي الاستعادة", en: "Resettable Fuse", vals: [0.1, 0.5, 1.1, 2.5], def: 0.5 },
  power_resistor: { prefix: "RP", ar: "مقاومة قدرة", en: "Power Resistor", vals: [0.1, 0.22, 0.47, 1, 2.2, 4.7, 10, 22, 47, 100], def: 1 },
  shunt_resistor: { prefix: "RSH", ar: "مقاومة شنت", en: "Shunt Resistor", vals: [0.001, 0.01, 0.05, 0.1], def: 0.1 },
  trimmer_pot: { prefix: "RVT", ar: "مقاومة معايرة", en: "Trimmer Pot", vals: [100, 1000, 10000, 100000], def: 10000, pins: 3 },
  slide_pot: { prefix: "RVS", ar: "مقاومة انزلاقية", en: "Slide Pot", vals: [1000, 10000, 100000], def: 10000, pins: 3 },
  rheostat: { prefix: "RVR", ar: "ريوستات", en: "Rheostat", vals: [10, 100, 1000], def: 100, pins: 3 },
  q_tip120: { prefix: "Q120", ar: "TIP120 دارلنجتون", en: "TIP120 Darlington", vals: ["NPN"], def: "NPN", pins: 3 },
  q_tip31: { prefix: "Q31", ar: "TIP31 قدرة", en: "TIP31 Power NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_bc547: { prefix: "Q547", ar: "ترانزستور BC547", en: "BC547 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_2n2222: { prefix: "Q2222", ar: "ترانزستور 2N2222", en: "2N2222 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_2n3904: { prefix: "Q3904", ar: "ترانزستور 2N3904", en: "2N3904 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_bd139: { prefix: "Q139", ar: "ترانزستور BD139", en: "BD139 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_bc557: { prefix: "QP557", ar: "ترانزستور BC557", en: "BC557 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_2n3906: { prefix: "QP3906", ar: "ترانزستور 2N3906", en: "2N3906 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_tip32: { prefix: "QP32", ar: "TIP32 قدرة", en: "TIP32 Power PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_tip127: { prefix: "QP127", ar: "TIP127 دارلنجتون", en: "TIP127 Darlington PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_bd140: { prefix: "QP140", ar: "ترانزستور BD140", en: "BD140 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  m_irf540: { prefix: "MN540", ar: "MOSFET IRF540", en: "IRF540 MOSFET", vals: ["IRF540"], def: "IRF540", pins: 3 },
  m_irlz44n: { prefix: "MN44", ar: "MOSFET IRLZ44N", en: "IRLZ44N MOSFET", vals: ["IRLZ44N"], def: "IRLZ44N", pins: 3 },
  m_2n7000: { prefix: "MN7000", ar: "MOSFET 2N7000", en: "2N7000 MOSFET", vals: ["2N7000"], def: "2N7000", pins: 3 },
  m_irf3205: { prefix: "MN3205", ar: "MOSFET IRF3205", en: "IRF3205 MOSFET", vals: ["IRF3205"], def: "IRF3205", pins: 3 },
  m_irlb8721: { prefix: "MN8721", ar: "MOSFET IRLB8721", en: "IRLB8721 MOSFET", vals: ["IRLB8721"], def: "IRLB8721", pins: 3 },
  power_inductor: { prefix: "LP", ar: "ملف قدرة", en: "Power Inductor", vals: [1, 10, 47, 100, 330, 1000], def: 100 },
  ferrite_choke: { prefix: "LF", ar: "ملف خانق فيريت", en: "Ferrite Choke", vals: [1, 10, 100], def: 10 },
  halogen_lamp: { prefix: "LH", ar: "مصباح هالوجين", en: "Halogen Lamp", vals: [20, 35, 50], def: 35 },
  dc_fan: { prefix: "FAN", ar: "مروحة DC", en: "DC Fan", vals: [5, 10, 20], def: 10 },
  vibration_motor: { prefix: "MVB", ar: "محرك اهتزاز", en: "Vibration Motor", vals: [5, 10], def: 5 },
  piezo_buzzer: { prefix: "BZP", ar: "جرس بيزو", en: "Piezo Buzzer", vals: [50, 100, 200], def: 100 },
  headphones: { prefix: "HP", ar: "سماعة رأس", en: "Headphones", vals: [16, 32, 64], def: 32 },
  push_button: { prefix: "SB", ar: "زر ضغط", en: "Push Button", vals: [], def: 0 },
  toggle_switch: { prefix: "ST", ar: "مفتاح تبديل", en: "Toggle Switch", vals: [], def: 0 },
  slide_switch: { prefix: "SS", ar: "مفتاح انزلاقي", en: "Slide Switch", vals: [], def: 0 },
  limit_switch: { prefix: "SL", ar: "مفتاح حدّي", en: "Limit Switch", vals: [], def: 0 },
  lipo_battery: { prefix: "LIPO", ar: "بطارية ليثيوم", en: "LiPo Battery", vals: [3.7, 7.4, 11.1], def: 3.7 },
  aa_cell: { prefix: "AA", ar: "بطارية AA", en: "AA Cell", vals: [1.2, 1.5], def: 1.5 },
  coin_cell: { prefix: "CR", ar: "بطارية زر", en: "Coin Cell", vals: [3], def: 3 },
  nine_volt: { prefix: "B9V", ar: "بطارية 9 فولت", en: "9V Battery", vals: [9], def: 9 },
  usb_power: { prefix: "USB", ar: "مصدر USB", en: "USB Power", vals: [5], def: 5 },
  bench_supply: { prefix: "PSU", ar: "مصدر مخبري", en: "Bench Supply", vals: [3.3, 5, 9, 12, 24], def: 5 },
  lead_acid: { prefix: "PB", ar: "بطارية رصاص", en: "Lead-Acid Battery", vals: [6, 12], def: 12 },
  tmp117: { prefix: "TMP117", ar: "TMP117 حرارة", en: "TMP117 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  max30205: { prefix: "MAX205", ar: "MAX30205 حرارة", en: "MAX30205 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  amg8833: { prefix: "AMG833", ar: "AMG8833 حرارة", en: "AMG8833 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  mlx90640: { prefix: "MLX640", ar: "MLX90640 حرارة", en: "MLX90640 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  lm73: { prefix: "LM73", ar: "LM73 حرارة", en: "LM73 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  si7050: { prefix: "SI7050", ar: "SI7050 حرارة", en: "SI7050 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  ds28ea00: { prefix: "DS2A00", ar: "DS28EA00 حرارة", en: "DS28EA00 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  ad8495: { prefix: "AD8495", ar: "AD8495 حرارة", en: "AD8495 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  hih6130: { prefix: "HIH130", ar: "HIH6130 رطوبة", en: "HIH6130 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  dht21: { prefix: "DHT21", ar: "DHT21 رطوبة", en: "DHT21 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  sht40: { prefix: "SHT40", ar: "SHT40 رطوبة", en: "SHT40 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  sht45: { prefix: "SHT45", ar: "SHT45 رطوبة", en: "SHT45 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  hdc2080: { prefix: "HDC080", ar: "HDC2080 رطوبة", en: "HDC2080 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  bme688: { prefix: "BME688", ar: "BME688 رطوبة", en: "BME688 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  bmp390: { prefix: "BMP390", ar: "BMP390 ضغط", en: "BMP390 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  bmp581: { prefix: "BMP581", ar: "BMP581 ضغط", en: "BMP581 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  lps35hw: { prefix: "LPS5HW", ar: "LPS35HW ضغط", en: "LPS35HW Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  lps33hw: { prefix: "LPS3HW", ar: "LPS33HW ضغط", en: "LPS33HW Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  spl06: { prefix: "SPL06", ar: "SPL06 ضغط", en: "SPL06 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  ms5837: { prefix: "MS5837", ar: "MS5837 ضغط", en: "MS5837 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  mq137: { prefix: "MQ137", ar: "MQ137 غاز", en: "MQ137 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mq138: { prefix: "MQ138", ar: "MQ138 غاز", en: "MQ138 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mq214: { prefix: "MQ214", ar: "MQ214 غاز", en: "MQ214 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mq216: { prefix: "MQ216", ar: "MQ216 غاز", en: "MQ216 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  scd30: { prefix: "SCD30", ar: "SCD30 غاز", en: "SCD30 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  scd40: { prefix: "SCD40", ar: "SCD40 غاز", en: "SCD40 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  scd41: { prefix: "SCD41", ar: "SCD41 غاز", en: "SCD41 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  sgp40: { prefix: "SGP40", ar: "SGP40 غاز", en: "SGP40 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  sen54: { prefix: "SEN54", ar: "SEN54 غاز", en: "SEN54 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  ags02ma: { prefix: "AGS2MA", ar: "AGS02MA غاز", en: "AGS02MA Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  as7341: { prefix: "AS7341", ar: "AS7341 ضوء", en: "AS7341 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  as7262: { prefix: "AS7262", ar: "AS7262 ضوء", en: "AS7262 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  tsl2591: { prefix: "TSL591", ar: "TSL2591 ضوء", en: "TSL2591 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  veml6075: { prefix: "VEM075", ar: "VEML6075 ضوء", en: "VEML6075 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  guva_s12sd: { prefix: "GUV2SD", ar: "GUVA-S12SD ضوء", en: "GUVA-S12SD Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  bh1745: { prefix: "BH1745", ar: "BH1745 ضوء", en: "BH1745 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  isl29125: { prefix: "ISL125", ar: "ISL29125 ضوء", en: "ISL29125 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  apds9306: { prefix: "APD306", ar: "APDS9306 ضوء", en: "APDS9306 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  mpu6500: { prefix: "MPU500", ar: "MPU6500 حركة", en: "MPU6500 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lsm9ds1: { prefix: "LSMDS1", ar: "LSM9DS1 حركة", en: "LSM9DS1 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lsm303: { prefix: "LSM303", ar: "LSM303 حركة", en: "LSM303 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  l3gd20h: { prefix: "L3G20H", ar: "L3GD20H حركة", en: "L3GD20H Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  bmi160: { prefix: "BMI160", ar: "BMI160 حركة", en: "BMI160 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  bmi270: { prefix: "BMI270", ar: "BMI270 حركة", en: "BMI270 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  adxl375: { prefix: "ADX375", ar: "ADXL375 حركة", en: "ADXL375 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  icm42688: { prefix: "ICM688", ar: "ICM42688 حركة", en: "ICM42688 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lis2dh12: { prefix: "LISH12", ar: "LIS2DH12 حركة", en: "LIS2DH12 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  kxtj3: { prefix: "KXTJ3", ar: "KXTJ3 حركة", en: "KXTJ3 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  vl53l1x: { prefix: "VL5L1X", ar: "VL53L1X مسافة", en: "VL53L1X Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  gp2y0a21: { prefix: "GP2A21", ar: "GP2Y0A21 مسافة", en: "GP2Y0A21 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  gp2y0a02: { prefix: "GP2A02", ar: "GP2Y0A02 مسافة", en: "GP2Y0A02 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  us100: { prefix: "US100", ar: "US-100 مسافة", en: "US-100 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  a02yyuw: { prefix: "A02YUW", ar: "A02YYUW مسافة", en: "A02YYUW Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  ld2410: { prefix: "LD2410", ar: "LD2410 رادار مسافة", en: "LD2410 رادار Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  rcwl0516: { prefix: "RCW516", ar: "RCWL-0516 مسافة", en: "RCWL-0516 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  tfmini: { prefix: "TFMINI", ar: "TFmini مسافة", en: "TFmini Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  tf_luna: { prefix: "TFLUNA", ar: "TF-Luna مسافة", en: "TF-Luna Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  vcnl4040: { prefix: "VCN040", ar: "VCNL4040 مسافة", en: "VCNL4040 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  jsn_sr04t: { prefix: "JSN04T", ar: "JSN-SR04T مسافة", en: "JSN-SR04T Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  max30100: { prefix: "MAX100", ar: "MAX30100 حيوي", en: "MAX30100 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  ad8232: { prefix: "AD8232", ar: "AD8232 ECG حيوي", en: "AD8232 ECG Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  pulse_sensor: { prefix: "PULSOR", ar: "Pulse Sensor حيوي", en: "Pulse Sensor Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  gsr_sensor: { prefix: "GSRSOR", ar: "GSR حيوي", en: "GSR Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  r307: { prefix: "R307", ar: "R307 بصمة حيوي", en: "R307 بصمة Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  ina169: { prefix: "INA169", ar: "INA169 تيار", en: "INA169 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  acs758: { prefix: "ACS758", ar: "ACS758 تيار", en: "ACS758 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  max471: { prefix: "MAX471", ar: "MAX471 تيار", en: "MAX471 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  pzem004t: { prefix: "PZE04T", ar: "PZEM-004T تيار", en: "PZEM-004T Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  hlw8012: { prefix: "HLW012", ar: "HLW8012 تيار", en: "HLW8012 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ina228: { prefix: "INA228", ar: "INA228 تيار", en: "INA228 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ina238: { prefix: "INA238", ar: "INA238 تيار", en: "INA238 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ss49e: { prefix: "SS49E", ar: "SS49E مغناطيس", en: "SS49E Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  a1302: { prefix: "A1302", ar: "A1302 مغناطيس", en: "A1302 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  drv5053: { prefix: "DRV053", ar: "DRV5053 مغناطيس", en: "DRV5053 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  as5600: { prefix: "AS5600", ar: "AS5600 مغناطيس", en: "AS5600 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  as5048a: { prefix: "AS548A", ar: "AS5048A مغناطيس", en: "AS5048A Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  sh1106: { prefix: "SH1106", ar: "SH1106 OLED شاشة", en: "SH1106 OLED Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ssd1305: { prefix: "SSD305", ar: "SSD1305 OLED شاشة", en: "SSD1305 OLED Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  gc9a01: { prefix: "GC9A01", ar: "GC9A01 دائرية شاشة", en: "GC9A01 دائرية Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  st7796: { prefix: "ST7796", ar: "ST7796 TFT شاشة", en: "ST7796 TFT Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ili9225: { prefix: "ILI225", ar: "ILI9225 TFT شاشة", en: "ILI9225 TFT Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ssd1963: { prefix: "SSD963", ar: "SSD1963 TFT شاشة", en: "SSD1963 TFT Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  epd_154: { prefix: "EPD154", ar: "E-Paper 1.54 شاشة", en: "E-Paper 1.54 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  epd_213: { prefix: "EPD213", ar: "E-Paper 2.13 شاشة", en: "E-Paper 2.13 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  epd_29: { prefix: "EPD29", ar: "E-Paper 2.9 شاشة", en: "E-Paper 2.9 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  lcd_12864: { prefix: "LCD864", ar: "LCD 128x64 شاشة", en: "LCD 128x64 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  lcd_16x4: { prefix: "LCD6X4", ar: "LCD 16x4 شاشة", en: "LCD 16x4 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  lcd_8x2: { prefix: "LCD8X2", ar: "LCD 8x2 شاشة", en: "LCD 8x2 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  tm1638: { prefix: "TM1638", ar: "TM1638 LED شاشة", en: "TM1638 LED Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ht1621: { prefix: "HT1621", ar: "HT1621 LCD شاشة", en: "HT1621 LCD Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  drv8847: { prefix: "DRV847", ar: "DRV8847 تشغيل محرك", en: "DRV8847 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  drv8880: { prefix: "DRV880", ar: "DRV8880 تشغيل محرك", en: "DRV8880 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2208: { prefix: "TMC208", ar: "TMC2208 تشغيل محرك", en: "TMC2208 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2160: { prefix: "TMC160", ar: "TMC2160 تشغيل محرك", en: "TMC2160 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc5160: { prefix: "TMC162", ar: "TMC5160 تشغيل محرك", en: "TMC5160 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  l6208: { prefix: "L6208", ar: "L6208 تشغيل محرك", en: "L6208 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  l6235: { prefix: "L6235", ar: "L6235 تشغيل محرك", en: "L6235 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  vnh2sp30: { prefix: "VNHP30", ar: "VNH2SP30 تشغيل محرك", en: "VNH2SP30 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  ibt2: { prefix: "IBT2", ar: "IBT-2 تشغيل محرك", en: "IBT-2 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  lv8548: { prefix: "LV8548", ar: "LV8548 تشغيل محرك", en: "LV8548 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  lm7818: { prefix: "LM7818", ar: "LM7818 منظم", en: "LM7818 Regulator", vals: [18], def: 18, pins: 3 },
  lm78l05: { prefix: "LM7L05", ar: "LM78L05 منظم", en: "LM78L05 Regulator", vals: [5], def: 5, pins: 3 },
  lm79l05: { prefix: "LM7L02", ar: "LM79L05 سالب منظم", en: "LM79L05 سالب Regulator", vals: [-5], def: -5, pins: 3 },
  lm317l: { prefix: "LM317L", ar: "LM317L منظم", en: "LM317L Regulator", vals: [1.25, 3.3, 5, 9], def: 5, pins: 3 },
  lm350: { prefix: "LM350", ar: "LM350 منظم", en: "LM350 Regulator", vals: [1.25, 5, 12], def: 5, pins: 3 },
  ld1117: { prefix: "LD1117", ar: "LD1117 منظم", en: "LD1117 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  xc6206: { prefix: "XC6206", ar: "XC6206 منظم", en: "XC6206 Regulator", vals: [1.8, 3.3], def: 3.3, pins: 3 },
  ap2112: { prefix: "AP2112", ar: "AP2112 منظم", en: "AP2112 Regulator", vals: [1.8, 3.3], def: 3.3, pins: 3 },
  tlv1117: { prefix: "TLV117", ar: "TLV1117 منظم", en: "TLV1117 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  lt3045: { prefix: "LT3045", ar: "LT3045 منظم", en: "LT3045 Regulator", vals: [1.2, 3.3, 5], def: 3.3, pins: 3 },
  lm2575: { prefix: "LM2575", ar: "LM2575 Buck محول", en: "LM2575 Buck Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm2595: { prefix: "LM2595", ar: "LM2595 Buck محول", en: "LM2595 Buck Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  xl4015: { prefix: "XL4015", ar: "XL4015 Buck محول", en: "XL4015 Buck Converter", vals: [5, 12, 24], def: 12, pins: 3 },
  xl4005: { prefix: "XL4005", ar: "XL4005 Buck محول", en: "XL4005 Buck Converter", vals: [5, 12, 24], def: 12, pins: 3 },
  xl7005: { prefix: "XL7005", ar: "XL7005 Buck محول", en: "XL7005 Buck Converter", vals: [5, 12], def: 5, pins: 3 },
  mp2307: { prefix: "MP2307", ar: "MP2307 Buck محول", en: "MP2307 Buck Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  mp2315: { prefix: "MP2315", ar: "MP2315 Buck محول", en: "MP2315 Buck Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  tps54331: { prefix: "TPS331", ar: "TPS54331 Buck محول", en: "TPS54331 Buck Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  sx1308: { prefix: "SX1308", ar: "SX1308 Boost محول", en: "SX1308 Boost Converter", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  cn3791: { prefix: "CN3791", ar: "CN3791 MPPT شاحن", en: "CN3791 MPPT Charger", vals: [4.2, 8.4, 12.6], def: 8.4, pins: 3 },
  bq24074: { prefix: "BQ2074", ar: "BQ24074 شاحن", en: "BQ24074 Charger", vals: [4.2], def: 4.2, pins: 3 },
  tp5100: { prefix: "TP5100", ar: "TP5100 شاحن", en: "TP5100 Charger", vals: [4.2, 8.4], def: 4.2, pins: 3 },
  ip5306: { prefix: "IP5306", ar: "IP5306 باور بانك", en: "IP5306 Power Bank", vals: [5], def: 5, pins: 3 },
  esp32_c3: { prefix: "ESP2C3", ar: "ESP32-C3 اتصال", en: "ESP32-C3 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  esp32_s3: { prefix: "ESP2S3", ar: "ESP32-S3 اتصال", en: "ESP32-S3 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  nrf52840: { prefix: "NRF840", ar: "NRF52840 اتصال", en: "NRF52840 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  hc06: { prefix: "HC06", ar: "HC-06 اتصال", en: "HC-06 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  hm11: { prefix: "HM11", ar: "HM-11 اتصال", en: "HM-11 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  jdy31: { prefix: "JDY31", ar: "JDY-31 اتصال", en: "JDY-31 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  e32: { prefix: "E32", ar: "E32 LoRa اتصال", en: "E32 LoRa Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sx1262: { prefix: "SX1262", ar: "SX1262 اتصال", en: "SX1262 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  dw1000: { prefix: "DW1000", ar: "DW1000 UWB اتصال", en: "DW1000 UWB Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  pn532: { prefix: "PN532", ar: "PN532 NFC اتصال", en: "PN532 NFC Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  w5100: { prefix: "W5100", ar: "W5100 ETH اتصال", en: "W5100 ETH Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  enc424j600: { prefix: "ENC600", ar: "ENC424J600 اتصال", en: "ENC424J600 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  mcp2551: { prefix: "MCP551", ar: "MCP2551 CAN اتصال", en: "MCP2551 CAN Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  tja1050: { prefix: "TJA050", ar: "TJA1050 CAN اتصال", en: "TJA1050 CAN Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sn65hvd230: { prefix: "SN6230", ar: "SN65HVD230 CAN اتصال", en: "SN65HVD230 CAN Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  max232: { prefix: "MAX232", ar: "MAX232 اتصال", en: "MAX232 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  max3232: { prefix: "MAX233", ar: "MAX3232 اتصال", en: "MAX3232 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ft232: { prefix: "FT232", ar: "FT232 USB اتصال", en: "FT232 USB Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  pl2303: { prefix: "PL2303", ar: "PL2303 USB اتصال", en: "PL2303 USB Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cp2104: { prefix: "CP2104", ar: "CP2104 USB اتصال", en: "CP2104 USB Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  l76k: { prefix: "L76K", ar: "L76K GPS اتصال", en: "L76K GPS Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  neo_m8n: { prefix: "NEOM8N", ar: "NEO-M8N GPS اتصال", en: "NEO-M8N GPS Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sim7600: { prefix: "SIM600", ar: "SIM7600 4G خلوي", en: "SIM7600 4G Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim868: { prefix: "SIM868", ar: "SIM868 خلوي", en: "SIM868 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  a7670: { prefix: "A7670", ar: "A7670 4G خلوي", en: "A7670 4G Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  ic_74hc02: { prefix: "HC02", ar: "74HC02 NOR", en: "74HC02 NOR", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc10: { prefix: "HC10", ar: "74HC10 NAND3", en: "74HC10 NAND3", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc20: { prefix: "HC20", ar: "74HC20 NAND4", en: "74HC20 NAND4", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc30: { prefix: "HC30", ar: "74HC30 NAND8", en: "74HC30 NAND8", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc125: { prefix: "HC125", ar: "74HC125 Buffer", en: "74HC125 Buffer", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc157: { prefix: "HC157", ar: "74HC157 Mux", en: "74HC157 Mux", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc151: { prefix: "HC151", ar: "74HC151 Mux8", en: "74HC151 Mux8", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc139: { prefix: "HC139", ar: "74HC139 Dec", en: "74HC139 Dec", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc154: { prefix: "HC154", ar: "74HC154 Dec16", en: "74HC154 Dec16", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc161: { prefix: "HC161", ar: "74HC161 Counter", en: "74HC161 Counter", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc164: { prefix: "HC164", ar: "74HC164 Shift", en: "74HC164 Shift", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc166: { prefix: "HC166", ar: "74HC166 Shift", en: "74HC166 Shift", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc174: { prefix: "HC174", ar: "74HC174 FF6", en: "74HC174 FF6", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc175: { prefix: "HC175", ar: "74HC175 FF4", en: "74HC175 FF4", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc193: { prefix: "HC193", ar: "74HC193 UpDown", en: "74HC193 UpDown", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc244: { prefix: "HC244", ar: "74HC244 Buffer8", en: "74HC244 Buffer8", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc245: { prefix: "HC245", ar: "74HC245 Bus", en: "74HC245 Bus", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc283: { prefix: "HC283", ar: "74HC283 Adder", en: "74HC283 Adder", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc374: { prefix: "HC374", ar: "74HC374 Latch", en: "74HC374 Latch", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc4040: { prefix: "HC4040", ar: "74HC4040 Ripple", en: "74HC4040 Ripple", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc4046: { prefix: "HC4046", ar: "74HC4046 PLL", en: "74HC4046 PLL", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc4053: { prefix: "HC4053", ar: "74HC4053 Mux", en: "74HC4053 Mux", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc4094: { prefix: "HC4094", ar: "74HC4094 Shift", en: "74HC4094 Shift", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mcp23008: { prefix: "MCP008", ar: "MCP23008 IO", en: "MCP23008 IO", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  tca9535: { prefix: "TCA535", ar: "TCA9535 IO", en: "TCA9535 IO", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  txs0108: { prefix: "TXS108", ar: "TXS0108 Level", en: "TXS0108 Level", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  sn74lvc245: { prefix: "SN7245", ar: "LVC245 Bus", en: "LVC245 Bus", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24c02: { prefix: "AT2C02", ar: "AT24C02 ذاكرة", en: "AT24C02 EEPROM", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24c08: { prefix: "AT2C08", ar: "AT24C08 ذاكرة", en: "AT24C08 EEPROM", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24c16: { prefix: "AT2C16", ar: "AT24C16 ذاكرة", en: "AT24C16 EEPROM", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  lm1875: { prefix: "LM1875", ar: "LM1875 مضخم", en: "LM1875 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda2040: { prefix: "TDA040", ar: "TDA2040 مضخم", en: "TDA2040 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda7498: { prefix: "TDA498", ar: "TDA7498 مضخم", en: "TDA7498 Amp", vals: [40, 80, 160], def: 80, pins: 3 },
  tpa3110: { prefix: "TPA110", ar: "TPA3110 مضخم", en: "TPA3110 Amp", vals: [5, 15, 30], def: 15, pins: 3 },
  pam8610: { prefix: "PAM610", ar: "PAM8610 مضخم", en: "PAM8610 Amp", vals: [5, 15], def: 15, pins: 3 },
  pam8302: { prefix: "PAM302", ar: "PAM8302 مضخم", en: "PAM8302 Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  max9744: { prefix: "MAX744", ar: "MAX9744 مضخم", en: "MAX9744 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  mcp6002: { prefix: "MCP002", ar: "MCP6002 مكبر عمليات", en: "MCP6002 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  mcp6022: { prefix: "MCP022", ar: "MCP6022 مكبر عمليات", en: "MCP6022 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  tl082: { prefix: "TL082", ar: "TL082 مكبر عمليات", en: "TL082 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  tl084: { prefix: "TL084", ar: "TL084 مكبر عمليات", en: "TL084 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lf353: { prefix: "LF353", ar: "LF353 مكبر عمليات", en: "LF353 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lf411: { prefix: "LF411", ar: "LF411 مكبر عمليات", en: "LF411 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  op07: { prefix: "OP07", ar: "OP07 مكبر عمليات", en: "OP07 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  op27: { prefix: "OP27", ar: "OP27 مكبر عمليات", en: "OP27 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8605: { prefix: "AD8605", ar: "AD8605 مكبر عمليات", en: "AD8605 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  led_white: { prefix: "LEDITE", ar: "LED أبيض", en: "White LED", vals: ["white"], def: "white" },
  led_blue: { prefix: "LEDLUE", ar: "LED أزرق", en: "Blue LED", vals: ["blue"], def: "blue" },
  led_green: { prefix: "LEDEEN", ar: "LED أخضر", en: "Green LED", vals: ["green"], def: "green" },
  led_yellow: { prefix: "LEDLOW", ar: "LED أصفر", en: "Yellow LED", vals: ["yellow"], def: "yellow" },
  led_red: { prefix: "LEDRED", ar: "LED أحمر", en: "Red LED", vals: ["red"], def: "red" },
  photocell: { prefix: "PHOELL", ar: "خلية ضوئية", en: "Photocell", vals: [1000, 10000, 100000], def: 10000 },
  schottky_1n5817: { prefix: "SCH817", ar: "شوتكي 1N5817", en: "1N5817 Schottky", vals: ["1N5817"], def: "1N5817" },
  schottky_sb340: { prefix: "SCH340", ar: "شوتكي SB340", en: "SB340 Schottky", vals: ["SB340"], def: "SB340" },
  schottky_mbr1045: { prefix: "SCH045", ar: "شوتكي MBR1045", en: "MBR1045 Schottky", vals: ["MBR1045"], def: "MBR1045" },
  zener_0w5: { prefix: "ZEN0W5", ar: "زينر نصف واط", en: "0.5W Zener", vals: [2.7, 3.3, 4.7, 5.1, 6.2, 9.1, 12, 15], def: 5.1 },
  zener_5w: { prefix: "ZENR5W", ar: "زينر 5 واط", en: "5W Zener", vals: [5.6, 9.1, 12, 15, 24, 33], def: 12 },
  tvs_smbj: { prefix: "TVSMBJ", ar: "TVS SMBJ", en: "SMBJ TVS", vals: [5, 12, 24, 36], def: 12 },
  diode_1n4001: { prefix: "DIO001", ar: "دايود 1N4001", en: "1N4001 Diode", vals: ["silicon"], def: "silicon" },
  diode_1n4004: { prefix: "DIO004", ar: "دايود 1N4004", en: "1N4004 Diode", vals: ["silicon"], def: "silicon" },
  diode_1n5408: { prefix: "DIO408", ar: "دايود 1N5408 3A", en: "1N5408 3A Diode", vals: ["silicon"], def: "silicon" },
  diode_uf4007: { prefix: "DIO007", ar: "دايود فائق السرعة UF4007", en: "UF4007 Ultrafast", vals: ["silicon"], def: "silicon" },
  diode_1n34a: { prefix: "DIO34A", ar: "دايود جرمانيوم 1N34A", en: "1N34A Germanium", vals: ["germanium"], def: "germanium" },
  film_cap: { prefix: "FILCAP", ar: "مكثف فيلم", en: "Film Cap", vals: [0.01, 0.1, 1, 10], def: 0.1 },
  mica_cap: { prefix: "MICCAP", ar: "مكثف ميكا", en: "Mica Cap", vals: [0.0001, 0.001, 0.01], def: 0.001 },
  polymer_cap: { prefix: "POLCAP", ar: "مكثف بوليمر", en: "Polymer Cap", vals: [10, 47, 100, 470, 1000], def: 100 },
  bipolar_cap: { prefix: "BIPCAP", ar: "مكثف غير قطبي", en: "Bipolar Electrolytic", vals: [1, 10, 47, 100], def: 10 },
  mkp_cap: { prefix: "MKPCAP", ar: "مكثف MKP", en: "MKP Cap", vals: [0.1, 1, 10], def: 1 },
  x2_cap: { prefix: "X2CAP", ar: "مكثف X2", en: "X2 Cap", vals: [0.1, 0.22, 0.47], def: 0.1 },
  y_cap: { prefix: "YCAP", ar: "مكثف Y", en: "Y Cap", vals: [0.001, 0.0047], def: 0.001 },
  trimmer_cap: { prefix: "TRICAP", ar: "مكثف معايرة", en: "Trimmer Cap", vals: [0.001, 0.01], def: 0.001 },
  carbon_resistor: { prefix: "CARTOR", ar: "مقاومة كربونية", en: "Carbon Resistor", vals: [10, 47, 100, 220, 330, 470, 1000, 2200, 4700, 10000], def: 330 },
  metal_film_resistor: { prefix: "METTOR", ar: "مقاومة فيلم معدني", en: "Metal Film Resistor", vals: [10, 47, 100, 220, 330, 470, 1000, 2200, 4700, 10000], def: 1000 },
  wirewound_resistor: { prefix: "WIRTOR", ar: "مقاومة سلكية", en: "Wirewound Resistor", vals: [1, 10, 47, 100, 470, 1000], def: 100 },
  smd_resistor: { prefix: "SMDTOR", ar: "مقاومة SMD", en: "SMD Resistor", vals: [10, 47, 100, 220, 330, 470, 1000, 2200, 4700, 10000], def: 1000 },
  fusible_resistor: { prefix: "FUSTOR", ar: "مقاومة فيوزية", en: "Fusible Resistor", vals: [1, 10, 47, 100], def: 10 },
  pullup_resistor: { prefix: "PULTOR", ar: "مقاومة رفع", en: "Pull-up Resistor", vals: [4700, 10000, 47000], def: 10000 },
  current_sense_res: { prefix: "CURRES", ar: "مقاومة قياس تيار", en: "Current Sense Resistor", vals: [0.005, 0.01, 0.05, 0.1], def: 0.01 },
  high_value_resistor: { prefix: "HIGTOR", ar: "مقاومة عالية", en: "High-Value Resistor", vals: [100000, 470000, 1000000, 10000000], def: 1000000 },
  multiturn_pot: { prefix: "MULPOT", ar: "مقاومة متعددة اللفات", en: "Multiturn Pot", vals: [1000, 10000, 100000], def: 10000, pins: 3 },
  log_pot: { prefix: "LOGPOT", ar: "مقاومة لوغاريتمية", en: "Log Pot", vals: [10000, 50000, 100000], def: 50000, pins: 3 },
  volume_pot: { prefix: "VOLPOT", ar: "مقاومة صوت", en: "Volume Pot", vals: [10000, 50000, 100000], def: 10000, pins: 3 },
  joystick_axis: { prefix: "JOYXIS", ar: "محور جويستيك", en: "Joystick Axis", vals: [10000], def: 10000, pins: 3 },
  ntc_probe: { prefix: "NTCOBE", ar: "مجس NTC", en: "NTC Probe", vals: [10000, 100000], def: 10000 },
  q_bc337: { prefix: "QBC337", ar: "ترانزستور BC337", en: "BC337 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_s8050: { prefix: "QS8050", ar: "ترانزستور S8050", en: "S8050 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_c945: { prefix: "QC945", ar: "ترانزستور C945", en: "C945 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_2n3055: { prefix: "Q2N055", ar: "ترانزستور 2N3055", en: "2N3055 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_mje3055: { prefix: "QMJ055", ar: "ترانزستور MJE3055", en: "MJE3055 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_tip41c: { prefix: "QTI41C", ar: "ترانزستور TIP41C", en: "TIP41C NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_bd137: { prefix: "QBD137", ar: "ترانزستور BD137", en: "BD137 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_2sc1815: { prefix: "Q2S815", ar: "ترانزستور 2SC1815", en: "2SC1815 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_2sc5200: { prefix: "Q2S200", ar: "ترانزستور 2SC5200", en: "2SC5200 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_2n5551: { prefix: "Q2N551", ar: "ترانزستور 2N5551", en: "2N5551 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_mpsa42: { prefix: "QMPA42", ar: "ترانزستور MPSA42", en: "MPSA42 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_bc639: { prefix: "QBC639", ar: "ترانزستور BC639", en: "BC639 NPN", vals: ["NPN"], def: "NPN", pins: 3 },
  q_2n2907: { prefix: "Q2N907", ar: "ترانزستور 2N2907", en: "2N2907 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_bc327: { prefix: "QBC327", ar: "ترانزستور BC327", en: "BC327 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_s8550: { prefix: "QS8550", ar: "ترانزستور S8550", en: "S8550 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_a1015: { prefix: "QA1015", ar: "ترانزستور A1015", en: "A1015 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_tip42c: { prefix: "QTI42C", ar: "ترانزستور TIP42C", en: "TIP42C PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_2sa1943: { prefix: "Q2S943", ar: "ترانزستور 2SA1943", en: "2SA1943 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_2n5401: { prefix: "Q2N401", ar: "ترانزستور 2N5401", en: "2N5401 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_mpsa92: { prefix: "QMPA92", ar: "ترانزستور MPSA92", en: "MPSA92 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_bc640: { prefix: "QBC640", ar: "ترانزستور BC640", en: "BC640 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  q_bd138: { prefix: "QBD138", ar: "ترانزستور BD138", en: "BD138 PNP", vals: ["PNP"], def: "PNP", pins: 3 },
  m_irf520: { prefix: "MIR520", ar: "MOSFET IRF520", en: "IRF520 MOSFET", vals: ["IRF520"], def: "IRF520", pins: 3 },
  m_irf640: { prefix: "MIR640", ar: "MOSFET IRF640", en: "IRF640 MOSFET", vals: ["IRF640"], def: "IRF640", pins: 3 },
  m_irfz44n: { prefix: "MIR44N", ar: "MOSFET IRFZ44N", en: "IRFZ44N MOSFET", vals: ["IRFZ44N"], def: "IRFZ44N", pins: 3 },
  m_irf1404: { prefix: "MIR404", ar: "MOSFET IRF1404", en: "IRF1404 MOSFET", vals: ["IRF1404"], def: "IRF1404", pins: 3 },
  m_ao3400: { prefix: "MAO400", ar: "MOSFET AO3400", en: "AO3400 MOSFET", vals: ["AO3400"], def: "AO3400", pins: 3 },
  m_fqp30n06: { prefix: "MFQN06", ar: "MOSFET FQP30N06", en: "FQP30N06 MOSFET", vals: ["FQP30N06"], def: "FQP30N06", pins: 3 },
  m_stp55nf06: { prefix: "MSTF06", ar: "MOSFET STP55NF06", en: "STP55NF06 MOSFET", vals: ["STP55NF06"], def: "STP55NF06", pins: 3 },
  m_irlml2502: { prefix: "MIR502", ar: "MOSFET IRLML2502", en: "IRLML2502 MOSFET", vals: ["IRLML2502"], def: "IRLML2502", pins: 3 },
  m_irf530: { prefix: "MIR530", ar: "MOSFET IRF530", en: "IRF530 MOSFET", vals: ["IRF530"], def: "IRF530", pins: 3 },
  m_irlb3034: { prefix: "MIR034", ar: "MOSFET IRLB3034", en: "IRLB3034 MOSFET", vals: ["IRLB3034"], def: "IRLB3034", pins: 3 },
  m_si2302: { prefix: "MSI302", ar: "MOSFET SI2302", en: "SI2302 MOSFET", vals: ["SI2302"], def: "SI2302", pins: 3 },
  m_bss138: { prefix: "MBS138", ar: "MOSFET BSS138", en: "BSS138 MOSFET", vals: ["BSS138"], def: "BSS138", pins: 3 },
  toroid_inductor: { prefix: "TORTOR", ar: "ملف حلقي", en: "Toroid Inductor", vals: [10, 100, 1000, 4700], def: 100 },
  air_coil: { prefix: "AIROIL", ar: "ملف هوائي", en: "Air Coil", vals: [0.001, 0.01, 0.1], def: 0.01 },
  smd_inductor: { prefix: "SMDTO2", ar: "ملف SMD", en: "SMD Inductor", vals: [1, 4.7, 10, 47], def: 10 },
  common_mode_choke: { prefix: "COMOKE", ar: "خانق وضع مشترك", en: "Common-Mode Choke", vals: [10, 100, 1000], def: 100 },
  incandescent_lamp: { prefix: "INCAMP", ar: "مصباح متوهج", en: "Incandescent Lamp", vals: [10, 25, 60], def: 25 },
  led_bulb: { prefix: "LEDULB", ar: "مصباح LED", en: "LED Bulb", vals: [5, 10, 20], def: 10 },
  heating_element: { prefix: "HEAENT", ar: "عنصر تسخين", en: "Heating Element", vals: [10, 25, 50], def: 25 },
  water_pump: { prefix: "WATUMP", ar: "مضخة ماء", en: "Water Pump", vals: [5, 10, 20], def: 10 },
  n20_motor: { prefix: "N20TOR", ar: "محرك N20", en: "N20 Motor", vals: [5, 10], def: 5 },
  gear_motor: { prefix: "GEATOR", ar: "محرك بتروس", en: "Gear Motor", vals: [5, 10, 20], def: 10 },
  mini_speaker: { prefix: "MINKER", ar: "سماعة صغيرة", en: "Mini Speaker", vals: [4, 8], def: 8 },
  woofer: { prefix: "WOOFER", ar: "ووفر", en: "Woofer", vals: [4, 8], def: 8 },
  tweeter: { prefix: "TWETER", ar: "تويتر", en: "Tweeter", vals: [4, 8, 16], def: 8 },
  active_buzzer: { prefix: "ACTZER", ar: "جرس نشط", en: "Active Buzzer", vals: [50, 100, 200], def: 100 },
  passive_buzzer: { prefix: "PASZER", ar: "جرس سلبي", en: "Passive Buzzer", vals: [50, 100, 200], def: 100 },
  siren: { prefix: "SIREN", ar: "صفارة إنذار", en: "Siren", vals: [100, 200], def: 100 },
  dip_switch: { prefix: "DIPTCH", ar: "مفتاح DIP", en: "DIP Switch", vals: [], def: 0 },
  rocker_switch: { prefix: "ROCTCH", ar: "مفتاح بسيط", en: "Rocker Switch", vals: [], def: 0 },
  key_switch: { prefix: "KEYTCH", ar: "مفتاح بمفتاح", en: "Key Switch", vals: [], def: 0 },
  micro_switch: { prefix: "MICTCH", ar: "مفتاح مايكرو", en: "Micro Switch", vals: [], def: 0 },
  foot_switch: { prefix: "FOOTCH", ar: "مفتاح قدم", en: "Foot Switch", vals: [], def: 0 },
  selector_switch: { prefix: "SELTCH", ar: "مفتاح اختيار", en: "Selector Switch", vals: [], def: 0 },
  li_ion_18650: { prefix: "LII650", ar: "بطارية 18650", en: "18650 Li-ion", vals: [3.7], def: 3.7 },
  nimh_pack: { prefix: "NIMACK", ar: "حزمة NiMH", en: "NiMH Pack", vals: [4.8, 6, 9.6, 12], def: 4.8 },
  car_battery: { prefix: "CARERY", ar: "بطارية سيارة", en: "Car Battery", vals: [12], def: 12 },
  wall_adapter: { prefix: "WALTER", ar: "محول جداري DC", en: "Wall Adapter", vals: [5, 9, 12, 24], def: 12 },
  solar_panel_5v: { prefix: "SOLL5V", ar: "لوح شمسي", en: "Solar Panel", vals: [5, 6, 9], def: 6 },
  usb_c_pd: { prefix: "USBCPD", ar: "مصدر USB-C PD", en: "USB-C PD", vals: [5, 9, 12, 15, 20], def: 9 },
  powerbank: { prefix: "POWANK", ar: "باور بانك", en: "Power Bank", vals: [5], def: 5 },
  dry_cell_d: { prefix: "DRYLLD", ar: "بطارية D", en: "D Cell", vals: [1.5], def: 1.5 },
  lifepo4: { prefix: "LIFPO4", ar: "بطارية LiFePO4", en: "LiFePO4", vals: [3.2, 6.4, 12.8], def: 3.2 },
  button_cell_lr44: { prefix: "BUTR44", ar: "بطارية LR44", en: "LR44 Cell", vals: [1.5], def: 1.5 },
  ac_transformer: { prefix: "ACTMER", ar: "محول متردد", en: "AC Transformer", vals: [5, 12, 24], def: 12 },
  ac_generator: { prefix: "ACGTOR", ar: "مولد متردد", en: "AC Generator", vals: [5, 12, 24], def: 12 },
  tmp116: { prefix: "TMP116", ar: "TMP116 حرارة", en: "TMP116 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  tmp1075: { prefix: "TMP075", ar: "TMP1075 حرارة", en: "TMP1075 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  max6633: { prefix: "MAX633", ar: "MAX6633 حرارة", en: "MAX6633 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  mcp9701: { prefix: "MCP701", ar: "MCP9701 حرارة", en: "MCP9701 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  lm19: { prefix: "LM19", ar: "LM19 حرارة", en: "LM19 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  lm34: { prefix: "LM34", ar: "LM34 حرارة", en: "LM34 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  lm335: { prefix: "LM335", ar: "LM335 حرارة", en: "LM335 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  ad590: { prefix: "AD590", ar: "AD590 حرارة", en: "AD590 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  tmp35: { prefix: "TMP35", ar: "TMP35 حرارة", en: "TMP35 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  tmp37: { prefix: "TMP37", ar: "TMP37 حرارة", en: "TMP37 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  sts31: { prefix: "STS31", ar: "STS31 حرارة", en: "STS31 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  stlm20: { prefix: "STLM20", ar: "STLM20 حرارة", en: "STLM20 Temp", vals: [-20, 0, 25, 50, 85], def: 25, pins: 3 },
  sht85: { prefix: "SHT85", ar: "SHT85 رطوبة", en: "SHT85 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  hih7130: { prefix: "HIH132", ar: "HIH7130 رطوبة", en: "HIH7130 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  hts221: { prefix: "HTS221", ar: "HTS221 رطوبة", en: "HTS221 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  hdc3020: { prefix: "HDC020", ar: "HDC3020 رطوبة", en: "HDC3020 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  shtc3: { prefix: "SHTC3", ar: "SHTC3 رطوبة", en: "SHTC3 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  shtc1: { prefix: "SHTC1", ar: "SHTC1 رطوبة", en: "SHTC1 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  si7020: { prefix: "SI7020", ar: "SI7020 رطوبة", en: "SI7020 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  am2301: { prefix: "AM2301", ar: "AM2301 رطوبة", en: "AM2301 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  am2302: { prefix: "AM2302", ar: "AM2302 رطوبة", en: "AM2302 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  capacitive_soil: { prefix: "CAPOIL", ar: "CAPACITIVE-SOIL رطوبة", en: "CAPACITIVE-SOIL Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  fc28: { prefix: "FC28", ar: "FC28 رطوبة", en: "FC28 Humidity", vals: [20, 40, 60, 80], def: 40, pins: 3 },
  lps22hh: { prefix: "LPS2HH", ar: "LPS22HH ضغط", en: "LPS22HH Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  mpl115a2: { prefix: "MPL5A2", ar: "MPL115A2 ضغط", en: "MPL115A2 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  ms5803: { prefix: "MS5803", ar: "MS5803 ضغط", en: "MS5803 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  ms5607: { prefix: "MS5607", ar: "MS5607 ضغط", en: "MS5607 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  mprls: { prefix: "MPRLS", ar: "MPRLS ضغط", en: "MPRLS Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  bmp384: { prefix: "BMP384", ar: "BMP384 ضغط", en: "BMP384 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  icp10125: { prefix: "ICP125", ar: "ICP10125 ضغط", en: "ICP10125 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  icp20100: { prefix: "ICP100", ar: "ICP20100 ضغط", en: "ICP20100 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  mpx4115: { prefix: "MPX115", ar: "MPX4115 ضغط", en: "MPX4115 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  mpxv7002: { prefix: "MPX002", ar: "MPXV7002 ضغط", en: "MPXV7002 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  xgzp6847: { prefix: "XGZ847", ar: "XGZP6847 ضغط", en: "XGZP6847 Pressure", vals: [300, 600, 1013, 1100], def: 1013, pins: 3 },
  mq136: { prefix: "MQ136", ar: "MQ136 غاز", en: "MQ136 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mq139: { prefix: "MQ139", ar: "MQ139 غاز", en: "MQ139 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mq309: { prefix: "MQ309", ar: "MQ309 غاز", en: "MQ309 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  tgs2600: { prefix: "TGS600", ar: "TGS2600 غاز", en: "TGS2600 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  tgs2602: { prefix: "TGS602", ar: "TGS2602 غاز", en: "TGS2602 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  tgs2620: { prefix: "TGS620", ar: "TGS2620 غاز", en: "TGS2620 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mics5524: { prefix: "MIC524", ar: "MICS5524 غاز", en: "MICS5524 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mics6814: { prefix: "MIC814", ar: "MICS6814 غاز", en: "MICS6814 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mh_z14a: { prefix: "MHZ14A", ar: "MH-Z14A غاز", en: "MH-Z14A Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  mh_z16: { prefix: "MHZ16", ar: "MH-Z16 غاز", en: "MH-Z16 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  s8_co2: { prefix: "S8CO2", ar: "S8-CO2 غاز", en: "S8-CO2 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  iaq_core: { prefix: "IAQORE", ar: "IAQ-CORE غاز", en: "IAQ-CORE Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  zmod4410: { prefix: "ZMO410", ar: "ZMOD4410 غاز", en: "ZMOD4410 Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  zh03b: { prefix: "ZH03B", ar: "ZH03B غاز", en: "ZH03B Gas", vals: [0, 100, 400, 1000, 2000], def: 400, pins: 3 },
  tsl2572: { prefix: "TSL572", ar: "TSL2572 ضوء", en: "TSL2572 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  veml3235: { prefix: "VEM235", ar: "VEML3235 ضوء", en: "VEML3235 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  opt4048: { prefix: "OPT048", ar: "OPT4048 ضوء", en: "OPT4048 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  opt3004: { prefix: "OPT004", ar: "OPT3004 ضوء", en: "OPT3004 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  ltr390: { prefix: "LTR390", ar: "LTR390 ضوء", en: "LTR390 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  ltr303: { prefix: "LTR303", ar: "LTR303 ضوء", en: "LTR303 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  ltr559: { prefix: "LTR559", ar: "LTR559 ضوء", en: "LTR559 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  as7343: { prefix: "AS7343", ar: "AS7343 ضوء", en: "AS7343 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  as7265x: { prefix: "AS765X", ar: "AS7265X ضوء", en: "AS7265X Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  ap3216: { prefix: "AP3216", ar: "AP3216 ضوء", en: "AP3216 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  vcnl4200: { prefix: "VCN200", ar: "VCNL4200 ضوء", en: "VCNL4200 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  si1133: { prefix: "SI1133", ar: "SI1133 ضوء", en: "SI1133 Light", vals: [0, 100, 1000, 10000, 65000], def: 1000, pins: 3 },
  mpu6886: { prefix: "MPU886", ar: "MPU6886 حركة", en: "MPU6886 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  mpu9255: { prefix: "MPU255", ar: "MPU9255 حركة", en: "MPU9255 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lsm6dso: { prefix: "LSMDSO", ar: "LSM6DSO حركة", en: "LSM6DSO Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lsm6dsox: { prefix: "LSMSOX", ar: "LSM6DSOX حركة", en: "LSM6DSOX Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lis3mdl: { prefix: "LISMDL", ar: "LIS3MDL حركة", en: "LIS3MDL Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lis2mdl: { prefix: "LISMD2", ar: "LIS2MDL حركة", en: "LIS2MDL Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  lis3dsh: { prefix: "LISDSH", ar: "LIS3DSH حركة", en: "LIS3DSH Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  mma7660: { prefix: "MMA660", ar: "MMA7660 حركة", en: "MMA7660 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  mma8451: { prefix: "MMA451", ar: "MMA8451 حركة", en: "MMA8451 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  mma7361: { prefix: "MMA361", ar: "MMA7361 حركة", en: "MMA7361 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  bma280: { prefix: "BMA280", ar: "BMA280 حركة", en: "BMA280 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  bma423: { prefix: "BMA423", ar: "BMA423 حركة", en: "BMA423 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  bmi088: { prefix: "BMI088", ar: "BMI088 حركة", en: "BMI088 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  bmx160: { prefix: "BMX160", ar: "BMX160 حركة", en: "BMX160 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  icm20689: { prefix: "ICM689", ar: "ICM20689 حركة", en: "ICM20689 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  icm42605: { prefix: "ICM605", ar: "ICM42605 حركة", en: "ICM42605 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  fxos8700: { prefix: "FXO700", ar: "FXOS8700 حركة", en: "FXOS8700 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  fxas21002: { prefix: "FXA002", ar: "FXAS21002 حركة", en: "FXAS21002 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  l3g4200d: { prefix: "L3G00D", ar: "L3G4200D حركة", en: "L3G4200D Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  itg3200: { prefix: "ITG200", ar: "ITG3200 حركة", en: "ITG3200 Motion", vals: [0, 1, 2, 8, 16], def: 1, pins: 3 },
  vl53l4cd: { prefix: "VL54CD", ar: "VL53L4CD مسافة", en: "VL53L4CD Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  vl53l3cx: { prefix: "VL53CX", ar: "VL53L3CX مسافة", en: "VL53L3CX Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  tof050c: { prefix: "TOF50C", ar: "TOF050C مسافة", en: "TOF050C Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  tf02: { prefix: "TF02", ar: "TF02 مسافة", en: "TF02 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  tf03: { prefix: "TF03", ar: "TF03 مسافة", en: "TF03 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  hcsr05: { prefix: "HCSR05", ar: "HCSR05 مسافة", en: "HCSR05 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  srf05: { prefix: "SRF05", ar: "SRF05 مسافة", en: "SRF05 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  maxsonar_ez1: { prefix: "MAXEZ1", ar: "MAXSONAR-EZ1 مسافة", en: "MAXSONAR-EZ1 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  us015: { prefix: "US015", ar: "US015 مسافة", en: "US015 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  us020: { prefix: "US020", ar: "US020 مسافة", en: "US020 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  urm37: { prefix: "URM37", ar: "URM37 مسافة", en: "URM37 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  ld2450: { prefix: "LD2450", ar: "LD2450 مسافة", en: "LD2450 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  ld2420: { prefix: "LD2420", ar: "LD2420 مسافة", en: "LD2420 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  hb100: { prefix: "HB100", ar: "HB100 مسافة", en: "HB100 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  sen0311: { prefix: "SEN311", ar: "SEN0311 مسافة", en: "SEN0311 Distance", vals: [5, 20, 100, 200, 400], def: 100, pins: 3 },
  max30101: { prefix: "MAX101", ar: "MAX30101 حيوي", en: "MAX30101 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  max86150: { prefix: "MAX150", ar: "MAX86150 حيوي", en: "MAX86150 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  afe4490: { prefix: "AFE490", ar: "AFE4490 حيوي", en: "AFE4490 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  ads1292: { prefix: "ADS292", ar: "ADS1292 حيوي", en: "ADS1292 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  ad8233: { prefix: "AD8233", ar: "AD8233 حيوي", en: "AD8233 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  max30003: { prefix: "MAX003", ar: "MAX30003 حيوي", en: "MAX30003 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  emg_sensor: { prefix: "EMGSOR", ar: "EMG-SENSOR حيوي", en: "EMG-SENSOR Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  muscle_v3: { prefix: "MUSEV3", ar: "MUSCLE-V3 حيوي", en: "MUSCLE-V3 Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  gsr_grove: { prefix: "GSROVE", ar: "GSR-GROVE حيوي", en: "GSR-GROVE Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  skin_temp_mlx: { prefix: "SKIMLX", ar: "SKIN-TEMP-MLX حيوي", en: "SKIN-TEMP-MLX Biosensor", vals: [40, 60, 80, 120, 180], def: 80, pins: 3 },
  ina180: { prefix: "INA180", ar: "INA180 تيار", en: "INA180 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ina199: { prefix: "INA199", ar: "INA199 تيار", en: "INA199 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ina210: { prefix: "INA210", ar: "INA210 تيار", en: "INA210 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ina230: { prefix: "INA230", ar: "INA230 تيار", en: "INA230 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ina233: { prefix: "INA233", ar: "INA233 تيار", en: "INA233 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  acs711: { prefix: "ACS711", ar: "ACS711 تيار", en: "ACS711 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  acs723: { prefix: "ACS723", ar: "ACS723 تيار", en: "ACS723 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  acs724: { prefix: "ACS724", ar: "ACS724 تيار", en: "ACS724 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  acs781: { prefix: "ACS781", ar: "ACS781 تيار", en: "ACS781 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  max9611: { prefix: "MAX611", ar: "MAX9611 تيار", en: "MAX9611 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ltc4151: { prefix: "LTC151", ar: "LTC4151 تيار", en: "LTC4151 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ltc2945: { prefix: "LTC945", ar: "LTC2945 تيار", en: "LTC2945 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  pac1934: { prefix: "PAC934", ar: "PAC1934 تيار", en: "PAC1934 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  bl0937: { prefix: "BL0937", ar: "BL0937 تيار", en: "BL0937 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  pzem017: { prefix: "PZE017", ar: "PZEM017 تيار", en: "PZEM017 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  ade7753: { prefix: "ADE753", ar: "ADE7753 تيار", en: "ADE7753 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  atm90e26: { prefix: "ATME26", ar: "ATM90E26 تيار", en: "ATM90E26 Current", vals: [0, 0.5, 1, 5, 10, 30], def: 1, pins: 3 },
  hmc5983: { prefix: "HMC983", ar: "HMC5983 مغناطيس", en: "HMC5983 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  mmc5603: { prefix: "MMC603", ar: "MMC5603 مغناطيس", en: "MMC5603 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  mmc5983ma: { prefix: "MMC3MA", ar: "MMC5983MA مغناطيس", en: "MMC5983MA Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  ak8963: { prefix: "AK8963", ar: "AK8963 مغناطيس", en: "AK8963 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  ak09916: { prefix: "AK0916", ar: "AK09916 مغناطيس", en: "AK09916 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  qmc6310: { prefix: "QMC310", ar: "QMC6310 مغناطيس", en: "QMC6310 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  bmm150: { prefix: "BMM150", ar: "BMM150 مغناطيس", en: "BMM150 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  tmag5273: { prefix: "TMA273", ar: "TMAG5273 مغناطيس", en: "TMAG5273 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  tlv493d: { prefix: "TLV93D", ar: "TLV493D مغناطيس", en: "TLV493D Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  a1324: { prefix: "A1324", ar: "A1324 مغناطيس", en: "A1324 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  ss495a: { prefix: "SS495A", ar: "SS495A مغناطيس", en: "SS495A Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  drv5055: { prefix: "DRV055", ar: "DRV5055 مغناطيس", en: "DRV5055 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  as5047p: { prefix: "AS547P", ar: "AS5047P مغناطيس", en: "AS5047P Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  ma730: { prefix: "MA730", ar: "MA730 مغناطيس", en: "MA730 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  mt6701: { prefix: "MT6701", ar: "MT6701 مغناطيس", en: "MT6701 Magnetic", vals: [0, 50, 100, 200, 400], def: 50, pins: 3 },
  max9814: { prefix: "MAX814", ar: "MAX9814 صوت", en: "MAX9814 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  max4466: { prefix: "MAX466", ar: "MAX4466 صوت", en: "MAX4466 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  ics43434: { prefix: "ICS434", ar: "ICS43434 صوت", en: "ICS43434 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  inmp441: { prefix: "INM441", ar: "INMP441 صوت", en: "INMP441 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  sph0645: { prefix: "SPH645", ar: "SPH0645 صوت", en: "SPH0645 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  spm0405: { prefix: "SPM405", ar: "SPM0405 صوت", en: "SPM0405 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  mp34dt05: { prefix: "MP3T05", ar: "MP34DT05 صوت", en: "MP34DT05 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  ky037: { prefix: "KY037", ar: "KY037 صوت", en: "KY037 Sound", vals: [30, 50, 70, 90, 120], def: 50, pins: 3 },
  fsr402: { prefix: "FSR402", ar: "FSR402 قوة", en: "FSR402 Force", vals: [0, 10, 50, 100], def: 10, pins: 3 },
  fsr406: { prefix: "FSR406", ar: "FSR406 قوة", en: "FSR406 Force", vals: [0, 10, 50, 100], def: 10, pins: 3 },
  load_cell_5kg: { prefix: "LOA5KG", ar: "LOAD-CELL-5KG قوة", en: "LOAD-CELL-5KG Force", vals: [0, 10, 50, 100], def: 10, pins: 3 },
  load_cell_20kg: { prefix: "LOA0KG", ar: "LOAD-CELL-20KG قوة", en: "LOAD-CELL-20KG Force", vals: [0, 10, 50, 100], def: 10, pins: 3 },
  piezo_film: { prefix: "PIEILM", ar: "PIEZO-FILM قوة", en: "PIEZO-FILM Force", vals: [0, 10, 50, 100], def: 10, pins: 3 },
  flex_4in: { prefix: "FLE4IN", ar: "FLEX-4IN قوة", en: "FLEX-4IN Force", vals: [0, 10, 50, 100], def: 10, pins: 3 },
  yfs201: { prefix: "YFS201", ar: "YFS201 تدفق", en: "YFS201 Flow", vals: [0, 1, 5, 10, 30], def: 5, pins: 3 },
  yfs401: { prefix: "YFS401", ar: "YFS401 تدفق", en: "YFS401 Flow", vals: [0, 1, 5, 10, 30], def: 5, pins: 3 },
  yfs210: { prefix: "YFS210", ar: "YFS210 تدفق", en: "YFS210 Flow", vals: [0, 1, 5, 10, 30], def: 5, pins: 3 },
  yfb08: { prefix: "YFB08", ar: "YFB08 تدفق", en: "YFB08 Flow", vals: [0, 1, 5, 10, 30], def: 5, pins: 3 },
  fs300a: { prefix: "FS300A", ar: "FS300A تدفق", en: "FS300A Flow", vals: [0, 1, 5, 10, 30], def: 5, pins: 3 },
  fs400a: { prefix: "FS400A", ar: "FS400A تدفق", en: "FS400A Flow", vals: [0, 1, 5, 10, 30], def: 5, pins: 3 },
  float_switch: { prefix: "FLOTCH", ar: "FLOAT-SWITCH مستوى", en: "FLOAT-SWITCH Level", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  ultrasonic_level: { prefix: "ULTVEL", ar: "ULTRASONLEVEL مستوى", en: "ULTRASONLEVEL Level", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  capacitive_level: { prefix: "CAPVEL", ar: "CAPACITIVE-LEVEL مستوى", en: "CAPACITIVE-LEVEL Level", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  optical_level: { prefix: "OPTVEL", ar: "OPTICAL-LEVEL مستوى", en: "OPTICAL-LEVEL Level", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  soil_moisture_v2: { prefix: "SOIEV2", ar: "SOIL-MOISTURE-V2 مستوى", en: "SOIL-MOISTURE-V2 Level", vals: [0, 25, 50, 75, 100], def: 50, pins: 3 },
  st7567: { prefix: "ST7567", ar: "ST7567 شاشة", en: "ST7567 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  st7789_135: { prefix: "ST7135", ar: "ST7789-135 شاشة", en: "ST7789-135 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  st7735_80: { prefix: "ST7580", ar: "ST7735-80 شاشة", en: "ST7735-80 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ili9163: { prefix: "ILI163", ar: "ILI9163 شاشة", en: "ILI9163 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ili9327: { prefix: "ILI327", ar: "ILI9327 شاشة", en: "ILI9327 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ili9342: { prefix: "ILI342", ar: "ILI9342 شاشة", en: "ILI9342 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ili9806: { prefix: "ILI806", ar: "ILI9806 شاشة", en: "ILI9806 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  hx8357: { prefix: "HX8357", ar: "HX8357 شاشة", en: "HX8357 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  hx8347: { prefix: "HX8347", ar: "HX8347 شاشة", en: "HX8347 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ra8875: { prefix: "RA8875", ar: "RA8875 شاشة", en: "RA8875 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ssd1289: { prefix: "SSD289", ar: "SSD1289 شاشة", en: "SSD1289 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ssd2119: { prefix: "SSD119", ar: "SSD2119 شاشة", en: "SSD2119 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  sed1520: { prefix: "SED520", ar: "SED1520 شاشة", en: "SED1520 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  ks0108: { prefix: "KS0108", ar: "KS0108 شاشة", en: "KS0108 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  pcd8544: { prefix: "PCD544", ar: "PCD8544 شاشة", en: "PCD8544 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  uc1701: { prefix: "UC1701", ar: "UC1701 شاشة", en: "UC1701 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  uc1609: { prefix: "UC1609", ar: "UC1609 شاشة", en: "UC1609 Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  t6963c: { prefix: "T6963C", ar: "T6963C شاشة", en: "T6963C Display", vals: ["Hi", "OK", "Menu", "Err"], def: "Hi", pins: 3 },
  drv8701: { prefix: "DRV701", ar: "DRV8701 تشغيل محرك", en: "DRV8701 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  drv8424: { prefix: "DRV424", ar: "DRV8424 تشغيل محرك", en: "DRV8424 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  drv8428: { prefix: "DRV428", ar: "DRV8428 تشغيل محرك", en: "DRV8428 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2100: { prefix: "TMC100", ar: "TMC2100 تشغيل محرك", en: "TMC2100 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2226: { prefix: "TMC226", ar: "TMC2226 تشغيل محرك", en: "TMC2226 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2225: { prefix: "TMC225", ar: "TMC2225 تشغيل محرك", en: "TMC2225 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2240: { prefix: "TMC240", ar: "TMC2240 تشغيل محرك", en: "TMC2240 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tmc2660: { prefix: "TMC660", ar: "TMC2660 تشغيل محرك", en: "TMC2660 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  a4982: { prefix: "A4982", ar: "A4982 تشغيل محرك", en: "A4982 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  a4983: { prefix: "A4983", ar: "A4983 تشغيل محرك", en: "A4983 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  l6219: { prefix: "L6219", ar: "L6219 تشغيل محرك", en: "L6219 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  l297: { prefix: "L297", ar: "L297 تشغيل محرك", en: "L297 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  l298p: { prefix: "L298P", ar: "L298P تشغيل محرك", en: "L298P Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tb6560: { prefix: "TB6560", ar: "TB6560 تشغيل محرك", en: "TB6560 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tb6600: { prefix: "TB6600", ar: "TB6600 تشغيل محرك", en: "TB6600 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  tb67s109: { prefix: "TB6109", ar: "TB67S109 تشغيل محرك", en: "TB67S109 Motor Driver", vals: ["FWD", "REV", "STOP"], def: "FWD", pins: 3 },
  lm78m05: { prefix: "LM7M05", ar: "LM78M05 منظم", en: "LM78M05 Regulator", vals: [5], def: 5, pins: 3 },
  lm2937: { prefix: "LM2937", ar: "LM2937 منظم", en: "LM2937 Regulator", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm2931: { prefix: "LM2931", ar: "LM2931 منظم", en: "LM2931 Regulator", vals: [3.3, 5], def: 5, pins: 3 },
  lm1086: { prefix: "LM1086", ar: "LM1086 منظم", en: "LM1086 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  lm1085: { prefix: "LM1085", ar: "LM1085 منظم", en: "LM1085 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  lt1763: { prefix: "LT1763", ar: "LT1763 منظم", en: "LT1763 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  lt1963: { prefix: "LT1963", ar: "LT1963 منظم", en: "LT1963 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  lt3042: { prefix: "LT3042", ar: "LT3042 منظم", en: "LT3042 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  tps7a20: { prefix: "TPSA20", ar: "TPS7A20 منظم", en: "TPS7A20 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  tps73401: { prefix: "TPS401", ar: "TPS73401 منظم", en: "TPS73401 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  adp150: { prefix: "ADP150", ar: "ADP150 منظم", en: "ADP150 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  adp3338: { prefix: "ADP338", ar: "ADP3338 منظم", en: "ADP3338 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  mcp1802: { prefix: "MCP802", ar: "MCP1802 منظم", en: "MCP1802 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  mcp1826: { prefix: "MCP826", ar: "MCP1826 منظم", en: "MCP1826 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  ap7361: { prefix: "AP7361", ar: "AP7361 منظم", en: "AP7361 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  ap7333: { prefix: "AP7333", ar: "AP7333 منظم", en: "AP7333 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  rt9013: { prefix: "RT9013", ar: "RT9013 منظم", en: "RT9013 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  ld39050: { prefix: "LD3050", ar: "LD39050 منظم", en: "LD39050 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  tlv70033: { prefix: "TLV033", ar: "TLV70033 منظم", en: "TLV70033 Regulator", vals: [1.8, 3.3, 5], def: 3.3, pins: 3 },
  lm22676: { prefix: "LM2676", ar: "LM22676 محول", en: "LM22676 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm2672: { prefix: "LM2672", ar: "LM2672 محول", en: "LM2672 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm2674: { prefix: "LM2674", ar: "LM2674 محول", en: "LM2674 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm5008: { prefix: "LM5008", ar: "LM5008 محول", en: "LM5008 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  lm5164: { prefix: "LM5164", ar: "LM5164 محول", en: "LM5164 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  ltc3630: { prefix: "LTC630", ar: "LTC3630 محول", en: "LTC3630 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  ltc3115: { prefix: "LTC115", ar: "LTC3115 محول", en: "LTC3115 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  tps54360: { prefix: "TPS360", ar: "TPS54360 محول", en: "TPS54360 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  tps62130: { prefix: "TPS130", ar: "TPS62130 محول", en: "TPS62130 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  tps62160: { prefix: "TPS160", ar: "TPS62160 محول", en: "TPS62160 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  tps62933: { prefix: "TPS933", ar: "TPS62933 محول", en: "TPS62933 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  mp1470: { prefix: "MP1470", ar: "MP1470 محول", en: "MP1470 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  mp2359: { prefix: "MP2359", ar: "MP2359 محول", en: "MP2359 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  mp2491: { prefix: "MP2491", ar: "MP2491 محول", en: "MP2491 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  xl1509: { prefix: "XL1509", ar: "XL1509 محول", en: "XL1509 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  xl2596: { prefix: "XL2596", ar: "XL2596 محول", en: "XL2596 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  mc34063: { prefix: "MC3063", ar: "MC34063 محول", en: "MC34063 Converter", vals: [3.3, 5, 12], def: 5, pins: 3 },
  tps63020: { prefix: "TPS020", ar: "TPS63020 رافع", en: "TPS63020 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  tps61088: { prefix: "TPS088", ar: "TPS61088 رافع", en: "TPS61088 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  tps61230: { prefix: "TPS230", ar: "TPS61230 رافع", en: "TPS61230 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  mp3429: { prefix: "MP3429", ar: "MP3429 رافع", en: "MP3429 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  xl6019: { prefix: "XL6019", ar: "XL6019 رافع", en: "XL6019 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  xl6012: { prefix: "XL6012", ar: "XL6012 رافع", en: "XL6012 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  ap3012: { prefix: "AP3012", ar: "AP3012 رافع", en: "AP3012 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  lm2621: { prefix: "LM2621", ar: "LM2621 رافع", en: "LM2621 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  lm3478: { prefix: "LM3478", ar: "LM3478 رافع", en: "LM3478 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  tps55340: { prefix: "TPS340", ar: "TPS55340 رافع", en: "TPS55340 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  tps61200: { prefix: "TPS200", ar: "TPS61200 رافع", en: "TPS61200 Boost", vals: [5, 9, 12, 24], def: 9, pins: 3 },
  tp4057: { prefix: "TP4057", ar: "TP4057 شاحن", en: "TP4057 Charger", vals: [4.2], def: 4.2, pins: 3 },
  tp4054: { prefix: "TP4054", ar: "TP4054 شاحن", en: "TP4054 Charger", vals: [4.2], def: 4.2, pins: 3 },
  mcp73831: { prefix: "MCP831", ar: "MCP73831 شاحن", en: "MCP73831 Charger", vals: [4.2], def: 4.2, pins: 3 },
  mcp73832: { prefix: "MCP832", ar: "MCP73832 شاحن", en: "MCP73832 Charger", vals: [4.2], def: 4.2, pins: 3 },
  bq24072: { prefix: "BQ2072", ar: "BQ24072 شاحن", en: "BQ24072 Charger", vals: [4.2], def: 4.2, pins: 3 },
  bq24075: { prefix: "BQ2075", ar: "BQ24075 شاحن", en: "BQ24075 Charger", vals: [4.2], def: 4.2, pins: 3 },
  bq25606: { prefix: "BQ2606", ar: "BQ25606 شاحن", en: "BQ25606 Charger", vals: [4.2], def: 4.2, pins: 3 },
  bq25895: { prefix: "BQ2895", ar: "BQ25895 شاحن", en: "BQ25895 Charger", vals: [4.2], def: 4.2, pins: 3 },
  ltc4054: { prefix: "LTC054", ar: "LTC4054 شاحن", en: "LTC4054 Charger", vals: [4.2], def: 4.2, pins: 3 },
  ltc4065: { prefix: "LTC065", ar: "LTC4065 شاحن", en: "LTC4065 Charger", vals: [4.2], def: 4.2, pins: 3 },
  cn3722: { prefix: "CN3722", ar: "CN3722 شاحن", en: "CN3722 Charger", vals: [4.2], def: 4.2, pins: 3 },
  cn3765: { prefix: "CN3765", ar: "CN3765 شاحن", en: "CN3765 Charger", vals: [4.2], def: 4.2, pins: 3 },
  ip2312: { prefix: "IP2312", ar: "IP2312 شاحن", en: "IP2312 Charger", vals: [4.2], def: 4.2, pins: 3 },
  ip5310: { prefix: "IP5310", ar: "IP5310 شاحن", en: "IP5310 Charger", vals: [4.2], def: 4.2, pins: 3 },
  esp32_wroom: { prefix: "ESPOOM", ar: "ESP32-WROOM اتصال", en: "ESP32-WROOM Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  esp32_s2: { prefix: "ESP2S2", ar: "ESP32-S2 اتصال", en: "ESP32-S2 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  esp32_c6: { prefix: "ESP2C6", ar: "ESP32-C6 اتصال", en: "ESP32-C6 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  esp12f: { prefix: "ESP12F", ar: "ESP12F اتصال", en: "ESP12F Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  esp12e: { prefix: "ESP12E", ar: "ESP12E اتصال", en: "ESP12E Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  esp07: { prefix: "ESP07", ar: "ESP07 اتصال", en: "ESP07 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  bl602: { prefix: "BL602", ar: "BL602 اتصال", en: "BL602 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  rtl8710: { prefix: "RTL710", ar: "RTL8710 اتصال", en: "RTL8710 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  rtl8720dn: { prefix: "RTL0DN", ar: "RTL8720DN اتصال", en: "RTL8720DN Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  nrf51822: { prefix: "NRF822", ar: "NRF51822 اتصال", en: "NRF51822 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  nrf52810: { prefix: "NRF810", ar: "NRF52810 اتصال", en: "NRF52810 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  nrf5340: { prefix: "NRF340", ar: "NRF5340 اتصال", en: "NRF5340 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  nrf9160: { prefix: "NRF160", ar: "NRF9160 اتصال", en: "NRF9160 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc2530: { prefix: "CC2530", ar: "CC2530 اتصال", en: "CC2530 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc2531: { prefix: "CC2531", ar: "CC2531 اتصال", en: "CC2531 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc2640: { prefix: "CC2640", ar: "CC2640 اتصال", en: "CC2640 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc2652: { prefix: "CC2652", ar: "CC2652 اتصال", en: "CC2652 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc3200: { prefix: "CC3200", ar: "CC3200 اتصال", en: "CC3200 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc1310: { prefix: "CC1310", ar: "CC1310 اتصال", en: "CC1310 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc1125: { prefix: "CC1125", ar: "CC1125 اتصال", en: "CC1125 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cc2500: { prefix: "CC2500", ar: "CC2500 اتصال", en: "CC2500 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  si4432: { prefix: "SI4432", ar: "SI4432 اتصال", en: "SI4432 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  si4463: { prefix: "SI4463", ar: "SI4463 اتصال", en: "SI4463 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  si4455: { prefix: "SI4455", ar: "SI4455 اتصال", en: "SI4455 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sx1280: { prefix: "SX1280", ar: "SX1280 اتصال", en: "SX1280 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sx1272: { prefix: "SX1272", ar: "SX1272 اتصال", en: "SX1272 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sx1301: { prefix: "SX1301", ar: "SX1301 اتصال", en: "SX1301 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  rfm12b: { prefix: "RFM12B", ar: "RFM12B اتصال", en: "RFM12B Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  rfm22b: { prefix: "RFM22B", ar: "RFM22B اتصال", en: "RFM22B Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  rfm98: { prefix: "RFM98", ar: "RFM98 اتصال", en: "RFM98 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  rfm96: { prefix: "RFM96", ar: "RFM96 اتصال", en: "RFM96 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  rfm63: { prefix: "RFM63", ar: "RFM63 اتصال", en: "RFM63 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  xbee_pro: { prefix: "XBEPRO", ar: "XBEE-PRO اتصال", en: "XBEE-PRO Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  xbee3: { prefix: "XBEE3", ar: "XBEE3 اتصال", en: "XBEE3 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  bl654: { prefix: "BL654", ar: "BL654 اتصال", en: "BL654 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ch341: { prefix: "CH341", ar: "CH341 اتصال", en: "CH341 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ch9102: { prefix: "CH9102", ar: "CH9102 اتصال", en: "CH9102 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ch343: { prefix: "CH343", ar: "CH343 اتصال", en: "CH343 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  cp2102n: { prefix: "CP202N", ar: "CP2102N اتصال", en: "CP2102N Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ft231x: { prefix: "FT231X", ar: "FT231X اتصال", en: "FT231X Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ft2232: { prefix: "FT2232", ar: "FT2232 اتصال", en: "FT2232 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ft232h: { prefix: "FT232H", ar: "FT232H اتصال", en: "FT232H Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  mcp2221: { prefix: "MCP221", ar: "MCP2221 اتصال", en: "MCP2221 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  max3485: { prefix: "MAX485", ar: "MAX3485 اتصال", en: "MAX3485 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sp3485: { prefix: "SP3485", ar: "SP3485 اتصال", en: "SP3485 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sn65hvd72: { prefix: "SN6D72", ar: "SN65HVD72 اتصال", en: "SN65HVD72 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  ltc2850: { prefix: "LTC850", ar: "LTC2850 اتصال", en: "LTC2850 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  iso1176: { prefix: "ISO176", ar: "ISO1176 اتصال", en: "ISO1176 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  adm2587: { prefix: "ADM587", ar: "ADM2587 اتصال", en: "ADM2587 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  adm3053: { prefix: "ADM053", ar: "ADM3053 اتصال", en: "ADM3053 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  mcp2562: { prefix: "MCP562", ar: "MCP2562 اتصال", en: "MCP2562 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  tcan1042: { prefix: "TCA042", ar: "TCAN1042 اتصال", en: "TCAN1042 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  tja1051: { prefix: "TJA051", ar: "TJA1051 اتصال", en: "TJA1051 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sn65hvd1050: { prefix: "SN6050", ar: "SN65HVD1050 اتصال", en: "SN65HVD1050 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  l80: { prefix: "L80", ar: "L80 اتصال", en: "L80 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  l86: { prefix: "L86", ar: "L86 اتصال", en: "L86 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  atgm336h: { prefix: "ATG36H", ar: "ATGM336H اتصال", en: "ATGM336H Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  gt_u7: { prefix: "GTU7", ar: "GT-U7 اتصال", en: "GT-U7 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  neo_m9n: { prefix: "NEOM9N", ar: "NEO-M9N اتصال", en: "NEO-M9N Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  zoe_m8q: { prefix: "ZOEM8Q", ar: "ZOE-M8Q اتصال", en: "ZOE-M8Q Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  max_m10s: { prefix: "MAX10S", ar: "MAX-M10S اتصال", en: "MAX-M10S Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  teseo_liv3: { prefix: "TESIV3", ar: "TESEO-LIV3 اتصال", en: "TESEO-LIV3 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  mtk3339: { prefix: "MTK339", ar: "MTK3339 اتصال", en: "MTK3339 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  pa1010d: { prefix: "PA110D", ar: "PA1010D اتصال", en: "PA1010D Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sim28: { prefix: "SIM28", ar: "SIM28 اتصال", en: "SIM28 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  l96: { prefix: "L96", ar: "L96 اتصال", en: "L96 Comms", vals: ["OFF", "IDLE", "TX", "RX"], def: "IDLE", pins: 3 },
  sim800c: { prefix: "SIM00C", ar: "SIM800C خلوي", en: "SIM800C Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim808: { prefix: "SIM808", ar: "SIM808 خلوي", en: "SIM808 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim5320: { prefix: "SIM320", ar: "SIM5320 خلوي", en: "SIM5320 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim7000: { prefix: "SIM000", ar: "SIM7000 خلوي", en: "SIM7000 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim7070: { prefix: "SIM070", ar: "SIM7070 خلوي", en: "SIM7070 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim7080: { prefix: "SIM080", ar: "SIM7080 خلوي", en: "SIM7080 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim7500: { prefix: "SIM500", ar: "SIM7500 خلوي", en: "SIM7500 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  sim7670: { prefix: "SIM670", ar: "SIM7670 خلوي", en: "SIM7670 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  ec200s: { prefix: "EC200S", ar: "EC200S خلوي", en: "EC200S Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  ec25: { prefix: "EC25", ar: "EC25 خلوي", en: "EC25 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  bg95: { prefix: "BG95", ar: "BG95 خلوي", en: "BG95 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  bg96: { prefix: "BG96", ar: "BG96 خلوي", en: "BG96 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  m26: { prefix: "M26", ar: "M26 خلوي", en: "M26 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  ec21: { prefix: "EC21", ar: "EC21 خلوي", en: "EC21 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  ec600: { prefix: "EC600", ar: "EC600 خلوي", en: "EC600 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  a9g: { prefix: "A9G", ar: "A9G خلوي", en: "A9G Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  a6: { prefix: "A6", ar: "A6 خلوي", en: "A6 Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  a7672e: { prefix: "A7672E", ar: "A7672E خلوي", en: "A7672E Cellular", vals: ["OFF", "REG", "ERR"], def: "REG", pins: 3 },
  ic_74hc03: { prefix: "HC03", ar: "74HC03", en: "74HC03", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc05: { prefix: "HC05", ar: "74HC05", en: "74HC05", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc09: { prefix: "HC09", ar: "74HC09", en: "74HC09", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc21: { prefix: "HC21", ar: "74HC21", en: "74HC21", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc27: { prefix: "HC27", ar: "74HC27", en: "74HC27", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc51: { prefix: "HC51", ar: "74HC51", en: "74HC51", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc58: { prefix: "HC58", ar: "74HC58", en: "74HC58", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc85: { prefix: "HC85", ar: "74HC85", en: "74HC85", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc107: { prefix: "HC107", ar: "74HC107", en: "74HC107", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc109: { prefix: "HC109", ar: "74HC109", en: "74HC109", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc112: { prefix: "HC112", ar: "74HC112", en: "74HC112", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc123: { prefix: "HC123", ar: "74HC123", en: "74HC123", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc126: { prefix: "HC126", ar: "74HC126", en: "74HC126", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc132: { prefix: "HC132", ar: "74HC132", en: "74HC132", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc137: { prefix: "HC137", ar: "74HC137", en: "74HC137", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc147: { prefix: "HC147", ar: "74HC147", en: "74HC147", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc148: { prefix: "HC148", ar: "74HC148", en: "74HC148", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc153: { prefix: "HC153", ar: "74HC153", en: "74HC153", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc158: { prefix: "HC158", ar: "74HC158", en: "74HC158", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc160: { prefix: "HC160", ar: "74HC160", en: "74HC160", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc162: { prefix: "HC162", ar: "74HC162", en: "74HC162", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc163: { prefix: "HC163", ar: "74HC163", en: "74HC163", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc168: { prefix: "HC168", ar: "74HC168", en: "74HC168", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc169: { prefix: "HC169", ar: "74HC169", en: "74HC169", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc173: { prefix: "HC173", ar: "74HC173", en: "74HC173", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc182: { prefix: "HC182", ar: "74HC182", en: "74HC182", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc190: { prefix: "HC190", ar: "74HC190", en: "74HC190", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc191: { prefix: "HC191", ar: "74HC191", en: "74HC191", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc192: { prefix: "HC192", ar: "74HC192", en: "74HC192", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc194: { prefix: "HC194", ar: "74HC194", en: "74HC194", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc195: { prefix: "HC195", ar: "74HC195", en: "74HC195", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc238: { prefix: "HC238", ar: "74HC238", en: "74HC238", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc239: { prefix: "HC239", ar: "74HC239", en: "74HC239", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc240: { prefix: "HC240", ar: "74HC240", en: "74HC240", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc241: { prefix: "HC241", ar: "74HC241", en: "74HC241", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc251: { prefix: "HC251", ar: "74HC251", en: "74HC251", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc253: { prefix: "HC253", ar: "74HC253", en: "74HC253", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc257: { prefix: "HC257", ar: "74HC257", en: "74HC257", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc258: { prefix: "HC258", ar: "74HC258", en: "74HC258", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ic_74hc259: { prefix: "HC259", ar: "74HC259", en: "74HC259", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4000: { prefix: "CD4000", ar: "CD4000", en: "CD4000", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4002: { prefix: "CD4002", ar: "CD4002", en: "CD4002", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4006: { prefix: "CD4006", ar: "CD4006", en: "CD4006", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4007: { prefix: "CD4007", ar: "CD4007", en: "CD4007", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4008: { prefix: "CD4008", ar: "CD4008", en: "CD4008", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4009: { prefix: "CD4009", ar: "CD4009", en: "CD4009", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4010: { prefix: "CD4010", ar: "CD4010", en: "CD4010", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4011: { prefix: "CD4011", ar: "CD4011", en: "CD4011", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4012: { prefix: "CD4012", ar: "CD4012", en: "CD4012", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4014: { prefix: "CD4014", ar: "CD4014", en: "CD4014", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4016: { prefix: "CD4016", ar: "CD4016", en: "CD4016", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4018: { prefix: "CD4018", ar: "CD4018", en: "CD4018", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4019: { prefix: "CD4019", ar: "CD4019", en: "CD4019", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4020: { prefix: "CD4020", ar: "CD4020", en: "CD4020", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4021: { prefix: "CD4021", ar: "CD4021", en: "CD4021", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4024: { prefix: "CD4024", ar: "CD4024", en: "CD4024", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4026: { prefix: "CD4026", ar: "CD4026", en: "CD4026", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4033: { prefix: "CD4033", ar: "CD4033", en: "CD4033", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4034: { prefix: "CD4034", ar: "CD4034", en: "CD4034", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4035: { prefix: "CD4035", ar: "CD4035", en: "CD4035", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4040: { prefix: "CD4040", ar: "CD4040", en: "CD4040", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4042: { prefix: "CD4042", ar: "CD4042", en: "CD4042", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4043: { prefix: "CD4043", ar: "CD4043", en: "CD4043", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4044: { prefix: "CD4044", ar: "CD4044", en: "CD4044", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4049: { prefix: "CD4049", ar: "CD4049", en: "CD4049", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4050: { prefix: "CD4050", ar: "CD4050", en: "CD4050", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4052: { prefix: "CD4052", ar: "CD4052", en: "CD4052", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4053: { prefix: "CD4053", ar: "CD4053", en: "CD4053", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4069: { prefix: "CD4069", ar: "CD4069", en: "CD4069", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4072: { prefix: "CD4072", ar: "CD4072", en: "CD4072", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4073: { prefix: "CD4073", ar: "CD4073", en: "CD4073", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4078: { prefix: "CD4078", ar: "CD4078", en: "CD4078", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4082: { prefix: "CD4082", ar: "CD4082", en: "CD4082", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4094: { prefix: "CD4094", ar: "CD4094", en: "CD4094", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4099: { prefix: "CD4099", ar: "CD4099", en: "CD4099", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd40106: { prefix: "CD4106", ar: "CD40106", en: "CD40106", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd40193: { prefix: "CD4193", ar: "CD40193", en: "CD40193", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  cd4585: { prefix: "CD4585", ar: "CD4585", en: "CD4585", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  tlc555: { prefix: "TLC555", ar: "TLC555", en: "TLC555", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  icm7555: { prefix: "ICM555", ar: "ICM7555", en: "ICM7555", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  lmc555: { prefix: "LMC555", ar: "LMC555", en: "LMC555", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  xr2206: { prefix: "XR2206", ar: "XR2206", en: "XR2206", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  icl8038: { prefix: "ICL038", ar: "ICL8038", en: "ICL8038", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  max038: { prefix: "MAX038", ar: "MAX038", en: "MAX038", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  lm566: { prefix: "LM566", ar: "LM566", en: "LM566", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  lm567: { prefix: "LM567", ar: "LM567", en: "LM567", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ne565: { prefix: "NE565", ar: "NE565", en: "NE565", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  ne567: { prefix: "NE567", ar: "NE567", en: "NE567", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24c01: { prefix: "AT2C01", ar: "AT24C01 ذاكرة", en: "AT24C01 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24c04: { prefix: "AT2C04", ar: "AT24C04 ذاكرة", en: "AT24C04 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24cm01: { prefix: "AT2M01", ar: "AT24CM01 ذاكرة", en: "AT24CM01 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at24cm02: { prefix: "AT2M02", ar: "AT24CM02 ذاكرة", en: "AT24CM02 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  m24c64: { prefix: "M24C64", ar: "M24C64 ذاكرة", en: "M24C64 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  m24256: { prefix: "M24256", ar: "M24256 ذاكرة", en: "M24256 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  w25q16: { prefix: "W25Q16", ar: "W25Q16 ذاكرة", en: "W25Q16 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  w25q32: { prefix: "W25Q32", ar: "W25Q32 ذاكرة", en: "W25Q32 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  w25q80: { prefix: "W25Q80", ar: "W25Q80 ذاكرة", en: "W25Q80 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  w25q256: { prefix: "W25256", ar: "W25Q256 ذاكرة", en: "W25Q256 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  w25q512: { prefix: "W25512", ar: "W25Q512 ذاكرة", en: "W25Q512 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mx25l1606: { prefix: "MX2606", ar: "MX25L1606 ذاكرة", en: "MX25L1606 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mx25l3206: { prefix: "MX2206", ar: "MX25L3206 ذاكرة", en: "MX25L3206 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mx25l6406: { prefix: "MX2406", ar: "MX25L6406 ذاكرة", en: "MX25L6406 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mx25l12805: { prefix: "MX2805", ar: "MX25L12805 ذاكرة", en: "MX25L12805 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  sst25vf016: { prefix: "SST016", ar: "SST25VF016 ذاكرة", en: "SST25VF016 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  s25fl064: { prefix: "S25064", ar: "S25FL064 ذاكرة", en: "S25FL064 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  is25lp128: { prefix: "IS2128", ar: "IS25LP128 ذاكرة", en: "IS25LP128 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  gd25q32: { prefix: "GD2Q32", ar: "GD25Q32 ذاكرة", en: "GD25Q32 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  gd25q64: { prefix: "GD2Q64", ar: "GD25Q64 ذاكرة", en: "GD25Q64 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  fm24cl64: { prefix: "FM2L64", ar: "FM24CL64 ذاكرة", en: "FM24CL64 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  fm24v10: { prefix: "FM2V10", ar: "FM24V10 ذاكرة", en: "FM24V10 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  fm25cl64: { prefix: "FM2L62", ar: "FM25CL64 ذاكرة", en: "FM25CL64 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mb85rs64: { prefix: "MB8S64", ar: "MB85RS64 ذاكرة", en: "MB85RS64 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mb85rs256: { prefix: "MB8256", ar: "MB85RS256 ذاكرة", en: "MB85RS256 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  mcp23k256: { prefix: "MCP256", ar: "MCP23K256 ذاكرة", en: "MCP23K256 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  sram_23lc1024: { prefix: "SRA024", ar: "SRAM-23LC1024 ذاكرة", en: "SRAM-23LC1024 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  sram_23lc512: { prefix: "SRA512", ar: "SRAM-23LC512 ذاكرة", en: "SRAM-23LC512 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  sram_23k256: { prefix: "SRA256", ar: "SRAM-23K256 ذاكرة", en: "SRAM-23K256 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  c93c46: { prefix: "C93C46", ar: "C93C46 ذاكرة", en: "C93C46 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  c93c56: { prefix: "C93C56", ar: "C93C56 ذاكرة", en: "C93C56 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  c93c66: { prefix: "C93C66", ar: "C93C66 ذاكرة", en: "C93C66 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  c93c86: { prefix: "C93C86", ar: "C93C86 ذاكرة", en: "C93C86 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at25010: { prefix: "AT2010", ar: "AT25010 ذاكرة", en: "AT25010 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at25640: { prefix: "AT2640", ar: "AT25640 ذاكرة", en: "AT25640 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  at25m01: { prefix: "AT2M03", ar: "AT25M01 ذاكرة", en: "AT25M01 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  sdram_is42s16160: { prefix: "SDR160", ar: "SDRAM-IS42S16160 ذاكرة", en: "SDRAM-IS42S16160 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  sdram_w9825g6: { prefix: "SDR5G6", ar: "SDRAM-W9825G6 ذاكرة", en: "SDRAM-W9825G6 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  psram_aps6404: { prefix: "PSR404", ar: "PSRAM-APS6404 ذاكرة", en: "PSRAM-APS6404 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  psram_ips6404: { prefix: "PSR402", ar: "PSRAM-IPS6404 ذاكرة", en: "PSRAM-IPS6404 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  nand_w25n01: { prefix: "NANN01", ar: "NAND-W25N01 ذاكرة", en: "NAND-W25N01 Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  nand_mt29f: { prefix: "NAN29F", ar: "NAND-MT29F ذاكرة", en: "NAND-MT29F Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  emmc_4gb: { prefix: "EMM4GB", ar: "EMMC-4GB ذاكرة", en: "EMMC-4GB Memory", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 },
  lm1876: { prefix: "LM1876", ar: "LM1876 مضخم", en: "LM1876 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  lm2877: { prefix: "LM2877", ar: "LM2877 مضخم", en: "LM2877 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  lm3875: { prefix: "LM3875", ar: "LM3875 مضخم", en: "LM3875 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  lm4780: { prefix: "LM4780", ar: "LM4780 مضخم", en: "LM4780 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda1514: { prefix: "TDA514", ar: "TDA1514 مضخم", en: "TDA1514 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda1521: { prefix: "TDA521", ar: "TDA1521 مضخم", en: "TDA1521 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda2005: { prefix: "TDA005", ar: "TDA2005 مضخم", en: "TDA2005 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda2006: { prefix: "TDA006", ar: "TDA2006 مضخم", en: "TDA2006 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda2009: { prefix: "TDA009", ar: "TDA2009 مضخم", en: "TDA2009 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda7240: { prefix: "TDA240", ar: "TDA7240 مضخم", en: "TDA7240 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda7266: { prefix: "TDA266", ar: "TDA7266 مضخم", en: "TDA7266 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda7293: { prefix: "TDA293", ar: "TDA7293 مضخم", en: "TDA7293 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda7296: { prefix: "TDA296", ar: "TDA7296 مضخم", en: "TDA7296 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tda7379: { prefix: "TDA379", ar: "TDA7379 مضخم", en: "TDA7379 Amp", vals: [20, 40, 80], def: 40, pins: 3 },
  tda7384: { prefix: "TDA384", ar: "TDA7384 مضخم", en: "TDA7384 Amp", vals: [20, 40, 80], def: 40, pins: 3 },
  tda7388: { prefix: "TDA388", ar: "TDA7388 مضخم", en: "TDA7388 Amp", vals: [20, 40, 80], def: 40, pins: 3 },
  tda7391: { prefix: "TDA391", ar: "TDA7391 مضخم", en: "TDA7391 Amp", vals: [20, 40, 80], def: 40, pins: 3 },
  tpa3118: { prefix: "TPA118", ar: "TPA3118 مضخم", en: "TPA3118 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tpa3123: { prefix: "TPA123", ar: "TPA3123 مضخم", en: "TPA3123 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tpa3128: { prefix: "TPA128", ar: "TPA3128 مضخم", en: "TPA3128 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tpa3130: { prefix: "TPA130", ar: "TPA3130 مضخم", en: "TPA3130 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tpa3140: { prefix: "TPA140", ar: "TPA3140 مضخم", en: "TPA3140 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  tpa3220: { prefix: "TPA220", ar: "TPA3220 مضخم", en: "TPA3220 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  max9768: { prefix: "MAX768", ar: "MAX9768 مضخم", en: "MAX9768 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  max9788: { prefix: "MAX788", ar: "MAX9788 مضخم", en: "MAX9788 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  max98400: { prefix: "MAX400", ar: "MAX98400 مضخم", en: "MAX98400 Amp", vals: [5, 10, 20], def: 10, pins: 3 },
  ssm3582: { prefix: "SSM582", ar: "SSM3582 مضخم", en: "SSM3582 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  stk4141: { prefix: "STK141", ar: "STK4141 مضخم", en: "STK4141 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  pam8620: { prefix: "PAM620", ar: "PAM8620 مضخم", en: "PAM8620 Amp", vals: [10, 20, 30], def: 20, pins: 3 },
  lm4950: { prefix: "LM4950", ar: "LM4950 مضخم صغير", en: "LM4950 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  lm4991: { prefix: "LM4991", ar: "LM4991 مضخم صغير", en: "LM4991 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  tpa6120: { prefix: "TPA120", ar: "TPA6120 مضخم صغير", en: "TPA6120 Small Amp", vals: [0.1, 0.5, 1], def: 0.5, pins: 3 },
  tpa6132: { prefix: "TPA132", ar: "TPA6132 مضخم صغير", en: "TPA6132 Small Amp", vals: [0.05, 0.1, 0.15], def: 0.1, pins: 3 },
  tpa6211: { prefix: "TPA211", ar: "TPA6211 مضخم صغير", en: "TPA6211 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  tpa2012: { prefix: "TPA012", ar: "TPA2012 مضخم صغير", en: "TPA2012 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  tpa2031: { prefix: "TPA031", ar: "TPA2031 مضخم صغير", en: "TPA2031 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  pam8406: { prefix: "PAM406", ar: "PAM8406 مضخم صغير", en: "PAM8406 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  pam8304: { prefix: "PAM304", ar: "PAM8304 مضخم صغير", en: "PAM8304 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  ssm2302: { prefix: "SSM302", ar: "SSM2302 مضخم صغير", en: "SSM2302 Small Amp", vals: [1, 2, 3], def: 2, pins: 3 },
  lm833: { prefix: "LM833", ar: "LM833 مكبر عمليات", en: "LM833 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lm4562: { prefix: "LM4562", ar: "LM4562 مكبر عمليات", en: "LM4562 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lm4558: { prefix: "LM4558", ar: "LM4558 مكبر عمليات", en: "LM4558 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lm1458: { prefix: "LM1458", ar: "LM1458 مكبر عمليات", en: "LM1458 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa134: { prefix: "OPA134", ar: "OPA134 مكبر عمليات", en: "OPA134 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa227: { prefix: "OPA227", ar: "OPA227 مكبر عمليات", en: "OPA227 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa277: { prefix: "OPA277", ar: "OPA277 مكبر عمليات", en: "OPA277 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa337: { prefix: "OPA337", ar: "OPA337 مكبر عمليات", en: "OPA337 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa343: { prefix: "OPA343", ar: "OPA343 مكبر عمليات", en: "OPA343 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa350: { prefix: "OPA350", ar: "OPA350 مكبر عمليات", en: "OPA350 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa551: { prefix: "OPA551", ar: "OPA551 مكبر عمليات", en: "OPA551 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa564: { prefix: "OPA564", ar: "OPA564 مكبر عمليات", en: "OPA564 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa1612: { prefix: "OPA612", ar: "OPA1612 مكبر عمليات", en: "OPA1612 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa1656: { prefix: "OPA656", ar: "OPA1656 مكبر عمليات", en: "OPA1656 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa1678: { prefix: "OPA678", ar: "OPA1678 مكبر عمليات", en: "OPA1678 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa2604: { prefix: "OPA604", ar: "OPA2604 مكبر عمليات", en: "OPA2604 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  opa2350: { prefix: "OPA352", ar: "OPA2350 مكبر عمليات", en: "OPA2350 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8066: { prefix: "AD8066", ar: "AD8066 مكبر عمليات", en: "AD8066 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8397: { prefix: "AD8397", ar: "AD8397 مكبر عمليات", en: "AD8397 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad797: { prefix: "AD797", ar: "AD797 مكبر عمليات", en: "AD797 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8099: { prefix: "AD8099", ar: "AD8099 مكبر عمليات", en: "AD8099 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8221: { prefix: "AD8221", ar: "AD8221 مكبر عمليات", en: "AD8221 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8276: { prefix: "AD8276", ar: "AD8276 مكبر عمليات", en: "AD8276 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8429: { prefix: "AD8429", ar: "AD8429 مكبر عمليات", en: "AD8429 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8606: { prefix: "AD8606", ar: "AD8606 مكبر عمليات", en: "AD8606 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ad8628: { prefix: "AD8628", ar: "AD8628 مكبر عمليات", en: "AD8628 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lt1013: { prefix: "LT1013", ar: "LT1013 مكبر عمليات", en: "LT1013 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lt1028: { prefix: "LT1028", ar: "LT1028 مكبر عمليات", en: "LT1028 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lt1124: { prefix: "LT1124", ar: "LT1124 مكبر عمليات", en: "LT1124 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lt1677: { prefix: "LT1677", ar: "LT1677 مكبر عمليات", en: "LT1677 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lt6015: { prefix: "LT6015", ar: "LT6015 مكبر عمليات", en: "LT6015 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lmv358: { prefix: "LMV358", ar: "LMV358 مكبر عمليات", en: "LMV358 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lmv321: { prefix: "LMV321", ar: "LMV321 مكبر عمليات", en: "LMV321 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lmv324: { prefix: "LMV324", ar: "LMV324 مكبر عمليات", en: "LMV324 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lmc6482: { prefix: "LMC482", ar: "LMC6482 مكبر عمليات", en: "LMC6482 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lmc662: { prefix: "LMC662", ar: "LMC662 مكبر عمليات", en: "LMC662 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  lmp7701: { prefix: "LMP701", ar: "LMP7701 مكبر عمليات", en: "LMP7701 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  mcp6001: { prefix: "MCP001", ar: "MCP6001 مكبر عمليات", en: "MCP6001 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  mcp6004: { prefix: "MCP004", ar: "MCP6004 مكبر عمليات", en: "MCP6004 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  mcp6231: { prefix: "MCP231", ar: "MCP6231 مكبر عمليات", en: "MCP6231 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  mcp6241: { prefix: "MCP241", ar: "MCP6241 مكبر عمليات", en: "MCP6241 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  mcp6271: { prefix: "MCP271", ar: "MCP6271 مكبر عمليات", en: "MCP6271 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  tlv2371: { prefix: "TLV371", ar: "TLV2371 مكبر عمليات", en: "TLV2371 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  tlv2462: { prefix: "TLV462", ar: "TLV2462 مكبر عمليات", en: "TLV2462 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  tlv271: { prefix: "TLV271", ar: "TLV271 مكبر عمليات", en: "TLV271 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  tlv9061: { prefix: "TLV061", ar: "TLV9061 مكبر عمليات", en: "TLV9061 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  tlv9062: { prefix: "TLV062", ar: "TLV9062 مكبر عمليات", en: "TLV9062 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ca3140: { prefix: "CA3140", ar: "CA3140 مكبر عمليات", en: "CA3140 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 },
  ca3130: { prefix: "CA3130", ar: "CA3130 مكبر عمليات", en: "CA3130 Op-Amp", vals: [1, 10, 100], def: 10, pins: 3 }
};
var BATCH19 = {ds18s20: 1, lm35: 1, lm75: 1, tmp102: 1, mcp9808: 1, max31865: 1, ads1118: 1, hdc1080: 1, htu21d: 1, sht21: 1, sht35: 1, aht10: 1, aht20: 1, ms5611: 1, lps25h: 1, bmp388: 1, dps310: 1, bmp085: 1, lps22hb: 1, mpx5700: 1, mq131: 1, mq303: 1, mhz19: 1, sds011: 1, pms5003: 1, ccs811: 1, ens160: 1, si1145: 1, veml7700: 1, opt3001: 1, max44009: 1, ltr329: 1, ml8511: 1, veml6070: 1, ina226: 1, ina260: 1, ina3221: 1, lis3dh: 1, mma8452: 1, adxl335: 1, adxl362: 1, lsm6ds3: 1, icm20948: 1, bno055: 1, hmc5883l: 1, qmc5883l: 1, mlx90393: 1, lm7815: 1, lm7824: 1, lm7808: 1, lm7806: 1, lm317hv: 1, lm2940: 1, tps7a47: 1, lm2576: 1, lm2574: 1, mp1584: 1, tps5430: 1, mt3608: 1, lm2577: 1, tps61023: 1, max1771: 1, lm3886: 1, tda7294: 1, tda2050: 1, tda7377: 1, tpa3116: 1, tpa2005: 1, lm4766: 1, drv8434: 1, tmc2209: 1, tmc2130: 1, l6470: 1, vnh5019: 1, drv8313: 1, a4950: 1, mx1508: 1, esp32cam: 1, sx1278: 1, sx1276: 1, nrf52832: 1, hm10: 1, jdy23: 1, ublox_neo6m: 1, ublox_neo7m: 1, w5500: 1, cp2102: 1, ch340: 1, max485: 1, mcp2515: 1, ssd1322: 1, ssd1327: 1, ssd1306_64: 1, st7789: 1, ili9488: 1, hd44780: 1, tm1637: 1, ht16k33: 1, cd4017b: 1, ic_74hc14: 1, ic_74hc04: 1, ic_74hc08: 1, ic_74hc32: 1, ic_74hc86: 1, ic_74hc74: 1, ic_74hc590: 1, ic_74hc4067: 1, at24c64: 1, at24c128: 1, w25q128: 1, fm25v02: 1, mcp23s17: 1, tca9534: 1, max7301: 1};
var BATCH20 = {tmp117: 1, max30205: 1, amg8833: 1, mlx90640: 1, lm73: 1, si7050: 1, ds28ea00: 1, ad8495: 1, hih6130: 1, dht21: 1, sht40: 1, sht45: 1, hdc2080: 1, bme688: 1, bmp390: 1, bmp581: 1, lps35hw: 1, lps33hw: 1, spl06: 1, ms5837: 1, mq137: 1, mq138: 1, mq214: 1, mq216: 1, scd30: 1, scd40: 1, scd41: 1, sgp40: 1, sen54: 1, ags02ma: 1, as7341: 1, as7262: 1, tsl2591: 1, veml6075: 1, guva_s12sd: 1, bh1745: 1, isl29125: 1, apds9306: 1, mpu6500: 1, lsm9ds1: 1, lsm303: 1, l3gd20h: 1, bmi160: 1, bmi270: 1, adxl375: 1, icm42688: 1, lis2dh12: 1, kxtj3: 1, vl53l1x: 1, gp2y0a21: 1, gp2y0a02: 1, us100: 1, a02yyuw: 1, ld2410: 1, rcwl0516: 1, tfmini: 1, tf_luna: 1, vcnl4040: 1, jsn_sr04t: 1, max30100: 1, ad8232: 1, pulse_sensor: 1, gsr_sensor: 1, r307: 1, ina169: 1, acs758: 1, max471: 1, pzem004t: 1, hlw8012: 1, ina228: 1, ina238: 1, ss49e: 1, a1302: 1, drv5053: 1, as5600: 1, as5048a: 1, sh1106: 1, ssd1305: 1, gc9a01: 1, st7796: 1, ili9225: 1, ssd1963: 1, epd_154: 1, epd_213: 1, epd_29: 1, lcd_12864: 1, lcd_16x4: 1, lcd_8x2: 1, tm1638: 1, ht1621: 1, drv8847: 1, drv8880: 1, tmc2208: 1, tmc2160: 1, tmc5160: 1, l6208: 1, l6235: 1, vnh2sp30: 1, ibt2: 1, lv8548: 1, lm7818: 1, lm78l05: 1, lm79l05: 1, lm317l: 1, lm350: 1, ld1117: 1, xc6206: 1, ap2112: 1, tlv1117: 1, lt3045: 1, lm2575: 1, lm2595: 1, xl4015: 1, xl4005: 1, xl7005: 1, mp2307: 1, mp2315: 1, tps54331: 1, sx1308: 1, cn3791: 1, bq24074: 1, tp5100: 1, ip5306: 1, esp32_c3: 1, esp32_s3: 1, nrf52840: 1, hc06: 1, hm11: 1, jdy31: 1, e32: 1, sx1262: 1, dw1000: 1, pn532: 1, w5100: 1, enc424j600: 1, mcp2551: 1, tja1050: 1, sn65hvd230: 1, max232: 1, max3232: 1, ft232: 1, pl2303: 1, cp2104: 1, l76k: 1, neo_m8n: 1, sim7600: 1, sim868: 1, a7670: 1, ic_74hc02: 1, ic_74hc10: 1, ic_74hc20: 1, ic_74hc30: 1, ic_74hc125: 1, ic_74hc157: 1, ic_74hc151: 1, ic_74hc139: 1, ic_74hc154: 1, ic_74hc161: 1, ic_74hc164: 1, ic_74hc166: 1, ic_74hc174: 1, ic_74hc175: 1, ic_74hc193: 1, ic_74hc244: 1, ic_74hc245: 1, ic_74hc283: 1, ic_74hc374: 1, ic_74hc4040: 1, ic_74hc4046: 1, ic_74hc4053: 1, ic_74hc4094: 1, mcp23008: 1, tca9535: 1, txs0108: 1, sn74lvc245: 1, at24c02: 1, at24c08: 1, at24c16: 1, lm1875: 1, tda2040: 1, tda7498: 1, tpa3110: 1, pam8610: 1, pam8302: 1, max9744: 1, mcp6002: 1, mcp6022: 1, tl082: 1, tl084: 1, lf353: 1, lf411: 1, op07: 1, op27: 1, ad8605: 1};
// عناصر أساسية إضافية تعمل بنموذج عنصر أصلي (محاكاة/رسم/أطراف) مع قيم واسم خاصين بها.
var ALIAS = {elec_cap: "capacitor", tantalum_cap: "capacitor", ceramic_cap: "capacitor", supercap: "capacitor", fast_diode: "diode", rectifier_diode: "diode", germanium_diode: "diode", zener_1w: "zener", tvs_diode: "zener", schottky_ss34: "schottky", ntc: "thermistor", polyfuse: "fuse", power_resistor: "resistor", shunt_resistor: "resistor", trimmer_pot: "potentiometer", slide_pot: "potentiometer", rheostat: "potentiometer", q_tip120: "transistor", q_tip31: "transistor", q_bc547: "transistor", q_2n2222: "transistor", q_2n3904: "transistor", q_bd139: "transistor", q_bc557: "transistor_pnp", q_2n3906: "transistor_pnp", q_tip32: "transistor_pnp", q_tip127: "transistor_pnp", q_bd140: "transistor_pnp", m_irf540: "mosfet_n", m_irlz44n: "mosfet_n", m_2n7000: "mosfet_n", m_irf3205: "mosfet_n", m_irlb8721: "mosfet_n", power_inductor: "inductor", ferrite_choke: "inductor", halogen_lamp: "bulb", dc_fan: "motor", vibration_motor: "motor", piezo_buzzer: "buzzer", headphones: "speaker", push_button: "switch", toggle_switch: "switch", slide_switch: "switch", limit_switch: "switch", lipo_battery: "battery", aa_cell: "battery", coin_cell: "battery", nine_volt: "battery", usb_power: "battery", bench_supply: "battery", lead_acid: "battery"};
function aliasView(c) {
  var b = ALIAS[c.type];
  if (!b) return c;
  var o = {}, k;
  for (k in c) o[k] = c[k];
  o.type = b;
  return o;
}
var BATCH21 = {tmp116: 1, tmp1075: 1, max6633: 1, mcp9701: 1, lm19: 1, lm34: 1, lm335: 1, ad590: 1, tmp35: 1, tmp37: 1, sts31: 1, stlm20: 1, sht85: 1, hih7130: 1, hts221: 1, hdc3020: 1, shtc3: 1, shtc1: 1, si7020: 1, am2301: 1, am2302: 1, capacitive_soil: 1, fc28: 1, lps22hh: 1, mpl115a2: 1, ms5803: 1, ms5607: 1, mprls: 1, bmp384: 1, icp10125: 1, icp20100: 1, mpx4115: 1, mpxv7002: 1, xgzp6847: 1, mq136: 1, mq139: 1, mq309: 1, tgs2600: 1, tgs2602: 1, tgs2620: 1, mics5524: 1, mics6814: 1, mh_z14a: 1, mh_z16: 1, s8_co2: 1, iaq_core: 1, zmod4410: 1, zh03b: 1, tsl2572: 1, veml3235: 1, opt4048: 1, opt3004: 1, ltr390: 1, ltr303: 1, ltr559: 1, as7343: 1, as7265x: 1, ap3216: 1, vcnl4200: 1, si1133: 1, mpu6886: 1, mpu9255: 1, lsm6dso: 1, lsm6dsox: 1, lis3mdl: 1, lis2mdl: 1, lis3dsh: 1, mma7660: 1, mma8451: 1, mma7361: 1, bma280: 1, bma423: 1, bmi088: 1, bmx160: 1, icm20689: 1, icm42605: 1, fxos8700: 1, fxas21002: 1, l3g4200d: 1, itg3200: 1, vl53l4cd: 1, vl53l3cx: 1, tof050c: 1, tf02: 1, tf03: 1, hcsr05: 1, srf05: 1, maxsonar_ez1: 1, us015: 1, us020: 1, urm37: 1, ld2450: 1, ld2420: 1, hb100: 1, sen0311: 1, max30101: 1, max86150: 1, afe4490: 1, ads1292: 1, ad8233: 1, max30003: 1, emg_sensor: 1, muscle_v3: 1, gsr_grove: 1, skin_temp_mlx: 1, ina180: 1, ina199: 1, ina210: 1, ina230: 1, ina233: 1, acs711: 1, acs723: 1, acs724: 1, acs781: 1, max9611: 1, ltc4151: 1, ltc2945: 1, pac1934: 1, bl0937: 1, pzem017: 1, ade7753: 1, atm90e26: 1, hmc5983: 1, mmc5603: 1, mmc5983ma: 1, ak8963: 1, ak09916: 1, qmc6310: 1, bmm150: 1, tmag5273: 1, tlv493d: 1, a1324: 1, ss495a: 1, drv5055: 1, as5047p: 1, ma730: 1, mt6701: 1, max9814: 1, max4466: 1, ics43434: 1, inmp441: 1, sph0645: 1, spm0405: 1, mp34dt05: 1, ky037: 1, fsr402: 1, fsr406: 1, load_cell_5kg: 1, load_cell_20kg: 1, piezo_film: 1, flex_4in: 1, yfs201: 1, yfs401: 1, yfs210: 1, yfb08: 1, fs300a: 1, fs400a: 1, float_switch: 1, ultrasonic_level: 1, capacitive_level: 1, optical_level: 1, soil_moisture_v2: 1, st7567: 1, st7789_135: 1, st7735_80: 1, ili9163: 1, ili9327: 1, ili9342: 1, ili9806: 1, hx8357: 1, hx8347: 1, ra8875: 1, ssd1289: 1, ssd2119: 1, sed1520: 1, ks0108: 1, pcd8544: 1, uc1701: 1, uc1609: 1, t6963c: 1, drv8701: 1, drv8424: 1, drv8428: 1, tmc2100: 1, tmc2226: 1, tmc2225: 1, tmc2240: 1, tmc2660: 1, a4982: 1, a4983: 1, l6219: 1, l297: 1, l298p: 1, tb6560: 1, tb6600: 1, tb67s109: 1, lm78m05: 1, lm2937: 1, lm2931: 1, lm1086: 1, lm1085: 1, lt1763: 1, lt1963: 1, lt3042: 1, tps7a20: 1, tps73401: 1, adp150: 1, adp3338: 1, mcp1802: 1, mcp1826: 1, ap7361: 1, ap7333: 1, rt9013: 1, ld39050: 1, tlv70033: 1, lm22676: 1, lm2672: 1, lm2674: 1, lm5008: 1, lm5164: 1, ltc3630: 1, ltc3115: 1, tps54360: 1, tps62130: 1, tps62160: 1, tps62933: 1, mp1470: 1, mp2359: 1, mp2491: 1, xl1509: 1, xl2596: 1, mc34063: 1, tps63020: 1, tps61088: 1, tps61230: 1, mp3429: 1, xl6019: 1, xl6012: 1, ap3012: 1, lm2621: 1, lm3478: 1, tps55340: 1, tps61200: 1, tp4057: 1, tp4054: 1, mcp73831: 1, mcp73832: 1, bq24072: 1, bq24075: 1, bq25606: 1, bq25895: 1, ltc4054: 1, ltc4065: 1, cn3722: 1, cn3765: 1, ip2312: 1, ip5310: 1, esp32_wroom: 1, esp32_s2: 1, esp32_c6: 1, esp12f: 1, esp12e: 1, esp07: 1, bl602: 1, rtl8710: 1, rtl8720dn: 1, nrf51822: 1, nrf52810: 1, nrf5340: 1, nrf9160: 1, cc2530: 1, cc2531: 1, cc2640: 1, cc2652: 1, cc3200: 1, cc1310: 1, cc1125: 1, cc2500: 1, si4432: 1, si4463: 1, si4455: 1, sx1280: 1, sx1272: 1, sx1301: 1, rfm12b: 1, rfm22b: 1, rfm98: 1, rfm96: 1, rfm63: 1, xbee_pro: 1, xbee3: 1, bl654: 1, ch341: 1, ch9102: 1, ch343: 1, cp2102n: 1, ft231x: 1, ft2232: 1, ft232h: 1, mcp2221: 1, max3485: 1, sp3485: 1, sn65hvd72: 1, ltc2850: 1, iso1176: 1, adm2587: 1, adm3053: 1, mcp2562: 1, tcan1042: 1, tja1051: 1, sn65hvd1050: 1, l80: 1, l86: 1, atgm336h: 1, gt_u7: 1, neo_m9n: 1, zoe_m8q: 1, max_m10s: 1, teseo_liv3: 1, mtk3339: 1, pa1010d: 1, sim28: 1, l96: 1, sim800c: 1, sim808: 1, sim5320: 1, sim7000: 1, sim7070: 1, sim7080: 1, sim7500: 1, sim7670: 1, ec200s: 1, ec25: 1, bg95: 1, bg96: 1, m26: 1, ec21: 1, ec600: 1, a9g: 1, a6: 1, a7672e: 1, ic_74hc03: 1, ic_74hc05: 1, ic_74hc09: 1, ic_74hc21: 1, ic_74hc27: 1, ic_74hc51: 1, ic_74hc58: 1, ic_74hc85: 1, ic_74hc107: 1, ic_74hc109: 1, ic_74hc112: 1, ic_74hc123: 1, ic_74hc126: 1, ic_74hc132: 1, ic_74hc137: 1, ic_74hc147: 1, ic_74hc148: 1, ic_74hc153: 1, ic_74hc158: 1, ic_74hc160: 1, ic_74hc162: 1, ic_74hc163: 1, ic_74hc168: 1, ic_74hc169: 1, ic_74hc173: 1, ic_74hc182: 1, ic_74hc190: 1, ic_74hc191: 1, ic_74hc192: 1, ic_74hc194: 1, ic_74hc195: 1, ic_74hc238: 1, ic_74hc239: 1, ic_74hc240: 1, ic_74hc241: 1, ic_74hc251: 1, ic_74hc253: 1, ic_74hc257: 1, ic_74hc258: 1, ic_74hc259: 1, cd4000: 1, cd4002: 1, cd4006: 1, cd4007: 1, cd4008: 1, cd4009: 1, cd4010: 1, cd4011: 1, cd4012: 1, cd4014: 1, cd4016: 1, cd4018: 1, cd4019: 1, cd4020: 1, cd4021: 1, cd4024: 1, cd4026: 1, cd4033: 1, cd4034: 1, cd4035: 1, cd4040: 1, cd4042: 1, cd4043: 1, cd4044: 1, cd4049: 1, cd4050: 1, cd4052: 1, cd4053: 1, cd4069: 1, cd4072: 1, cd4073: 1, cd4078: 1, cd4082: 1, cd4094: 1, cd4099: 1, cd40106: 1, cd40193: 1, cd4585: 1, tlc555: 1, icm7555: 1, lmc555: 1, xr2206: 1, icl8038: 1, max038: 1, lm566: 1, lm567: 1, ne565: 1, ne567: 1, at24c01: 1, at24c04: 1, at24cm01: 1, at24cm02: 1, m24c64: 1, m24256: 1, w25q16: 1, w25q32: 1, w25q80: 1, w25q256: 1, w25q512: 1, mx25l1606: 1, mx25l3206: 1, mx25l6406: 1, mx25l12805: 1, sst25vf016: 1, s25fl064: 1, is25lp128: 1, gd25q32: 1, gd25q64: 1, fm24cl64: 1, fm24v10: 1, fm25cl64: 1, mb85rs64: 1, mb85rs256: 1, mcp23k256: 1, sram_23lc1024: 1, sram_23lc512: 1, sram_23k256: 1, c93c46: 1, c93c56: 1, c93c66: 1, c93c86: 1, at25010: 1, at25640: 1, at25m01: 1, sdram_is42s16160: 1, sdram_w9825g6: 1, psram_aps6404: 1, psram_ips6404: 1, nand_w25n01: 1, nand_mt29f: 1, emmc_4gb: 1, lm1876: 1, lm2877: 1, lm3875: 1, lm4780: 1, tda1514: 1, tda1521: 1, tda2005: 1, tda2006: 1, tda2009: 1, tda7240: 1, tda7266: 1, tda7293: 1, tda7296: 1, tda7379: 1, tda7384: 1, tda7388: 1, tda7391: 1, tpa3118: 1, tpa3123: 1, tpa3128: 1, tpa3130: 1, tpa3140: 1, tpa3220: 1, max9768: 1, max9788: 1, max98400: 1, ssm3582: 1, stk4141: 1, pam8620: 1, lm4950: 1, lm4991: 1, tpa6120: 1, tpa6132: 1, tpa6211: 1, tpa2012: 1, tpa2031: 1, pam8406: 1, pam8304: 1, ssm2302: 1, lm833: 1, lm4562: 1, lm4558: 1, lm1458: 1, opa134: 1, opa227: 1, opa277: 1, opa337: 1, opa343: 1, opa350: 1, opa551: 1, opa564: 1, opa1612: 1, opa1656: 1, opa1678: 1, opa2604: 1, opa2350: 1, ad8066: 1, ad8397: 1, ad797: 1, ad8099: 1, ad8221: 1, ad8276: 1, ad8429: 1, ad8606: 1, ad8628: 1, lt1013: 1, lt1028: 1, lt1124: 1, lt1677: 1, lt6015: 1, lmv358: 1, lmv321: 1, lmv324: 1, lmc6482: 1, lmc662: 1, lmp7701: 1, mcp6001: 1, mcp6004: 1, mcp6231: 1, mcp6241: 1, mcp6271: 1, tlv2371: 1, tlv2462: 1, tlv271: 1, tlv9061: 1, tlv9062: 1, ca3140: 1, ca3130: 1};
Object.assign(ALIAS, {led_white: "led", led_blue: "led", led_green: "led", led_yellow: "led", led_red: "led", photocell: "ldr", schottky_1n5817: "schottky", schottky_sb340: "schottky", schottky_mbr1045: "schottky", zener_0w5: "zener", zener_5w: "zener", tvs_smbj: "zener", diode_1n4001: "diode", diode_1n4004: "diode", diode_1n5408: "diode", diode_uf4007: "diode", diode_1n34a: "diode", film_cap: "capacitor", mica_cap: "capacitor", polymer_cap: "capacitor", bipolar_cap: "capacitor", mkp_cap: "capacitor", x2_cap: "capacitor", y_cap: "capacitor", trimmer_cap: "capacitor", carbon_resistor: "resistor", metal_film_resistor: "resistor", wirewound_resistor: "resistor", smd_resistor: "resistor", fusible_resistor: "resistor", pullup_resistor: "resistor", current_sense_res: "resistor", high_value_resistor: "resistor", multiturn_pot: "potentiometer", log_pot: "potentiometer", volume_pot: "potentiometer", joystick_axis: "potentiometer", ntc_probe: "thermistor", q_bc337: "transistor", q_s8050: "transistor", q_c945: "transistor", q_2n3055: "transistor", q_mje3055: "transistor", q_tip41c: "transistor", q_bd137: "transistor", q_2sc1815: "transistor", q_2sc5200: "transistor", q_2n5551: "transistor", q_mpsa42: "transistor", q_bc639: "transistor", q_2n2907: "transistor_pnp", q_bc327: "transistor_pnp", q_s8550: "transistor_pnp", q_a1015: "transistor_pnp", q_tip42c: "transistor_pnp", q_2sa1943: "transistor_pnp", q_2n5401: "transistor_pnp", q_mpsa92: "transistor_pnp", q_bc640: "transistor_pnp", q_bd138: "transistor_pnp", m_irf520: "mosfet_n", m_irf640: "mosfet_n", m_irfz44n: "mosfet_n", m_irf1404: "mosfet_n", m_ao3400: "mosfet_n", m_fqp30n06: "mosfet_n", m_stp55nf06: "mosfet_n", m_irlml2502: "mosfet_n", m_irf530: "mosfet_n", m_irlb3034: "mosfet_n", m_si2302: "mosfet_n", m_bss138: "mosfet_n", toroid_inductor: "inductor", air_coil: "inductor", smd_inductor: "inductor", common_mode_choke: "inductor", incandescent_lamp: "bulb", led_bulb: "bulb", heating_element: "bulb", water_pump: "motor", n20_motor: "motor", gear_motor: "motor", mini_speaker: "speaker", woofer: "speaker", tweeter: "speaker", active_buzzer: "buzzer", passive_buzzer: "buzzer", siren: "buzzer", dip_switch: "switch", rocker_switch: "switch", key_switch: "switch", micro_switch: "switch", foot_switch: "switch", selector_switch: "switch", li_ion_18650: "battery", nimh_pack: "battery", car_battery: "battery", wall_adapter: "battery", solar_panel_5v: "battery", usb_c_pd: "battery", powerbank: "battery", dry_cell_d: "battery", lifepo4: "battery", button_cell_lr44: "battery", ac_transformer: "ac_source", ac_generator: "ac_source"});
var cntState = {}; // حالة العداد CD4017 وعناصر التخزين (تبقى بين عمليات المحاكاة)
function icState(c) { var s = cntState[c.id]; return s && s.t === c.type ? s : null; }
function logicSt(c) { var s = icState(c); if (!s) s = cntState[c.id] = { t: c.type, setVal: null, hi: null, q: 0, bits: 0, reg: 0, latched: 0 }; return s; }
function hex2(v) { return "0x" + Number(v || 0).toString(16).toUpperCase().padStart(2, "0"); }
var IC12 = {
  tda7297:    { col: "#dc2626", name: "TDA7297", sub: function (c) { return "×" + c.val + "W"; } },
  opa2134:    { col: "#a78bfa", name: "OPA2134", pm: 1, sub: function (c) { return "Studio"; } },
  ad620:      { col: "#1e3a8a", name: "AD620", pm: 1, sub: function (c) { return "×" + c.val; } },
  opa548:     { col: "#ea580c", name: "OPA548", sub: function (c) { return c.val + "A"; } },
  lm337:      { col: "#b91c1c", name: "LM337", sub: function (c) { return c.val + "V"; } },
  cd4013:     { col: "#0ea5e9", name: "CD4013", sub: function (c) { var s = icState(c); return "Q=" + (s ? s.q : c.val); } },
  cd4015:     { col: "#7c3aed", name: "CD4015", sub: function (c) { var s = icState(c); return "4b " + (s ? s.bits : c.val).toString(2).padStart(4, "0"); } },
  ic_74hc273: { col: "#475569", name: "74HC273", sub: function (c) { var s = icState(c); return hex2(s ? s.reg : 0); } },
  ic_74hc373: { col: "#14532d", name: "74HC373", sub: function (c) { var s = icState(c); return hex2(s ? s.latched : 0); } },
  at24c32:    { col: "#78350f", name: "AT24C32", sub: function (c) { return "EEPROM " + c.val; } },
  mcp23017:   { col: "#1e3a8a", name: "MCP23017", sub: function (c) { return "0x" + Number(c.val).toString(16).toUpperCase(); } },
  ic_74hc00:  { col: "#475569", name: "74HC00", sub: function (c) { return "NAND×4"; } },
  mpu6050:    { col: "#be123c", name: "MPU6050", sub: function (c) { return String(c.val); } },
  bmp280:     { col: "#0369a1", name: "BMP280",  sub: function (c) { return c.val + " hPa"; } },
  acs712:     { col: "#7c3aed", name: "ACS712",  sub: function (c) { return "±" + c.val + "A"; } },
  a3144:      { col: "#b45309", name: "A3144",   sub: function (c) { return c.closed ? "MAG" : "—"; } },
  ky038:      { col: "#0891b2", name: "KY-038",  sub: function (c) { return "L" + c.val; } },
  yl69:       { col: "#78350f", name: "YL-69",   sub: function (c) { return c.val + "%"; } },
  ttp223:     { col: "#be185d", name: "TTP223",  sub: function (c) { return c.closed ? "TOUCH" : "—"; } },
  ky040:      { col: "#1e40af", name: "KY-040",  sub: function (c) { return c.val + "°"; } },
  tsop:       { col: "#1e293b", name: "TSOP",    sub: function (c) { return c.closed ? "IR" : "—"; } },
  hc05:       { col: "#1e3a8a", name: "HC-05",   sub: function (c) { return String(c.val); } },
  l298n:      { col: "#7c2d12", name: "L298N",   sub: function (c) { return String(c.val); } },
  a4988:      { col: "#1e40af", name: "A4988",   sub: function (c) { return String(c.val); } },
  pam8403:    { col: "#7c3aed", name: "PAM8403", sub: function (c) { return "×" + c.val + "W"; } },
  max98357:   { col: "#9333ea", name: "MAX98357", sub: function (c) { return "×" + c.val + "W"; } },
  ads1115:    { col: "#0369a1", name: "ADS1115", sub: function (c) { return "0x" + Number(c.val).toString(16).toUpperCase().padStart(4, "0"); } },
  mcp4725:    { col: "#b45309", name: "MCP4725", sub: function (c) { return "0x" + Number(c.val).toString(16).toUpperCase().padStart(3, "0"); } },
  ina219:     { col: "#0891b2", name: "INA219",  sub: function (c) { return c.val + "mA"; } },
  mq2:        { col: "#78350f", name: "MQ-2",    sub: function (c) { return String(c.val); } },
  bh1750:     { col: "#facc15", name: "BH1750",  sub: function (c) { return c.val + "lx"; } },
  vl53l0x:    { col: "#be185d", name: "VL53L0X", sub: function (c) { return c.val + "mm"; } },
  ic_74hc165: { col: "#475569", name: "74HC165", sub: function (c) { return "0x" + Number(c.val).toString(16).toUpperCase().padStart(2, "0"); } },
  nrf24l01:   { col: "#1e3a8a", name: "NRF24",   sub: function (c) { return String(c.val); } },
  sim800l:    { col: "#dc2626", name: "SIM800L", sub: function (c) { return String(c.val); } },
  drv8825:    { col: "#0e7490", name: "DRV8825", sub: function (c) { return String(c.val); } },
  tb6612:     { col: "#0369a1", name: "TB6612",  sub: function (c) { return String(c.val); } },
  bts7960:    { col: "#b91c1c", name: "BTS7960", sub: function (c) { return String(c.val); } },
  tcs34725:   { col: "#be123c", name: "TCS34725", sub: function (c) { return String(c.val); } },
  mlx90614:   { col: "#7c3aed", name: "MLX90614", sub: function (c) { return Number(c.val).toFixed(0) + "°C"; } },
  max30102:   { col: "#be185d", name: "MAX30102", sub: function (c) { return c.val + "bpm"; } },
  adxl345:    { col: "#0891b2", name: "ADXL345", sub: function (c) { return String(c.val); } },
  hx711:      { col: "#78350f", name: "HX711",   sub: function (c) { return c.val + "g"; } },
  dht22:      { col: "#059669", name: "DHT22",   sub: function (c) { return c.val + "°C"; } },
  sgp30:      { col: "#475569", name: "SGP30",   sub: function (c) { return c.val + "ppm"; } },
  rc522:      { col: "#1e3a8a", name: "RC522",   sub: function (c) { return String(c.val); } },
  bme680:     { col: "#15803d", name: "BME680",  sub: function (c) { return c.val + " IAQ"; } },
  pca9685:    { col: "#7c3aed", name: "PCA9685", sub: function (c) { return c.val + "%"; } },
  tca9548a:   { col: "#1e40af", name: "TCA9548A", sub: function (c) { return "CH" + c.val; } },
  l9110s:     { col: "#0891b2", name: "L9110S",  sub: function (c) { return String(c.val); } },
  tmp36:      { col: "#dc2626", name: "TMP36",   sub: function (c) { return c.val + "°C"; } },
  am2320:     { col: "#059669", name: "AM2320",  sub: function (c) { return c.val + "%RH"; } },
  ds1307:     { col: "#1e3a8a", name: "DS1307",  sub: function (c) { return String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00"; } },
  pcf8563:    { col: "#0369a1", name: "PCF8563", sub: function (c) { return String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00"; } },
  st7735:     { col: "#be123c", name: "ST7735",  sub: function (c) { return String(c.val); } },
  ssd1351:    { col: "#9333ea", name: "SSD1351", sub: function (c) { return String(c.val); } },
  bmp180:     { col: "#0891b2", name: "BMP180",  sub: function (c) { return c.val + "hPa"; } },
  sht31:      { col: "#15803d", name: "SHT31",   sub: function (c) { return c.val + "°C"; } },
  apds9960:   { col: "#b45309", name: "APDS9960", sub: function (c) { return String(c.val); } },
  ds1302:     { col: "#1e40af", name: "DS1302",  sub: function (c) { return String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00"; } },
  max6675:    { col: "#7c3aed", name: "MAX6675", sub: function (c) { return Math.round(c.val / 4) + "°C"; } },
  max31855:   { col: "#0369a1", name: "MAX31855", sub: function (c) { return c.val + "°C"; } },
  sd_card:    { col: "#78350f", name: "microSD", sub: function (c) { return String(c.val); } },
  enc28j60:   { col: "#475569", name: "ENC28J60", sub: function (c) { return String(c.val); } },
  uln2803:    { col: "#7c2d12", name: "ULN2803", sub: function (c) { return c.val + "/8"; } },
  tlc5940:    { col: "#be185d", name: "TLC5940", sub: function (c) { return c.val + "%"; } },
  mpu9250:    { col: "#be123c", name: "MPU9250", sub: function (c) { return String(c.val); } },
  ad9833:     { col: "#9333ea", name: "AD9833",  sub: function (c) { return (c.val >= 1000 ? (c.val / 1000) + "k" : c.val) + "Hz"; } },
  ams1117:    { col: "#0891b2", name: "AMS1117", sub: function (c) { return c.val + "V"; } },
  xl6009:     { col: "#dc2626", name: "XL6009",  sub: function (c) { return c.val + "V"; } },
  vl6180x:    { col: "#15803d", name: "VL6180X", sub: function (c) { return c.val + "mm"; } },
  sht10: { col: "#0891b2", name: "SHT10", sub: function (c) { return Number(c.val).toFixed(0) + "°C"; } },
  sht75: { col: "#0891b2", name: "SHT75", sub: function (c) { return Number(c.val).toFixed(0) + "°C"; } },
  si7021: { col: "#0891b2", name: "SI7021", sub: function (c) { return Number(c.val).toFixed(0) + "%"; } },
  bme280: { col: "#0891b2", name: "BME280", sub: function (c) { return Number(c.val).toFixed(0) + "hPa"; } },
  mpl3115a2: { col: "#0891b2", name: "MPL3115", sub: function (c) { return Number(c.val).toFixed(0) + "hPa"; } },
  mq3: { col: "#0891b2", name: "MQ3", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  mq4: { col: "#0891b2", name: "MQ4", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  mq5: { col: "#0891b2", name: "MQ5", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  mq6: { col: "#0891b2", name: "MQ6", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  mq7: { col: "#0891b2", name: "MQ7", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  mq8: { col: "#0891b2", name: "MQ8", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  mq9: { col: "#0891b2", name: "MQ9", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  mq135: { col: "#0891b2", name: "MQ135", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  gp2y1010: { col: "#0891b2", name: "DUST", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  tsl2561: { col: "#0891b2", name: "TSL", sub: function (c) { return Number(c.val).toFixed(0) + "lx"; } },
  tcs3200: { col: "#0891b2", name: "CLR2", sub: function (c) { return String(c.val); } },
  reed_switch: { col: "#0891b2", name: "REED", sub: function (c) { return String(c.val); } },
  vibration_sensor: { col: "#0891b2", name: "VIB", sub: function (c) { return String(c.val); } },
  water_level: { col: "#0891b2", name: "WLVL", sub: function (c) { return Number(c.val).toFixed(0) + "%"; } },
  flex_sensor: { col: "#0891b2", name: "FLEX", sub: function (c) { return Number(c.val).toFixed(0) + "%"; } },
  tilt_switch: { col: "#0891b2", name: "TILT", sub: function (c) { return String(c.val); } },
  shock_sensor: { col: "#0891b2", name: "SHOCK", sub: function (c) { return String(c.val); } },
  flame_sensor: { col: "#0891b2", name: "FLAME", sub: function (c) { return Number(c.val).toFixed(0) + "ppm"; } },
  rain_sensor: { col: "#0891b2", name: "RAIN", sub: function (c) { return Number(c.val).toFixed(0) + "%"; } },
  hall_linear: { col: "#0891b2", name: "HALLL", sub: function (c) { return String(c.val); } },
  cd4071: { col: "#475569", name: "OR4", sub: function (c) { return String(c.val); } },
  cd4081: { col: "#475569", name: "AND4", sub: function (c) { return String(c.val); } },
  cd4030: { col: "#475569", name: "XOR4", sub: function (c) { return String(c.val); } },
  cd4001: { col: "#475569", name: "NOR4", sub: function (c) { return String(c.val); } },
  cd4023: { col: "#475569", name: "NAND3", sub: function (c) { return String(c.val); } },
  cd4025: { col: "#475569", name: "NOR3", sub: function (c) { return String(c.val); } },
  cd4070: { col: "#475569", name: "XOR4B", sub: function (c) { return String(c.val); } },
  cd4075: { col: "#475569", name: "OR3", sub: function (c) { return String(c.val); } },
  cd4077: { col: "#475569", name: "XNOR4", sub: function (c) { return String(c.val); } },
  cd4093: { col: "#475569", name: "NSCH", sub: function (c) { return String(c.val); } },
  cd4538: { col: "#475569", name: "MONO2", sub: function (c) { return String(c.val); } },
  cd4047: { col: "#475569", name: "ASTAB", sub: function (c) { return String(c.val); } },
  cd4027: { col: "#475569", name: "JK2", sub: function (c) { return String(c.val); } },
  cd4029: { col: "#475569", name: "CNT29", sub: function (c) { return String(c.val); } },
  cd4076: { col: "#475569", name: "REG4", sub: function (c) { return String(c.val); } },
  cd4022: { col: "#475569", name: "CNT22", sub: function (c) { return String(c.val); } },
  cd4060: { col: "#475569", name: "CNT60", sub: function (c) { return String(c.val); } },
  cd4541: { col: "#475569", name: "TIM41", sub: function (c) { return String(c.val); } },
  cd4511: { col: "#475569", name: "BCD7S", sub: function (c) { return String(c.val); } },
  cd4028: { col: "#475569", name: "BCD10", sub: function (c) { return String(c.val); } },
  mcp3008: { col: "#475569", name: "A10", sub: function (c) { return String(c.val); } },
  mcp3208: { col: "#475569", name: "A12", sub: function (c) { return String(c.val); } },
  ads1015: { col: "#475569", name: "ADS1", sub: function (c) { return String(c.val); } },
  pcf8591: { col: "#475569", name: "PCF", sub: function (c) { return String(c.val); } },
  tlc5615: { col: "#475569", name: "DA10", sub: function (c) { return String(c.val); } },
  mcp4921: { col: "#475569", name: "DA4921", sub: function (c) { return String(c.val); } },
  at24c256: { col: "#475569", name: "E256", sub: function (c) { return String(c.val); } },
  at24c512: { col: "#475569", name: "E512", sub: function (c) { return String(c.val); } },
  w25q64: { col: "#475569", name: "FLASH", sub: function (c) { return String(c.val); } },
  mb85rc: { col: "#475569", name: "FRAM", sub: function (c) { return String(c.val); } },
  ds3234: { col: "#0891b2", name: "RTC34", sub: function (c) { return String(c.val); } },
  rv3028: { col: "#0891b2", name: "RTC28", sub: function (c) { return String(c.val); } },
  mcp7940: { col: "#0891b2", name: "RTC40", sub: function (c) { return String(c.val); } },
  nokia5110: { col: "#be123c", name: "LCD51", sub: function (c) { return String(c.val); } },
  ssd1309: { col: "#be123c", name: "OL9", sub: function (c) { return String(c.val); } },
  st7565: { col: "#be123c", name: "LCD56", sub: function (c) { return String(c.val); } },
  st7920: { col: "#be123c", name: "LCD79", sub: function (c) { return String(c.val); } },
  ili9341: { col: "#be123c", name: "TFT93", sub: function (c) { return String(c.val); } },
  ili9486: { col: "#be123c", name: "TFT94", sub: function (c) { return String(c.val); } },
  max6954: { col: "#be123c", name: "LED69", sub: function (c) { return String(c.val); } },
  lcd_20x4: { col: "#be123c", name: "LCD20", sub: function (c) { return String(c.val); } },
  st7735_160: { col: "#be123c", name: "TFT160", sub: function (c) { return String(c.val); } },
  ssd1331: { col: "#be123c", name: "OL96", sub: function (c) { return String(c.val); } },
  drv8833: { col: "#7c2d12", name: "DRV33", sub: function (c) { return String(c.val); } },
  drv8871: { col: "#7c2d12", name: "DRV71", sub: function (c) { return String(c.val); } },
  l293e: { col: "#7c2d12", name: "L293E", sub: function (c) { return String(c.val); } },
  sn754410: { col: "#7c2d12", name: "SN41", sub: function (c) { return String(c.val); } },
  uln2004: { col: "#7c2d12", name: "ULN04", sub: function (c) { return String(c.val); } },
  mc33926: { col: "#7c2d12", name: "MC26", sub: function (c) { return String(c.val); } },
  bd6221: { col: "#7c2d12", name: "BD62", sub: function (c) { return String(c.val); } },
  tb67h420: { col: "#7c2d12", name: "TB67", sub: function (c) { return String(c.val); } },
  a3959: { col: "#7c2d12", name: "A3959", sub: function (c) { return String(c.val); } },
  drv8824: { col: "#7c2d12", name: "DRV24", sub: function (c) { return String(c.val); } },
  esp01: { col: "#1e3a8a", name: "ESP1", sub: function (c) { return String(c.val); } },
  rn2483: { col: "#1e3a8a", name: "LORA", sub: function (c) { return String(c.val); } },
  rfm69: { col: "#1e3a8a", name: "RF69", sub: function (c) { return String(c.val); } },
  rfm95: { col: "#1e3a8a", name: "RF95", sub: function (c) { return String(c.val); } },
  hc12: { col: "#1e3a8a", name: "HC12", sub: function (c) { return String(c.val); } },
  xbee: { col: "#1e3a8a", name: "XBEE", sub: function (c) { return String(c.val); } },
  sim900: { col: "#1e3a8a", name: "GSM90", sub: function (c) { return String(c.val); } },
  m95: { col: "#1e3a8a", name: "M95", sub: function (c) { return String(c.val); } },
  nrf905: { col: "#1e3a8a", name: "RF905", sub: function (c) { return String(c.val); } },
  cc1101: { col: "#1e3a8a", name: "CC11", sub: function (c) { return String(c.val); } },
  lm7809: { col: "#7c3aed", name: "VR09", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lm7812: { col: "#7c3aed", name: "VR12", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lm7905: { col: "#7c3aed", name: "VR-5", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lm7912: { col: "#7c3aed", name: "VR-12", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lm1084: { col: "#7c3aed", name: "LDO84", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lm2678: { col: "#7c3aed", name: "BUK78", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lm5007: { col: "#7c3aed", name: "BUK07", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  mcp1700: { col: "#7c3aed", name: "LDO17", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  mic5205: { col: "#7c3aed", name: "LDO05", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lp2985: { col: "#7c3aed", name: "LDO85", sub: function (c) { return Number(c.val).toFixed(0) + "V"; } },
  lm4871: { col: "#7c3aed", name: "AUD81", sub: function (c) { return String(c.val); } },
  tda2003: { col: "#7c3aed", name: "AMP03", sub: function (c) { return String(c.val); } },
  ds18s20: { col: "#0891b2", name: "SNS20", sub: function (c) { return String(c.val) + "°C"; } },
  lm35: { col: "#0891b2", name: "SNS35", sub: function (c) { return String(c.val) + "°C"; } },
  lm75: { col: "#0891b2", name: "SNS75", sub: function (c) { return String(c.val) + "°C"; } },
  tmp102: { col: "#0891b2", name: "SNS02", sub: function (c) { return String(c.val) + "°C"; } },
  mcp9808: { col: "#0891b2", name: "SNS08", sub: function (c) { return String(c.val) + "°C"; } },
  max31865: { col: "#0891b2", name: "SNS65", sub: function (c) { return String(c.val) + "°C"; } },
  ads1118: { col: "#0891b2", name: "SNS18", sub: function (c) { return String(c.val) + "°C"; } },
  hdc1080: { col: "#0ea5e9", name: "HUM80", sub: function (c) { return String(c.val) + "%"; } },
  htu21d: { col: "#0ea5e9", name: "HUM21", sub: function (c) { return String(c.val) + "%"; } },
  sht21: { col: "#0ea5e9", name: "HUM22", sub: function (c) { return String(c.val) + "%"; } },
  sht35: { col: "#0ea5e9", name: "HUM35", sub: function (c) { return String(c.val) + "%"; } },
  aht10: { col: "#0ea5e9", name: "HUM10", sub: function (c) { return String(c.val) + "%"; } },
  aht20: { col: "#0ea5e9", name: "HUM20", sub: function (c) { return String(c.val) + "%"; } },
  ms5611: { col: "#14b8a6", name: "PRS61", sub: function (c) { return String(c.val) + "hPa"; } },
  lps25h: { col: "#14b8a6", name: "PRS25", sub: function (c) { return String(c.val) + "hPa"; } },
  bmp388: { col: "#14b8a6", name: "PRS88", sub: function (c) { return String(c.val) + "hPa"; } },
  dps310: { col: "#14b8a6", name: "PRS31", sub: function (c) { return String(c.val) + "hPa"; } },
  bmp085: { col: "#14b8a6", name: "PRS85", sub: function (c) { return String(c.val) + "hPa"; } },
  lps22hb: { col: "#14b8a6", name: "PRS22", sub: function (c) { return String(c.val) + "hPa"; } },
  mpx5700: { col: "#14b8a6", name: "PRS57", sub: function (c) { return String(c.val) + "hPa"; } },
  mq131: { col: "#65a30d", name: "GAS31", sub: function (c) { return String(c.val) + "ppm"; } },
  mq303: { col: "#65a30d", name: "GAS03", sub: function (c) { return String(c.val) + "ppm"; } },
  mhz19: { col: "#65a30d", name: "CO2_9", sub: function (c) { return String(c.val) + "ppm"; } },
  sds011: { col: "#65a30d", name: "PM011", sub: function (c) { return String(c.val) + "µg"; } },
  pms5003: { col: "#65a30d", name: "PM503", sub: function (c) { return String(c.val) + "µg"; } },
  ccs811: { col: "#65a30d", name: "CCS11", sub: function (c) { return String(c.val) + "ppb"; } },
  ens160: { col: "#65a30d", name: "ENS60", sub: function (c) { return String(c.val) + "ppb"; } },
  si1145: { col: "#f59e0b", name: "LUX45", sub: function (c) { return String(c.val) + "lux"; } },
  veml7700: { col: "#f59e0b", name: "LUX77", sub: function (c) { return String(c.val) + "lux"; } },
  opt3001: { col: "#f59e0b", name: "LUX01", sub: function (c) { return String(c.val) + "lux"; } },
  max44009: { col: "#f59e0b", name: "LUX09", sub: function (c) { return String(c.val) + "lux"; } },
  ltr329: { col: "#f59e0b", name: "LUX29", sub: function (c) { return String(c.val) + "lux"; } },
  ml8511: { col: "#f59e0b", name: "UV851", sub: function (c) { return String(c.val) + "UVI"; } },
  veml6070: { col: "#f59e0b", name: "UV607", sub: function (c) { return String(c.val) + "UVI"; } },
  ina226: { col: "#dc2626", name: "PWR26", sub: function (c) { return String(c.val) + "V"; } },
  ina260: { col: "#dc2626", name: "PWR60", sub: function (c) { return String(c.val) + "V"; } },
  ina3221: { col: "#dc2626", name: "PWR21", sub: function (c) { return String(c.val) + "V"; } },
  lis3dh: { col: "#7c3aed", name: "ACC3D", sub: function (c) { return String(c.val) + "g"; } },
  mma8452: { col: "#7c3aed", name: "ACC52", sub: function (c) { return String(c.val) + "g"; } },
  adxl335: { col: "#7c3aed", name: "ACC35", sub: function (c) { return String(c.val) + "g"; } },
  adxl362: { col: "#7c3aed", name: "ACC62", sub: function (c) { return String(c.val) + "g"; } },
  lsm6ds3: { col: "#7c3aed", name: "IMU63", sub: function (c) { return String(c.val) + "g"; } },
  icm20948: { col: "#7c3aed", name: "IMU48", sub: function (c) { return String(c.val) + "g"; } },
  bno055: { col: "#7c3aed", name: "IMU55", sub: function (c) { return String(c.val) + "g"; } },
  hmc5883l: { col: "#7c3aed", name: "MAG83", sub: function (c) { return String(c.val) + "µT"; } },
  qmc5883l: { col: "#7c3aed", name: "MAG88", sub: function (c) { return String(c.val) + "µT"; } },
  mlx90393: { col: "#7c3aed", name: "MAG93", sub: function (c) { return String(c.val) + "µT"; } },
  lm7815: { col: "#7c3aed", name: "LDO15", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm7824: { col: "#7c3aed", name: "LDO24", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm7808: { col: "#7c3aed", name: "LDO08", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm7806: { col: "#7c3aed", name: "LDO06", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm317hv: { col: "#7c3aed", name: "LDOHV", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2940: { col: "#7c3aed", name: "LDO40", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps7a47: { col: "#7c3aed", name: "LDO47", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2576: { col: "#7c3aed", name: "BUK76", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2574: { col: "#7c3aed", name: "BUK74", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mp1584: { col: "#7c3aed", name: "BUK84", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps5430: { col: "#7c3aed", name: "BUK30", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mt3608: { col: "#7c3aed", name: "BST08", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2577: { col: "#7c3aed", name: "BST77", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps61023: { col: "#7c3aed", name: "BST23", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  max1771: { col: "#7c3aed", name: "BST71", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm3886: { col: "#7c3aed", name: "AUD86", sub: function (c) { return c.val + "W"; } },
  tda7294: { col: "#7c3aed", name: "AUD94", sub: function (c) { return c.val + "W"; } },
  tda2050: { col: "#7c3aed", name: "AUD50", sub: function (c) { return c.val + "W"; } },
  tda7377: { col: "#7c3aed", name: "AUD77", sub: function (c) { return c.val + "W"; } },
  tpa3116: { col: "#7c3aed", name: "AUD16", sub: function (c) { return c.val + "W"; } },
  tpa2005: { col: "#7c3aed", name: "AUD05", sub: function (c) { return c.val + "W"; } },
  lm4766: { col: "#7c3aed", name: "AUD66", sub: function (c) { return c.val + "W"; } },
  drv8434: { col: "#7c2d12", name: "DRV34", sub: function (c) { return String(c.val); } },
  tmc2209: { col: "#7c2d12", name: "TMC09", sub: function (c) { return String(c.val); } },
  tmc2130: { col: "#7c2d12", name: "TMC30", sub: function (c) { return String(c.val); } },
  l6470: { col: "#7c2d12", name: "STP70", sub: function (c) { return String(c.val); } },
  vnh5019: { col: "#7c2d12", name: "VNH19", sub: function (c) { return String(c.val); } },
  drv8313: { col: "#7c2d12", name: "DRV13", sub: function (c) { return String(c.val); } },
  a4950: { col: "#7c2d12", name: "A4950", sub: function (c) { return String(c.val); } },
  mx1508: { col: "#7c2d12", name: "MX508", sub: function (c) { return String(c.val); } },
  esp32cam: { col: "#0369a1", name: "CAM32", sub: function (c) { return String(c.val); } },
  sx1278: { col: "#0369a1", name: "LOR78", sub: function (c) { return String(c.val); } },
  sx1276: { col: "#0369a1", name: "LOR76", sub: function (c) { return String(c.val); } },
  nrf52832: { col: "#0369a1", name: "BLE32", sub: function (c) { return String(c.val); } },
  hm10: { col: "#0369a1", name: "BLE10", sub: function (c) { return String(c.val); } },
  jdy23: { col: "#0369a1", name: "BLE23", sub: function (c) { return String(c.val); } },
  ublox_neo6m: { col: "#0369a1", name: "GPS06", sub: function (c) { return String(c.val); } },
  ublox_neo7m: { col: "#0369a1", name: "GPS07", sub: function (c) { return String(c.val); } },
  w5500: { col: "#0369a1", name: "ETH55", sub: function (c) { return String(c.val); } },
  cp2102: { col: "#0369a1", name: "USB02", sub: function (c) { return String(c.val); } },
  ch340: { col: "#0369a1", name: "USB40", sub: function (c) { return String(c.val); } },
  max485: { col: "#0369a1", name: "RS485", sub: function (c) { return String(c.val); } },
  mcp2515: { col: "#0369a1", name: "CAN15", sub: function (c) { return String(c.val); } },
  ssd1322: { col: "#0f766e", name: "DSP22", sub: function (c) { return String(c.val); } },
  ssd1327: { col: "#0f766e", name: "DSP27", sub: function (c) { return String(c.val); } },
  ssd1306_64: { col: "#0f766e", name: "DSP64", sub: function (c) { return String(c.val); } },
  st7789: { col: "#0f766e", name: "DSP89", sub: function (c) { return String(c.val); } },
  ili9488: { col: "#0f766e", name: "DSP88", sub: function (c) { return String(c.val); } },
  hd44780: { col: "#0f766e", name: "DSP44", sub: function (c) { return String(c.val); } },
  tm1637: { col: "#0f766e", name: "DSP37", sub: function (c) { return String(c.val); } },
  ht16k33: { col: "#0f766e", name: "DSP33", sub: function (c) { return String(c.val); } },
  cd4017b: { col: "#4f46e5", name: "CNT17", sub: function (c) { return String(c.val); } },
  ic_74hc14: { col: "#4f46e5", name: "LGC14", sub: function (c) { return String(c.val); } },
  ic_74hc04: { col: "#4f46e5", name: "LGC04", sub: function (c) { return String(c.val); } },
  ic_74hc08: { col: "#4f46e5", name: "LGC08", sub: function (c) { return String(c.val); } },
  ic_74hc32: { col: "#4f46e5", name: "LGC32", sub: function (c) { return String(c.val); } },
  ic_74hc86: { col: "#4f46e5", name: "LGC86", sub: function (c) { return String(c.val); } },
  ic_74hc74: { col: "#4f46e5", name: "LGC74", sub: function (c) { return String(c.val); } },
  ic_74hc590: { col: "#4f46e5", name: "LGC90", sub: function (c) { return String(c.val); } },
  ic_74hc4067: { col: "#4f46e5", name: "MUX67", sub: function (c) { return String(c.val); } },
  at24c64: { col: "#4f46e5", name: "MEM64", sub: function (c) { return String(c.val); } },
  at24c128: { col: "#4f46e5", name: "MEM28", sub: function (c) { return String(c.val); } },
  w25q128: { col: "#4f46e5", name: "MEM12", sub: function (c) { return String(c.val); } },
  fm25v02: { col: "#4f46e5", name: "MEM02", sub: function (c) { return String(c.val); } },
  mcp23s17: { col: "#4f46e5", name: "IOX17", sub: function (c) { return String(c.val); } },
  tca9534: { col: "#4f46e5", name: "IOX34", sub: function (c) { return String(c.val); } },
  max7301: { col: "#4f46e5", name: "IOX01", sub: function (c) { return String(c.val); } },
  tmp117: { col: "#0891b2", name: "TMP117", sub: function (c) { return String(c.val) + "°C"; } },
  max30205: { col: "#0891b2", name: "MAX205", sub: function (c) { return String(c.val) + "°C"; } },
  amg8833: { col: "#0891b2", name: "AMG833", sub: function (c) { return String(c.val) + "°C"; } },
  mlx90640: { col: "#0891b2", name: "MLX640", sub: function (c) { return String(c.val) + "°C"; } },
  lm73: { col: "#0891b2", name: "LM73", sub: function (c) { return String(c.val) + "°C"; } },
  si7050: { col: "#0891b2", name: "SI7050", sub: function (c) { return String(c.val) + "°C"; } },
  ds28ea00: { col: "#0891b2", name: "DS2A00", sub: function (c) { return String(c.val) + "°C"; } },
  ad8495: { col: "#0891b2", name: "AD8495", sub: function (c) { return String(c.val) + "°C"; } },
  hih6130: { col: "#0ea5e9", name: "HIH130", sub: function (c) { return String(c.val) + "%"; } },
  dht21: { col: "#0ea5e9", name: "DHT21", sub: function (c) { return String(c.val) + "%"; } },
  sht40: { col: "#0ea5e9", name: "SHT40", sub: function (c) { return String(c.val) + "%"; } },
  sht45: { col: "#0ea5e9", name: "SHT45", sub: function (c) { return String(c.val) + "%"; } },
  hdc2080: { col: "#0ea5e9", name: "HDC080", sub: function (c) { return String(c.val) + "%"; } },
  bme688: { col: "#0ea5e9", name: "BME688", sub: function (c) { return String(c.val) + "%"; } },
  bmp390: { col: "#6366f1", name: "BMP390", sub: function (c) { return String(c.val) + "hPa"; } },
  bmp581: { col: "#6366f1", name: "BMP581", sub: function (c) { return String(c.val) + "hPa"; } },
  lps35hw: { col: "#6366f1", name: "LPS5HW", sub: function (c) { return String(c.val) + "hPa"; } },
  lps33hw: { col: "#6366f1", name: "LPS3HW", sub: function (c) { return String(c.val) + "hPa"; } },
  spl06: { col: "#6366f1", name: "SPL06", sub: function (c) { return String(c.val) + "hPa"; } },
  ms5837: { col: "#6366f1", name: "MS5837", sub: function (c) { return String(c.val) + "hPa"; } },
  mq137: { col: "#b45309", name: "MQ137", sub: function (c) { return String(c.val) + "ppm"; } },
  mq138: { col: "#b45309", name: "MQ138", sub: function (c) { return String(c.val) + "ppm"; } },
  mq214: { col: "#b45309", name: "MQ214", sub: function (c) { return String(c.val) + "ppm"; } },
  mq216: { col: "#b45309", name: "MQ216", sub: function (c) { return String(c.val) + "ppm"; } },
  scd30: { col: "#b45309", name: "SCD30", sub: function (c) { return String(c.val) + "ppm"; } },
  scd40: { col: "#b45309", name: "SCD40", sub: function (c) { return String(c.val) + "ppm"; } },
  scd41: { col: "#b45309", name: "SCD41", sub: function (c) { return String(c.val) + "ppm"; } },
  sgp40: { col: "#b45309", name: "SGP40", sub: function (c) { return String(c.val) + "ppm"; } },
  sen54: { col: "#b45309", name: "SEN54", sub: function (c) { return String(c.val) + "ppm"; } },
  ags02ma: { col: "#b45309", name: "AGS2MA", sub: function (c) { return String(c.val) + "ppm"; } },
  as7341: { col: "#ca8a04", name: "AS7341", sub: function (c) { return String(c.val) + "lux"; } },
  as7262: { col: "#ca8a04", name: "AS7262", sub: function (c) { return String(c.val) + "lux"; } },
  tsl2591: { col: "#ca8a04", name: "TSL591", sub: function (c) { return String(c.val) + "lux"; } },
  veml6075: { col: "#ca8a04", name: "VEM075", sub: function (c) { return String(c.val) + "lux"; } },
  guva_s12sd: { col: "#ca8a04", name: "GUV2SD", sub: function (c) { return String(c.val) + "lux"; } },
  bh1745: { col: "#ca8a04", name: "BH1745", sub: function (c) { return String(c.val) + "lux"; } },
  isl29125: { col: "#ca8a04", name: "ISL125", sub: function (c) { return String(c.val) + "lux"; } },
  apds9306: { col: "#ca8a04", name: "APD306", sub: function (c) { return String(c.val) + "lux"; } },
  mpu6500: { col: "#7c3aed", name: "MPU500", sub: function (c) { return String(c.val) + "g"; } },
  lsm9ds1: { col: "#7c3aed", name: "LSMDS1", sub: function (c) { return String(c.val) + "g"; } },
  lsm303: { col: "#7c3aed", name: "LSM303", sub: function (c) { return String(c.val) + "g"; } },
  l3gd20h: { col: "#7c3aed", name: "L3G20H", sub: function (c) { return String(c.val) + "g"; } },
  bmi160: { col: "#7c3aed", name: "BMI160", sub: function (c) { return String(c.val) + "g"; } },
  bmi270: { col: "#7c3aed", name: "BMI270", sub: function (c) { return String(c.val) + "g"; } },
  adxl375: { col: "#7c3aed", name: "ADX375", sub: function (c) { return String(c.val) + "g"; } },
  icm42688: { col: "#7c3aed", name: "ICM688", sub: function (c) { return String(c.val) + "g"; } },
  lis2dh12: { col: "#7c3aed", name: "LISH12", sub: function (c) { return String(c.val) + "g"; } },
  kxtj3: { col: "#7c3aed", name: "KXTJ3", sub: function (c) { return String(c.val) + "g"; } },
  vl53l1x: { col: "#059669", name: "VL5L1X", sub: function (c) { return String(c.val) + "cm"; } },
  gp2y0a21: { col: "#059669", name: "GP2A21", sub: function (c) { return String(c.val) + "cm"; } },
  gp2y0a02: { col: "#059669", name: "GP2A02", sub: function (c) { return String(c.val) + "cm"; } },
  us100: { col: "#059669", name: "US100", sub: function (c) { return String(c.val) + "cm"; } },
  a02yyuw: { col: "#059669", name: "A02YUW", sub: function (c) { return String(c.val) + "cm"; } },
  ld2410: { col: "#059669", name: "LD2410", sub: function (c) { return String(c.val) + "cm"; } },
  rcwl0516: { col: "#059669", name: "RCW516", sub: function (c) { return String(c.val) + "cm"; } },
  tfmini: { col: "#059669", name: "TFMINI", sub: function (c) { return String(c.val) + "cm"; } },
  tf_luna: { col: "#059669", name: "TFLUNA", sub: function (c) { return String(c.val) + "cm"; } },
  vcnl4040: { col: "#059669", name: "VCN040", sub: function (c) { return String(c.val) + "cm"; } },
  jsn_sr04t: { col: "#059669", name: "JSN04T", sub: function (c) { return String(c.val) + "cm"; } },
  max30100: { col: "#dc2626", name: "MAX100", sub: function (c) { return String(c.val) + "BPM"; } },
  ad8232: { col: "#dc2626", name: "AD8232", sub: function (c) { return String(c.val) + "BPM"; } },
  pulse_sensor: { col: "#dc2626", name: "PULSOR", sub: function (c) { return String(c.val) + "BPM"; } },
  gsr_sensor: { col: "#dc2626", name: "GSRSOR", sub: function (c) { return String(c.val) + "BPM"; } },
  r307: { col: "#dc2626", name: "R307", sub: function (c) { return String(c.val) + "BPM"; } },
  ina169: { col: "#ea580c", name: "INA169", sub: function (c) { return String(c.val) + "A"; } },
  acs758: { col: "#ea580c", name: "ACS758", sub: function (c) { return String(c.val) + "A"; } },
  max471: { col: "#ea580c", name: "MAX471", sub: function (c) { return String(c.val) + "A"; } },
  pzem004t: { col: "#ea580c", name: "PZE04T", sub: function (c) { return String(c.val) + "A"; } },
  hlw8012: { col: "#ea580c", name: "HLW012", sub: function (c) { return String(c.val) + "A"; } },
  ina228: { col: "#ea580c", name: "INA228", sub: function (c) { return String(c.val) + "A"; } },
  ina238: { col: "#ea580c", name: "INA238", sub: function (c) { return String(c.val) + "A"; } },
  ss49e: { col: "#7c3aed", name: "SS49E", sub: function (c) { return String(c.val) + "µT"; } },
  a1302: { col: "#7c3aed", name: "A1302", sub: function (c) { return String(c.val) + "µT"; } },
  drv5053: { col: "#7c3aed", name: "DRV053", sub: function (c) { return String(c.val) + "µT"; } },
  as5600: { col: "#7c3aed", name: "AS5600", sub: function (c) { return String(c.val) + "µT"; } },
  as5048a: { col: "#7c3aed", name: "AS548A", sub: function (c) { return String(c.val) + "µT"; } },
  sh1106: { col: "#be123c", name: "SH1106", sub: function (c) { return String(c.val); } },
  ssd1305: { col: "#be123c", name: "SSD305", sub: function (c) { return String(c.val); } },
  gc9a01: { col: "#be123c", name: "GC9A01", sub: function (c) { return String(c.val); } },
  st7796: { col: "#be123c", name: "ST7796", sub: function (c) { return String(c.val); } },
  ili9225: { col: "#be123c", name: "ILI225", sub: function (c) { return String(c.val); } },
  ssd1963: { col: "#be123c", name: "SSD963", sub: function (c) { return String(c.val); } },
  epd_154: { col: "#be123c", name: "EPD154", sub: function (c) { return String(c.val); } },
  epd_213: { col: "#be123c", name: "EPD213", sub: function (c) { return String(c.val); } },
  epd_29: { col: "#be123c", name: "EPD29", sub: function (c) { return String(c.val); } },
  lcd_12864: { col: "#be123c", name: "LCD864", sub: function (c) { return String(c.val); } },
  lcd_16x4: { col: "#be123c", name: "LCD6X4", sub: function (c) { return String(c.val); } },
  lcd_8x2: { col: "#be123c", name: "LCD8X2", sub: function (c) { return String(c.val); } },
  tm1638: { col: "#be123c", name: "TM1638", sub: function (c) { return String(c.val); } },
  ht1621: { col: "#be123c", name: "HT1621", sub: function (c) { return String(c.val); } },
  drv8847: { col: "#7c2d12", name: "DRV847", sub: function (c) { return String(c.val); } },
  drv8880: { col: "#7c2d12", name: "DRV880", sub: function (c) { return String(c.val); } },
  tmc2208: { col: "#7c2d12", name: "TMC208", sub: function (c) { return String(c.val); } },
  tmc2160: { col: "#7c2d12", name: "TMC160", sub: function (c) { return String(c.val); } },
  tmc5160: { col: "#7c2d12", name: "TMC162", sub: function (c) { return String(c.val); } },
  l6208: { col: "#7c2d12", name: "L6208", sub: function (c) { return String(c.val); } },
  l6235: { col: "#7c2d12", name: "L6235", sub: function (c) { return String(c.val); } },
  vnh2sp30: { col: "#7c2d12", name: "VNHP30", sub: function (c) { return String(c.val); } },
  ibt2: { col: "#7c2d12", name: "IBT2", sub: function (c) { return String(c.val); } },
  lv8548: { col: "#7c2d12", name: "LV8548", sub: function (c) { return String(c.val); } },
  lm7818: { col: "#7c3aed", name: "LM7818", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm78l05: { col: "#7c3aed", name: "LM7L05", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm79l05: { col: "#7c3aed", name: "LM7L02", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm317l: { col: "#7c3aed", name: "LM317L", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm350: { col: "#7c3aed", name: "LM350", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ld1117: { col: "#7c3aed", name: "LD1117", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xc6206: { col: "#7c3aed", name: "XC6206", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ap2112: { col: "#7c3aed", name: "AP2112", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tlv1117: { col: "#7c3aed", name: "TLV117", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lt3045: { col: "#7c3aed", name: "LT3045", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2575: { col: "#7c3aed", name: "LM2575", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2595: { col: "#7c3aed", name: "LM2595", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xl4015: { col: "#7c3aed", name: "XL4015", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xl4005: { col: "#7c3aed", name: "XL4005", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xl7005: { col: "#7c3aed", name: "XL7005", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mp2307: { col: "#7c3aed", name: "MP2307", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mp2315: { col: "#7c3aed", name: "MP2315", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps54331: { col: "#7c3aed", name: "TPS331", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  sx1308: { col: "#7c3aed", name: "SX1308", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  cn3791: { col: "#7c3aed", name: "CN3791", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  bq24074: { col: "#7c3aed", name: "BQ2074", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tp5100: { col: "#7c3aed", name: "TP5100", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ip5306: { col: "#7c3aed", name: "IP5306", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  esp32_c3: { col: "#1e3a8a", name: "ESP2C3", sub: function (c) { return String(c.val); } },
  esp32_s3: { col: "#1e3a8a", name: "ESP2S3", sub: function (c) { return String(c.val); } },
  nrf52840: { col: "#1e3a8a", name: "NRF840", sub: function (c) { return String(c.val); } },
  hc06: { col: "#1e3a8a", name: "HC06", sub: function (c) { return String(c.val); } },
  hm11: { col: "#1e3a8a", name: "HM11", sub: function (c) { return String(c.val); } },
  jdy31: { col: "#1e3a8a", name: "JDY31", sub: function (c) { return String(c.val); } },
  e32: { col: "#1e3a8a", name: "E32", sub: function (c) { return String(c.val); } },
  sx1262: { col: "#1e3a8a", name: "SX1262", sub: function (c) { return String(c.val); } },
  dw1000: { col: "#1e3a8a", name: "DW1000", sub: function (c) { return String(c.val); } },
  pn532: { col: "#1e3a8a", name: "PN532", sub: function (c) { return String(c.val); } },
  w5100: { col: "#1e3a8a", name: "W5100", sub: function (c) { return String(c.val); } },
  enc424j600: { col: "#1e3a8a", name: "ENC600", sub: function (c) { return String(c.val); } },
  mcp2551: { col: "#1e3a8a", name: "MCP551", sub: function (c) { return String(c.val); } },
  tja1050: { col: "#1e3a8a", name: "TJA050", sub: function (c) { return String(c.val); } },
  sn65hvd230: { col: "#1e3a8a", name: "SN6230", sub: function (c) { return String(c.val); } },
  max232: { col: "#1e3a8a", name: "MAX232", sub: function (c) { return String(c.val); } },
  max3232: { col: "#1e3a8a", name: "MAX233", sub: function (c) { return String(c.val); } },
  ft232: { col: "#1e3a8a", name: "FT232", sub: function (c) { return String(c.val); } },
  pl2303: { col: "#1e3a8a", name: "PL2303", sub: function (c) { return String(c.val); } },
  cp2104: { col: "#1e3a8a", name: "CP2104", sub: function (c) { return String(c.val); } },
  l76k: { col: "#1e3a8a", name: "L76K", sub: function (c) { return String(c.val); } },
  neo_m8n: { col: "#1e3a8a", name: "NEOM8N", sub: function (c) { return String(c.val); } },
  sim7600: { col: "#1e3a8a", name: "SIM600", sub: function (c) { return String(c.val); } },
  sim868: { col: "#1e3a8a", name: "SIM868", sub: function (c) { return String(c.val); } },
  a7670: { col: "#1e3a8a", name: "A7670", sub: function (c) { return String(c.val); } },
  ic_74hc02: { col: "#4f46e5", name: "HC02", sub: function (c) { return String(c.val); } },
  ic_74hc10: { col: "#4f46e5", name: "HC10", sub: function (c) { return String(c.val); } },
  ic_74hc20: { col: "#4f46e5", name: "HC20", sub: function (c) { return String(c.val); } },
  ic_74hc30: { col: "#4f46e5", name: "HC30", sub: function (c) { return String(c.val); } },
  ic_74hc125: { col: "#4f46e5", name: "HC125", sub: function (c) { return String(c.val); } },
  ic_74hc157: { col: "#4f46e5", name: "HC157", sub: function (c) { return String(c.val); } },
  ic_74hc151: { col: "#4f46e5", name: "HC151", sub: function (c) { return String(c.val); } },
  ic_74hc139: { col: "#4f46e5", name: "HC139", sub: function (c) { return String(c.val); } },
  ic_74hc154: { col: "#4f46e5", name: "HC154", sub: function (c) { return String(c.val); } },
  ic_74hc161: { col: "#4f46e5", name: "HC161", sub: function (c) { return String(c.val); } },
  ic_74hc164: { col: "#4f46e5", name: "HC164", sub: function (c) { return String(c.val); } },
  ic_74hc166: { col: "#4f46e5", name: "HC166", sub: function (c) { return String(c.val); } },
  ic_74hc174: { col: "#4f46e5", name: "HC174", sub: function (c) { return String(c.val); } },
  ic_74hc175: { col: "#4f46e5", name: "HC175", sub: function (c) { return String(c.val); } },
  ic_74hc193: { col: "#4f46e5", name: "HC193", sub: function (c) { return String(c.val); } },
  ic_74hc244: { col: "#4f46e5", name: "HC244", sub: function (c) { return String(c.val); } },
  ic_74hc245: { col: "#4f46e5", name: "HC245", sub: function (c) { return String(c.val); } },
  ic_74hc283: { col: "#4f46e5", name: "HC283", sub: function (c) { return String(c.val); } },
  ic_74hc374: { col: "#4f46e5", name: "HC374", sub: function (c) { return String(c.val); } },
  ic_74hc4040: { col: "#4f46e5", name: "HC4040", sub: function (c) { return String(c.val); } },
  ic_74hc4046: { col: "#4f46e5", name: "HC4046", sub: function (c) { return String(c.val); } },
  ic_74hc4053: { col: "#4f46e5", name: "HC4053", sub: function (c) { return String(c.val); } },
  ic_74hc4094: { col: "#4f46e5", name: "HC4094", sub: function (c) { return String(c.val); } },
  mcp23008: { col: "#4f46e5", name: "MCP008", sub: function (c) { return String(c.val); } },
  tca9535: { col: "#4f46e5", name: "TCA535", sub: function (c) { return String(c.val); } },
  txs0108: { col: "#4f46e5", name: "TXS108", sub: function (c) { return String(c.val); } },
  sn74lvc245: { col: "#4f46e5", name: "SN7245", sub: function (c) { return String(c.val); } },
  at24c02: { col: "#4f46e5", name: "AT2C02", sub: function (c) { return String(c.val); } },
  at24c08: { col: "#4f46e5", name: "AT2C08", sub: function (c) { return String(c.val); } },
  at24c16: { col: "#4f46e5", name: "AT2C16", sub: function (c) { return String(c.val); } },
  lm1875: { col: "#7c3aed", name: "LM1875", sub: function (c) { return c.val + "W"; } },
  tda2040: { col: "#7c3aed", name: "TDA040", sub: function (c) { return c.val + "W"; } },
  tda7498: { col: "#7c3aed", name: "TDA498", sub: function (c) { return c.val + "W"; } },
  tpa3110: { col: "#7c3aed", name: "TPA110", sub: function (c) { return c.val + "W"; } },
  pam8610: { col: "#7c3aed", name: "PAM610", sub: function (c) { return c.val + "W"; } },
  pam8302: { col: "#7c3aed", name: "PAM302", sub: function (c) { return c.val + "W"; } },
  max9744: { col: "#7c3aed", name: "MAX744", sub: function (c) { return c.val + "W"; } },
  mcp6002: { col: "#7c3aed", name: "MCP002", sub: function (c) { return c.val + "x"; } },
  mcp6022: { col: "#7c3aed", name: "MCP022", sub: function (c) { return c.val + "x"; } },
  tl082: { col: "#7c3aed", name: "TL082", sub: function (c) { return c.val + "x"; } },
  tl084: { col: "#7c3aed", name: "TL084", sub: function (c) { return c.val + "x"; } },
  lf353: { col: "#7c3aed", name: "LF353", sub: function (c) { return c.val + "x"; } },
  lf411: { col: "#7c3aed", name: "LF411", sub: function (c) { return c.val + "x"; } },
  op07: { col: "#7c3aed", name: "OP07", sub: function (c) { return c.val + "x"; } },
  op27: { col: "#7c3aed", name: "OP27", sub: function (c) { return c.val + "x"; } },
  ad8605: { col: "#7c3aed", name: "AD8605", sub: function (c) { return c.val + "x"; } },
  tmp116: { col: "#0891b2", name: "TMP116", sub: function (c) { return String(c.val) + "°C"; } },
  tmp1075: { col: "#0891b2", name: "TMP075", sub: function (c) { return String(c.val) + "°C"; } },
  max6633: { col: "#0891b2", name: "MAX633", sub: function (c) { return String(c.val) + "°C"; } },
  mcp9701: { col: "#0891b2", name: "MCP701", sub: function (c) { return String(c.val) + "°C"; } },
  lm19: { col: "#0891b2", name: "LM19", sub: function (c) { return String(c.val) + "°C"; } },
  lm34: { col: "#0891b2", name: "LM34", sub: function (c) { return String(c.val) + "°C"; } },
  lm335: { col: "#0891b2", name: "LM335", sub: function (c) { return String(c.val) + "°C"; } },
  ad590: { col: "#0891b2", name: "AD590", sub: function (c) { return String(c.val) + "°C"; } },
  tmp35: { col: "#0891b2", name: "TMP35", sub: function (c) { return String(c.val) + "°C"; } },
  tmp37: { col: "#0891b2", name: "TMP37", sub: function (c) { return String(c.val) + "°C"; } },
  sts31: { col: "#0891b2", name: "STS31", sub: function (c) { return String(c.val) + "°C"; } },
  stlm20: { col: "#0891b2", name: "STLM20", sub: function (c) { return String(c.val) + "°C"; } },
  sht85: { col: "#0ea5e9", name: "SHT85", sub: function (c) { return String(c.val) + "%"; } },
  hih7130: { col: "#0ea5e9", name: "HIH132", sub: function (c) { return String(c.val) + "%"; } },
  hts221: { col: "#0ea5e9", name: "HTS221", sub: function (c) { return String(c.val) + "%"; } },
  hdc3020: { col: "#0ea5e9", name: "HDC020", sub: function (c) { return String(c.val) + "%"; } },
  shtc3: { col: "#0ea5e9", name: "SHTC3", sub: function (c) { return String(c.val) + "%"; } },
  shtc1: { col: "#0ea5e9", name: "SHTC1", sub: function (c) { return String(c.val) + "%"; } },
  si7020: { col: "#0ea5e9", name: "SI7020", sub: function (c) { return String(c.val) + "%"; } },
  am2301: { col: "#0ea5e9", name: "AM2301", sub: function (c) { return String(c.val) + "%"; } },
  am2302: { col: "#0ea5e9", name: "AM2302", sub: function (c) { return String(c.val) + "%"; } },
  capacitive_soil: { col: "#0ea5e9", name: "CAPOIL", sub: function (c) { return String(c.val) + "%"; } },
  fc28: { col: "#0ea5e9", name: "FC28", sub: function (c) { return String(c.val) + "%"; } },
  lps22hh: { col: "#6366f1", name: "LPS2HH", sub: function (c) { return String(c.val) + "hPa"; } },
  mpl115a2: { col: "#6366f1", name: "MPL5A2", sub: function (c) { return String(c.val) + "hPa"; } },
  ms5803: { col: "#6366f1", name: "MS5803", sub: function (c) { return String(c.val) + "hPa"; } },
  ms5607: { col: "#6366f1", name: "MS5607", sub: function (c) { return String(c.val) + "hPa"; } },
  mprls: { col: "#6366f1", name: "MPRLS", sub: function (c) { return String(c.val) + "hPa"; } },
  bmp384: { col: "#6366f1", name: "BMP384", sub: function (c) { return String(c.val) + "hPa"; } },
  icp10125: { col: "#6366f1", name: "ICP125", sub: function (c) { return String(c.val) + "hPa"; } },
  icp20100: { col: "#6366f1", name: "ICP100", sub: function (c) { return String(c.val) + "hPa"; } },
  mpx4115: { col: "#6366f1", name: "MPX115", sub: function (c) { return String(c.val) + "hPa"; } },
  mpxv7002: { col: "#6366f1", name: "MPX002", sub: function (c) { return String(c.val) + "hPa"; } },
  xgzp6847: { col: "#6366f1", name: "XGZ847", sub: function (c) { return String(c.val) + "hPa"; } },
  mq136: { col: "#b45309", name: "MQ136", sub: function (c) { return String(c.val) + "ppm"; } },
  mq139: { col: "#b45309", name: "MQ139", sub: function (c) { return String(c.val) + "ppm"; } },
  mq309: { col: "#b45309", name: "MQ309", sub: function (c) { return String(c.val) + "ppm"; } },
  tgs2600: { col: "#b45309", name: "TGS600", sub: function (c) { return String(c.val) + "ppm"; } },
  tgs2602: { col: "#b45309", name: "TGS602", sub: function (c) { return String(c.val) + "ppm"; } },
  tgs2620: { col: "#b45309", name: "TGS620", sub: function (c) { return String(c.val) + "ppm"; } },
  mics5524: { col: "#b45309", name: "MIC524", sub: function (c) { return String(c.val) + "ppm"; } },
  mics6814: { col: "#b45309", name: "MIC814", sub: function (c) { return String(c.val) + "ppm"; } },
  mh_z14a: { col: "#b45309", name: "MHZ14A", sub: function (c) { return String(c.val) + "ppm"; } },
  mh_z16: { col: "#b45309", name: "MHZ16", sub: function (c) { return String(c.val) + "ppm"; } },
  s8_co2: { col: "#b45309", name: "S8CO2", sub: function (c) { return String(c.val) + "ppm"; } },
  iaq_core: { col: "#b45309", name: "IAQORE", sub: function (c) { return String(c.val) + "ppm"; } },
  zmod4410: { col: "#b45309", name: "ZMO410", sub: function (c) { return String(c.val) + "ppm"; } },
  zh03b: { col: "#b45309", name: "ZH03B", sub: function (c) { return String(c.val) + "ppm"; } },
  tsl2572: { col: "#ca8a04", name: "TSL572", sub: function (c) { return String(c.val) + "lux"; } },
  veml3235: { col: "#ca8a04", name: "VEM235", sub: function (c) { return String(c.val) + "lux"; } },
  opt4048: { col: "#ca8a04", name: "OPT048", sub: function (c) { return String(c.val) + "lux"; } },
  opt3004: { col: "#ca8a04", name: "OPT004", sub: function (c) { return String(c.val) + "lux"; } },
  ltr390: { col: "#ca8a04", name: "LTR390", sub: function (c) { return String(c.val) + "lux"; } },
  ltr303: { col: "#ca8a04", name: "LTR303", sub: function (c) { return String(c.val) + "lux"; } },
  ltr559: { col: "#ca8a04", name: "LTR559", sub: function (c) { return String(c.val) + "lux"; } },
  as7343: { col: "#ca8a04", name: "AS7343", sub: function (c) { return String(c.val) + "lux"; } },
  as7265x: { col: "#ca8a04", name: "AS765X", sub: function (c) { return String(c.val) + "lux"; } },
  ap3216: { col: "#ca8a04", name: "AP3216", sub: function (c) { return String(c.val) + "lux"; } },
  vcnl4200: { col: "#ca8a04", name: "VCN200", sub: function (c) { return String(c.val) + "lux"; } },
  si1133: { col: "#ca8a04", name: "SI1133", sub: function (c) { return String(c.val) + "lux"; } },
  mpu6886: { col: "#7c3aed", name: "MPU886", sub: function (c) { return String(c.val) + "g"; } },
  mpu9255: { col: "#7c3aed", name: "MPU255", sub: function (c) { return String(c.val) + "g"; } },
  lsm6dso: { col: "#7c3aed", name: "LSMDSO", sub: function (c) { return String(c.val) + "g"; } },
  lsm6dsox: { col: "#7c3aed", name: "LSMSOX", sub: function (c) { return String(c.val) + "g"; } },
  lis3mdl: { col: "#7c3aed", name: "LISMDL", sub: function (c) { return String(c.val) + "g"; } },
  lis2mdl: { col: "#7c3aed", name: "LISMD2", sub: function (c) { return String(c.val) + "g"; } },
  lis3dsh: { col: "#7c3aed", name: "LISDSH", sub: function (c) { return String(c.val) + "g"; } },
  mma7660: { col: "#7c3aed", name: "MMA660", sub: function (c) { return String(c.val) + "g"; } },
  mma8451: { col: "#7c3aed", name: "MMA451", sub: function (c) { return String(c.val) + "g"; } },
  mma7361: { col: "#7c3aed", name: "MMA361", sub: function (c) { return String(c.val) + "g"; } },
  bma280: { col: "#7c3aed", name: "BMA280", sub: function (c) { return String(c.val) + "g"; } },
  bma423: { col: "#7c3aed", name: "BMA423", sub: function (c) { return String(c.val) + "g"; } },
  bmi088: { col: "#7c3aed", name: "BMI088", sub: function (c) { return String(c.val) + "g"; } },
  bmx160: { col: "#7c3aed", name: "BMX160", sub: function (c) { return String(c.val) + "g"; } },
  icm20689: { col: "#7c3aed", name: "ICM689", sub: function (c) { return String(c.val) + "g"; } },
  icm42605: { col: "#7c3aed", name: "ICM605", sub: function (c) { return String(c.val) + "g"; } },
  fxos8700: { col: "#7c3aed", name: "FXO700", sub: function (c) { return String(c.val) + "g"; } },
  fxas21002: { col: "#7c3aed", name: "FXA002", sub: function (c) { return String(c.val) + "g"; } },
  l3g4200d: { col: "#7c3aed", name: "L3G00D", sub: function (c) { return String(c.val) + "g"; } },
  itg3200: { col: "#7c3aed", name: "ITG200", sub: function (c) { return String(c.val) + "g"; } },
  vl53l4cd: { col: "#059669", name: "VL54CD", sub: function (c) { return String(c.val) + "cm"; } },
  vl53l3cx: { col: "#059669", name: "VL53CX", sub: function (c) { return String(c.val) + "cm"; } },
  tof050c: { col: "#059669", name: "TOF50C", sub: function (c) { return String(c.val) + "cm"; } },
  tf02: { col: "#059669", name: "TF02", sub: function (c) { return String(c.val) + "cm"; } },
  tf03: { col: "#059669", name: "TF03", sub: function (c) { return String(c.val) + "cm"; } },
  hcsr05: { col: "#059669", name: "HCSR05", sub: function (c) { return String(c.val) + "cm"; } },
  srf05: { col: "#059669", name: "SRF05", sub: function (c) { return String(c.val) + "cm"; } },
  maxsonar_ez1: { col: "#059669", name: "MAXEZ1", sub: function (c) { return String(c.val) + "cm"; } },
  us015: { col: "#059669", name: "US015", sub: function (c) { return String(c.val) + "cm"; } },
  us020: { col: "#059669", name: "US020", sub: function (c) { return String(c.val) + "cm"; } },
  urm37: { col: "#059669", name: "URM37", sub: function (c) { return String(c.val) + "cm"; } },
  ld2450: { col: "#059669", name: "LD2450", sub: function (c) { return String(c.val) + "cm"; } },
  ld2420: { col: "#059669", name: "LD2420", sub: function (c) { return String(c.val) + "cm"; } },
  hb100: { col: "#059669", name: "HB100", sub: function (c) { return String(c.val) + "cm"; } },
  sen0311: { col: "#059669", name: "SEN311", sub: function (c) { return String(c.val) + "cm"; } },
  max30101: { col: "#dc2626", name: "MAX101", sub: function (c) { return String(c.val) + "BPM"; } },
  max86150: { col: "#dc2626", name: "MAX150", sub: function (c) { return String(c.val) + "BPM"; } },
  afe4490: { col: "#dc2626", name: "AFE490", sub: function (c) { return String(c.val) + "BPM"; } },
  ads1292: { col: "#dc2626", name: "ADS292", sub: function (c) { return String(c.val) + "BPM"; } },
  ad8233: { col: "#dc2626", name: "AD8233", sub: function (c) { return String(c.val) + "BPM"; } },
  max30003: { col: "#dc2626", name: "MAX003", sub: function (c) { return String(c.val) + "BPM"; } },
  emg_sensor: { col: "#dc2626", name: "EMGSOR", sub: function (c) { return String(c.val) + "BPM"; } },
  muscle_v3: { col: "#dc2626", name: "MUSEV3", sub: function (c) { return String(c.val) + "BPM"; } },
  gsr_grove: { col: "#dc2626", name: "GSROVE", sub: function (c) { return String(c.val) + "BPM"; } },
  skin_temp_mlx: { col: "#dc2626", name: "SKIMLX", sub: function (c) { return String(c.val) + "BPM"; } },
  ina180: { col: "#ea580c", name: "INA180", sub: function (c) { return String(c.val) + "A"; } },
  ina199: { col: "#ea580c", name: "INA199", sub: function (c) { return String(c.val) + "A"; } },
  ina210: { col: "#ea580c", name: "INA210", sub: function (c) { return String(c.val) + "A"; } },
  ina230: { col: "#ea580c", name: "INA230", sub: function (c) { return String(c.val) + "A"; } },
  ina233: { col: "#ea580c", name: "INA233", sub: function (c) { return String(c.val) + "A"; } },
  acs711: { col: "#ea580c", name: "ACS711", sub: function (c) { return String(c.val) + "A"; } },
  acs723: { col: "#ea580c", name: "ACS723", sub: function (c) { return String(c.val) + "A"; } },
  acs724: { col: "#ea580c", name: "ACS724", sub: function (c) { return String(c.val) + "A"; } },
  acs781: { col: "#ea580c", name: "ACS781", sub: function (c) { return String(c.val) + "A"; } },
  max9611: { col: "#ea580c", name: "MAX611", sub: function (c) { return String(c.val) + "A"; } },
  ltc4151: { col: "#ea580c", name: "LTC151", sub: function (c) { return String(c.val) + "A"; } },
  ltc2945: { col: "#ea580c", name: "LTC945", sub: function (c) { return String(c.val) + "A"; } },
  pac1934: { col: "#ea580c", name: "PAC934", sub: function (c) { return String(c.val) + "A"; } },
  bl0937: { col: "#ea580c", name: "BL0937", sub: function (c) { return String(c.val) + "A"; } },
  pzem017: { col: "#ea580c", name: "PZE017", sub: function (c) { return String(c.val) + "A"; } },
  ade7753: { col: "#ea580c", name: "ADE753", sub: function (c) { return String(c.val) + "A"; } },
  atm90e26: { col: "#ea580c", name: "ATME26", sub: function (c) { return String(c.val) + "A"; } },
  hmc5983: { col: "#7c3aed", name: "HMC983", sub: function (c) { return String(c.val) + "µT"; } },
  mmc5603: { col: "#7c3aed", name: "MMC603", sub: function (c) { return String(c.val) + "µT"; } },
  mmc5983ma: { col: "#7c3aed", name: "MMC3MA", sub: function (c) { return String(c.val) + "µT"; } },
  ak8963: { col: "#7c3aed", name: "AK8963", sub: function (c) { return String(c.val) + "µT"; } },
  ak09916: { col: "#7c3aed", name: "AK0916", sub: function (c) { return String(c.val) + "µT"; } },
  qmc6310: { col: "#7c3aed", name: "QMC310", sub: function (c) { return String(c.val) + "µT"; } },
  bmm150: { col: "#7c3aed", name: "BMM150", sub: function (c) { return String(c.val) + "µT"; } },
  tmag5273: { col: "#7c3aed", name: "TMA273", sub: function (c) { return String(c.val) + "µT"; } },
  tlv493d: { col: "#7c3aed", name: "TLV93D", sub: function (c) { return String(c.val) + "µT"; } },
  a1324: { col: "#7c3aed", name: "A1324", sub: function (c) { return String(c.val) + "µT"; } },
  ss495a: { col: "#7c3aed", name: "SS495A", sub: function (c) { return String(c.val) + "µT"; } },
  drv5055: { col: "#7c3aed", name: "DRV055", sub: function (c) { return String(c.val) + "µT"; } },
  as5047p: { col: "#7c3aed", name: "AS547P", sub: function (c) { return String(c.val) + "µT"; } },
  ma730: { col: "#7c3aed", name: "MA730", sub: function (c) { return String(c.val) + "µT"; } },
  mt6701: { col: "#7c3aed", name: "MT6701", sub: function (c) { return String(c.val) + "µT"; } },
  max9814: { col: "#0d9488", name: "MAX814", sub: function (c) { return String(c.val) + "dB"; } },
  max4466: { col: "#0d9488", name: "MAX466", sub: function (c) { return String(c.val) + "dB"; } },
  ics43434: { col: "#0d9488", name: "ICS434", sub: function (c) { return String(c.val) + "dB"; } },
  inmp441: { col: "#0d9488", name: "INM441", sub: function (c) { return String(c.val) + "dB"; } },
  sph0645: { col: "#0d9488", name: "SPH645", sub: function (c) { return String(c.val) + "dB"; } },
  spm0405: { col: "#0d9488", name: "SPM405", sub: function (c) { return String(c.val) + "dB"; } },
  mp34dt05: { col: "#0d9488", name: "MP3T05", sub: function (c) { return String(c.val) + "dB"; } },
  ky037: { col: "#0d9488", name: "KY037", sub: function (c) { return String(c.val) + "dB"; } },
  fsr402: { col: "#be185d", name: "FSR402", sub: function (c) { return String(c.val) + "N"; } },
  fsr406: { col: "#be185d", name: "FSR406", sub: function (c) { return String(c.val) + "N"; } },
  load_cell_5kg: { col: "#be185d", name: "LOA5KG", sub: function (c) { return String(c.val) + "N"; } },
  load_cell_20kg: { col: "#be185d", name: "LOA0KG", sub: function (c) { return String(c.val) + "N"; } },
  piezo_film: { col: "#be185d", name: "PIEILM", sub: function (c) { return String(c.val) + "N"; } },
  flex_4in: { col: "#be185d", name: "FLE4IN", sub: function (c) { return String(c.val) + "N"; } },
  yfs201: { col: "#0369a1", name: "YFS201", sub: function (c) { return String(c.val) + "L/min"; } },
  yfs401: { col: "#0369a1", name: "YFS401", sub: function (c) { return String(c.val) + "L/min"; } },
  yfs210: { col: "#0369a1", name: "YFS210", sub: function (c) { return String(c.val) + "L/min"; } },
  yfb08: { col: "#0369a1", name: "YFB08", sub: function (c) { return String(c.val) + "L/min"; } },
  fs300a: { col: "#0369a1", name: "FS300A", sub: function (c) { return String(c.val) + "L/min"; } },
  fs400a: { col: "#0369a1", name: "FS400A", sub: function (c) { return String(c.val) + "L/min"; } },
  float_switch: { col: "#0f766e", name: "FLOTCH", sub: function (c) { return String(c.val) + "%"; } },
  ultrasonic_level: { col: "#0f766e", name: "ULTVEL", sub: function (c) { return String(c.val) + "%"; } },
  capacitive_level: { col: "#0f766e", name: "CAPVEL", sub: function (c) { return String(c.val) + "%"; } },
  optical_level: { col: "#0f766e", name: "OPTVEL", sub: function (c) { return String(c.val) + "%"; } },
  soil_moisture_v2: { col: "#0f766e", name: "SOIEV2", sub: function (c) { return String(c.val) + "%"; } },
  st7567: { col: "#be123c", name: "ST7567", sub: function (c) { return String(c.val); } },
  st7789_135: { col: "#be123c", name: "ST7135", sub: function (c) { return String(c.val); } },
  st7735_80: { col: "#be123c", name: "ST7580", sub: function (c) { return String(c.val); } },
  ili9163: { col: "#be123c", name: "ILI163", sub: function (c) { return String(c.val); } },
  ili9327: { col: "#be123c", name: "ILI327", sub: function (c) { return String(c.val); } },
  ili9342: { col: "#be123c", name: "ILI342", sub: function (c) { return String(c.val); } },
  ili9806: { col: "#be123c", name: "ILI806", sub: function (c) { return String(c.val); } },
  hx8357: { col: "#be123c", name: "HX8357", sub: function (c) { return String(c.val); } },
  hx8347: { col: "#be123c", name: "HX8347", sub: function (c) { return String(c.val); } },
  ra8875: { col: "#be123c", name: "RA8875", sub: function (c) { return String(c.val); } },
  ssd1289: { col: "#be123c", name: "SSD289", sub: function (c) { return String(c.val); } },
  ssd2119: { col: "#be123c", name: "SSD119", sub: function (c) { return String(c.val); } },
  sed1520: { col: "#be123c", name: "SED520", sub: function (c) { return String(c.val); } },
  ks0108: { col: "#be123c", name: "KS0108", sub: function (c) { return String(c.val); } },
  pcd8544: { col: "#be123c", name: "PCD544", sub: function (c) { return String(c.val); } },
  uc1701: { col: "#be123c", name: "UC1701", sub: function (c) { return String(c.val); } },
  uc1609: { col: "#be123c", name: "UC1609", sub: function (c) { return String(c.val); } },
  t6963c: { col: "#be123c", name: "T6963C", sub: function (c) { return String(c.val); } },
  drv8701: { col: "#7c2d12", name: "DRV701", sub: function (c) { return String(c.val); } },
  drv8424: { col: "#7c2d12", name: "DRV424", sub: function (c) { return String(c.val); } },
  drv8428: { col: "#7c2d12", name: "DRV428", sub: function (c) { return String(c.val); } },
  tmc2100: { col: "#7c2d12", name: "TMC100", sub: function (c) { return String(c.val); } },
  tmc2226: { col: "#7c2d12", name: "TMC226", sub: function (c) { return String(c.val); } },
  tmc2225: { col: "#7c2d12", name: "TMC225", sub: function (c) { return String(c.val); } },
  tmc2240: { col: "#7c2d12", name: "TMC240", sub: function (c) { return String(c.val); } },
  tmc2660: { col: "#7c2d12", name: "TMC660", sub: function (c) { return String(c.val); } },
  a4982: { col: "#7c2d12", name: "A4982", sub: function (c) { return String(c.val); } },
  a4983: { col: "#7c2d12", name: "A4983", sub: function (c) { return String(c.val); } },
  l6219: { col: "#7c2d12", name: "L6219", sub: function (c) { return String(c.val); } },
  l297: { col: "#7c2d12", name: "L297", sub: function (c) { return String(c.val); } },
  l298p: { col: "#7c2d12", name: "L298P", sub: function (c) { return String(c.val); } },
  tb6560: { col: "#7c2d12", name: "TB6560", sub: function (c) { return String(c.val); } },
  tb6600: { col: "#7c2d12", name: "TB6600", sub: function (c) { return String(c.val); } },
  tb67s109: { col: "#7c2d12", name: "TB6109", sub: function (c) { return String(c.val); } },
  lm78m05: { col: "#7c3aed", name: "LM7M05", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2937: { col: "#7c3aed", name: "LM2937", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2931: { col: "#7c3aed", name: "LM2931", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm1086: { col: "#7c3aed", name: "LM1086", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm1085: { col: "#7c3aed", name: "LM1085", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lt1763: { col: "#7c3aed", name: "LT1763", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lt1963: { col: "#7c3aed", name: "LT1963", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lt3042: { col: "#7c3aed", name: "LT3042", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps7a20: { col: "#7c3aed", name: "TPSA20", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps73401: { col: "#7c3aed", name: "TPS401", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  adp150: { col: "#7c3aed", name: "ADP150", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  adp3338: { col: "#7c3aed", name: "ADP338", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mcp1802: { col: "#7c3aed", name: "MCP802", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mcp1826: { col: "#7c3aed", name: "MCP826", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ap7361: { col: "#7c3aed", name: "AP7361", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ap7333: { col: "#7c3aed", name: "AP7333", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  rt9013: { col: "#7c3aed", name: "RT9013", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ld39050: { col: "#7c3aed", name: "LD3050", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tlv70033: { col: "#7c3aed", name: "TLV033", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm22676: { col: "#7c3aed", name: "LM2676", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2672: { col: "#7c3aed", name: "LM2672", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2674: { col: "#7c3aed", name: "LM2674", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm5008: { col: "#7c3aed", name: "LM5008", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm5164: { col: "#7c3aed", name: "LM5164", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ltc3630: { col: "#7c3aed", name: "LTC630", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ltc3115: { col: "#7c3aed", name: "LTC115", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps54360: { col: "#7c3aed", name: "TPS360", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps62130: { col: "#7c3aed", name: "TPS130", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps62160: { col: "#7c3aed", name: "TPS160", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps62933: { col: "#7c3aed", name: "TPS933", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mp1470: { col: "#7c3aed", name: "MP1470", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mp2359: { col: "#7c3aed", name: "MP2359", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mp2491: { col: "#7c3aed", name: "MP2491", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xl1509: { col: "#7c3aed", name: "XL1509", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xl2596: { col: "#7c3aed", name: "XL2596", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mc34063: { col: "#7c3aed", name: "MC3063", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps63020: { col: "#7c3aed", name: "TPS020", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps61088: { col: "#7c3aed", name: "TPS088", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps61230: { col: "#7c3aed", name: "TPS230", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mp3429: { col: "#7c3aed", name: "MP3429", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xl6019: { col: "#7c3aed", name: "XL6019", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  xl6012: { col: "#7c3aed", name: "XL6012", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ap3012: { col: "#7c3aed", name: "AP3012", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm2621: { col: "#7c3aed", name: "LM2621", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  lm3478: { col: "#7c3aed", name: "LM3478", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps55340: { col: "#7c3aed", name: "TPS340", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tps61200: { col: "#7c3aed", name: "TPS200", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tp4057: { col: "#7c3aed", name: "TP4057", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  tp4054: { col: "#7c3aed", name: "TP4054", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mcp73831: { col: "#7c3aed", name: "MCP831", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  mcp73832: { col: "#7c3aed", name: "MCP832", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  bq24072: { col: "#7c3aed", name: "BQ2072", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  bq24075: { col: "#7c3aed", name: "BQ2075", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  bq25606: { col: "#7c3aed", name: "BQ2606", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  bq25895: { col: "#7c3aed", name: "BQ2895", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ltc4054: { col: "#7c3aed", name: "LTC054", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ltc4065: { col: "#7c3aed", name: "LTC065", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  cn3722: { col: "#7c3aed", name: "CN3722", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  cn3765: { col: "#7c3aed", name: "CN3765", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ip2312: { col: "#7c3aed", name: "IP2312", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  ip5310: { col: "#7c3aed", name: "IP5310", sub: function (c) { return Number(c.val).toFixed(1) + "V"; } },
  esp32_wroom: { col: "#1e3a8a", name: "ESPOOM", sub: function (c) { return String(c.val); } },
  esp32_s2: { col: "#1e3a8a", name: "ESP2S2", sub: function (c) { return String(c.val); } },
  esp32_c6: { col: "#1e3a8a", name: "ESP2C6", sub: function (c) { return String(c.val); } },
  esp12f: { col: "#1e3a8a", name: "ESP12F", sub: function (c) { return String(c.val); } },
  esp12e: { col: "#1e3a8a", name: "ESP12E", sub: function (c) { return String(c.val); } },
  esp07: { col: "#1e3a8a", name: "ESP07", sub: function (c) { return String(c.val); } },
  bl602: { col: "#1e3a8a", name: "BL602", sub: function (c) { return String(c.val); } },
  rtl8710: { col: "#1e3a8a", name: "RTL710", sub: function (c) { return String(c.val); } },
  rtl8720dn: { col: "#1e3a8a", name: "RTL0DN", sub: function (c) { return String(c.val); } },
  nrf51822: { col: "#1e3a8a", name: "NRF822", sub: function (c) { return String(c.val); } },
  nrf52810: { col: "#1e3a8a", name: "NRF810", sub: function (c) { return String(c.val); } },
  nrf5340: { col: "#1e3a8a", name: "NRF340", sub: function (c) { return String(c.val); } },
  nrf9160: { col: "#1e3a8a", name: "NRF160", sub: function (c) { return String(c.val); } },
  cc2530: { col: "#1e3a8a", name: "CC2530", sub: function (c) { return String(c.val); } },
  cc2531: { col: "#1e3a8a", name: "CC2531", sub: function (c) { return String(c.val); } },
  cc2640: { col: "#1e3a8a", name: "CC2640", sub: function (c) { return String(c.val); } },
  cc2652: { col: "#1e3a8a", name: "CC2652", sub: function (c) { return String(c.val); } },
  cc3200: { col: "#1e3a8a", name: "CC3200", sub: function (c) { return String(c.val); } },
  cc1310: { col: "#1e3a8a", name: "CC1310", sub: function (c) { return String(c.val); } },
  cc1125: { col: "#1e3a8a", name: "CC1125", sub: function (c) { return String(c.val); } },
  cc2500: { col: "#1e3a8a", name: "CC2500", sub: function (c) { return String(c.val); } },
  si4432: { col: "#1e3a8a", name: "SI4432", sub: function (c) { return String(c.val); } },
  si4463: { col: "#1e3a8a", name: "SI4463", sub: function (c) { return String(c.val); } },
  si4455: { col: "#1e3a8a", name: "SI4455", sub: function (c) { return String(c.val); } },
  sx1280: { col: "#1e3a8a", name: "SX1280", sub: function (c) { return String(c.val); } },
  sx1272: { col: "#1e3a8a", name: "SX1272", sub: function (c) { return String(c.val); } },
  sx1301: { col: "#1e3a8a", name: "SX1301", sub: function (c) { return String(c.val); } },
  rfm12b: { col: "#1e3a8a", name: "RFM12B", sub: function (c) { return String(c.val); } },
  rfm22b: { col: "#1e3a8a", name: "RFM22B", sub: function (c) { return String(c.val); } },
  rfm98: { col: "#1e3a8a", name: "RFM98", sub: function (c) { return String(c.val); } },
  rfm96: { col: "#1e3a8a", name: "RFM96", sub: function (c) { return String(c.val); } },
  rfm63: { col: "#1e3a8a", name: "RFM63", sub: function (c) { return String(c.val); } },
  xbee_pro: { col: "#1e3a8a", name: "XBEPRO", sub: function (c) { return String(c.val); } },
  xbee3: { col: "#1e3a8a", name: "XBEE3", sub: function (c) { return String(c.val); } },
  bl654: { col: "#1e3a8a", name: "BL654", sub: function (c) { return String(c.val); } },
  ch341: { col: "#1e3a8a", name: "CH341", sub: function (c) { return String(c.val); } },
  ch9102: { col: "#1e3a8a", name: "CH9102", sub: function (c) { return String(c.val); } },
  ch343: { col: "#1e3a8a", name: "CH343", sub: function (c) { return String(c.val); } },
  cp2102n: { col: "#1e3a8a", name: "CP202N", sub: function (c) { return String(c.val); } },
  ft231x: { col: "#1e3a8a", name: "FT231X", sub: function (c) { return String(c.val); } },
  ft2232: { col: "#1e3a8a", name: "FT2232", sub: function (c) { return String(c.val); } },
  ft232h: { col: "#1e3a8a", name: "FT232H", sub: function (c) { return String(c.val); } },
  mcp2221: { col: "#1e3a8a", name: "MCP221", sub: function (c) { return String(c.val); } },
  max3485: { col: "#1e3a8a", name: "MAX485", sub: function (c) { return String(c.val); } },
  sp3485: { col: "#1e3a8a", name: "SP3485", sub: function (c) { return String(c.val); } },
  sn65hvd72: { col: "#1e3a8a", name: "SN6D72", sub: function (c) { return String(c.val); } },
  ltc2850: { col: "#1e3a8a", name: "LTC850", sub: function (c) { return String(c.val); } },
  iso1176: { col: "#1e3a8a", name: "ISO176", sub: function (c) { return String(c.val); } },
  adm2587: { col: "#1e3a8a", name: "ADM587", sub: function (c) { return String(c.val); } },
  adm3053: { col: "#1e3a8a", name: "ADM053", sub: function (c) { return String(c.val); } },
  mcp2562: { col: "#1e3a8a", name: "MCP562", sub: function (c) { return String(c.val); } },
  tcan1042: { col: "#1e3a8a", name: "TCA042", sub: function (c) { return String(c.val); } },
  tja1051: { col: "#1e3a8a", name: "TJA051", sub: function (c) { return String(c.val); } },
  sn65hvd1050: { col: "#1e3a8a", name: "SN6050", sub: function (c) { return String(c.val); } },
  l80: { col: "#1e3a8a", name: "L80", sub: function (c) { return String(c.val); } },
  l86: { col: "#1e3a8a", name: "L86", sub: function (c) { return String(c.val); } },
  atgm336h: { col: "#1e3a8a", name: "ATG36H", sub: function (c) { return String(c.val); } },
  gt_u7: { col: "#1e3a8a", name: "GTU7", sub: function (c) { return String(c.val); } },
  neo_m9n: { col: "#1e3a8a", name: "NEOM9N", sub: function (c) { return String(c.val); } },
  zoe_m8q: { col: "#1e3a8a", name: "ZOEM8Q", sub: function (c) { return String(c.val); } },
  max_m10s: { col: "#1e3a8a", name: "MAX10S", sub: function (c) { return String(c.val); } },
  teseo_liv3: { col: "#1e3a8a", name: "TESIV3", sub: function (c) { return String(c.val); } },
  mtk3339: { col: "#1e3a8a", name: "MTK339", sub: function (c) { return String(c.val); } },
  pa1010d: { col: "#1e3a8a", name: "PA110D", sub: function (c) { return String(c.val); } },
  sim28: { col: "#1e3a8a", name: "SIM28", sub: function (c) { return String(c.val); } },
  l96: { col: "#1e3a8a", name: "L96", sub: function (c) { return String(c.val); } },
  sim800c: { col: "#1e3a8a", name: "SIM00C", sub: function (c) { return String(c.val); } },
  sim808: { col: "#1e3a8a", name: "SIM808", sub: function (c) { return String(c.val); } },
  sim5320: { col: "#1e3a8a", name: "SIM320", sub: function (c) { return String(c.val); } },
  sim7000: { col: "#1e3a8a", name: "SIM000", sub: function (c) { return String(c.val); } },
  sim7070: { col: "#1e3a8a", name: "SIM070", sub: function (c) { return String(c.val); } },
  sim7080: { col: "#1e3a8a", name: "SIM080", sub: function (c) { return String(c.val); } },
  sim7500: { col: "#1e3a8a", name: "SIM500", sub: function (c) { return String(c.val); } },
  sim7670: { col: "#1e3a8a", name: "SIM670", sub: function (c) { return String(c.val); } },
  ec200s: { col: "#1e3a8a", name: "EC200S", sub: function (c) { return String(c.val); } },
  ec25: { col: "#1e3a8a", name: "EC25", sub: function (c) { return String(c.val); } },
  bg95: { col: "#1e3a8a", name: "BG95", sub: function (c) { return String(c.val); } },
  bg96: { col: "#1e3a8a", name: "BG96", sub: function (c) { return String(c.val); } },
  m26: { col: "#1e3a8a", name: "M26", sub: function (c) { return String(c.val); } },
  ec21: { col: "#1e3a8a", name: "EC21", sub: function (c) { return String(c.val); } },
  ec600: { col: "#1e3a8a", name: "EC600", sub: function (c) { return String(c.val); } },
  a9g: { col: "#1e3a8a", name: "A9G", sub: function (c) { return String(c.val); } },
  a6: { col: "#1e3a8a", name: "A6", sub: function (c) { return String(c.val); } },
  a7672e: { col: "#1e3a8a", name: "A7672E", sub: function (c) { return String(c.val); } },
  ic_74hc03: { col: "#4f46e5", name: "HC03", sub: function (c) { return String(c.val); } },
  ic_74hc05: { col: "#4f46e5", name: "HC05", sub: function (c) { return String(c.val); } },
  ic_74hc09: { col: "#4f46e5", name: "HC09", sub: function (c) { return String(c.val); } },
  ic_74hc21: { col: "#4f46e5", name: "HC21", sub: function (c) { return String(c.val); } },
  ic_74hc27: { col: "#4f46e5", name: "HC27", sub: function (c) { return String(c.val); } },
  ic_74hc51: { col: "#4f46e5", name: "HC51", sub: function (c) { return String(c.val); } },
  ic_74hc58: { col: "#4f46e5", name: "HC58", sub: function (c) { return String(c.val); } },
  ic_74hc85: { col: "#4f46e5", name: "HC85", sub: function (c) { return String(c.val); } },
  ic_74hc107: { col: "#4f46e5", name: "HC107", sub: function (c) { return String(c.val); } },
  ic_74hc109: { col: "#4f46e5", name: "HC109", sub: function (c) { return String(c.val); } },
  ic_74hc112: { col: "#4f46e5", name: "HC112", sub: function (c) { return String(c.val); } },
  ic_74hc123: { col: "#4f46e5", name: "HC123", sub: function (c) { return String(c.val); } },
  ic_74hc126: { col: "#4f46e5", name: "HC126", sub: function (c) { return String(c.val); } },
  ic_74hc132: { col: "#4f46e5", name: "HC132", sub: function (c) { return String(c.val); } },
  ic_74hc137: { col: "#4f46e5", name: "HC137", sub: function (c) { return String(c.val); } },
  ic_74hc147: { col: "#4f46e5", name: "HC147", sub: function (c) { return String(c.val); } },
  ic_74hc148: { col: "#4f46e5", name: "HC148", sub: function (c) { return String(c.val); } },
  ic_74hc153: { col: "#4f46e5", name: "HC153", sub: function (c) { return String(c.val); } },
  ic_74hc158: { col: "#4f46e5", name: "HC158", sub: function (c) { return String(c.val); } },
  ic_74hc160: { col: "#4f46e5", name: "HC160", sub: function (c) { return String(c.val); } },
  ic_74hc162: { col: "#4f46e5", name: "HC162", sub: function (c) { return String(c.val); } },
  ic_74hc163: { col: "#4f46e5", name: "HC163", sub: function (c) { return String(c.val); } },
  ic_74hc168: { col: "#4f46e5", name: "HC168", sub: function (c) { return String(c.val); } },
  ic_74hc169: { col: "#4f46e5", name: "HC169", sub: function (c) { return String(c.val); } },
  ic_74hc173: { col: "#4f46e5", name: "HC173", sub: function (c) { return String(c.val); } },
  ic_74hc182: { col: "#4f46e5", name: "HC182", sub: function (c) { return String(c.val); } },
  ic_74hc190: { col: "#4f46e5", name: "HC190", sub: function (c) { return String(c.val); } },
  ic_74hc191: { col: "#4f46e5", name: "HC191", sub: function (c) { return String(c.val); } },
  ic_74hc192: { col: "#4f46e5", name: "HC192", sub: function (c) { return String(c.val); } },
  ic_74hc194: { col: "#4f46e5", name: "HC194", sub: function (c) { return String(c.val); } },
  ic_74hc195: { col: "#4f46e5", name: "HC195", sub: function (c) { return String(c.val); } },
  ic_74hc238: { col: "#4f46e5", name: "HC238", sub: function (c) { return String(c.val); } },
  ic_74hc239: { col: "#4f46e5", name: "HC239", sub: function (c) { return String(c.val); } },
  ic_74hc240: { col: "#4f46e5", name: "HC240", sub: function (c) { return String(c.val); } },
  ic_74hc241: { col: "#4f46e5", name: "HC241", sub: function (c) { return String(c.val); } },
  ic_74hc251: { col: "#4f46e5", name: "HC251", sub: function (c) { return String(c.val); } },
  ic_74hc253: { col: "#4f46e5", name: "HC253", sub: function (c) { return String(c.val); } },
  ic_74hc257: { col: "#4f46e5", name: "HC257", sub: function (c) { return String(c.val); } },
  ic_74hc258: { col: "#4f46e5", name: "HC258", sub: function (c) { return String(c.val); } },
  ic_74hc259: { col: "#4f46e5", name: "HC259", sub: function (c) { return String(c.val); } },
  cd4000: { col: "#4f46e5", name: "CD4000", sub: function (c) { return String(c.val); } },
  cd4002: { col: "#4f46e5", name: "CD4002", sub: function (c) { return String(c.val); } },
  cd4006: { col: "#4f46e5", name: "CD4006", sub: function (c) { return String(c.val); } },
  cd4007: { col: "#4f46e5", name: "CD4007", sub: function (c) { return String(c.val); } },
  cd4008: { col: "#4f46e5", name: "CD4008", sub: function (c) { return String(c.val); } },
  cd4009: { col: "#4f46e5", name: "CD4009", sub: function (c) { return String(c.val); } },
  cd4010: { col: "#4f46e5", name: "CD4010", sub: function (c) { return String(c.val); } },
  cd4011: { col: "#4f46e5", name: "CD4011", sub: function (c) { return String(c.val); } },
  cd4012: { col: "#4f46e5", name: "CD4012", sub: function (c) { return String(c.val); } },
  cd4014: { col: "#4f46e5", name: "CD4014", sub: function (c) { return String(c.val); } },
  cd4016: { col: "#4f46e5", name: "CD4016", sub: function (c) { return String(c.val); } },
  cd4018: { col: "#4f46e5", name: "CD4018", sub: function (c) { return String(c.val); } },
  cd4019: { col: "#4f46e5", name: "CD4019", sub: function (c) { return String(c.val); } },
  cd4020: { col: "#4f46e5", name: "CD4020", sub: function (c) { return String(c.val); } },
  cd4021: { col: "#4f46e5", name: "CD4021", sub: function (c) { return String(c.val); } },
  cd4024: { col: "#4f46e5", name: "CD4024", sub: function (c) { return String(c.val); } },
  cd4026: { col: "#4f46e5", name: "CD4026", sub: function (c) { return String(c.val); } },
  cd4033: { col: "#4f46e5", name: "CD4033", sub: function (c) { return String(c.val); } },
  cd4034: { col: "#4f46e5", name: "CD4034", sub: function (c) { return String(c.val); } },
  cd4035: { col: "#4f46e5", name: "CD4035", sub: function (c) { return String(c.val); } },
  cd4040: { col: "#4f46e5", name: "CD4040", sub: function (c) { return String(c.val); } },
  cd4042: { col: "#4f46e5", name: "CD4042", sub: function (c) { return String(c.val); } },
  cd4043: { col: "#4f46e5", name: "CD4043", sub: function (c) { return String(c.val); } },
  cd4044: { col: "#4f46e5", name: "CD4044", sub: function (c) { return String(c.val); } },
  cd4049: { col: "#4f46e5", name: "CD4049", sub: function (c) { return String(c.val); } },
  cd4050: { col: "#4f46e5", name: "CD4050", sub: function (c) { return String(c.val); } },
  cd4052: { col: "#4f46e5", name: "CD4052", sub: function (c) { return String(c.val); } },
  cd4053: { col: "#4f46e5", name: "CD4053", sub: function (c) { return String(c.val); } },
  cd4069: { col: "#4f46e5", name: "CD4069", sub: function (c) { return String(c.val); } },
  cd4072: { col: "#4f46e5", name: "CD4072", sub: function (c) { return String(c.val); } },
  cd4073: { col: "#4f46e5", name: "CD4073", sub: function (c) { return String(c.val); } },
  cd4078: { col: "#4f46e5", name: "CD4078", sub: function (c) { return String(c.val); } },
  cd4082: { col: "#4f46e5", name: "CD4082", sub: function (c) { return String(c.val); } },
  cd4094: { col: "#4f46e5", name: "CD4094", sub: function (c) { return String(c.val); } },
  cd4099: { col: "#4f46e5", name: "CD4099", sub: function (c) { return String(c.val); } },
  cd40106: { col: "#4f46e5", name: "CD4106", sub: function (c) { return String(c.val); } },
  cd40193: { col: "#4f46e5", name: "CD4193", sub: function (c) { return String(c.val); } },
  cd4585: { col: "#4f46e5", name: "CD4585", sub: function (c) { return String(c.val); } },
  tlc555: { col: "#4f46e5", name: "TLC555", sub: function (c) { return String(c.val); } },
  icm7555: { col: "#4f46e5", name: "ICM555", sub: function (c) { return String(c.val); } },
  lmc555: { col: "#4f46e5", name: "LMC555", sub: function (c) { return String(c.val); } },
  xr2206: { col: "#4f46e5", name: "XR2206", sub: function (c) { return String(c.val); } },
  icl8038: { col: "#4f46e5", name: "ICL038", sub: function (c) { return String(c.val); } },
  max038: { col: "#4f46e5", name: "MAX038", sub: function (c) { return String(c.val); } },
  lm566: { col: "#4f46e5", name: "LM566", sub: function (c) { return String(c.val); } },
  lm567: { col: "#4f46e5", name: "LM567", sub: function (c) { return String(c.val); } },
  ne565: { col: "#4f46e5", name: "NE565", sub: function (c) { return String(c.val); } },
  ne567: { col: "#4f46e5", name: "NE567", sub: function (c) { return String(c.val); } },
  at24c01: { col: "#4f46e5", name: "AT2C01", sub: function (c) { return String(c.val); } },
  at24c04: { col: "#4f46e5", name: "AT2C04", sub: function (c) { return String(c.val); } },
  at24cm01: { col: "#4f46e5", name: "AT2M01", sub: function (c) { return String(c.val); } },
  at24cm02: { col: "#4f46e5", name: "AT2M02", sub: function (c) { return String(c.val); } },
  m24c64: { col: "#4f46e5", name: "M24C64", sub: function (c) { return String(c.val); } },
  m24256: { col: "#4f46e5", name: "M24256", sub: function (c) { return String(c.val); } },
  w25q16: { col: "#4f46e5", name: "W25Q16", sub: function (c) { return String(c.val); } },
  w25q32: { col: "#4f46e5", name: "W25Q32", sub: function (c) { return String(c.val); } },
  w25q80: { col: "#4f46e5", name: "W25Q80", sub: function (c) { return String(c.val); } },
  w25q256: { col: "#4f46e5", name: "W25256", sub: function (c) { return String(c.val); } },
  w25q512: { col: "#4f46e5", name: "W25512", sub: function (c) { return String(c.val); } },
  mx25l1606: { col: "#4f46e5", name: "MX2606", sub: function (c) { return String(c.val); } },
  mx25l3206: { col: "#4f46e5", name: "MX2206", sub: function (c) { return String(c.val); } },
  mx25l6406: { col: "#4f46e5", name: "MX2406", sub: function (c) { return String(c.val); } },
  mx25l12805: { col: "#4f46e5", name: "MX2805", sub: function (c) { return String(c.val); } },
  sst25vf016: { col: "#4f46e5", name: "SST016", sub: function (c) { return String(c.val); } },
  s25fl064: { col: "#4f46e5", name: "S25064", sub: function (c) { return String(c.val); } },
  is25lp128: { col: "#4f46e5", name: "IS2128", sub: function (c) { return String(c.val); } },
  gd25q32: { col: "#4f46e5", name: "GD2Q32", sub: function (c) { return String(c.val); } },
  gd25q64: { col: "#4f46e5", name: "GD2Q64", sub: function (c) { return String(c.val); } },
  fm24cl64: { col: "#4f46e5", name: "FM2L64", sub: function (c) { return String(c.val); } },
  fm24v10: { col: "#4f46e5", name: "FM2V10", sub: function (c) { return String(c.val); } },
  fm25cl64: { col: "#4f46e5", name: "FM2L62", sub: function (c) { return String(c.val); } },
  mb85rs64: { col: "#4f46e5", name: "MB8S64", sub: function (c) { return String(c.val); } },
  mb85rs256: { col: "#4f46e5", name: "MB8256", sub: function (c) { return String(c.val); } },
  mcp23k256: { col: "#4f46e5", name: "MCP256", sub: function (c) { return String(c.val); } },
  sram_23lc1024: { col: "#4f46e5", name: "SRA024", sub: function (c) { return String(c.val); } },
  sram_23lc512: { col: "#4f46e5", name: "SRA512", sub: function (c) { return String(c.val); } },
  sram_23k256: { col: "#4f46e5", name: "SRA256", sub: function (c) { return String(c.val); } },
  c93c46: { col: "#4f46e5", name: "C93C46", sub: function (c) { return String(c.val); } },
  c93c56: { col: "#4f46e5", name: "C93C56", sub: function (c) { return String(c.val); } },
  c93c66: { col: "#4f46e5", name: "C93C66", sub: function (c) { return String(c.val); } },
  c93c86: { col: "#4f46e5", name: "C93C86", sub: function (c) { return String(c.val); } },
  at25010: { col: "#4f46e5", name: "AT2010", sub: function (c) { return String(c.val); } },
  at25640: { col: "#4f46e5", name: "AT2640", sub: function (c) { return String(c.val); } },
  at25m01: { col: "#4f46e5", name: "AT2M03", sub: function (c) { return String(c.val); } },
  sdram_is42s16160: { col: "#4f46e5", name: "SDR160", sub: function (c) { return String(c.val); } },
  sdram_w9825g6: { col: "#4f46e5", name: "SDR5G6", sub: function (c) { return String(c.val); } },
  psram_aps6404: { col: "#4f46e5", name: "PSR404", sub: function (c) { return String(c.val); } },
  psram_ips6404: { col: "#4f46e5", name: "PSR402", sub: function (c) { return String(c.val); } },
  nand_w25n01: { col: "#4f46e5", name: "NANN01", sub: function (c) { return String(c.val); } },
  nand_mt29f: { col: "#4f46e5", name: "NAN29F", sub: function (c) { return String(c.val); } },
  emmc_4gb: { col: "#4f46e5", name: "EMM4GB", sub: function (c) { return String(c.val); } },
  lm1876: { col: "#7c3aed", name: "LM1876", sub: function (c) { return c.val + "W"; } },
  lm2877: { col: "#7c3aed", name: "LM2877", sub: function (c) { return c.val + "W"; } },
  lm3875: { col: "#7c3aed", name: "LM3875", sub: function (c) { return c.val + "W"; } },
  lm4780: { col: "#7c3aed", name: "LM4780", sub: function (c) { return c.val + "W"; } },
  tda1514: { col: "#7c3aed", name: "TDA514", sub: function (c) { return c.val + "W"; } },
  tda1521: { col: "#7c3aed", name: "TDA521", sub: function (c) { return c.val + "W"; } },
  tda2005: { col: "#7c3aed", name: "TDA005", sub: function (c) { return c.val + "W"; } },
  tda2006: { col: "#7c3aed", name: "TDA006", sub: function (c) { return c.val + "W"; } },
  tda2009: { col: "#7c3aed", name: "TDA009", sub: function (c) { return c.val + "W"; } },
  tda7240: { col: "#7c3aed", name: "TDA240", sub: function (c) { return c.val + "W"; } },
  tda7266: { col: "#7c3aed", name: "TDA266", sub: function (c) { return c.val + "W"; } },
  tda7293: { col: "#7c3aed", name: "TDA293", sub: function (c) { return c.val + "W"; } },
  tda7296: { col: "#7c3aed", name: "TDA296", sub: function (c) { return c.val + "W"; } },
  tda7379: { col: "#7c3aed", name: "TDA379", sub: function (c) { return c.val + "W"; } },
  tda7384: { col: "#7c3aed", name: "TDA384", sub: function (c) { return c.val + "W"; } },
  tda7388: { col: "#7c3aed", name: "TDA388", sub: function (c) { return c.val + "W"; } },
  tda7391: { col: "#7c3aed", name: "TDA391", sub: function (c) { return c.val + "W"; } },
  tpa3118: { col: "#7c3aed", name: "TPA118", sub: function (c) { return c.val + "W"; } },
  tpa3123: { col: "#7c3aed", name: "TPA123", sub: function (c) { return c.val + "W"; } },
  tpa3128: { col: "#7c3aed", name: "TPA128", sub: function (c) { return c.val + "W"; } },
  tpa3130: { col: "#7c3aed", name: "TPA130", sub: function (c) { return c.val + "W"; } },
  tpa3140: { col: "#7c3aed", name: "TPA140", sub: function (c) { return c.val + "W"; } },
  tpa3220: { col: "#7c3aed", name: "TPA220", sub: function (c) { return c.val + "W"; } },
  max9768: { col: "#7c3aed", name: "MAX768", sub: function (c) { return c.val + "W"; } },
  max9788: { col: "#7c3aed", name: "MAX788", sub: function (c) { return c.val + "W"; } },
  max98400: { col: "#7c3aed", name: "MAX400", sub: function (c) { return c.val + "W"; } },
  ssm3582: { col: "#7c3aed", name: "SSM582", sub: function (c) { return c.val + "W"; } },
  stk4141: { col: "#7c3aed", name: "STK141", sub: function (c) { return c.val + "W"; } },
  pam8620: { col: "#7c3aed", name: "PAM620", sub: function (c) { return c.val + "W"; } },
  lm4950: { col: "#7c3aed", name: "LM4950", sub: function (c) { return c.val + "W"; } },
  lm4991: { col: "#7c3aed", name: "LM4991", sub: function (c) { return c.val + "W"; } },
  tpa6120: { col: "#7c3aed", name: "TPA120", sub: function (c) { return c.val + "W"; } },
  tpa6132: { col: "#7c3aed", name: "TPA132", sub: function (c) { return c.val + "W"; } },
  tpa6211: { col: "#7c3aed", name: "TPA211", sub: function (c) { return c.val + "W"; } },
  tpa2012: { col: "#7c3aed", name: "TPA012", sub: function (c) { return c.val + "W"; } },
  tpa2031: { col: "#7c3aed", name: "TPA031", sub: function (c) { return c.val + "W"; } },
  pam8406: { col: "#7c3aed", name: "PAM406", sub: function (c) { return c.val + "W"; } },
  pam8304: { col: "#7c3aed", name: "PAM304", sub: function (c) { return c.val + "W"; } },
  ssm2302: { col: "#7c3aed", name: "SSM302", sub: function (c) { return c.val + "W"; } },
  lm833: { col: "#7c3aed", name: "LM833", sub: function (c) { return c.val + "x"; } },
  lm4562: { col: "#7c3aed", name: "LM4562", sub: function (c) { return c.val + "x"; } },
  lm4558: { col: "#7c3aed", name: "LM4558", sub: function (c) { return c.val + "x"; } },
  lm1458: { col: "#7c3aed", name: "LM1458", sub: function (c) { return c.val + "x"; } },
  opa134: { col: "#7c3aed", name: "OPA134", sub: function (c) { return c.val + "x"; } },
  opa227: { col: "#7c3aed", name: "OPA227", sub: function (c) { return c.val + "x"; } },
  opa277: { col: "#7c3aed", name: "OPA277", sub: function (c) { return c.val + "x"; } },
  opa337: { col: "#7c3aed", name: "OPA337", sub: function (c) { return c.val + "x"; } },
  opa343: { col: "#7c3aed", name: "OPA343", sub: function (c) { return c.val + "x"; } },
  opa350: { col: "#7c3aed", name: "OPA350", sub: function (c) { return c.val + "x"; } },
  opa551: { col: "#7c3aed", name: "OPA551", sub: function (c) { return c.val + "x"; } },
  opa564: { col: "#7c3aed", name: "OPA564", sub: function (c) { return c.val + "x"; } },
  opa1612: { col: "#7c3aed", name: "OPA612", sub: function (c) { return c.val + "x"; } },
  opa1656: { col: "#7c3aed", name: "OPA656", sub: function (c) { return c.val + "x"; } },
  opa1678: { col: "#7c3aed", name: "OPA678", sub: function (c) { return c.val + "x"; } },
  opa2604: { col: "#7c3aed", name: "OPA604", sub: function (c) { return c.val + "x"; } },
  opa2350: { col: "#7c3aed", name: "OPA352", sub: function (c) { return c.val + "x"; } },
  ad8066: { col: "#7c3aed", name: "AD8066", sub: function (c) { return c.val + "x"; } },
  ad8397: { col: "#7c3aed", name: "AD8397", sub: function (c) { return c.val + "x"; } },
  ad797: { col: "#7c3aed", name: "AD797", sub: function (c) { return c.val + "x"; } },
  ad8099: { col: "#7c3aed", name: "AD8099", sub: function (c) { return c.val + "x"; } },
  ad8221: { col: "#7c3aed", name: "AD8221", sub: function (c) { return c.val + "x"; } },
  ad8276: { col: "#7c3aed", name: "AD8276", sub: function (c) { return c.val + "x"; } },
  ad8429: { col: "#7c3aed", name: "AD8429", sub: function (c) { return c.val + "x"; } },
  ad8606: { col: "#7c3aed", name: "AD8606", sub: function (c) { return c.val + "x"; } },
  ad8628: { col: "#7c3aed", name: "AD8628", sub: function (c) { return c.val + "x"; } },
  lt1013: { col: "#7c3aed", name: "LT1013", sub: function (c) { return c.val + "x"; } },
  lt1028: { col: "#7c3aed", name: "LT1028", sub: function (c) { return c.val + "x"; } },
  lt1124: { col: "#7c3aed", name: "LT1124", sub: function (c) { return c.val + "x"; } },
  lt1677: { col: "#7c3aed", name: "LT1677", sub: function (c) { return c.val + "x"; } },
  lt6015: { col: "#7c3aed", name: "LT6015", sub: function (c) { return c.val + "x"; } },
  lmv358: { col: "#7c3aed", name: "LMV358", sub: function (c) { return c.val + "x"; } },
  lmv321: { col: "#7c3aed", name: "LMV321", sub: function (c) { return c.val + "x"; } },
  lmv324: { col: "#7c3aed", name: "LMV324", sub: function (c) { return c.val + "x"; } },
  lmc6482: { col: "#7c3aed", name: "LMC482", sub: function (c) { return c.val + "x"; } },
  lmc662: { col: "#7c3aed", name: "LMC662", sub: function (c) { return c.val + "x"; } },
  lmp7701: { col: "#7c3aed", name: "LMP701", sub: function (c) { return c.val + "x"; } },
  mcp6001: { col: "#7c3aed", name: "MCP001", sub: function (c) { return c.val + "x"; } },
  mcp6004: { col: "#7c3aed", name: "MCP004", sub: function (c) { return c.val + "x"; } },
  mcp6231: { col: "#7c3aed", name: "MCP231", sub: function (c) { return c.val + "x"; } },
  mcp6241: { col: "#7c3aed", name: "MCP241", sub: function (c) { return c.val + "x"; } },
  mcp6271: { col: "#7c3aed", name: "MCP271", sub: function (c) { return c.val + "x"; } },
  tlv2371: { col: "#7c3aed", name: "TLV371", sub: function (c) { return c.val + "x"; } },
  tlv2462: { col: "#7c3aed", name: "TLV462", sub: function (c) { return c.val + "x"; } },
  tlv271: { col: "#7c3aed", name: "TLV271", sub: function (c) { return c.val + "x"; } },
  tlv9061: { col: "#7c3aed", name: "TLV061", sub: function (c) { return c.val + "x"; } },
  tlv9062: { col: "#7c3aed", name: "TLV062", sub: function (c) { return c.val + "x"; } },
  ca3140: { col: "#7c3aed", name: "CA3140", sub: function (c) { return c.val + "x"; } },
  ca3130: { col: "#7c3aed", name: "CA3130", sub: function (c) { return c.val + "x"; } }
};
var MAX_COMPS = 150, MAX_WIRES = 300;

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
var scope = {
  visible: false, x: 10, y: 150, w: 260, h: 120, maxData: 100,
  probeA: { key: null, x: 0, y: 0, data: [], col: "#38bdf8" },
  probeB: { key: null, x: 0, y: 0, data: [], col: "#fbbf24" }
};
function probeByTarget(tg) {
  return tg === "meterA" ? meter.probeA : tg === "meterB" ? meter.probeB : tg === "scopeA" ? scope.probeA : scope.probeB;
}
function scopeState() {
  function pr(p) { return { x: p.x, y: p.y, key: p.key }; }
  return { visible: scope.visible, x: scope.x, y: scope.y, probeA: pr(scope.probeA), probeB: pr(scope.probeB) };
}
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
function isGate(c) { return c.type.indexOf("gate_") === 0; }
// أنواع قديمة لها طرف c دون pins: 3 في TYPES. أي عنصر جديد يكفيه pins: 3.
var THREE_PIN_LEGACY = { transistor: 1, transistor_pnp: 1, seven_seg: 1, timer555: 1, mosfet_n: 1, lm317: 1, servo: 1, lcd_16x2: 1, hc_sr04: 1, ds18b20: 1 };
function hasThreePins(c) { c = aliasView(c); return TYPES[c.type].pins === 3 || !!THREE_PIN_LEGACY[c.type]; }
function termList(c) {
  c = aliasView(c);
  if (c.type === "relay") return ["a", "b", "c", "out"];
  if (c.type === "gate_not") return ["a", "out"];
  if (isGate(c)) return ["a", "b", "out"];
  if (hasThreePins(c)) return ["a", "b", "c"];
  return ["a", "b"];
}
function localTerm(c, which) {
  c = aliasView(c);
  if (c.type === "relay") {
    if (which === "a") return { x: -HL, y: -15 };
    if (which === "b") return { x: -HL, y: 15 };
    if (which === "c") return { x: HL, y: -15 };
    return { x: HL, y: 15 };
  }
  if (isGate(c)) {
    if (which === "out") return { x: HL, y: 0 };
    if (c.type === "gate_not") return { x: -HL, y: 0 };
    return { x: -HL, y: which === "a" ? -15 : 15 };
  }
  if (c.type === "reg7805" || c.type === "reg7803") {
    if (which === "a") return { x: -HL, y: 0 };
    if (which === "b") return { x: 0, y: HL };
    return { x: HL, y: 0 };
  }
  if (c.type === "opamp") {
    if (which === "a") return { x: -HL, y: -10 };
    if (which === "b") return { x: -HL, y: 10 };
    return { x: HL, y: 0 };
  }
  if (c.type === "seven_seg") {
    if (which === "a") return { x: -HL, y: -15 };
    if (which === "b") return { x: -HL, y: 15 };
    return { x: 0, y: HL };
  }
  if (c.type === "timer555") {
    if (which === "a") return { x: -HL, y: -15 };
    if (which === "b") return { x: -HL, y: 15 };
    return { x: HL, y: 0 };
  }
  if (c.type === "mosfet_n") {
    if (which === "a") return { x: 0, y: HL };
    if (which === "b") return { x: 0, y: -HL };
    return { x: -HL, y: 0 };
  }
  if (c.type === "lm317") {
    if (which === "a") return { x: -HL, y: 0 };
    if (which === "b") return { x: 0, y: HL };
    return { x: HL, y: 0 };
  }
  // Generic 3-pin layout shared by every IC added from batch 5 onward:
  if (hasThreePins(c) && c.type !== "transistor" && c.type !== "transistor_pnp" && c.type !== "potentiometer") {
    if (which === "a") return { x: -HL, y: -12 };
    if (which === "b") return { x: -HL, y: 12 };
    return { x: HL, y: 0 };
  }
  if (which === "c") return { x: 0, y: HL };
  return { x: which === "a" ? -HL : HL, y: 0 };
}
function termPos(c, which) {
  var o = localTerm(c, which);
  if (c.rot) o = { x: -o.y, y: o.x }; // نفس دوران اللوحة (90°)
  return { x: c.x + o.x, y: c.y + o.y };
}
function keyPos(key) {
  var p = key.split("."), c = findComp(p[0]);
  return c ? termPos(c, p[1]) : null;
}

/* ===================================================================================================================
   المحاكي
   =================================================================================================================== */
/*SOLVER_START*/
var R_BATT = 0.1, R_SW_ON = 0.01, R_LED = 5, R_TRANSISTOR = 1.0, G_MIN = 1e-9, R_GATE = 10, R_RELAY_COIL = 200;
function potPos(c) { return (typeof c.pos === "number" && isFinite(c.pos)) ? Math.max(0, Math.min(1, c.pos)) : 0.5; }
function ldrRes(c) { return c.closed ? c.val * 100 : c.val; } // closed = مظلم
function isSource(c) { c = aliasView(c); return c.type === "battery" || c.type === "ac_source" || c.type === "arduino" || c.type === "esp32" || c.type === "nano" || c.type === "mega" || c.type === "esp8266" || c.type === "pico" || c.type === "solar" || c.type === "dc_jack"; }
function srcV(c, t) { return c.type === "ac_source" ? c.val * Math.sin(2 * Math.PI * 50 * t) : c.val; }
var SENSOR_SET = { mpu6050: 1, bmp280: 1, acs712: 1, a3144: 1, ky038: 1, yl69: 1, ttp223: 1, ky040: 1, tsop: 1, hc05: 1, l298n: 1, a4988: 1, pam8403: 1, max98357: 1, ads1115: 1, mcp4725: 1, ina219: 1, mq2: 1, bh1750: 1, vl53l0x: 1, ic_74hc165: 1, nrf24l01: 1, sim800l: 1, drv8825: 1, tb6612: 1, bts7960: 1, tcs34725: 1, mlx90614: 1, max30102: 1, adxl345: 1, hx711: 1, dht22: 1, sgp30: 1, rc522: 1, bme680: 1, pca9685: 1, tca9548a: 1, l9110s: 1, tmp36: 1, am2320: 1, ds1307: 1, pcf8563: 1, st7735: 1, ssd1351: 1, bmp180: 1, sht31: 1, apds9960: 1, ds1302: 1, max6675: 1, max31855: 1, sd_card: 1, enc28j60: 1, uln2803: 1, tlc5940: 1, mpu9250: 1, ad9833: 1, ams1117: 1, xl6009: 1, vl6180x: 1, sht10: 1, sht75: 1, si7021: 1, bme280: 1, mpl3115a2: 1, mq3: 1, mq4: 1, mq5: 1, mq6: 1, mq7: 1, mq8: 1, mq9: 1, mq135: 1, gp2y1010: 1, tsl2561: 1, tcs3200: 1, reed_switch: 1, vibration_sensor: 1, water_level: 1, flex_sensor: 1, tilt_switch: 1, shock_sensor: 1, flame_sensor: 1, rain_sensor: 1, hall_linear: 1, cd4071: 1, cd4081: 1, cd4030: 1, cd4001: 1, cd4023: 1, cd4025: 1, cd4070: 1, cd4075: 1, cd4077: 1, cd4093: 1, cd4538: 1, cd4047: 1, cd4027: 1, cd4029: 1, cd4076: 1, cd4022: 1, cd4060: 1, cd4541: 1, cd4511: 1, cd4028: 1, mcp3008: 1, mcp3208: 1, ads1015: 1, pcf8591: 1, tlc5615: 1, mcp4921: 1, at24c256: 1, at24c512: 1, w25q64: 1, mb85rc: 1, ds3234: 1, rv3028: 1, mcp7940: 1, nokia5110: 1, ssd1309: 1, st7565: 1, st7920: 1, ili9341: 1, ili9486: 1, max6954: 1, lcd_20x4: 1, st7735_160: 1, ssd1331: 1, drv8833: 1, drv8871: 1, l293e: 1, sn754410: 1, uln2004: 1, mc33926: 1, bd6221: 1, tb67h420: 1, a3959: 1, drv8824: 1, esp01: 1, rn2483: 1, rfm69: 1, rfm95: 1, hc12: 1, xbee: 1, sim900: 1, m95: 1, nrf905: 1, cc1101: 1, lm7809: 1, lm7812: 1, lm7905: 1, lm7912: 1, lm1084: 1, lm2678: 1, lm5007: 1, mcp1700: 1, mic5205: 1, lp2985: 1, lm4871: 1, tda2003: 1, ds18s20: 1, lm35: 1, lm75: 1, tmp102: 1, mcp9808: 1, max31865: 1, ads1118: 1, hdc1080: 1, htu21d: 1, sht21: 1, sht35: 1, aht10: 1, aht20: 1, ms5611: 1, lps25h: 1, bmp388: 1, dps310: 1, bmp085: 1, lps22hb: 1, mpx5700: 1, mq131: 1, mq303: 1, mhz19: 1, sds011: 1, pms5003: 1, ccs811: 1, ens160: 1, si1145: 1, veml7700: 1, opt3001: 1, max44009: 1, ltr329: 1, ml8511: 1, veml6070: 1, ina226: 1, ina260: 1, ina3221: 1, lis3dh: 1, mma8452: 1, adxl335: 1, adxl362: 1, lsm6ds3: 1, icm20948: 1, bno055: 1, hmc5883l: 1, qmc5883l: 1, mlx90393: 1, lm7815: 1, lm7824: 1, lm7808: 1, lm7806: 1, lm317hv: 1, lm2940: 1, tps7a47: 1, lm2576: 1, lm2574: 1, mp1584: 1, tps5430: 1, mt3608: 1, lm2577: 1, tps61023: 1, max1771: 1, lm3886: 1, tda7294: 1, tda2050: 1, tda7377: 1, tpa3116: 1, tpa2005: 1, lm4766: 1, drv8434: 1, tmc2209: 1, tmc2130: 1, l6470: 1, vnh5019: 1, drv8313: 1, a4950: 1, mx1508: 1, esp32cam: 1, sx1278: 1, sx1276: 1, nrf52832: 1, hm10: 1, jdy23: 1, ublox_neo6m: 1, ublox_neo7m: 1, w5500: 1, cp2102: 1, ch340: 1, max485: 1, mcp2515: 1, ssd1322: 1, ssd1327: 1, ssd1306_64: 1, st7789: 1, ili9488: 1, hd44780: 1, tm1637: 1, ht16k33: 1, cd4017b: 1, ic_74hc14: 1, ic_74hc04: 1, ic_74hc08: 1, ic_74hc32: 1, ic_74hc86: 1, ic_74hc74: 1, ic_74hc590: 1, ic_74hc4067: 1, at24c64: 1, at24c128: 1, w25q128: 1, fm25v02: 1, mcp23s17: 1, tca9534: 1, max7301: 1, tmp117: 1, max30205: 1, amg8833: 1, mlx90640: 1, lm73: 1, si7050: 1, ds28ea00: 1, ad8495: 1, hih6130: 1, dht21: 1, sht40: 1, sht45: 1, hdc2080: 1, bme688: 1, bmp390: 1, bmp581: 1, lps35hw: 1, lps33hw: 1, spl06: 1, ms5837: 1, mq137: 1, mq138: 1, mq214: 1, mq216: 1, scd30: 1, scd40: 1, scd41: 1, sgp40: 1, sen54: 1, ags02ma: 1, as7341: 1, as7262: 1, tsl2591: 1, veml6075: 1, guva_s12sd: 1, bh1745: 1, isl29125: 1, apds9306: 1, mpu6500: 1, lsm9ds1: 1, lsm303: 1, l3gd20h: 1, bmi160: 1, bmi270: 1, adxl375: 1, icm42688: 1, lis2dh12: 1, kxtj3: 1, vl53l1x: 1, gp2y0a21: 1, gp2y0a02: 1, us100: 1, a02yyuw: 1, ld2410: 1, rcwl0516: 1, tfmini: 1, tf_luna: 1, vcnl4040: 1, jsn_sr04t: 1, max30100: 1, ad8232: 1, pulse_sensor: 1, gsr_sensor: 1, r307: 1, ina169: 1, acs758: 1, max471: 1, pzem004t: 1, hlw8012: 1, ina228: 1, ina238: 1, ss49e: 1, a1302: 1, drv5053: 1, as5600: 1, as5048a: 1, sh1106: 1, ssd1305: 1, gc9a01: 1, st7796: 1, ili9225: 1, ssd1963: 1, epd_154: 1, epd_213: 1, epd_29: 1, lcd_12864: 1, lcd_16x4: 1, lcd_8x2: 1, tm1638: 1, ht1621: 1, drv8847: 1, drv8880: 1, tmc2208: 1, tmc2160: 1, tmc5160: 1, l6208: 1, l6235: 1, vnh2sp30: 1, ibt2: 1, lv8548: 1, lm7818: 1, lm78l05: 1, lm79l05: 1, lm317l: 1, lm350: 1, ld1117: 1, xc6206: 1, ap2112: 1, tlv1117: 1, lt3045: 1, lm2575: 1, lm2595: 1, xl4015: 1, xl4005: 1, xl7005: 1, mp2307: 1, mp2315: 1, tps54331: 1, sx1308: 1, cn3791: 1, bq24074: 1, tp5100: 1, ip5306: 1, esp32_c3: 1, esp32_s3: 1, nrf52840: 1, hc06: 1, hm11: 1, jdy31: 1, e32: 1, sx1262: 1, dw1000: 1, pn532: 1, w5100: 1, enc424j600: 1, mcp2551: 1, tja1050: 1, sn65hvd230: 1, max232: 1, max3232: 1, ft232: 1, pl2303: 1, cp2104: 1, l76k: 1, neo_m8n: 1, sim7600: 1, sim868: 1, a7670: 1, ic_74hc02: 1, ic_74hc10: 1, ic_74hc20: 1, ic_74hc30: 1, ic_74hc125: 1, ic_74hc157: 1, ic_74hc151: 1, ic_74hc139: 1, ic_74hc154: 1, ic_74hc161: 1, ic_74hc164: 1, ic_74hc166: 1, ic_74hc174: 1, ic_74hc175: 1, ic_74hc193: 1, ic_74hc244: 1, ic_74hc245: 1, ic_74hc283: 1, ic_74hc374: 1, ic_74hc4040: 1, ic_74hc4046: 1, ic_74hc4053: 1, ic_74hc4094: 1, mcp23008: 1, tca9535: 1, txs0108: 1, sn74lvc245: 1, at24c02: 1, at24c08: 1, at24c16: 1, lm1875: 1, tda2040: 1, tda7498: 1, tpa3110: 1, pam8610: 1, pam8302: 1, max9744: 1, mcp6002: 1, mcp6022: 1, tl082: 1, tl084: 1, lf353: 1, lf411: 1, op07: 1, op27: 1, ad8605: 1, tmp116: 1, tmp1075: 1, max6633: 1, mcp9701: 1, lm19: 1, lm34: 1, lm335: 1, ad590: 1, tmp35: 1, tmp37: 1, sts31: 1, stlm20: 1, sht85: 1, hih7130: 1, hts221: 1, hdc3020: 1, shtc3: 1, shtc1: 1, si7020: 1, am2301: 1, am2302: 1, capacitive_soil: 1, fc28: 1, lps22hh: 1, mpl115a2: 1, ms5803: 1, ms5607: 1, mprls: 1, bmp384: 1, icp10125: 1, icp20100: 1, mpx4115: 1, mpxv7002: 1, xgzp6847: 1, mq136: 1, mq139: 1, mq309: 1, tgs2600: 1, tgs2602: 1, tgs2620: 1, mics5524: 1, mics6814: 1, mh_z14a: 1, mh_z16: 1, s8_co2: 1, iaq_core: 1, zmod4410: 1, zh03b: 1, tsl2572: 1, veml3235: 1, opt4048: 1, opt3004: 1, ltr390: 1, ltr303: 1, ltr559: 1, as7343: 1, as7265x: 1, ap3216: 1, vcnl4200: 1, si1133: 1, mpu6886: 1, mpu9255: 1, lsm6dso: 1, lsm6dsox: 1, lis3mdl: 1, lis2mdl: 1, lis3dsh: 1, mma7660: 1, mma8451: 1, mma7361: 1, bma280: 1, bma423: 1, bmi088: 1, bmx160: 1, icm20689: 1, icm42605: 1, fxos8700: 1, fxas21002: 1, l3g4200d: 1, itg3200: 1, vl53l4cd: 1, vl53l3cx: 1, tof050c: 1, tf02: 1, tf03: 1, hcsr05: 1, srf05: 1, maxsonar_ez1: 1, us015: 1, us020: 1, urm37: 1, ld2450: 1, ld2420: 1, hb100: 1, sen0311: 1, max30101: 1, max86150: 1, afe4490: 1, ads1292: 1, ad8233: 1, max30003: 1, emg_sensor: 1, muscle_v3: 1, gsr_grove: 1, skin_temp_mlx: 1, ina180: 1, ina199: 1, ina210: 1, ina230: 1, ina233: 1, acs711: 1, acs723: 1, acs724: 1, acs781: 1, max9611: 1, ltc4151: 1, ltc2945: 1, pac1934: 1, bl0937: 1, pzem017: 1, ade7753: 1, atm90e26: 1, hmc5983: 1, mmc5603: 1, mmc5983ma: 1, ak8963: 1, ak09916: 1, qmc6310: 1, bmm150: 1, tmag5273: 1, tlv493d: 1, a1324: 1, ss495a: 1, drv5055: 1, as5047p: 1, ma730: 1, mt6701: 1, max9814: 1, max4466: 1, ics43434: 1, inmp441: 1, sph0645: 1, spm0405: 1, mp34dt05: 1, ky037: 1, fsr402: 1, fsr406: 1, load_cell_5kg: 1, load_cell_20kg: 1, piezo_film: 1, flex_4in: 1, yfs201: 1, yfs401: 1, yfs210: 1, yfb08: 1, fs300a: 1, fs400a: 1, float_switch: 1, ultrasonic_level: 1, capacitive_level: 1, optical_level: 1, soil_moisture_v2: 1, st7567: 1, st7789_135: 1, st7735_80: 1, ili9163: 1, ili9327: 1, ili9342: 1, ili9806: 1, hx8357: 1, hx8347: 1, ra8875: 1, ssd1289: 1, ssd2119: 1, sed1520: 1, ks0108: 1, pcd8544: 1, uc1701: 1, uc1609: 1, t6963c: 1, drv8701: 1, drv8424: 1, drv8428: 1, tmc2100: 1, tmc2226: 1, tmc2225: 1, tmc2240: 1, tmc2660: 1, a4982: 1, a4983: 1, l6219: 1, l297: 1, l298p: 1, tb6560: 1, tb6600: 1, tb67s109: 1, lm78m05: 1, lm2937: 1, lm2931: 1, lm1086: 1, lm1085: 1, lt1763: 1, lt1963: 1, lt3042: 1, tps7a20: 1, tps73401: 1, adp150: 1, adp3338: 1, mcp1802: 1, mcp1826: 1, ap7361: 1, ap7333: 1, rt9013: 1, ld39050: 1, tlv70033: 1, lm22676: 1, lm2672: 1, lm2674: 1, lm5008: 1, lm5164: 1, ltc3630: 1, ltc3115: 1, tps54360: 1, tps62130: 1, tps62160: 1, tps62933: 1, mp1470: 1, mp2359: 1, mp2491: 1, xl1509: 1, xl2596: 1, mc34063: 1, tps63020: 1, tps61088: 1, tps61230: 1, mp3429: 1, xl6019: 1, xl6012: 1, ap3012: 1, lm2621: 1, lm3478: 1, tps55340: 1, tps61200: 1, tp4057: 1, tp4054: 1, mcp73831: 1, mcp73832: 1, bq24072: 1, bq24075: 1, bq25606: 1, bq25895: 1, ltc4054: 1, ltc4065: 1, cn3722: 1, cn3765: 1, ip2312: 1, ip5310: 1, esp32_wroom: 1, esp32_s2: 1, esp32_c6: 1, esp12f: 1, esp12e: 1, esp07: 1, bl602: 1, rtl8710: 1, rtl8720dn: 1, nrf51822: 1, nrf52810: 1, nrf5340: 1, nrf9160: 1, cc2530: 1, cc2531: 1, cc2640: 1, cc2652: 1, cc3200: 1, cc1310: 1, cc1125: 1, cc2500: 1, si4432: 1, si4463: 1, si4455: 1, sx1280: 1, sx1272: 1, sx1301: 1, rfm12b: 1, rfm22b: 1, rfm98: 1, rfm96: 1, rfm63: 1, xbee_pro: 1, xbee3: 1, bl654: 1, ch341: 1, ch9102: 1, ch343: 1, cp2102n: 1, ft231x: 1, ft2232: 1, ft232h: 1, mcp2221: 1, max3485: 1, sp3485: 1, sn65hvd72: 1, ltc2850: 1, iso1176: 1, adm2587: 1, adm3053: 1, mcp2562: 1, tcan1042: 1, tja1051: 1, sn65hvd1050: 1, l80: 1, l86: 1, atgm336h: 1, gt_u7: 1, neo_m9n: 1, zoe_m8q: 1, max_m10s: 1, teseo_liv3: 1, mtk3339: 1, pa1010d: 1, sim28: 1, l96: 1, sim800c: 1, sim808: 1, sim5320: 1, sim7000: 1, sim7070: 1, sim7080: 1, sim7500: 1, sim7670: 1, ec200s: 1, ec25: 1, bg95: 1, bg96: 1, m26: 1, ec21: 1, ec600: 1, a9g: 1, a6: 1, a7672e: 1, ic_74hc03: 1, ic_74hc05: 1, ic_74hc09: 1, ic_74hc21: 1, ic_74hc27: 1, ic_74hc51: 1, ic_74hc58: 1, ic_74hc85: 1, ic_74hc107: 1, ic_74hc109: 1, ic_74hc112: 1, ic_74hc123: 1, ic_74hc126: 1, ic_74hc132: 1, ic_74hc137: 1, ic_74hc147: 1, ic_74hc148: 1, ic_74hc153: 1, ic_74hc158: 1, ic_74hc160: 1, ic_74hc162: 1, ic_74hc163: 1, ic_74hc168: 1, ic_74hc169: 1, ic_74hc173: 1, ic_74hc182: 1, ic_74hc190: 1, ic_74hc191: 1, ic_74hc192: 1, ic_74hc194: 1, ic_74hc195: 1, ic_74hc238: 1, ic_74hc239: 1, ic_74hc240: 1, ic_74hc241: 1, ic_74hc251: 1, ic_74hc253: 1, ic_74hc257: 1, ic_74hc258: 1, ic_74hc259: 1, cd4000: 1, cd4002: 1, cd4006: 1, cd4007: 1, cd4008: 1, cd4009: 1, cd4010: 1, cd4011: 1, cd4012: 1, cd4014: 1, cd4016: 1, cd4018: 1, cd4019: 1, cd4020: 1, cd4021: 1, cd4024: 1, cd4026: 1, cd4033: 1, cd4034: 1, cd4035: 1, cd4040: 1, cd4042: 1, cd4043: 1, cd4044: 1, cd4049: 1, cd4050: 1, cd4052: 1, cd4053: 1, cd4069: 1, cd4072: 1, cd4073: 1, cd4078: 1, cd4082: 1, cd4094: 1, cd4099: 1, cd40106: 1, cd40193: 1, cd4585: 1, tlc555: 1, icm7555: 1, lmc555: 1, xr2206: 1, icl8038: 1, max038: 1, lm566: 1, lm567: 1, ne565: 1, ne567: 1, at24c01: 1, at24c04: 1, at24cm01: 1, at24cm02: 1, m24c64: 1, m24256: 1, w25q16: 1, w25q32: 1, w25q80: 1, w25q256: 1, w25q512: 1, mx25l1606: 1, mx25l3206: 1, mx25l6406: 1, mx25l12805: 1, sst25vf016: 1, s25fl064: 1, is25lp128: 1, gd25q32: 1, gd25q64: 1, fm24cl64: 1, fm24v10: 1, fm25cl64: 1, mb85rs64: 1, mb85rs256: 1, mcp23k256: 1, sram_23lc1024: 1, sram_23lc512: 1, sram_23k256: 1, c93c46: 1, c93c56: 1, c93c66: 1, c93c86: 1, at25010: 1, at25640: 1, at25m01: 1, sdram_is42s16160: 1, sdram_w9825g6: 1, psram_aps6404: 1, psram_ips6404: 1, nand_w25n01: 1, nand_mt29f: 1, emmc_4gb: 1, lm1876: 1, lm2877: 1, lm3875: 1, lm4780: 1, tda1514: 1, tda1521: 1, tda2005: 1, tda2006: 1, tda2009: 1, tda7240: 1, tda7266: 1, tda7293: 1, tda7296: 1, tda7379: 1, tda7384: 1, tda7388: 1, tda7391: 1, tpa3118: 1, tpa3123: 1, tpa3128: 1, tpa3130: 1, tpa3140: 1, tpa3220: 1, max9768: 1, max9788: 1, max98400: 1, ssm3582: 1, stk4141: 1, pam8620: 1, lm4950: 1, lm4991: 1, tpa6120: 1, tpa6132: 1, tpa6211: 1, tpa2012: 1, tpa2031: 1, pam8406: 1, pam8304: 1, ssm2302: 1, lm833: 1, lm4562: 1, lm4558: 1, lm1458: 1, opa134: 1, opa227: 1, opa277: 1, opa337: 1, opa343: 1, opa350: 1, opa551: 1, opa564: 1, opa1612: 1, opa1656: 1, opa1678: 1, opa2604: 1, opa2350: 1, ad8066: 1, ad8397: 1, ad797: 1, ad8099: 1, ad8221: 1, ad8276: 1, ad8429: 1, ad8606: 1, ad8628: 1, lt1013: 1, lt1028: 1, lt1124: 1, lt1677: 1, lt6015: 1, lmv358: 1, lmv321: 1, lmv324: 1, lmc6482: 1, lmc662: 1, lmp7701: 1, mcp6001: 1, mcp6004: 1, mcp6231: 1, mcp6241: 1, mcp6271: 1, tlv2371: 1, tlv2462: 1, tlv271: 1, tlv9061: 1, tlv9062: 1, ca3140: 1, ca3130: 1 };
function sensorOut(c, vcc, vp, t) {
  if (vp < 1.5) return 0;
  if (c.type === "mpu6050") return c.val === "shake" ? vcc * (0.4 + 0.2 * Math.sin((t || 0) * 8)) : c.val === "tilt" ? vcc * 0.7 : c.val === "rotated" ? vcc * 0.3 : vcc * 0.5;
  if (c.type === "bmp280")  return vcc * Math.max(0, Math.min(1, (c.val - 500) / 513));
  if (c.type === "acs712")  return vcc * 0.5;
  if (c.type === "a3144")   return c.closed ? 0 : vcc;
  if (c.type === "ky038")   return c.val > 0 ? vcc : 0;
  if (c.type === "yl69")    return vcc * Math.max(0, Math.min(1, c.val / 100));
  if (c.type === "ttp223")  return c.closed ? vcc : 0;
  if (c.type === "ky040")   return vcc * Math.max(0, Math.min(1, c.val / 270));
  if (c.type === "tsop")    return c.closed ? 0 : vcc;
  if (c.type === "hc05")    return c.val === "ON" ? vcc : (c.val === "PAIR" ? vcc * 0.5 : 0);
  if (c.type === "l298n")   return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "a4988")    return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "pam8403")  return vp > 2 ? vcc * (c.val / 3) : 0;
  if (c.type === "max98357") return vp > 2 ? vcc * (c.val / 3) : 0;
  if (c.type === "ads1115")  return vcc * c.val / 4095;
  if (c.type === "mcp4725")  return vcc * c.val / 4095;
  if (c.type === "ina219")   return vcc * c.val / 2000;
  if (c.type === "mq2")      return vcc * c.val / 1023;
  if (c.type === "bh1750")   return vcc * Math.min(1, c.val / 65535);
  if (c.type === "vl53l0x")  return vcc * (1 - Math.min(1, c.val / 2000));
  if (c.type === "ic_74hc165") return vcc * (c.val & 1);
  if (c.type === "nrf24l01") return c.val === "RX" ? vcc * 0.3 : c.val === "TX" ? vcc * 0.7 : c.val === "SLEEP" ? vcc * 0.1 : 0;
  if (c.type === "sim800l")  return c.val === "REG" ? vcc * 0.8 : c.val === "ERR" ? vcc * 0.1 : 0;
  if (c.type === "drv8825")  return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tb6612")   return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "bts7960")  return c.val === "FWD" ? vcc * 0.9 : c.val === "REV" ? vcc * 0.1 : 0;
  if (c.type === "tcs34725") return c.val === "red" ? vcc * 0.9 : c.val === "green" ? vcc * 0.7 : c.val === "blue" ? vcc * 0.5 : c.val === "white" ? vcc * 0.8 : vcc * 0.6;
  if (c.type === "mlx90614") return vp > 2 ? vcc * Math.max(0, Math.min(1, (c.val - 20) / 80)) : 0;
  if (c.type === "max30102") return vcc * Math.max(0, Math.min(1, c.val / 150));
  if (c.type === "adxl345")  return c.val === "shake" ? vcc * (0.4 + 0.3 * Math.sin((t || 0) * 10)) : c.val === "tilt" ? vcc * 0.7 : c.val === "freefall" ? 0 : vcc * 0.5;
  if (c.type === "hx711")    return vcc * Math.max(0, Math.min(1, c.val / 20000));
  if (c.type === "dht22")    return vcc * Math.max(0, Math.min(1, (c.val - 10) / 40));
  if (c.type === "sgp30")    return vcc * Math.max(0, Math.min(1, c.val / 5000));
  if (c.type === "rc522")    return c.val === "CARD" ? vcc * 0.9 : c.val === "IDLE" ? vcc * 0.3 : 0;
  if (c.type === "bme680")   return vcc * Math.max(0, Math.min(1, 1 - c.val / 500));
  if (c.type === "pca9685")  return vcc * c.val / 100;
  if (c.type === "tca9548a") return vcc * c.val / 7;
  if (c.type === "l9110s")   return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmp36")    return vcc * Math.max(0, Math.min(1, c.val / 100));
  if (c.type === "am2320")   return vcc * c.val / 100;
  if (c.type === "ds1307")   return vcc * c.val / 24;
  if (c.type === "pcf8563")  return vcc * c.val / 24;
  if (c.type === "st7735")   return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssd1351")  return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "bmp180")   return vcc * Math.max(0, Math.min(1, (c.val - 500) / 513));
  if (c.type === "sht31")    return vcc * Math.max(0, Math.min(1, (c.val - 10) / 50));
  if (c.type === "apds9960") return c.val === "NEAR" ? vcc * 0.8 : c.val === "FAR" ? vcc * 0.2 : vcc * 0.5;
  if (c.type === "ds1302")   return vcc * c.val / 24;
  if (c.type === "max6675")  return vp > 2 ? vcc * Math.max(0, Math.min(1, c.val / 1024)) : 0;
  if (c.type === "max31855") return vp > 2 ? vcc * Math.max(0, Math.min(1, c.val / 2000)) : 0;
  if (c.type === "sd_card")  return c.val === "READ" ? vcc * 0.8 : c.val === "WRITE" ? vcc * 0.9 : c.val === "IDLE" ? vcc * 0.3 : 0;
  if (c.type === "enc28j60") return c.val === "RX" ? vcc * 0.4 : c.val === "TX" ? vcc * 0.7 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "uln2803")  return vcc * c.val / 8;
  if (c.type === "tlc5940")  return vcc * c.val / 100;
  if (c.type === "mpu9250")  return c.val === "shake" ? vcc * (0.4 + 0.3 * Math.sin((t || 0) * 10)) : c.val === "tilt" ? vcc * 0.7 : c.val === "rotated" ? vcc * 0.3 : vcc * 0.5;
  if (c.type === "ad9833")   return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ams1117")  return vp > c.val + 1.2 ? c.val : (vp > 0.2 ? Math.max(0, vp - 1.0) : 0);
  if (c.type === "xl6009")   return vp > 0.8 ? Math.min(c.val, vp * 3) : 0;
  if (c.type === "vl6180x")  return vcc * (1 - Math.min(1, c.val / 400));
  if (c.type === "sht10") return vcc * Math.max(0, Math.min(1, (c.val - 10) / 40));
  if (c.type === "sht75") return vcc * Math.max(0, Math.min(1, (c.val - 10) / 40));
  if (c.type === "si7021") return vcc * Math.max(0, Math.min(1, c.val / 100));
  if (c.type === "bme280") return vcc * Math.max(0, Math.min(1, (c.val - 500) / 600));
  if (c.type === "mpl3115a2") return vcc * Math.max(0, Math.min(1, (c.val - 500) / 600));
  if (c.type === "mq3") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "mq4") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "mq5") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "mq6") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "mq7") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "mq8") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "mq9") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "mq135") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "gp2y1010") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "tsl2561") return vcc * Math.min(1, c.val / 65535);
  if (c.type === "tcs3200") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "reed_switch") return c.closed ? vcc : 0;
  if (c.type === "vibration_sensor") return c.closed ? vcc : 0;
  if (c.type === "water_level") return vcc * Math.max(0, Math.min(1, c.val / 100));
  if (c.type === "flex_sensor") return vcc * Math.max(0, Math.min(1, c.val / 100));
  if (c.type === "tilt_switch") return c.closed ? vcc : 0;
  if (c.type === "shock_sensor") return c.closed ? vcc : 0;
  if (c.type === "flame_sensor") return vcc * Math.max(0, Math.min(1, c.val / 2000));
  if (c.type === "rain_sensor") return vcc * Math.max(0, Math.min(1, c.val / 100));
  if (c.type === "hall_linear") return c.closed ? vcc : 0;
  if (c.type === "cd4071") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4081") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4030") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4001") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4023") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4025") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4070") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4075") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4077") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4093") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4538") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4047") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4027") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4029") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4076") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4022") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4060") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4541") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4511") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "cd4028") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp3008") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp3208") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ads1015") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "pcf8591") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tlc5615") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp4921") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "at24c256") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "at24c512") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "w25q64") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mb85rc") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ds3234") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "rv3028") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp7940") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "nokia5110") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssd1309") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "st7565") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "st7920") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ili9341") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ili9486") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "max6954") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lcd_20x4") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "st7735_160") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssd1331") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "drv8833") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "drv8871") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "l293e") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "sn754410") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "uln2004") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "mc33926") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "bd6221") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tb67h420") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "a3959") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "drv8824") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "esp01") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rn2483") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rfm69") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rfm95") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "hc12") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "xbee") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sim900") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "m95") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nrf905") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc1101") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "lm7809") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm7812") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm7905") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm7912") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm1084") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2678") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm5007") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mcp1700") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mic5205") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lp2985") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm4871") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda2003") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ds18s20") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "lm35") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "lm75") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "tmp102") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "mcp9808") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "max31865") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "ads1118") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "hdc1080") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "htu21d") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "sht21") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "sht35") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "aht10") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "aht20") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "ms5611") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "lps25h") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "bmp388") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "dps310") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "bmp085") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "lps22hb") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mpx5700") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mq131") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mq303") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mhz19") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (5000 - (0))));
  if (c.type === "sds011") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (500 - (0))));
  if (c.type === "pms5003") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (500 - (0))));
  if (c.type === "ccs811") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "ens160") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "si1145") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (50000 - (0))));
  if (c.type === "veml7700") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (50000 - (0))));
  if (c.type === "opt3001") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (50000 - (0))));
  if (c.type === "max44009") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (50000 - (0))));
  if (c.type === "ltr329") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (50000 - (0))));
  if (c.type === "ml8511") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (11 - (0))));
  if (c.type === "veml6070") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (11 - (0))));
  if (c.type === "ina226") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (26 - (0))));
  if (c.type === "ina260") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (26 - (0))));
  if (c.type === "ina3221") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (26 - (0))));
  if (c.type === "lis3dh") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (8 - (0))));
  if (c.type === "mma8452") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (8 - (0))));
  if (c.type === "adxl335") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (8 - (0))));
  if (c.type === "adxl362") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (8 - (0))));
  if (c.type === "lsm6ds3") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (8 - (0))));
  if (c.type === "icm20948") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (8 - (0))));
  if (c.type === "bno055") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (8 - (0))));
  if (c.type === "hmc5883l") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "qmc5883l") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "mlx90393") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "lm7815") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm7824") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm7808") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm7806") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm317hv") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2940") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps7a47") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2576") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2574") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mp1584") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps5430") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mt3608") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2577") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps61023") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "max1771") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm3886") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7294") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda2050") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7377") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3116") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa2005") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm4766") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "drv8434") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2209") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2130") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "l6470") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "vnh5019") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "drv8313") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "a4950") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "mx1508") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "esp32cam") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sx1278") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sx1276") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nrf52832") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "hm10") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "jdy23") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ublox_neo6m") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ublox_neo7m") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w5500") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cp2102") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ch340") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "max485") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mcp2515") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ssd1322") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "ssd1327") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "ssd1306_64") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "st7789") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "ili9488") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "hd44780") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "tm1637") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "ht16k33") return c.val === "ON" ? vcc * 0.8 : 0;
  if (c.type === "cd4017b") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc14") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc04") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc08") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc32") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc86") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc74") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc590") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc4067") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24c64") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24c128") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w25q128") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "fm25v02") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mcp23s17") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "tca9534") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "max7301") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "tmp117") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "max30205") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "amg8833") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "mlx90640") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "lm73") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "si7050") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "ds28ea00") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "ad8495") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "hih6130") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "dht21") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "sht40") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "sht45") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "hdc2080") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "bme688") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "bmp390") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "bmp581") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "lps35hw") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "lps33hw") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "spl06") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "ms5837") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mq137") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mq138") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mq214") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mq216") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "scd30") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "scd40") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "scd41") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "sgp40") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "sen54") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "ags02ma") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "as7341") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "as7262") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "tsl2591") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "veml6075") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "guva_s12sd") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "bh1745") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "isl29125") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "apds9306") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "mpu6500") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lsm9ds1") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lsm303") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "l3gd20h") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "bmi160") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "bmi270") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "adxl375") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "icm42688") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lis2dh12") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "kxtj3") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "vl53l1x") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "gp2y0a21") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "gp2y0a02") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "us100") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "a02yyuw") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "ld2410") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "rcwl0516") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "tfmini") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "tf_luna") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "vcnl4040") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "jsn_sr04t") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "max30100") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "ad8232") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "pulse_sensor") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "gsr_sensor") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "r307") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "ina169") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "acs758") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "max471") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "pzem004t") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "hlw8012") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ina228") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ina238") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ss49e") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "a1302") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "drv5053") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "as5600") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "as5048a") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "sh1106") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssd1305") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "gc9a01") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "st7796") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ili9225") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssd1963") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "epd_154") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "epd_213") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "epd_29") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lcd_12864") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lcd_16x4") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lcd_8x2") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tm1638") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ht1621") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "drv8847") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "drv8880") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2208") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2160") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc5160") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "l6208") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "l6235") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "vnh2sp30") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "ibt2") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "lv8548") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "lm7818") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm78l05") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm79l05") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm317l") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm350") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ld1117") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xc6206") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ap2112") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tlv1117") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lt3045") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2575") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2595") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xl4015") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xl4005") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xl7005") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mp2307") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mp2315") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps54331") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "sx1308") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "cn3791") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "bq24074") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tp5100") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ip5306") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "esp32_c3") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "esp32_s3") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nrf52840") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "hc06") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "hm11") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "jdy31") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "e32") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sx1262") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "dw1000") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "pn532") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w5100") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "enc424j600") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mcp2551") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "tja1050") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sn65hvd230") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "max232") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "max3232") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ft232") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "pl2303") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cp2104") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "l76k") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "neo_m8n") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sim7600") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim868") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "a7670") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc02") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc10") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc20") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc30") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc125") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc157") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc151") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc139") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc154") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc161") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc164") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc166") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc174") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc175") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc193") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc244") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc245") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc283") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc374") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc4040") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc4046") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc4053") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc4094") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mcp23008") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "tca9535") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "txs0108") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sn74lvc245") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24c02") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24c08") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24c16") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "lm1875") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda2040") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7498") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3110") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "pam8610") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "pam8302") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "max9744") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp6002") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp6022") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tl082") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tl084") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lf353") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lf411") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "op07") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "op27") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8605") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tmp116") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "tmp1075") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "max6633") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "mcp9701") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "lm19") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "lm34") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "lm335") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "ad590") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "tmp35") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "tmp37") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "sts31") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "stlm20") return vcc * Math.max(0, Math.min(1, (c.val - (-40)) / (125 - (-40))));
  if (c.type === "sht85") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "hih7130") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "hts221") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "hdc3020") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "shtc3") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "shtc1") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "si7020") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "am2301") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "am2302") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "capacitive_soil") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "fc28") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "lps22hh") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mpl115a2") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "ms5803") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "ms5607") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mprls") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "bmp384") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "icp10125") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "icp20100") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mpx4115") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mpxv7002") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "xgzp6847") return vcc * Math.max(0, Math.min(1, (c.val - (300)) / (1100 - (300))));
  if (c.type === "mq136") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mq139") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mq309") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "tgs2600") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "tgs2602") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "tgs2620") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mics5524") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mics6814") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mh_z14a") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "mh_z16") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "s8_co2") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "iaq_core") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "zmod4410") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "zh03b") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (2000 - (0))));
  if (c.type === "tsl2572") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "veml3235") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "opt4048") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "opt3004") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "ltr390") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "ltr303") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "ltr559") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "as7343") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "as7265x") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "ap3216") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "vcnl4200") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "si1133") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100000 - (0))));
  if (c.type === "mpu6886") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "mpu9255") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lsm6dso") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lsm6dsox") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lis3mdl") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lis2mdl") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "lis3dsh") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "mma7660") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "mma8451") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "mma7361") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "bma280") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "bma423") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "bmi088") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "bmx160") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "icm20689") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "icm42605") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "fxos8700") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "fxas21002") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "l3g4200d") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "itg3200") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (16 - (0))));
  if (c.type === "vl53l4cd") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "vl53l3cx") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "tof050c") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "tf02") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "tf03") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "hcsr05") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "srf05") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "maxsonar_ez1") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "us015") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "us020") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "urm37") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "ld2450") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "ld2420") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "hb100") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "sen0311") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "max30101") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "max86150") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "afe4490") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "ads1292") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "ad8233") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "max30003") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "emg_sensor") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "muscle_v3") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "gsr_grove") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "skin_temp_mlx") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (200 - (0))));
  if (c.type === "ina180") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ina199") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ina210") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ina230") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ina233") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "acs711") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "acs723") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "acs724") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "acs781") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "max9611") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ltc4151") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ltc2945") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "pac1934") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "bl0937") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "pzem017") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "ade7753") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "atm90e26") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "hmc5983") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "mmc5603") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "mmc5983ma") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "ak8963") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "ak09916") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "qmc6310") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "bmm150") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "tmag5273") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "tlv493d") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "a1324") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "ss495a") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "drv5055") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "as5047p") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "ma730") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "mt6701") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (400 - (0))));
  if (c.type === "max9814") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "max4466") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "ics43434") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "inmp441") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "sph0645") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "spm0405") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "mp34dt05") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "ky037") return vcc * Math.max(0, Math.min(1, (c.val - (30)) / (130 - (30))));
  if (c.type === "fsr402") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "fsr406") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "load_cell_5kg") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "load_cell_20kg") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "piezo_film") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "flex_4in") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "yfs201") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "yfs401") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "yfs210") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "yfb08") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "fs300a") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "fs400a") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (30 - (0))));
  if (c.type === "float_switch") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "ultrasonic_level") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "capacitive_level") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "optical_level") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "soil_moisture_v2") return vcc * Math.max(0, Math.min(1, (c.val - (0)) / (100 - (0))));
  if (c.type === "st7567") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "st7789_135") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "st7735_80") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ili9163") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ili9327") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ili9342") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ili9806") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "hx8357") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "hx8347") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ra8875") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssd1289") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssd2119") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "sed1520") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ks0108") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "pcd8544") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "uc1701") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "uc1609") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "t6963c") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "drv8701") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "drv8424") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "drv8428") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2100") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2226") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2225") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2240") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tmc2660") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "a4982") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "a4983") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "l6219") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "l297") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "l298p") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tb6560") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tb6600") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "tb67s109") return c.val === "FWD" ? vcc * 0.8 : c.val === "REV" ? vcc * 0.2 : 0;
  if (c.type === "lm78m05") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2937") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2931") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm1086") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm1085") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lt1763") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lt1963") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lt3042") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps7a20") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps73401") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "adp150") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "adp3338") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mcp1802") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mcp1826") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ap7361") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ap7333") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "rt9013") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ld39050") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tlv70033") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm22676") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2672") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2674") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm5008") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm5164") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ltc3630") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ltc3115") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps54360") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps62130") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps62160") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps62933") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mp1470") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mp2359") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mp2491") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xl1509") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xl2596") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mc34063") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps63020") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps61088") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps61230") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mp3429") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xl6019") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "xl6012") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ap3012") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm2621") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "lm3478") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps55340") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tps61200") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tp4057") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "tp4054") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mcp73831") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "mcp73832") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "bq24072") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "bq24075") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "bq25606") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "bq25895") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ltc4054") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ltc4065") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "cn3722") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "cn3765") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ip2312") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "ip5310") return vp > c.val + 1.5 ? c.val : (vp > 0.5 ? Math.max(0, vp - 1.5) : 0);
  if (c.type === "esp32_wroom") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "esp32_s2") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "esp32_c6") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "esp12f") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "esp12e") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "esp07") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "bl602") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rtl8710") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rtl8720dn") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nrf51822") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nrf52810") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nrf5340") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nrf9160") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc2530") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc2531") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc2640") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc2652") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc3200") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc1310") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc1125") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cc2500") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "si4432") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "si4463") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "si4455") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sx1280") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sx1272") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sx1301") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rfm12b") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rfm22b") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rfm98") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rfm96") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "rfm63") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "xbee_pro") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "xbee3") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "bl654") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ch341") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ch9102") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ch343") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cp2102n") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ft231x") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ft2232") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ft232h") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mcp2221") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "max3485") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sp3485") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sn65hvd72") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ltc2850") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "iso1176") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "adm2587") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "adm3053") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mcp2562") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "tcan1042") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "tja1051") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sn65hvd1050") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "l80") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "l86") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "atgm336h") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "gt_u7") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "neo_m9n") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "zoe_m8q") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "max_m10s") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "teseo_liv3") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mtk3339") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "pa1010d") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sim28") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "l96") return c.val === "TX" ? vcc * 0.7 : c.val === "RX" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sim800c") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim808") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim5320") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim7000") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim7070") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim7080") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim7500") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "sim7670") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "ec200s") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "ec25") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "bg95") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "bg96") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "m26") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "ec21") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "ec600") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "a9g") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "a6") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "a7672e") return c.val === "REG" ? vcc * 0.7 : c.val === "ERR" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc03") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc05") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc09") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc21") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc27") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc51") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc58") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc85") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc107") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc109") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc112") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc123") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc126") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc132") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc137") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc147") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc148") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc153") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc158") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc160") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc162") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc163") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc168") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc169") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc173") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc182") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc190") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc191") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc192") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc194") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc195") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc238") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc239") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc240") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc241") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc251") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc253") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc257") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc258") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ic_74hc259") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4000") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4002") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4006") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4007") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4008") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4009") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4010") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4011") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4012") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4014") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4016") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4018") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4019") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4020") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4021") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4024") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4026") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4033") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4034") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4035") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4040") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4042") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4043") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4044") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4049") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4050") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4052") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4053") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4069") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4072") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4073") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4078") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4082") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4094") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4099") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd40106") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd40193") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "cd4585") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "tlc555") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "icm7555") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "lmc555") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "xr2206") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "icl8038") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "max038") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "lm566") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "lm567") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ne565") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "ne567") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24c01") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24c04") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24cm01") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at24cm02") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "m24c64") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "m24256") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w25q16") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w25q32") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w25q80") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w25q256") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "w25q512") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mx25l1606") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mx25l3206") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mx25l6406") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mx25l12805") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sst25vf016") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "s25fl064") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "is25lp128") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "gd25q32") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "gd25q64") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "fm24cl64") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "fm24v10") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "fm25cl64") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mb85rs64") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mb85rs256") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "mcp23k256") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sram_23lc1024") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sram_23lc512") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sram_23k256") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "c93c46") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "c93c56") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "c93c66") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "c93c86") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at25010") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at25640") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "at25m01") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sdram_is42s16160") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "sdram_w9825g6") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "psram_aps6404") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "psram_ips6404") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nand_w25n01") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "nand_mt29f") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "emmc_4gb") return c.val === "READ" ? vcc * 0.7 : c.val === "WRITE" ? vcc * 0.4 : c.val === "IDLE" ? vcc * 0.2 : 0;
  if (c.type === "lm1876") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm2877") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm3875") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm4780") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda1514") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda1521") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda2005") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda2006") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda2009") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7240") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7266") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7293") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7296") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7379") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7384") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7388") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tda7391") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3118") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3123") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3128") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3130") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3140") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa3220") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "max9768") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "max9788") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "max98400") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssm3582") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "stk4141") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "pam8620") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm4950") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm4991") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa6120") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa6132") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa6211") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa2012") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tpa2031") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "pam8406") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "pam8304") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ssm2302") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm833") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm4562") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm4558") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lm1458") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa134") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa227") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa277") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa337") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa343") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa350") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa551") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa564") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa1612") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa1656") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa1678") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa2604") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "opa2350") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8066") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8397") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad797") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8099") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8221") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8276") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8429") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8606") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ad8628") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lt1013") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lt1028") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lt1124") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lt1677") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lt6015") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lmv358") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lmv321") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lmv324") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lmc6482") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lmc662") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "lmp7701") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp6001") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp6004") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp6231") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp6241") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "mcp6271") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tlv2371") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tlv2462") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tlv271") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tlv9061") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "tlv9062") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ca3140") return vp > 2 ? vcc * 0.5 : 0;
  if (c.type === "ca3130") return vp > 2 ? vcc * 0.5 : 0;
  return 0;
}

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
  comps.forEach(function (c) {
    parent[c.id + ".a"] = c.id + ".a";
    parent[c.id + ".b"] = c.id + ".b";
    if (hasThreePins(c)) parent[c.id + ".c"] = c.id + ".c";
    if (c.type.indexOf("gate_") === 0) parent[c.id + ".out"] = c.id + ".out";
    if (c.type === "relay") { parent[c.id + ".c"] = c.id + ".c"; parent[c.id + ".out"] = c.id + ".out"; }
  });
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

function simulate(comps, wires, timeSec, realSec) {
  timeSec = timeSec || 0; realSec = realSec || 0;
  comps = comps.map(aliasView);
  var out = { ok: false, reason: "", V: {}, I: {}, P: {}, ledOn: {}, diodeOn: {}, transOn: {}, nodeOf: {}, warnings: [] };
  var bat = null;
  for (var i = 0; i < comps.length; i++) {
    if (isSource(comps[i])) { bat = comps[i]; break; }
  }
  if (!bat) { out.reason = "nobattery"; return out; }
  var nm = nodeMap(comps, wires);
  out.nodeOf = nm.node;
  var gnd = nm.node[bat.id + ".b"];
  var map = new Array(nm.count), n = 0, k;
  for (k = 0; k < nm.count; k++) map[k] = (k === gnd) ? -1 : n++;
  function mi(c, t) { return map[nm.node[c.id + "." + t]]; }

  var ledOn = {}, diodeOn = {}, transOn = {}, gateOut = {}, relayOn = {}, vcc = bat.type === "ac_source" ? 5 : bat.val;
  var zenerSt = {};
  var regSt = {}, regTh = {}, opOut = {};
  var timer555Out = {}, timer555V = {}, pirActive = {}, servoOn = {}, hcV = {}, movSt = {}, devV = {};
  comps.forEach(function (c) {
    if (c.type.indexOf("gate_") === 0) gateOut[c.id] = false;
    if (c.type === "relay") relayOn[c.id] = false;
    if (c.type === "led" || c.type === "rgb_led" || c.type === "ws2812") ledOn[c.id] = false;
    if (c.type === "diode" || c.type === "schottky") diodeOn[c.id] = false;
    if (c.type === "zener") zenerSt[c.id] = 0;
    if (c.type === "transistor" || c.type === "transistor_pnp") transOn[c.id] = false;
    if (c.type === "reg7805" || c.type === "reg7803") { regSt[c.id] = 0; regTh[c.id] = 0; }
    if (c.type === "opamp") opOut[c.id] = false;
    if (c.type === "timer555") { timer555Out[c.id] = false; timer555V[c.id] = 0; }
    if (c.type === "pir") pirActive[c.id] = !!c.closed;
    if (c.type === "mosfet_n") transOn[c.id] = false;
    if (c.type === "lm317") { regSt[c.id] = 0; regTh[c.id] = 0; }
    if (c.type === "servo") servoOn[c.id] = false;
    if (c.type === "hc_sr04") hcV[c.id] = 0;
    if (c.type === "varistor") movSt[c.id] = 0;
    if (c.type === "seven_seg_4" || c.type === "l293d" || c.type === "hc595" || c.type === "optocoupler") devV[c.id] = 0;
    if (c.type === "lm386" || c.type === "lm358" || c.type === "ne5532" || c.type === "lm393" || c.type === "cd4017" || c.type === "ic_74hc138") devV[c.id] = 0;
    if (c.type === "tl072" || c.type === "lm324" || c.type === "ne556" || c.type === "uln2003" || c.type === "lm1117" || c.type === "lm3914") devV[c.id] = 0;
    if (c.type === "tda2030" || c.type === "lm2596" || c.type === "tp4056" || c.type === "adc0804" || c.type === "dac0808" || c.type === "max7219") devV[c.id] = 0;
    if (c.type === "lm741" || c.type === "ne5534" || c.type === "tda2822" || c.type === "cd4051" || c.type === "pcf8574") devV[c.id] = 0;
    if (c.type === "tda7297" || c.type === "opa2134" || c.type === "ad620" || c.type === "opa548" || c.type === "lm337" || c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017" || c.type === "ic_74hc00") devV[c.id] = 0;
    if (SENSOR_SET[c.type]) devV[c.id] = 0;
  });
  function diodeVf(c) { return c.type === "schottky" ? 0.3 : (c.val === "germanium" ? 0.3 : 0.7); }
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
      if (isSource(c)) {
        var g = 1 / R_BATT; stampG(a, b, g); stampI(a, b, srcV(c, timeSec) * g);
      }
      else if (c.type === "resistor" || c.type === "bulb" || c.type === "motor" || c.type === "buzzer" || c.type === "ldr" || c.type === "inductor" || c.type === "speaker" || c.type === "thermistor") {
        var res = c.val;
        if (c.type === "ldr") res = ldrRes(c);
        else if (c.type === "inductor") res = 0.001;
        else if (c.type === "thermistor") res = c.val * (c.closed ? 0.1 : 10);
        if (res <= 0) res = 0.001;
        stampG(a, b, 1 / res);
      }
      else if (c.type === "potentiometer") {
        var wc = mi(c, "c"), rt = c.val > 0.002 ? c.val : 0.002, pp = potPos(c);
        stampG(a, wc, 1 / Math.max(rt * pp, 0.001));
        stampG(wc, b, 1 / Math.max(rt * (1 - pp), 0.001));
      }
      else if (c.type.indexOf("gate_") === 0) {
        var go = mi(c, "out"), gg = 1 / R_GATE;
        stampG(go, -1, gg); stampI(go, -1, (gateOut[c.id] ? vcc : 0) * gg);
      }
      else if (c.type === "relay") {
        stampG(a, b, 1 / R_RELAY_COIL);
        if (relayOn[c.id]) stampG(mi(c, "c"), mi(c, "out"), 1 / 0.01);
      }
      else if (c.type === "fuse") { stampG(a, b, 1 / 0.01); }
      else if (c.type === "capacitor") { stampG(a, b, 1e-9); }
      else if (c.type === "switch") { if (c.closed) stampG(a, b, 1 / R_SW_ON); } // مغلق = يمرر
      else if (c.type === "led" && ledOn[c.id]) {
        var gl = 1 / R_LED, vf = LED_COLORS[c.val] ? LED_COLORS[c.val].vf : 2;
        stampG(a, b, gl); stampI(a, b, gl * vf);
      }
      else if ((c.type === "diode" || c.type === "schottky") && diodeOn[c.id]) {
        stampG(a, b, 1.0); stampI(a, b, diodeVf(c));
      }
      else if (c.type === "zener" && zenerSt[c.id] === 1) {
        stampG(a, b, 1.0); stampI(a, b, 0.7);
      }
      else if (c.type === "zener" && zenerSt[c.id] === -1) {
        stampG(a, b, 1.0); stampI(a, b, -c.val);
      }
      else if (c.type === "transistor" && transOn[c.id]) {
        stampG(a, b, 1 / R_TRANSISTOR);
      }
      else if (c.type === "transistor_pnp" && transOn[c.id]) {
        stampG(a, b, 1 / R_TRANSISTOR);
      }
      else if (c.type === "reg7805" || c.type === "reg7803") {
        if (regSt[c.id]) {
          var gReg = 1 / 0.05, oReg = mi(c, "c");
          stampG(oReg, b, gReg); stampI(oReg, b, regTh[c.id] * gReg);
          stampG(a, b, 1 / 2200);
        }
      }
      else if (c.type === "opamp") {
        var gOp = 1 / 0.05, oOp = mi(c, "c");
        stampG(oOp, -1, gOp); stampI(oOp, -1, (opOut[c.id] ? vcc : 0) * gOp);
      }
      else if (c.type === "pir") {
        if (pirActive[c.id]) stampG(a, b, 1 / 0.05);
      }
      else if (c.type === "dht11") {
        stampG(a, b, 1 / 10000);
      }
      else if (c.type === "seven_seg") {
        stampG(a, b, 1 / 500);
        if (mi(c, "c") >= 0) stampG(mi(c, "c"), -1, 1 / 10000);
      }
      else if (c.type === "timer555") {
        if (timer555V[c.id] > 0) {
          var g555 = 1 / 0.05, o555 = mi(c, "c");
          stampG(o555, b, g555); stampI(o555, b, (timer555Out[c.id] ? timer555V[c.id] : 0) * g555);
          stampG(a, b, 1 / 50000);
        }
      }
      else if (c.type === "mosfet_n" && transOn[c.id]) {
        stampG(a, b, 1 / 0.05);
      }
      else if (c.type === "lm317") {
        if (regSt[c.id]) {
          var g317 = 1 / 0.05, o317 = mi(c, "c");
          stampG(o317, b, g317); stampI(o317, b, regTh[c.id] * g317);
          stampG(a, b, 1 / 1500);
        }
      }
      else if (c.type === "servo") {
        if (servoOn[c.id]) stampG(mi(c, "b"), mi(c, "c"), 1 / 40);
      }
      else if (c.type === "lcd_16x2" || c.type === "ds18b20") {
        stampG(a, b, 1 / 100000);
      }
      else if (c.type === "hc_sr04") {
        stampG(a, b, 1 / 200);
        if (hcV[c.id] > 0) {
          var gSr = 1 / 0.05, oSr = mi(c, "c");
          stampG(oSr, b, gSr); stampI(oSr, b, hcV[c.id] * gSr);
        }
      }
      else if (c.type === "stepper_motor") {
        stampG(a, b, 1 / (c.val > 0 ? c.val * 0.05 : 10));
      }
      else if ((c.type === "rgb_led" || c.type === "ws2812") && ledOn[c.id]) {
        var glRgb = 1 / R_LED, vfRgb = 2.5;
        stampG(a, b, glRgb); stampI(a, b, glRgb * vfRgb);
      }
      else if (c.type === "varistor") {
        if (movSt[c.id] === 0) stampG(a, b, 1e-7);
        else { stampG(a, b, 1 / 10); stampI(a, b, movSt[c.id] * c.val / 10); }
      }
      else if (c.type === "oled_ssd1306" || c.type === "ds3231") { stampG(a, b, 1 / 100000); }
      else if (c.type === "seven_seg_4") {
        stampG(a, b, 1 / 800);
        if (devV[c.id] > 0) { var g7 = 1 / 0.05, o7 = mi(c, "c"); stampG(o7, b, g7); stampI(o7, b, devV[c.id] * g7); }
      }
      else if (c.type === "l293d") {
        stampG(a, b, 1 / 5000);
        if (devV[c.id] !== 0) { var gL = 1 / 0.5, oL = mi(c, "c"); stampG(oL, b, gL); stampI(oL, b, devV[c.id] * gL); }
      }
      else if (c.type === "hc595") {
        stampG(a, b, 1 / 50000);
        if (devV[c.id] > 0) { var g5 = 1 / 0.1, o5 = mi(c, "c"); stampG(o5, b, g5); stampI(o5, b, devV[c.id] * g5); }
      }
      else if (c.type === "optocoupler") {
        if (devV[c.id] > 0) { var gO = 1 / 50; stampG(a, b, gO); stampI(a, b, gO * 1.2); }
        else stampG(a, b, 1e-7);
      }
      else if (c.type === "lm386" || c.type === "lm358" || c.type === "ne5532" || c.type === "lm393" || c.type === "cd4017" || c.type === "ic_74hc138") {
        stampG(a, b, 1 / 50000);
        var gN = 1 / (c.type === "lm386" ? 1 : 0.05), oN = mi(c, "c");
        stampG(oN, b, gN); stampI(oN, b, devV[c.id] * gN);
      }
      else if (c.type === "tl072" || c.type === "lm324" || c.type === "ne556" || c.type === "lm1117" || c.type === "lm3914") {
        stampG(a, b, c.type === "lm1117" ? 1 / 5000 : (c.type === "tl072" ? 1 / 1000000 : 1 / 50000));
        var gM = 1 / 0.05, oM = mi(c, "c");
        stampG(oM, b, gM); stampI(oM, b, devV[c.id] * gM);
      }
      else if (c.type === "uln2003") {
        stampG(a, b, 1 / 100000);
        stampG(mi(c, "c"), b, devV[c.id] > 0 ? 1 : 1e-6);
      }
      else if (c.type === "tda2030" || c.type === "lm2596" || c.type === "tp4056" || c.type === "adc0804" || c.type === "dac0808" || c.type === "max7219") {
        stampG(a, b, c.type === "lm2596" ? 1 / 3000 : (c.type === "tda2030" ? 1 / 100000 : (c.type === "adc0804" ? 1 / 1000000 : 1 / 50000)));
        var gQ = 1 / (c.type === "tda2030" ? 4 : (c.type === "lm2596" || c.type === "tp4056" ? 0.1 : 0.05)), oQ = mi(c, "c");
        stampG(oQ, b, gQ); stampI(oQ, b, devV[c.id] * gQ);
      }
      else if (c.type === "lm741" || c.type === "ne5534" || c.type === "tda2822" || c.type === "cd4051" || c.type === "pcf8574") {
        stampG(a, b, c.type === "lm741" ? 1 / 2000000 : (c.type === "ne5534" ? 1 / 500000 : (c.type === "tda2822" ? 1 / 200000 : (c.type === "cd4051" ? 1 / 100000 : 1 / 50000))));
        var gR = 1 / (c.type === "tda2822" ? 1 : (c.type === "cd4051" ? 0.1 : 0.05)), oR = mi(c, "c");
        stampG(oR, b, gR); stampI(oR, b, devV[c.id] * gR);
      }
      else if (c.type === "cd4066") { stampG(a, b, c.val === "closed" ? 1 / 15 : 1e-7); }
      else if (c.type === "tda7297" || c.type === "opa2134" || c.type === "ad620" || c.type === "opa548" || c.type === "lm337") {
        stampG(a, b, c.type === "tda7297" ? 1 / 100000 : (c.type === "opa2134" ? 1 / 300000 : (c.type === "ad620" ? 1 / 10000000 : (c.type === "opa548" ? 1 / 100000 : 1 / 5000))));
        var gS = 1 / (c.type === "tda7297" ? 1 : (c.type === "opa548" ? 0.5 : 0.05)), oS = mi(c, "c");
        stampG(oS, b, gS); stampI(oS, b, devV[c.id] * gS);
      }
      else if (c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017" || c.type === "ic_74hc00") {
        stampG(a, -1, 1 / 100000); stampG(b, -1, 1 / 100000);
        var gT = 1 / 0.05, oT = mi(c, "c");
        stampG(oT, -1, gT); stampI(oT, -1, devV[c.id] * gT);
      }
      else if (SENSOR_SET[c.type]) {
        stampG(a, b, 1 / 100000);
        var gSen = 1 / 100, oSen = mi(c, "c");
        stampG(oSen, b, gSen); stampI(oSen, b, devV[c.id] * gSen);
      }
    });

    var x = n > 0 ? solveLinear(A, z) : [];
    if (!x) { out.reason = "singular"; return out; }
    volt = x;
    var changed = false;
    comps.forEach(function (c) {
      if (c.type === "led" || c.type === "rgb_led" || c.type === "ws2812" || c.type === "diode" || c.type === "schottky") {
        var va = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, vb = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
        var vf = c.type === "led" ? (LED_COLORS[c.val] ? LED_COLORS[c.val].vf : 2) : ((c.type === "rgb_led" || c.type === "ws2812") ? 2.5 : diodeVf(c));
        var on = (va - vb) > vf;
        var st = (c.type === "led" || c.type === "rgb_led" || c.type === "ws2812") ? ledOn : diodeOn;
        if (on !== st[c.id]) { st[c.id] = on; changed = true; }
      } else if (c.type === "zener") {
        var zva = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, zvb = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
        var zon = (zva - zvb) > 0.7 ? 1 : ((zvb - zva) > c.val ? -1 : 0);
        if (zon !== zenerSt[c.id]) { zenerSt[c.id] = zon; changed = true; }
      } else if (c.type === "transistor") {
        var vc = mi(c, "c") >= 0 ? x[mi(c, "c")] : 0;
        var vb2 = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
        var on2 = (vc - vb2) > 0.7;
        if (on2 !== transOn[c.id]) { transOn[c.id] = on2; changed = true; }
      } else if (c.type === "transistor_pnp") {
        var vBpnp = mi(c, "c") >= 0 ? x[mi(c, "c")] : 0;
        var vEpnp = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
        var onPnp = (vEpnp - vBpnp) > 0.7;
        if (onPnp !== transOn[c.id]) { transOn[c.id] = onPnp; changed = true; }
      } else if (c.type === "reg7805" || c.type === "reg7803") {
        var rgI = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, rgG = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, rgH = rgI - rgG;
        var rgOn = rgH > 0.2 ? 1 : 0;
        var rgTh = rgOn ? Math.max(0, Math.min(c.val, rgH - 1.0)) : 0;
        if (rgOn !== regSt[c.id] || Math.abs(rgTh - regTh[c.id]) > 0.002) { regSt[c.id] = rgOn; regTh[c.id] = rgTh; changed = true; }
      } else if (c.type === "opamp") {
        var opN = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, opP = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
        var opWant = opOut[c.id] ? (opP - opN) > -0.001 : (opP - opN) > 0.001;
        if (opWant !== opOut[c.id]) { opOut[c.id] = opWant; changed = true; }
      } else if (c.type === "pir") {
        var pirNow = !!c.closed;
        if (pirNow !== pirActive[c.id]) { pirActive[c.id] = pirNow; changed = true; }
      } else if (c.type === "timer555") {
        var vSup = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, vGg = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
        var pw555 = (vSup - vGg) > 2.0, sv555 = pw555 ? (vSup - vGg) : 0;
        var wave555 = pw555 && (Math.floor(realSec * c.val * 2) % 2 === 1);
        if (wave555 !== timer555Out[c.id] || Math.abs(sv555 - timer555V[c.id]) > 0.002) { timer555Out[c.id] = wave555; timer555V[c.id] = sv555; changed = true; }
      } else if (c.type === "mosfet_n") {
        var mVg = mi(c, "c") >= 0 ? x[mi(c, "c")] : 0, mVs = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0;
        var mOn = (mVg - mVs) > (c.val === "IRLZ44" ? 2.0 : 4.0);
        if (mOn !== transOn[c.id]) { transOn[c.id] = mOn; changed = true; }
      } else if (c.type === "lm317") {
        var l3I = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, l3G = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, l3H = l3I - l3G;
        var l3On = l3H > 0.2 ? 1 : 0;
        var l3Th = l3On ? Math.max(0, Math.min(c.val, l3H - 2.0)) : 0;
        if (l3On !== regSt[c.id] || Math.abs(l3Th - regTh[c.id]) > 0.002) { regSt[c.id] = l3On; regTh[c.id] = l3Th; changed = true; }
      } else if (c.type === "servo") {
        var svG = mi(c, "c") >= 0 ? x[mi(c, "c")] : 0;
        var svP = (mi(c, "b") >= 0 ? x[mi(c, "b")] : 0) - svG, svSig = (mi(c, "a") >= 0 ? x[mi(c, "a")] : 0) - svG;
        var svNow = svP > 3.0 && svSig > 0.5;
        if (svNow !== servoOn[c.id]) { servoOn[c.id] = svNow; changed = true; }
      } else if (c.type === "hc_sr04") {
        var srA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, srB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, srP = srA - srB;
        var srNew = srP > 3.0 ? srP * Math.min(1, c.val / 400) : 0;
        if (Math.abs(srNew - hcV[c.id]) > 0.002) { hcV[c.id] = srNew; changed = true; }
      } else if (c.type === "varistor") {
        var mvA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, mvB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, mvD = mvA - mvB;
        var mvNew = mvD > c.val ? 1 : (mvD < -c.val ? -1 : 0);
        if (mvNew !== movSt[c.id]) { movSt[c.id] = mvNew; changed = true; }
      } else if (c.type === "seven_seg_4" || c.type === "l293d" || c.type === "hc595" || c.type === "optocoupler") {
        var dvA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, dvB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, dvP = dvA - dvB, dvNew = 0;
        if (c.type === "seven_seg_4") dvNew = dvP > 1.5 ? dvP * 0.3 : 0;
        else if (c.type === "l293d") dvNew = (dvP > 2.0 && c.val !== "STOP") ? dvP * 0.5 * (c.val === "FWD" ? 1 : -1) : 0;
        else if (c.type === "hc595") dvNew = dvP > 2.0 ? dvP * 0.3 : 0;
        else dvNew = dvP > 1.2 ? 1 : 0;
        if (Math.abs(dvNew - devV[c.id]) > 0.002) { devV[c.id] = dvNew; changed = true; }
      } else if (c.type === "lm386" || c.type === "lm358" || c.type === "ne5532" || c.type === "lm393" || c.type === "cd4017" || c.type === "ic_74hc138") {
        var nvA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, nvB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, nvP = nvA - nvB, nvNew = 0;
        if (c.type === "lm386") nvNew = Math.max(0, Math.min(vcc, nvP * (c.val || 20)));
        else if (c.type === "lm358") nvNew = Math.max(0, Math.min(vcc, nvP * 100));
        else if (c.type === "ne5532") nvNew = Math.max(0, Math.min(vcc, nvP * 1000));
        else if (c.type === "lm393") nvNew = nvP > vcc / 2 ? vcc : 0;
        else if (c.type === "cd4017") {
          var cdS = cntState[c.id] || (cntState[c.id] = { step: 0, setVal: null, hi: null });
          if (cdS.setVal !== c.val) { cdS.step = c.val; cdS.setVal = c.val; }
          var cdHi = nvP > 2.5;
          if (cdS.hi === false && cdHi) { cdS.step = (cdS.step + 1) % 10; changed = true; }
          cdS.hi = cdHi;
          nvNew = vcc * cdS.step / 9;
        }
        else nvNew = nvP > 2.5 ? vcc * c.val / 7 : 0;
        if (Math.abs(nvNew - devV[c.id]) > 0.002) { devV[c.id] = nvNew; changed = true; }
      } else if (c.type === "tl072" || c.type === "lm324" || c.type === "ne556" || c.type === "uln2003" || c.type === "lm1117" || c.type === "lm3914") {
        var wvA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, wvB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, wvP = wvA - wvB, wvNew = 0;
        if (c.type === "tl072") wvNew = Math.max(0, Math.min(vcc, wvP * 200));
        else if (c.type === "lm324") wvNew = Math.max(0, Math.min(vcc, wvP * 100));
        else if (c.type === "ne556") wvNew = (wvP > 2.0 && Math.floor(realSec * (c.val > 0 ? c.val : 1) * 2) % 2 === 1) ? wvP : 0;
        else if (c.type === "uln2003") wvNew = wvP > 2.5 ? 1 : 0;
        else if (c.type === "lm1117") wvNew = wvP > c.val + 1.2 ? c.val : (wvP > 0.2 ? Math.max(0, wvP - 1.0) : 0);
        else wvNew = Math.max(0, Math.min(1, wvP / c.val)) * vcc;
        if (Math.abs(wvNew - devV[c.id]) > 0.002) { devV[c.id] = wvNew; changed = true; }
      } else if (c.type === "tda2030" || c.type === "lm2596" || c.type === "tp4056" || c.type === "adc0804" || c.type === "dac0808" || c.type === "max7219") {
        var qvA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, qvB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, qvP = qvA - qvB, qvNew = 0;
        if (c.type === "tda2030") qvNew = Math.max(0, Math.min(vcc, qvP * (c.val || 20)));
        else if (c.type === "lm2596") qvNew = qvP > c.val + 1.5 ? c.val : (qvP > 0.2 ? Math.max(0, qvP - 1.5) : 0);
        else if (c.type === "tp4056") qvNew = qvP > 4.0 ? 3.7 + 0.5 * (c.val / 100) : (c.val > 0 ? 3.0 + 1.2 * (c.val / 100) : 0);
        else if (c.type === "adc0804") {
          var adcRef = c.val || 5, adcCode = Math.round(Math.max(0, Math.min(adcRef, qvP)) / adcRef * 255);
          qvNew = vcc * adcCode / 255;
        }
        else if (c.type === "dac0808") qvNew = vcc * Math.max(0, Math.min(255, c.val || 0)) / 255;
        else qvNew = qvP > 3.0 ? Math.min(vcc, 5.0) : 0;
        if (Math.abs(qvNew - devV[c.id]) > 0.002) { devV[c.id] = qvNew; changed = true; }
      } else if (c.type === "lm741" || c.type === "ne5534" || c.type === "tda2822" || c.type === "cd4051" || c.type === "pcf8574") {
        var rvA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, rvB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, rvP = rvA - rvB, rvNew = 0;
        if (c.type === "lm741") rvNew = Math.max(0, Math.min(vcc, rvP * 100000));
        else if (c.type === "ne5534") rvNew = Math.max(0, Math.min(vcc, rvP * 1000));
        else if (c.type === "tda2822") rvNew = Math.max(0, Math.min(vcc, rvP * (c.val || 2) * 100));
        else if (c.type === "cd4051") rvNew = rvP * (((c.val || 0) % 8) + 1) / 8;
        else rvNew = rvP * ((c.val || 0) & 255) / 255;
        if (Math.abs(rvNew - devV[c.id]) > 0.002) { devV[c.id] = rvNew; changed = true; }
      } else if (c.type === "tda7297" || c.type === "opa2134" || c.type === "ad620" || c.type === "opa548" || c.type === "lm337" || c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017" || c.type === "ic_74hc00") {
        var zA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, zB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, zTh = vcc / 2, zNew = 0, zst, zHi;
        if (c.type === "tda7297") zNew = Math.max(0, Math.min(vcc, (zA - zB) * (c.val || 10) * 50));
        else if (c.type === "opa2134") zNew = Math.max(0, Math.min(vcc, (zA - zB) * 1000));
        else if (c.type === "ad620") zNew = Math.max(0, Math.min(vcc, (zA - zB) * (c.val || 100)));
        else if (c.type === "opa548") zNew = Math.max(0, Math.min(vcc, (zA - zB) * (c.val || 2) * 100));
        else if (c.type === "lm337") {
          var z337 = zA - zB, zReg = c.val || -5;
          zNew = z337 < zReg - 2.0 ? zReg : (z337 < -0.5 ? Math.min(0, z337 + 2.0) : 0);
        }
        else if (c.type === "cd4013") {
          zst = logicSt(c); if (zst.setVal !== c.val) { zst.q = c.val ? 1 : 0; zst.setVal = c.val; }
          zHi = zB > zTh;
          if (zst.hi === false && zHi) { zst.q = zA > zTh ? 1 : 0; changed = true; }
          zst.hi = zHi; zNew = zst.q ? vcc : 0;
        }
        else if (c.type === "cd4015") {
          zst = logicSt(c); if (zst.setVal !== c.val) { zst.bits = (c.val || 0) & 15; zst.setVal = c.val; }
          zHi = zB > zTh;
          if (zst.hi === false && zHi) { zst.bits = ((zst.bits << 1) | (zA > zTh ? 1 : 0)) & 15; changed = true; }
          zst.hi = zHi; zNew = (zst.bits & 8) ? vcc : 0;
        }
        else if (c.type === "ic_74hc273") {
          zst = logicSt(c); zHi = zB > zTh;
          if (zA <= zTh) { if (zst.reg !== 0) { zst.reg = 0; changed = true; } }
          else if (zst.hi === false && zHi) { zst.reg = c.val || 0; changed = true; }
          zst.hi = zHi; zNew = vcc * zst.reg / 255;
        }
        else if (c.type === "ic_74hc373") {
          zst = logicSt(c);
          if (zB > zTh) { var zLat = zA > zTh ? (c.val || 0) : 0; if (zst.latched !== zLat) { zst.latched = zLat; changed = true; } }
          zNew = vcc * zst.latched / 255;
        }
        else if (c.type === "at24c32") zNew = (zA > zTh && zB > zTh) ? vcc * (c.val || 0) / 255 : 0;
        else if (c.type === "mcp23017") {
          var zPop = 0, zV = (c.val || 0) & 65535; while (zV) { zPop += zV & 1; zV >>= 1; }
          zNew = (zA > zTh && zB > zTh) ? vcc * zPop / 16 : 0;
        }
        else zNew = (zA > zTh && zB > zTh) ? 0 : vcc;
        if (Math.abs(zNew - devV[c.id]) > 0.002) { devV[c.id] = zNew; changed = true; }
      } else if (SENSOR_SET[c.type]) {
        var svA = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, svB = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0;
        var svNew = sensorOut(c, vcc, svA - svB, animT || 0);
        if (Math.abs(svNew - devV[c.id]) > 0.002) { devV[c.id] = svNew; changed = true; }
      } else if (c.type.indexOf("gate_") === 0) {
        var ga = mi(c, "a") >= 0 ? x[mi(c, "a")] : 0, gb = mi(c, "b") >= 0 ? x[mi(c, "b")] : 0, th = vcc / 2, want;
        if (c.type === "gate_and") want = ga > th && gb > th;
        else if (c.type === "gate_or") want = ga > th || gb > th;
        else if (c.type === "gate_nand") want = !(ga > th && gb > th);
        else if (c.type === "gate_xor") want = (ga > th) !== (gb > th);
        else if (c.type === "gate_xnor") want = (ga > th) === (gb > th);
        else want = !(ga > th);
        if (want !== gateOut[c.id]) { gateOut[c.id] = want; changed = true; }
      } else if (c.type === "relay") {
        var rv = Math.abs((mi(c, "a") >= 0 ? x[mi(c, "a")] : 0) - (mi(c, "b") >= 0 ? x[mi(c, "b")] : 0));
        var ron = relayOn[c.id] ? rv > c.val * 0.4 : rv > c.val * 0.7;
        if (ron !== relayOn[c.id]) { relayOn[c.id] = ron; changed = true; }
      }
    });
    if (!changed) break;
  }

  function vOf(c, t) { var m = mi(c, t); return m >= 0 ? volt[m] : 0; }
  comps.forEach(function (c) {
    var va = vOf(c, "a"), vb = vOf(c, "b"), vd = va - vb, cur = 0;
    if (isSource(c)) cur = (srcV(c, timeSec) - vd) / R_BATT;
    else if (c.type === "resistor" || c.type === "bulb" || c.type === "motor" || c.type === "buzzer" || c.type === "ldr" || c.type === "inductor" || c.type === "speaker" || c.type === "thermistor") {
      var res = c.val;
      if (c.type === "ldr") res = ldrRes(c);
        else if (c.type === "inductor") res = 0.001;
        else if (c.type === "thermistor") res = c.val * (c.closed ? 0.1 : 10);
      if (res <= 0) res = 0.001;
      cur = vd / res;
    }
    else if (c.type === "potentiometer") {
      var rtp = c.val > 0.002 ? c.val : 0.002, ppp = potPos(c);
      cur = (va - vOf(c, "c")) / Math.max(rtp * ppp, 0.001);
    }
    else if (c.type === "relay") cur = vd / R_RELAY_COIL;
    else if (c.type === "fuse") cur = vd / 0.01;
    else if (c.type === "capacitor") cur = 0;
    else if (c.type === "switch") cur = c.closed ? vd / R_SW_ON : 0;
    else if (c.type === "led") { var vf = LED_COLORS[c.val] ? LED_COLORS[c.val].vf : 2; cur = ledOn[c.id] ? Math.max(0, (vd - vf) / R_LED) : 0; }
    else if (c.type === "diode" || c.type === "schottky") { cur = diodeOn[c.id] ? Math.max(0, (vd - diodeVf(c)) / 1.0) : 0; }
    else if (c.type === "zener") { cur = zenerSt[c.id] === 1 ? Math.max(0, (vd - 0.7) / 1.0) : (zenerSt[c.id] === -1 ? Math.min(0, (vd + c.val) / 1.0) : 0); }
    else if (c.type === "transistor") { cur = transOn[c.id] ? vd / R_TRANSISTOR : 0; }
    else if (c.type === "transistor_pnp") { cur = transOn[c.id] ? vd / R_TRANSISTOR : 0; }
    else if (c.type === "reg7805" || c.type === "reg7803") {
      cur = regSt[c.id] ? Math.max(0, (regTh[c.id] - (vOf(c, "c") - vb)) / 0.05) + vd / 2200 : 0;
    }
    else if (c.type === "opamp") { cur = ((opOut[c.id] ? vcc : 0) - vOf(c, "c")) / 0.05; }
    else if (c.type === "pir") { cur = pirActive[c.id] ? vd / 0.05 : 0; }
    else if (c.type === "dht11") { cur = vd / 10000; }
    else if (c.type === "seven_seg") { cur = vd / 500; }
    else if (c.type === "timer555") { cur = timer555V[c.id] > 0 ? ((timer555Out[c.id] ? timer555V[c.id] : 0) - (vOf(c, "c") - vb)) / 0.05 : 0; }
    else if (c.type === "mosfet_n") { cur = transOn[c.id] ? vd / 0.05 : 0; }
    else if (c.type === "lm317") { cur = regSt[c.id] ? Math.max(0, (regTh[c.id] - (vOf(c, "c") - vb)) / 0.05) + vd / 1500 : 0; }
    else if (c.type === "servo") { cur = servoOn[c.id] ? (vOf(c, "b") - vOf(c, "c")) / 40 : 0; }
    else if (c.type === "lcd_16x2" || c.type === "ds18b20") { cur = vd / 100000; }
    else if (c.type === "hc_sr04") { cur = vd / 200; }
    else if (c.type === "stepper_motor") { cur = vd / (c.val > 0 ? c.val * 0.05 : 10); }
    else if (c.type === "rgb_led") { cur = ledOn[c.id] ? Math.max(0, (vd - 2.5) / R_LED) : 0; }
    else if (c.type === "varistor") { cur = movSt[c.id] === 0 ? vd / 1e7 : (vd - movSt[c.id] * c.val) / 10; }
    else if (c.type === "oled_ssd1306") { cur = vd / 100000; }
    else if (c.type === "seven_seg_4") { cur = vd / 800; }
    else if (c.type === "l293d") { cur = vd / 5000; }
    else if (c.type === "hc595") { cur = vd / 50000; }
    else if (c.type === "ds3231") { cur = vd / 100000; }
    else if (c.type === "optocoupler") { cur = devV[c.id] > 0 ? Math.max(0, (vd - 1.2) / 50) : vd / 1e7; }
    else if (c.type === "lm386" || c.type === "lm358" || c.type === "ne5532" || c.type === "lm393" || c.type === "cd4017" || c.type === "ic_74hc138") { cur = vd / 50000; }
    else if (c.type === "lm1117") { cur = vd / 5000; }
    else if (c.type === "uln2003") { cur = vd / 100000; }
    else if (c.type === "tl072" || c.type === "lm324" || c.type === "ne556" || c.type === "lm3914") { cur = vd / 50000; }
    else if (c.type === "tda2030") { cur = vd / 100000; }
    else if (c.type === "lm2596") { cur = vd / 3000; }
    else if (c.type === "tp4056" || c.type === "dac0808" || c.type === "max7219") { cur = vd / 50000; }
    else if (c.type === "lm741") { cur = vd / 2000000; }
    else if (c.type === "ne5534") { cur = vd / 500000; }
    else if (c.type === "tda2822") { cur = vd / 200000; }
    else if (c.type === "cd4051") { cur = vd / 100000; }
    else if (c.type === "pcf8574") { cur = vd / 50000; }
    else if (c.type === "cd4066") { cur = c.val === "closed" ? vd / 15 : vd / 1e7; }
    else if (c.type === "tda7297" || c.type === "opa548") { cur = vd / 100000; }
    else if (c.type === "opa2134") { cur = vd / 300000; }
    else if (c.type === "ad620") { cur = vd / 10000000; }
    else if (c.type === "lm337") { cur = vd / 5000; }
    else if (c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017" || c.type === "ic_74hc00") { cur = 0.0003; }
    else if (c.type === "adc0804") { cur = vd / 1000000; }
    if (SENSOR_SET[c.type]) cur = vd / 100000;
    if (c.type === "ws2812") cur = ledOn[c.id] ? Math.max(0, (vd - 2.5) / R_LED) : 0;

    out.V[c.id] = vd; out.I[c.id] = cur; out.P[c.id] = Math.abs(vd * cur);
    if (Math.abs(cur) < 1e-12) out.I[c.id] = 0;
  });
  out.ledOn = ledOn; out.diodeOn = diodeOn; out.transOn = transOn; out.gateOut = gateOut; out.relayOn = relayOn; out.timer555On = timer555Out; out.servoOn = servoOn; out.devV = devV;
  out.nodeV = function (key) { var node = nm.node[key]; if (node === undefined) return 0; var m = map[node]; return m >= 0 ? volt[m] : 0; };
  out.ok = true;

  var anyCurrent = false;
  comps.forEach(function (c) {
    var i = Math.abs(out.I[c.id]);
    if ((isSource(c)) && i > 0.01) anyCurrent = true;
    if (regSt[c.id]) anyCurrent = true;
    if ((isSource(c)) && i > 2) out.warnings.push({ k: "short", id: c.id });
    if ((c.type === "led" || c.type === "rgb_led") && i > 0.030) out.warnings.push({ k: "ledburn", id: c.id });
    if (c.type === "resistor" && out.P[c.id] > 0.25) out.warnings.push({ k: "hot", id: c.id });
    if (c.type === "fuse" && i > c.val) out.warnings.push({ k: "fuse_blow", id: c.id, val: c.val });
  });
  out.anyCurrent = anyCurrent;
  return out;
}

function measureResistance(keyA, keyB) {
  if (!keyA || !keyB || keyA === keyB) return 0;
  var testComps = comps.map(function (c) { return { id: c.id, type: c.type, x: c.x, y: c.y, rot: c.rot, val: c.val, closed: c.closed, pos: c.pos }; });
  var seen = {}; testComps.forEach(function (c) { seen[c.id] = true; });
  var bid = "M1", n = 1;
  while (seen[bid]) { n++; bid = "M" + n; }
  testComps.push({ id: bid, type: "battery", val: 1, x: 0, y: 0, rot: 0, closed: true });
  var testWires = wires.map(function (w) { return { a: w.a, b: w.b }; });
  testWires.push({ a: bid + ".a", b: keyA });
  testWires.push({ a: bid + ".b", b: keyB });
  var s = simulate(testComps, testWires, 0);
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
  if (ALIAS[c.type]) c = aliasView(c);
  if (c.type === "ac_source") return c.val + "V AC";
  if (c.type === "relay") return c.val + "V" + (sim && sim.ok && sim.relayOn && sim.relayOn[c.id] ? " ●" : "");
  if (isSource(c)) return c.val + "V";
  if (c.type === "resistor" || c.type === "bulb" || c.type === "motor" || c.type === "buzzer") return fmtR(c.val);
  if (c.type === "potentiometer") return fmtR(c.val) + " @" + Math.round(potPos(c) * 100) + "%";
  if (c.type === "ldr") return (c.closed ? t("مظلم","Dark") : t("مضيء","Light")) + " (" + fmtR(ldrRes(c)) + ")";
  if (c.type === "capacitor") return fmtC(c.val);
  if (c.type === "fuse") return c.val + "A";
  if (c.type === "diode") return AR ? (c.val === "silicon" ? "سيليكون" : "جرمانيوم") : c.val;
  if (c.type === "transistor") return "NPN";
  if (c.type === "led") { var lc = LED_COLORS[c.val]; return lc ? (AR ? lc.ar : lc.en) : ""; }
  if (c.type === "inductor") return c.val + " mH";
  if (c.type === "thermistor") return fmtR(c.val * (c.closed ? 0.1 : 10));
  if (c.type === "speaker") return c.val + "Ω";
  if (c.type === "zener") return c.val + "V";
  if (c.type === "schottky") return String(c.val);
  if (c.type === "solar" || c.type === "dc_jack" || c.type === "nano" || c.type === "mega" || c.type === "esp8266" || c.type === "pico") return c.val + "V";
  if (c.type === "reg7805" || c.type === "reg7803") return c.val + "V out";
  if (c.type === "opamp") return String(c.val);
  if (c.type === "transistor_pnp") return "PNP";
  if (c.type === "pir") return c.closed ? t("حركة", "Motion") : t("ساكن", "Still");
  if (c.type === "dht11") return c.val + "°C";
  if (c.type === "seven_seg") return "→ " + c.val;
  if (c.type === "timer555") return c.val + "Hz" + (sim && sim.ok && sim.timer555On && sim.timer555On[c.id] ? " ●" : "");
  if (c.type === "mosfet_n") return String(c.val);
  if (c.type === "lm317") return c.val + "V out";
  if (c.type === "servo") return c.val + "°";
  if (c.type === "lcd_16x2") return String(c.val);
  if (c.type === "hc_sr04") return c.val + "cm";
  if (c.type === "ds18b20") return Number(c.val).toFixed(1) + "°C";
  if (c.type === "stepper_motor") return c.val + " st/rev";
  if (c.type === "rgb_led") return String(c.val);
  if (c.type === "varistor") return c.val + "V";
  if (c.type === "tda7297") return "×" + c.val + "W";
  if (c.type === "opa2134") return "OPA2134";
  if (c.type === "ad620") return "×" + c.val;
  if (c.type === "opa548") return c.val + "A";
  if (c.type === "lm337") return c.val + "V";
  if (c.type === "cd4013") return "Q=" + (icState(c) ? icState(c).q : c.val);
  if (c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "mcp23017") return "0x" + Number(c.val).toString(16).toUpperCase();
  if (c.type === "at24c32") return "byte " + c.val;
  if (c.type === "ic_74hc00") return "74HC00";
  if (c.type === "lm741") return "LM741";
  if (c.type === "ne5534") return "NE5534";
  if (c.type === "tda2822") return "×" + c.val + "W stereo";
  if (c.type === "cd4051") return "CH" + c.val;
  if (c.type === "pcf8574") return "0x" + Number(c.val || 0).toString(16).toUpperCase().padStart(2, "0");
  if (c.type === "cd4066") return String(c.val);
  if (c.type === "tda2030") return "×" + c.val;
  if (c.type === "lm2596") return c.val + "V out";
  if (c.type === "tp4056") return c.val + "% " + (c.val < 100 ? t("يشحن", "charging") : t("ممتلئ", "full"));
  if (c.type === "adc0804") return "0-" + c.val + "V";
  if (c.type === "dac0808") return "0x" + Number(c.val).toString(16).toUpperCase().padStart(2, "0");
  if (c.type === "max7219") return String(c.val).padStart(4, "0");
  if (c.type === "tl072") return "TL072";
  if (c.type === "lm324") return "LM324 (×4)";
  if (c.type === "ne556") return c.val + "Hz (×2)";
  if (c.type === "uln2003") return "ULN2003 (×7)";
  if (c.type === "lm1117") return c.val + "V out";
  if (c.type === "lm3914") return c.val + "V range";
  if (c.type === "lm386") return "×" + c.val;
  if (c.type === "lm358" || c.type === "ne5532" || c.type === "lm393") return String(c.val);
  if (c.type === "cd4017") return "Q" + (cntState[c.id] ? cntState[c.id].step : c.val);
  if (c.type === "ic_74hc138") return "Y" + c.val;
  if (c.type === "oled_ssd1306" || c.type === "l293d" || c.type === "optocoupler") return String(c.val);
  if (c.type === "seven_seg_4") return String(c.val).padStart(2, "0");
  if (c.type === "hc595") return "0x" + (c.val || 1).toString(16).toUpperCase();
  if (c.type === "ds3231") return String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00";
  if (c.type === "mpu6050") return String(c.val);
  if (c.type === "bmp280")  return c.val + " hPa";
  if (c.type === "acs712")  return "±" + c.val + "A";
  if (c.type === "a3144")   return c.closed ? t("مغناطيس", "MAG") : t("لا شيء", "none");
  if (c.type === "ky038")   return "L" + c.val;
  if (c.type === "yl69")    return c.val + "%";
  if (c.type === "ttp223")  return c.closed ? t("مُلامس", "TOUCH") : t("ساكن", "idle");
  if (c.type === "ky040")   return c.val + "°";
  if (c.type === "ws2812")  return String(c.val);
  if (c.type === "tsop")    return c.closed ? t("مستلم", "IR") : t("صامت", "silent");
  if (c.type === "hc05")    return String(c.val);
  if (c.type === "l298n")   return String(c.val);
  if (c.type === "a4988")    return String(c.val);
  if (c.type === "pam8403")  return "×" + c.val + "W";
  if (c.type === "max98357") return "×" + c.val + "W";
  if (c.type === "ads1115")  return "0x" + Number(c.val).toString(16).toUpperCase().padStart(4, "0");
  if (c.type === "mcp4725")  return "0x" + Number(c.val).toString(16).toUpperCase().padStart(3, "0");
  if (c.type === "ina219")   return c.val + "mA";
  if (c.type === "mq2")      return String(c.val);
  if (c.type === "bh1750")   return c.val + "lx";
  if (c.type === "vl53l0x")  return c.val + "mm";
  if (c.type === "ic_74hc165") return "0x" + Number(c.val).toString(16).toUpperCase().padStart(2, "0");
  if (c.type === "nrf24l01") return String(c.val);
  if (c.type === "sim800l")  return String(c.val);
  if (c.type === "drv8825")  return String(c.val);
  if (c.type === "tb6612")   return String(c.val);
  if (c.type === "bts7960")  return String(c.val);
  if (c.type === "tcs34725") return String(c.val);
  if (c.type === "mlx90614") return Number(c.val).toFixed(1) + "°C";
  if (c.type === "max30102") return c.val + "bpm";
  if (c.type === "adxl345")  return String(c.val);
  if (c.type === "hx711")    return c.val + "g";
  if (c.type === "dht22")    return c.val + "°C";
  if (c.type === "sgp30")    return c.val + "ppm";
  if (c.type === "rc522")    return String(c.val);
  if (c.type === "bme680")   return c.val + " IAQ";
  if (c.type === "pca9685")  return c.val + "%";
  if (c.type === "tca9548a") return "CH" + c.val;
  if (c.type === "l9110s")   return String(c.val);
  if (c.type === "tmp36")    return c.val + "°C";
  if (c.type === "am2320")   return c.val + "%RH";
  if (c.type === "ds1307")   return String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00";
  if (c.type === "pcf8563")  return String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00";
  if (c.type === "st7735")   return String(c.val);
  if (c.type === "ssd1351")  return String(c.val);
  if (c.type === "bmp180")   return c.val + " hPa";
  if (c.type === "sht31")    return c.val + "°C";
  if (c.type === "apds9960") return String(c.val);
  if (c.type === "ds1302")   return String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00";
  if (c.type === "max6675")  return Math.round(c.val / 4) + "°C";
  if (c.type === "max31855") return c.val + "°C";
  if (c.type === "sd_card")  return String(c.val);
  if (c.type === "enc28j60") return String(c.val);
  if (c.type === "uln2803")  return c.val + "/8 CH";
  if (c.type === "tlc5940")  return c.val + "%";
  if (c.type === "mpu9250")  return String(c.val);
  if (c.type === "ad9833")   return (c.val >= 1000 ? (c.val / 1000) + "kHz" : c.val + "Hz");
  if (c.type === "ams1117")  return c.val + "V out";
  if (c.type === "xl6009")   return c.val + "V out";
  if (c.type === "vl6180x")  return c.val + "mm";
  if (c.type === "sht10") return c.val + "°C";
  if (c.type === "sht75") return c.val + "°C";
  if (c.type === "si7021") return c.val + "%";
  if (c.type === "bme280") return c.val + " hPa";
  if (c.type === "mpl3115a2") return c.val + " hPa";
  if (c.type === "mq3") return c.val + " ppm";
  if (c.type === "mq4") return c.val + " ppm";
  if (c.type === "mq5") return c.val + " ppm";
  if (c.type === "mq6") return c.val + " ppm";
  if (c.type === "mq7") return c.val + " ppm";
  if (c.type === "mq8") return c.val + " ppm";
  if (c.type === "mq9") return c.val + " ppm";
  if (c.type === "mq135") return c.val + " ppm";
  if (c.type === "gp2y1010") return c.val + " ppm";
  if (c.type === "tsl2561") return c.val + " lx";
  if (c.type === "tcs3200") return String(c.val);
  if (c.type === "reed_switch") return c.closed ? t("نشط", "ON") : t("ساكن", "OFF");
  if (c.type === "vibration_sensor") return c.closed ? t("نشط", "ON") : t("ساكن", "OFF");
  if (c.type === "water_level") return c.val + "%";
  if (c.type === "flex_sensor") return c.val + "%";
  if (c.type === "tilt_switch") return c.closed ? t("نشط", "ON") : t("ساكن", "OFF");
  if (c.type === "shock_sensor") return c.closed ? t("نشط", "ON") : t("ساكن", "OFF");
  if (c.type === "flame_sensor") return c.val + " ppm";
  if (c.type === "rain_sensor") return c.val + "%";
  if (c.type === "hall_linear") return c.closed ? t("نشط", "ON") : t("ساكن", "OFF");
  if (c.type === "cd4071") return String(c.val);
  if (c.type === "cd4081") return String(c.val);
  if (c.type === "cd4030") return String(c.val);
  if (c.type === "cd4001") return String(c.val);
  if (c.type === "cd4023") return String(c.val);
  if (c.type === "cd4025") return String(c.val);
  if (c.type === "cd4070") return String(c.val);
  if (c.type === "cd4075") return String(c.val);
  if (c.type === "cd4077") return String(c.val);
  if (c.type === "cd4093") return String(c.val);
  if (c.type === "cd4538") return String(c.val);
  if (c.type === "cd4047") return String(c.val);
  if (c.type === "cd4027") return String(c.val);
  if (c.type === "cd4029") return String(c.val);
  if (c.type === "cd4076") return String(c.val);
  if (c.type === "cd4022") return String(c.val);
  if (c.type === "cd4060") return String(c.val);
  if (c.type === "cd4541") return String(c.val);
  if (c.type === "cd4511") return String(c.val);
  if (c.type === "cd4028") return String(c.val);
  if (c.type === "mcp3008") return String(c.val);
  if (c.type === "mcp3208") return String(c.val);
  if (c.type === "ads1015") return String(c.val);
  if (c.type === "pcf8591") return String(c.val);
  if (c.type === "tlc5615") return String(c.val);
  if (c.type === "mcp4921") return String(c.val);
  if (c.type === "at24c256") return String(c.val);
  if (c.type === "at24c512") return String(c.val);
  if (c.type === "w25q64") return String(c.val);
  if (c.type === "mb85rc") return String(c.val);
  if (c.type === "ds3234") return String(c.val);
  if (c.type === "rv3028") return String(c.val);
  if (c.type === "mcp7940") return String(c.val);
  if (c.type === "nokia5110") return String(c.val);
  if (c.type === "ssd1309") return String(c.val);
  if (c.type === "st7565") return String(c.val);
  if (c.type === "st7920") return String(c.val);
  if (c.type === "ili9341") return String(c.val);
  if (c.type === "ili9486") return String(c.val);
  if (c.type === "max6954") return String(c.val);
  if (c.type === "lcd_20x4") return String(c.val);
  if (c.type === "st7735_160") return String(c.val);
  if (c.type === "ssd1331") return String(c.val);
  if (c.type === "drv8833") return String(c.val);
  if (c.type === "drv8871") return String(c.val);
  if (c.type === "l293e") return String(c.val);
  if (c.type === "sn754410") return String(c.val);
  if (c.type === "uln2004") return String(c.val);
  if (c.type === "mc33926") return String(c.val);
  if (c.type === "bd6221") return String(c.val);
  if (c.type === "tb67h420") return String(c.val);
  if (c.type === "a3959") return String(c.val);
  if (c.type === "drv8824") return String(c.val);
  if (c.type === "esp01") return String(c.val);
  if (c.type === "rn2483") return String(c.val);
  if (c.type === "rfm69") return String(c.val);
  if (c.type === "rfm95") return String(c.val);
  if (c.type === "hc12") return String(c.val);
  if (c.type === "xbee") return String(c.val);
  if (c.type === "sim900") return String(c.val);
  if (c.type === "m95") return String(c.val);
  if (c.type === "nrf905") return String(c.val);
  if (c.type === "cc1101") return String(c.val);
  if (c.type === "lm7809") return c.val + "V out";
  if (c.type === "lm7812") return c.val + "V out";
  if (c.type === "lm7905") return c.val + "V out";
  if (c.type === "lm7912") return c.val + "V out";
  if (c.type === "lm1084") return c.val + "V out";
  if (c.type === "lm2678") return c.val + "V out";
  if (c.type === "lm5007") return c.val + "V out";
  if (c.type === "mcp1700") return c.val + "V out";
  if (c.type === "mic5205") return c.val + "V out";
  if (c.type === "lp2985") return c.val + "V out";
  if (c.type === "lm4871") return String(c.val);
  if (c.type === "tda2003") return String(c.val);
  if (c.type === "ds18s20") return c.val + "°C";
  if (c.type === "lm35") return c.val + "°C";
  if (c.type === "lm75") return c.val + "°C";
  if (c.type === "tmp102") return c.val + "°C";
  if (c.type === "mcp9808") return c.val + "°C";
  if (c.type === "max31865") return c.val + "°C";
  if (c.type === "ads1118") return c.val + "°C";
  if (c.type === "hdc1080") return c.val + "%";
  if (c.type === "htu21d") return c.val + "%";
  if (c.type === "sht21") return c.val + "%";
  if (c.type === "sht35") return c.val + "%";
  if (c.type === "aht10") return c.val + "%";
  if (c.type === "aht20") return c.val + "%";
  if (c.type === "ms5611") return c.val + "hPa";
  if (c.type === "lps25h") return c.val + "hPa";
  if (c.type === "bmp388") return c.val + "hPa";
  if (c.type === "dps310") return c.val + "hPa";
  if (c.type === "bmp085") return c.val + "hPa";
  if (c.type === "lps22hb") return c.val + "hPa";
  if (c.type === "mpx5700") return c.val + "hPa";
  if (c.type === "mq131") return c.val + "ppm";
  if (c.type === "mq303") return c.val + "ppm";
  if (c.type === "mhz19") return c.val + "ppm";
  if (c.type === "sds011") return c.val + "µg";
  if (c.type === "pms5003") return c.val + "µg";
  if (c.type === "ccs811") return c.val + "ppb";
  if (c.type === "ens160") return c.val + "ppb";
  if (c.type === "si1145") return c.val + "lux";
  if (c.type === "veml7700") return c.val + "lux";
  if (c.type === "opt3001") return c.val + "lux";
  if (c.type === "max44009") return c.val + "lux";
  if (c.type === "ltr329") return c.val + "lux";
  if (c.type === "ml8511") return c.val + "UVI";
  if (c.type === "veml6070") return c.val + "UVI";
  if (c.type === "ina226") return c.val + "V";
  if (c.type === "ina260") return c.val + "V";
  if (c.type === "ina3221") return c.val + "V";
  if (c.type === "lis3dh") return c.val + "g";
  if (c.type === "mma8452") return c.val + "g";
  if (c.type === "adxl335") return c.val + "g";
  if (c.type === "adxl362") return c.val + "g";
  if (c.type === "lsm6ds3") return c.val + "g";
  if (c.type === "icm20948") return c.val + "g";
  if (c.type === "bno055") return c.val + "g";
  if (c.type === "hmc5883l") return c.val + "µT";
  if (c.type === "qmc5883l") return c.val + "µT";
  if (c.type === "mlx90393") return c.val + "µT";
  if (c.type === "lm7815") return c.val + "V out";
  if (c.type === "lm7824") return c.val + "V out";
  if (c.type === "lm7808") return c.val + "V out";
  if (c.type === "lm7806") return c.val + "V out";
  if (c.type === "lm317hv") return c.val + "V out";
  if (c.type === "lm2940") return c.val + "V out";
  if (c.type === "tps7a47") return c.val + "V out";
  if (c.type === "lm2576") return c.val + "V out";
  if (c.type === "lm2574") return c.val + "V out";
  if (c.type === "mp1584") return c.val + "V out";
  if (c.type === "tps5430") return c.val + "V out";
  if (c.type === "mt3608") return c.val + "V out";
  if (c.type === "lm2577") return c.val + "V out";
  if (c.type === "tps61023") return c.val + "V out";
  if (c.type === "max1771") return c.val + "V out";
  if (c.type === "lm3886") return c.val + "W";
  if (c.type === "tda7294") return c.val + "W";
  if (c.type === "tda2050") return c.val + "W";
  if (c.type === "tda7377") return c.val + "W";
  if (c.type === "tpa3116") return c.val + "W";
  if (c.type === "tpa2005") return c.val + "W";
  if (c.type === "lm4766") return c.val + "W";
  if (c.type === "drv8434") return String(c.val);
  if (c.type === "tmc2209") return String(c.val);
  if (c.type === "tmc2130") return String(c.val);
  if (c.type === "l6470") return String(c.val);
  if (c.type === "vnh5019") return String(c.val);
  if (c.type === "drv8313") return String(c.val);
  if (c.type === "a4950") return String(c.val);
  if (c.type === "mx1508") return String(c.val);
  if (c.type === "esp32cam") return String(c.val);
  if (c.type === "sx1278") return String(c.val);
  if (c.type === "sx1276") return String(c.val);
  if (c.type === "nrf52832") return String(c.val);
  if (c.type === "hm10") return String(c.val);
  if (c.type === "jdy23") return String(c.val);
  if (c.type === "ublox_neo6m") return String(c.val);
  if (c.type === "ublox_neo7m") return String(c.val);
  if (c.type === "w5500") return String(c.val);
  if (c.type === "cp2102") return String(c.val);
  if (c.type === "ch340") return String(c.val);
  if (c.type === "max485") return String(c.val);
  if (c.type === "mcp2515") return String(c.val);
  if (c.type === "ssd1322") return String(c.val);
  if (c.type === "ssd1327") return String(c.val);
  if (c.type === "ssd1306_64") return String(c.val);
  if (c.type === "st7789") return String(c.val);
  if (c.type === "ili9488") return String(c.val);
  if (c.type === "hd44780") return String(c.val);
  if (c.type === "tm1637") return String(c.val);
  if (c.type === "ht16k33") return String(c.val);
  if (c.type === "cd4017b") return String(c.val);
  if (c.type === "ic_74hc14") return String(c.val);
  if (c.type === "ic_74hc04") return String(c.val);
  if (c.type === "ic_74hc08") return String(c.val);
  if (c.type === "ic_74hc32") return String(c.val);
  if (c.type === "ic_74hc86") return String(c.val);
  if (c.type === "ic_74hc74") return String(c.val);
  if (c.type === "ic_74hc590") return String(c.val);
  if (c.type === "ic_74hc4067") return String(c.val);
  if (c.type === "at24c64") return String(c.val);
  if (c.type === "at24c128") return String(c.val);
  if (c.type === "w25q128") return String(c.val);
  if (c.type === "fm25v02") return String(c.val);
  if (c.type === "mcp23s17") return String(c.val);
  if (c.type === "tca9534") return String(c.val);
  if (c.type === "max7301") return String(c.val);
  if (c.type === "tmp117") return c.val + "°C";
  if (c.type === "max30205") return c.val + "°C";
  if (c.type === "amg8833") return c.val + "°C";
  if (c.type === "mlx90640") return c.val + "°C";
  if (c.type === "lm73") return c.val + "°C";
  if (c.type === "si7050") return c.val + "°C";
  if (c.type === "ds28ea00") return c.val + "°C";
  if (c.type === "ad8495") return c.val + "°C";
  if (c.type === "hih6130") return c.val + "%";
  if (c.type === "dht21") return c.val + "%";
  if (c.type === "sht40") return c.val + "%";
  if (c.type === "sht45") return c.val + "%";
  if (c.type === "hdc2080") return c.val + "%";
  if (c.type === "bme688") return c.val + "%";
  if (c.type === "bmp390") return c.val + "hPa";
  if (c.type === "bmp581") return c.val + "hPa";
  if (c.type === "lps35hw") return c.val + "hPa";
  if (c.type === "lps33hw") return c.val + "hPa";
  if (c.type === "spl06") return c.val + "hPa";
  if (c.type === "ms5837") return c.val + "hPa";
  if (c.type === "mq137") return c.val + "ppm";
  if (c.type === "mq138") return c.val + "ppm";
  if (c.type === "mq214") return c.val + "ppm";
  if (c.type === "mq216") return c.val + "ppm";
  if (c.type === "scd30") return c.val + "ppm";
  if (c.type === "scd40") return c.val + "ppm";
  if (c.type === "scd41") return c.val + "ppm";
  if (c.type === "sgp40") return c.val + "ppm";
  if (c.type === "sen54") return c.val + "ppm";
  if (c.type === "ags02ma") return c.val + "ppm";
  if (c.type === "as7341") return c.val + "lux";
  if (c.type === "as7262") return c.val + "lux";
  if (c.type === "tsl2591") return c.val + "lux";
  if (c.type === "veml6075") return c.val + "lux";
  if (c.type === "guva_s12sd") return c.val + "lux";
  if (c.type === "bh1745") return c.val + "lux";
  if (c.type === "isl29125") return c.val + "lux";
  if (c.type === "apds9306") return c.val + "lux";
  if (c.type === "mpu6500") return c.val + "g";
  if (c.type === "lsm9ds1") return c.val + "g";
  if (c.type === "lsm303") return c.val + "g";
  if (c.type === "l3gd20h") return c.val + "g";
  if (c.type === "bmi160") return c.val + "g";
  if (c.type === "bmi270") return c.val + "g";
  if (c.type === "adxl375") return c.val + "g";
  if (c.type === "icm42688") return c.val + "g";
  if (c.type === "lis2dh12") return c.val + "g";
  if (c.type === "kxtj3") return c.val + "g";
  if (c.type === "vl53l1x") return c.val + "cm";
  if (c.type === "gp2y0a21") return c.val + "cm";
  if (c.type === "gp2y0a02") return c.val + "cm";
  if (c.type === "us100") return c.val + "cm";
  if (c.type === "a02yyuw") return c.val + "cm";
  if (c.type === "ld2410") return c.val + "cm";
  if (c.type === "rcwl0516") return c.val + "cm";
  if (c.type === "tfmini") return c.val + "cm";
  if (c.type === "tf_luna") return c.val + "cm";
  if (c.type === "vcnl4040") return c.val + "cm";
  if (c.type === "jsn_sr04t") return c.val + "cm";
  if (c.type === "max30100") return c.val + "BPM";
  if (c.type === "ad8232") return c.val + "BPM";
  if (c.type === "pulse_sensor") return c.val + "BPM";
  if (c.type === "gsr_sensor") return c.val + "BPM";
  if (c.type === "r307") return c.val + "BPM";
  if (c.type === "ina169") return c.val + "A";
  if (c.type === "acs758") return c.val + "A";
  if (c.type === "max471") return c.val + "A";
  if (c.type === "pzem004t") return c.val + "A";
  if (c.type === "hlw8012") return c.val + "A";
  if (c.type === "ina228") return c.val + "A";
  if (c.type === "ina238") return c.val + "A";
  if (c.type === "ss49e") return c.val + "µT";
  if (c.type === "a1302") return c.val + "µT";
  if (c.type === "drv5053") return c.val + "µT";
  if (c.type === "as5600") return c.val + "µT";
  if (c.type === "as5048a") return c.val + "µT";
  if (c.type === "sh1106") return String(c.val);
  if (c.type === "ssd1305") return String(c.val);
  if (c.type === "gc9a01") return String(c.val);
  if (c.type === "st7796") return String(c.val);
  if (c.type === "ili9225") return String(c.val);
  if (c.type === "ssd1963") return String(c.val);
  if (c.type === "epd_154") return String(c.val);
  if (c.type === "epd_213") return String(c.val);
  if (c.type === "epd_29") return String(c.val);
  if (c.type === "lcd_12864") return String(c.val);
  if (c.type === "lcd_16x4") return String(c.val);
  if (c.type === "lcd_8x2") return String(c.val);
  if (c.type === "tm1638") return String(c.val);
  if (c.type === "ht1621") return String(c.val);
  if (c.type === "drv8847") return String(c.val);
  if (c.type === "drv8880") return String(c.val);
  if (c.type === "tmc2208") return String(c.val);
  if (c.type === "tmc2160") return String(c.val);
  if (c.type === "tmc5160") return String(c.val);
  if (c.type === "l6208") return String(c.val);
  if (c.type === "l6235") return String(c.val);
  if (c.type === "vnh2sp30") return String(c.val);
  if (c.type === "ibt2") return String(c.val);
  if (c.type === "lv8548") return String(c.val);
  if (c.type === "lm7818") return c.val + "V out";
  if (c.type === "lm78l05") return c.val + "V out";
  if (c.type === "lm79l05") return c.val + "V out";
  if (c.type === "lm317l") return c.val + "V out";
  if (c.type === "lm350") return c.val + "V out";
  if (c.type === "ld1117") return c.val + "V out";
  if (c.type === "xc6206") return c.val + "V out";
  if (c.type === "ap2112") return c.val + "V out";
  if (c.type === "tlv1117") return c.val + "V out";
  if (c.type === "lt3045") return c.val + "V out";
  if (c.type === "lm2575") return c.val + "V out";
  if (c.type === "lm2595") return c.val + "V out";
  if (c.type === "xl4015") return c.val + "V out";
  if (c.type === "xl4005") return c.val + "V out";
  if (c.type === "xl7005") return c.val + "V out";
  if (c.type === "mp2307") return c.val + "V out";
  if (c.type === "mp2315") return c.val + "V out";
  if (c.type === "tps54331") return c.val + "V out";
  if (c.type === "sx1308") return c.val + "V out";
  if (c.type === "cn3791") return c.val + "V out";
  if (c.type === "bq24074") return c.val + "V out";
  if (c.type === "tp5100") return c.val + "V out";
  if (c.type === "ip5306") return c.val + "V out";
  if (c.type === "esp32_c3") return String(c.val);
  if (c.type === "esp32_s3") return String(c.val);
  if (c.type === "nrf52840") return String(c.val);
  if (c.type === "hc06") return String(c.val);
  if (c.type === "hm11") return String(c.val);
  if (c.type === "jdy31") return String(c.val);
  if (c.type === "e32") return String(c.val);
  if (c.type === "sx1262") return String(c.val);
  if (c.type === "dw1000") return String(c.val);
  if (c.type === "pn532") return String(c.val);
  if (c.type === "w5100") return String(c.val);
  if (c.type === "enc424j600") return String(c.val);
  if (c.type === "mcp2551") return String(c.val);
  if (c.type === "tja1050") return String(c.val);
  if (c.type === "sn65hvd230") return String(c.val);
  if (c.type === "max232") return String(c.val);
  if (c.type === "max3232") return String(c.val);
  if (c.type === "ft232") return String(c.val);
  if (c.type === "pl2303") return String(c.val);
  if (c.type === "cp2104") return String(c.val);
  if (c.type === "l76k") return String(c.val);
  if (c.type === "neo_m8n") return String(c.val);
  if (c.type === "sim7600") return String(c.val);
  if (c.type === "sim868") return String(c.val);
  if (c.type === "a7670") return String(c.val);
  if (c.type === "ic_74hc02") return String(c.val);
  if (c.type === "ic_74hc10") return String(c.val);
  if (c.type === "ic_74hc20") return String(c.val);
  if (c.type === "ic_74hc30") return String(c.val);
  if (c.type === "ic_74hc125") return String(c.val);
  if (c.type === "ic_74hc157") return String(c.val);
  if (c.type === "ic_74hc151") return String(c.val);
  if (c.type === "ic_74hc139") return String(c.val);
  if (c.type === "ic_74hc154") return String(c.val);
  if (c.type === "ic_74hc161") return String(c.val);
  if (c.type === "ic_74hc164") return String(c.val);
  if (c.type === "ic_74hc166") return String(c.val);
  if (c.type === "ic_74hc174") return String(c.val);
  if (c.type === "ic_74hc175") return String(c.val);
  if (c.type === "ic_74hc193") return String(c.val);
  if (c.type === "ic_74hc244") return String(c.val);
  if (c.type === "ic_74hc245") return String(c.val);
  if (c.type === "ic_74hc283") return String(c.val);
  if (c.type === "ic_74hc374") return String(c.val);
  if (c.type === "ic_74hc4040") return String(c.val);
  if (c.type === "ic_74hc4046") return String(c.val);
  if (c.type === "ic_74hc4053") return String(c.val);
  if (c.type === "ic_74hc4094") return String(c.val);
  if (c.type === "mcp23008") return String(c.val);
  if (c.type === "tca9535") return String(c.val);
  if (c.type === "txs0108") return String(c.val);
  if (c.type === "sn74lvc245") return String(c.val);
  if (c.type === "at24c02") return String(c.val);
  if (c.type === "at24c08") return String(c.val);
  if (c.type === "at24c16") return String(c.val);
  if (c.type === "lm1875") return c.val + "W";
  if (c.type === "tda2040") return c.val + "W";
  if (c.type === "tda7498") return c.val + "W";
  if (c.type === "tpa3110") return c.val + "W";
  if (c.type === "pam8610") return c.val + "W";
  if (c.type === "pam8302") return c.val + "W";
  if (c.type === "max9744") return c.val + "W";
  if (c.type === "mcp6002") return c.val + "x";
  if (c.type === "mcp6022") return c.val + "x";
  if (c.type === "tl082") return c.val + "x";
  if (c.type === "tl084") return c.val + "x";
  if (c.type === "lf353") return c.val + "x";
  if (c.type === "lf411") return c.val + "x";
  if (c.type === "op07") return c.val + "x";
  if (c.type === "op27") return c.val + "x";
  if (c.type === "ad8605") return c.val + "x";
  if (c.type === "tmp116") return c.val + "°C";
  if (c.type === "tmp1075") return c.val + "°C";
  if (c.type === "max6633") return c.val + "°C";
  if (c.type === "mcp9701") return c.val + "°C";
  if (c.type === "lm19") return c.val + "°C";
  if (c.type === "lm34") return c.val + "°C";
  if (c.type === "lm335") return c.val + "°C";
  if (c.type === "ad590") return c.val + "°C";
  if (c.type === "tmp35") return c.val + "°C";
  if (c.type === "tmp37") return c.val + "°C";
  if (c.type === "sts31") return c.val + "°C";
  if (c.type === "stlm20") return c.val + "°C";
  if (c.type === "sht85") return c.val + "%";
  if (c.type === "hih7130") return c.val + "%";
  if (c.type === "hts221") return c.val + "%";
  if (c.type === "hdc3020") return c.val + "%";
  if (c.type === "shtc3") return c.val + "%";
  if (c.type === "shtc1") return c.val + "%";
  if (c.type === "si7020") return c.val + "%";
  if (c.type === "am2301") return c.val + "%";
  if (c.type === "am2302") return c.val + "%";
  if (c.type === "capacitive_soil") return c.val + "%";
  if (c.type === "fc28") return c.val + "%";
  if (c.type === "lps22hh") return c.val + "hPa";
  if (c.type === "mpl115a2") return c.val + "hPa";
  if (c.type === "ms5803") return c.val + "hPa";
  if (c.type === "ms5607") return c.val + "hPa";
  if (c.type === "mprls") return c.val + "hPa";
  if (c.type === "bmp384") return c.val + "hPa";
  if (c.type === "icp10125") return c.val + "hPa";
  if (c.type === "icp20100") return c.val + "hPa";
  if (c.type === "mpx4115") return c.val + "hPa";
  if (c.type === "mpxv7002") return c.val + "hPa";
  if (c.type === "xgzp6847") return c.val + "hPa";
  if (c.type === "mq136") return c.val + "ppm";
  if (c.type === "mq139") return c.val + "ppm";
  if (c.type === "mq309") return c.val + "ppm";
  if (c.type === "tgs2600") return c.val + "ppm";
  if (c.type === "tgs2602") return c.val + "ppm";
  if (c.type === "tgs2620") return c.val + "ppm";
  if (c.type === "mics5524") return c.val + "ppm";
  if (c.type === "mics6814") return c.val + "ppm";
  if (c.type === "mh_z14a") return c.val + "ppm";
  if (c.type === "mh_z16") return c.val + "ppm";
  if (c.type === "s8_co2") return c.val + "ppm";
  if (c.type === "iaq_core") return c.val + "ppm";
  if (c.type === "zmod4410") return c.val + "ppm";
  if (c.type === "zh03b") return c.val + "ppm";
  if (c.type === "tsl2572") return c.val + "lux";
  if (c.type === "veml3235") return c.val + "lux";
  if (c.type === "opt4048") return c.val + "lux";
  if (c.type === "opt3004") return c.val + "lux";
  if (c.type === "ltr390") return c.val + "lux";
  if (c.type === "ltr303") return c.val + "lux";
  if (c.type === "ltr559") return c.val + "lux";
  if (c.type === "as7343") return c.val + "lux";
  if (c.type === "as7265x") return c.val + "lux";
  if (c.type === "ap3216") return c.val + "lux";
  if (c.type === "vcnl4200") return c.val + "lux";
  if (c.type === "si1133") return c.val + "lux";
  if (c.type === "mpu6886") return c.val + "g";
  if (c.type === "mpu9255") return c.val + "g";
  if (c.type === "lsm6dso") return c.val + "g";
  if (c.type === "lsm6dsox") return c.val + "g";
  if (c.type === "lis3mdl") return c.val + "g";
  if (c.type === "lis2mdl") return c.val + "g";
  if (c.type === "lis3dsh") return c.val + "g";
  if (c.type === "mma7660") return c.val + "g";
  if (c.type === "mma8451") return c.val + "g";
  if (c.type === "mma7361") return c.val + "g";
  if (c.type === "bma280") return c.val + "g";
  if (c.type === "bma423") return c.val + "g";
  if (c.type === "bmi088") return c.val + "g";
  if (c.type === "bmx160") return c.val + "g";
  if (c.type === "icm20689") return c.val + "g";
  if (c.type === "icm42605") return c.val + "g";
  if (c.type === "fxos8700") return c.val + "g";
  if (c.type === "fxas21002") return c.val + "g";
  if (c.type === "l3g4200d") return c.val + "g";
  if (c.type === "itg3200") return c.val + "g";
  if (c.type === "vl53l4cd") return c.val + "cm";
  if (c.type === "vl53l3cx") return c.val + "cm";
  if (c.type === "tof050c") return c.val + "cm";
  if (c.type === "tf02") return c.val + "cm";
  if (c.type === "tf03") return c.val + "cm";
  if (c.type === "hcsr05") return c.val + "cm";
  if (c.type === "srf05") return c.val + "cm";
  if (c.type === "maxsonar_ez1") return c.val + "cm";
  if (c.type === "us015") return c.val + "cm";
  if (c.type === "us020") return c.val + "cm";
  if (c.type === "urm37") return c.val + "cm";
  if (c.type === "ld2450") return c.val + "cm";
  if (c.type === "ld2420") return c.val + "cm";
  if (c.type === "hb100") return c.val + "cm";
  if (c.type === "sen0311") return c.val + "cm";
  if (c.type === "max30101") return c.val + "BPM";
  if (c.type === "max86150") return c.val + "BPM";
  if (c.type === "afe4490") return c.val + "BPM";
  if (c.type === "ads1292") return c.val + "BPM";
  if (c.type === "ad8233") return c.val + "BPM";
  if (c.type === "max30003") return c.val + "BPM";
  if (c.type === "emg_sensor") return c.val + "BPM";
  if (c.type === "muscle_v3") return c.val + "BPM";
  if (c.type === "gsr_grove") return c.val + "BPM";
  if (c.type === "skin_temp_mlx") return c.val + "BPM";
  if (c.type === "ina180") return c.val + "A";
  if (c.type === "ina199") return c.val + "A";
  if (c.type === "ina210") return c.val + "A";
  if (c.type === "ina230") return c.val + "A";
  if (c.type === "ina233") return c.val + "A";
  if (c.type === "acs711") return c.val + "A";
  if (c.type === "acs723") return c.val + "A";
  if (c.type === "acs724") return c.val + "A";
  if (c.type === "acs781") return c.val + "A";
  if (c.type === "max9611") return c.val + "A";
  if (c.type === "ltc4151") return c.val + "A";
  if (c.type === "ltc2945") return c.val + "A";
  if (c.type === "pac1934") return c.val + "A";
  if (c.type === "bl0937") return c.val + "A";
  if (c.type === "pzem017") return c.val + "A";
  if (c.type === "ade7753") return c.val + "A";
  if (c.type === "atm90e26") return c.val + "A";
  if (c.type === "hmc5983") return c.val + "µT";
  if (c.type === "mmc5603") return c.val + "µT";
  if (c.type === "mmc5983ma") return c.val + "µT";
  if (c.type === "ak8963") return c.val + "µT";
  if (c.type === "ak09916") return c.val + "µT";
  if (c.type === "qmc6310") return c.val + "µT";
  if (c.type === "bmm150") return c.val + "µT";
  if (c.type === "tmag5273") return c.val + "µT";
  if (c.type === "tlv493d") return c.val + "µT";
  if (c.type === "a1324") return c.val + "µT";
  if (c.type === "ss495a") return c.val + "µT";
  if (c.type === "drv5055") return c.val + "µT";
  if (c.type === "as5047p") return c.val + "µT";
  if (c.type === "ma730") return c.val + "µT";
  if (c.type === "mt6701") return c.val + "µT";
  if (c.type === "max9814") return c.val + "dB";
  if (c.type === "max4466") return c.val + "dB";
  if (c.type === "ics43434") return c.val + "dB";
  if (c.type === "inmp441") return c.val + "dB";
  if (c.type === "sph0645") return c.val + "dB";
  if (c.type === "spm0405") return c.val + "dB";
  if (c.type === "mp34dt05") return c.val + "dB";
  if (c.type === "ky037") return c.val + "dB";
  if (c.type === "fsr402") return c.val + "N";
  if (c.type === "fsr406") return c.val + "N";
  if (c.type === "load_cell_5kg") return c.val + "N";
  if (c.type === "load_cell_20kg") return c.val + "N";
  if (c.type === "piezo_film") return c.val + "N";
  if (c.type === "flex_4in") return c.val + "N";
  if (c.type === "yfs201") return c.val + "L/min";
  if (c.type === "yfs401") return c.val + "L/min";
  if (c.type === "yfs210") return c.val + "L/min";
  if (c.type === "yfb08") return c.val + "L/min";
  if (c.type === "fs300a") return c.val + "L/min";
  if (c.type === "fs400a") return c.val + "L/min";
  if (c.type === "float_switch") return c.val + "%";
  if (c.type === "ultrasonic_level") return c.val + "%";
  if (c.type === "capacitive_level") return c.val + "%";
  if (c.type === "optical_level") return c.val + "%";
  if (c.type === "soil_moisture_v2") return c.val + "%";
  if (c.type === "st7567") return String(c.val);
  if (c.type === "st7789_135") return String(c.val);
  if (c.type === "st7735_80") return String(c.val);
  if (c.type === "ili9163") return String(c.val);
  if (c.type === "ili9327") return String(c.val);
  if (c.type === "ili9342") return String(c.val);
  if (c.type === "ili9806") return String(c.val);
  if (c.type === "hx8357") return String(c.val);
  if (c.type === "hx8347") return String(c.val);
  if (c.type === "ra8875") return String(c.val);
  if (c.type === "ssd1289") return String(c.val);
  if (c.type === "ssd2119") return String(c.val);
  if (c.type === "sed1520") return String(c.val);
  if (c.type === "ks0108") return String(c.val);
  if (c.type === "pcd8544") return String(c.val);
  if (c.type === "uc1701") return String(c.val);
  if (c.type === "uc1609") return String(c.val);
  if (c.type === "t6963c") return String(c.val);
  if (c.type === "drv8701") return String(c.val);
  if (c.type === "drv8424") return String(c.val);
  if (c.type === "drv8428") return String(c.val);
  if (c.type === "tmc2100") return String(c.val);
  if (c.type === "tmc2226") return String(c.val);
  if (c.type === "tmc2225") return String(c.val);
  if (c.type === "tmc2240") return String(c.val);
  if (c.type === "tmc2660") return String(c.val);
  if (c.type === "a4982") return String(c.val);
  if (c.type === "a4983") return String(c.val);
  if (c.type === "l6219") return String(c.val);
  if (c.type === "l297") return String(c.val);
  if (c.type === "l298p") return String(c.val);
  if (c.type === "tb6560") return String(c.val);
  if (c.type === "tb6600") return String(c.val);
  if (c.type === "tb67s109") return String(c.val);
  if (c.type === "lm78m05") return c.val + "V out";
  if (c.type === "lm2937") return c.val + "V out";
  if (c.type === "lm2931") return c.val + "V out";
  if (c.type === "lm1086") return c.val + "V out";
  if (c.type === "lm1085") return c.val + "V out";
  if (c.type === "lt1763") return c.val + "V out";
  if (c.type === "lt1963") return c.val + "V out";
  if (c.type === "lt3042") return c.val + "V out";
  if (c.type === "tps7a20") return c.val + "V out";
  if (c.type === "tps73401") return c.val + "V out";
  if (c.type === "adp150") return c.val + "V out";
  if (c.type === "adp3338") return c.val + "V out";
  if (c.type === "mcp1802") return c.val + "V out";
  if (c.type === "mcp1826") return c.val + "V out";
  if (c.type === "ap7361") return c.val + "V out";
  if (c.type === "ap7333") return c.val + "V out";
  if (c.type === "rt9013") return c.val + "V out";
  if (c.type === "ld39050") return c.val + "V out";
  if (c.type === "tlv70033") return c.val + "V out";
  if (c.type === "lm22676") return c.val + "V out";
  if (c.type === "lm2672") return c.val + "V out";
  if (c.type === "lm2674") return c.val + "V out";
  if (c.type === "lm5008") return c.val + "V out";
  if (c.type === "lm5164") return c.val + "V out";
  if (c.type === "ltc3630") return c.val + "V out";
  if (c.type === "ltc3115") return c.val + "V out";
  if (c.type === "tps54360") return c.val + "V out";
  if (c.type === "tps62130") return c.val + "V out";
  if (c.type === "tps62160") return c.val + "V out";
  if (c.type === "tps62933") return c.val + "V out";
  if (c.type === "mp1470") return c.val + "V out";
  if (c.type === "mp2359") return c.val + "V out";
  if (c.type === "mp2491") return c.val + "V out";
  if (c.type === "xl1509") return c.val + "V out";
  if (c.type === "xl2596") return c.val + "V out";
  if (c.type === "mc34063") return c.val + "V out";
  if (c.type === "tps63020") return c.val + "V out";
  if (c.type === "tps61088") return c.val + "V out";
  if (c.type === "tps61230") return c.val + "V out";
  if (c.type === "mp3429") return c.val + "V out";
  if (c.type === "xl6019") return c.val + "V out";
  if (c.type === "xl6012") return c.val + "V out";
  if (c.type === "ap3012") return c.val + "V out";
  if (c.type === "lm2621") return c.val + "V out";
  if (c.type === "lm3478") return c.val + "V out";
  if (c.type === "tps55340") return c.val + "V out";
  if (c.type === "tps61200") return c.val + "V out";
  if (c.type === "tp4057") return c.val + "V out";
  if (c.type === "tp4054") return c.val + "V out";
  if (c.type === "mcp73831") return c.val + "V out";
  if (c.type === "mcp73832") return c.val + "V out";
  if (c.type === "bq24072") return c.val + "V out";
  if (c.type === "bq24075") return c.val + "V out";
  if (c.type === "bq25606") return c.val + "V out";
  if (c.type === "bq25895") return c.val + "V out";
  if (c.type === "ltc4054") return c.val + "V out";
  if (c.type === "ltc4065") return c.val + "V out";
  if (c.type === "cn3722") return c.val + "V out";
  if (c.type === "cn3765") return c.val + "V out";
  if (c.type === "ip2312") return c.val + "V out";
  if (c.type === "ip5310") return c.val + "V out";
  if (c.type === "esp32_wroom") return String(c.val);
  if (c.type === "esp32_s2") return String(c.val);
  if (c.type === "esp32_c6") return String(c.val);
  if (c.type === "esp12f") return String(c.val);
  if (c.type === "esp12e") return String(c.val);
  if (c.type === "esp07") return String(c.val);
  if (c.type === "bl602") return String(c.val);
  if (c.type === "rtl8710") return String(c.val);
  if (c.type === "rtl8720dn") return String(c.val);
  if (c.type === "nrf51822") return String(c.val);
  if (c.type === "nrf52810") return String(c.val);
  if (c.type === "nrf5340") return String(c.val);
  if (c.type === "nrf9160") return String(c.val);
  if (c.type === "cc2530") return String(c.val);
  if (c.type === "cc2531") return String(c.val);
  if (c.type === "cc2640") return String(c.val);
  if (c.type === "cc2652") return String(c.val);
  if (c.type === "cc3200") return String(c.val);
  if (c.type === "cc1310") return String(c.val);
  if (c.type === "cc1125") return String(c.val);
  if (c.type === "cc2500") return String(c.val);
  if (c.type === "si4432") return String(c.val);
  if (c.type === "si4463") return String(c.val);
  if (c.type === "si4455") return String(c.val);
  if (c.type === "sx1280") return String(c.val);
  if (c.type === "sx1272") return String(c.val);
  if (c.type === "sx1301") return String(c.val);
  if (c.type === "rfm12b") return String(c.val);
  if (c.type === "rfm22b") return String(c.val);
  if (c.type === "rfm98") return String(c.val);
  if (c.type === "rfm96") return String(c.val);
  if (c.type === "rfm63") return String(c.val);
  if (c.type === "xbee_pro") return String(c.val);
  if (c.type === "xbee3") return String(c.val);
  if (c.type === "bl654") return String(c.val);
  if (c.type === "ch341") return String(c.val);
  if (c.type === "ch9102") return String(c.val);
  if (c.type === "ch343") return String(c.val);
  if (c.type === "cp2102n") return String(c.val);
  if (c.type === "ft231x") return String(c.val);
  if (c.type === "ft2232") return String(c.val);
  if (c.type === "ft232h") return String(c.val);
  if (c.type === "mcp2221") return String(c.val);
  if (c.type === "max3485") return String(c.val);
  if (c.type === "sp3485") return String(c.val);
  if (c.type === "sn65hvd72") return String(c.val);
  if (c.type === "ltc2850") return String(c.val);
  if (c.type === "iso1176") return String(c.val);
  if (c.type === "adm2587") return String(c.val);
  if (c.type === "adm3053") return String(c.val);
  if (c.type === "mcp2562") return String(c.val);
  if (c.type === "tcan1042") return String(c.val);
  if (c.type === "tja1051") return String(c.val);
  if (c.type === "sn65hvd1050") return String(c.val);
  if (c.type === "l80") return String(c.val);
  if (c.type === "l86") return String(c.val);
  if (c.type === "atgm336h") return String(c.val);
  if (c.type === "gt_u7") return String(c.val);
  if (c.type === "neo_m9n") return String(c.val);
  if (c.type === "zoe_m8q") return String(c.val);
  if (c.type === "max_m10s") return String(c.val);
  if (c.type === "teseo_liv3") return String(c.val);
  if (c.type === "mtk3339") return String(c.val);
  if (c.type === "pa1010d") return String(c.val);
  if (c.type === "sim28") return String(c.val);
  if (c.type === "l96") return String(c.val);
  if (c.type === "sim800c") return String(c.val);
  if (c.type === "sim808") return String(c.val);
  if (c.type === "sim5320") return String(c.val);
  if (c.type === "sim7000") return String(c.val);
  if (c.type === "sim7070") return String(c.val);
  if (c.type === "sim7080") return String(c.val);
  if (c.type === "sim7500") return String(c.val);
  if (c.type === "sim7670") return String(c.val);
  if (c.type === "ec200s") return String(c.val);
  if (c.type === "ec25") return String(c.val);
  if (c.type === "bg95") return String(c.val);
  if (c.type === "bg96") return String(c.val);
  if (c.type === "m26") return String(c.val);
  if (c.type === "ec21") return String(c.val);
  if (c.type === "ec600") return String(c.val);
  if (c.type === "a9g") return String(c.val);
  if (c.type === "a6") return String(c.val);
  if (c.type === "a7672e") return String(c.val);
  if (c.type === "ic_74hc03") return String(c.val);
  if (c.type === "ic_74hc05") return String(c.val);
  if (c.type === "ic_74hc09") return String(c.val);
  if (c.type === "ic_74hc21") return String(c.val);
  if (c.type === "ic_74hc27") return String(c.val);
  if (c.type === "ic_74hc51") return String(c.val);
  if (c.type === "ic_74hc58") return String(c.val);
  if (c.type === "ic_74hc85") return String(c.val);
  if (c.type === "ic_74hc107") return String(c.val);
  if (c.type === "ic_74hc109") return String(c.val);
  if (c.type === "ic_74hc112") return String(c.val);
  if (c.type === "ic_74hc123") return String(c.val);
  if (c.type === "ic_74hc126") return String(c.val);
  if (c.type === "ic_74hc132") return String(c.val);
  if (c.type === "ic_74hc137") return String(c.val);
  if (c.type === "ic_74hc147") return String(c.val);
  if (c.type === "ic_74hc148") return String(c.val);
  if (c.type === "ic_74hc153") return String(c.val);
  if (c.type === "ic_74hc158") return String(c.val);
  if (c.type === "ic_74hc160") return String(c.val);
  if (c.type === "ic_74hc162") return String(c.val);
  if (c.type === "ic_74hc163") return String(c.val);
  if (c.type === "ic_74hc168") return String(c.val);
  if (c.type === "ic_74hc169") return String(c.val);
  if (c.type === "ic_74hc173") return String(c.val);
  if (c.type === "ic_74hc182") return String(c.val);
  if (c.type === "ic_74hc190") return String(c.val);
  if (c.type === "ic_74hc191") return String(c.val);
  if (c.type === "ic_74hc192") return String(c.val);
  if (c.type === "ic_74hc194") return String(c.val);
  if (c.type === "ic_74hc195") return String(c.val);
  if (c.type === "ic_74hc238") return String(c.val);
  if (c.type === "ic_74hc239") return String(c.val);
  if (c.type === "ic_74hc240") return String(c.val);
  if (c.type === "ic_74hc241") return String(c.val);
  if (c.type === "ic_74hc251") return String(c.val);
  if (c.type === "ic_74hc253") return String(c.val);
  if (c.type === "ic_74hc257") return String(c.val);
  if (c.type === "ic_74hc258") return String(c.val);
  if (c.type === "ic_74hc259") return String(c.val);
  if (c.type === "cd4000") return String(c.val);
  if (c.type === "cd4002") return String(c.val);
  if (c.type === "cd4006") return String(c.val);
  if (c.type === "cd4007") return String(c.val);
  if (c.type === "cd4008") return String(c.val);
  if (c.type === "cd4009") return String(c.val);
  if (c.type === "cd4010") return String(c.val);
  if (c.type === "cd4011") return String(c.val);
  if (c.type === "cd4012") return String(c.val);
  if (c.type === "cd4014") return String(c.val);
  if (c.type === "cd4016") return String(c.val);
  if (c.type === "cd4018") return String(c.val);
  if (c.type === "cd4019") return String(c.val);
  if (c.type === "cd4020") return String(c.val);
  if (c.type === "cd4021") return String(c.val);
  if (c.type === "cd4024") return String(c.val);
  if (c.type === "cd4026") return String(c.val);
  if (c.type === "cd4033") return String(c.val);
  if (c.type === "cd4034") return String(c.val);
  if (c.type === "cd4035") return String(c.val);
  if (c.type === "cd4040") return String(c.val);
  if (c.type === "cd4042") return String(c.val);
  if (c.type === "cd4043") return String(c.val);
  if (c.type === "cd4044") return String(c.val);
  if (c.type === "cd4049") return String(c.val);
  if (c.type === "cd4050") return String(c.val);
  if (c.type === "cd4052") return String(c.val);
  if (c.type === "cd4053") return String(c.val);
  if (c.type === "cd4069") return String(c.val);
  if (c.type === "cd4072") return String(c.val);
  if (c.type === "cd4073") return String(c.val);
  if (c.type === "cd4078") return String(c.val);
  if (c.type === "cd4082") return String(c.val);
  if (c.type === "cd4094") return String(c.val);
  if (c.type === "cd4099") return String(c.val);
  if (c.type === "cd40106") return String(c.val);
  if (c.type === "cd40193") return String(c.val);
  if (c.type === "cd4585") return String(c.val);
  if (c.type === "tlc555") return String(c.val);
  if (c.type === "icm7555") return String(c.val);
  if (c.type === "lmc555") return String(c.val);
  if (c.type === "xr2206") return String(c.val);
  if (c.type === "icl8038") return String(c.val);
  if (c.type === "max038") return String(c.val);
  if (c.type === "lm566") return String(c.val);
  if (c.type === "lm567") return String(c.val);
  if (c.type === "ne565") return String(c.val);
  if (c.type === "ne567") return String(c.val);
  if (c.type === "at24c01") return String(c.val);
  if (c.type === "at24c04") return String(c.val);
  if (c.type === "at24cm01") return String(c.val);
  if (c.type === "at24cm02") return String(c.val);
  if (c.type === "m24c64") return String(c.val);
  if (c.type === "m24256") return String(c.val);
  if (c.type === "w25q16") return String(c.val);
  if (c.type === "w25q32") return String(c.val);
  if (c.type === "w25q80") return String(c.val);
  if (c.type === "w25q256") return String(c.val);
  if (c.type === "w25q512") return String(c.val);
  if (c.type === "mx25l1606") return String(c.val);
  if (c.type === "mx25l3206") return String(c.val);
  if (c.type === "mx25l6406") return String(c.val);
  if (c.type === "mx25l12805") return String(c.val);
  if (c.type === "sst25vf016") return String(c.val);
  if (c.type === "s25fl064") return String(c.val);
  if (c.type === "is25lp128") return String(c.val);
  if (c.type === "gd25q32") return String(c.val);
  if (c.type === "gd25q64") return String(c.val);
  if (c.type === "fm24cl64") return String(c.val);
  if (c.type === "fm24v10") return String(c.val);
  if (c.type === "fm25cl64") return String(c.val);
  if (c.type === "mb85rs64") return String(c.val);
  if (c.type === "mb85rs256") return String(c.val);
  if (c.type === "mcp23k256") return String(c.val);
  if (c.type === "sram_23lc1024") return String(c.val);
  if (c.type === "sram_23lc512") return String(c.val);
  if (c.type === "sram_23k256") return String(c.val);
  if (c.type === "c93c46") return String(c.val);
  if (c.type === "c93c56") return String(c.val);
  if (c.type === "c93c66") return String(c.val);
  if (c.type === "c93c86") return String(c.val);
  if (c.type === "at25010") return String(c.val);
  if (c.type === "at25640") return String(c.val);
  if (c.type === "at25m01") return String(c.val);
  if (c.type === "sdram_is42s16160") return String(c.val);
  if (c.type === "sdram_w9825g6") return String(c.val);
  if (c.type === "psram_aps6404") return String(c.val);
  if (c.type === "psram_ips6404") return String(c.val);
  if (c.type === "nand_w25n01") return String(c.val);
  if (c.type === "nand_mt29f") return String(c.val);
  if (c.type === "emmc_4gb") return String(c.val);
  if (c.type === "lm1876") return c.val + "W";
  if (c.type === "lm2877") return c.val + "W";
  if (c.type === "lm3875") return c.val + "W";
  if (c.type === "lm4780") return c.val + "W";
  if (c.type === "tda1514") return c.val + "W";
  if (c.type === "tda1521") return c.val + "W";
  if (c.type === "tda2005") return c.val + "W";
  if (c.type === "tda2006") return c.val + "W";
  if (c.type === "tda2009") return c.val + "W";
  if (c.type === "tda7240") return c.val + "W";
  if (c.type === "tda7266") return c.val + "W";
  if (c.type === "tda7293") return c.val + "W";
  if (c.type === "tda7296") return c.val + "W";
  if (c.type === "tda7379") return c.val + "W";
  if (c.type === "tda7384") return c.val + "W";
  if (c.type === "tda7388") return c.val + "W";
  if (c.type === "tda7391") return c.val + "W";
  if (c.type === "tpa3118") return c.val + "W";
  if (c.type === "tpa3123") return c.val + "W";
  if (c.type === "tpa3128") return c.val + "W";
  if (c.type === "tpa3130") return c.val + "W";
  if (c.type === "tpa3140") return c.val + "W";
  if (c.type === "tpa3220") return c.val + "W";
  if (c.type === "max9768") return c.val + "W";
  if (c.type === "max9788") return c.val + "W";
  if (c.type === "max98400") return c.val + "W";
  if (c.type === "ssm3582") return c.val + "W";
  if (c.type === "stk4141") return c.val + "W";
  if (c.type === "pam8620") return c.val + "W";
  if (c.type === "lm4950") return c.val + "W";
  if (c.type === "lm4991") return c.val + "W";
  if (c.type === "tpa6120") return c.val + "W";
  if (c.type === "tpa6132") return c.val + "W";
  if (c.type === "tpa6211") return c.val + "W";
  if (c.type === "tpa2012") return c.val + "W";
  if (c.type === "tpa2031") return c.val + "W";
  if (c.type === "pam8406") return c.val + "W";
  if (c.type === "pam8304") return c.val + "W";
  if (c.type === "ssm2302") return c.val + "W";
  if (c.type === "lm833") return c.val + "x";
  if (c.type === "lm4562") return c.val + "x";
  if (c.type === "lm4558") return c.val + "x";
  if (c.type === "lm1458") return c.val + "x";
  if (c.type === "opa134") return c.val + "x";
  if (c.type === "opa227") return c.val + "x";
  if (c.type === "opa277") return c.val + "x";
  if (c.type === "opa337") return c.val + "x";
  if (c.type === "opa343") return c.val + "x";
  if (c.type === "opa350") return c.val + "x";
  if (c.type === "opa551") return c.val + "x";
  if (c.type === "opa564") return c.val + "x";
  if (c.type === "opa1612") return c.val + "x";
  if (c.type === "opa1656") return c.val + "x";
  if (c.type === "opa1678") return c.val + "x";
  if (c.type === "opa2604") return c.val + "x";
  if (c.type === "opa2350") return c.val + "x";
  if (c.type === "ad8066") return c.val + "x";
  if (c.type === "ad8397") return c.val + "x";
  if (c.type === "ad797") return c.val + "x";
  if (c.type === "ad8099") return c.val + "x";
  if (c.type === "ad8221") return c.val + "x";
  if (c.type === "ad8276") return c.val + "x";
  if (c.type === "ad8429") return c.val + "x";
  if (c.type === "ad8606") return c.val + "x";
  if (c.type === "ad8628") return c.val + "x";
  if (c.type === "lt1013") return c.val + "x";
  if (c.type === "lt1028") return c.val + "x";
  if (c.type === "lt1124") return c.val + "x";
  if (c.type === "lt1677") return c.val + "x";
  if (c.type === "lt6015") return c.val + "x";
  if (c.type === "lmv358") return c.val + "x";
  if (c.type === "lmv321") return c.val + "x";
  if (c.type === "lmv324") return c.val + "x";
  if (c.type === "lmc6482") return c.val + "x";
  if (c.type === "lmc662") return c.val + "x";
  if (c.type === "lmp7701") return c.val + "x";
  if (c.type === "mcp6001") return c.val + "x";
  if (c.type === "mcp6004") return c.val + "x";
  if (c.type === "mcp6231") return c.val + "x";
  if (c.type === "mcp6241") return c.val + "x";
  if (c.type === "mcp6271") return c.val + "x";
  if (c.type === "tlv2371") return c.val + "x";
  if (c.type === "tlv2462") return c.val + "x";
  if (c.type === "tlv271") return c.val + "x";
  if (c.type === "tlv9061") return c.val + "x";
  if (c.type === "tlv9062") return c.val + "x";
  if (c.type === "ca3140") return c.val + "x";
  if (c.type === "ca3130") return c.val + "x";
  if (c.type === "switch") return c.closed ? t("مغلق", "closed") : t("مفتوح", "open");
  if (c.type.indexOf("gate_") === 0) return c.type.slice(5).toUpperCase() + (sim && sim.ok && sim.gateOut ? (sim.gateOut[c.id] ? " = 1" : " = 0") : "");
  return "";
}

var cv = document.getElementById("cv"), ctx = cv.getContext("2d"), stage = document.getElementById("stage");
var cssW = 300, cssH = 300, dpr = 1, animT = 0;
function resize() {
  dpr = Math.max(1, window.devicePixelRatio || 1);
  cssW = Math.max(100, stage.clientWidth); cssH = Math.max(100, stage.clientHeight);
  cv.width = Math.round(cssW * dpr); cv.height = Math.round(cssH * dpr);
  draw();
}

function drawComp(c) {
  c = aliasView(c);
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
  } else if (c.type === "potentiometer") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-24, 0);
    for (k = 0; k < 6; k++) ctx.lineTo(-24 + 4 + k * 8, k % 2 === 0 ? -9 : 9);
    ctx.lineTo(24, 0); ctx.stroke();
    // المؤشر (الطرف c): يتحرك على امتداد المقاومة حسب النسبة
    var wx = (potPos(c) - 0.5) * 36;
    line(0, HL, wx, 14);
    ctx.beginPath(); ctx.moveTo(wx, 10); ctx.lineTo(wx - 4, 18); ctx.lineTo(wx + 4, 18); ctx.closePath(); ctx.fill();
  } else if (c.type === "motor" || c.type === "buzzer") {
    var on2 = s && Math.abs(s.V[c.id]) > 1.0 && Math.abs(cur) > 0.001;
    line(-HL, 0, -18, 0); line(18, 0, HL, 0);
    ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI * 2);
    ctx.save(); ctx.fillStyle = on2 ? "rgba(56,189,248,.18)" : "rgba(148,163,184,.12)"; ctx.fill(); ctx.restore(); ctx.stroke();
    if (c.type === "motor") {
      ctx.save(); ctx.rotate(c.ang || 0); ctx.lineWidth = 3; line(-11, 0, 11, 0); line(0, -11, 0, 11); ctx.restore();
    } else {
      ctx.save(); ctx.fillStyle = "#94a3b8"; ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center"; ctx.fillText("BZ", 0, 3); ctx.restore();
      if (on2) {
        ctx.save(); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2;
        for (k = 1; k <= 2; k++) { ctx.globalAlpha = 0.9 - ((animT * 2 + k * 0.4) % 1) * 0.6; ctx.beginPath(); ctx.arc(0, 0, 18 + k * 7, -0.9, 0.9); ctx.stroke(); }
        ctx.restore();
      }
    }
  } else if (c.type === "ldr") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    ctx.beginPath(); ctx.rect(-24, -10, 48, 20); ctx.stroke();
    // أسهم الضوء
    ctx.beginPath(); ctx.moveTo(-10, -25); ctx.lineTo(-10, -15); ctx.moveTo(10, -25); ctx.lineTo(10, -15); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-12, -20); ctx.lineTo(-10, -15); ctx.lineTo(-8, -20); ctx.moveTo(8, -20); ctx.lineTo(10, -15); ctx.lineTo(12, -20); ctx.fill();
  } else if (c.type === "relay") {
    var ron2 = s && s.relayOn && s.relayOn[c.id];
    line(-HL, -15, -22, -15); line(-HL, 15, -22, 15);
    if (ron2) { ctx.save(); ctx.fillStyle = "rgba(251,191,36,.22)"; ctx.fillRect(-22, -22, 20, 44); ctx.restore(); }
    ctx.strokeRect(-22, -22, 20, 44);
    ctx.save(); ctx.fillStyle = "#94a3b8"; ctx.font = "bold 10px sans-serif"; ctx.textAlign = "center"; ctx.fillText("K", -12, 4); ctx.restore();
    line(HL, -15, 20, -15); line(20, 15, HL, 15);
    ctx.beginPath(); ctx.arc(20, -15, 3, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(20, 15, 3, 0, Math.PI * 2); ctx.fill();
    if (ron2) line(20, -15, 20, 12); else line(20, -15, 8, 8);
    ctx.save(); ctx.setLineDash([3, 3]); ctx.lineWidth = 1.5; line(-2, 0, 8, 0); ctx.restore();
  } else if (c.type === "ac_source") {
    line(-HL, 0, -14, 0); line(14, 0, HL, 0);
    ctx.beginPath(); ctx.arc(0, 0, 14, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-8, 0); ctx.quadraticCurveTo(-4, -10, 0, 0); ctx.quadraticCurveTo(4, 10, 8, 0); ctx.stroke();
  } else if (c.type === "battery") {
    line(-HL, 0, -6, 0); line(6, 0, HL, 0);
    line(-6, -15, -6, 15); line(6, -8, 6, 8);
    ctx.font = "bold 13px sans-serif"; ctx.textAlign = "center"; ctx.fillText("+", -20, -8);
  } else if (c.type === "arduino") {
    line(-HL, 0, -30, 0); line(30, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#00979d"; ctx.fillRect(-30, -20, 60, 40); ctx.restore();
    ctx.strokeRect(-30, -20, 60, 40);
    ctx.fillStyle = "white"; ctx.font = "bold 11px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("UNO", 0, 4);
  } else if (c.type === "esp32") {
    line(-HL, 0, -25, 0); line(25, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#2c3e50"; ctx.fillRect(-25, -25, 50, 50); ctx.restore();
    ctx.strokeRect(-25, -25, 50, 50);
    ctx.fillStyle = "#f1c40f"; ctx.font = "bold 10px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("ESP32", 0, 4);
  } else if (c.type === "capacitor") {
    line(-HL, 0, -8, 0); line(8, 0, HL, 0);
    line(-8, -15, -8, 15); line(8, -15, 8, 15);
  } else if (c.type === "diode") {
    line(-HL, 0, -10, 0); line(10, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-10, -14); ctx.lineTo(-10, 14); ctx.lineTo(10, 0); ctx.closePath(); ctx.stroke();
    line(10, -14, 10, 14);
  } else if (c.type === "transistor") {
    line(-HL, 0, -10, 0); line(HL, 0, 10, 0);
    ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI * 2); ctx.stroke();
    line(-10, -10, -5, -5); line(10, -10, 5, -5); line(0, HL, 0, -10);
    ctx.beginPath(); ctx.moveTo(10, -10); ctx.lineTo(5, -5); ctx.lineTo(15, -15); ctx.fill();
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
  } else if (c.type === "inductor") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    for (k = 0; k < 4; k++) { ctx.beginPath(); ctx.arc(-18 + k * 12, 0, 6, Math.PI, 0); ctx.stroke(); }
  } else if (c.type === "thermistor") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    ctx.beginPath(); ctx.rect(-24, -10, 48, 20); ctx.stroke();
    line(-18, 16, 16, -16);
    ctx.beginPath(); ctx.moveTo(18, -18); ctx.lineTo(10, -15); ctx.lineTo(15, -10); ctx.closePath(); ctx.fill();
  } else if (c.type === "speaker") {
    line(-HL, 0, -20, 0); line(14, 0, HL, 0);
    ctx.beginPath(); ctx.rect(-20, -8, 16, 16); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-4, -8); ctx.lineTo(14, -18); ctx.lineTo(14, 18); ctx.lineTo(-4, 8); ctx.closePath(); ctx.stroke();
  } else if (c.type === "zener") {
    line(-HL, 0, -10, 0); line(10, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-10, -14); ctx.lineTo(-10, 14); ctx.lineTo(10, 0); ctx.closePath(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(6, -14); ctx.lineTo(10, -14); ctx.lineTo(10, 14); ctx.lineTo(14, 14); ctx.stroke();
  } else if (c.type === "schottky") {
    line(-HL, 0, -10, 0); line(10, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-10, -14); ctx.lineTo(-10, 14); ctx.lineTo(10, 0); ctx.closePath(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(6, -8); ctx.lineTo(6, -14); ctx.lineTo(10, -14); ctx.lineTo(10, 14); ctx.lineTo(14, 14); ctx.lineTo(14, 8); ctx.stroke();
  } else if (c.type === "solar") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#facc15"; ctx.fillRect(-24, -16, 48, 32); ctx.restore();
    ctx.strokeRect(-24, -16, 48, 32);
    line(-8, -16, -8, 16); line(8, -16, 8, 16); line(-24, 0, 24, 0);
  } else if (c.type === "dc_jack") {
    line(-HL, 0, -16, 0); line(16, 0, HL, 0);
    ctx.beginPath(); ctx.arc(0, 0, 16, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.arc(0, 0, 8, 0, Math.PI * 2); ctx.stroke();
  } else if (c.type === "nano") {
    line(-HL, 0, -30, 0); line(30, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#1d4ed8"; ctx.fillRect(-30, -20, 60, 40); ctx.restore();
    ctx.strokeRect(-30, -20, 60, 40);
    ctx.fillStyle = "white"; ctx.font = "bold 11px sans-serif"; ctx.textAlign = "center"; ctx.fillText("NANO", 0, 4);
  } else if (c.type === "mega") {
    line(-HL, 0, -30, 0); line(30, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#15803d"; ctx.fillRect(-30, -20, 60, 40); ctx.restore();
    ctx.strokeRect(-30, -20, 60, 40);
    ctx.fillStyle = "white"; ctx.font = "bold 11px sans-serif"; ctx.textAlign = "center"; ctx.fillText("MEGA", 0, 4);
  } else if (c.type === "esp8266") {
    line(-HL, 0, -25, 0); line(25, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#6b7280"; ctx.fillRect(-25, -25, 50, 50); ctx.restore();
    ctx.strokeRect(-25, -25, 50, 50);
    ctx.fillStyle = "white"; ctx.font = "bold 10px sans-serif"; ctx.textAlign = "center"; ctx.fillText("8266", 0, 4);
  } else if (c.type === "pico") {
    line(-HL, 0, -30, 0); line(30, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#dc2626"; ctx.fillRect(-30, -20, 60, 40); ctx.restore();
    ctx.strokeRect(-30, -20, 60, 40);
    ctx.fillStyle = "white"; ctx.font = "bold 11px sans-serif"; ctx.textAlign = "center"; ctx.fillText("PICO", 0, 4);
  } else if (c.type === "reg7805" || c.type === "reg7803") {
    line(-HL, 0, -20, 0); line(20, 0, HL, 0); line(0, 22, 0, HL);
    ctx.save(); ctx.fillStyle = "#1e293b"; ctx.fillRect(-20, -22, 40, 44); ctx.restore();
    ctx.strokeRect(-20, -22, 40, 44);
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(c.type === "reg7805" ? "7805" : "7803", 0, 4); ctx.restore();
  } else if (c.type === "opamp") {
    line(-HL, -10, -20, -10); line(-HL, 10, -20, 10); line(20, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-20, -22); ctx.lineTo(-20, 22); ctx.lineTo(20, 0); ctx.closePath();
    ctx.save(); ctx.fillStyle = "rgba(30,41,59,.85)"; ctx.fill(); ctx.restore(); ctx.stroke();
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 11px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("−", -14, -5); ctx.fillText("+", -14, 15); ctx.restore();
  } else if (c.type === "transistor_pnp") {
    line(-HL, 0, -10, 0); line(HL, 0, 10, 0);
    ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI * 2); ctx.stroke();
    line(-10, -10, -5, -5); line(10, -10, 5, -5); line(0, HL, 0, -10);
    ctx.beginPath(); ctx.moveTo(5, -5); ctx.lineTo(10.8, -7.2); ctx.lineTo(7.2, -10.8); ctx.closePath(); ctx.fill();
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 8px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("PNP", 0, -22); ctx.restore();
  } else if (c.type === "pir") {
    line(-HL, 0, -20, 0); line(20, 0, HL, 0);
    ctx.save(); ctx.fillStyle = c.closed ? "#fbbf24" : "#64748b"; ctx.fillRect(-20, -18, 40, 36); ctx.restore();
    ctx.strokeRect(-20, -18, 40, 36);
    ctx.save(); ctx.fillStyle = "#0f172a"; ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("PIR", 0, 3); ctx.restore();
  } else if (c.type === "dht11") {
    line(-HL, 0, -18, 0); line(18, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#22c55e"; ctx.fillRect(-18, -18, 36, 36); ctx.restore();
    ctx.strokeRect(-18, -18, 36, 36);
    ctx.save(); ctx.fillStyle = "white"; ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(c.val + "°C", 0, 3); ctx.restore();
  } else if (c.type === "seven_seg") {
    var segOn = {
      0: [1,1,1,1,1,1,0], 1: [0,1,1,0,0,0,0], 2: [1,1,0,1,1,0,1],
      3: [1,1,1,1,0,0,1], 4: [0,1,1,0,0,1,1], 5: [1,0,1,1,0,1,1],
      6: [1,0,1,1,1,1,1], 7: [1,1,1,0,0,0,0], 8: [1,1,1,1,1,1,1],
      9: [1,1,1,1,0,1,1]
    }[c.val] || [0,0,0,0,0,0,0];
    var segLit = s && Math.abs(s.V[c.id]) > 2;
    line(-HL, -15, -20, -15); line(-HL, 15, -20, 15); line(20, 0, HL, 0); line(0, 22, 0, HL);
    ctx.save(); ctx.fillStyle = "#0f172a"; ctx.fillRect(-20, -22, 40, 44); ctx.strokeStyle = "#64748b"; ctx.strokeRect(-20, -22, 40, 44); ctx.restore();
    var segs = [[-10,-16,8,-16],[10,-14,10,-2],[10,2,10,14],[-10,16,8,16],[-12,2,-12,14],[-12,-14,-12,-2],[-10,0,8,0]];
    for (k = 0; k < 7; k++) {
      ctx.save(); ctx.lineWidth = 3; ctx.strokeStyle = (segLit && segOn[k]) ? "#ef4444" : "#3b1d24";
      line(segs[k][0], segs[k][1], segs[k][2], segs[k][3]); ctx.restore();
    }
  } else if (c.type === "timer555") {
    var on555 = !!(s && s.timer555On && s.timer555On[c.id]);
    line(-HL, -15, -20, -15); line(-HL, 15, -20, 15); line(20, 0, HL, 0);
    ctx.save(); ctx.fillStyle = on555 ? "#fbbf24" : "#1e293b"; ctx.fillRect(-20, -22, 40, 44); ctx.restore();
    ctx.strokeRect(-20, -22, 40, 44);
    ctx.save(); ctx.fillStyle = on555 ? "#0f172a" : "#e2e8f0"; ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("555", 0, 3); ctx.restore();
    if (on555) {
      ctx.save(); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2;
      for (k = 1; k <= 2; k++) { ctx.globalAlpha = 0.9 - ((animT * 3 + k * 0.5) % 1) * 0.7; ctx.beginPath(); ctx.arc(0, 0, 22 + k * 5, -0.9, 0.9); ctx.stroke(); }
      ctx.restore();
    }
  } else if (c.type === "gate_nand" || c.type === "gate_xor" || c.type === "gate_xnor") {
    var hiGN = s && s.gateOut && s.gateOut[c.id];
    ctx.beginPath();
    if (c.type === "gate_nand") {
      ctx.moveTo(-20, -15); ctx.lineTo(-2, -15); ctx.arc(-2, 0, 13, -Math.PI / 2, Math.PI / 2); ctx.lineTo(-20, 15); ctx.closePath();
    } else {
      ctx.moveTo(-20, -15); ctx.quadraticCurveTo(-7, -15, 8, 0); ctx.quadraticCurveTo(-7, 15, -20, 15);
      ctx.quadraticCurveTo(-12, 0, -20, -15); ctx.closePath();
    }
    if (hiGN) { ctx.save(); ctx.fillStyle = "rgba(74,222,128,.28)"; ctx.fill(); ctx.restore(); }
    ctx.stroke();
    line(-HL, -15, -20, -15); line(-HL, 15, -20, 15);
    if (c.type === "gate_nand") {
      ctx.beginPath(); ctx.arc(15, 0, 3, 0, Math.PI * 2); ctx.stroke();
      line(18, 0, HL, 0);
    } else {
      ctx.beginPath(); ctx.moveTo(-25, -15); ctx.quadraticCurveTo(-17, 0, -25, 15); ctx.stroke();
      if (c.type === "gate_xnor") { ctx.beginPath(); ctx.arc(11, 0, 3, 0, Math.PI * 2); ctx.stroke(); line(14, 0, HL, 0); }
      else line(8, 0, HL, 0);
    }
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 7px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(c.type === "gate_nand" ? "NAND" : c.type === "gate_xor" ? "XOR" : "XNOR", 0, 22); ctx.restore();
  } else if (c.type === "mosfet_n") {
    line(0, -HL, 0, -18); line(0, 18, 0, HL); line(-HL, 0, -10, 0);
    ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI * 2); ctx.stroke();
    line(-6, -12, 6, -12); line(-6, -8, 6, -8);
    line(-6, 8, 6, 8); line(-6, 12, 6, 12);
    line(-6, -12, -6, 12);
    line(0, -12, 0, 12);
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 8px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("N", 12, 4); ctx.restore();
  } else if (c.type === "lm317") {
    line(-HL, 0, -20, 0); line(20, 0, HL, 0); line(0, 22, 0, HL);
    ctx.save(); ctx.fillStyle = "#1e293b"; ctx.fillRect(-20, -22, 40, 44); ctx.restore();
    ctx.strokeRect(-20, -22, 40, 44);
    ctx.save(); ctx.fillStyle = "#f59e0b"; ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("LM317", 0, 4); ctx.restore();
  } else if (c.type === "servo") {
    var svRun = !!(s && s.servoOn && s.servoOn[c.id]);
    line(-HL, -12, -18, -12); line(-HL, 12, -18, 12); line(18, 0, HL, 0);
    ctx.save(); ctx.fillStyle = svRun ? "#3b82f6" : "#475569"; ctx.fillRect(-18, -18, 36, 36); ctx.restore();
    ctx.strokeRect(-18, -18, 36, 36);
    ctx.save(); ctx.translate(0, 4); ctx.rotate((c.val - 90) * Math.PI / 180); ctx.lineWidth = 3; ctx.strokeStyle = svRun ? "#fbbf24" : "#94a3b8";
    line(0, 0, 0, -16); ctx.restore();
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 8px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(c.val + "°", 0, 16); ctx.restore();
  } else if (c.type === "lcd_16x2") {
    line(-HL, -12, -38, -12); line(-HL, 12, -38, 12); line(38, 0, HL, 0);
    var lcdOn = s && Math.abs(s.V[c.id]) > 3.0;
    ctx.save(); ctx.fillStyle = lcdOn ? "#22c55e" : "#1e293b"; ctx.fillRect(-38, -22, 76, 44); ctx.restore();
    ctx.strokeRect(-38, -22, 76, 44);
    if (lcdOn) {
      ctx.save(); ctx.fillStyle = "#0f172a"; ctx.font = "bold 10px monospace"; ctx.textAlign = "left";
      ctx.fillText(String(c.val).substring(0, 10), -34, 4); ctx.restore();
    }
  } else if (c.type === "hc_sr04") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#1e40af"; ctx.fillRect(-22, -20, 44, 40); ctx.restore();
    ctx.strokeRect(-22, -20, 44, 40);
    ctx.save(); ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(-11, -5, 7, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.arc(11, -5, 7, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
    ctx.save(); ctx.fillStyle = "#fbbf24"; ctx.font = "bold 8px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(c.val + "cm", 0, 15); ctx.restore();
  } else if (c.type === "ds18b20") {
    line(-HL, -12, -18, -12); line(-HL, 12, -18, 12); line(18, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#059669"; ctx.fillRect(-18, -18, 36, 36); ctx.restore();
    ctx.strokeRect(-18, -18, 36, 36);
    ctx.save(); ctx.fillStyle = "white"; ctx.font = "bold 9px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(Number(c.val).toFixed(1) + "°", 0, 3); ctx.restore();
  } else if (c.type === "stepper_motor") {
    var stpOn = s && Math.abs(s.V[c.id]) > 1.0 && Math.abs(cur) > 0.001;
    line(-HL, 0, -20, 0); line(20, 0, HL, 0);
    ctx.save(); ctx.fillStyle = stpOn ? "rgba(56,189,248,.18)" : "rgba(148,163,184,.12)";
    ctx.beginPath(); ctx.arc(0, 0, 20, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    ctx.beginPath(); ctx.arc(0, 0, 20, 0, Math.PI * 2); ctx.stroke();
    ctx.save(); ctx.rotate(c.ang || 0); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 3;
    for (k = 0; k < 4; k++) { ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(k * Math.PI / 2) * 14, Math.sin(k * Math.PI / 2) * 14); ctx.stroke(); }
    ctx.restore();
  } else if (c.type === "rgb_led") {
    var rgbCol = RGB_COLORS[c.val] || RGB_COLORS.red;
    var rgbBr = s && s.ledOn[c.id] ? Math.min(1, cur / 0.02) : 0;
    if (rgbBr > 0) {
      var gRGB = ctx.createRadialGradient(0, 0, 4, 0, 0, 14 + 34 * rgbBr);
      gRGB.addColorStop(0, rgbCol); gRGB.addColorStop(1, "rgba(0,0,0,0)");
      ctx.save(); ctx.globalAlpha = 0.25 + 0.7 * rgbBr; ctx.fillStyle = gRGB;
      ctx.beginPath(); ctx.arc(0, 0, 14 + 34 * rgbBr, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    line(-HL, 0, -10, 0); line(10, 0, HL, 0);
    ctx.beginPath(); ctx.moveTo(-10, -14); ctx.lineTo(-10, 14); ctx.lineTo(10, 0); ctx.closePath();
    ctx.save(); ctx.fillStyle = rgbBr > 0 ? rgbCol : "rgba(148,163,184,.25)"; ctx.fill(); ctx.restore(); ctx.stroke();
    line(10, -14, 10, 14);
  } else if (c.type === "varistor") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    ctx.beginPath(); ctx.rect(-24, -10, 48, 20); ctx.stroke();
    line(-24, -10, 24, 10);
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 8px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("V", -14, 3); ctx.fillText("I", 8, 3); ctx.restore();
  } else if (c.type === "oled_ssd1306") {
    line(-HL, -12, -36, -12); line(-HL, 12, -36, 12); line(36, 0, HL, 0);
    var oledOn = s && Math.abs(s.V[c.id]) > 2.5;
    ctx.save(); ctx.fillStyle = oledOn ? "#0a1929" : "#050505"; ctx.fillRect(-36, -20, 72, 40);
    ctx.strokeStyle = "#1e40af"; ctx.lineWidth = 2; ctx.strokeRect(-36, -20, 72, 40);
    if (oledOn) { ctx.fillStyle = "#38bdf8"; ctx.font = "bold 11px monospace"; ctx.textAlign = "left"; ctx.fillText("> " + String(c.val), -32, 4); }
    ctx.restore();
  } else if (c.type === "seven_seg_4") {
    var digitOn = s && Math.abs(s.V[c.id]) > 1.5;
    line(-HL, -12, -38, -12); line(-HL, 12, -38, 12); line(38, 0, HL, 0);
    ctx.save(); ctx.fillStyle = digitOn ? "#1e293b" : "#0f172a"; ctx.fillRect(-38, -20, 76, 40);
    ctx.strokeStyle = "#64748b"; ctx.lineWidth = 1; ctx.strokeRect(-38, -20, 76, 40);
    var digits = String(parseInt(c.val) || 0).padStart(2, "0");
    var segOn2 = { "0": [1,1,1,1,1,1,0], "1": [0,1,1,0,0,0,0], "2": [1,1,0,1,1,0,1], "3": [1,1,1,1,0,0,1], "4": [0,1,1,0,0,1,1],
                   "5": [1,0,1,1,0,1,1], "6": [1,0,1,1,1,1,1], "7": [1,1,1,0,0,0,0], "8": [1,1,1,1,1,1,1], "9": [1,1,1,1,0,1,1] };
    var segPos = [[[-14,-16],[0,-16]], [[2,-14],[2,-2]], [[2,2],[2,14]], [[-14,16],[0,16]], [[-16,2],[-16,14]], [[-16,-14],[-16,-2]], [[-14,0],[0,0]]];
    ctx.strokeStyle = digitOn ? "#ef4444" : "#450a0a"; ctx.lineWidth = 2.5;
    digits.split("").forEach(function (d, di) {
      var offX = di === 0 ? -6 : 20, onS = segOn2[d] || [];
      for (var si = 0; si < 7; si++) if (onS[si]) {
        ctx.beginPath(); ctx.moveTo(segPos[si][0][0] + offX, segPos[si][0][1]); ctx.lineTo(segPos[si][1][0] + offX, segPos[si][1][1]); ctx.stroke();
      }
    });
    ctx.restore();
  } else if (c.type === "l293d") {
    line(-HL, -12, -30, -12); line(-HL, 12, -30, 12); line(30, 0, HL, 0);
    ctx.save(); ctx.fillStyle = c.val === "STOP" ? "#475569" : "#0ea5e9"; ctx.fillRect(-30, -20, 60, 40); ctx.restore();
    ctx.strokeRect(-30, -20, 60, 40);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center";
    ctx.font = "bold 10px sans-serif"; ctx.fillText("L293D", 0, -4);
    ctx.font = "bold 9px sans-serif"; ctx.fillText(String(c.val), 0, 8); ctx.restore();
  } else if (c.type === "hc595") {
    line(-HL, -12, -25, -12); line(-HL, 12, -25, 12); line(25, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#374151"; ctx.fillRect(-25, -22, 50, 44); ctx.restore();
    ctx.strokeRect(-25, -22, 50, 44);
    ctx.save(); ctx.textAlign = "center";
    ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 9px sans-serif"; ctx.fillText("74HC595", 0, -6);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 8px monospace";
    ctx.fillText("0x" + (c.val || 1).toString(16).toUpperCase().padStart(2, "0"), 0, 8); ctx.restore();
  } else if (c.type === "ds3231") {
    line(-HL, -12, -24, -12); line(-HL, 12, -24, 12); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#1e3a8a"; ctx.fillRect(-24, -22, 48, 44); ctx.restore();
    ctx.strokeRect(-24, -22, 48, 44);
    ctx.save(); ctx.textAlign = "center";
    ctx.fillStyle = "white"; ctx.font = "bold 8px sans-serif"; ctx.fillText("DS3231", 0, -8);
    ctx.fillStyle = "#22c55e"; ctx.font = "bold 10px monospace";
    ctx.fillText(String(Math.min(23, Math.max(0, c.val))).padStart(2, "0") + ":00", 0, 8); ctx.restore();
  } else if (c.type === "optocoupler") {
    line(-HL, 0, -24, 0); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#1e293b"; ctx.fillRect(-24, -18, 48, 36); ctx.restore();
    ctx.strokeRect(-24, -18, 48, 36);
    ctx.beginPath(); ctx.moveTo(-18, 0); ctx.lineTo(-12, -6); ctx.lineTo(-12, 6); ctx.closePath(); ctx.stroke();
    line(-12, -6, -12, 6);
    ctx.save(); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 1.5; ctx.beginPath();
    ctx.moveTo(-6, -4); ctx.lineTo(0, 0); ctx.moveTo(-6, 4); ctx.lineTo(0, 0); ctx.stroke(); ctx.restore();
    ctx.beginPath(); ctx.moveTo(6, -10); ctx.lineTo(6, 10); ctx.moveTo(6, 0); ctx.lineTo(18, 0); ctx.stroke();
    line(10, -6, 10, 6);
    ctx.save(); ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 7px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(String(c.val), 0, 15); ctx.restore();
  } else if (c.type === "lm386") {
    line(-HL, -12, -25, -12); line(-HL, 12, -25, 12); line(25, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#7c3aed"; ctx.fillRect(-25, -22, 50, 44); ctx.restore();
    ctx.strokeRect(-25, -22, 50, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center";
    ctx.font = "bold 10px sans-serif"; ctx.fillText("LM386", 0, -4);
    ctx.font = "bold 8px monospace"; ctx.fillStyle = "#fbbf24"; ctx.fillText("×" + c.val, 0, 8); ctx.restore();
  } else if (c.type === "lm358" || c.type === "ne5532" || c.type === "lm393") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = c.type === "ne5532" ? "#dc2626" : (c.type === "lm393" ? "#16a34a" : "#0891b2");
    ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif";
    ctx.fillText(c.type === "ne5532" ? "NE5532" : (c.type === "lm393" ? "LM393" : "LM358"), 4, 3);
    ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 11px sans-serif";
    ctx.fillText("+", -16, -8); ctx.fillText("−", -16, 18); ctx.restore();
  } else if (c.type === "cd4017") {
    line(-HL, -12, -25, -12); line(-HL, 12, -25, 12); line(25, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#b45309"; ctx.fillRect(-25, -22, 50, 44); ctx.restore();
    ctx.strokeRect(-25, -22, 50, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 9px sans-serif"; ctx.fillText("CD4017", 0, -6);
    ctx.font = "bold 12px monospace"; ctx.fillStyle = "#fbbf24";
    ctx.fillText("Q" + (cntState[c.id] ? cntState[c.id].step : c.val), 0, 10); ctx.restore();
  } else if (c.type === "ic_74hc138") {
    line(-HL, -12, -25, -12); line(-HL, 12, -25, 12); line(25, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#7c2d12"; ctx.fillRect(-25, -22, 50, 44); ctx.restore();
    ctx.strokeRect(-25, -22, 50, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 9px sans-serif"; ctx.fillText("74HC138", 0, -6);
    ctx.font = "bold 11px monospace"; ctx.fillStyle = "#fbbf24"; ctx.fillText("Y" + c.val, 0, 10); ctx.restore();
  } else if (c.type === "tl072" || c.type === "lm324") {
    line(-HL, -12, -24, -12); line(-HL, 12, -24, 12); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = c.type === "tl072" ? "#9333ea" : "#7c3aed"; ctx.fillRect(-24, -22, 48, 44); ctx.restore();
    ctx.strokeRect(-24, -22, 48, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 9px sans-serif";
    ctx.fillText(c.type === "tl072" ? "TL072" : "LM324", 4, -2);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 7px sans-serif"; ctx.fillText(c.type === "tl072" ? "JFET" : "×4", 4, 12);
    ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 11px sans-serif"; ctx.fillText("+", -18, -8); ctx.fillText("−", -18, 18);
    ctx.restore();
  } else if (c.type === "ne556") {
    var on556 = !!(s && s.devV && s.devV[c.id] > 0);
    line(-HL, -12, -24, -12); line(-HL, 12, -24, 12); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = on556 ? "#f59e0b" : "#1e293b"; ctx.fillRect(-24, -22, 48, 44); ctx.restore();
    ctx.strokeRect(-24, -22, 48, 44);
    ctx.save(); ctx.fillStyle = on556 ? "#0f172a" : "#e2e8f0"; ctx.textAlign = "center"; ctx.font = "bold 9px sans-serif";
    ctx.fillText("NE556", 0, -2); ctx.font = "bold 7px sans-serif"; ctx.fillText("×2", 0, 12); ctx.restore();
    if (on556) {
      ctx.save(); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2;
      for (var kk = 1; kk <= 2; kk++) { ctx.globalAlpha = 0.9 - ((animT * 3 + kk * 0.5) % 1) * 0.7; ctx.beginPath(); ctx.arc(0, 0, 26 + kk * 5, -0.9, 0.9); ctx.stroke(); }
      ctx.restore();
    }
  } else if (c.type === "uln2003") {
    var ulnOn = !!(s && s.devV && s.devV[c.id] > 0);
    line(-HL, -12, -24, -12); line(-HL, 12, -24, 12); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = ulnOn ? "#0ea5e9" : "#1e293b"; ctx.fillRect(-24, -22, 48, 44); ctx.restore();
    ctx.strokeRect(-24, -22, 48, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif";
    ctx.fillText("ULN2003", 0, -2); ctx.fillStyle = "#fbbf24"; ctx.font = "bold 7px sans-serif"; ctx.fillText("×7", 0, 12); ctx.restore();
  } else if (c.type === "lm1117") {
    line(-HL, -12, -20, -12); line(-HL, 12, -20, 12); line(20, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#0891b2"; ctx.fillRect(-20, -22, 40, 44); ctx.restore();
    ctx.strokeRect(-20, -22, 40, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("LM1117", 0, -4);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 8px monospace"; ctx.fillText(c.val + "V", 0, 10); ctx.restore();
  } else if (c.type === "lm3914") {
    line(-HL, -12, -28, -12); line(-HL, 12, -28, 12); line(28, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#1e293b"; ctx.fillRect(-28, -22, 56, 44); ctx.restore();
    ctx.strokeRect(-28, -22, 56, 44);
    var vIn3914 = s ? Math.abs(s.V[c.id] || 0) : 0;
    for (var li = 0; li < 10; li++) {
      ctx.save(); ctx.fillStyle = vIn3914 > (li + 1) * (c.val / 10) ? "#22c55e" : "#334155";
      ctx.beginPath(); ctx.arc(-22 + li * 4.9, 6, 2, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    ctx.save(); ctx.fillStyle = "white"; ctx.font = "bold 7px sans-serif"; ctx.textAlign = "center"; ctx.fillText("LM3914", 0, -6); ctx.restore();
  } else if (c.type === "tda2030") {
    line(-HL, -12, -24, -12); line(-HL, 12, -24, 12); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#dc2626"; ctx.fillRect(-24, -22, 48, 44); ctx.restore();
    ctx.strokeRect(-24, -22, 48, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("TDA2030", 0, -4);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 9px monospace"; ctx.fillText("×" + c.val, 0, 9); ctx.restore();
  } else if (c.type === "lm2596") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#7c3aed"; ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("LM2596", 0, -4);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 9px monospace"; ctx.fillText(c.val + "V", 0, 9); ctx.restore();
  } else if (c.type === "tp4056") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#059669"; ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("TP4056", 0, -8);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 9px monospace"; ctx.fillText(c.val + "%", 0, 3);
    ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1; ctx.strokeRect(-16, 10, 32, 6);
    ctx.fillStyle = c.val > 50 ? "#22c55e" : "#f59e0b"; ctx.fillRect(-16, 10, 32 * (c.val / 100), 6); ctx.restore();
  } else if (c.type === "adc0804") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#0891b2"; ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("ADC0804", 0, -8);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 8px monospace";
    var adcDraw = s ? Math.round(Math.max(0, Math.min(c.val || 5, s.V[c.id] || 0)) / (c.val || 5) * 255) : 0;
    ctx.fillText("→" + adcDraw, 0, 3); ctx.restore();
    ctx.save(); ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(-18, 17);
    for (var aci = 0; aci < 4; aci++) { ctx.lineTo(-18 + aci * 9 + 4, 17 - aci * 2); ctx.lineTo(-18 + aci * 9 + 9, 17 - aci * 2); }
    ctx.stroke(); ctx.restore();
  } else if (c.type === "dac0808") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#b45309"; ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("DAC0808", 0, -8);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 8px monospace"; ctx.fillText("0x" + Number(c.val).toString(16).toUpperCase().padStart(2, "0"), 0, 3); ctx.restore();
    ctx.save(); ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(-18, 17);
    for (var dci = 0; dci < 4; dci++) { ctx.lineTo(-18 + dci * 9 + 4, 17 - dci * 2); ctx.lineTo(-18 + dci * 9 + 9, 17 - dci * 2); }
    ctx.stroke(); ctx.restore();
  } else if (c.type === "max7219") {
    var maxOn = !!(s && s.devV && s.devV[c.id] > 0);
    line(-HL, -12, -28, -12); line(-HL, 12, -28, 12); line(28, 0, HL, 0);
    ctx.save(); ctx.fillStyle = maxOn ? "#0f172a" : "#1e293b"; ctx.fillRect(-28, -22, 56, 44);
    ctx.strokeStyle = "#64748b"; ctx.lineWidth = 1; ctx.strokeRect(-28, -22, 56, 44);
    ctx.textAlign = "center"; ctx.fillStyle = "#94a3b8"; ctx.font = "bold 7px sans-serif"; ctx.fillText("MAX7219", 0, -12);
    ctx.fillStyle = maxOn ? "#ef4444" : "#450a0a"; ctx.font = "bold 13px monospace"; ctx.fillText(String(c.val).padStart(4, "0"), 0, 10); ctx.restore();
  } else if (c.type === "lm741" || c.type === "ne5534") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = c.type === "lm741" ? "#0284c7" : "#be185d"; ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif";
    ctx.fillText(c.type === "lm741" ? "LM741" : "NE5534", 4, 3);
    ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 11px sans-serif"; ctx.fillText("+", -16, -8); ctx.fillText("−", -16, 18); ctx.restore();
  } else if (c.type === "tda2822") {
    line(-HL, -12, -24, -12); line(-HL, 12, -24, 12); line(24, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#7c2d12"; ctx.fillRect(-24, -22, 48, 44); ctx.restore();
    ctx.strokeRect(-24, -22, 48, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 7px sans-serif"; ctx.fillText("TDA2822", 0, -4);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 8px monospace"; ctx.fillText("×" + c.val + "W", 0, 8); ctx.restore();
  } else if (c.type === "cd4051") {
    line(-HL, -12, -25, -12); line(-HL, 12, -25, 12); line(25, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#0e7490"; ctx.fillRect(-25, -22, 50, 44); ctx.restore();
    ctx.strokeRect(-25, -22, 50, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("CD4051", 4, -4);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 9px monospace"; ctx.fillText("CH" + (c.val || 0), 4, 8); ctx.restore();
    for (var ci = 0; ci < 8; ci++) {
      ctx.save(); ctx.fillStyle = ci === (c.val || 0) ? "#38bdf8" : "#475569";
      ctx.beginPath(); ctx.arc(-20, -14 + ci * 4, 1.3, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
  } else if (c.type === "pcf8574") {
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#15803d"; ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    var bitsStr = Number(c.val || 0).toString(2).padStart(8, "0");
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 7px sans-serif"; ctx.fillText("PCF8574", 0, -8);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 8px monospace"; ctx.fillText(bitsStr.substring(0, 4), 0, 3); ctx.fillText(bitsStr.substring(4), 0, 13); ctx.restore();
  } else if (c.type === "cd4066") {
    var swClosed = c.val === "closed";
    line(-HL, -12, -22, -12); line(-HL, 12, -22, 12); line(22, 0, HL, 0);
    ctx.save(); ctx.fillStyle = swClosed ? "#15803d" : "#475569"; ctx.fillRect(-22, -22, 44, 44); ctx.restore();
    ctx.strokeRect(-22, -22, 44, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText("CD4066", 0, -4);
    ctx.fillStyle = swClosed ? "#fbbf24" : "#94a3b8"; ctx.font = "bold 10px sans-serif"; ctx.fillText(swClosed ? "•—•" : "• ·", 0, 10); ctx.restore();
  } else if (c.type === "ws2812") {
    var wsc = RGB_COLORS[c.val] || RGB_COLORS.red;
    var wsb = s && s.ledOn[c.id] ? Math.min(1, Math.abs(cur) / 0.02) : 0;
    if (wsb > 0) {
      var gWs = ctx.createRadialGradient(0, 0, 4, 0, 0, 14 + 34 * wsb);
      gWs.addColorStop(0, wsc); gWs.addColorStop(1, "rgba(0,0,0,0)");
      ctx.save(); ctx.globalAlpha = 0.25 + 0.7 * wsb; ctx.fillStyle = gWs;
      ctx.beginPath(); ctx.arc(0, 0, 14 + 34 * wsb, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    line(-HL, 0, -20, 0); line(20, 0, HL, 0);
    ctx.save(); ctx.fillStyle = "#1e293b"; ctx.fillRect(-20, -18, 40, 36); ctx.restore();
    ctx.strokeRect(-20, -18, 40, 36);
    ctx.save(); ctx.fillStyle = wsb > 0 ? wsc : "#334155";
    ctx.beginPath(); ctx.arc(0, -4, 7, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    ctx.save(); ctx.fillStyle = "white"; ctx.font = "bold 7px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("WS2812", 0, 15); ctx.restore();
  } else if (IC12[c.type]) {
    var ic12 = IC12[c.type], icx = ic12.pm ? 4 : 0;
    line(-HL, -12, -26, -12); line(-HL, 12, -26, 12); line(26, 0, HL, 0);
    ctx.save(); ctx.fillStyle = ic12.col; ctx.fillRect(-26, -22, 52, 44); ctx.restore();
    ctx.strokeRect(-26, -22, 52, 44);
    ctx.save(); ctx.fillStyle = "white"; ctx.textAlign = "center"; ctx.font = "bold 8px sans-serif"; ctx.fillText(ic12.name, icx, -3);
    ctx.fillStyle = "#fbbf24"; ctx.font = "bold 9px monospace"; ctx.fillText(ic12.sub(c), icx, 10);
    if (ic12.pm) { ctx.fillStyle = "#e2e8f0"; ctx.font = "bold 11px sans-serif"; ctx.fillText("+", -19, -8); ctx.fillText("−", -19, 18); }
    ctx.restore();
  } else if (c.type === "switch") {
    line(-HL, 0, -16, 0); line(16, 0, HL, 0);
    ctx.beginPath(); ctx.arc(-16, 0, 3, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(16, 0, 3, 0, Math.PI * 2); ctx.fill();
    if (c.closed) line(-16, 0, 16, 0); else line(-16, 0, 12, -17);
  } else if (c.type.indexOf("gate_") === 0) {
    var hi = s && s.gateOut && s.gateOut[c.id];
    ctx.beginPath();
    if (c.type === "gate_and") {
      ctx.moveTo(-20, -15); ctx.lineTo(0, -15); ctx.arc(0, 0, 15, -Math.PI / 2, Math.PI / 2); ctx.lineTo(-20, 15); ctx.closePath();
    } else if (c.type === "gate_or") {
      ctx.moveTo(-20, -15); ctx.quadraticCurveTo(-5, -15, 10, 0); ctx.quadraticCurveTo(-5, 15, -20, 15);
      ctx.quadraticCurveTo(-10, 0, -20, -15); ctx.closePath();
    } else {
      ctx.moveTo(-15, -15); ctx.lineTo(10, 0); ctx.lineTo(-15, 15); ctx.closePath();
    }
    if (hi) { ctx.save(); ctx.fillStyle = "rgba(74,222,128,.28)"; ctx.fill(); ctx.restore(); }
    ctx.stroke();
    if (c.type === "gate_not") {
      line(-HL, 0, -15, 0); line(16, 0, HL, 0);
      ctx.beginPath(); ctx.arc(13, 0, 3, 0, Math.PI * 2); ctx.stroke();
    } else {
      line(-HL, -15, -20, -15); line(-HL, 15, -20, 15);
      line(c.type === "gate_and" ? 15 : 10, 0, HL, 0);
    }
  }

  var termNames = termList(c);

  termNames.forEach(function (w) {
    var key = c.id + "." + w, on = pending === key;
    var pos = termPos({x:0, y:0, rot:0, type:c.type}, w);
    ctx.beginPath(); ctx.arc(pos.x, pos.y, on ? 8 : 5.5, 0, Math.PI * 2);
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

function drawScope() {
  if (!scope.visible) return;
  ctx.save();
  ctx.fillStyle = "rgba(15,23,42,.92)"; ctx.strokeStyle = "#334155"; ctx.lineWidth = 2;
  ctx.fillRect(scope.x, scope.y, scope.w, scope.h); ctx.strokeRect(scope.x, scope.y, scope.w, scope.h);
  ctx.strokeStyle = "rgba(71,85,105,.5)"; ctx.lineWidth = 1;
  for (var i = 1; i < 10; i++) {
    ctx.beginPath(); ctx.moveTo(scope.x + i * (scope.w / 10), scope.y); ctx.lineTo(scope.x + i * (scope.w / 10), scope.y + scope.h); ctx.stroke();
  }
  for (var r = 1; r < 8; r++) {
    ctx.beginPath(); ctx.moveTo(scope.x, scope.y + r * (scope.h / 8)); ctx.lineTo(scope.x + scope.w, scope.y + r * (scope.h / 8)); ctx.stroke();
  }
  ctx.strokeStyle = "rgba(148,163,184,.7)";
  ctx.beginPath(); ctx.moveTo(scope.x, scope.y + scope.h / 2); ctx.lineTo(scope.x + scope.w, scope.y + scope.h / 2); ctx.stroke();
  var half = scope.h / 2, FULL = 30;
  [scope.probeA, scope.probeB].forEach(function (p) {
    if (p.data.length < 2) return;
    ctx.beginPath(); ctx.strokeStyle = p.col; ctx.lineWidth = 2;
    for (var j = 0; j < p.data.length; j++) {
      var px = scope.x + (j / scope.maxData) * scope.w;
      var py = scope.y + half - Math.max(-1, Math.min(1, p.data[j] / FULL)) * half;
      if (j === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.stroke();
  });
  ctx.fillStyle = "#94a3b8"; ctx.font = "bold 10px monospace"; ctx.textAlign = "left";
  ctx.fillText("CH1: " + (scope.probeA.key || "---"), scope.x + 5, scope.y + 12);
  ctx.fillText("CH2: " + (scope.probeB.key || "---"), scope.x + 5, scope.y + 24);
  ctx.textAlign = "right";
  ctx.fillText("±30V  slow-mo x" + TIME_SCALE, scope.x + scope.w - 5, scope.y + 12);
  ctx.restore();
  var pa = probePos(scope.probeA), pb = probePos(scope.probeB);
  ctx.save();
  ctx.lineWidth = 2; ctx.lineCap = "round";
  ctx.beginPath(); ctx.moveTo(scope.x, scope.y + 30); ctx.lineTo(pa.x, pa.y); ctx.strokeStyle = scope.probeA.col; ctx.stroke();
  ctx.beginPath(); ctx.arc(pa.x, pa.y, 6, 0, Math.PI * 2); ctx.fillStyle = scope.probeA.col; ctx.fill();
  ctx.beginPath(); ctx.moveTo(scope.x, scope.y + 50); ctx.lineTo(pb.x, pb.y); ctx.strokeStyle = scope.probeB.col; ctx.stroke();
  ctx.beginPath(); ctx.arc(pb.x, pb.y, 6, 0, Math.PI * 2); ctx.fillStyle = scope.probeB.col; ctx.fill();
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
    var live = sim && sim.ok && sim.anyCurrent && Math.abs(sim.nodeV(w.a)) > 0.05;
    var isSel = sel && sel.kind === "wire" && sel.i === i;
    ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
    ctx.lineWidth = isSel ? 5 : 3; ctx.lineCap = "round";
    ctx.strokeStyle = isSel ? "#38bdf8" : (live ? "#fbbf24" : "#64748b");
    if (live && !isSel) { ctx.setLineDash([8, 6]); ctx.lineDashOffset = -animT * 24; } else ctx.setLineDash([]);
    ctx.stroke();
  });
  ctx.setLineDash([]);
  comps.forEach(drawComp);
  drawMeter();
  drawScope();
}

/* ================================================== الحالة والرسائل ============================================== */
var statusEl = document.getElementById("status");
function setStatus(cls, msg) { statusEl.className = cls; statusEl.textContent = msg; }

function recompute(fast) {
  sim = simulate(comps, wires, simTime, animT);
  if (sim.ok && (hasAC() || has555())) { if (sim.anyCurrent) acHold = 40; else if (acHold > 0) { acHold--; sim.anyCurrent = true; } } else acHold = 0;
  var msg, cls = "";
  if (comps.length === 0) { msg = t("أضف عناصر من الشريط العلوي، ثم المس طرفَين لتوصيلهما بسلك.", "Add parts from the bar above, then tap two terminals to wire them."); }
  else if (pending) { msg = t("اختر الطرف الثاني لإكمال السلك (أو المس مكاناً فارغاً للإلغاء).", "Tap the second terminal to finish the wire (or tap empty space to cancel)."); }
  else if (!sim.ok && sim.reason === "nobattery") { cls = "warn"; msg = t("أضف بطارية أو مصدر طاقة (اردوينو/ESP32) لتشغيل الدائرة.", "Add a battery or power source (Arduino/ESP32) to power the circuit."); }
  else if (!sim.ok) { cls = "bad"; msg = t("تعذّر حل الدائرة، تحقق من التوصيلات.", "Could not solve the circuit — check the wiring."); }
  else if (sim.warnings.length) {
    var w = sim.warnings[0]; cls = "bad";
    if (w.k === "short") msg = t("⚠ قصر دائرة! المصدر " + w.id + " يعطي تياراً هائلاً.", "⚠ Short circuit! Source " + w.id + " is driving a huge current.");
    else if (w.k === "ledburn") msg = t("⚠ " + w.id + " سيحترق: التيار أعلى من 30mA — أضف مقاومة على التوالي.", "⚠ " + w.id + " would burn out: over 30 mA — add a series resistor.");
    else if (w.k === "fuse_blow") msg = t("⚠ الفيوز " + w.id + " احترق: التيار أعلى من " + w.val + "A!", "⚠ Fuse " + w.id + " blew: current over " + w.val + "A!");
    else msg = t("⚠ " + w.id + " يسخن جداً (أكثر من ربع واط).", "⚠ " + w.id + " is overheating (over 0.25 W).");
  }
  else if (!sim.anyCurrent) { cls = "warn"; msg = t("الدائرة مفتوحة: لا يمر تيار. تأكد من إغلاق الحلقة.", "Open circuit: no current. Close the loop."); }
  else {
    var b = null; for (var i = 0; i < comps.length; i++) if (isSource(comps[i])) { b = comps[i]; break; }
    cls = "ok"; msg = t("✔ الدائرة تعمل — تيار المصدر " + fmtI(sim.I[b.id]) + " عند " + b.val + "V", "✔ Circuit is live — source current " + fmtI(sim.I[b.id]) + " at " + b.val + "V");
  }
  setStatus(cls, msg);

  if (meter.visible) {
    if (meter.mode === "V") {
      var va = sim.ok && meter.probeA.key ? sim.nodeV(meter.probeA.key) : 0;
      var vb = sim.ok && meter.probeB.key ? sim.nodeV(meter.probeB.key) : 0;
      meter.reading = (va - vb).toFixed(2) + " V";
    } else if (comps.some(function (c) { return isSource(c); })) {
      meter.reading = t("أزل المصدر", "Remove source");
    } else {
      var rr = measureResistance(meter.probeA.key, meter.probeB.key);
      meter.reading = rr > 900000 ? "OL" : rr.toFixed(1) + " Ω";
    }
  }
  if (!fast) updateTools();
  updateSound();
  if (!fast) { draw(); scheduleSave(); }
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
  btnToggle.style.display = (ALIAS[c.type] === "switch" || ALIAS[c.type] === "potentiometer" || ALIAS[c.type] === "thermistor" || c.type === "switch" || c.type === "ldr" || c.type === "a3144" || c.type === "ttp223" || c.type === "tsop" || c.type === "reed_switch" || c.type === "vibration_sensor" || c.type === "tilt_switch" || c.type === "shock_sensor" || c.type === "hall_linear" || c.type === "potentiometer" || c.type === "thermistor" || c.type === "pir" || c.type === "oled_ssd1306" || c.type === "cd4017" || c.type === "ne556" || c.type === "tp4056" || c.type === "adc0804" || c.type === "dac0808" || c.type === "max7219" || c.type === "cd4051" || c.type === "pcf8574" || c.type === "cd4066" || c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017") ? "" : "none";
  btnToggle.textContent = (c.type === "tp4056" || c.type === "adc0804" || c.type === "dac0808" || c.type === "max7219" || c.type === "cd4051" || c.type === "pcf8574" || c.type === "cd4066" || c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017") ? t("القيمة التالية", "Next value") : c.type === "ne556" ? t("تغيير التردد", "Next frequency") : c.type === "cd4017" ? t("الخطوة التالية", "Next step") : c.type === "oled_ssd1306" ? t("تغيير النص", "Next text") : c.type === "pir" ? t("تبديل الحركة", "Toggle motion") : (c.type === "ldr" || c.type === "thermistor") ? t("تغيير الإضاءة", "Toggle Light") : c.type === "potentiometer" ? t("تحريك المؤشر", "Move wiper") : t("فتح/إغلاق", "Open/Close");
  btnRot.style.display = "";
}
function stepValue(dir) {
  if (!sel || sel.kind !== "comp") return;
  var c = findComp(sel.id); if (!c) return;
  var vals = TYPES[c.type].vals; if (!vals.length) return;
  snap();
  var i = vals.indexOf(c.val); if (i < 0) i = 0;
  c.val = vals[Math.max(0, Math.min(vals.length - 1, i + dir))];
  recompute();
}
btnMinus.onclick = function () { stepValue(-1); };
btnPlus.onclick = function () { stepValue(1); };
btnToggle.onclick = function () {
  var c = sel && sel.kind === "comp" ? findComp(sel.id) : null;
  if (c && ALIAS[c.type] === "potentiometer") { snap(); c.pos = ((Math.round(potPos(c) * 10) + 1) % 11) / 10; recompute(); }
  else if (c && (ALIAS[c.type] === "switch" || ALIAS[c.type] === "thermistor")) { snap(); c.closed = !c.closed; recompute(); }
  else if (c && c.type === "potentiometer") { snap(); c.pos = ((Math.round(potPos(c) * 10) + 1) % 11) / 10; recompute(); }
  else if (c && (c.type === "tp4056" || c.type === "adc0804" || c.type === "dac0808" || c.type === "max7219" || c.type === "cd4051" || c.type === "pcf8574" || c.type === "cd4066" || c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017")) {
    var nv = TYPES[c.type].vals, nvi = nv.indexOf(c.val);
    snap(); c.val = nv[(nvi + 1) % nv.length]; recompute();
  }
  else if (c && c.type === "ne556") {
    var fq = TYPES.ne556.vals, fqi = fq.indexOf(c.val);
    snap(); c.val = fq[(fqi + 1) % fq.length]; recompute();
  }
  else if (c && c.type === "cd4017") {
    var cs = cntState[c.id] || (cntState[c.id] = { step: 0, setVal: null, hi: null });
    snap(); cs.step = (cs.step + 1) % 10; c.val = cs.step; cs.setVal = c.val; recompute();
  }
  else if (c && c.type === "oled_ssd1306") {
    var oi = TYPES.oled_ssd1306.vals.indexOf(c.val);
    snap(); c.val = TYPES.oled_ssd1306.vals[(oi + 1) % TYPES.oled_ssd1306.vals.length]; recompute();
  }
  else if (c && (c.type === "switch" || c.type === "ldr" || c.type === "thermistor" || c.type === "pir" || c.type === "a3144" || c.type === "ttp223" || c.type === "tsop" || c.type === "reed_switch" || c.type === "vibration_sensor" || c.type === "tilt_switch" || c.type === "shock_sensor" || c.type === "hall_linear")) { snap(); c.closed = !c.closed; recompute(); }
};
btnRot.onclick = function () { var c = sel && sel.kind === "comp" ? findComp(sel.id) : null; if (c) { snap(); c.rot = c.rot ? 0 : 1; recompute(); } };
document.getElementById("btnDel").onclick = function () {
  if (!sel) return;
  snap();
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
  var c = { id: id || newId(type), type: type, x: x, y: y, rot: 0, val: val === undefined ? d.def : val, closed: closed === undefined ? (type !== "ldr" && type !== "pir" && type !== "a3144" && type !== "ttp223" && type !== "tsop" && type !== "reed_switch" && type !== "vibration_sensor" && type !== "tilt_switch" && type !== "shock_sensor" && type !== "hall_linear") : !!closed, pos: 0.5 };
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
(function buildPaletteBar() {
  var bar = document.getElementById("paletteBar");
  var ub = document.createElement("button"); ub.id = "btnUndo"; ub.textContent = "↶"; ub.disabled = true; ub.onclick = function () { doUndo(); };
  var rb = document.createElement("button"); rb.id = "btnRedo"; rb.textContent = "↷"; rb.disabled = true; rb.onclick = function () { doRedo(); };
  bar.appendChild(ub);
  bar.appendChild(rb);
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
  bar.appendChild(mbtn);
  var sbtn = document.createElement("button");
  sbtn.textContent = "📈 " + (AR ? "راسم إشارة" : "Oscilloscope");
  sbtn.id = "btnScope";
  sbtn.onclick = function () {
    scope.visible = !scope.visible;
    sbtn.style.background = scope.visible ? "#0284c7" : "";
    if (scope.visible && scope.probeA.x === 0 && scope.probeB.x === 0) {
      scope.probeA.x = scope.x + 20; scope.probeA.y = scope.y + scope.h + 25;
      scope.probeB.x = scope.x + 60; scope.probeB.y = scope.y + scope.h + 25;
    }
    var csvBtn = document.getElementById("btnScopeCsv");
    if (csvBtn) csvBtn.style.display = scope.visible ? "" : "none";
    recompute();
  };
  bar.appendChild(sbtn);
  var pcbBtn = document.createElement("button");
  pcbBtn.textContent = "🟩 PCB";
  pcbBtn.onclick = function () { openPcb(); };
  bar.appendChild(pcbBtn);
})();

var PALETTE_CATS = [
  { id: "basics",  ar: "أساسيات",  en: "Basics",  types: ["resistor", "potentiometer", "ldr", "thermistor", "capacitor", "inductor", "diode", "zener", "schottky", "transistor", "transistor_pnp", "mosfet_n", "relay", "fuse", "led", "rgb_led", "ws2812", "bulb", "switch", "varistor"] },
  { id: "sources", ar: "مصادر",   en: "Sources", types: ["battery", "ac_source", "arduino", "esp32", "nano", "mega", "esp8266", "pico", "solar", "dc_jack"] },
  { id: "power",   ar: "طاقة",    en: "Power",   types: ["reg7805", "reg7803", "lm317", "lm337", "lm1117", "lm2596", "ams1117", "xl6009", "tp4056"] },
  { id: "sensors", ar: "حساسات",  en: "Sensors", types: ["pir", "dht11", "ds18b20", "hc_sr04", "ds3231", "mpu6050", "bmp280", "acs712", "a3144", "ky038", "yl69", "ttp223", "ky040", "tsop", "ina219", "mq2", "bh1750", "vl53l0x", "tcs34725", "mlx90614", "max30102", "adxl345", "hx711", "dht22", "sgp30", "bme680", "tmp36", "am2320", "ds1307", "pcf8563", "bmp180", "sht31", "apds9960", "ds1302", "max6675", "max31855", "mpu9250", "vl6180x"] },
  { id: "displays", ar: "شاشات",   en: "Displays", types: ["seven_seg", "seven_seg_4", "lcd_16x2", "oled_ssd1306", "st7735", "ssd1351", "max7219", "lm3914"] },
  { id: "amps",    ar: "مضخمات",  en: "Amps",    types: ["speaker", "buzzer", "lm386", "tda2030", "tda7297", "pam8403", "max98357", "tda2822", "opamp", "lm358", "ne5532", "lm393", "tl072", "lm324", "lm741", "ne5534", "opa2134", "ad620", "opa548"] },
  { id: "motors",  ar: "محركات",  en: "Motors",  types: ["motor", "servo", "stepper_motor", "l293d", "l298n", "a4988", "drv8825", "tb6612", "bts7960", "l9110s"] },
  { id: "comms",   ar: "اتصالات", en: "Comms",   types: ["hc05", "nrf24l01", "sim800l", "rc522", "enc28j60"] },
  { id: "logic",   ar: "منطق",    en: "Logic",   types: ["gate_and", "gate_or", "gate_not", "gate_nand", "gate_xor", "gate_xnor", "hc595", "ic_74hc165", "ic_74hc138", "cd4017", "cd4013", "cd4015", "ic_74hc273", "ic_74hc373", "ic_74hc00", "cd4051", "cd4066", "pcf8574", "mcp23017", "at24c32", "sd_card", "tca9548a", "adc0804", "dac0808", "ads1115", "mcp4725", "ad9833", "timer555", "ne556", "uln2003", "uln2803", "tlc5940", "pca9685", "optocoupler"] },
  { id: "other",   ar: "أخرى",    en: "Other",   types: [] }
];
var activeCat = "basics";

function paletteRenderTabs() {
  var tabs = document.getElementById("paletteTabs");
  tabs.innerHTML = "";
  PALETTE_CATS.forEach(function (cat) {
    var b = document.createElement("button");
    b.textContent = AR ? cat.ar : cat.en;
    b.className = cat.id === activeCat ? "active" : "";
    b.onclick = function () { activeCat = cat.id; paletteRenderTabs(); paletteRenderButtons(); };
    tabs.appendChild(b);
  });
}

function paletteGetActiveTypes() {
  var cat = null;
  for (var i = 0; i < PALETTE_CATS.length; i++) if (PALETTE_CATS[i].id === activeCat) { cat = PALETTE_CATS[i]; break; }
  if (!cat) return [];
  if (cat.id === "other") {
    var used = {};
    PALETTE_CATS.forEach(function (cc) { if (cc.id !== "other") cc.types.forEach(function (t) { used[t] = 1; }); });
    Object.keys(PALETTE_EXTRA).forEach(function (k) { PALETTE_EXTRA[k].forEach(function (t) { used[t] = 1; }); });
    return Object.keys(TYPES).filter(function (t) { return !used[t]; });
  }
  var extra = PALETTE_EXTRA[cat.id] || [];
  return cat.types.concat(extra).filter(function (t) { return !!TYPES[t]; });
}

var PALETTE_EXTRA = {
  sensors: ["sht10", "sht75", "si7021", "bme280", "mpl3115a2", "mq3", "mq4", "mq5", "mq6", "mq7", "mq8", "mq9", "mq135", "gp2y1010", "tsl2561", "tcs3200", "reed_switch", "vibration_sensor", "water_level", "flex_sensor", "tilt_switch", "shock_sensor", "flame_sensor", "rain_sensor", "hall_linear", "ds3234", "rv3028", "mcp7940"],
  logic: ["cd4071", "cd4081", "cd4030", "cd4001", "cd4023", "cd4025", "cd4070", "cd4075", "cd4077", "cd4093", "cd4538", "cd4047", "cd4027", "cd4029", "cd4076", "cd4022", "cd4060", "cd4541", "cd4511", "cd4028", "mcp3008", "mcp3208", "ads1015", "pcf8591", "tlc5615", "mcp4921", "at24c256", "at24c512", "w25q64", "mb85rc"],
  displays: ["nokia5110", "ssd1309", "st7565", "st7920", "ili9341", "ili9486", "max6954", "lcd_20x4", "st7735_160", "ssd1331"],
  motors: ["drv8833", "drv8871", "l293e", "sn754410", "uln2004", "mc33926", "bd6221", "tb67h420", "a3959", "drv8824"],
  comms: ["esp01", "rn2483", "rfm69", "rfm95", "hc12", "xbee", "sim900", "m95", "nrf905", "cc1101"],
  power: ["lm7809", "lm7812", "lm7905", "lm7912", "lm1084", "lm2678", "lm5007", "mcp1700", "mic5205", "lp2985"],
  amps: ["lm4871", "tda2003"]
};

(function addBatch19Palette() {
  var add = {"sensors": ["ds18s20", "lm35", "lm75", "tmp102", "mcp9808", "max31865", "ads1118", "hdc1080", "htu21d", "sht21", "sht35", "aht10", "aht20", "ms5611", "lps25h", "bmp388", "dps310", "bmp085", "lps22hb", "mpx5700", "mq131", "mq303", "mhz19", "sds011", "pms5003", "ccs811", "ens160", "si1145", "veml7700", "opt3001", "max44009", "ltr329", "ml8511", "veml6070", "ina226", "ina260", "ina3221", "lis3dh", "mma8452", "adxl335", "adxl362", "lsm6ds3", "icm20948", "bno055", "hmc5883l", "qmc5883l", "mlx90393"], "power": ["lm7815", "lm7824", "lm7808", "lm7806", "lm317hv", "lm2940", "tps7a47", "lm2576", "lm2574", "mp1584", "tps5430", "mt3608", "lm2577", "tps61023", "max1771"], "amps": ["lm3886", "tda7294", "tda2050", "tda7377", "tpa3116", "tpa2005", "lm4766"], "motors": ["drv8434", "tmc2209", "tmc2130", "l6470", "vnh5019", "drv8313", "a4950", "mx1508"], "comms": ["esp32cam", "sx1278", "sx1276", "nrf52832", "hm10", "jdy23", "ublox_neo6m", "ublox_neo7m", "w5500", "cp2102", "ch340", "max485", "mcp2515"], "displays": ["ssd1322", "ssd1327", "ssd1306_64", "st7789", "ili9488", "hd44780", "tm1637", "ht16k33"], "logic": ["cd4017b", "ic_74hc14", "ic_74hc04", "ic_74hc08", "ic_74hc32", "ic_74hc86", "ic_74hc74", "ic_74hc590", "ic_74hc4067", "at24c64", "at24c128", "w25q128", "fm25v02", "mcp23s17", "tca9534", "max7301"]};
  Object.keys(add).forEach(function (k) { PALETTE_EXTRA[k] = (PALETTE_EXTRA[k] || []).concat(add[k]); });
})();

(function addBatch20Palette() {
  var add = {"sensors": ["tmp117", "max30205", "amg8833", "mlx90640", "lm73", "si7050", "ds28ea00", "ad8495", "hih6130", "dht21", "sht40", "sht45", "hdc2080", "bme688", "bmp390", "bmp581", "lps35hw", "lps33hw", "spl06", "ms5837", "mq137", "mq138", "mq214", "mq216", "scd30", "scd40", "scd41", "sgp40", "sen54", "ags02ma", "as7341", "as7262", "tsl2591", "veml6075", "guva_s12sd", "bh1745", "isl29125", "apds9306", "mpu6500", "lsm9ds1", "lsm303", "l3gd20h", "bmi160", "bmi270", "adxl375", "icm42688", "lis2dh12", "kxtj3", "vl53l1x", "gp2y0a21", "gp2y0a02", "us100", "a02yyuw", "ld2410", "rcwl0516", "tfmini", "tf_luna", "vcnl4040", "jsn_sr04t", "max30100", "ad8232", "pulse_sensor", "gsr_sensor", "r307", "ina169", "acs758", "max471", "pzem004t", "hlw8012", "ina228", "ina238", "ss49e", "a1302", "drv5053", "as5600", "as5048a"], "displays": ["sh1106", "ssd1305", "gc9a01", "st7796", "ili9225", "ssd1963", "epd_154", "epd_213", "epd_29", "lcd_12864", "lcd_16x4", "lcd_8x2", "tm1638", "ht1621"], "motors": ["drv8847", "drv8880", "tmc2208", "tmc2160", "tmc5160", "l6208", "l6235", "vnh2sp30", "ibt2", "lv8548"], "power": ["lm7818", "lm78l05", "lm79l05", "lm317l", "lm350", "ld1117", "xc6206", "ap2112", "tlv1117", "lt3045", "lm2575", "lm2595", "xl4015", "xl4005", "xl7005", "mp2307", "mp2315", "tps54331", "sx1308", "cn3791", "bq24074", "tp5100", "ip5306"], "comms": ["esp32_c3", "esp32_s3", "nrf52840", "hc06", "hm11", "jdy31", "e32", "sx1262", "dw1000", "pn532", "w5100", "enc424j600", "mcp2551", "tja1050", "sn65hvd230", "max232", "max3232", "ft232", "pl2303", "cp2104", "l76k", "neo_m8n", "sim7600", "sim868", "a7670"], "logic": ["ic_74hc02", "ic_74hc10", "ic_74hc20", "ic_74hc30", "ic_74hc125", "ic_74hc157", "ic_74hc151", "ic_74hc139", "ic_74hc154", "ic_74hc161", "ic_74hc164", "ic_74hc166", "ic_74hc174", "ic_74hc175", "ic_74hc193", "ic_74hc244", "ic_74hc245", "ic_74hc283", "ic_74hc374", "ic_74hc4040", "ic_74hc4046", "ic_74hc4053", "ic_74hc4094", "mcp23008", "tca9535", "txs0108", "sn74lvc245", "at24c02", "at24c08", "at24c16"], "amps": ["lm1875", "tda2040", "tda7498", "tpa3110", "pam8610", "pam8302", "max9744", "mcp6002", "mcp6022", "tl082", "tl084", "lf353", "lf411", "op07", "op27", "ad8605"]};
  Object.keys(add).forEach(function (k) { PALETTE_EXTRA[k] = (PALETTE_EXTRA[k] || []).concat(add[k]); });
  PALETTE_CATS.splice(1, 0, { id: "parts", ar: "مكونات", en: "Parts", types: ["elec_cap", "tantalum_cap", "ceramic_cap", "supercap", "fast_diode", "rectifier_diode", "germanium_diode", "zener_1w", "tvs_diode", "schottky_ss34", "ntc", "polyfuse", "power_resistor", "shunt_resistor", "trimmer_pot", "slide_pot", "rheostat", "q_tip120", "q_tip31", "q_bc547", "q_2n2222", "q_2n3904", "q_bd139", "q_bc557", "q_2n3906", "q_tip32", "q_tip127", "q_bd140", "m_irf540", "m_irlz44n", "m_2n7000", "m_irf3205", "m_irlb8721", "power_inductor", "ferrite_choke", "halogen_lamp", "dc_fan", "vibration_motor", "piezo_buzzer", "headphones", "push_button", "toggle_switch", "slide_switch", "limit_switch", "lipo_battery", "aa_cell", "coin_cell", "nine_volt", "usb_power", "bench_supply", "lead_acid"] });
})();

(function addBatch21Palette() {
  var add = {"sensors": ["tmp116", "tmp1075", "max6633", "mcp9701", "lm19", "lm34", "lm335", "ad590", "tmp35", "tmp37", "sts31", "stlm20", "sht85", "hih7130", "hts221", "hdc3020", "shtc3", "shtc1", "si7020", "am2301", "am2302", "capacitive_soil", "fc28", "lps22hh", "mpl115a2", "ms5803", "ms5607", "mprls", "bmp384", "icp10125", "icp20100", "mpx4115", "mpxv7002", "xgzp6847", "mq136", "mq139", "mq309", "tgs2600", "tgs2602", "tgs2620", "mics5524", "mics6814", "mh_z14a", "mh_z16", "s8_co2", "iaq_core", "zmod4410", "zh03b", "tsl2572", "veml3235", "opt4048", "opt3004", "ltr390", "ltr303", "ltr559", "as7343", "as7265x", "ap3216", "vcnl4200", "si1133", "mpu6886", "mpu9255", "lsm6dso", "lsm6dsox", "lis3mdl", "lis2mdl", "lis3dsh", "mma7660", "mma8451", "mma7361", "bma280", "bma423", "bmi088", "bmx160", "icm20689", "icm42605", "fxos8700", "fxas21002", "l3g4200d", "itg3200", "vl53l4cd", "vl53l3cx", "tof050c", "tf02", "tf03", "hcsr05", "srf05", "maxsonar_ez1", "us015", "us020", "urm37", "ld2450", "ld2420", "hb100", "sen0311", "max30101", "max86150", "afe4490", "ads1292", "ad8233", "max30003", "emg_sensor", "muscle_v3", "gsr_grove", "skin_temp_mlx", "ina180", "ina199", "ina210", "ina230", "ina233", "acs711", "acs723", "acs724", "acs781", "max9611", "ltc4151", "ltc2945", "pac1934", "bl0937", "pzem017", "ade7753", "atm90e26", "hmc5983", "mmc5603", "mmc5983ma", "ak8963", "ak09916", "qmc6310", "bmm150", "tmag5273", "tlv493d", "a1324", "ss495a", "drv5055", "as5047p", "ma730", "mt6701", "max9814", "max4466", "ics43434", "inmp441", "sph0645", "spm0405", "mp34dt05", "ky037", "fsr402", "fsr406", "load_cell_5kg", "load_cell_20kg", "piezo_film", "flex_4in", "yfs201", "yfs401", "yfs210", "yfb08", "fs300a", "fs400a", "float_switch", "ultrasonic_level", "capacitive_level", "optical_level", "soil_moisture_v2"], "displays": ["st7567", "st7789_135", "st7735_80", "ili9163", "ili9327", "ili9342", "ili9806", "hx8357", "hx8347", "ra8875", "ssd1289", "ssd2119", "sed1520", "ks0108", "pcd8544", "uc1701", "uc1609", "t6963c"], "motors": ["drv8701", "drv8424", "drv8428", "tmc2100", "tmc2226", "tmc2225", "tmc2240", "tmc2660", "a4982", "a4983", "l6219", "l297", "l298p", "tb6560", "tb6600", "tb67s109"], "power": ["lm78m05", "lm2937", "lm2931", "lm1086", "lm1085", "lt1763", "lt1963", "lt3042", "tps7a20", "tps73401", "adp150", "adp3338", "mcp1802", "mcp1826", "ap7361", "ap7333", "rt9013", "ld39050", "tlv70033", "lm22676", "lm2672", "lm2674", "lm5008", "lm5164", "ltc3630", "ltc3115", "tps54360", "tps62130", "tps62160", "tps62933", "mp1470", "mp2359", "mp2491", "xl1509", "xl2596", "mc34063", "tps63020", "tps61088", "tps61230", "mp3429", "xl6019", "xl6012", "ap3012", "lm2621", "lm3478", "tps55340", "tps61200", "tp4057", "tp4054", "mcp73831", "mcp73832", "bq24072", "bq24075", "bq25606", "bq25895", "ltc4054", "ltc4065", "cn3722", "cn3765", "ip2312", "ip5310"], "comms": ["esp32_wroom", "esp32_s2", "esp32_c6", "esp12f", "esp12e", "esp07", "bl602", "rtl8710", "rtl8720dn", "nrf51822", "nrf52810", "nrf5340", "nrf9160", "cc2530", "cc2531", "cc2640", "cc2652", "cc3200", "cc1310", "cc1125", "cc2500", "si4432", "si4463", "si4455", "sx1280", "sx1272", "sx1301", "rfm12b", "rfm22b", "rfm98", "rfm96", "rfm63", "xbee_pro", "xbee3", "bl654", "ch341", "ch9102", "ch343", "cp2102n", "ft231x", "ft2232", "ft232h", "mcp2221", "max3485", "sp3485", "sn65hvd72", "ltc2850", "iso1176", "adm2587", "adm3053", "mcp2562", "tcan1042", "tja1051", "sn65hvd1050", "l80", "l86", "atgm336h", "gt_u7", "neo_m9n", "zoe_m8q", "max_m10s", "teseo_liv3", "mtk3339", "pa1010d", "sim28", "l96", "sim800c", "sim808", "sim5320", "sim7000", "sim7070", "sim7080", "sim7500", "sim7670", "ec200s", "ec25", "bg95", "bg96", "m26", "ec21", "ec600", "a9g", "a6", "a7672e"], "logic": ["ic_74hc03", "ic_74hc05", "ic_74hc09", "ic_74hc21", "ic_74hc27", "ic_74hc51", "ic_74hc58", "ic_74hc85", "ic_74hc107", "ic_74hc109", "ic_74hc112", "ic_74hc123", "ic_74hc126", "ic_74hc132", "ic_74hc137", "ic_74hc147", "ic_74hc148", "ic_74hc153", "ic_74hc158", "ic_74hc160", "ic_74hc162", "ic_74hc163", "ic_74hc168", "ic_74hc169", "ic_74hc173", "ic_74hc182", "ic_74hc190", "ic_74hc191", "ic_74hc192", "ic_74hc194", "ic_74hc195", "ic_74hc238", "ic_74hc239", "ic_74hc240", "ic_74hc241", "ic_74hc251", "ic_74hc253", "ic_74hc257", "ic_74hc258", "ic_74hc259", "cd4000", "cd4002", "cd4006", "cd4007", "cd4008", "cd4009", "cd4010", "cd4011", "cd4012", "cd4014", "cd4016", "cd4018", "cd4019", "cd4020", "cd4021", "cd4024", "cd4026", "cd4033", "cd4034", "cd4035", "cd4040", "cd4042", "cd4043", "cd4044", "cd4049", "cd4050", "cd4052", "cd4053", "cd4069", "cd4072", "cd4073", "cd4078", "cd4082", "cd4094", "cd4099", "cd40106", "cd40193", "cd4585", "tlc555", "icm7555", "lmc555", "xr2206", "icl8038", "max038", "lm566", "lm567", "ne565", "ne567", "at24c01", "at24c04", "at24cm01", "at24cm02", "m24c64", "m24256", "w25q16", "w25q32", "w25q80", "w25q256", "w25q512", "mx25l1606", "mx25l3206", "mx25l6406", "mx25l12805", "sst25vf016", "s25fl064", "is25lp128", "gd25q32", "gd25q64", "fm24cl64", "fm24v10", "fm25cl64", "mb85rs64", "mb85rs256", "mcp23k256", "sram_23lc1024", "sram_23lc512", "sram_23k256", "c93c46", "c93c56", "c93c66", "c93c86", "at25010", "at25640", "at25m01", "sdram_is42s16160", "sdram_w9825g6", "psram_aps6404", "psram_ips6404", "nand_w25n01", "nand_mt29f", "emmc_4gb"], "amps": ["lm1876", "lm2877", "lm3875", "lm4780", "tda1514", "tda1521", "tda2005", "tda2006", "tda2009", "tda7240", "tda7266", "tda7293", "tda7296", "tda7379", "tda7384", "tda7388", "tda7391", "tpa3118", "tpa3123", "tpa3128", "tpa3130", "tpa3140", "tpa3220", "max9768", "max9788", "max98400", "ssm3582", "stk4141", "pam8620", "lm4950", "lm4991", "tpa6120", "tpa6132", "tpa6211", "tpa2012", "tpa2031", "pam8406", "pam8304", "ssm2302", "lm833", "lm4562", "lm4558", "lm1458", "opa134", "opa227", "opa277", "opa337", "opa343", "opa350", "opa551", "opa564", "opa1612", "opa1656", "opa1678", "opa2604", "opa2350", "ad8066", "ad8397", "ad797", "ad8099", "ad8221", "ad8276", "ad8429", "ad8606", "ad8628", "lt1013", "lt1028", "lt1124", "lt1677", "lt6015", "lmv358", "lmv321", "lmv324", "lmc6482", "lmc662", "lmp7701", "mcp6001", "mcp6004", "mcp6231", "mcp6241", "mcp6271", "tlv2371", "tlv2462", "tlv271", "tlv9061", "tlv9062", "ca3140", "ca3130"]};
  Object.keys(add).forEach(function (k) { PALETTE_EXTRA[k] = (PALETTE_EXTRA[k] || []).concat(add[k]); });
  PALETTE_CATS.forEach(function (c) { if (c.id === "parts") c.types = c.types.concat(["led_white", "led_blue", "led_green", "led_yellow", "led_red", "photocell", "schottky_1n5817", "schottky_sb340", "schottky_mbr1045", "zener_0w5", "zener_5w", "tvs_smbj", "diode_1n4001", "diode_1n4004", "diode_1n5408", "diode_uf4007", "diode_1n34a", "film_cap", "mica_cap", "polymer_cap", "bipolar_cap", "mkp_cap", "x2_cap", "y_cap", "trimmer_cap", "carbon_resistor", "metal_film_resistor", "wirewound_resistor", "smd_resistor", "fusible_resistor", "pullup_resistor", "current_sense_res", "high_value_resistor", "multiturn_pot", "log_pot", "volume_pot", "joystick_axis", "ntc_probe", "q_bc337", "q_s8050", "q_c945", "q_2n3055", "q_mje3055", "q_tip41c", "q_bd137", "q_2sc1815", "q_2sc5200", "q_2n5551", "q_mpsa42", "q_bc639", "q_2n2907", "q_bc327", "q_s8550", "q_a1015", "q_tip42c", "q_2sa1943", "q_2n5401", "q_mpsa92", "q_bc640", "q_bd138", "m_irf520", "m_irf640", "m_irfz44n", "m_irf1404", "m_ao3400", "m_fqp30n06", "m_stp55nf06", "m_irlml2502", "m_irf530", "m_irlb3034", "m_si2302", "m_bss138", "toroid_inductor", "air_coil", "smd_inductor", "common_mode_choke", "incandescent_lamp", "led_bulb", "heating_element", "water_pump", "n20_motor", "gear_motor", "mini_speaker", "woofer", "tweeter", "active_buzzer", "passive_buzzer", "siren", "dip_switch", "rocker_switch", "key_switch", "micro_switch", "foot_switch", "selector_switch", "li_ion_18650", "nimh_pack", "car_battery", "wall_adapter", "solar_panel_5v", "usb_c_pd", "powerbank", "dry_cell_d", "lifepo4", "button_cell_lr44", "ac_transformer", "ac_generator"]); });
})();

function paletteRenderButtons() {
  var box = document.getElementById("paletteButtons");
  box.innerHTML = "";
  var types = paletteGetActiveTypes();
  if (types.length === 0) {
    var empty = document.createElement("span");
    empty.style.cssText = "padding:6px 10px;color:#64748b;font-size:12.5px";
    empty.textContent = AR ? "لا عناصر هنا" : "Nothing here";
    box.appendChild(empty);
    return;
  }
  types.forEach(function (type) {
    var b = document.createElement("button");
    b.textContent = "+ " + (AR ? TYPES[type].ar : TYPES[type].en);
    b.onclick = function () {
      snap();
      var p = freeSpot(), c = addComp(type, p.x, p.y);
      if (c) { sel = { kind: "comp", id: c.id }; pending = null; recompute(); }
    };
    box.appendChild(b);
  });
}

(function initPalette() {
  var used = {};
  PALETTE_CATS.forEach(function (c) { if (c.id !== "other") c.types.forEach(function (t) { used[t] = 1; }); });
  var extras = Object.keys(TYPES).filter(function (t) { return !used[t]; });
  if (extras.length === 0) {
    PALETTE_CATS = PALETTE_CATS.filter(function (c) { return c.id !== "other"; });
  }
  paletteRenderTabs();
  paletteRenderButtons();
})();

/* ======================================================== اللمس ================================================== */
var drag = null;
function evPos(e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
function hitTerminal(p) {
  var best = null, bd = 20;
  comps.forEach(function (c) {
    var termNames = termList(c);
    termNames.forEach(function (w) {
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
    if (Math.hypot(pA.x - p.x, pA.y - p.y) < 20) { drag = { mode: "probe", target: "meterA", sx: p.x, sy: p.y }; return; }
    if (Math.hypot(pB.x - p.x, pB.y - p.y) < 20) { drag = { mode: "probe", target: "meterB", sx: p.x, sy: p.y }; return; }
    if (p.x > meter.x + 10 && p.x < meter.x + 40 && p.y > meter.y + 30 && p.y < meter.y + 52) { meter.mode = "V"; recompute(); return; }
    if (p.x > meter.x + 45 && p.x < meter.x + 75 && p.y > meter.y + 30 && p.y < meter.y + 52) { meter.mode = "R"; recompute(); return; }
    if (p.x > meter.x && p.x < meter.x + meter.w && p.y > meter.y && p.y < meter.y + meter.h) { drag = { mode: "meter", ox: p.x - meter.x, oy: p.y - meter.y, sx: p.x, sy: p.y }; return; }
  }
  if (scope.visible) {
    var sA = probePos(scope.probeA), sB = probePos(scope.probeB);
    if (Math.hypot(sA.x - p.x, sA.y - p.y) < 20) { drag = { mode: "probe", target: "scopeA", sx: p.x, sy: p.y }; return; }
    if (Math.hypot(sB.x - p.x, sB.y - p.y) < 20) { drag = { mode: "probe", target: "scopeB", sx: p.x, sy: p.y }; return; }
    if (p.x > scope.x && p.x < scope.x + scope.w && p.y > scope.y && p.y < scope.y + scope.h) { drag = { mode: "scope", ox: p.x - scope.x, oy: p.y - scope.y, sx: p.x, sy: p.y }; return; }
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
  if (drag.mode === "scope") { scope.x = p.x - drag.ox; scope.y = p.y - drag.oy; draw(); return; }
  if (drag.mode === "probe") {
    var pr = probeByTarget(drag.target);
    pr.x = p.x; pr.y = p.y; pr.key = null; draw(); return;
  }
  if (drag.mode !== "comp") return;
  if (!drag.moved && Math.hypot(p.x - drag.sx, p.y - drag.sy) < 6) return;
  if (!drag.moved) snap();
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
  if (d.mode === "meter" || d.mode === "scope") { scheduleSave(); return; }
  if (d.mode === "probe") {
    var tkp = hitTerminal(p);
    var pr2 = probeByTarget(d.target); pr2.key = tkp; if (d.target.indexOf("scope") === 0) pr2.data = [];
    recompute(); return;
  }
  if (d.mode === "comp") {
    if (!moved && !d.moved) {
      var c = findComp(d.id);
      if (c) {
        if (c.type === "switch" || c.type === "ldr" || c.type === "pir" || c.type === "a3144" || c.type === "ttp223" || c.type === "tsop" || c.type === "reed_switch" || c.type === "vibration_sensor" || c.type === "tilt_switch" || c.type === "shock_sensor" || c.type === "hall_linear") { snap(); c.closed = !c.closed; }
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
      if (!dup && wires.length < MAX_WIRES) { snap(); wires.push({ a: pending, b: d.key }); }
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
function serialize() { return JSON.stringify({ comps: comps, wires: wires, meter: meter, scope: scopeState() }); }
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
    if (!/^[A-Za-z][A-Za-z0-9]{0,8}$/.test(id) || seen[id]) id = null;
    var d = TYPES[c.type], val = c.val;
    if (d.vals.length) {
      if (typeof d.vals[0] === "string") { if (d.vals.indexOf(val) < 0) val = d.def; }
      else { val = Number(val); if (d.vals.indexOf(val) < 0) { var best = d.vals[0]; d.vals.forEach(function (v) { if (Math.abs(v - val) < Math.abs(best - val)) best = v; }); val = isNaN(val) ? d.def : best; } }
    } else val = 0;
    var item = { id: id, type: c.type, x: Number(c.x), y: Number(c.y), rot: c.rot ? 1 : 0, val: val, closed: c.closed === undefined ? (c.type !== "ldr" && c.type !== "pir" && c.type !== "a3144" && c.type !== "ttp223" && c.type !== "tsop" && c.type !== "reed_switch" && c.type !== "vibration_sensor" && c.type !== "tilt_switch" && c.type !== "shock_sensor" && c.type !== "hall_linear") : !!c.closed, pos: isFinite(c.pos) ? Math.max(0, Math.min(1, Number(c.pos))) : 0.5 };
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
    var ok = function (k) { return typeof k === "string" && /^[A-Za-z][A-Za-z0-9]{0,8}\.(?:a|b|c|out)$/.test(k) && seen[k.split(".")[0]]; };
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
  snap();
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
  if (!forceLayout && obj.scope && typeof obj.scope === "object") {
    var sc = obj.scope;
    scope.visible = !!sc.visible;
    scope.x = isFinite(sc.x) ? Number(sc.x) : 10; scope.y = isFinite(sc.y) ? Number(sc.y) : 150;
    ["probeA", "probeB"].forEach(function (k) {
      var pr = sc[k] || {};
      scope[k].x = isFinite(pr.x) ? Number(pr.x) : 0; scope[k].y = isFinite(pr.y) ? Number(pr.y) : 0;
      scope[k].key = (typeof pr.key === "string" && keyPos(pr.key)) ? pr.key : null;
      scope[k].data = [];
    });
  }
  ["probeA", "probeB"].forEach(function (k) {
    if (meter[k].key && !keyPos(meter[k].key)) meter[k].key = null;
    if (scope[k].key && !keyPos(scope[k].key)) scope[k].key = null;
  });
  var sbt = document.getElementById("btnScope");
  if (sbt) sbt.style.background = scope.visible ? "#0284c7" : "";
  var mb = document.getElementById("btnMeter");
  if (mb) mb.style.background = meter.visible ? "#0284c7" : "";
  recompute();
  return true;
}
var demoN = 0;
function demo() { var k = demoN++ % 3; if (k === 1) demoAc(); else if (k === 2) demoRelay(); else demoLed(); }
function demoRelay() {
  loadState({
    comps: [
      { id: "B1", type: "battery", val: 5 }, { id: "S1", type: "switch", closed: false }, { id: "K1", type: "relay", val: 5 },
      { id: "R1", type: "resistor", val: 330 }, { id: "D1", type: "led", val: "red" }
    ],
    wires: [["B1.a", "S1.a"], ["S1.b", "K1.a"], ["K1.b", "B1.b"], ["B1.a", "K1.c"], ["K1.out", "R1.a"], ["R1.b", "D1.a"], ["D1.b", "B1.b"]]
  }, true);
}
function demoAc() {
  loadState({
    comps: [{ id: "AC1", type: "ac_source", val: 12 }, { id: "E1", type: "diode", val: "silicon" }, { id: "R1", type: "resistor", val: 1000 }],
    wires: [["AC1.a", "E1.a"], ["E1.b", "R1.a"], ["R1.b", "AC1.b"]]
  }, true);
  scope.visible = true; scope.x = 10; scope.y = Math.max(150, cssH - scope.h - 40);
  scope.probeA.key = "AC1.a"; scope.probeB.key = "R1.a"; scope.probeA.data = []; scope.probeB.data = [];
  var sbt = document.getElementById("btnScope");
  if (sbt) sbt.style.background = "#0284c7";
  recompute();
}
function demoLed() {
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
var busyEl = document.getElementById("busy"), btnGen = document.getElementById("btnGen"), btnExplain = document.getElementById("btnExplain"), btnFix = document.getElementById("btnFix"), btnCode = document.getElementById("btnCode");
function setBusy(v) { busyEl.className = v ? "show" : ""; btnGen.disabled = btnExplain.disabled = btnFix.disabled = btnCode.disabled = v; }
function compDesc(c, withSim) {
  var o = { id: c.id, type: c.type, value: c.val };
  if (c.type === "switch" || c.type === "ldr") o.closed = c.closed;
  if (c.type === "potentiometer") o.pos = potPos(c);
  if (withSim && sim && sim.ok) { o.voltage_V = +sim.V[c.id].toFixed(3); o.current_A = +sim.I[c.id].toFixed(5); }
  return o;
}

btnGen.onclick = function () {
  var txt = document.getElementById("aiText").value.trim();
  if (!txt) { setStatus("warn", t("اكتب وصف الدائرة أولاً.", "Describe the circuit first.")); return; }
  setBusy(true);
  askAi("generate", txt).then(function (reply) {
    var obj = extractJson(reply);
    if (!obj || !loadState(obj, true)) throw new Error(t("لم أستطع فهم رد الذكاء الاصطناعي، جرّب وصفاً آخر.", "Could not understand the AI reply — try another description."));
  }).catch(function (e) { setStatus("bad", e.message || String(e)); }).then(function () { setBusy(false); });
};

btnExplain.onclick = function () {
  if (comps.length === 0) { setStatus("warn", t("لا توجد دائرة لشرحها.", "There is no circuit to explain.")); return; }
  var desc = { components: comps.map(function (c) { return compDesc(c, true); }),
               wires: wires.map(function (w) { return [w.a, w.b]; }) };
  setBusy(true);
  askAi("explain", JSON.stringify(desc)).then(function (reply) {
    document.getElementById("answerText").textContent = reply;
    document.getElementById("answer").className = "show";
  }).catch(function (e) { setStatus("bad", e.message || String(e)); }).then(function () { setBusy(false); });
};

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
    components: comps.map(function (c) { return compDesc(c, false); }),
    wires: wires.map(function (w) { return [w.a, w.b]; })
  };

  askAi("fix", JSON.stringify(desc)).then(function (reply) {
    var obj = extractJson(reply);
    if (!obj || !loadState(obj, true)) throw new Error(t("لم أستطع إصلاح الدائرة، حاول تعديلها يدوياً.", "Could not fix the circuit, try editing it manually."));
    setStatus("ok", t("تم إصلاح الدائرة بنجاح! 🪄", "Circuit fixed successfully! 🪄"));
  }).catch(function (e) { setStatus("bad", e.message || String(e)); }).then(function () { setBusy(false); });
};

btnCode.onclick = function () {
  if (comps.length === 0) { setStatus("warn", t("لا توجد دائرة لتوليد كود لها.", "No circuit to generate code for.")); return; }
  var desc = { components: comps.map(function (c) { return compDesc(c, false); }), wires: wires.map(function (w) { return [w.a, w.b]; }) };
  setBusy(true);
  askAi("arduino_code", JSON.stringify(desc)).then(function (reply) {
    document.getElementById("answerText").textContent = reply.replace(/^\s*```[a-zA-Z+]*\n?/, "").replace(/```\s*$/, "");
    document.getElementById("answer").className = "show";
  }).catch(function (e) { setStatus("bad", e.message || String(e)); }).then(function () { setBusy(false); });
};

document.getElementById("btnAnswerClose").onclick = function () { document.getElementById("answer").className = ""; };

/* ================================================== الحفظ السحابي ============================================== */
window.onCloudSaved = function(code, error) {
  if (error === 'no_license') {
    setStatus("warn", t("يتطلب الحفظ السحابي ترخيصاً مفعّلاً. اشحن رصيدك من الشاشة الرئيسية.",
                        "Cloud saving requires an active license. Top up from the main screen."));
  } else if (error === 'no_server') {
    setStatus("bad", t("لم يتم ضبط رابط الخادم.", "Server URL is not configured."));
  } else if (error === 'network_error') {
    setStatus("bad", t("تعذّر الاتصال بالسحابة. تحقق من الإنترنت.",
                       "Could not reach the cloud. Check your connection."));
  } else if (code && code.length > 0) {
    prompt(t("تم الحفظ بنجاح! انسخ هذا الكود لاستعادتها لاحقاً:",
             "Saved! Copy this code to restore it later:"), code);
  } else {
    setStatus("bad", t("تعذّر الحفظ في السحابة.",
                       "Could not save to cloud."));
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
  var state = serialize();
  try { if (window.Android && Android.saveCloud) Android.saveCloud(state); else setStatus("warn", t("غير مدعوم هنا.", "Not supported here.")); } catch(e) {}
};
document.getElementById("btnLoad").onclick = function() {
  var code = prompt(t("أدخل كود التحميل المكون من 6 أحرف:", "Enter the 6-letter load code:"));
  if (code && code.trim().length > 0) {
    try { if (window.Android && Android.loadCloud) Android.loadCloud(code.trim().toUpperCase()); else setStatus("warn", t("غير مدعوم هنا.", "Not supported here.")); } catch(e) {}
  }
};

/* ====================================================== أزرار الرأس ============================================== */
window.onImageSaved = function (ok) {
  setStatus(ok ? "ok" : "bad", ok ? t("تم حفظ الصورة في المعرض (Pictures/CircuitLab).", "Image saved to Pictures/CircuitLab.") : t("تعذّر حفظ الصورة.", "Could not save the image."));
};
document.getElementById("btnDownload").onclick = function () {
  var prevSel = sel, prevPending = pending;
  try {
    sel = null; pending = null; draw();
    var off = document.createElement("canvas"); off.width = cv.width; off.height = cv.height;
    var o = off.getContext("2d"); o.fillStyle = "#0f172a"; o.fillRect(0, 0, off.width, off.height); o.drawImage(cv, 0, 0);
    var url = off.toDataURL("image/png");
    if (window.Android && Android.saveImage) Android.saveImage(url);
    else { var a = document.createElement("a"); a.download = "circuit_" + Date.now() + ".png"; a.href = url; a.click(); setStatus("ok", t("تم تجهيز الصورة.", "Image ready.")); }
  } catch (e) { setStatus("bad", t("تعذّر تصدير الصورة.", "Could not export the image.")); }
  sel = prevSel; pending = prevPending; draw();
};

var clearArmed = false, clearTimer = null, btnClear = document.getElementById("btnClear");
btnClear.onclick = function () {
  if (!clearArmed) {
    clearArmed = true; btnClear.textContent = t("تأكيد؟", "Sure?");
    clearTimer = setTimeout(function () { clearArmed = false; btnClear.textContent = t("مسح", "Clear"); }, 3000);
    return;
  }
  clearTimeout(clearTimer); clearArmed = false; btnClear.textContent = t("مسح", "Clear");
  snap(); comps = []; wires = []; sel = null; pending = null;
  meter.probeA.key = null; meter.probeB.key = null;
  scope.probeA.key = null; scope.probeB.key = null; scope.probeA.data = []; scope.probeB.data = [];
  recompute();
};

// ===== تصدير/استيراد JSON =====
document.getElementById("btnExport").onclick = function () {
  if (comps.length === 0) { setStatus("warn", t("لا توجد دائرة لتصديرها.", "No circuit to export.")); return; }
  var ok = saveFile("circuit_" + Date.now() + ".json", "application/json", serialize(), false);
  setStatus(ok ? "ok" : "bad", ok
    ? t("تم تصدير الدائرة كملف JSON.", "Circuit exported as JSON.")
    : t("تعذّر حفظ الملف.", "Could not save the file."));
};

document.getElementById("btnImport").onclick = function () {
  document.getElementById("fileInput").click();
};

document.getElementById("fileInput").onchange = function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  if (file.size > 5000000) { setStatus("bad", t("الملف كبير جداً.", "File too large.")); e.target.value = ""; return; }
  var reader = new FileReader();
  reader.onload = function (ev) {
    try {
      if (loadState(JSON.parse(ev.target.result), true)) {
        setStatus("ok", t("تم استيراد الدائرة.", "Circuit imported."));
      } else {
        setStatus("bad", t("ملف غير صالح (لا يحتوي دائرة).", "Invalid file (no circuit)."));
      }
    } catch (err) {
      setStatus("bad", t("الملف تالف أو ليس JSON صالحاً.", "Corrupted or invalid JSON."));
    }
    e.target.value = "";
  };
  reader.onerror = function () { setStatus("bad", t("تعذّر قراءة الملف.", "Could not read the file.")); e.target.value = ""; };
  reader.readAsText(file);
};
document.getElementById("btnDemo").onclick = demo;
document.getElementById("btnClose").onclick = function () { try { if (window.Android && Android.close) { Android.close(); return; } } catch (e) {} history.back(); };

/* ===================================================== الحركة والصوت ============================================= */
var soundOn = true, audioCtx = null, osc = null, gainNode = null, lastTs = 0;
function buzzing() {
  if (!sim || !sim.ok) return false;
  return comps.some(function (c) {
    var baseType = ALIAS[c.type] || c.type;
    return baseType === "buzzer" && Math.abs(sim.V[c.id]) > 1.0 && Math.abs(sim.I[c.id]) > 0.001;
  });
}
function updateSound() {
  try {
    var want = soundOn && buzzing();
    if (want && !audioCtx) {
      var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
      audioCtx = new AC(); osc = audioCtx.createOscillator(); gainNode = audioCtx.createGain();
      osc.type = "square"; osc.frequency.value = 880; gainNode.gain.value = 0;
      osc.connect(gainNode); gainNode.connect(audioCtx.destination); osc.start();
    }
    if (gainNode) { if (audioCtx.state === "suspended") audioCtx.resume(); gainNode.gain.value = want ? 0.04 : 0; }
  } catch (e) {}
}
document.getElementById("btnSound").onclick = function () { soundOn = !soundOn; this.textContent = soundOn ? "🔊" : "🔇"; updateSound(); };

// ===== تصدير بيانات الراسم كـ CSV =====
document.getElementById("btnScopeCsv").onclick = function () {
  if (!scope.visible) { setStatus("warn", t("الراسم غير مفعّل.", "Scope is not active.")); return; }
  var a = scope.probeA.data || [], b = scope.probeB.data || [];
  var n = Math.max(a.length, b.length);
  if (n === 0) { setStatus("warn", t("لا توجد بيانات بعد. شغّل الراسم وانتظر قليلاً.", "No data yet. Turn on the scope and wait a moment.")); return; }
  var lines = ["time_s,CH1_V,CH2_V"];
  for (var i = 0; i < n; i++) {
    var ts = (i * TIME_SCALE).toFixed(4);
    var v1 = (a[i] != null) ? a[i].toFixed(4) : "";
    var v2 = (b[i] != null) ? b[i].toFixed(4) : "";
    lines.push(ts + "," + v1 + "," + v2);
  }
  var ok = saveFile("scope_" + Date.now() + ".csv", "text/csv", lines.join("\n") + "\n", false);
  setStatus(ok ? "ok" : "bad", ok
    ? t("تم حفظ " + n + " عيّنة.", "Saved " + n + " samples.")
    : t("تعذّر حفظ الملف.", "Could not save the file."));
};
var TIME_SCALE = 0.05, simTime = 0, lastSample = 0, acHold = 0;
function hasAC() { return comps.some(function (c) { return c.type === "ac_source"; }); }
function has555() { return comps.some(function (c) { return c.type === "timer555"; }); }
function sampleScope() {
  if (!scope.visible) return;
  ["probeA", "probeB"].forEach(function (k) {
    var p = scope[k];
    if (p.key && sim && sim.ok) { p.data.push(sim.nodeV(p.key)); if (p.data.length > scope.maxData) p.data.shift(); }
    else p.data = [];
  });
}
function loop(ts) {
  var dt = lastTs ? Math.min(0.1, (ts - lastTs) / 1000) : 0; lastTs = ts; animT = ts / 1000;
  var ac = hasAC(), tm = has555(), need = false;
  if (ac) simTime = animT * TIME_SCALE;
  if ((ac || tm || scope.visible) && ts - lastSample > 30 && !drag) {
    lastSample = ts;
    if (ac || tm) recompute(true);
    sampleScope(); need = true;
  }
  if (sim && sim.ok && sim.anyCurrent && !drag) {
    comps.forEach(function (c) {
      var baseType = ALIAS[c.type] || c.type;
      if (baseType === "stepper_motor") c.ang = (c.ang || 0) + dt * Math.min(8, Math.abs(sim.V[c.id]) * 0.8) * (sim.I[c.id] < 0 ? -1 : 1);
      if (baseType === "motor") c.ang = (c.ang || 0) + dt * Math.min(30, Math.abs(sim.V[c.id]) * 3) * (sim.I[c.id] < 0 ? -1 : 1);
    });
    need = true;
  }
  if (need) draw();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

/* ========================================================= البدء ================================================= */
/* ============================================ تراجع / إعادة ============================================ */
var undoStack = [], redoStack = [];
function snapStr() { return JSON.stringify({ comps: comps, wires: wires }); }
function snap() { undoStack.push(snapStr()); if (undoStack.length > 60) undoStack.shift(); redoStack = []; updateUndoBtns(); }
function restoreSnap(str) {
  var o = JSON.parse(str);
  comps = o.comps; wires = o.wires; sel = null; pending = null;
  [meter.probeA, meter.probeB, scope.probeA, scope.probeB].forEach(function (pr) { if (pr.key && !keyPos(pr.key)) pr.key = null; });
  recompute();
}
function doUndo() { if (!undoStack.length) return; redoStack.push(snapStr()); restoreSnap(undoStack.pop()); updateUndoBtns(); }
function doRedo() { if (!redoStack.length) return; undoStack.push(snapStr()); restoreSnap(redoStack.pop()); updateUndoBtns(); }
function updateUndoBtns() {
  var u = document.getElementById("btnUndo"), r = document.getElementById("btnRedo");
  if (u) u.disabled = !undoStack.length;
  if (r) r.disabled = !redoStack.length;
}

/* ============================================ حفظ الملفات و ZIP ============================================ */
function gid(id) { return document.getElementById(id); }
function saveFile(name, mime, data, isB64) {
  try {
    if (window.Android && Android.saveFile) return !!Android.saveFile(name, mime, data, !!isB64);
    var blob = isB64 ? new Blob([Uint8Array.from(atob(data), function (ch) { return ch.charCodeAt(0); })], { type: mime }) : new Blob([data], { type: mime });
    var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    return true;
  } catch (e) { return false; }
}
var crcT = null;
function crc32(bytes) {
  if (!crcT) { crcT = []; for (var n = 0; n < 256; n++) { var c0 = n; for (var k = 0; k < 8; k++) c0 = (c0 & 1) ? (0xEDB88320 ^ (c0 >>> 1)) : (c0 >>> 1); crcT[n] = c0 >>> 0; } }
  var c = 0xFFFFFFFF;
  for (var i = 0; i < bytes.length; i++) c = crcT[(c ^ bytes[i]) & 255] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
function makeZip(files) {
  var enc = new TextEncoder(), parts = [], central = [], off = 0;
  function u16(v) { return [v & 255, (v >>> 8) & 255]; }
  function u32(v) { return [v & 255, (v >>> 8) & 255, (v >>> 16) & 255, (v >>> 24) & 255]; }
  files.forEach(function (f) {
    var nb = enc.encode(f.name), db = enc.encode(f.text), crc = crc32(db);
    var lh = [0x50, 0x4b, 3, 4].concat(u16(20), u16(0x0800), u16(0), u16(0), u16(0x21), u32(crc), u32(db.length), u32(db.length), u16(nb.length), u16(0));
    parts.push(new Uint8Array(lh), nb, db);
    var ch = [0x50, 0x4b, 1, 2].concat(u16(20), u16(20), u16(0x0800), u16(0), u16(0), u16(0x21), u32(crc), u32(db.length), u32(db.length), u16(nb.length), u16(0), u16(0), u16(0), u16(0), u32(0), u32(off));
    central.push(new Uint8Array(ch), nb);
    off += lh.length + nb.length + db.length;
  });
  var cdSize = 0; central.forEach(function (p) { cdSize += p.length; });
  var eocd = [0x50, 0x4b, 5, 6].concat(u16(0), u16(0), u16(files.length), u16(files.length), u32(cdSize), u32(off), u16(0));
  var all = parts.concat(central, [new Uint8Array(eocd)]), total = 0;
  all.forEach(function (p) { total += p.length; });
  var out = new Uint8Array(total), pos = 0;
  all.forEach(function (p) { out.set(p, pos); pos += p.length; });
  return out;
}
function b64(u8) {
  var s = "", ch = 0x8000;
  for (var i = 0; i < u8.length; i += ch) s += String.fromCharCode.apply(null, u8.subarray(i, i + ch));
  return btoa(s);
}
function saveZip(name, files) { return saveFile(name, "application/zip", b64(makeZip(files)), true); }

/* ===================================================== PCB ===================================================== */
var GRID = 2.54, TRACE_W = 0.6, PAD_R = 0.9, VIA_R = 0.6;
var PCB = { data: null, layers: 2, showTop: true, showBot: true, path: null, seed: 0 };
function mmx(g) { return (g + 0.5) * GRID; }

function footprint(type) {
  type = ALIAS[type] || type;
  if (type === "relay") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 4, 0], ["out", 4, 2]] };
  if (type === "transistor") return { w: 3, h: 1, pads: [["a", 0, 0], ["c", 1, 0], ["b", 2, 0]] };
  if (type === "gate_not") return { w: 5, h: 1, pads: [["a", 0, 0], ["out", 4, 0]] };
  if (type === "gate_and" || type === "gate_or" || type === "gate_nand" || type === "gate_xor" || type === "gate_xnor") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["out", 4, 1]] };
  if (type === "battery" || type === "ac_source" || type === "arduino" || type === "esp32") return { w: 2, h: 1, pads: [["a", 0, 0], ["b", 1, 0]] };
  if (type === "nano" || type === "mega" || type === "pico" || type === "esp8266") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 5, 2]] };
  if (type === "reg7805" || type === "reg7803") return { w: 3, h: 2, pads: [["a", 0, 0], ["b", 1, 2], ["c", 2, 0]] };
  if (type === "opamp") return { w: 3, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 2, 1]] };
  if (type === "transistor_pnp") return { w: 3, h: 1, pads: [["a", 0, 0], ["c", 1, 0], ["b", 2, 0]] };
  if (type === "seven_seg" || type === "timer555") return { w: 3, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 2, 1]] };
  if (type === "mosfet_n") return { w: 3, h: 2, pads: [["a", 1, 2], ["b", 1, 0], ["c", 0, 1]] };
  if (type === "lm317") return { w: 3, h: 2, pads: [["a", 0, 0], ["b", 1, 2], ["c", 2, 0]] };
  if (type === "servo") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 2, 2], ["c", 3, 0]] };
  if (type === "lcd_16x2") return { w: 8, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 7, 1]] };
  if (type === "hc_sr04") return { w: 4, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "ds18b20") return { w: 3, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 2, 1]] };
  if (type === "lm386" || type === "lm358" || type === "ne5532" || type === "lm393") return { w: 3, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 2, 1]] };
  if (type === "cd4017") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 5, 1]] };
  if (type === "ic_74hc138") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 4, 1]] };
  if (type === "tda7297") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 5, 1]] };
  if (type === "opa2134" || type === "ad620" || type === "opa548" || type === "cd4013" || type === "cd4015") return { w: 4, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "lm337") return { w: 3, h: 2, pads: [["a", 0, 0], ["b", 1, 2], ["c", 2, 0]] };
  if (type === "ic_74hc273" || type === "ic_74hc373" || type === "mcp23017" || type === "ic_74hc00") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 4, 1]] };
  if (type === "at24c32") return { w: 3, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 2, 1]] };
  if (type === "lm741" || type === "ne5534") return { w: 3, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 2, 1]] };
  if (type === "tda2822" || type === "cd4066") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 4, 1]] };
  if (type === "cd4051") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 5, 1]] };
  if (type === "pcf8574") return { w: 4, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "tda2030" || type === "lm2596" || type === "adc0804" || type === "dac0808") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 4, 1]] };
  if (type === "tp4056") return { w: 4, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "max7219") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 5, 1]] };
  if (type === "tl072") return { w: 4, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "lm324" || type === "ne556") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 4, 1]] };
  if (type === "uln2003" || type === "lm3914") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 5, 1]] };
  if (type === "lm1117") return { w: 4, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "oled_ssd1306") return { w: 5, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 4, 1]] };
  if (type === "seven_seg_4") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 5, 1]] };
  if (type === "l293d") return { w: 6, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 5, 1]] };
  if (type === "hc595") return { w: 5, h: 2, pads: [["a", 0, 0], ["b", 0, 1], ["c", 4, 0]] };
  if (type === "ds3231") return { w: 4, h: 3, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "optocoupler") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 3, 0]] };
  if (type === "potentiometer") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 3, 0], ["c", 1.5, 2]] };
  if (type === "mpu6050" || type === "bmp280" || type === "acs712" || type === "a3144" || type === "ky038" || type === "yl69" || type === "ttp223" || type === "ky040" || type === "ws2812" || type === "tsop" || type === "hc05" || type === "l298n") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "a4988" || type === "pam8403" || type === "max98357" || type === "ads1115" || type === "mcp4725" || type === "ina219" || type === "mq2" || type === "bh1750" || type === "vl53l0x" || type === "ic_74hc165" || type === "nrf24l01" || type === "sim800l") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "drv8825" || type === "tb6612" || type === "bts7960" || type === "tcs34725" || type === "mlx90614" || type === "max30102" || type === "adxl345" || type === "hx711" || type === "dht22" || type === "sgp30" || type === "rc522" || type === "bme680") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "pca9685" || type === "tca9548a" || type === "l9110s" || type === "tmp36" || type === "am2320" || type === "ds1307" || type === "pcf8563" || type === "st7735" || type === "ssd1351" || type === "bmp180" || type === "sht31" || type === "apds9960") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "ds1302" || type === "max6675" || type === "max31855" || type === "sd_card" || type === "enc28j60" || type === "uln2803" || type === "tlc5940" || type === "mpu9250" || type === "ad9833" || type === "ams1117" || type === "xl6009" || type === "vl6180x") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (BATCH19[type]) return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (BATCH20[type]) return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (BATCH21[type]) return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "sht10" || type === "sht75" || type === "si7021" || type === "bme280" || type === "mpl3115a2" || type === "mq3" || type === "mq4" || type === "mq5" || type === "mq6" || type === "mq7" || type === "mq8" || type === "mq9" || type === "mq135" || type === "gp2y1010" || type === "tsl2561" || type === "tcs3200" || type === "reed_switch" || type === "vibration_sensor" || type === "water_level" || type === "flex_sensor" || type === "tilt_switch" || type === "shock_sensor" || type === "flame_sensor" || type === "rain_sensor" || type === "hall_linear" || type === "cd4071" || type === "cd4081" || type === "cd4030" || type === "cd4001" || type === "cd4023" || type === "cd4025" || type === "cd4070" || type === "cd4075" || type === "cd4077" || type === "cd4093" || type === "cd4538" || type === "cd4047" || type === "cd4027" || type === "cd4029" || type === "cd4076" || type === "cd4022" || type === "cd4060" || type === "cd4541" || type === "cd4511" || type === "cd4028" || type === "mcp3008" || type === "mcp3208" || type === "ads1015" || type === "pcf8591" || type === "tlc5615" || type === "mcp4921" || type === "at24c256" || type === "at24c512" || type === "w25q64" || type === "mb85rc" || type === "ds3234" || type === "rv3028" || type === "mcp7940" || type === "nokia5110" || type === "ssd1309" || type === "st7565" || type === "st7920" || type === "ili9341" || type === "ili9486" || type === "max6954" || type === "lcd_20x4" || type === "st7735_160" || type === "ssd1331" || type === "drv8833" || type === "drv8871" || type === "l293e" || type === "sn754410" || type === "uln2004" || type === "mc33926" || type === "bd6221" || type === "tb67h420" || type === "a3959" || type === "drv8824" || type === "esp01" || type === "rn2483" || type === "rfm69" || type === "rfm95" || type === "hc12" || type === "xbee" || type === "sim900" || type === "m95" || type === "nrf905" || type === "cc1101" || type === "lm7809" || type === "lm7812" || type === "lm7905" || type === "lm7912" || type === "lm1084" || type === "lm2678" || type === "lm5007" || type === "mcp1700" || type === "mic5205" || type === "lp2985" || type === "lm4871" || type === "tda2003") return { w: 4, h: 2, pads: [["a", 0, 0], ["b", 0, 2], ["c", 3, 1]] };
  if (type === "switch") return { w: 3, h: 1, pads: [["a", 0, 0], ["b", 2, 0]] };
  return { w: 4, h: 1, pads: [["a", 0, 0], ["b", 3, 0]] };
}

function pcbBuild() {
  var nm = nodeMap(comps, wires);
  var items = comps.map(function (c) { return { c: c, fp: footprint(c.type) }; });
  var area = 0;
  items.forEach(function (it) { area += (it.fp.w + 3) * (it.fp.h + 3); });
  var rowW = Math.max(18, Math.ceil(Math.sqrt(area) * 1.4));
  var px = 1, py = 1, rowH = 0, maxX = 1;
  items.forEach(function (it) {
    if (px > 1 && px + it.fp.w > rowW) { px = 1; py += rowH + 3; rowH = 0; }
    it.gx = px; it.gy = py; px += it.fp.w + 3;
    rowH = Math.max(rowH, it.fp.h);
    maxX = Math.max(maxX, it.gx + it.fp.w);
  });
  var cols = maxX + 2, rows = py + rowH + 2;
  var plane = cols * rows, N = plane * 2;
  function idx(l, gx, gy) { return l * plane + gy * cols + gx; }
  var base = new Int32Array(N).fill(-1), gx, gy;
  for (gx = 0; gx < cols; gx++) for (gy = 0; gy < rows; gy++) {
    if (gx === 0 || gy === 0 || gx === cols - 1 || gy === rows - 1) { base[idx(0, gx, gy)] = -2; base[idx(1, gx, gy)] = -2; }
  }
  var pads = [], byNet = {}, isPad = new Uint8Array(plane);
  items.forEach(function (it) {
    it.fp.pads.forEach(function (p) {
      var key = it.c.id + "." + p[0], net = nm.node[key];
      if (net === undefined) net = 100000 + pads.length;
      var pd = { key: key, comp: it.c.id, term: p[0], gx: it.gx + p[1], gy: it.gy + p[2], net: net };
      pads.push(pd);
      base[idx(0, pd.gx, pd.gy)] = net; base[idx(1, pd.gx, pd.gy)] = net;
      isPad[pd.gy * cols + pd.gx] = 1;
      (byNet[net] = byNet[net] || []).push(pd);
    });
  });

  var oneLayer = PCB.layers === 1, allowed = oneLayer ? [1] : [0, 1];
  var occ = new Int32Array(N);
  var segs, vias, failed;
  var DX = [1, -1, 0, 0], DY = [0, 0, 1, -1];

  function pathFrom(n0, prev) { var p = []; for (var n = n0; n !== -1; n = prev[n]) p.push(n); return p; }
  function dijkstra(tgt, tree, netId) {
    var dist = new Int32Array(N).fill(1000000000), prev = new Int32Array(N).fill(-1);
    var buckets = [], maxB = 0;
    function push(nn, d, p) { if (d < dist[nn]) { dist[nn] = d; prev[nn] = p; (buckets[d] || (buckets[d] = [])).push(nn); if (d > maxB) maxB = d; } }
    allowed.forEach(function (l) { push(idx(l, tgt.gx, tgt.gy), 0, -1); });
    for (var d = 0; d <= maxB; d++) {
      var bk = buckets[d]; if (!bk) continue;
      for (var q = 0; q < bk.length; q++) {
        var n0 = bk[q]; if (dist[n0] !== d) continue;
        if (tree[n0]) return pathFrom(n0, prev);
        var l = n0 >= plane ? 1 : 0, rem = n0 - l * plane, y = (rem / cols) | 0, x = rem - y * cols;
        for (var k = 0; k < 4; k++) {
          var nx = x + DX[k], ny = y + DY[k];
          if (nx < 0 || ny < 0 || nx >= cols || ny >= rows) continue;
          var ni = idx(l, nx, ny);
          if (occ[ni] !== -1 && occ[ni] !== netId) continue;
          var horiz = k < 2, cost = oneLayer ? 1 : (((l === 0) === horiz) ? 1 : 3);
          push(ni, d + cost, n0);
        }
        if (!oneLayer) { var vi = idx(1 - l, x, y); if (occ[vi] === -1 || occ[vi] === netId) push(vi, d + 8, n0); }
      }
    }
    return null;
  }
  function applyPath(p, netId, tree) {
    var cur = null;
    function flush() { if (cur) { segs.push(cur); cur = null; } }
    for (var j = 0; j < p.length; j++) {
      occ[p[j]] = netId; tree[p[j]] = 1;
      if (j === 0) continue;
      var a = p[j - 1], b = p[j], la = a >= plane ? 1 : 0, lb = b >= plane ? 1 : 0;
      var ra = a - la * plane, rb = b - lb * plane;
      var ya = (ra / cols) | 0, xa = ra - ya * cols, yb = (rb / cols) | 0, xb = rb - yb * cols;
      if (la !== lb) { flush(); if (!isPad[ya * cols + xa]) vias.push({ x: xa, y: ya, net: netId }); continue; }
      var dx = xb - xa, dy = yb - ya;
      if (cur && cur.l === la && cur.dx === dx && cur.dy === dy) { cur.x2 = xb; cur.y2 = yb; }
      else { flush(); cur = { l: la, x1: xa, y1: ya, x2: xb, y2: yb, dx: dx, dy: dy, net: netId }; }
    }
    flush();
  }
  function hpwl(ps) {
    var x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    ps.forEach(function (p) { x0 = Math.min(x0, p.gx); x1 = Math.max(x1, p.gx); y0 = Math.min(y0, p.gy); y1 = Math.max(y1, p.gy); });
    return (x1 - x0) + (y1 - y0);
  }
  function attempt(order) {
    occ.set(base); segs = []; vias = []; failed = [];
    order.forEach(function (k) {
      var netId = Number(k), np = byNet[k], tree = new Uint8Array(N);
      var first = np[0]; tree[idx(0, first.gx, first.gy)] = 1; tree[idx(1, first.gx, first.gy)] = 1;
      var done = [first], rest = np.slice(1);
      while (rest.length) {
        var bi = 0, bd = 1e9, bq = null;
        rest.forEach(function (p, j) { done.forEach(function (q) { var dd = Math.abs(p.gx - q.gx) + Math.abs(p.gy - q.gy); if (dd < bd) { bd = dd; bi = j; bq = q; } }); });
        var tgt = rest.splice(bi, 1)[0], path = dijkstra(tgt, tree, netId);
        if (path) { applyPath(path, netId, tree); done.push(tgt); }
        else failed.push({ a: tgt, b: bq, net: netId });
      }
    });
  }

  var netIds = Object.keys(byNet).filter(function (k) { return byNet[k].length > 1; });
  var jitter = PCB.seed * 3;
  netIds.sort(function (a, b) { return (hpwl(byNet[a]) + Math.random() * jitter) - (hpwl(byNet[b]) + Math.random() * jitter); });
  var best = null, order = netIds.slice();
  for (var tryN = 0; tryN < 5; tryN++) {
    attempt(order);
    if (!best || failed.length < best.failed.length) best = { segs: segs, vias: vias, failed: failed };
    if (!failed.length) break;
    var bad = {}; failed.forEach(function (f) { bad[f.net] = 1; });
    order = order.filter(function (k) { return bad[k]; }).concat(order.filter(function (k) { return !bad[k]; }));
  }
  PCB.data = { cols: cols, rows: rows, W: cols * GRID, H: rows * GRID, items: items, pads: pads, segs: best.segs, vias: best.vias, failed: best.failed, nets: netIds.length, layers: PCB.layers };
}

function pcbDraw() {
  var d = PCB.data; if (!d) return;
  var cvp = gid("pcbCv"), g = cvp.getContext("2d");
  var w = Math.max(100, cvp.clientWidth), h = Math.max(100, cvp.clientHeight), ratio = window.devicePixelRatio || 1;
  cvp.width = Math.round(w * ratio); cvp.height = Math.round(h * ratio);
  g.setTransform(ratio, 0, 0, ratio, 0, 0);
  g.clearRect(0, 0, w, h);
  var sc = Math.min((w - 16) / d.W, (h - 16) / d.H), ox = (w - d.W * sc) / 2, oy = (h - d.H * sc) / 2;
  function X(v) { return ox + v * sc; }
  function Y(v) { return oy + v * sc; }
  g.fillStyle = "#14532d"; g.fillRect(X(0), Y(0), d.W * sc, d.H * sc);
  g.strokeStyle = "#a3e635"; g.lineWidth = 1; g.strokeRect(X(0), Y(0), d.W * sc, d.H * sc);
  g.lineCap = "round";
  [1, 0].forEach(function (l) {
    if (l === 1 && !PCB.showBot) return;
    if (l === 0 && (!PCB.showTop || d.layers === 1)) return;
    g.strokeStyle = l === 0 ? "rgba(239,68,68,.92)" : "rgba(59,130,246,.88)";
    g.lineWidth = Math.max(1.5, TRACE_W * sc);
    d.segs.forEach(function (s) {
      if (s.l !== l) return;
      g.beginPath(); g.moveTo(X(mmx(s.x1)), Y(mmx(s.y1))); g.lineTo(X(mmx(s.x2)), Y(mmx(s.y2))); g.stroke();
    });
  });
  d.vias.forEach(function (v) {
    g.beginPath(); g.arc(X(mmx(v.x)), Y(mmx(v.y)), Math.max(2, VIA_R * sc), 0, Math.PI * 2); g.fillStyle = "#e5e7eb"; g.fill();
    g.beginPath(); g.arc(X(mmx(v.x)), Y(mmx(v.y)), Math.max(1, 0.3 * sc), 0, Math.PI * 2); g.fillStyle = "#111827"; g.fill();
  });
  g.strokeStyle = "rgba(255,255,255,.75)"; g.lineWidth = 1; g.fillStyle = "rgba(255,255,255,.9)"; g.font = Math.max(8, 1.3 * sc) + "px sans-serif"; g.textAlign = "left";
  d.items.forEach(function (it) {
    g.strokeRect(X(it.gx * GRID + 0.3), Y(it.gy * GRID + 0.3), (it.fp.w * GRID - 0.6) * sc, (it.fp.h * GRID - 0.6) * sc);
    g.fillText(it.c.id, X(it.gx * GRID + 0.5), Y(it.gy * GRID - 0.1));
  });
  d.pads.forEach(function (p) {
    g.beginPath(); g.arc(X(mmx(p.gx)), Y(mmx(p.gy)), Math.max(3, PAD_R * sc), 0, Math.PI * 2); g.fillStyle = "#d4af37"; g.fill();
    g.beginPath(); g.arc(X(mmx(p.gx)), Y(mmx(p.gy)), Math.max(1.2, 0.4 * sc), 0, Math.PI * 2); g.fillStyle = "#111827"; g.fill();
  });
  g.setLineDash([4, 3]); g.strokeStyle = "#fde047"; g.lineWidth = 1.5;
  d.failed.forEach(function (f) { g.beginPath(); g.moveTo(X(mmx(f.a.gx)), Y(mmx(f.a.gy))); g.lineTo(X(mmx(f.b.gx)), Y(mmx(f.b.gy))); g.stroke(); });
  g.setLineDash([]);
  if (PCB.path) {
    g.strokeStyle = "#e879f9"; g.lineWidth = 1;
    PCB.path.forEach(function (lp) { g.beginPath(); lp.forEach(function (pt, i) { if (i === 0) g.moveTo(X(pt[0]), Y(pt[1])); else g.lineTo(X(pt[0]), Y(pt[1])); }); g.stroke(); });
  }
}

function pcbMsg(cls, msg) { var e = gid("pcbStatus"); e.className = cls; e.textContent = msg; }
function pcbRun() {
  PCB.path = null;
  pcbBuild(); pcbDraw();
  var d = PCB.data, len = 0, bad = {}, nBad = 0;
  d.segs.forEach(function (s) { len += (Math.abs(s.x2 - s.x1) + Math.abs(s.y2 - s.y1)) * GRID; });
  d.failed.forEach(function (f) { bad[f.net] = 1; });
  for (var k in bad) nBad++;
  var msg = t("اللوحة ", "Board ") + d.W.toFixed(1) + "×" + d.H.toFixed(1) + " mm · " + t("شبكات ", "nets ") + (d.nets - nBad) + "/" + d.nets +
    " · " + t("فيا ", "vias ") + d.vias.length + " · " + t("مسارات ", "traces ") + len.toFixed(0) + " mm";
  if (d.failed.length) msg += "\n⚠ " + t("تعذّر توجيه " + d.failed.length + " وصلة (خطوط صفراء) — جرّب طبقتين أو أعد التوجيه.", d.failed.length + " connection(s) unrouted (yellow) — try 2 layers or re-route.");
  pcbMsg(d.failed.length ? "warn" : "ok", msg);
}
function openPcb() {
  if (!comps.length) { setStatus("warn", t("ارسم الدائرة أولاً.", "Draw a circuit first.")); return; }
  gid("pcb").className = "show";
  PCB.layers = parseInt(gid("pcbLayers").value, 10) === 1 ? 1 : 2;
  requestAnimationFrame(pcbRun);
}
function pcbToggleBtns() {
  gid("pcbTop").className = PCB.showTop ? "" : "off";
  gid("pcbBot").className = PCB.showBot ? "" : "off";
}

/* ---------------------------------------------- SVG / Gerber / Excellon ---------------------------------------------- */
function f3(v) { return v.toFixed(3); }
function pcbSVG() {
  var d = PCB.data, o = [];
  o.push('<svg xmlns="http://www.w3.org/2000/svg" width="' + f3(d.W) + 'mm" height="' + f3(d.H) + 'mm" viewBox="0 0 ' + f3(d.W) + " " + f3(d.H) + '">');
  o.push('<rect width="' + f3(d.W) + '" height="' + f3(d.H) + '" fill="#14532d"/>');
  [1, 0].forEach(function (l) {
    if (l === 0 && d.layers === 1) return;
    var col = l === 0 ? "#ef4444" : "#3b82f6";
    d.segs.forEach(function (s) {
      if (s.l !== l) return;
      o.push('<line x1="' + f3(mmx(s.x1)) + '" y1="' + f3(mmx(s.y1)) + '" x2="' + f3(mmx(s.x2)) + '" y2="' + f3(mmx(s.y2)) + '" stroke="' + col + '" stroke-width="' + TRACE_W + '" stroke-linecap="round"/>');
    });
  });
  d.vias.forEach(function (v) { o.push('<circle cx="' + f3(mmx(v.x)) + '" cy="' + f3(mmx(v.y)) + '" r="' + VIA_R + '" fill="#e5e7eb"/><circle cx="' + f3(mmx(v.x)) + '" cy="' + f3(mmx(v.y)) + '" r="0.3" fill="#111"/>'); });
  d.items.forEach(function (it) {
    o.push('<rect x="' + f3(it.gx * GRID + 0.3) + '" y="' + f3(it.gy * GRID + 0.3) + '" width="' + f3(it.fp.w * GRID - 0.6) + '" height="' + f3(it.fp.h * GRID - 0.6) + '" fill="none" stroke="#fff" stroke-width="0.15"/>');
    o.push('<text x="' + f3(it.gx * GRID + 0.5) + '" y="' + f3(it.gy * GRID - 0.2) + '" font-size="1.4" fill="#fff" font-family="sans-serif">' + it.c.id + "</text>");
  });
  d.pads.forEach(function (p) { o.push('<circle cx="' + f3(mmx(p.gx)) + '" cy="' + f3(mmx(p.gy)) + '" r="' + PAD_R + '" fill="#d4af37"/><circle cx="' + f3(mmx(p.gx)) + '" cy="' + f3(mmx(p.gy)) + '" r="0.4" fill="#111"/>'); });
  o.push("</svg>");
  return o.join("\n");
}

function gUnits(v) { return Math.round(v * 1e6); }
function gerberHead(title, apertures) {
  var L = ["G04 " + title + "*", "%FSLAX36Y36*%", "%MOMM*%"];
  apertures.forEach(function (a, i) { L.push("%ADD" + (10 + i) + "C," + a.toFixed(6) + "*%"); });
  L.push("G01*", "%LPD*%");
  return L;
}
function gerberCopper(layer) {
  var d = PCB.data, L = gerberHead("Circuit Lab copper layer " + layer, [TRACE_W, PAD_R * 2, VIA_R * 2]);
  function P(gx, gy) { return "X" + gUnits(mmx(gx)) + "Y" + gUnits(d.H - mmx(gy)); }
  L.push("D10*");
  d.segs.forEach(function (s) { if (s.l === layer) { L.push(P(s.x1, s.y1) + "D02*"); L.push(P(s.x2, s.y2) + "D01*"); } });
  L.push("D11*");
  d.pads.forEach(function (p) { L.push(P(p.gx, p.gy) + "D03*"); });
  L.push("D12*");
  d.vias.forEach(function (v) { L.push(P(v.x, v.y) + "D03*"); });
  L.push("M02*");
  return L.join("\n") + "\n";
}
function gerberRect(title, x0, y0, x1, y1, width, list) {
  var d = PCB.data, L = gerberHead(title, [width]);
  function P(x, y) { return "X" + gUnits(x) + "Y" + gUnits(d.H - y); }
  L.push("D10*");
  (list || [[x0, y0, x1, y1]]).forEach(function (r) {
    L.push(P(r[0], r[1]) + "D02*", P(r[2], r[1]) + "D01*", P(r[2], r[3]) + "D01*", P(r[0], r[3]) + "D01*", P(r[0], r[1]) + "D01*");
  });
  L.push("M02*");
  return L.join("\n") + "\n";
}
function gerberSilk() {
  var d = PCB.data, rects = d.items.map(function (it) { return [it.gx * GRID + 0.3, it.gy * GRID + 0.3, (it.gx + it.fp.w) * GRID - 0.3, (it.gy + it.fp.h) * GRID - 0.3]; });
  return gerberRect("Circuit Lab silkscreen", 0, 0, 0, 0, 0.15, rects);
}
function excellon(cfg) {
  var d = PCB.data, groups = {}, keys;
  function add(x, y, dia) { var k = dia.toFixed(3); (groups[k] = groups[k] || []).push([x, d.H - y]); }
  d.pads.forEach(function (p) { add(mmx(p.gx), mmx(p.gy), cfg.drill); });
  d.vias.forEach(function (v) { add(mmx(v.x), mmx(v.y), cfg.via); });
  keys = Object.keys(groups);
  var L = ["M48", "METRIC,TZ"];
  keys.forEach(function (k, i) { L.push("T" + (i + 1) + "C" + k); });
  L.push("%", "G90");
  keys.forEach(function (k, i) { L.push("T" + (i + 1)); groups[k].forEach(function (p) { L.push("X" + f3(p[0]) + "Y" + f3(p[1])); }); });
  L.push("M30");
  return L.join("\n") + "\n";
}

/* ----------------------------------------------------- عزل المسارات ----------------------------------------------------- */
function rdpOpen(p, tol) {
  var keep = new Uint8Array(p.length); keep[0] = 1; keep[p.length - 1] = 1;
  var st = [[0, p.length - 1]];
  while (st.length) {
    var r = st.pop(), a = r[0], b = r[1], md = 0, mi2 = -1;
    for (var i = a + 1; i < b; i++) { var dd = distSeg(p[i][0], p[i][1], p[a][0], p[a][1], p[b][0], p[b][1]); if (dd > md) { md = dd; mi2 = i; } }
    if (md > tol && mi2 > 0) { keep[mi2] = 1; st.push([a, mi2], [mi2, b]); }
  }
  return p.filter(function (_, i) { return keep[i]; });
}
function simplifyLoop(pts, tol) {
  if (pts.length < 4) return pts;
  var far = 0, fd = 0, i;
  for (i = 1; i < pts.length; i++) { var dd = Math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]); if (dd > fd) { fd = dd; far = i; } }
  var c1 = rdpOpen(pts.slice(0, far + 1), tol), c2 = rdpOpen(pts.slice(far).concat([pts[0]]), tol);
  return c1.concat(c2.slice(1));
}
function isoLoops(layer, off) {
  var d = PCB.data, res = 10, pad = 3;
  var wpx = Math.ceil((d.W + 2 * pad) * res), hpx = Math.ceil((d.H + 2 * pad) * res);
  var cnv = document.createElement("canvas"); cnv.width = wpx; cnv.height = hpx;
  var g = cnv.getContext("2d", { willReadFrequently: true });
  g.fillStyle = "#000"; g.strokeStyle = "#000"; g.lineCap = "round"; g.lineJoin = "round";
  function P(gc) { return (mmx(gc) + pad) * res; }
  g.lineWidth = (TRACE_W + 2 * off) * res;
  d.segs.forEach(function (s) { if (s.l !== layer) return; g.beginPath(); g.moveTo(P(s.x1), P(s.y1)); g.lineTo(P(s.x2), P(s.y2)); g.stroke(); });
  function disc(gx, gy, r) { g.beginPath(); g.arc(P(gx), P(gy), (r + off) * res, 0, Math.PI * 2); g.fill(); }
  d.pads.forEach(function (p) { disc(p.gx, p.gy, PAD_R); });
  d.vias.forEach(function (v) { disc(v.x, v.y, VIA_R); });

  var im = g.getImageData(0, 0, wpx, hpx).data, A = new Uint8Array(wpx * hpx), ii;
  for (ii = 0; ii < A.length; ii++) A[ii] = im[ii * 4 + 3];
  var T = 128, adj = new Map();
  function ek(type, x, y) { return (y * wpx + x) * 2 + type; }
  function lk(a, b) { var u = adj.get(a); if (!u) adj.set(a, u = []); u.push(b); var v = adj.get(b); if (!v) adj.set(b, v = []); v.push(a); }
  for (var y = 0; y < hpx - 1; y++) for (var x = 0; x < wpx - 1; x++) {
    var tl = A[y * wpx + x] >= T ? 8 : 0, tr = A[y * wpx + x + 1] >= T ? 4 : 0, br = A[(y + 1) * wpx + x + 1] >= T ? 2 : 0, bl = A[(y + 1) * wpx + x] >= T ? 1 : 0;
    var cs = tl | tr | br | bl; if (cs === 0 || cs === 15) continue;
    var tp = ek(0, x, y), bt = ek(0, x, y + 1), lf = ek(1, x, y), rt = ek(1, x + 1, y);
    switch (cs) {
      case 1: case 14: lk(lf, bt); break;
      case 2: case 13: lk(bt, rt); break;
      case 3: case 12: lk(lf, rt); break;
      case 4: case 11: lk(tp, rt); break;
      case 5: lk(tp, lf); lk(bt, rt); break;
      case 6: case 9: lk(tp, bt); break;
      case 7: case 8: lk(lf, tp); break;
      case 10: lk(tp, rt); lk(lf, bt); break;
    }
  }
  function ep(k) {
    var type = k & 1, i = k >> 1, yy = (i / wpx) | 0, xx = i - yy * wpx;
    var v1 = A[yy * wpx + xx], v2 = type === 0 ? A[yy * wpx + xx + 1] : A[(yy + 1) * wpx + xx];
    var tt = v1 === v2 ? 0.5 : (T - v1) / (v2 - v1);
    var qx = type === 0 ? xx + tt : xx, qy = type === 0 ? yy : yy + tt;
    return [(qx + 0.5) / res - pad, (qy + 0.5) / res - pad];
  }
  var seen = new Set(), loops = [];
  adj.forEach(function (nb, k0) {
    if (seen.has(k0)) return;
    var chain = [], prevK = -1, k = k0;
    while (k !== undefined && !seen.has(k)) {
      seen.add(k); chain.push(k);
      var n2 = adj.get(k);
      if (!n2 || n2.length < 2) break;
      var nx2 = (n2[0] !== prevK) ? n2[0] : n2[1];
      prevK = k; k = nx2;
    }
    if (chain.length >= 6) {
      var pts = chain.map(ep); pts.push(pts[0]);
      var sp = simplifyLoop(pts, 0.03);
      if (sp.length >= 4) loops.push(sp);
    }
  });
  return loops;
}

/* ------------------------------------------------------- G-code ------------------------------------------------------- */
function num(id, def, min) { var v = parseFloat(gid(id).value); return (isFinite(v) && v >= min) ? v : def; }
function readCfg() {
  return {
    tool: num("cTool", 0.2, 0.01), depth: num("cDepth", 0.1, 0.01), feed: num("cFeed", 200, 1), plunge: num("cPlunge", 80, 1),
    safe: num("cSafe", 2, 0.5), rpm: num("cRpm", 12000, 1), drill: num("cDrill", 0.9, 0.2), via: num("cVia", 0.6, 0.2),
    thick: num("cThick", 1.6, 0.1), mill: num("cMill", 2, 0.5), passes: Math.max(1, Math.min(4, Math.round(num("cPass", 1, 1)))),
    side: gid("cSide").value
  };
}
function gcHead(title, cfg, spindle) {
  var L = ["(" + title + ")", "(Generated by Circuit Lab - verify before running!)",
    "(Origin: lower-left corner of the board, Z0 = top surface of the board)",
    "(Board facing up: " + cfg.side + ")", "G21 (mm)", "G90 (absolute)", "G17", "G94"];
  if (spindle) L.push("M3 S" + Math.round(cfg.rpm));
  L.push("G0 Z" + f3(cfg.safe));
  return L;
}
function gcFoot(cfg) { return ["G0 Z" + f3(cfg.safe), "M5", "G0 X0 Y0", "M30"]; }
function orderNearest(items, startOf) {
  var rest = items.slice(), out = [], cx = 0, cy = 0;
  while (rest.length) {
    var bi = 0, bd = 1e18;
    for (var i = 0; i < rest.length; i++) { var p = startOf(rest[i]), dd = (p[0] - cx) * (p[0] - cx) + (p[1] - cy) * (p[1] - cy); if (dd < bd) { bd = dd; bi = i; } }
    var it = rest.splice(bi, 1)[0]; out.push(it); var sp = startOf(it); cx = sp[0]; cy = sp[1];
  }
  return out;
}
function gcIsolation(cfg) {
  var d = PCB.data, layer = cfg.side === "bottom" ? 1 : 0, mir = cfg.side === "bottom";
  if (layer === 0 && d.layers === 1) return null;
  var loops = [];
  for (var p = 0; p < cfg.passes; p++) {
    isoLoops(layer, cfg.tool / 2 + 0.03 + p * cfg.tool * 0.8).forEach(function (lp) { loops.push(lp); });
  }
  PCB.path = loops;
  function GX(x) { return mir ? d.W - x : x; }
  function GY(y) { return d.H - y; }
  var ordered = orderNearest(loops, function (lp) { return [GX(lp[0][0]), GY(lp[0][1])]; });
  var L = gcHead("Isolation routing - " + cfg.side + " copper - bit " + cfg.tool + " mm", cfg, true), len = 0;
  ordered.forEach(function (lp) {
    L.push("G0 X" + f3(GX(lp[0][0])) + " Y" + f3(GY(lp[0][1])));
    L.push("G1 Z" + f3(-cfg.depth) + " F" + Math.round(cfg.plunge));
    for (var i = 1; i < lp.length; i++) {
      L.push("G1 X" + f3(GX(lp[i][0])) + " Y" + f3(GY(lp[i][1])) + (i === 1 ? " F" + Math.round(cfg.feed) : ""));
      len += Math.hypot(lp[i][0] - lp[i - 1][0], lp[i][1] - lp[i - 1][1]);
    }
    L.push("G0 Z" + f3(cfg.safe));
  });
  gcFoot(cfg).forEach(function (l) { L.push(l); });
  return { text: L.join("\n") + "\n", loops: ordered.length, len: len, min: len / cfg.feed };
}
function gcDrill(cfg) {
  var d = PCB.data, mir = cfg.side === "bottom", groups = {};
  function add(x, y, dia) { var k = dia.toFixed(2); (groups[k] = groups[k] || []).push([mir ? d.W - x : x, d.H - y]); }
  d.pads.forEach(function (p) { add(mmx(p.gx), mmx(p.gy), cfg.drill); });
  d.vias.forEach(function (v) { add(mmx(v.x), mmx(v.y), cfg.via); });
  var L = gcHead("Drilling - board facing up: " + cfg.side, cfg, false), total = 0;
  Object.keys(groups).sort(function (a, b) { return Number(b) - Number(a); }).forEach(function (k) {
    L.push("M5", "M0 (Insert drill bit " + k + " mm, then press start)", "M3 S" + Math.round(cfg.rpm), "G0 Z" + f3(cfg.safe));
    orderNearest(groups[k], function (p) { return p; }).forEach(function (p) {
      L.push("G0 X" + f3(p[0]) + " Y" + f3(p[1]));
      L.push("G1 Z" + f3(-(cfg.thick + 0.3)) + " F" + Math.round(cfg.plunge));
      L.push("G0 Z" + f3(cfg.safe));
      total++;
    });
  });
  gcFoot(cfg).forEach(function (l) { L.push(l); });
  return { text: L.join("\n") + "\n", holes: total };
}
function gcOutline(cfg) {
  var d = PCB.data, r = cfg.mill / 2, x0 = -r, y0 = -r, x1 = d.W + r, y1 = d.H + r;
  var total = cfg.thick + 0.2, step = 0.5, passes = Math.ceil(total / step);
  var L = gcHead("Board outline cut - mill " + cfg.mill + " mm (add tabs/tape to hold the board)", cfg, false);
  L.push("M5", "M0 (Insert mill bit " + cfg.mill + " mm, then press start)", "M3 S" + Math.round(cfg.rpm), "G0 Z" + f3(cfg.safe));
  L.push("G0 X" + f3(x0) + " Y" + f3(y0));
  for (var k = 1; k <= passes; k++) {
    var z = -Math.min(total, k * step);
    L.push("G1 Z" + f3(z) + " F" + Math.round(cfg.plunge));
    L.push("G1 X" + f3(x1) + " Y" + f3(y0) + " F" + Math.round(cfg.feed));
    L.push("G1 X" + f3(x1) + " Y" + f3(y1));
    L.push("G1 X" + f3(x0) + " Y" + f3(y1));
    L.push("G1 X" + f3(x0) + " Y" + f3(y0));
  }
  gcFoot(cfg).forEach(function (l) { L.push(l); });
  return { text: L.join("\n") + "\n", passes: passes };
}
function cncReadme(cfg) {
  return ["Circuit Lab - CNC package", "",
    "Side facing up: " + cfg.side + " (X is mirrored automatically for the bottom side)", "",
    "1) 1_isolation.nc : engraving bit (V-bit) " + cfg.tool + " mm, depth " + cfg.depth + " mm",
    "2) 2_drill.nc     : drills pad holes " + cfg.drill + " mm and via holes " + cfg.via + " mm (tool change pauses with M0)",
    "3) 3_outline.nc   : cuts the board outline with a " + cfg.mill + " mm end mill",
    "", "Set X0 Y0 at the lower-left corner of the board and Z0 on the copper surface.",
    "Always dry-run above the material first. Wear eye protection."].join("\n") + "\n";
}
function cncGenerate() {
  if (!PCB.data) { pcbMsg("warn", t("افتح مصمم PCB أولاً.", "Open the PCB designer first.")); return null; }
  return readCfg();
}
function cncStamp() { return Date.now(); }

gid("pcbClose").onclick = function () { gid("pcb").className = ""; };
gid("pcbRoute").onclick = function () { PCB.seed++; pcbRun(); };
gid("pcbLayers").onchange = function () { PCB.layers = parseInt(gid("pcbLayers").value, 10) === 1 ? 1 : 2; if (PCB.layers === 1) gid("cSide").value = "bottom"; PCB.seed = 0; pcbRun(); };
gid("pcbTop").onclick = function () { PCB.showTop = !PCB.showTop; pcbToggleBtns(); pcbDraw(); };
gid("pcbBot").onclick = function () { PCB.showBot = !PCB.showBot; pcbToggleBtns(); pcbDraw(); };
window.addEventListener("resize", function () { if (gid("pcb").className === "show") pcbDraw(); });
gid("pcbSvg").onclick = function () {
  if (!PCB.data) return;
  var ok = saveFile("pcb_" + cncStamp() + ".svg", "image/svg+xml", pcbSVG(), false);
  pcbMsg(ok ? "ok" : "bad", ok ? t("تم حفظ SVG في التنزيلات.", "SVG saved to Downloads.") : t("تعذّر الحفظ.", "Could not save."));
};
gid("pcbPng").onclick = function () {
  if (!PCB.data) return;
  pcbDraw();
  var ok = saveFile("pcb_" + cncStamp() + ".png", "image/png", gid("pcbCv").toDataURL("image/png").split(",")[1], true);
  pcbMsg(ok ? "ok" : "bad", ok ? t("تم حفظ الصورة في التنزيلات.", "PNG saved to Downloads.") : t("تعذّر الحفظ.", "Could not save."));
};
gid("pcbGerber").onclick = function () {
  if (!PCB.data) return;
  var cfg = readCfg(), d = PCB.data, files = [];
  if (d.layers === 2) files.push({ name: "top_copper.gtl", text: gerberCopper(0) });
  files.push({ name: "bottom_copper.gbl", text: gerberCopper(1) });
  files.push({ name: "top_silk.gto", text: gerberSilk() });
  files.push({ name: "board_outline.gko", text: gerberRect("Circuit Lab outline", 0, 0, d.W, d.H, 0.1) });
  files.push({ name: "drill.drl", text: excellon(cfg) });
  files.push({ name: "README.txt", text: "Gerber RS-274X (metric, 3.6) + Excellon drill. Upload the ZIP to any PCB manufacturer.\nGrid: 2.54 mm, trace 0.6 mm, pad 1.8 mm, via 1.2 mm.\n" });
  var ok = saveZip("gerber_" + cncStamp() + ".zip", files);
  pcbMsg(ok ? "ok" : "bad", ok ? t("تم حفظ Gerber ZIP في التنزيلات.", "Gerber ZIP saved to Downloads.") : t("تعذّر الحفظ.", "Could not save."));
};
gid("cncIso").onclick = function () {
  var cfg = cncGenerate(); if (!cfg) return;
  var r = gcIsolation(cfg);
  if (!r) { pcbMsg("warn", t("لا توجد طبقة علوية في وضع طبقة واحدة.", "No top layer in 1-layer mode.")); return; }
  pcbDraw();
  var ok = saveFile("isolation_" + cfg.side + "_" + cncStamp() + ".nc", "text/plain", r.text, false);
  pcbMsg(ok ? "ok" : "bad", (ok ? t("تم الحفظ — ", "Saved — ") : t("تعذّر الحفظ — ", "Save failed — ")) + r.loops + t(" مسار، ", " paths, ") + r.len.toFixed(0) + " mm" + t("، الوقت ≈ ", ", ≈ ") + r.min.toFixed(1) + " min");
};
gid("cncDrill").onclick = function () {
  var cfg = cncGenerate(); if (!cfg) return;
  var r = gcDrill(cfg);
  var ok = saveFile("drill_" + cfg.side + "_" + cncStamp() + ".nc", "text/plain", r.text, false);
  pcbMsg(ok ? "ok" : "bad", (ok ? t("تم الحفظ — ", "Saved — ") : t("تعذّر الحفظ — ", "Save failed — ")) + r.holes + t(" ثقب", " holes"));
};
gid("cncOutline").onclick = function () {
  var cfg = cncGenerate(); if (!cfg) return;
  var r = gcOutline(cfg);
  var ok = saveFile("outline_" + cncStamp() + ".nc", "text/plain", r.text, false);
  pcbMsg(ok ? "ok" : "bad", (ok ? t("تم الحفظ — ", "Saved — ") : t("تعذّر الحفظ — ", "Save failed — ")) + r.passes + t(" تمريرات", " passes"));
};
gid("cncZip").onclick = function () {
  var cfg = cncGenerate(); if (!cfg) return;
  var iso = gcIsolation(cfg);
  if (!iso) { pcbMsg("warn", t("لا توجد طبقة علوية في وضع طبقة واحدة.", "No top layer in 1-layer mode.")); return; }
  var dr = gcDrill(cfg), ol = gcOutline(cfg);
  pcbDraw();
  var ok = saveZip("cnc_" + cfg.side + "_" + cncStamp() + ".zip", [
    { name: "1_isolation.nc", text: iso.text }, { name: "2_drill.nc", text: dr.text }, { name: "3_outline.nc", text: ol.text }, { name: "README.txt", text: cncReadme(cfg) }
  ]);
  pcbMsg(ok ? "ok" : "bad", ok ? t("تم حفظ حزمة CNC في التنزيلات.", "CNC package saved to Downloads.") : t("تعذّر الحفظ.", "Could not save."));
};

applyLang();
if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener("resize", resize);
resize();
(function init() {
  var saved = "";
  try { if (window.Android && Android.loadState) saved = Android.loadState() || ""; } catch (e) { saved = ""; }
  var ok = false;
  if (saved) { try { ok = loadState(JSON.parse(saved), false); } catch (e) { ok = false; } }
  if (!ok) demo();
  undoStack = []; redoStack = []; updateUndoBtns();
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
import android.app.AlertDialog
import android.content.ContentValues
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import android.webkit.JsPromptResult
import android.webkit.WebChromeClient
import android.widget.EditText
import java.io.File
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
        s.mediaPlaybackRequiresUserGesture = false
        wv.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
                return !request.url.toString().startsWith(PAGE_PREFIX)
            }
        }
        wv.addJavascriptInterface(Bridge(), "Android")
        wv.webChromeClient = object : WebChromeClient() {
            override fun onJsPrompt(view: WebView?, url: String?, message: String?, defaultValue: String?, result: JsPromptResult?): Boolean {
                val input = EditText(this@CircuitSimulatorActivity).apply { setText(defaultValue ?: ""); setSingleLine(true) }
                AlertDialog.Builder(this@CircuitSimulatorActivity)
                    .setMessage(message ?: "")
                    .setView(input)
                    .setPositiveButton(android.R.string.ok) { _, _ -> result?.confirm(input.text.toString()) }
                    .setNegativeButton(android.R.string.cancel) { _, _ -> result?.cancel() }
                    .setOnCancelListener { result?.cancel() }
                    .show()
                return true
            }
        }
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

    override fun onPause() {
        web?.onPause()
        super.onPause()
    }

    override fun onResume() {
        super.onResume()
        web?.onResume()
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
        fun saveFile(name: String, mime: String, data: String, isBase64: Boolean): Boolean {
            return try {
                if (data.length > 12_000_000) return false
                val safe = name.replace(Regex("[^A-Za-z0-9._-]"), "_").take(80)
                if (safe.isEmpty()) return false
                val bytes = if (isBase64) android.util.Base64.decode(data, android.util.Base64.DEFAULT) else data.toByteArray(Charsets.UTF_8)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    val values = ContentValues().apply {
                        put(MediaStore.Downloads.DISPLAY_NAME, safe)
                        put(MediaStore.Downloads.MIME_TYPE, mime)
                        put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/CircuitLab")
                        put(MediaStore.Downloads.IS_PENDING, 1)
                    }
                    val uri = contentResolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values) ?: return false
                    val stream = contentResolver.openOutputStream(uri) ?: return false
                    stream.use { it.write(bytes) }
                    values.clear()
                    values.put(MediaStore.Downloads.IS_PENDING, 0)
                    contentResolver.update(uri, values, null, null)
                } else {
                    val dir = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS) ?: return false
                    dir.mkdirs()
                    File(dir, safe).writeBytes(bytes)
                }
                true
            } catch (e: Exception) {
                false
            }
        }

        @JavascriptInterface
        fun saveImage(dataUrl: String) {
            Thread {
                var ok = false
                try {
                    val b64 = dataUrl.substringAfter("base64,", "")
                    if (b64.isEmpty() || b64.length > 14_000_000) throw IOException("bad image")
                    val bytes = android.util.Base64.decode(b64, android.util.Base64.DEFAULT)
                    val name = "circuit_" + System.currentTimeMillis() + ".png"
                    if (android.os.Build.VERSION.SDK_INT >= 29) {
                        val values = android.content.ContentValues()
                        values.put(android.provider.MediaStore.Images.Media.DISPLAY_NAME, name)
                        values.put(android.provider.MediaStore.Images.Media.MIME_TYPE, "image/png")
                        values.put(android.provider.MediaStore.Images.Media.RELATIVE_PATH, android.os.Environment.DIRECTORY_PICTURES + "/CircuitLab")
                        values.put(android.provider.MediaStore.Images.Media.IS_PENDING, 1)
                        val uri = contentResolver.insert(android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values) ?: throw IOException("insert failed")
                        contentResolver.openOutputStream(uri)?.use { it.write(bytes) } ?: throw IOException("stream failed")
                        values.clear()
                        values.put(android.provider.MediaStore.Images.Media.IS_PENDING, 0)
                        contentResolver.update(uri, values, null, null)
                    } else {
                        val dir = getExternalFilesDir(android.os.Environment.DIRECTORY_PICTURES) ?: throw IOException("no dir")
                        java.io.File(dir, name).writeBytes(bytes)
                    }
                    ok = true
                } catch (e: Exception) {
                    ok = false
                }
                runOnUiThread { web?.evaluateJavascript("onImageSaved(" + ok + ")", null) }
            }.start()
        }

        @JavascriptInterface
        fun saveCloud(json: String) {
            Thread {
                try {
                    val base = backendBase()
                    val key = LicenseManager.getBackendKey()
                    val did = CreditsManager.currentDeviceId()
                    if (base.isEmpty()) {
                        runOnUiThread { web?.evaluateJavascript("onCloudSaved('', 'no_server')", null) }
                        return@Thread
                    }
                    if (key.isEmpty() || did.isEmpty()) {
                        runOnUiThread { web?.evaluateJavascript("onCloudSaved('', 'no_license')", null) }
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
                    runOnUiThread { web?.evaluateJavascript("onCloudSaved('', 'network_error')", null) }
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
            if (mode != "generate" && mode != "explain" && mode != "fix" && mode != "arduino_code") {
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
            fun buildChatRequest(): JSONObject = JSONObject().put("licenseKey", key).put("deviceId", did).put("provider", names.first()).put("providers", JSONArray(names)).put("systemPrompt", systemPrompt(mode, lang)).put("cost", 1).put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", payload)))

            var res: HttpRes
            if (mode == "arduino_code") {
                // غير مدعوم في /api/ai/circuit (يرد 400) → مباشرة إلى /api/ai/chat
                res = post(base + "/api/ai/chat", buildChatRequest())
            } else {
                val dedicated = JSONObject().put("licenseKey", key).put("deviceId", did).put("provider", names.first()).put("providers", JSONArray(names)).put("mode", mode).put("prompt", payload).put("lang", lang).put("cost", 1)
                res = post(base + "/api/ai/circuit", dedicated)
                if (res.code == 404) {
                    res = post(base + "/api/ai/chat", buildChatRequest())
                }
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
            return "You design simple DC circuits for a circuit simulator. Reply with ONE JSON object and nothing else (no markdown). Schema: {\"comps\":[{\"id\":\"B1\",\"type\":\"arduino\",\"val\":5},{\"id\":\"S1\",\"type\":\"switch\",\"closed\":true},{\"id\":\"RV1\",\"type\":\"potentiometer\",\"val\":1000,\"pos\":0.5},{\"id\":\"R1\",\"type\":\"resistor\",\"val\":330},{\"id\":\"D1\",\"type\":\"led\",\"val\":\"red\"}],\"wires\":[[\"B1.a\",\"S1.a\"],[\"S1.b\",\"RV1.a\"],[\"RV1.c\",\"R1.a\"],[\"R1.b\",\"D1.a\"],[\"D1.b\",\"B1.b\"]]}. Allowed types: battery (1.5,3,4.5,5,9,12), ac_source (5,12,24; 50 Hz sine, val is peak volts), arduino (5V), esp32 (3.3V), resistor (10,47,100,220,330,470,1000,2200,4700,10000), potentiometer (0,100,500,1000,5000,10000; terminals a and b are the ends, c is the wiper; optional pos 0..1 is the wiper position), ldr (1000,10000,100000; closed=true means dark), capacitor (10,47,100,470,1000), diode (silicon, germanium), transistor (NPN, terminals a=collector, b=emitter, c=base), relay (5,12; terminals a,b = coil, c = common contact, out = normally-open contact), gate_and (terminals a, b, out), gate_or (terminals a, b, out), gate_not (terminals a, out), fuse (0.5,1,2,5), led (red,green,yellow,blue,white), bulb (25,50,100), motor (5,10,20), buzzer (50,100,200), switch (conducts when closed=true). Every part has exactly two terminals a and b, except transistor and potentiometer which also have c; relay has a, b, c and out. Newer ICs in this lab: tda2030 (TDA2030 14W audio amplifier), lm2596 (buck converter), tp4056 (Li-ion charger), adc0804 (8-bit ADC), dac0808 (8-bit DAC), max7219 (7-segment display driver, 4 digits). These are simplified to 3 terminals (a=input, b=gnd, c=output). Additional ICs: lm741 (classic op-amp), ne5534 (low-noise audio op-amp), tda2822 (stereo 2W audio amplifier), cd4051 (8-channel analog MUX), pcf8574 (I2C 8-bit port expander), cd4066 (quad bilateral analog switch). All simplified to 3 terminals. More advanced ICs: tda7297 (stereo 15W amp), opa2134 (studio op-amp), ad620 (instrumentation amp), opa548 (3A power op-amp), lm337 (negative regulator), cd4013 (D flip-flop), cd4015 (shift register), 74hc273 (octal D-FF), 74hc373 (octal latch), at24c32 (EEPROM I2C), mcp23017 (16-bit I2C expander), 74hc00 (quad NAND). Logic gates output the supply voltage when true and read inputs against half the supply. Use ids B1,R1,D1. Always include exactly one power source, close the loop."
        } else if (mode == "arduino_code") {
            return "You are an Arduino expert. The user sends a circuit as JSON. Write complete, compilable Arduino C++ code (setup and loop) that makes the circuit behave as intended on an Arduino UNO. Infer the pin mapping from the wires: LEDs, buzzers and transistor bases are digital outputs, switches are inputs using INPUT_PULLUP, potentiometer wipers and LDR dividers are analog inputs, and logic gates are implemented as boolean expressions in code. Additional ICs available: TL072 (audio op-amp), LM324 (quad op-amp), NE556 (dual timer), ULN2003 (Darlington driver), LM1117 (LDO regulator), LM3914 (LED bar driver). When generating code for these, treat them as their functional equivalent (e.g., LM324 as a generic op-amp, NE556 as a dual 555). Start with a comment block listing the pin mapping. Write comments in $language. Return ONLY the code as plain text, no markdown fences."
        } else if (mode == "fix") {
            return "You are an electronics expert. The user sends a broken circuit as JSON. Fix it so it works perfectly. Return ONLY the fixed JSON object with the same schema (no markdown, no text). Ensure all LEDs have series resistors, there are no short circuits, and all loops are closed. A switch conducts when closed=true; an ldr is dark when closed=true; a potentiometer has ends a,b and wiper c."
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
        # الزر موجود، لكن استيراد Memory قد يكون مفقوداً (حالة حافة عند إعادة التشغيل)
        if MEMORY_IMPORT not in main_text:
            new_main = main_text
            for anchor in IMPORT_ANCHORS:
                if anchor in new_main:
                    new_main = new_main.replace(anchor, anchor + MEMORY_IMPORT, 1)
                    break
            else:
                die("لم أجد موضعاً لإضافة استيراد أيقونة Memory في ui/MainScreen.kt")
            writes[MAIN_SCREEN] = new_main
            done.append("ui/MainScreen.kt (إضافة استيراد Memory المفقود)")
        else:
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

    print(">> CIRCUIT LAB V15 applied:")
    for item in done:
        print("   + " + item)
    for item in skipped:
        print("   = تخطّي: " + item)

main()

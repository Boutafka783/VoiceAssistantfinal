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
  max7301: { prefix: "IOX01", ar: "MAX7301 توسعة", en: "MAX7301 IO Exp", vals: ["READ", "WRITE", "IDLE"], def: "IDLE", pins: 3 }
};
var BATCH19 = {ds18s20: 1, lm35: 1, lm75: 1, tmp102: 1, mcp9808: 1, max31865: 1, ads1118: 1, hdc1080: 1, htu21d: 1, sht21: 1, sht35: 1, aht10: 1, aht20: 1, ms5611: 1, lps25h: 1, bmp388: 1, dps310: 1, bmp085: 1, lps22hb: 1, mpx5700: 1, mq131: 1, mq303: 1, mhz19: 1, sds011: 1, pms5003: 1, ccs811: 1, ens160: 1, si1145: 1, veml7700: 1, opt3001: 1, max44009: 1, ltr329: 1, ml8511: 1, veml6070: 1, ina226: 1, ina260: 1, ina3221: 1, lis3dh: 1, mma8452: 1, adxl335: 1, adxl362: 1, lsm6ds3: 1, icm20948: 1, bno055: 1, hmc5883l: 1, qmc5883l: 1, mlx90393: 1, lm7815: 1, lm7824: 1, lm7808: 1, lm7806: 1, lm317hv: 1, lm2940: 1, tps7a47: 1, lm2576: 1, lm2574: 1, mp1584: 1, tps5430: 1, mt3608: 1, lm2577: 1, tps61023: 1, max1771: 1, lm3886: 1, tda7294: 1, tda2050: 1, tda7377: 1, tpa3116: 1, tpa2005: 1, lm4766: 1, drv8434: 1, tmc2209: 1, tmc2130: 1, l6470: 1, vnh5019: 1, drv8313: 1, a4950: 1, mx1508: 1, esp32cam: 1, sx1278: 1, sx1276: 1, nrf52832: 1, hm10: 1, jdy23: 1, ublox_neo6m: 1, ublox_neo7m: 1, w5500: 1, cp2102: 1, ch340: 1, max485: 1, mcp2515: 1, ssd1322: 1, ssd1327: 1, ssd1306_64: 1, st7789: 1, ili9488: 1, hd44780: 1, tm1637: 1, ht16k33: 1, cd4017b: 1, ic_74hc14: 1, ic_74hc04: 1, ic_74hc08: 1, ic_74hc32: 1, ic_74hc86: 1, ic_74hc74: 1, ic_74hc590: 1, ic_74hc4067: 1, at24c64: 1, at24c128: 1, w25q128: 1, fm25v02: 1, mcp23s17: 1, tca9534: 1, max7301: 1};
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
  max7301: { col: "#4f46e5", name: "IOX01", sub: function (c) { return String(c.val); } }
};
var MAX_COMPS = 45, MAX_WIRES = 100;

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
function hasThreePins(c) { return TYPES[c.type].pins === 3 || !!THREE_PIN_LEGACY[c.type]; }
function termList(c) {
  if (c.type === "relay") return ["a", "b", "c", "out"];
  if (c.type === "gate_not") return ["a", "out"];
  if (isGate(c)) return ["a", "b", "out"];
  if (hasThreePins(c)) return ["a", "b", "c"];
  return ["a", "b"];
}
function localTerm(c, which) {
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
function isSource(c) { return c.type === "battery" || c.type === "ac_source" || c.type === "arduino" || c.type === "esp32" || c.type === "nano" || c.type === "mega" || c.type === "esp8266" || c.type === "pico" || c.type === "solar" || c.type === "dc_jack"; }
function srcV(c, t) { return c.type === "ac_source" ? c.val * Math.sin(2 * Math.PI * 50 * t) : c.val; }
var SENSOR_SET = { mpu6050: 1, bmp280: 1, acs712: 1, a3144: 1, ky038: 1, yl69: 1, ttp223: 1, ky040: 1, tsop: 1, hc05: 1, l298n: 1, a4988: 1, pam8403: 1, max98357: 1, ads1115: 1, mcp4725: 1, ina219: 1, mq2: 1, bh1750: 1, vl53l0x: 1, ic_74hc165: 1, nrf24l01: 1, sim800l: 1, drv8825: 1, tb6612: 1, bts7960: 1, tcs34725: 1, mlx90614: 1, max30102: 1, adxl345: 1, hx711: 1, dht22: 1, sgp30: 1, rc522: 1, bme680: 1, pca9685: 1, tca9548a: 1, l9110s: 1, tmp36: 1, am2320: 1, ds1307: 1, pcf8563: 1, st7735: 1, ssd1351: 1, bmp180: 1, sht31: 1, apds9960: 1, ds1302: 1, max6675: 1, max31855: 1, sd_card: 1, enc28j60: 1, uln2803: 1, tlc5940: 1, mpu9250: 1, ad9833: 1, ams1117: 1, xl6009: 1, vl6180x: 1, sht10: 1, sht75: 1, si7021: 1, bme280: 1, mpl3115a2: 1, mq3: 1, mq4: 1, mq5: 1, mq6: 1, mq7: 1, mq8: 1, mq9: 1, mq135: 1, gp2y1010: 1, tsl2561: 1, tcs3200: 1, reed_switch: 1, vibration_sensor: 1, water_level: 1, flex_sensor: 1, tilt_switch: 1, shock_sensor: 1, flame_sensor: 1, rain_sensor: 1, hall_linear: 1, cd4071: 1, cd4081: 1, cd4030: 1, cd4001: 1, cd4023: 1, cd4025: 1, cd4070: 1, cd4075: 1, cd4077: 1, cd4093: 1, cd4538: 1, cd4047: 1, cd4027: 1, cd4029: 1, cd4076: 1, cd4022: 1, cd4060: 1, cd4541: 1, cd4511: 1, cd4028: 1, mcp3008: 1, mcp3208: 1, ads1015: 1, pcf8591: 1, tlc5615: 1, mcp4921: 1, at24c256: 1, at24c512: 1, w25q64: 1, mb85rc: 1, ds3234: 1, rv3028: 1, mcp7940: 1, nokia5110: 1, ssd1309: 1, st7565: 1, st7920: 1, ili9341: 1, ili9486: 1, max6954: 1, lcd_20x4: 1, st7735_160: 1, ssd1331: 1, drv8833: 1, drv8871: 1, l293e: 1, sn754410: 1, uln2004: 1, mc33926: 1, bd6221: 1, tb67h420: 1, a3959: 1, drv8824: 1, esp01: 1, rn2483: 1, rfm69: 1, rfm95: 1, hc12: 1, xbee: 1, sim900: 1, m95: 1, nrf905: 1, cc1101: 1, lm7809: 1, lm7812: 1, lm7905: 1, lm7912: 1, lm1084: 1, lm2678: 1, lm5007: 1, mcp1700: 1, mic5205: 1, lp2985: 1, lm4871: 1, tda2003: 1, ds18s20: 1, lm35: 1, lm75: 1, tmp102: 1, mcp9808: 1, max31865: 1, ads1118: 1, hdc1080: 1, htu21d: 1, sht21: 1, sht35: 1, aht10: 1, aht20: 1, ms5611: 1, lps25h: 1, bmp388: 1, dps310: 1, bmp085: 1, lps22hb: 1, mpx5700: 1, mq131: 1, mq303: 1, mhz19: 1, sds011: 1, pms5003: 1, ccs811: 1, ens160: 1, si1145: 1, veml7700: 1, opt3001: 1, max44009: 1, ltr329: 1, ml8511: 1, veml6070: 1, ina226: 1, ina260: 1, ina3221: 1, lis3dh: 1, mma8452: 1, adxl335: 1, adxl362: 1, lsm6ds3: 1, icm20948: 1, bno055: 1, hmc5883l: 1, qmc5883l: 1, mlx90393: 1, lm7815: 1, lm7824: 1, lm7808: 1, lm7806: 1, lm317hv: 1, lm2940: 1, tps7a47: 1, lm2576: 1, lm2574: 1, mp1584: 1, tps5430: 1, mt3608: 1, lm2577: 1, tps61023: 1, max1771: 1, lm3886: 1, tda7294: 1, tda2050: 1, tda7377: 1, tpa3116: 1, tpa2005: 1, lm4766: 1, drv8434: 1, tmc2209: 1, tmc2130: 1, l6470: 1, vnh5019: 1, drv8313: 1, a4950: 1, mx1508: 1, esp32cam: 1, sx1278: 1, sx1276: 1, nrf52832: 1, hm10: 1, jdy23: 1, ublox_neo6m: 1, ublox_neo7m: 1, w5500: 1, cp2102: 1, ch340: 1, max485: 1, mcp2515: 1, ssd1322: 1, ssd1327: 1, ssd1306_64: 1, st7789: 1, ili9488: 1, hd44780: 1, tm1637: 1, ht16k33: 1, cd4017b: 1, ic_74hc14: 1, ic_74hc04: 1, ic_74hc08: 1, ic_74hc32: 1, ic_74hc86: 1, ic_74hc74: 1, ic_74hc590: 1, ic_74hc4067: 1, at24c64: 1, at24c128: 1, w25q128: 1, fm25v02: 1, mcp23s17: 1, tca9534: 1, max7301: 1 };
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
  btnToggle.style.display = (c.type === "switch" || c.type === "ldr" || c.type === "a3144" || c.type === "ttp223" || c.type === "tsop" || c.type === "reed_switch" || c.type === "vibration_sensor" || c.type === "tilt_switch" || c.type === "shock_sensor" || c.type === "hall_linear" || c.type === "potentiometer" || c.type === "thermistor" || c.type === "pir" || c.type === "oled_ssd1306" || c.type === "cd4017" || c.type === "ne556" || c.type === "tp4056" || c.type === "adc0804" || c.type === "dac0808" || c.type === "max7219" || c.type === "cd4051" || c.type === "pcf8574" || c.type === "cd4066" || c.type === "cd4013" || c.type === "cd4015" || c.type === "ic_74hc273" || c.type === "ic_74hc373" || c.type === "at24c32" || c.type === "mcp23017") ? "" : "none";
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
  if (c && c.type === "potentiometer") { snap(); c.pos = ((Math.round(potPos(c) * 10) + 1) % 11) / 10; recompute(); }
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
  return comps.some(function (c) { return c.type === "buzzer" && Math.abs(sim.V[c.id]) > 1.0 && Math.abs(sim.I[c.id]) > 0.001; });
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
      if (c.type === "stepper_motor") c.ang = (c.ang || 0) + dt * Math.min(8, Math.abs(sim.V[c.id]) * 0.8) * (sim.I[c.id] < 0 ? -1 : 1);
      if (c.type === "motor") c.ang = (c.ang || 0) + dt * Math.min(30, Math.abs(sim.V[c.id]) * 3) * (sim.I[c.id] < 0 ? -1 : 1);
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

import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"
MAIN_SCREEN = PKG_DIR + "/ui/MainScreen.kt"

def replace_once(file_path, old, new, silent_if_exists=True):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if silent_if_exists and new in content:
        return
    if content.count(old) != 1:
        raise RuntimeError(f"Anchor not found exactly once in {file_path}: {old[:60]}")
    content = content.replace(old, new, 1)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

print(">> Applying Advanced Flight Simulator & Engineering Patch...")

# 1) إنشاء ملف flight_sim.html في مجلد assets
html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>مختبر هندسة الطيران</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
  :root { --bg: #0a0f18; --panel: rgba(13, 21, 34, 0.95); --border: rgba(53, 208, 255, 0.4); --text: #e8edf5; --accent: #35d0ff; --btn-bg: #ff9f1c; --btn-text: #1a1100; --warn: #ff4444; --good: #00ff88; }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  body, html { margin: 0; height: 100%; background: var(--bg); color: var(--text); font-family: system-ui, -apple-system, sans-serif; overflow: hidden; }
  #app { display: flex; flex-direction: column; height: 100vh; position: relative; }
  
  /* 3D Canvas */
  #canvas-container { position: absolute; inset: 0; z-index: 1; }
  
  /* HUD - يعرض الحسابات الفيزيائية */
  #hud { position: absolute; top: 10px; right: 10px; z-index: 2; background: var(--panel); border: 1px solid var(--border); padding: 8px 12px; border-radius: 8px; font-family: monospace; font-size: 0.85rem; text-align: right; pointer-events: none; line-height: 1.4; }
  #hud .val { color: var(--accent); font-weight: bold; }
  #hud .warn { color: var(--warn); font-weight: bold; }
  #hud .good { color: var(--good); font-weight: bold; }
  
  /* Builder Menu */
  #builder-panel { position: absolute; top: 10px; left: 10px; z-index: 2; background: var(--panel); border: 1px solid var(--border); padding: 8px; border-radius: 8px; display: flex; flex-direction: column; gap: 6px; width: 190px; max-height: 80vh; overflow-y: auto; }
  .builder-row { display: flex; flex-direction: column; gap: 2px; }
  .builder-row label { font-size: 0.75rem; color: #aaa; }
  .builder-row select { padding: 4px; border-radius: 4px; border: 1px solid var(--border); background: #060a12; color: #fff; outline: none; font-size: 0.8rem; }
  
  /* AI Panel */
  #ai-panel { position: absolute; bottom: 90px; left: 10px; z-index: 2; width: 250px; display: flex; flex-direction: column; gap: 6px; }
  #ai-input { width: 100%; padding: 8px; border-radius: 6px; border: 1px solid var(--border); background: var(--panel); color: var(--text); outline: none; font-size: 0.85rem; }
  #ai-btn { padding: 8px; background: var(--accent); color: #000; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.9rem; }
  #ai-result { font-size: 0.75rem; color: #ff9f1c; background: var(--panel); padding: 6px; border-radius: 6px; display: none; border: 1px solid #ff9f1c; line-height: 1.3; }
  
  /* Controls */
  #controls { position: absolute; bottom: 15px; left: 15px; right: 15px; z-index: 2; display: flex; justify-content: space-between; pointer-events: none; }
  .control-group { display: flex; gap: 8px; pointer-events: auto; }
  .btn-ctrl { width: 50px; height: 50px; border-radius: 50%; border: 2px solid var(--border); background: var(--panel); color: var(--text); font-size: 1.2rem; display: flex; justify-content: center; align-items: center; cursor: pointer; user-select: none; }
  .btn-ctrl:active { background: rgba(53, 208, 255, 0.3); border-color: var(--accent); }
  
  #throttle-group { flex-direction: column; align-items: flex-end; }
  #throttle-bar { width: 15px; height: 100px; background: var(--panel); border: 2px solid var(--border); border-radius: 8px; position: relative; overflow: hidden; }
  #throttle-fill { position: absolute; bottom: 0; left: 0; right: 0; background: var(--accent); transition: height 0.1s; }
  #throttle-text { margin-top: 4px; font-family: monospace; font-size: 0.9rem; }
</style>
</head>
<body>
<div id="app">
  <div id="canvas-container"></div>
  
  <div id="hud">
    السرعة: <span class="val" id="hud-speed">0</span> km/h<br>
    الارتفاع: <span class="val" id="hud-alt">0</span> m<br>
    <hr style="border-color:#333; margin:4px 0;">
    الوزن: <span class="val" id="hud-weight">0</span> g<br>
    الدفع: <span class="val" id="hud-thrust">0</span> g<br>
    TWR: <span id="hud-twr">0</span><br>
    البطارية: <span class="val" id="hud-bat">100</span>%<br>
    الطيران: <span class="val" id="hud-time">0</span> دقيقة<br>
    المدى: <span class="val" id="hud-range">0</span> كم
  </div>
  
  <div id="builder-panel">
    <div class="builder-row">
      <label>الهيكل (Fuselage)</label>
      <select id="sel-fuselage" onchange="updatePlane()">
        <option value="standard">طائرة عادية (400g)</option>
        <option value="drone">درون (300g)</option>
        <option value="heavy">شحن ثقيل (1200g)</option>
      </select>
    </div>
    <div class="builder-row">
      <label>البطارية (Battery)</label>
      <select id="sel-battery" onchange="updatePlane()">
        <option value="3s">3S 1500mAh (130g)</option>
        <option value="4s">4S 2200mAh (250g)</option>
        <option value="6s">6S 5000mAh (650g)</option>
      </select>
    </div>
    <div class="builder-row">
      <label>المحرك (Motor)</label>
      <select id="sel-engine" onchange="updatePlane()">
        <option value="small">صغير (200g دفع - 30g)</option>
        <option value="medium">متوسط (800g دفع - 60g)</option>
        <option value="large">كبير (2000g دفع - 120g)</option>
      </select>
    </div>
    <div class="builder-row">
      <label>المروحة (Propeller)</label>
      <select id="sel-prop" onchange="updatePlane()">
        <option value="small">صغيرة (كفاءة عالية - 10g)</option>
        <option value="large">كبيرة (دفع أعلى - 25g)</option>
      </select>
    </div>
    <div class="builder-row">
      <label>التحكم (RC Tech)</label>
      <select id="sel-rc" onchange="updatePlane()">
        <option value="24g">2.4GHz (مدى 1كم)</option>
        <option value="58g">5.8GHz (مدى 3كم)</option>
        <option value="4g">4G/WiFi (مدى لامحدود)</option>
      </select>
    </div>
  </div>
  
  <div id="ai-panel">
    <input type="text" id="ai-input" placeholder="مثال: طائرة تطير 20 دقيقة..." />
    <button id="ai-btn">✨ مهندس الطيران AI</button>
    <div id="ai-result"></div>
  </div>
  
  <div id="controls">
    <div class="control-group">
      <div class="btn-ctrl" id="btn-pitch-down">⬇️</div>
      <div class="btn-ctrl" id="btn-pitch-up">⬆️</div>
    </div>
    <div class="control-group" id="throttle-group">
      <div id="throttle-bar"><div id="throttle-fill" style="height: 0%;"></div></div>
      <div id="throttle-text">0%</div>
    </div>
    <div class="control-group">
      <div class="btn-ctrl" id="btn-roll-left">⬅️</div>
      <div class="btn-ctrl" id="btn-roll-right">➡️</div>
    </div>
  </div>
</div>

<script>
  // --- إعداد Three.js ---
  const container = document.getElementById('canvas-container');
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x87CEEB);
  scene.fog = new THREE.Fog(0x87CEEB, 100, 1000);

  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  container.appendChild(renderer.domElement);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(100, 200, 50);
  scene.add(dirLight);

  const gridHelper = new THREE.GridHelper(2000, 100, 0x000000, 0x444444);
  gridHelper.position.y = -10;
  scene.add(gridHelper);

  // --- نظام بناء الطائرة والفيزياء ---
  let planeGroup = new THREE.Group();
  scene.add(planeGroup);
  
  let specs = {
    mass: 0,          // الوزن الكلي بالجرام
    maxThrust: 0,     // أقصى قوة دفع بالجرام
    batteryMah: 0,    // سعة البطارية
    ampDrawMax: 0,    // سحب التيار الأقصى (أمبير)
    rcRangeKm: 0      // مدى التحكم
  };

  function updatePlane() {
    // 1. جلب الاختيارات
    const fType = document.getElementById('sel-fuselage').value;
    const bType = document.getElementById('sel-battery').value;
    const eType = document.getElementById('sel-engine').value;
    const pType = document.getElementById('sel-prop').value;
    const rcType = document.getElementById('sel-rc').value;

    // 2. إعادة بناء المجسم (شكل الطائرة)
    while(planeGroup.children.length > 0) planeGroup.remove(planeGroup.children[0]);
    
    let bodyMat = new THREE.MeshStandardMaterial({ color: 0xcccccc });
    let bodyGeo;
    if (fType === 'drone') {
      bodyGeo = new THREE.BoxGeometry(2, 0.5, 2);
      bodyMat.color.setHex(0x333333);
    } else if (fType === 'heavy') {
      bodyGeo = new THREE.CylinderGeometry(1.2, 1.2, 8, 8);
      bodyGeo.rotateX(Math.PI / 2);
      bodyMat.color.setHex(0x808080);
    } else {
      bodyGeo = new THREE.CylinderGeometry(0.5, 0.5, 6, 8);
      bodyGeo.rotateX(Math.PI / 2);
    }
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    planeGroup.add(body);

    // الأجنحة
    const wingGeo = new THREE.BoxGeometry(fType === 'drone' ? 6 : 8, 0.2, 1.5);
    const wingMat = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
    const wing = new THREE.Mesh(wingGeo, wingMat);
    planeGroup.add(wing);

    // الذيل (ليس للدرون)
    if (fType !== 'drone') {
      const tail = new THREE.Mesh(new THREE.BoxGeometry(2, 0.2, 0.8), wingMat);
      tail.position.set(0, 0.5, -2.5);
      planeGroup.add(tail);
    }

    // 3. الحسابات الفيزيائية
    let mass = 0;
    let thrust = 0;
    let batMah = 0;
    let ampMax = 0;

    // الهيكل
    mass += fType === 'drone' ? 300 : fType === 'heavy' ? 1200 : 400;

    // البطارية
    if (bType === '3s') { mass += 130; batMah = 1500; }
    else if (bType === '4s') { mass += 250; batMah = 2200; }
    else { mass += 650; batMah = 5000; }

    // المحرك
    if (eType === 'small') { mass += 30; thrust += 200; ampMax = 10; }
    else if (eType === 'medium') { mass += 60; thrust += 800; ampMax = 25; }
    else { mass += 120; thrust += 2000; ampMax = 50; }

    // المروحة
    if (pType === 'small') { mass += 10; thrust *= 0.8; ampMax *= 0.7; } // كفاءة عالية، دفع أقل
    else { mass += 25; thrust *= 1.2; ampMax *= 1.3; } // دفع أعلى، استهلاك أعلى

    // التحكم
    let range = 0;
    if (rcType === '24g') range = 1;
    else if (rcType === '58g') range = 3;
    else range = 999; // 4G

    specs.mass = mass;
    specs.maxThrust = thrust;
    specs.batteryMah = batMah;
    specs.ampDrawMax = ampMax;
    specs.rcRangeKm = range;

    // تحديث شاشة HUD
    document.getElementById('hud-weight').innerText = mass;
    document.getElementById('hud-thrust').innerText = thrust;
    
    let twr = thrust / mass;
    let twrEl = document.getElementById('hud-twr');
    twrEl.innerText = twr.toFixed(2);
    if (twr < 1) {
      twrEl.className = 'warn';
      twrEl.innerText += ' (لا يطير!)';
    } else if (twr > 2) {
      twrEl.className = 'good';
      twrEl.innerText += ' (قوي جداً)';
    } else {
      twrEl.className = 'val';
    }

    document.getElementById('hud-range').innerText = range === 999 ? '∞' : range;

    // إعادة ضبط حالة الطيران عند تغيير القطع
    state.throttle = 0;
    document.getElementById('throttle-fill').style.height = '0%';
    document.getElementById('throttle-text').innerText = '0%';
    state.battery = 100;
  }

  updatePlane();
  planeGroup.position.set(0, 0, 0);

  // --- حالة الطيران ---
  let state = {
    speed: 0,         // m/s
    throttle: 0,      // 0 to 1
    pitch: 0,         // degrees
    roll: 0,          // degrees
    altitude: 0,      // meters
    pitchInput: 0,
    rollInput: 0,
    battery: 100      // %
  };

  // --- التحكم ---
  function setThrottle(val) {
    state.throttle = Math.max(0, Math.min(1, val));
    document.getElementById('throttle-fill').style.height = (state.throttle * 100) + '%';
    document.getElementById('throttle-text').innerText = Math.round(state.throttle * 100) + '%';
  }

  document.getElementById('btn-pitch-up').addEventListener('pointerdown', () => state.pitchInput = 1);
  document.getElementById('btn-pitch-down').addEventListener('pointerdown', () => state.pitchInput = -1);
  document.getElementById('btn-roll-left').addEventListener('pointerdown', () => state.rollInput = -1);
  document.getElementById('btn-roll-right').addEventListener('pointerdown', () => state.rollInput = 1);
  window.addEventListener('pointerup', () => { state.pitchInput = 0; state.rollInput = 0; });

  // --- المساعد الذكي (مهندس الطيران) ---
  const aiInput = document.getElementById('ai-input');
  const aiBtn = document.getElementById('ai-btn');
  const aiResult = document.getElementById('ai-result');

  aiBtn.addEventListener('click', () => {
    const prompt = aiInput.value.trim();
    if (!prompt) return;
    
    aiResult.style.display = 'block';
    aiResult.innerText = 'جاري الحساب الهندسي...';
    
    if (window.Android && window.Android.askAi) {
      let sysPrompt = `أنت مهندس طيران خبير. المستخدم يطلب: "${prompt}". 
      عليك اختيار أفضل قطع للطائرة بناءً على هذا الطلب. الخيارات المتاحة:
      - الهيكل (fuselage): 'standard' (400g), 'drone' (300g), 'heavy' (1200g)
      - البطارية (battery): '3s' (1500mAh/130g), '4s' (2200mAh/250g), '6s' (5000mAh/650g)
      - المحرك (engine): 'small' (200g thrust), 'medium' (800g thrust), 'large' (2000g thrust)
      - المروحة (prop): 'small' (efficient), 'large' (high thrust)
      - التحكم (rc): '24g' (1km), '58g' (3km), '4g' (unlimited)
      
      أعد كود JavaScript فقط لتغيير الاختيارات، متبوعاً بشرح قصير جداً.
      مثال للرد:
      document.getElementById('sel-fuselage').value = 'drone';
      document.getElementById('sel-battery').value = '4s';
      document.getElementById('sel-engine').value = 'medium';
      document.getElementById('sel-prop').value = 'large';
      document.getElementById('sel-rc').value = '58g';
      updatePlane();
      aiResult.innerText = 'اخترت محرك متوسط مع بطارية 4S لتحقيق التوازن بين الوزن والوقت.';
      
      أعد الكود والشرح فقط بدون أي markdown.`;
      window.Android.askAi('flight_engineer', sysPrompt);
    } else {
      aiResult.innerText = 'Android bridge not available';
    }
  });

  window.onAiResult = function(id, ok, text) {
    if (id !== 'flight_engineer') return;
    if (!ok) {
      aiResult.innerText = 'خطأ: ' + text;
      return;
    }
    let code = text.trim();
    if (code.startsWith('```')) code = code.replace(/^```[a-z]*\n/, '').replace(/\n```$/, '');
    
    try {
      // تنفيذ كود الذكاء الاصطناعي لبناء الطائرة
      eval(code);
    } catch (e) {
      aiResult.innerText = 'خطأ في التنفيذ: ' + e.message;
    }
  };

  // --- دورة المحاكاة (الفيزياء) ---
  let lastTime = performance.now();
  
  function animate() {
    requestAnimationFrame(animate);
    let dt = (performance.now() - lastTime) / 1000;
    lastTime = performance.now();
    if (dt > 0.1) dt = 0.1;

    // 1. حساب الدفع المتاح
    const currentThrust = specs.maxThrust * state.throttle;
    
    // إذا كانت البطارية فارغة، يتوقف المحرك
    if (state.battery <= 0) {
      state.throttle = 0;
      currentThrust = 0;
    }

    // 2. حساب المقاومة (Drag) - تزيد مع مربع السرعة
    const drag = 0.05 * state.speed * state.speed;
    
    // 3. حساب التسارع (F = ma -> a = F/m)
    // القوة الصافية = الدفع - المقاومة - (الجاذبية إذا كان يصعد)
    const netForce = currentThrust - drag;
    const acceleration = netForce / specs.mass;
    state.speed += acceleration * dt * 0.1; // معامل تصغير للعبة
    
    if (state.speed < 0) state.speed = 0;

    // 4. حساب الرفع (Lift)
    // الرفع يعتمد على مربع السرعة. إذا قل الرفع عن الوزن، تسقط الطائرة.
    const lift = 0.01 * state.speed * state.speed;
    const gravity = specs.mass * 0.0098;
    
    let verticalSpeed = 0;
    if (lift > gravity) {
      verticalSpeed = (lift - gravity) * 0.01;
    } else {
      verticalSpeed = (lift - gravity) * 0.05; // سقوط أسرع
    }

    state.altitude += verticalSpeed * dt;
    if (state.altitude < 0) {
      state.altitude = 0;
      state.speed *= 0.9; // احتكاك بالأرض
    }

    // 5. استهلاك البطارية
    if (state.throttle > 0) {
      const amps = specs.ampDrawMax * state.throttle;
      const batteryDrain = (amps / specs.batteryMah) * 100 / 60; // % لكل ثانية
      state.battery -= batteryDrain * dt * 10; // معامل تصغير للعبة
      if (state.battery < 0) state.battery = 0;
    }

    // 6. التحكم بالزوايا
    state.pitch += state.pitchInput * 45 * dt;
    state.roll += state.rollInput * 90 * dt;
    if (state.pitchInput === 0) state.pitch *= 0.9;
    if (state.rollInput === 0) state.roll *= 0.9;
    state.pitch = Math.max(-45, Math.min(45, state.pitch));
    state.roll = Math.max(-60, Math.min(60, state.roll));

    // تطبيق الزوايا
    planeGroup.rotation.x = state.pitch * Math.PI / 180;
    planeGroup.rotation.z = state.roll * Math.PI / 180;

    // الحركة للأمام
    planeGroup.translateZ(state.speed * dt * 0.5);

    // تحديث HUD
    document.getElementById('hud-speed').innerText = Math.round(state.speed * 3.6); // m/s to km/h
    document.getElementById('hud-alt').innerText = Math.round(state.altitude);
    document.getElementById('hud-bat').innerText = Math.round(state.battery);

    // حساب زمن الطيران المتبقي التقريبي
    if (state.throttle > 0.1) {
      const amps = specs.ampDrawMax * state.throttle;
      const mins = (specs.batteryMah * (state.battery / 100) / 1000) / amps * 60;
      document.getElementById('hud-time').innerText = mins.toFixed(1);
    } else {
      document.getElementById('hud-time').innerText = '0';
    }

    // تتبع الكاميرا
    const camOffset = new THREE.Vector3(0, 5, -15);
    camOffset.applyQuaternion(planeGroup.quaternion);
    camera.position.lerp(planeGroup.position.clone().add(camOffset), 0.1);
    camera.lookAt(planeGroup.position);

    renderer.render(scene, camera);
  }

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  animate();
</script>
</body>
</html>
'''

os.makedirs("app/src/main/assets", exist_ok=True)
with open("app/src/main/assets/flight_sim.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# 2) إنشاء FlightSimActivity.kt
activity_content = r'''package com.zevorix.assistant

import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.material3.Surface
import androidx.compose.material3.MaterialTheme
import com.zevorix.assistant.data.AiChatService
import com.zevorix.assistant.data.AiResult
import com.zevorix.assistant.ui.theme.VoiceAssistantTheme
import kotlinx.coroutines.*

class FlightSimActivity : ComponentActivity() {
    private val aiService = AiChatService()
    
    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            VoiceAssistantTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    AndroidView(
                        modifier = Modifier.fillMaxSize(),
                        factory = { context ->
                            WebView(context).apply {
                                settings.javaScriptEnabled = true
                                settings.domStorageEnabled = true
                                settings.allowFileAccess = true
                                webViewClient = WebViewClient()
                                addJavascriptInterface(Bridge(this@FlightSimActivity, this, aiService), "Android")
                                loadUrl("file:///android_asset/flight_sim.html")
                            }
                        }
                    )
                }
            }
        }
    }
    
    class Bridge(private val activity: ComponentActivity, private val webView: WebView, private val aiService: AiChatService) {
        @JavascriptInterface
        fun askAi(id: String, prompt: String) {
            CoroutineScope(Dispatchers.IO).launch {
                val lang = if (prompt.any { it in '\u0600'..'\u06FF' }) com.zevorix.assistant.viewmodel.AppLanguage.ARABIC else com.zevorix.assistant.viewmodel.AppLanguage.ENGLISH
                val result = aiService.ask(prompt, lang)
                withContext(Dispatchers.Main) {
                    when (result) {
                        is AiResult.Success -> {
                            val safeText = result.text.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "")
                            webView.evaluateJavascript("window.onAiResult(\"$id\", true, \"$safeText\");", null)
                        }
                        is AiResult.Error -> {
                            val msg = "Error: ${result.kind} ${result.detail}"
                            val safeText = msg.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                            webView.evaluateJavascript("window.onAiResult(\"$id\", false, \"$safeText\");", null)
                        }
                    }
                }
            }
        }
    }
}
'''

with open(PKG_DIR + "/FlightSimActivity.kt", "w", encoding="utf-8") as f:
    f.write(activity_content)

# 3) تسجيل النشاط في AndroidManifest.xml
replace_once(
    MANIFEST,
    '</application>',
    '    <!-- Flight Simulator & Builder -->\n'
    '    <activity\n'
    '        android:name=".FlightSimActivity"\n'
    '        android:exported="false"\n'
    '        android:theme="@style/Theme.VoiceAssistant" />\n\n'
    '</application>'
)

# 4) إضافة الزر في واجهة التطبيق (MainScreen.kt)
replace_once(
    MAIN_SCREEN,
    "import com.zevorix.assistant.ui.components.AiSettingsSheet\n",
    "import com.zevorix.assistant.ui.components.AiSettingsSheet\n"
    "import com.zevorix.assistant.FlightSimActivity\n"
    "import androidx.compose.material.icons.filled.FlightTakeoff\n"
)

with open(MAIN_SCREEN, "r", encoding="utf-8") as f:
    ms_content = f.read()

if "FlightSimActivity" not in ms_content:
    match = re.search(r'(?m)^\s*DropdownMenuItem\(\s*$', ms_content)
    if match:
        line_start = ms_content.rfind("\n", 0, match.start()) + 1
        indent = ms_content[line_start:match.start()]
        insertion = (
            f"{indent}DropdownMenuItem(\n"
            f'{indent}    text = {{ Text(state.language.tr("مختبر هندسة الطيران", "Aerospace Engineering Lab")) }},\n'
            f"{indent}    leadingIcon = {{ Icon(Icons.Filled.FlightTakeoff, contentDescription = null) }},\n"
            f"{indent}    onClick = {{\n"
            f"{indent}        showSettingsMenu = false\n"
            f"{indent}        context.startActivity(android.content.Intent(context, FlightSimActivity::class.java))\n"
            f"{indent}    }}\n"
            f"{indent}}})\n"
        )
        ms_content = ms_content[:line_start] + insertion + ms_content[line_start:]
        with open(MAIN_SCREEN, "w", encoding="utf-8", newline="\n") as f:
            f.write(ms_content)
        print(">> Inserted Aerospace Engineering Lab menu item dynamically.")
    else:
        raise RuntimeError("Could not find DropdownMenuItem to insert Aerospace Engineering Lab.")

print(">> Aerospace Engineering Lab Patch applied successfully!")
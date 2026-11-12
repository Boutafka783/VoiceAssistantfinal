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

print(">> Applying Flight Simulator + Aircraft Builder Patch...")

# 1) إنشاء ملف flight_sim.html في مجلد assets
html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>محاكي ومصمم الطيران</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
  :root { --bg: #0a0f18; --panel: rgba(13, 21, 34, 0.9); --border: rgba(53, 208, 255, 0.4); --text: #e8edf5; --accent: #35d0ff; --btn-bg: #ff9f1c; --btn-text: #1a1100; }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  body, html { margin: 0; height: 100%; background: var(--bg); color: var(--text); font-family: system-ui, -apple-system, sans-serif; overflow: hidden; }
  #app { display: flex; flex-direction: column; height: 100vh; position: relative; }
  
  /* 3D Canvas */
  #canvas-container { position: absolute; inset: 0; z-index: 1; }
  
  /* HUD */
  #hud { position: absolute; top: 15px; right: 15px; z-index: 2; background: var(--panel); border: 1px solid var(--border); padding: 10px 15px; border-radius: 8px; font-family: monospace; font-size: 1.1rem; text-align: right; pointer-events: none; }
  #hud .val { color: var(--accent); font-weight: bold; }
  
  /* Builder Menu */
  #builder-panel { position: absolute; top: 15px; left: 15px; z-index: 2; background: var(--panel); border: 1px solid var(--border); padding: 10px; border-radius: 8px; display: flex; flex-direction: column; gap: 8px; width: 220px; }
  .builder-row { display: flex; flex-direction: column; gap: 4px; }
  .builder-row label { font-size: 0.8rem; color: #aaa; }
  .builder-row select { padding: 6px; border-radius: 6px; border: 1px solid var(--border); background: #060a12; color: #fff; outline: none; }
  
  /* AI Panel */
  #ai-panel { position: absolute; bottom: 100px; left: 15px; z-index: 2; width: 280px; display: flex; flex-direction: column; gap: 8px; }
  #ai-input { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--panel); color: var(--text); outline: none; }
  #ai-btn { padding: 10px; background: var(--accent); color: #000; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
  #ai-result { font-size: 0.85rem; color: #ff9f1c; background: var(--panel); padding: 8px; border-radius: 8px; display: none; }
  
  /* Controls */
  #controls { position: absolute; bottom: 20px; left: 20px; right: 20px; z-index: 2; display: flex; justify-content: space-between; pointer-events: none; }
  .control-group { display: flex; gap: 10px; pointer-events: auto; }
  .btn-ctrl { width: 60px; height: 60px; border-radius: 50%; border: 2px solid var(--border); background: var(--panel); color: var(--text); font-size: 1.5rem; display: flex; justify-content: center; align-items: center; cursor: pointer; user-select: none; }
  .btn-ctrl:active { background: rgba(53, 208, 255, 0.3); border-color: var(--accent); }
  
  #throttle-group { flex-direction: column; align-items: flex-end; }
  #throttle-bar { width: 20px; height: 150px; background: var(--panel); border: 2px solid var(--border); border-radius: 10px; position: relative; overflow: hidden; }
  #throttle-fill { position: absolute; bottom: 0; left: 0; right: 0; background: var(--accent); transition: height 0.1s; }
  #throttle-text { margin-top: 5px; font-family: monospace; font-size: 1.2rem; }
</style>
</head>
<body>
<div id="app">
  <div id="canvas-container"></div>
  
  <div id="hud">
    السرعة: <span class="val" id="hud-speed">0</span> kn<br>
    الارتفاع: <span class="val" id="hud-alt">0</span> ft
  </div>
  
  <div id="builder-panel">
    <div class="builder-row">
      <label>جسم الطائرة</label>
      <select id="sel-fuselage" onchange="updatePlane()">
        <option value="standard">عادي</option>
        <option value="fighter">مقاتلة</option>
        <option value="heavy">شحن ثقيل</option>
      </select>
    </div>
    <div class="builder-row">
      <label>الأجنحة</label>
      <select id="sel-wings" onchange="updatePlane()">
        <option value="standard">مستقيمة</option>
        <option value="delta">مثلثة (Delta)</option>
        <option value="biplane">مزدوجة</option>
      </select>
    </div>
    <div class="builder-row">
      <label>المحرك</label>
      <select id="sel-engine" onchange="updatePlane()">
        <option value="propeller">مروحة</option>
        <option value="jet">نفاث</option>
        <option value="twin">مزدوج</option>
      </select>
    </div>
    <div class="builder-row">
      <label>الذيل</label>
      <select id="sel-tail" onchange="updatePlane()">
        <option value="standard">عادي</option>
        <option value="v-tail">ذيل V</option>
      </select>
    </div>
  </div>
  
  <div id="ai-panel">
    <input type="text" id="ai-input" placeholder="مثال: اصنع لي طائرة مقاتلة سريعة..." />
    <button id="ai-btn">✨ المساعد الذكي</button>
    <div id="ai-result"></div>
  </div>
  
  <div id="controls">
    <div class="control-group">
      <div class="btn-ctrl" id="btn-pitch-down">⬇️</div>
      <div class="btn-ctrl" id="btn-pitch-up">⬆️</div>
    </div>
    <div class="control-group" id="throttle-group">
      <div id="throttle-bar"><div id="throttle-fill" style="height: 50%;"></div></div>
      <div id="throttle-text">50%</div>
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

  // --- نظام بناء الطائرة ---
  let planeGroup = new THREE.Group();
  scene.add(planeGroup);
  
  let specs = { speedMax: 150, agility: 1.0, lift: 1.0 };

  function buildPlaneModel() {
    // مسح الطائرة القديمة
    while(planeGroup.children.length > 0){ 
        planeGroup.remove(planeGroup.children[0]); 
    }

    const fuselageType = document.getElementById('sel-fuselage').value;
    const wingsType = document.getElementById('sel-wings').value;
    const engineType = document.getElementById('sel-engine').value;
    const tailType = document.getElementById('sel-tail').value;

    // 1. الجسم (Fuselage)
    let bodyGeo, bodyMat = new THREE.MeshStandardMaterial({ color: 0xcccccc });
    if (fuselageType === 'fighter') {
      bodyGeo = new THREE.CylinderGeometry(0.4, 0.8, 7, 8); // مدبب من الأمام
      bodyGeo.rotateX(Math.PI / 2);
      bodyMat.color.setHex(0x556b2f); // لون عسكري
      specs.speedMax = 250; specs.agility = 1.5; specs.lift = 0.8;
    } else if (fuselageType === 'heavy') {
      bodyGeo = new THREE.CylinderGeometry(1.2, 1.2, 8, 8);
      bodyGeo.rotateX(Math.PI / 2);
      bodyMat.color.setHex(0x808080); // رمادي ثقيل
      specs.speedMax = 100; specs.agility = 0.6; specs.lift = 1.5;
    } else {
      bodyGeo = new THREE.CylinderGeometry(0.5, 0.5, 6, 8);
      bodyGeo.rotateX(Math.PI / 2);
      specs.speedMax = 180; specs.agility = 1.0; specs.lift = 1.0;
    }
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    planeGroup.add(body);

    // 2. الأجنحة (Wings)
    let wingGeo, wingMat = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
    if (wingsType === 'delta') {
      wingGeo = new THREE.BoxGeometry(6, 0.2, 3);
      const wing = new THREE.Mesh(wingGeo, wingMat);
      wing.position.set(0, 0, 0.5);
      planeGroup.add(wing);
      specs.agility += 0.3;
    } else if (wingsType === 'biplane') {
      const w1 = new THREE.Mesh(new THREE.BoxGeometry(7, 0.2, 1.5), wingMat);
      const w2 = new THREE.Mesh(new THREE.BoxGeometry(7, 0.2, 1.5), wingMat);
      w1.position.set(0, 0.5, 0);
      w2.position.set(0, -0.5, 0);
      planeGroup.add(w1, w2);
      specs.speedMax -= 30; specs.lift += 0.5;
    } else {
      wingGeo = new THREE.BoxGeometry(8, 0.2, 1.5);
      const wing = new THREE.Mesh(wingGeo, wingMat);
      planeGroup.add(wing);
    }

    // 3. الذيل (Tail)
    let tailMat = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
    if (tailType === 'v-tail') {
      const t1 = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.2, 0.8), tailMat);
      t1.position.set(-0.5, 0.5, -2.5);
      t1.rotation.z = Math.PI / 4;
      const t2 = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.2, 0.8), tailMat);
      t2.position.set(0.5, 0.5, -2.5);
      t2.rotation.z = -Math.PI / 4;
      planeGroup.add(t1, t2);
    } else {
      const t1 = new THREE.Mesh(new THREE.BoxGeometry(2, 0.2, 0.8), tailMat);
      t1.position.set(0, 0.5, -2.5);
      const t2 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1, 0.8), tailMat);
      t2.position.set(0, 0.8, -2.5);
      planeGroup.add(t1, t2);
    }

    // 4. المحرك (Engine)
    let engMat = new THREE.MeshStandardMaterial({ color: 0x333333 });
    if (engineType === 'jet') {
      const eng = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 2, 8), engMat);
      eng.rotation.x = Math.PI / 2;
      eng.position.set(0, 0, 3.5);
      planeGroup.add(eng);
      specs.speedMax += 80;
    } else if (engineType === 'twin') {
      const e1 = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 1.5, 8), engMat);
      e1.rotation.x = Math.PI / 2;
      e1.position.set(-3, -0.5, 0);
      const e2 = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 1.5, 8), engMat);
      e2.rotation.x = Math.PI / 2;
      e2.position.set(3, -0.5, 0);
      planeGroup.add(e1, e2);
      specs.speedMax += 40; specs.lift += 0.3;
    } else {
      // مروحة
      const eng = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 1, 8), engMat);
      eng.rotation.x = Math.PI / 2;
      eng.position.set(0, 0, 3.5);
      const prop = new THREE.Mesh(new THREE.BoxGeometry(0.1, 3, 0.1), new THREE.MeshStandardMaterial({color: 0x000000}));
      prop.position.set(0, 0, 4);
      planeGroup.add(eng, prop);
    }

    // المقدمة
    const noseGeo = new THREE.ConeGeometry(0.5, 1.5, 8);
    noseGeo.rotateX(-Math.PI / 2);
    const nose = new THREE.Mesh(noseGeo, bodyMat);
    nose.position.set(0, 0, 3.75);
    planeGroup.add(nose);
  }

  // دالة تُستدعى عند تغيير الاختيارات اليدوية
  window.updatePlane = function() {
    buildPlaneModel();
  };

  // بناء الطائرة الافتراضية
  buildPlaneModel();
  planeGroup.position.set(0, 50, 0);

  // --- حالة الطيران ---
  let state = {
    speed: 0,
    throttle: 0.5,
    pitch: 0,
    roll: 0,
    altitude: 50,
    pitchInput: 0,
    rollInput: 0
  };

  // --- التحكم ---
  const throttleFill = document.getElementById('throttle-fill');
  const throttleText = document.getElementById('throttle-text');
  
  function setThrottle(val) {
    state.throttle = Math.max(0, Math.min(1, val));
    throttleFill.style.height = (state.throttle * 100) + '%';
    throttleText.innerText = Math.round(state.throttle * 100) + '%';
  }

  document.getElementById('btn-pitch-up').addEventListener('pointerdown', () => state.pitchInput = 1);
  document.getElementById('btn-pitch-down').addEventListener('pointerdown', () => state.pitchInput = -1);
  document.getElementById('btn-roll-left').addEventListener('pointerdown', () => state.rollInput = -1);
  document.getElementById('btn-roll-right').addEventListener('pointerdown', () => state.rollInput = 1);
  window.addEventListener('pointerup', () => { state.pitchInput = 0; state.rollInput = 0; });

  // --- المساعد الذكي (لبناء وتعديل الطائرة) ---
  const aiInput = document.getElementById('ai-input');
  const aiBtn = document.getElementById('ai-btn');
  const aiResult = document.getElementById('ai-result');

  aiBtn.addEventListener('click', () => {
    const prompt = aiInput.value.trim();
    if (!prompt) return;
    
    aiResult.style.display = 'block';
    aiResult.innerText = 'جاري تحليل الطلب...';
    
    if (window.Android && window.Android.askAi) {
      let sysPrompt = `أنت مهندس طيران ومصمم. المستخدم يطلب: "${prompt}". 
      يجب أن تختار قطع الطائرة المناسبة من الخيارات التالية:
      - fuselage: standard (عادي), fighter (مقاتلة سريعة), heavy (شحن ثقيل)
      - wings: standard (مستقيمة), delta (مثلثة للسرعة), biplane (مزدوجة للرفع)
      - engine: propeller (مروحة), jet (نفاث قوي), twin (مزدوج)
      - tail: standard (عادي), v-tail (ذيل V)
      
      أعد كود JavaScript فقط لتنفيذ التغيير، بهذا الشكل:
      document.getElementById('sel-fuselage').value = 'fighter';
      document.getElementById('sel-wings').value = 'delta';
      document.getElementById('sel-engine').value = 'jet';
      document.getElementById('sel-tail').value = 'standard';
      updatePlane();
      aiResult.innerText = 'تم تصنيع الطائرة!';
      
      أعد الكود فقط بدون أي كلام إضافي أو علامات markdown.`;
      window.Android.askAi('flight_builder', sysPrompt);
    } else {
      aiResult.innerText = 'Android bridge not available';
    }
  });

  window.onAiResult = function(id, ok, text) {
    if (id !== 'flight_builder') return;
    if (!ok) {
      aiResult.innerText = 'خطأ: ' + text;
      return;
    }
    let code = text.trim();
    if (code.startsWith('```')) code = code.replace(/^```[a-z]*\n/, '').replace(/\n```$/, '');
    
    try {
      // تنفيذ كود الذكاء الاصطناعي لبناء الطائرة
      eval(code);
      aiResult.innerText = 'تم تصميم الطائرة بنجاح!';
    } catch (e) {
      aiResult.innerText = 'خطأ في التنفيذ: ' + e.message;
    }
  };

  // --- دورة المحاكاة ---
  function animate() {
    requestAnimationFrame(animate);

    // الفيزياء بناءً على خصائص الطائرة المختارة
    const targetSpeed = state.throttle * specs.speedMax;
    state.speed += (targetSpeed - state.speed) * 0.02;

    state.pitch += state.pitchInput * 0.5 * specs.agility;
    state.roll += state.rollInput * 0.5 * specs.agility;

    if (state.pitchInput === 0) state.pitch *= 0.95;
    if (state.rollInput === 0) state.roll *= 0.95;

    state.pitch = Math.max(-45, Math.min(45, state.pitch));
    state.roll = Math.max(-60, Math.min(60, state.roll));

    planeGroup.rotation.x = state.pitch * Math.PI / 180;
    planeGroup.rotation.z = state.roll * Math.PI / 180;

    const moveSpeed = state.speed * 0.05;
    planeGroup.translateZ(moveSpeed);

    // الرفع يتأثر بخصائص الجناح
    state.altitude += Math.sin(state.pitch * Math.PI / 180) * moveSpeed * specs.lift;
    if (state.altitude < 0) {
        state.altitude = 0;
        state.pitch = 0;
        state.speed *= 0.5;
    }

    // تتبع الكاميرا
    const camOffset = new THREE.Vector3(0, 5, -15);
    camOffset.applyQuaternion(planeGroup.quaternion);
    camera.position.lerp(planeGroup.position.clone().add(camOffset), 0.1);
    camera.lookAt(planeGroup.position);

    // HUD
    document.getElementById('hud-speed').innerText = Math.round(state.speed);
    document.getElementById('hud-alt').innerText = Math.round(state.altitude * 10);

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
            f'{indent}    text = {{ Text(state.language.tr("محاكي ومصمم الطيران", "Flight Sim & Builder")) }},\n'
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
        print(">> Inserted Flight Simulator menu item dynamically.")
    else:
        raise RuntimeError("Could not find DropdownMenuItem to insert Flight Simulator.")

print(">> Flight Simulator + Builder Patch applied successfully!")
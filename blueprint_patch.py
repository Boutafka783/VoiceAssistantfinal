import os
import re

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
MANIFEST = "app/src/main/AndroidManifest.xml"

def replace_once(file_path, old, new, silent_if_exists=False, required=True):
    """Replace exactly one occurrence of `old`. Fails loudly instead of silently skipping.

    - silent_if_exists: if `new` is already in the file, do nothing (idempotent re-runs).
    - required: raise if the anchor is missing; with required=False a missing anchor returns False.
    - An anchor that appears more than once always raises (ambiguous).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if silent_if_exists and new in content:
        return True
    count = content.count(old)
    if count == 0:
        if required:
            raise RuntimeError(f"Anchor not found in {file_path}: {old!r}")
        return False
    if count > 1:
        raise RuntimeError(f"Anchor appears {count} times in {file_path}: {old!r}")
    content = content.replace(old, new, 1)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return True


def register_activity(name):
    """Register .<name> in AndroidManifest.xml (skips if already declared; raises if </application> is missing/ambiguous)."""
    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest = f.read()
    if re.search(r'android:name\s*=\s*"(?:com\.zevorix\.assistant)?\.?' + re.escape(name) + r'"', manifest):
        print(f">> {name} already declared in manifest - skipping")
        return
    block = (
        f'    <!-- {name} -->\n'
        f'    <activity\n'
        f'        android:name=".{name}"\n'
        f'        android:exported="false"\n'
        f'        android:hardwareAccelerated="true"\n'
        f'        android:configChanges="orientation|screenSize|keyboardHidden|screenLayout|smallestScreenSize|uiMode"\n'
        f'        android:theme="@style/Theme.VoiceAssistant" />\n\n'
        f'</application>'
    )
    replace_once(MANIFEST, "</application>", block, silent_if_exists=True, required=True)
    print(f">> Registered {name} in AndroidManifest.xml")

print(">> Applying Advanced Flight Simulator & Build Guide Patch...")

# 1) إنشاء ملف flight_sim.html
# (نفس الكود السابق، لا تغيير عليه) ... 
html_content = r'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>مختبر هندسة الطيران</title><script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script><style>:root { --bg: #0a0f18; --panel: rgba(13, 21, 34, 0.95); --border: rgba(53, 208, 255, 0.4); --text: #e8edf5; --accent: #35d0ff; --btn-bg: #ff9f1c; --btn-text: #1a1100; --warn: #ff4444; --good: #00ff88; } * { box-sizing: border-box; } body, html { margin: 0; height: 100%; background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; overflow: hidden; } #app { display: flex; flex-direction: column; height: 100vh; position: relative; } #canvas-container { position: absolute; inset: 0; z-index: 1; } #hud { position: absolute; top: 10px; right: 10px; z-index: 2; background: var(--panel); border: 1px solid var(--border); padding: 8px 12px; border-radius: 8px; font-family: monospace; font-size: 0.85rem; text-align: right; pointer-events: none; line-height: 1.4; } #hud .val { color: var(--accent); font-weight: bold; } #hud .warn { color: var(--warn); font-weight: bold; } #hud .good { color: var(--good); font-weight: bold; } #builder-panel { position: absolute; top: 10px; left: 10px; z-index: 2; background: var(--panel); border: 1px solid var(--border); padding: 8px; border-radius: 8px; display: flex; flex-direction: column; gap: 6px; width: 190px; max-height: 80vh; overflow-y: auto; } .builder-row { display: flex; flex-direction: column; gap: 2px; } .builder-row label { font-size: 0.75rem; color: #aaa; } .builder-row select { padding: 4px; border-radius: 4px; border: 1px solid var(--border); background: #060a12; color: #fff; outline: none; font-size: 0.8rem; } #ai-panel { position: absolute; bottom: 90px; left: 10px; z-index: 2; width: 250px; display: flex; flex-direction: column; gap: 6px; } #ai-input { width: 100%; padding: 8px; border-radius: 6px; border: 1px solid var(--border); background: var(--panel); color: var(--text); outline: none; font-size: 0.85rem; } #ai-btn { padding: 8px; background: var(--accent); color: #000; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.9rem; } #ai-result { font-size: 0.75rem; color: #ff9f1c; background: var(--panel); padding: 6px; border-radius: 6px; display: none; border: 1px solid #ff9f1c; line-height: 1.3; } #build-guide-modal { position: absolute; inset: 0; background: rgba(0,0,0,0.8); z-index: 100; display: none; justify-content: center; align-items: center; padding: 20px; backdrop-filter: blur(4px); } #build-guide-content { background: var(--panel); border: 2px solid var(--accent); border-radius: 12px; padding: 20px; max-width: 500px; width: 100%; max-height: 80vh; overflow-y: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); } #build-guide-content h2 { margin-top: 0; color: var(--accent); text-align: center; border-bottom: 1px solid #333; padding-bottom: 10px; } #build-guide-content p { line-height: 1.6; font-size: 0.95rem; color: #ccc; } #build-guide-content ol { line-height: 1.8; font-size: 0.95rem; color: #e8edf5; padding-right: 20px; } #build-guide-content li { margin-bottom: 8px; border-bottom: 1px dashed #333; padding-bottom: 8px; } #close-guide { width: 100%; padding: 12px; background: var(--accent); color: #000; border: none; border-radius: 8px; font-weight: bold; font-size: 1rem; margin-top: 15px; cursor: pointer; } #controls { position: absolute; bottom: 15px; left: 15px; right: 15px; z-index: 2; display: flex; justify-content: space-between; pointer-events: none; } .control-group { display: flex; gap: 8px; pointer-events: auto; } .btn-ctrl { width: 50px; height: 50px; border-radius: 50%; border: 2px solid var(--border); background: var(--panel); color: var(--text); font-size: 1.2rem; display: flex; justify-content: center; align-items: center; cursor: pointer; } #throttle-group { flex-direction: column; align-items: flex-end; } #throttle-bar { width: 15px; height: 100px; background: var(--panel); border: 2px solid var(--border); border-radius: 8px; position: relative; overflow: hidden; } #throttle-fill { position: absolute; bottom: 0; left: 0; right: 0; background: var(--accent); transition: height 0.1s; } #throttle-text { margin-top: 4px; font-family: monospace; font-size: 0.9rem; }</style></head><body><div id="app"><div id="canvas-container"></div><div id="hud">السرعة: <span class="val" id="hud-speed">0</span> km/h<br>الارتفاع: <span class="val" id="hud-alt">0</span> m<br><hr style="border-color:#333; margin:4px 0;">الوزن: <span class="val" id="hud-weight">0</span> g<br>الدفع: <span class="val" id="hud-thrust">0</span> g<br>TWR: <span id="hud-twr">0</span><br>البطارية: <span class="val" id="hud-bat">100</span>%<br>الطيران: <span class="val" id="hud-time">0</span> دقيقة<br>المدى: <span class="val" id="hud-range">0</span> كم</div><div id="builder-panel"><div class="builder-row"><label>الهيكل</label><select id="sel-fuselage" onchange="updatePlane()"><option value="standard">طائرة عادية (400g)</option><option value="drone">درون (300g)</option><option value="heavy">شحن ثقيل (1200g)</option></select></div><div class="builder-row"><label>البطارية</label><select id="sel-battery" onchange="updatePlane()"><option value="3s">3S 1500mAh (130g)</option><option value="4s">4S 2200mAh (250g)</option><option value="6s">6S 5000mAh (650g)</option></select></div><div class="builder-row"><label>المحرك</label><select id="sel-engine" onchange="updatePlane()"><option value="small">صغير (200g دفع - 30g)</option><option value="medium">متوسط (800g دفع - 60g)</option><option value="large">كبير (2000g دفع - 120g)</option></select></div><div class="builder-row"><label>المروحة</label><select id="sel-prop" onchange="updatePlane()"><option value="small">صغيرة (كفاءة عالية - 10g)</option><option value="large">كبيرة (دفع أعلى - 25g)</option></select></div><div class="builder-row"><label>التحكم</label><select id="sel-rc" onchange="updatePlane()"><option value="24g">2.4GHz (مدى 1كم)</option><option value="58g">5.8GHz (مدى 3كم)</option><option value="4g">4G/WiFi (مدى لامحدود)</option></select></div></div><div id="ai-panel"><input type="text" id="ai-input" placeholder="مثال: اريد طائرة للمبتدئين..." /><button id="ai-btn">✨ معلم ومهندس الطيران AI</button><div id="ai-result"></div></div><div id="build-guide-modal"><div id="build-guide-content"><h2>📘 دليل تصنيع الطائرة</h2><p id="guide-explanation">جاري التحضير...</p><h3 style="color:var(--accent); font-size:1.1rem;">خطوات التصنيع الحقيقية:</h3><ol id="guide-steps"></ol><button id="close-guide" onclick="document.getElementById('build-guide-modal').style.display='none'">فهمت!</button></div></div><div id="controls"><div class="control-group"><div class="btn-ctrl" id="btn-pitch-down">⬇️</div><div class="btn-ctrl" id="btn-pitch-up">⬆️</div></div><div class="control-group" id="throttle-group"><div id="throttle-bar"><div id="throttle-fill" style="height: 0%;"></div></div><div id="throttle-text">0%</div></div><div class="control-group"><div class="btn-ctrl" id="btn-roll-left">⬅️</div><div class="btn-ctrl" id="btn-roll-right">➡️</div></div></div></div><script>const container=document.getElementById('canvas-container'),scene=new THREE.Scene();scene.background=new THREE.Color(0x87CEEB);scene.fog=new THREE.Fog(0x87CEEB,100,1000);const camera=new THREE.PerspectiveCamera(75,window.innerWidth/window.innerHeight,0.1,2000),renderer=new THREE.WebGLRenderer({antialias:!0});renderer.setSize(window.innerWidth,window.innerHeight),container.appendChild(renderer.domElement),scene.add(new THREE.AmbientLight(0xffffff,.6));const dirLight=new THREE.DirectionalLight(0xffffff,.8);dirLight.position.set(100,200,50),scene.add(dirLight);const gridHelper=new THREE.GridHelper(2000,100,0,4473924);gridHelper.position.y=-10,scene.add(gridHelper);let planeGroup=new THREE.Group;scene.add(planeGroup);let specs={mass:0,maxThrust:0,batteryMah:0,ampDrawMax:0,rcRangeKm:0};function updatePlane(){const e=document.getElementById('sel-fuselage').value,t=document.getElementById('sel-battery').value,n=document.getElementById('sel-engine').value,a=document.getElementById('sel-prop').value,o=document.getElementById('sel-rc').value;for(;planeGroup.children.length>0;)planeGroup.remove(planeGroup.children[0]);let s=new THREE.MeshStandardMaterial({color:13224374}),r;r="drone"===e?new THREE.BoxGeometry(2,.5,2):"heavy"===e?new THREE.CylinderGeometry(1.2,1.2,8,8):new THREE.CylinderGeometry(.5,.5,6,8),"drone"!==e&&r.rotateX(Math.PI/2),"drone"===e&&s.color.setHex(3355443),"heavy"===e&&s.color.setHex(8421504),planeGroup.add(new THREE.Mesh(r,s));const c=new THREE.BoxGeometry("drone"===e?6:8,.2,1.5),l=new THREE.MeshStandardMaterial({color:15658734});if(planeGroup.add(new THREE.Mesh(c,l)),"drone"!==e){const e=new THREE.Mesh(new THREE.BoxGeometry(2,.2,.8),l);e.position.set(0,.5,-2.5),planeGroup.add(e)}let d=0,u=0,m=0,i=0;d+="drone"===e?300:"heavy"===e?1200:400,"3s"===t?(d+=130,m=1500):"4s"===t?(d+=250,m=2200):(d+=650,m=5000),"small"===n?(d+=30,u+=200,i=10):"medium"===n?(d+=60,u+=800,i=25):(d+=120,u+=2e3,i=50),"small"===a?(d+=10,u*=.8,i*=.7):(d+=25,u*=1.2,i*=1.3);let p="24g"===o?1:"58g"===o?3:999;specs={mass:d,maxThrust:u,batteryMah:m,ampDrawMax:i,rcRangeKm:p},document.getElementById('hud-weight').innerText=d,document.getElementById('hud-thrust').innerText=u;let g=u/d,b=document.getElementById('hud-twr');b.innerText=g.toFixed(2),g<1?(b.className="warn",b.innerText+=" (لا يطير!)"):g>2?(b.className="good",b.innerText+=" (قوي جداً)"):b.className="val",document.getElementById('hud-range').innerText=999===p?"∞":p,state.throttle=0,document.getElementById('throttle-fill').style.height="0%",document.getElementById('throttle-text').innerText="0%",state.battery=100}updatePlane(),planeGroup.position.set(0,0,0);let state={speed:0,throttle:0,pitch:0,roll:0,altitude:0,pitchInput:0,rollInput:0,battery:100};document.getElementById('btn-pitch-up').addEventListener('pointerdown',()=>state.pitchInput=1),document.getElementById('btn-pitch-down').addEventListener('pointerdown',()=>state.pitchInput=-1),document.getElementById('btn-roll-left').addEventListener('pointerdown',()=>state.rollInput=-1),document.getElementById('btn-roll-right').addEventListener('pointerdown',()=>state.rollInput=1),window.addEventListener('pointerup',()=>{state.pitchInput=0,state.rollInput=0});const aiBtn=document.getElementById('ai-btn'),aiResult=document.getElementById('ai-result');aiBtn.addEventListener('click',()=>{const e=document.getElementById('ai-input').value.trim();if(!e)return;aiResult.style.display='block',aiResult.innerText='جاري التصميم وكتابة دليل التصنيع...';if(window.Android&&window.Android.askAi){let t=`أنت مهندس طيران ومعلم للمبتدئين. المستخدم يطلب: "${e}". عليك اختيار أفضل قطع للطائرة، وشرح لماذا اخترتها، وكتابة خطوات تصنيع حقيقية. الخيارات: - fuselage: 'standard', 'drone', 'heavy' - battery: '3s', '4s', '6s' - engine: 'small', 'medium', 'large' - prop: 'small', 'large' - rc: '24g', '58g', '4g' أعد النتيجة بصيغة JSON فقط (بدون أي markdown أو كلام إضافي) بهذا الشكل: { "parts": { "fuselage": "drone", "battery": "4s", "engine": "medium", "prop": "large", "rc": "58g" }, "explanation": "شرح بسيط جداً للمبتدئ لماذا هذه القطع مناسبة (سطرين).", "steps": [ "الخطوة 1: قم بتثبيت المحرك على الهيكل...", "الخطوة 2: قم بتوصيل البطارية...", "الخطوة 3: ثبت المروحة...", "الخطوة 4: اربط مستقبل التحكم..." ] }`;window.Android.askAi('flight_engineer',t)}}),window.onAiResult=function(e,t,n){if('flight_engineer'===e){if(!t)return void(aiResult.innerText='خطأ: '+n);let a=n.trim();a.startsWith('```json')&&(a=a.replace(/^```json\n/,'').replace(/\n```$/,''));try{const e=JSON.parse(a);e.parts&&(document.getElementById('sel-fuselage').value=e.parts.fuselage||'standard',document.getElementById('sel-battery').value=e.parts.battery||'3s',document.getElementById('sel-engine').value=e.parts.engine||'small',document.getElementById('sel-prop').value=e.parts.prop||'small',document.getElementById('sel-rc').value=e.parts.rc||'24g',updatePlane()),document.getElementById('guide-explanation').innerText=e.explanation||'';const t=document.getElementById('guide-steps');t.innerHTML='',e.steps&&Array.isArray(e.steps)&&e.steps.forEach(e=>{const n=document.createElement('li');n.innerText=e,t.appendChild(n)}),document.getElementById('build-guide-modal').style.display='flex',aiResult.innerText='تم تجهيز الطائرة ودليل التصنيع!'}catch(e){aiResult.innerText='حدث خطأ، تم تطبيق إعدادات افتراضية.',document.getElementById('guide-explanation').innerText='تم اختيار قطع متوازنة لتناسب المبتدئين.',document.getElementById('guide-steps').innerHTML='<li>ثبت المحرك في مقدمة الهيكل.</li><li>صل البطارية بمتحكم السرعة (ESC).</li><li>اربط المروحة بالمحرك.</li><li>صل أسلاك التحكم عن بعد.</li>',document.getElementById('build-guide-modal').style.display='flex'}}};let lastTime=performance.now();function animate(){requestAnimationFrame(animate);let e=(performance.now()-lastTime)/1e3;lastTime=performance.now(),e>.1&&(e=.1);let t=specs.maxThrust*state.throttle;state.battery<=0&&(state.throttle=0,t=0);const n=.05*state.speed*state.speed,a=(t-n)/specs.mass;state.speed+=a*e*.1,state.speed<0&&(state.speed=0);const o=.01*state.speed*state.speed,s=specs.mass*.0098;let r=o>s?(o-s)*.01:(o-s)*.05;state.altitude+=r*e,state.altitude<0&&(state.altitude=0,state.speed*=.9),state.throttle>0&&(state.battery-=(specs.ampDrawMax*state.throttle/specs.batteryMah*100/60)*e*10,state.battery<0&&(state.battery=0)),state.pitch+=45*state.pitchInput*e,state.roll+=90*state.rollInput*e,0===state.pitchInput&&(state.pitch*=.9),0===state.rollInput&&(state.roll*=.9),state.pitch=Math.max(-45,Math.min(45,state.pitch)),state.roll=Math.max(-60,Math.min(60,state.roll)),planeGroup.rotation.x=state.pitch*Math.PI/180,planeGroup.rotation.z=state.roll*Math.PI/180,planeGroup.translateZ(state.speed*e*.5),document.getElementById('hud-speed').innerText=Math.round(3.6*state.speed),document.getElementById('hud-alt').innerText=Math.round(state.altitude),document.getElementById('hud-bat').innerText=Math.round(state.battery),state.throttle>.1?(document.getElementById('hud-time').innerText=(specs.batteryMah*(state.battery/100)/1e3/specs.ampDrawMax/state.throttle*60).toFixed(1)):document.getElementById('hud-time').innerText='0';const c=new THREE.Vector3(0,5,-15);c.applyQuaternion(planeGroup.quaternion),camera.position.lerp(planeGroup.position.clone().add(c),.1),camera.lookAt(planeGroup.position),renderer.render(scene,camera)}window.addEventListener('resize',()=>{camera.aspect=window.innerWidth/window.innerHeight,camera.updateProjectionMatrix(),renderer.setSize(window.innerWidth,window.innerHeight)}),animate();</script></body></html>'''

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
                                addJavascriptInterface(Bridge(this, aiService), "Android")
                                loadUrl("file:///android_asset/flight_sim.html")
                            }
                        }
                    )
                }
            }
        }
    }
    
    class Bridge(private val webView: WebView, private val aiService: AiChatService) {
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
register_activity("FlightSimActivity")

# 4) القائمة الجانبية: لا يتم تعديل MainScreen.kt هنا.
#    menu_items_patch.py هو المصدر الوحيد لإدراج عنصر القائمة (بأسماء كاملة، دون الحاجة لأي import).

print(">> Aerospace Lab Patch applied (activity + html + manifest). Menu item: menu_items_patch.py")
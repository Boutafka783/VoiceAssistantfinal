import os
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

PKG_DIR = "app/src/main/java/com/zevorix/assistant"
ASSETS_DIR = "app/src/main/assets"

# مفتاح التشفير (32 حرفاً = AES-256)
SECRET_KEY = b"ZevorixSuperSecretKey1234567890!"
cipher = AES.new(SECRET_KEY, AES.MODE_ECB)

def encrypt_file(path):
    if not os.path.exists(path):
        return False
    with open(path, "rb") as f:
        data = f.read()
    # إذا كان الملف مشفراً مسبقاً، لا تعيد تشفيره
    if data.startswith(b"ENC:"):
        return False
    
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    with open(path, "wb") as f:
        f.write(b"ENC:" + encrypted_data)
    return True

def patch_activity(filename, html_name):
    path = os.path.join(PKG_DIR, filename)
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    if "decryptAsset(" in code:
        return # تم التطبيق مسبقاً

    # 1. حقن دالة فك التشفير داخل الكلاس
    decrypt_func = """
    private fun decryptAsset(assetName: String): String {
        return try {
            val inputStream = assets.open(assetName)
            val bytes = inputStream.readBytes()
            inputStream.close()
            val actualBytes = if (bytes.size > 4 && String(bytes, 0, 4) == "ENC:") bytes.copyOfRange(4, bytes.size) else bytes
            val cipher = javax.crypto.Cipher.getInstance("AES/ECB/PKCS5Padding")
            val keySpec = javax.crypto.spec.SecretKeySpec("ZevorixSuperSecretKey1234567890!".toByteArray(), "AES")
            cipher.init(javax.crypto.Cipher.DECRYPT_MODE, keySpec)
            String(cipher.doFinal(actualBytes), Charsets.UTF_8)
        } catch (e: Exception) {
            android.util.Log.e("ZevorixDecrypt", "Failed to decrypt: $assetName", e)
            "Error loading secure content."
        }
    }
"""
    # إضافة الدالة بعد super.onCreate
    code = re.sub(r'(super\.onCreate\(savedInstanceState\))', r'\1\n' + decrypt_func, code, count=1)

    # 2. استبدال loadUrl بدالة فك التشفير وعرضها
    old_load = f'webView.loadUrl("file:///android_asset/{html_name}")'
    new_load = f'webView.loadDataWithBaseURL("file:///android_asset/", decryptAsset("{html_name}"), "text/html", "UTF-8", null)'
    
    if old_load in code:
        code = code.replace(old_load, new_load)
    else:
        # محاولة البحث بصيغة أخرى
        code = re.sub(
            rf'webView\.loadUrl\("file:///android_asset/{html_name}"\)',
            new_load,
            code
        )

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print(f">> Patched {filename} to decrypt {html_name} at runtime")

print(">> Applying WebView Encryption Patch...")

# تشفير الملفات وتعديل الأنشطة المرتبطة بها
targets = [
    ("architecture_lab.html", "ArchitectureActivity.kt"),
    ("flight_sim.html", "FlightSimActivity.kt")
]

for html, activity in targets:
    html_path = os.path.join(ASSETS_DIR, html)
    if encrypt_file(html_path):
        print(f">> Encrypted {html}")
    else:
        print(f"== {html} is already encrypted or not found")
    
    patch_activity(activity, html)

print(">> WebView Encryption applied successfully!")
import re
import sys

MANIFEST = "app/src/main/AndroidManifest.xml"
NAME = "ArchitectureActivity"

with open(MANIFEST, "r", encoding="utf-8") as f:
    m = f.read()

# declared = a real <activity ... android:name="...ArchitectureActivity"> (comments are ignored)
body = re.sub(r"<!--.*?-->", "", m, flags=re.S)
declared = re.search(r'<activity\b[^>]*android:name\s*=\s*"[^"]*\b' + NAME + r'"', body, re.S)

if declared:
    print(">> %s already declared in manifest" % NAME)
else:
    block = (
        '    <activity\n'
        '        android:name=".%s"\n'
        '        android:exported="false"\n'
        '        android:hardwareAccelerated="true"\n'
        '        android:configChanges="orientation|screenSize|keyboardHidden|screenLayout|smallestScreenSize|uiMode"\n'
        '        android:theme="@style/Theme.VoiceAssistant" />\n\n'
    ) % NAME
    idx = m.rfind("</application>")
    if idx < 0:
        # <application ... /> self-closing is not expected, fail loudly
        print("!! </application> not found in %s" % MANIFEST)
        sys.exit(1)
    m = m[:idx] + block + m[idx:]
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        f.write(m)
    print(">> Registered %s in manifest" % NAME)

with open(MANIFEST, "r", encoding="utf-8") as f:
    final = re.sub(r"<!--.*?-->", "", f.read(), flags=re.S)
if not re.search(r'<activity\b[^>]*android:name\s*=\s*"[^"]*\b' + NAME + r'"', final, re.S):
    print("!! VERIFY FAILED: %s still not in manifest" % NAME)
    sys.exit(1)
print(">> VERIFY OK: manifest=True")

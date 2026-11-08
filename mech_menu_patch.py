# يضيف زر "المختبر الميكانيكي" إلى قائمة الترس في MainScreen.kt
# يعتمد على عنصر "الذاكرة / Memory" الموجود دائماً (لا يحتاج عنصر الإلكترونيات)
import os, re, sys

main = None
for root, _, files in os.walk("app/src/main/java"):
    if "MainScreen.kt" in files:
        main = os.path.join(root, "MainScreen.kt")
        break
if not main:
    print("ERROR: MainScreen.kt not found"); sys.exit(1)

t = open(main, encoding="utf-8").read()
pkg = re.search(r"^package\s+([\w.]+)", t, re.M).group(1)
root_pkg = pkg[:-3] if pkg.endswith(".ui") else pkg

if "MechSimulatorActivity::class" in t:
    # الزر موجود (ربما من mech_patch) - تأكد فقط من الاستيراد
    fq = root_pkg + ".MechSimulatorActivity"
    if fq not in t:
        i = re.search(r"^import ", t, re.M).start()
        t = t[:i] + "import " + fq + "\n" + t[i:]
        open(main, "w", encoding="utf-8").write(t)
        print("+ added missing import", fq)
    else:
        print("= button already present")
    sys.exit(0)

item = '''DropdownMenuItem(
                                    text = { Text(state.language.tr("المختبر الميكانيكي", "Mechanical Lab")) },
                                    leadingIcon = { Icon(Icons.Filled.Build, contentDescription = null) },
                                    onClick = {
                                        showSettingsMenu = false
                                        context.startActivity(
                                            Intent(context, %s.MechSimulatorActivity::class.java)
                                        )
                                    }
                                )
                                ''' % root_pkg

# المرساة: عنصر الذاكرة، وإلا عنصر الحماية من السرقة
m = re.search(r'DropdownMenuItem\(\s*text = \{ Text\(state\.language\.tr\("الذاكرة"', t)
if not m:
    m = re.search(r'DropdownMenuItem\(\s*text = \{ Text\(state\.language\.tr\("محادثة جديدة"', t)
if not m:
    print("ERROR: anchor not found in MainScreen.kt"); sys.exit(1)

t = t[:m.start()] + item + t[m.start():]
imp = "import androidx.compose.material.icons.filled.Build\n"
if imp not in t:
    i = re.search(r"^import ", t, re.M).start()
    t = t[:i] + imp + t[i:]
open(main, "w", encoding="utf-8").write(t)
print("+ Mechanical Lab menu item added to", main)

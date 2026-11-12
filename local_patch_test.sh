#!/usr/bin/env bash
# Local sanity test for the 4 patch scripts. Usage: bash local_patch_test.sh  (run next to the patch files; needs python3)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
P="$T/app/src/main/java/com/zevorix/assistant"
mkdir -p "$P/ui" "$T/app/src/main/assets"
cat > "$T/app/src/main/AndroidManifest.xml" <<'XML'
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:label="x">
        <activity android:name=".MainActivity" />
    </application>
</manifest>
XML
# Synthetic MainScreen.kt with traps: ')' inside strings/comments/raw strings, another fun that already has `context`
cat > "$P/ui/MainScreen.kt" <<'KT'
package com.zevorix.assistant.ui

@Composable
fun Other() {
    val context = LocalContext.current   // NOT the menu's scope
}

@Composable
fun MainScreen(viewModel: MainViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    var showSettingsMenu by remember { mutableStateOf(false) }
    DropdownMenu(
        expanded = showSettingsMenu,
        onDismissRequest = { showSettingsMenu = false }
    ) {
        DropdownMenuItem(text = { Text(state.language.tr("فحص", "Scan apps")) }, onClick = {})
        DropdownMenuItem(
            text = { Text(state.language.tr("روبوت", "Robot Lab")) }, // tricky ) comment
            onClick = {
                /* block ) comment */
                val raw = """ a ) b " c """
                val t = "x ) ${foo("y)")} z"
                val ch = ')'
                showSettingsMenu = false
            }
        )
        DropdownMenuItem(text = { Text("Bluetooth") }, onClick = {})
    }
}
KT
cd "$T"
run() { python3 "$HERE/$1"; }
echo "== 1. blueprint / architecture"; run blueprint_patch.py >/dev/null; run architecture_patch.py >/dev/null
for a in FlightSimActivity ArchitectureActivity; do
  test -f "$P/$a.kt" || { echo "FAIL: $a.kt missing"; exit 1; }
  test "$(grep -c "android:name=\".$a\"" app/src/main/AndroidManifest.xml)" = 1 || { echo "FAIL: manifest $a"; exit 1; }
done
grep -q 'hardwareAccelerated="true"' app/src/main/AndroidManifest.xml || { echo "FAIL: hardwareAccelerated"; exit 1; }
cp "$P/ui/MainScreen.kt" /tmp/_ms_before.kt
cmp -s "$P/ui/MainScreen.kt" /tmp/_ms_before.kt   # patches 1+2 must NOT touch MainScreen.kt
echo "== 2. menu_items (run twice = idempotent)"; run menu_items_patch.py; run menu_items_patch.py >/dev/null
test "$(grep -c 'ArchitectureActivity::class.java' "$P/ui/MainScreen.kt")" = 1 || { echo "FAIL: duplicate/missing menu item"; exit 1; }
python3 - "$P/ui/MainScreen.kt" <<'PY'
import sys,re
s=open(sys.argv[1],encoding='utf-8').read()
main=s[s.index('fun MainScreen'):]
assert 'val context = androidx.compose.ui.platform.LocalContext.current' in main, 'context not injected in MainScreen'
assert s.count('val context =')==2, 'unexpected number of context vals'
assert s.index('Robot Lab') < s.index('Architecture Lab') < s.index('Bluetooth'), 'wrong order'
print('menu structure OK')
PY
echo "== 3. webview_fix (run twice)"; run webview_fix_patch.py; run webview_fix_patch.py >/dev/null
grep -q 'LAYER_TYPE_HARDWARE' "$P/ArchitectureActivity.kt"
grep -q 'Bridge(this, webView, aiService)' "$P/ArchitectureActivity.kt"
grep -q 'Bridge(webView, aiService)' "$P/FlightSimActivity.kt"
echo "== 4. must FAIL loudly"
# fresh manifest WITHOUT </application> and without the activity -> registration must raise, not skip silently
cat > app/src/main/AndroidManifest.xml <<'XML'
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:label="x">
</manifest>
XML
if python3 "$HERE/architecture_patch.py" >/dev/null 2>&1; then echo "FAIL: missing </application> not detected"; exit 1; else echo "OK: missing manifest anchor raises"; fi
sed -i 's/state\.language\.tr(/state.lang(/g' "$P/ui/MainScreen.kt"
if python3 "$HERE/menu_items_patch.py" >/dev/null 2>&1; then echo "FAIL: missing tr() not detected"; exit 1; else echo "OK: missing state.language.tr raises"; fi
echo "ALL PATCH TESTS PASSED"

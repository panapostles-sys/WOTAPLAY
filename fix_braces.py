import re

with open('app/src/main/java/com/wotaplayer/ui/screens/VideoListScreen.kt', encoding='utf-8') as f:
    content = f.read()

# Find the settings overlay section
start = content.find('    }   // closes Scaffold content lambda')
end = content.find('    }   // closes backdrop Box(layerBackdrop)')

if start < 0 or end < 0:
    print(f"Markers not found: start={start}, end={end}")
    # Debug: find similar markers
    for m in ['Matched/empty', 'closes backdrop Box', 'Scaffold content']:
        idx = content.find(m)
        if idx >= 0:
            print(f"  '{m}' found at {idx}")
    exit(1)

end_line = content.find('\n', end) + 1
block = content[start:end_line]
print(f"Block length: {len(block)}")

# Replace the block - just remove the extra closing braces that are at wrong indent
# The structure should be:
#   }   // closes Scaffold content lambda
#
#   // Settings glass overlay
#   if (...) {
#       ...
#   }   // closes backdrop Box(layerBackdrop)
#
# Then the rest of the function continues

new = """    }   // closes Scaffold content lambda

    // ── Settings glass overlay (inside same coordinate space as layerBackdrop) ──
    if (showSettings && listBackdrop != null && Build.VERSION.SDK_INT >= 31) {
        val surfaceBg = MaterialTheme.colorScheme.surface
        Box(modifier = Modifier.fillMaxSize()) {
            Box(modifier = Modifier.fillMaxSize().clickable(onClick = { showSettings = false }))
            Box(
                modifier = Modifier
                    .align(Alignment.TopEnd).padding(top = 48.dp, end = 8.dp)
                    .width(200.dp).wrapContentHeight()
                    .drawBackdrop(
                        backdrop = listBackdrop,
                        shape = { RoundedCornerShape(12.dp) },
                        effects = {
                            blur(4f.dp.toPx())
                            if (android.os.Build.VERSION.SDK_INT >= 33)
                                lens(16f.dp.toPx(), 32f.dp.toPx())
                        },
                        onDrawSurface = { drawRect(surfaceBg.copy(alpha = 0.65f)) }
                    )
            ) {
                Column {
                    val autoResume by viewModel.autoResume.collectAsState()
                    SettingsMenuItem(
                        text = "自动续播",
                        trailing = {
                            Switch(checked = autoResume,
                                onCheckedChange = { viewModel.toggleAutoResume() },
                                colors = SwitchDefaults.colors(
                                    checkedTrackColor = MaterialTheme.colorScheme.primary,
                                    uncheckedTrackColor = MaterialTheme.colorScheme.surfaceVariant
                                )
                            )
                        }
                    )
                    HorizontalDivider(
                        modifier = Modifier.padding(horizontal = 16.dp),
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.12f)
                    )
                    val portraitMode by viewModel.portraitMode.collectAsState()
                    SettingsMenuItem(
                        text = "横/竖屏",
                        trailing = {
                            Switch(checked = portraitMode,
                                onCheckedChange = { viewModel.togglePortraitMode() },
                                colors = SwitchDefaults.colors(
                                    checkedTrackColor = MaterialTheme.colorScheme.primary,
                                    uncheckedTrackColor = MaterialTheme.colorScheme.surfaceVariant
                                )
                            )
                        }
                    )
                    HorizontalDivider(
                        modifier = Modifier.padding(horizontal = 16.dp),
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.12f)
                    )
                    val doubleTapSeekMs by viewModel.doubleTapSeekMs.collectAsState()
                    val seekLabel = when (doubleTapSeekMs) {
                        500 -> "0.5s"; 1000 -> "1s"; 2000 -> "2s"; 3000 -> "3s"; 5000 -> "5s"
                        else -> "${doubleTapSeekMs / 1000}s"
                    }
                    SettingsMenuItem(
                        text = "双击快进/快退",
                        trailing = { Text(seekLabel, fontSize = 14.sp, fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary) },
                        onClick = {
                            val next = when (doubleTapSeekMs) {
                                500 -> 1000; 1000 -> 2000; 2000 -> 3000; 3000 -> 5000; else -> 500
                            }
                            viewModel.setDoubleTapSeekMs(next)
                        }
                    )
                    HorizontalDivider(
                        modifier = Modifier.padding(horizontal = 16.dp),
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.12f)
                    )
                    val themeMode by viewModel.themeMode.collectAsState()
                    val themeLabel = when (themeMode) {
                        com.wotaplayer.ui.theme.ThemeMode.DARK -> "深色"
                        com.wotaplayer.ui.theme.ThemeMode.LIGHT -> "浅色"
                        com.wotaplayer.ui.theme.ThemeMode.SYSTEM -> "跟随系统"
                    }
                    SettingsMenuItem(
                        text = "主题",
                        trailing = { Text(themeLabel, fontSize = 14.sp, fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary) },
                        onClick = {
                            val next = when (themeMode) {
                                com.wotaplayer.ui.theme.ThemeMode.DARK -> com.wotaplayer.ui.theme.ThemeMode.LIGHT
                                com.wotaplayer.ui.theme.ThemeMode.LIGHT -> com.wotaplayer.ui.theme.ThemeMode.SYSTEM
                                com.wotaplayer.ui.theme.ThemeMode.SYSTEM -> com.wotaplayer.ui.theme.ThemeMode.DARK
                            }
                            viewModel.setThemeMode(next)
                        }
                    )
                }
            }
        }
    }
}   // closes backdrop Box(layerBackdrop)"""

new_content = content[:start] + new + content[end_line:]
with open('app/src/main/java/com/wotaplayer/ui/screens/VideoListScreen.kt', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
import re
clean = re.sub(r'//.*', '', new_content)
clean = re.sub(r'\".*?\"', '', clean, flags=re.DOTALL)
ob = clean.count('{')
cb = clean.count('}')
print(f"Balance: {ob - cb}")
print("Done")

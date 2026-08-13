import re

with open('app/src/main/java/com/wotaplayer/ui/screens/VideoListScreen.kt', encoding='utf-8') as f:
    lines = f.readlines()

# Track depth by counting braces, but filter out string contents
depth = 0
started = False
key_points = {
    78: 'function open',
    178: 'backdrop Box {',
    180: 'topBar {',
    221: 'topBar }',
    222: 'scaffold content {',
    449: 'if/else close',
    450: 'outer Box close',
    451: 'scaffold content close',
    454: 'settings if {',
    550: 'settings if }',
    551: 'line 551',
    552: 'line 552',
}

for i, line in enumerate(lines):
    stripped = line.rstrip()
    if 'fun VideoListScreen(' in stripped:
        started = True
    if not started:
        continue
    for ch in stripped:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
    if (i+1) in key_points:
        print(f'  after line {i+1:3d} ({key_points[i+1]:26s}): d={depth:2d}')
    if i+1 >= 550 and i+1 <= 652:
        print(f'  line {i+1:3d}: d after = {depth:2d} | {stripped[:80]}')
    if depth <= 0 and i > 550 and i < 650:
        print(f'  *** depth 0 at {i+1}')

print(f'\nFinal: depth={depth}')

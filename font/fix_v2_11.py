#!/usr/bin/env python3
import fontforge, os

font = fontforge.open('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')

# U+0346 꺽쇠를 현재 대비 1.25배 확대
# 기존(v2.10) arm≈69, depth≈62, t≈23 → 1.25배
arm, depth, t = 86, 78, 29
cx, cy = 250, 860

g = font[0x0346]
g.clear()
pen = g.glyphPen()
pen.moveTo((cx + depth, cy + arm))
pen.lineTo((cx - depth, cy))
pen.lineTo((cx + depth, cy - arm))
pen.lineTo((cx + depth, cy - arm + t))
pen.lineTo((cx - depth + t*2, cy))
pen.lineTo((cx + depth, cy + arm - t))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = 'mark'

font.fontname = 'PaliHangulV211'
font.familyname = 'PaliHangul V211'
font.fullname = 'PaliHangul V2.11'
font.version = '2.11'

font.save('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')
for f in os.listdir(os.path.expanduser('~/Library/Fonts')):
    if f.startswith('PaliHangul'):
        os.remove(os.path.expanduser(f'~/Library/Fonts/{f}'))
font.generate(os.path.expanduser('~/Library/Fonts/PaliHangulV211.otf'))
font.close()
print('✅ v2.11 완료 (U+0346 1.25배 확대)')

#!/usr/bin/env python3
import fontforge, os

font = fontforge.open('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')
k = 0.5522

# 아래빈원: -130 -> -120 (좀 더 위로)
g = font[0x0325]; g.clear(); pen = g.glyphPen()
cx, cy = 250, -120
r_out, r_in = 70, 48
pen.moveTo((cx-r_out, cy))
pen.curveTo((cx-r_out, cy+r_out*k), (cx-r_out*k, cy+r_out), (cx, cy+r_out))
pen.curveTo((cx+r_out*k, cy+r_out), (cx+r_out, cy+r_out*k), (cx+r_out, cy))
pen.curveTo((cx+r_out, cy-r_out*k), (cx+r_out*k, cy-r_out), (cx, cy-r_out))
pen.curveTo((cx-r_out*k, cy-r_out), (cx-r_out, cy-r_out*k), (cx-r_out, cy))
pen.closePath()
pen.moveTo((cx+r_in, cy))
pen.curveTo((cx+r_in, cy+r_in*k), (cx+r_in*k, cy+r_in), (cx, cy+r_in))
pen.curveTo((cx-r_in*k, cy+r_in), (cx-r_in, cy+r_in*k), (cx-r_in, cy))
pen.curveTo((cx-r_in, cy-r_in*k), (cx-r_in*k, cy-r_in), (cx, cy-r_in))
pen.curveTo((cx+r_in*k, cy-r_in), (cx+r_in, cy-r_in*k), (cx+r_in, cy))
pen.closePath(); pen = None
g.width = 0; g.glyphclass = 'mark'

# 쉼표(U+05C0): x -10
g = font[0x05C0]; g.clear(); pen = g.glyphPen()
pen.moveTo((210, -15)); pen.lineTo((240, -15)); pen.lineTo((240, 585)); pen.lineTo((210, 585)); pen.closePath(); pen=None
g.width = 470

# 마침표(U+2225): x -10
g = font[0x2225]; g.clear(); pen = g.glyphPen()
pen.moveTo((160, -15)); pen.lineTo((190, -15)); pen.lineTo((190, 585)); pen.lineTo((160, 585)); pen.closePath()
pen.moveTo((260, -15)); pen.lineTo((290, -15)); pen.lineTo((290, 585)); pen.lineTo((260, 585)); pen.closePath(); pen=None
g.width = 470

font.fontname = 'PaliHangulV210'
font.familyname = 'PaliHangul V210'
font.fullname = 'PaliHangul V2.10'
font.version = '2.10'

font.save('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')
for f in os.listdir(os.path.expanduser('~/Library/Fonts')):
    if f.startswith('PaliHangul'):
        os.remove(os.path.expanduser(f'~/Library/Fonts/{f}'))
font.generate(os.path.expanduser('~/Library/Fonts/PaliHangulV210.otf'))
font.close()
print('✅ v2.10 완료 (아래빈원 y=-120, 쉼표/마침표 x-10)')

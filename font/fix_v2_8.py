#!/usr/bin/env python3
import fontforge, os

font = fontforge.open('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')
k = 0.5522

# 1) U+0346 꺽쇠 1.25배 확대
g = font[0x0346]; g.clear(); pen = g.glyphPen()
cx, cy = 250, 860
arm, depth, t = 69, 62, 23
pen.moveTo((cx + depth, cy + arm))
pen.lineTo((cx - depth, cy))
pen.lineTo((cx + depth, cy - arm))
pen.lineTo((cx + depth, cy - arm + t))
pen.lineTo((cx - depth + t*2, cy))
pen.lineTo((cx + depth, cy + arm - t))
pen.closePath(); pen = None
g.width = 0; g.glyphclass = 'mark'

# 2) U+02BA 겹따옴표 1.25배 + x -10
g = font[0x02BA]; g.clear(); pen = g.glyphPen()
# left
pen.moveTo((52, 790)); pen.lineTo((80, 790)); pen.lineTo((65, 586)); pen.lineTo((37, 586)); pen.closePath()
# right
pen.moveTo((133, 790)); pen.lineTo((161, 790)); pen.lineTo((146, 586)); pen.lineTo((118, 586)); pen.closePath()
pen = None
g.width = 220

# 3) 빈원 10씩 더 붙임: 위 780->770, 아래 -150->-140
for uc, cy in [(0x030A, 770), (0x0325, -140)]:
    g = font[uc]; g.clear(); pen = g.glyphPen(); cx=250; r_out=70; r_in=48
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

# 5) 쉼표/마침표 y -15
# U+05C0
g = font[0x05C0]; g.clear(); pen = g.glyphPen()
pen.moveTo((220, -15)); pen.lineTo((250, -15)); pen.lineTo((250, 585)); pen.lineTo((220, 585)); pen.closePath(); pen=None
g.width = 470
# U+2225
g = font[0x2225]; g.clear(); pen = g.glyphPen()
pen.moveTo((170, -15)); pen.lineTo((200, -15)); pen.lineTo((200, 585)); pen.lineTo((170, 585)); pen.closePath()
pen.moveTo((270, -15)); pen.lineTo((300, -15)); pen.lineTo((300, 585)); pen.lineTo((270, 585)); pen.closePath(); pen=None
g.width = 470

font.fontname = 'PaliHangulV28'
font.familyname = 'PaliHangul V28'
font.fullname = 'PaliHangul V2.8'
font.version = '2.8'

font.save('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')
for f in os.listdir(os.path.expanduser('~/Library/Fonts')):
    if f.startswith('PaliHangul'):
        os.remove(os.path.expanduser(f'~/Library/Fonts/{f}'))
font.generate(os.path.expanduser('~/Library/Fonts/PaliHangulV28.otf'))
font.close()
print('✅ v2.8 완료')

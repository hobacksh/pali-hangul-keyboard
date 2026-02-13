#!/usr/bin/env python3
import fontforge, os

font = fontforge.open('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')

# 요청 반영:
# - 쉼표/마침표 크기 0.7배
# - 왼쪽으로 10 더 이동
# - 아래로 5 이동

# U+05C0 쉼표 (세로선)
g = font[0x05C0]
g.clear()
pen = g.glyphPen()
# 기존(대략): x 210~240, y -15~585
# 0.7배 + x-10 + y-5 적용 좌표
pen.moveTo((137, -16))
pen.lineTo((158, -16))
pen.lineTo((158, 405))
pen.lineTo((137, 405))
pen.closePath()
pen = None
g.width = 470

# U+2225 마침표 (이중 세로선)
g = font[0x2225]
g.clear()
pen = g.glyphPen()
# 좌측 막대
pen.moveTo((102, -16))
pen.lineTo((123, -16))
pen.lineTo((123, 405))
pen.lineTo((102, 405))
pen.closePath()
# 우측 막대
pen.moveTo((172, -16))
pen.lineTo((193, -16))
pen.lineTo((193, 405))
pen.lineTo((172, 405))
pen.closePath()
pen = None
g.width = 470

font.fontname = 'PaliHangulV212'
font.familyname = 'PaliHangul V212'
font.fullname = 'PaliHangul V2.12'
font.version = '2.12'

font.save('/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd')
for f in os.listdir(os.path.expanduser('~/Library/Fonts')):
    if f.startswith('PaliHangul'):
        os.remove(os.path.expanduser(f'~/Library/Fonts/{f}'))
font.generate(os.path.expanduser('~/Library/Fonts/PaliHangulV212.otf'))
font.close()
print('✅ v2.12 완료 (쉼표/마침표 0.7배, x-10 추가, y-5)')

#!/usr/bin/env python3
"""PaliHangul v2.79 — add U+02D1 (ˑ) only.

요구사항: "일단 02D1만 반영".
기존 v2.78f 결과물(모든 GSUB 유지)에 U+02D1 글리프만 추가.
"""

import os
import fontforge
import psMat

SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV278f.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV279.otf')
NANUM = os.path.expanduser('~/Library/Fonts/NanumMyeongjo-Regular.ttf')

CP_TARGET = 0x02D1   # ˑ MODIFIER LETTER HALF TRIANGULAR COLON
CP_REF = 0x25BF      # ▿ WHITE DOWN-POINTING SMALL TRIANGLE (shape reference)

font = fontforge.open(SRC)

# Ensure reference glyph exists in working font
if CP_REF not in font:
    n = fontforge.open(NANUM)
    n.selection.select(CP_REF)
    n.copy()
    font.selection.select(CP_REF)
    font.paste()
    n.close()

src = font[CP_REF]
sbb = src.boundingBox()
sx = (sbb[0] + sbb[2]) / 2.0
sy = (sbb[1] + sbb[3]) / 2.0
sh = sbb[3] - sbb[1]

# Modifier-size target (작고 읽히는 크기)
target_h = 280.0
scale = target_h / sh

# Position near x-height center
target_cx = 200.0
target_cy = 400.0

font.createChar(CP_TARGET, 'uni02D1')
g = font[CP_TARGET]
g.clear()

mat = psMat.compose(psMat.translate(-sx, -sy), psMat.scale(scale))
mat = psMat.compose(mat, psMat.translate(target_cx, target_cy))
g.addReference(src.glyphname, mat)
g.width = 396

font.fontname = 'PaliHangulV279'
font.familyname = 'PaliHangul V279'
font.fullname = 'PaliHangul V279'
font.version = '2.79'

font.generate(OUT)
font.close()

print('Generated:', OUT)
print('Size:', os.path.getsize(OUT))

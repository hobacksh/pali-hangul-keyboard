#!/usr/bin/env python3
"""
PaliHangul v2.6 - 빈원 위치 조정
윗빈원: y=880 → y=800
아래빈원: y=-250 → y=-170
"""

import fontforge, os

print("빈원 위치 조정")
font = fontforge.open("/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd")
print("  ✓ 로드 완료\n")

k = 0.5522
r_out, r_in = 70, 48

for uc, name, cy in [(0x030A, "윗빈원", 800), (0x0325, "아래빈원", -170)]:
    print(f"{name} (U+{uc:04X}) → y={cy}")
    g = font[uc]
    g.clear()
    pen = g.glyphPen()
    cx = 250
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
    pen.closePath()
    pen = None
    g.width = 0
    g.glyphclass = "mark"
    print("  ✓ 완성\n")

font.fontname = "PaliHangulV26"
font.familyname = "PaliHangul V26"
font.fullname = "PaliHangul V2.6"
font.version = "2.6"

font.save("/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd")
print("  ✓ SFD 저장")

for f in os.listdir(os.path.expanduser("~/Library/Fonts")):
    if f.startswith("PaliHangul"):
        os.remove(os.path.expanduser(f"~/Library/Fonts/{f}"))

font.generate(os.path.expanduser("~/Library/Fonts/PaliHangulV26.otf"))
print("  ✓ OTF 설치")
font.close()
print("\n✅ v2.6 완료!")

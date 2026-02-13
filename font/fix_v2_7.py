#!/usr/bin/env python3
"""윗빈원 y=800→780, 아래빈원 y=-170→-150"""
import fontforge, os

font = fontforge.open("/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd")
k = 0.5522
r_out, r_in = 70, 48

for uc, cy in [(0x030A, 780), (0x0325, -150)]:
    g = font[uc]; g.clear(); pen = g.glyphPen(); cx = 250
    pen.moveTo((cx-r_out,cy)); pen.curveTo((cx-r_out,cy+r_out*k),(cx-r_out*k,cy+r_out),(cx,cy+r_out))
    pen.curveTo((cx+r_out*k,cy+r_out),(cx+r_out,cy+r_out*k),(cx+r_out,cy))
    pen.curveTo((cx+r_out,cy-r_out*k),(cx+r_out*k,cy-r_out),(cx,cy-r_out))
    pen.curveTo((cx-r_out*k,cy-r_out),(cx-r_out,cy-r_out*k),(cx-r_out,cy)); pen.closePath()
    pen.moveTo((cx+r_in,cy)); pen.curveTo((cx+r_in,cy+r_in*k),(cx+r_in*k,cy+r_in),(cx,cy+r_in))
    pen.curveTo((cx-r_in*k,cy+r_in),(cx-r_in,cy+r_in*k),(cx-r_in,cy))
    pen.curveTo((cx-r_in,cy-r_in*k),(cx-r_in*k,cy-r_in),(cx,cy-r_in))
    pen.curveTo((cx+r_in*k,cy-r_in),(cx+r_in,cy-r_in*k),(cx+r_in,cy)); pen.closePath()
    pen = None; g.width = 0; g.glyphclass = "mark"

font.fontname = "PaliHangulV27"; font.familyname = "PaliHangul V27"; font.fullname = "PaliHangul V2.7"; font.version = "2.7"
font.save("/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd")
for f in os.listdir(os.path.expanduser("~/Library/Fonts")):
    if f.startswith("PaliHangul"): os.remove(os.path.expanduser(f"~/Library/Fonts/{f}"))
font.generate(os.path.expanduser("~/Library/Fonts/PaliHangulV27.otf"))
font.close()
print("✅ v2.7 완료! 윗빈원 y=780, 아래빈원 y=-150")

#!/usr/bin/env python3
"""
PaliHangul v2.4 - 위치 재조정
한글 '가' 기준: yMin=-162, yMax=798, ascent=800

문제: 결합 문자가 글자 안쪽에 있어서 안 보임
해결: 글자 바깥으로 확실히 이동

윗 기호: yMax(798) 위로 → 850~950 영역
아래 기호: yMin(-162) 아래로 → -200~-300 영역
"""

import fontforge

print("PaliHangul v2.4 - 위치 재조정")

sfd_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd"
print("폰트 로드중...")
font = fontforge.open(sfd_path)
print("  ✓ 로드 완료\n")

k = 0.5522

# ============================================================
# 윗빈원 (U+030A) - 글자 위로 확실히 올림
# 한글 상단 798 위에 → 중심 y=880
# ============================================================
print("1. 윗빈원 (U+030A) - y=880 (글자 위)")

g = font[0x030A]
g.clear()
pen = g.glyphPen()

cx, cy = 250, 880
r_out, r_in = 70, 48

pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*k), (cx - r_out*k, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*k, cy + r_out), (cx + r_out, cy + r_out*k), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*k), (cx + r_out*k, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*k, cy - r_out), (cx - r_out, cy - r_out*k), (cx - r_out, cy))
pen.closePath()
pen.moveTo((cx + r_in, cy))
pen.curveTo((cx + r_in, cy + r_in*k), (cx + r_in*k, cy + r_in), (cx, cy + r_in))
pen.curveTo((cx - r_in*k, cy + r_in), (cx - r_in, cy + r_in*k), (cx - r_in, cy))
pen.curveTo((cx - r_in, cy - r_in*k), (cx - r_in*k, cy - r_in), (cx, cy - r_in))
pen.curveTo((cx + r_in*k, cy - r_in), (cx + r_in, cy - r_in*k), (cx + r_in, cy))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 아래빈원 (U+0325) - 글자 아래로 확실히 내림
# 한글 하단 -162 아래에 → 중심 y=-250
# ============================================================
print("2. 아래빈원 (U+0325) - y=-250 (글자 아래)")

g = font[0x0325]
g.clear()
pen = g.glyphPen()

cx, cy = 250, -250
r_out, r_in = 70, 48

pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*k), (cx - r_out*k, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*k, cy + r_out), (cx + r_out, cy + r_out*k), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*k), (cx + r_out*k, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*k, cy - r_out), (cx - r_out, cy - r_out*k), (cx - r_out, cy))
pen.closePath()
pen.moveTo((cx + r_in, cy))
pen.curveTo((cx + r_in, cy + r_in*k), (cx + r_in*k, cy + r_in), (cx, cy + r_in))
pen.curveTo((cx - r_in*k, cy + r_in), (cx - r_in, cy + r_in*k), (cx - r_in, cy))
pen.curveTo((cx - r_in, cy - r_in*k), (cx - r_in*k, cy - r_in), (cx, cy - r_in))
pen.curveTo((cx + r_in*k, cy - r_in), (cx + r_in, cy - r_in*k), (cx + r_in, cy))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 위물결 (U+0303) - 글자 위로 확실히 올림
# y=860
# ============================================================
print("3. 위물결 (U+0303) - y=860 (글자 위)")

g = font[0x0303]
g.clear()
pen = g.glyphPen()

base_y = 860
amp = 18
thick = 15

pen.moveTo((120, base_y))
pen.curveTo((150, base_y + amp*2), (195, base_y + amp*2.2), (255, base_y))
pen.curveTo((315, base_y - amp*2.2), (360, base_y - amp*2), (385, base_y))
pen.lineTo((385, base_y - thick))
pen.curveTo((362, base_y - thick - amp*1.8), (318, base_y - thick - amp*2), (255, base_y - thick))
pen.curveTo((192, base_y - thick + amp*2), (148, base_y - thick + amp*1.8), (120, base_y - thick))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 아래물결 (U+0330) - 글자 아래로 확실히 내림
# y=-230
# ============================================================
print("4. 아래물결 (U+0330) - y=-230 (글자 아래)")

g = font[0x0330]
g.clear()
pen = g.glyphPen()

base_y = -230
amp = 18
thick = 15

pen.moveTo((120, base_y))
pen.curveTo((150, base_y + amp*2), (195, base_y + amp*2.2), (255, base_y))
pen.curveTo((315, base_y - amp*2.2), (360, base_y - amp*2), (385, base_y))
pen.lineTo((385, base_y - thick))
pen.curveTo((362, base_y - thick - amp*1.8), (318, base_y - thick - amp*2), (255, base_y - thick))
pen.curveTo((192, base_y - thick + amp*2), (148, base_y - thick + amp*1.8), (120, base_y - thick))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 장음 (U+FE20) - 위치도 올림
# ============================================================
print("5. 장음 (U+FE20) - y=860 (글자 위)")

g = font[0xFE20]
g.clear()
pen = g.glyphPen()

pen.moveTo((50, 860))
pen.curveTo((100, 890), (200, 900), (300, 890))
pen.lineTo((300, 875))
pen.curveTo((200, 885), (100, 875), (50, 845))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 캐론 (U+030C) - 위치도 올림
# ============================================================
print("6. 캐론 (U+030C) - y=870 기준 (글자 위)")

g = font[0x030C]
g.clear()
pen = g.glyphPen()

pen.moveTo((130, 900))
pen.lineTo((250, 830))
pen.lineTo((370, 900))
pen.lineTo((355, 920))
pen.lineTo((250, 855))
pen.lineTo((145, 920))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 꺽쇠 (U+0346) - 위치도 올림
# ============================================================
print("7. 꺽쇠 (U+0346) - y=880 기준 (글자 위)")

g = font[0x0346]
g.clear()
pen = g.glyphPen()

t = 22
cx, cy = 250, 880
pen.moveTo((cx + 80, cy + 70))
pen.lineTo((cx - 60, cy))
pen.lineTo((cx - 60, cy - t))
pen.lineTo((cx + 80, cy + 70 - t))
pen.closePath()
pen.moveTo((cx - 60, cy))
pen.lineTo((cx + 80, cy - 70))
pen.lineTo((cx + 80, cy - 70 + t))
pen.lineTo((cx - 60, cy + t))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 저장 + OTF 생성 + 설치
# ============================================================
font.fontname = "PaliHangulV24"
font.familyname = "PaliHangul V24"
font.fullname = "PaliHangul V2.4"
font.version = "2.4"

output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
font.save(f"{output_dir}/PaliHangul-v2.sfd")
print("  ✓ SFD 저장")

# 직접 ~/Library/Fonts에 설치
otf_path = "/Users/hailie/Library/Fonts/PaliHangulV24.otf"
font.generate(otf_path)
print(f"  ✓ OTF 생성 + 설치: {otf_path}")

font.close()
print("\n✅ v2.4 완료!")

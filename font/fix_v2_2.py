#!/usr/bin/env python3
"""
PaliHangul v2.2 - 위치/크기 조정
1. 겹따옴표: 1.25배
2. 빈원: 1.25배 더 크게
3. 윗빈원 y=700, 아래빈원 y=0
4. 위물결 y=720, 아래물결 y=-5
"""

import fontforge

print("PaliHangul v2.2 - 위치/크기 조정")
print()

sfd_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd"
print(f"폰트 로드중...")
font = fontforge.open(sfd_path)
print("  ✓ 로드 완료\n")

k = 0.5522  # 원 근사 상수

# ============================================================
# 1. 겹따옴표 (U+02BA) - 1.25배 크기
# ============================================================
print("1. 겹따옴표 (U+02BA) - 1.25배")

g = font[0x02BA]
g.clear()
pen = g.glyphPen()
# 기존 높이 130 → 162.5, 폭도 1.25배
pen.moveTo((65, 770))
pen.lineTo((90, 770))
pen.lineTo((77, 607))
pen.lineTo((52, 607))
pen.closePath()
pen.moveTo((130, 770))
pen.lineTo((155, 770))
pen.lineTo((142, 607))
pen.lineTo((117, 607))
pen.closePath()
pen = None
g.width = 220
print("  ✓ 완성\n")

# ============================================================
# 2&3. 윗 빈원 (U+030A) - 1.25배 더 크게, y=700
# 현재 r_out=56 → 70, r_in=38 → 47.5
# ============================================================
print("2. 윗 빈원 (U+030A) - 1.25배, y=700")

g = font[0x030A]
g.clear()
pen = g.glyphPen()

cx, cy = 250, 700
r_out, r_in = 70, 48

# 바깥 원
pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*k), (cx - r_out*k, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*k, cy + r_out), (cx + r_out, cy + r_out*k), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*k), (cx + r_out*k, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*k, cy - r_out), (cx - r_out, cy - r_out*k), (cx - r_out, cy))
pen.closePath()
# 안쪽 원 (반시계)
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
# 3. 아래 빈원 (U+0325) - 1.25배 더 크게, y=0
# ============================================================
print("3. 아래 빈원 (U+0325) - 1.25배, y=0")

g = font[0x0325]
g.clear()
pen = g.glyphPen()

cx, cy = 250, 0
r_out, r_in = 70, 48

# 바깥 원
pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*k), (cx - r_out*k, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*k, cy + r_out), (cx + r_out, cy + r_out*k), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*k), (cx + r_out*k, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*k, cy - r_out), (cx - r_out, cy - r_out*k), (cx - r_out, cy))
pen.closePath()
# 안쪽 원 (반시계)
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
# 4. 위 물결 (U+0303) - y=720
# ============================================================
print("4. 위 물결 (U+0303) - y=720")

g = font[0x0303]
g.clear()
pen = g.glyphPen()

base_y = 720
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
# 5. 아래 물결 (U+0330) - y=-5
# ============================================================
print("5. 아래 물결 (U+0330) - y=-5")

g = font[0x0330]
g.clear()
pen = g.glyphPen()

base_y = -5
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
# 저장
# ============================================================
font.version = "2.2"

output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
font.save(f"{output_dir}/PaliHangul-v2.sfd")
print("  ✓ SFD 저장")
font.generate(f"{output_dir}/PaliHangul-v2.otf")
print("  ✓ OTF 생성")
font.close()

print("\n✅ v2.2 완료!")

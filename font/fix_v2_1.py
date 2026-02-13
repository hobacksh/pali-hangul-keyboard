#!/usr/bin/env python3
"""
PaliHangul v2.1 - 글리프 수정
1. 겹따옴표(U+02BA) - compart.com 참고하여 올바른 모양
2. 글자 위 꺽쇠(U+E001) - FontForge로 제대로 제작
3. 빈 원(U+030A, U+0325) - 1.25배 크기, 글자에 더 붙임
4. 물결(U+0303, U+0330) - 0.9배 크기, 글자에 더 붙임
"""

import fontforge

print("=" * 60)
print("PaliHangul v2.1 - 글리프 수정")
print("=" * 60)
print()

sfd_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd"
print(f"폰트 로드: {sfd_path}")
font = fontforge.open(sfd_path)
print("  ✓ 로드 완료\n")

# ============================================================
# 1. 겹따옴표 (U+02BA) - MODIFIER LETTER DOUBLE PRIME
# compart.com 참고: 두 개의 세로 직선 (따옴표 스타일)
# ============================================================
print("1. 겹따옴표 (U+02BA) 수정 - 올바른 Double Prime 모양")

UC = 0x02BA
g = font[UC]
g.clear()

pen = g.glyphPen()
# 첫 번째 " (왼쪽) - 약간 기울어진 직선
pen.moveTo((70, 750))
pen.lineTo((90, 750))
pen.lineTo((80, 620))
pen.lineTo((60, 620))
pen.closePath()
# 두 번째 " (오른쪽) - 약간 기울어진 직선
pen.moveTo((130, 750))
pen.lineTo((150, 750))
pen.lineTo((140, 620))
pen.lineTo((120, 620))
pen.closePath()
pen = None
g.width = 220
print("  ✓ 완성\n")

# ============================================================
# 2. 글자 위 꺽쇠 (U+E001) - PUA
# 작은 < 를 글자 상단에 위치
# ============================================================
print("2. 글자 위 꺽쇠 (U+E001) 수정 - 더 명확한 < 모양")

UC = 0xE001
g = font[UC]
g.clear()

pen = g.glyphPen()
# 작은 < 모양 (글자 위, 중앙 정렬)
# 더 또렷하고 명확하게
thickness = 18
# 위쪽 선 (오른쪽 위 → 왼쪽 중앙)
pen.moveTo((330, 850))
pen.lineTo((340, 850 - thickness))
pen.lineTo((210, 790))
pen.lineTo((200, 790 + thickness))
pen.closePath()
# 아래쪽 선 (왼쪽 중앙 → 오른쪽 아래)
pen.moveTo((200, 790 - thickness))
pen.lineTo((210, 790))
pen.lineTo((340, 730 + thickness))
pen.lineTo((330, 730))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 3. 유성대기음 (U+030A) - COMBINING RING ABOVE
# 1.25배 크기, 글자에 더 붙임
# ============================================================
print("3. 유성대기음 (U+030A) 수정 - 1.25배 크기, 글자에 붙임")

UC = 0x030A
g = font[UC]
g.clear()

pen = g.glyphPen()
# 빈 원 1.25배 크기 (r_out: 45→56, r_in: 30→38)
# 위치: 글자에 더 붙임 (cy: 800→760)
cx, cy = 250, 760
r_out, r_in = 56, 38
k = 0.5522  # 원 근사 상수

# 바깥 원
pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*k), (cx - r_out*k, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*k, cy + r_out), (cx + r_out, cy + r_out*k), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*k), (cx + r_out*k, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*k, cy - r_out), (cx - r_out, cy - r_out*k), (cx - r_out, cy))
pen.closePath()
# 안쪽 원 (구멍) - 반시계 방향
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
# 4. 권설음 (U+0325) - COMBINING RING BELOW
# 1.25배 크기, 글자에 더 붙임
# ============================================================
print("4. 권설음 (U+0325) 수정 - 1.25배 크기, 글자에 붙임")

UC = 0x0325
g = font[UC]
g.clear()

pen = g.glyphPen()
# 빈 원 1.25배 크기, 글자에 더 붙임 (cy: -80→-50)
cx, cy = 250, -50
r_out, r_in = 56, 38
k = 0.5522

# 바깥 원
pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*k), (cx - r_out*k, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*k, cy + r_out), (cx + r_out, cy + r_out*k), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*k), (cx + r_out*k, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*k, cy - r_out), (cx - r_out, cy - r_out*k), (cx - r_out, cy))
pen.closePath()
# 안쪽 원 (구멍) - 반시계 방향
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
# 5. L 표기 (U+0303) - COMBINING TILDE (위 물결)
# 0.9배 크기, 글자에 더 붙임
# ============================================================
print("5. L 표기 (U+0303) 수정 - 0.9배 크기, 글자에 붙임")

UC = 0x0303
g = font[UC]
g.clear()

pen = g.glyphPen()
# 0.9배 축소, 글자에 더 붙임 (y: 790→755 기준)
# 중심 맞추기 위해 x도 약간 조정
base_y = 755
amp = 18  # 물결 진폭 (기존 ~20에서 약간 줄임)
thick = 15  # 두께

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
# 6. 구개비음 (U+0330) - COMBINING TILDE BELOW (아래 물결)
# 0.9배 크기, 글자에 더 붙임
# ============================================================
print("6. 구개비음 (U+0330) 수정 - 0.9배 크기, 글자에 붙임")

UC = 0x0330
g = font[UC]
g.clear()

pen = g.glyphPen()
# 0.9배 축소, 글자에 더 붙임 (y: -60→-35 기준)
base_y = -35
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
# 폰트 버전 업데이트 & 저장
# ============================================================
font.version = "2.1"

print("=" * 60)
print("폰트 저장 중...")
print("=" * 60)

output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
sfd_out = f"{output_dir}/PaliHangul-v2.sfd"
otf_out = f"{output_dir}/PaliHangul-v2.otf"

font.save(sfd_out)
print(f"  ✓ SFD: {sfd_out}")

font.generate(otf_out)
print(f"  ✓ OTF: {otf_out}")

font.close()

print()
print("=" * 60)
print("✅ PaliHangul v2.1 수정 완료!")
print("=" * 60)
print()
print("수정 사항:")
print("  1. 겹따옴표 (U+02BA) - 올바른 Double Prime 모양")
print("  2. 글자 위 꺽쇠 (U+E001) - 더 명확한 < 모양")
print("  3. 빈 원 (U+030A/0325) - 1.25배 크기, 글자에 붙임")
print("  4. 물결 (U+0303/0330) - 0.9배 크기, 글자에 붙임")
print()

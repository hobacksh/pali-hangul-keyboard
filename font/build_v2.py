#!/usr/bin/env python3
"""
PaliHangul 폰트 v2.0 - 처음부터 새로 제작
11종 기호 (결합 문자 9종 + 독립 기호 2종)
출처: "뿌라베다숫따 법문" 부록 7 + JB님 유니코드 지정
"""

import fontforge

print("=" * 60)
print("PaliHangul 폰트 v2.0 - 완전 새 제작")
print("=" * 60)
print()

# 기존 PaliHangul SFD 열기 (나눔명조 기반 한글 포함)
sfd_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-Regular.sfd"
print(f"기존 폰트 로드: {sfd_path}")
font = fontforge.open(sfd_path)

# 기존 결합 문자 클리어 (이전 작업물 제거)
old_chars = [0x0323, 0x0303, 0x1DC7, 0x030B, 0x030A, 0x0306, 0x302C, 0x302D, 0x032B, 0x034C]
for uc in old_chars:
    if uc in font:
        font[uc].clear()
        print(f"  기존 글리프 클리어: U+{uc:04X}")

print(f"\n  ✓ 기존 폰트 로드 완료\n")

# ============================================================
# 한글 기준 좌표 참고 (나눔명조 기준)
# ascent ~880, descent ~-120
# 한글 글자 상단: ~780, 하단: ~-50
# 중앙: ~350
# ============================================================

# ============================================================
# 1. 장음 (U+FE20) - COMBINING LIGATURE LEFT HALF
# ============================================================
print("1. 장음 (U+FE20) - COMBINING LIGATURE LEFT HALF")

UC = 0xFE20
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 글자 위에 가로선 (왼쪽 반) - 눈썹형
# 얇고 살짝 곡선
pen.moveTo((50, 800))
pen.curveTo((100, 830), (200, 840), (300, 830))
pen.lineTo((300, 815))
pen.curveTo((200, 825), (100, 815), (50, 785))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 2 & 5. 캐론 / '와' 표기 (U+030C) - COMBINING CARON
# ============================================================
print("2&5. 캐론 (U+030C) - COMBINING CARON (와 표기)")

UC = 0x030C
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# ˇ 모양 (위로 오목한 V)
pen.moveTo((130, 830))
pen.lineTo((250, 760))
pen.lineTo((370, 830))
pen.lineTo((355, 850))
pen.lineTo((250, 785))
pen.lineTo((145, 850))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 3. 자음중복 (U+02BA) - MODIFIER LETTER DOUBLE PRIME
# ============================================================
print("3. 자음중복 (U+02BA) - MODIFIER LETTER DOUBLE PRIME")

UC = 0x02BA
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 첫 번째 ' (왼쪽)
pen.moveTo((80, 820))
pen.lineTo((100, 820))
pen.lineTo((110, 700))
pen.lineTo((90, 700))
pen.closePath()
# 두 번째 ' (오른쪽)
pen.moveTo((140, 820))
pen.lineTo((160, 820))
pen.lineTo((170, 700))
pen.lineTo((150, 700))
pen.closePath()
pen = None
g.width = 250  # modifier letter이므로 폭 있음
print("  ✓ 완성\n")

# ============================================================
# 4. '야'의 표기 - 글자 위 꺽쇠 (<)
# U+003C는 기본 문자이므로 PUA 영역에 별도 생성
# U+E001 (PUA) 사용
# ============================================================
print("4. '야' 표기 (U+E001 PUA) - 글자 위 작은 꺽쇠 <")

UC = 0xE001
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 작은 < 모양 (글자 위에)
pen.moveTo((300, 830))
pen.lineTo((200, 790))
pen.lineTo((300, 750))
pen.lineTo((290, 740))
pen.lineTo((180, 790))
pen.lineTo((290, 840))
pen.closePath()
pen = None
g.width = 0  # 결합 문자처럼 사용
g.glyphclass = "mark"
print("  ✓ 완성 (PUA U+E001)\n")

# ============================================================
# 6. 유성대기음 (U+030A) - COMBINING RING ABOVE (빈 원)
# ============================================================
print("6. 유성대기음 (U+030A) - COMBINING RING ABOVE")

UC = 0x030A
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 글자 위 빈 원 (바깥)
cx, cy, r_out, r_in = 250, 800, 45, 30
# 바깥 원
pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*0.55), (cx - r_out*0.55, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*0.55, cy + r_out), (cx + r_out, cy + r_out*0.55), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*0.55), (cx + r_out*0.55, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*0.55, cy - r_out), (cx - r_out, cy - r_out*0.55), (cx - r_out, cy))
pen.closePath()
# 안쪽 원 (구멍)
pen.moveTo((cx - r_in, cy))
pen.curveTo((cx - r_in, cy + r_in*0.55), (cx - r_in*0.55, cy + r_in), (cx, cy + r_in))
pen.curveTo((cx + r_in*0.55, cy + r_in), (cx + r_in, cy + r_in*0.55), (cx + r_in, cy))
pen.curveTo((cx + r_in, cy - r_in*0.55), (cx + r_in*0.55, cy - r_in), (cx, cy - r_in))
pen.curveTo((cx - r_in*0.55, cy - r_in), (cx - r_in, cy - r_in*0.55), (cx - r_in, cy))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 7. 권설음 (U+0325) - COMBINING RING BELOW (빈 원)
# ============================================================
print("7. 권설음 (U+0325) - COMBINING RING BELOW")

UC = 0x0325
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 글자 아래 빈 원
cx, cy, r_out, r_in = 250, -80, 45, 30
# 바깥 원
pen.moveTo((cx - r_out, cy))
pen.curveTo((cx - r_out, cy + r_out*0.55), (cx - r_out*0.55, cy + r_out), (cx, cy + r_out))
pen.curveTo((cx + r_out*0.55, cy + r_out), (cx + r_out, cy + r_out*0.55), (cx + r_out, cy))
pen.curveTo((cx + r_out, cy - r_out*0.55), (cx + r_out*0.55, cy - r_out), (cx, cy - r_out))
pen.curveTo((cx - r_out*0.55, cy - r_out), (cx - r_out, cy - r_out*0.55), (cx - r_out, cy))
pen.closePath()
# 안쪽 원 (구멍)
pen.moveTo((cx - r_in, cy))
pen.curveTo((cx - r_in, cy + r_in*0.55), (cx - r_in*0.55, cy + r_in), (cx, cy + r_in))
pen.curveTo((cx + r_in*0.55, cy + r_in), (cx + r_in, cy + r_in*0.55), (cx + r_in, cy))
pen.curveTo((cx + r_in, cy - r_in*0.55), (cx + r_in*0.55, cy - r_in), (cx, cy - r_in))
pen.curveTo((cx - r_in*0.55, cy - r_in), (cx - r_in, cy - r_in*0.55), (cx - r_in, cy))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 8. L의 표기 (U+0303) - COMBINING TILDE (위 물결)
# ============================================================
print("8. L 표기 (U+0303) - COMBINING TILDE (위 물결)")

UC = 0x0303
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# ~ 물결 (위쪽) - S자 곡선
pen.moveTo((100, 790))
pen.curveTo((130, 830), (180, 840), (250, 810))
pen.curveTo((320, 780), (370, 790), (400, 830))
pen.lineTo((400, 810))
pen.curveTo((375, 775), (325, 765), (250, 793))
pen.curveTo((175, 821), (130, 811), (100, 773))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 9. 구개비음 (U+0330) - COMBINING TILDE BELOW (아래 물결)
# ============================================================
print("9. 구개비음 (U+0330) - COMBINING TILDE BELOW (아래 물결)")

UC = 0x0330
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# ~ 물결 (아래쪽) - S자 곡선
pen.moveTo((100, -60))
pen.curveTo((130, -20), (180, -10), (250, -40))
pen.curveTo((320, -70), (370, -60), (400, -20))
pen.lineTo((400, -40))
pen.curveTo((375, -75), (325, -85), (250, -57))
pen.curveTo((175, -29), (130, -39), (100, -77))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# ============================================================
# 10. 쉼표 (U+05C0) - HEBREW PUNCTUATION PASEQ
# ============================================================
print("10. 쉼표 (U+05C0) - HEBREW PUNCTUATION PASEQ (세로선)")

UC = 0x05C0
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 세로 직선
pen.moveTo((220, 0))
pen.lineTo((250, 0))
pen.lineTo((250, 600))
pen.lineTo((220, 600))
pen.closePath()
pen = None
g.width = 470
print("  ✓ 완성\n")

# ============================================================
# 11. 마침표 (U+2225) - PARALLEL TO
# ============================================================
print("11. 마침표 (U+2225) - PARALLEL TO (이중 세로선)")

UC = 0x2225
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 왼쪽 세로선
pen.moveTo((170, 0))
pen.lineTo((200, 0))
pen.lineTo((200, 600))
pen.lineTo((170, 600))
pen.closePath()
# 오른쪽 세로선
pen.moveTo((270, 0))
pen.lineTo((300, 0))
pen.lineTo((300, 600))
pen.lineTo((270, 600))
pen.closePath()
pen = None
g.width = 470
print("  ✓ 완성\n")

# ============================================================
# 폰트 메타데이터 업데이트
# ============================================================
font.fontname = "PaliHangul-Regular"
font.familyname = "PaliHangul"
font.fullname = "PaliHangul Regular"
font.version = "2.0"
font.copyright = "Based on Nanum Myeongjo (OFL). Extended for Pali-Hangul notation by JB Park, 2026."

# ============================================================
# 저장
# ============================================================
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
print("✅ PaliHangul v2.0 폰트 완성!")
print("=" * 60)
print()
print("포함된 기호 11종:")
print("  1.  장음        U+FE20  ◌︠  (위 가로선)")
print("  2&5.캐론        U+030C  ◌̌   (위로 오목 ˇ)")
print("  3.  자음중복    U+02BA  ʺ   (위 겹따옴표)")
print("  4.  '야' 표기   U+E001  <   (위 꺽쇠, PUA)")
print("  6.  유성대기음  U+030A  ◌̊   (위 빈 원)")
print("  7.  권설음      U+0325  ◌̥   (아래 빈 원)")
print("  8.  L 표기      U+0303  ◌̃   (위 물결)")
print("  9.  구개비음    U+0330  ◌̰   (아래 물결)")
print("  10. 쉼표        U+05C0  ׀   (세로선)")
print("  11. 마침표      U+2225  ∥   (이중 세로선)")
print()

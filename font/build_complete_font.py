#!/usr/bin/env python3
"""
PaliHangul 폰트 - 완전한 6종 결합 문자
출처: "뿌라베다숫따 법문" 부록 7 (p.314-321)
"""

import fontforge

print("=" * 60)
print("PaliHangul 폰트 - 6종 결합 문자 생성")
print("=" * 60)
print()

# 기존 PaliHangul 폰트 열기
sfd_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-Regular.sfd"
print(f"기존 폰트 로드: {sfd_path}")

font = fontforge.open(sfd_path)
print(f"  ✓ {font.fontname} 로드 완료\n")

# ============================================================
# 6종 결합 문자 유니코드
# ============================================================

COMBINING_DOT_BELOW = 0x0323      # ◌̣ 아랫점 (권설음)
COMBINING_TILDE_ABOVE = 0x0303    # ◌̃ 윗물결 (구개비음 ñ)
COMBINING_MACRON = 0x1DC7         # ◌᷇ 장음 (Kavyka)
COMBINING_DOUBLE_ACUTE = 0x030B   # ◌̎ 더블어큐트 (자음중복)
COMBINING_RING_ABOVE = 0x030A     # ◌̊ 링 (y+모음)
COMBINING_BREVE = 0x0306          # ◌̆ 브레브 (v+모음)

chars = [
    (COMBINING_DOT_BELOW, "아랫점 (권설음)", "◌̣"),
    (COMBINING_TILDE_ABOVE, "윗물결 (구개비음)", "◌̃"),
    (COMBINING_MACRON, "장음 (Kavyka)", "◌᷇"),
    (COMBINING_DOUBLE_ACUTE, "더블어큐트 (자음중복)", "◌̎"),
    (COMBINING_RING_ABOVE, "링 (y+모음)", "◌̊"),
    (COMBINING_BREVE, "브레브 (v+모음)", "◌̆"),
]

print("결합 문자 생성 중...\n")

# ============================================================
# 1. ◌̣ 아랫점 (U+0323) - Dot Below
# ============================================================
print("1. ◌̣ 아랫점 (U+0323) - 권설음 표시")

if COMBINING_DOT_BELOW not in font:
    font.createChar(COMBINING_DOT_BELOW)

glyph = font[COMBINING_DOT_BELOW]
glyph.clear()

pen = glyph.glyphPen()
# 속이 찬 원 (작고 명확하게)
pen.moveTo((250, -120))
pen.curveTo((280, -120), (300, -100), (300, -70))
pen.curveTo((300, -40), (280, -20), (250, -20))
pen.curveTo((220, -20), (200, -40), (200, -70))
pen.curveTo((200, -100), (220, -120), (250, -120))
pen.closePath()
pen = None

glyph.width = 0  # 결합 문자는 폭 0
glyph.glyphclass = "mark"
print("  ✓ 아랫점 완성\n")

# ============================================================
# 2. ◌̃ 윗물결 (U+0303) - Tilde Above
# ============================================================
print("2. ◌̃ 윗물결 (U+0303) - 구개비음 (ñ)")

if COMBINING_TILDE_ABOVE not in font:
    font.createChar(COMBINING_TILDE_ABOVE)

glyph = font[COMBINING_TILDE_ABOVE]
glyph.clear()

pen = glyph.glyphPen()
# ~ 물결 모양 (위쪽)
pen.moveTo((100, 750))
pen.curveTo((120, 770), (140, 780), (170, 770))
pen.curveTo((200, 760), (230, 770), (260, 780))
pen.curveTo((290, 790), (310, 780), (330, 760))
pen.lineTo((340, 775))
pen.curveTo((320, 795), (295, 805), (270, 795))
pen.curveTo((240, 785), (210, 795), (180, 805))
pen.curveTo((150, 815), (125, 805), (100, 780))
pen.closePath()
pen = None

glyph.width = 0
glyph.glyphclass = "mark"
print("  ✓ 윗물결 완성\n")

# ============================================================
# 3. ◌᷇ 장음 (U+1DC7) - Combining Latin Small Letter A with Diaeresis
# ============================================================
print("3. ◌᷇ 장음 (U+1DC7) - Kavyka 스타일")

if COMBINING_MACRON not in font:
    font.createChar(COMBINING_MACRON)

glyph = font[COMBINING_MACRON]
glyph.clear()

pen = glyph.glyphPen()
# 작은 곡선 (오른쪽 위로 살짝 휘어짐)
pen.moveTo((320, 760))
pen.curveTo((300, 780), (280, 790), (260, 790))
pen.lineTo((260, 770))
pen.curveTo((275, 770), (295, 762), (320, 740))
pen.closePath()
pen = None

glyph.width = 0
glyph.glyphclass = "mark"
print("  ✓ 장음 완성 (Kavyka)\n")

# ============================================================
# 4. ◌̎ 더블어큐트 (U+030B) - Double Acute Accent
# ============================================================
print("4. ◌̎ 더블어큐트 (U+030B) - 자음 중복")

if COMBINING_DOUBLE_ACUTE not in font:
    font.createChar(COMBINING_DOUBLE_ACUTE)

glyph = font[COMBINING_DOUBLE_ACUTE]
glyph.clear()

pen = glyph.glyphPen()
# 첫 번째 "/" (왼쪽)
pen.moveTo((180, 750))
pen.lineTo((200, 800))
pen.lineTo((185, 810))
pen.lineTo((165, 760))
pen.closePath()
# 두 번째 "/" (오른쪽)
pen.moveTo((240, 750))
pen.lineTo((260, 800))
pen.lineTo((245, 810))
pen.lineTo((225, 760))
pen.closePath()
pen = None

glyph.width = 0
glyph.glyphclass = "mark"
print("  ✓ 더블어큐트 완성\n")

# ============================================================
# 5. ◌̊ 링 (U+030A) - Ring Above
# ============================================================
print("5. ◌̊ 링 (U+030A) - y+모음 표시")

if COMBINING_RING_ABOVE not in font:
    font.createChar(COMBINING_RING_ABOVE)

glyph = font[COMBINING_RING_ABOVE]
glyph.clear()

pen = glyph.glyphPen()
# 속이 빈 작은 원 (위)
# 바깥쪽
pen.moveTo((250, 740))
pen.curveTo((280, 740), (300, 760), (300, 790))
pen.curveTo((300, 820), (280, 840), (250, 840))
pen.curveTo((220, 840), (200, 820), (200, 790))
pen.curveTo((200, 760), (220, 740), (250, 740))
pen.closePath()
# 안쪽 구멍
pen.moveTo((250, 760))
pen.curveTo((265, 760), (280, 775), (280, 790))
pen.curveTo((280, 805), (265, 820), (250, 820))
pen.curveTo((235, 820), (220, 805), (220, 790))
pen.curveTo((220, 775), (235, 760), (250, 760))
pen.closePath()
pen = None

glyph.width = 0
glyph.glyphclass = "mark"
print("  ✓ 링 완성\n")

# ============================================================
# 6. ◌̆ 브레브 (U+0306) - Breve
# ============================================================
print("6. ◌̆ 브레브 (U+0306) - v+모음 표시")

if COMBINING_BREVE not in font:
    font.createChar(COMBINING_BREVE)

glyph = font[COMBINING_BREVE]
glyph.clear()

pen = glyph.glyphPen()
# 작은 아치 모양 (∪)
pen.moveTo((180, 750))
pen.curveTo((180, 780), (200, 800), (250, 800))
pen.curveTo((300, 800), (320, 780), (320, 750))
pen.lineTo((340, 755))
pen.curveTo((340, 795), (310, 820), (250, 820))
pen.curveTo((190, 820), (160, 795), (160, 755))
pen.closePath()
pen = None

glyph.width = 0
glyph.glyphclass = "mark"
print("  ✓ 브레브 완성\n")

# ============================================================
# 폰트 저장
# ============================================================
print("=" * 60)
print("폰트 저장 중...")
print("=" * 60)

output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
sfd_path = f"{output_dir}/PaliHangul-Regular.sfd"
otf_path = f"{output_dir}/PaliHangul-Regular.otf"

font.save(sfd_path)
print(f"  ✓ SFD 저장: {sfd_path}")

font.generate(otf_path)
print(f"  ✓ OTF 생성: {otf_path}")

font.close()

print()
print("=" * 60)
print("✅ PaliHangul 폰트 완성!")
print("=" * 60)
print()
print("포함된 결합 문자 6종:")
print("  1. ◌̣ (U+0323) - 아랫점 (권설음)")
print("  2. ◌̃ (U+0303) - 윗물결 (구개비음)")
print("  3. ◌᷇ (U+1DC7) - 장음 (Kavyka)")
print("  4. ◌̎ (U+030B) - 더블어큐트 (자음중복)")
print("  5. ◌̊ (U+030A) - 링 (y+모음)")
print("  6. ◌̆ (U+0306) - 브레브 (v+모음)")
print()
print("다음 단계: 폰트 설치 및 테스트")
print()

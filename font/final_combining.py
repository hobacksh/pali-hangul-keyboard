#!/usr/bin/env python3
"""
PaliHangul 결합 문자 최종 수정
PDF 문서 기준으로 정확히 반영
"""

import fontforge

print("PaliHangul 폰트 열기...\n")

font = fontforge.open("/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-Regular.sfd")

# 유니코드
COMBINING_DOT_ABOVE = 0x302C      # 〬 윗점
COMBINING_DOT_BELOW = 0x302D      # 〭 아랫점
COMBINING_TILDE_BELOW = 0x032B    # ̫ 아랫물결
COMBINING_MACRON = 0x1DC7         # ᷇ 장음표
PUA_COMMA = 0x0F0801              # 쉼표 (PUA)
PUA_PERIOD = 0x0F0307             # 마침표 (PUA)

print("결합 문자 정확히 수정 중...\n")

# 1. 윗점 (U+302C) - 글자에 딱 붙임
print("1. 윗점 (U+302C)...")
if COMBINING_DOT_ABOVE not in font:
    font.createChar(COMBINING_DOT_ABOVE)
glyph = font[COMBINING_DOT_ABOVE]
glyph.clear()

pen = glyph.glyphPen()
# 속이 빈 원 (글자에 딱 붙임, 거의 닿음)
pen.moveTo((200, 600))  # 더 낮게
pen.curveTo((230, 600), (250, 620), (250, 650))
pen.curveTo((250, 680), (230, 700), (200, 700))
pen.curveTo((170, 700), (150, 680), (150, 650))
pen.curveTo((150, 620), (170, 600), (200, 600))
pen.closePath()
# 안쪽 구멍
pen.moveTo((200, 620))
pen.curveTo((215, 620), (230, 635), (230, 650))
pen.curveTo((230, 665), (215, 680), (200, 680))
pen.curveTo((185, 680), (170, 665), (170, 650))
pen.curveTo((170, 635), (185, 620), (200, 620))
pen.closePath()
pen = None
glyph.width = 0
print("  ✓ 윗점 완성")

# 2. 아랫점 (U+302D) - 글자에 딱 붙임
print("2. 아랫점 (U+302D)...")
if COMBINING_DOT_BELOW not in font:
    font.createChar(COMBINING_DOT_BELOW)
glyph = font[COMBINING_DOT_BELOW]
glyph.clear()

pen = glyph.glyphPen()
# 속이 빈 원 (글자에 딱 붙임, 거의 닿음)
pen.moveTo((200, -100))  # 더 높게
pen.curveTo((230, -100), (250, -80), (250, -50))
pen.curveTo((250, -20), (230, 0), (200, 0))
pen.curveTo((170, 0), (150, -20), (150, -50))
pen.curveTo((150, -80), (170, -100), (200, -100))
pen.closePath()
# 안쪽 구멍
pen.moveTo((200, -80))
pen.curveTo((215, -80), (230, -65), (230, -50))
pen.curveTo((230, -35), (215, -20), (200, -20))
pen.curveTo((185, -20), (170, -35), (170, -50))
pen.curveTo((170, -65), (185, -80), (200, -80))
pen.closePath()
pen = None
glyph.width = 0
print("  ✓ 아랫점 완성")

# 3. 장음표 (U+1DC7) - https://symbl.cc/kr/1DC7/ 모양
print("3. 장음표 (U+1DC7) - Combining Kavyka Above Right...")
if COMBINING_MACRON not in font:
    font.createChar(COMBINING_MACRON)
glyph = font[COMBINING_MACRON]
glyph.clear()

# 작은 곡선 (오른쪽 위로 휘어짐)
pen = glyph.glyphPen()
pen.moveTo((280, 620))  # 오른쪽 위 시작
pen.curveTo((260, 640), (240, 650), (220, 650))  # 왼쪽 아래로 곡선
pen.lineTo((220, 630))  # 두께
pen.curveTo((235, 630), (255, 622), (280, 600))  # 다시 위로
pen.closePath()
pen = None
glyph.width = 0
print("  ✓ 장음표 완성 (Kavyka 스타일)")

# 4. 아랫물결 (U+032B) - Combining Inverted Double Arch Below
print("4. 아랫물결 (U+032B)...")
if COMBINING_TILDE_BELOW not in font:
    font.createChar(COMBINING_TILDE_BELOW)
glyph = font[COMBINING_TILDE_BELOW]
glyph.clear()

# ~ 모양
pen = glyph.glyphPen()
pen.moveTo((80, -30))
pen.curveTo((100, -5), (130, 5), (160, -5))
pen.curveTo((190, -15), (220, -5), (250, 5))
pen.curveTo((280, 15), (300, 5), (320, -10))
pen.lineTo((310, -20))
pen.curveTo((290, -10), (270, -15), (250, -20))
pen.curveTo((220, -30), (190, -40), (160, -30))
pen.curveTo((130, -20), (100, -30), (80, -30))
pen.closePath()
pen = None
glyph.width = 0
print("  ✓ 아랫물결 완성")

# 5. 쉼표 (U+0F0801) - PUA
print("5. 쉼표 (U+0F0801) - PUA...")
if PUA_COMMA not in font:
    font.createChar(PUA_COMMA)
glyph = font[PUA_COMMA]
glyph.clear()

# 세로 작은 선
pen = glyph.glyphPen()
pen.moveTo((200, -50))
pen.lineTo((220, -50))
pen.lineTo((220, 50))
pen.lineTo((200, 50))
pen.closePath()
pen = None
glyph.width = 400
print("  ✓ 쉼표 완성")

# 6. 마침표 (U+0F0307) - PUA
print("6. 마침표 (U+0F0307) - PUA...")
if PUA_PERIOD not in font:
    font.createChar(PUA_PERIOD)
glyph = font[PUA_PERIOD]
glyph.clear()

# 작은 원
pen = glyph.glyphPen()
pen.moveTo((200, 0))
pen.curveTo((230, 0), (250, 20), (250, 50))
pen.curveTo((250, 80), (230, 100), (200, 100))
pen.curveTo((170, 100), (150, 80), (150, 50))
pen.curveTo((150, 20), (170, 0), (200, 0))
pen.closePath()
pen = None
glyph.width = 400
print("  ✓ 마침표 완성")

print("\n폰트 저장 중...")
output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
sfd_path = f"{output_dir}/PaliHangul-Regular.sfd"
otf_path = f"{output_dir}/PaliHangul-Regular.otf"

font.save(sfd_path)
print(f"  ✓ SFD: {sfd_path}")

font.generate(otf_path)
print(f"  ✓ OTF: {otf_path}")

font.close()

print("\n✅ 결합 문자 최종 수정 완료!")
print("\n개선 사항:")
print("  • 윗점 (U+302C): 글자에 딱 붙음")
print("  • 아랫점 (U+302D): 글자에 딱 붙음")
print("  • 장음표 (U+1DC7): Kavyka 스타일 (symbl.cc 기준)")
print("  • 아랫물결 (U+032B): ~ 모양")
print("  • 쉼표 (U+0F0801): PUA 추가")
print("  • 마침표 (U+0F0307): PUA 추가")
print("\nHTML 테스트:")
print("  open /tmp/pali_full_test.html")

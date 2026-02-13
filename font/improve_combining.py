#!/usr/bin/env python3
"""
PaliHangul 결합 문자 디자인 개선
나눔명조와 조화롭게 위치/크기/모양 조정
"""

import fontforge

print("PaliHangul 폰트 열기...\n")

# 폰트 열기
font = fontforge.open("/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-Regular.sfd")

# 결합 문자 코드
COMBINING_DOT_ABOVE = 0x302C      # 〬 윗점
COMBINING_DOT_BELOW = 0x302D      # 〭 아랫점
COMBINING_TILDE_BELOW = 0x032B    # ̫ 아랫물결
COMBINING_MACRON = 0x1DC7         # ᷇ 장음표

print("결합 문자 디자인 개선 시작...\n")

# 1. 윗점 (U+302C) - 비음 표시
print("1. 윗점 (〬) 디자인...")
glyph_dot_above = font[COMBINING_DOT_ABOVE]
glyph_dot_above.clear()

# 속이 빈 원 (글자에 바로 붙임)
pen = glyph_dot_above.glyphPen()
# 바깥 원
pen.moveTo((200, 620))  # 훨씬 더 아래로 (글자 바로 위)
pen.curveTo((235, 620), (260, 645), (260, 680))
pen.curveTo((260, 715), (235, 740), (200, 740))
pen.curveTo((165, 740), (140, 715), (140, 680))
pen.curveTo((140, 645), (165, 620), (200, 620))
pen.closePath()
# 안쪽 원 (구멍)
pen.moveTo((200, 645))
pen.curveTo((220, 645), (235, 660), (235, 680))
pen.curveTo((235, 700), (220, 715), (200, 715))
pen.curveTo((180, 715), (165, 700), (165, 680))
pen.curveTo((165, 660), (180, 645), (200, 645))
pen.closePath()
pen = None

glyph_dot_above.width = 0
print("  ✓ 윗점 완성 (글자에 바로 붙임)")

# 2. 아랫점 (U+302D) - 권설음 표시
print("2. 아랫점 (〭) 디자인...")
glyph_dot_below = font[COMBINING_DOT_BELOW]
glyph_dot_below.clear()

# 속이 빈 원 (글자에 바로 붙임)
pen = glyph_dot_below.glyphPen()
# 바깥 원
pen.moveTo((200, -120))  # 훨씬 더 위로 (글자 바로 아래)
pen.curveTo((235, -120), (260, -95), (260, -60))
pen.curveTo((260, -25), (235, 0), (200, 0))
pen.curveTo((165, 0), (140, -25), (140, -60))
pen.curveTo((140, -95), (165, -120), (200, -120))
pen.closePath()
# 안쪽 원 (구멍)
pen.moveTo((200, -95))
pen.curveTo((220, -95), (235, -80), (235, -60))
pen.curveTo((235, -40), (220, -25), (200, -25))
pen.curveTo((180, -25), (165, -40), (165, -60))
pen.curveTo((165, -80), (180, -95), (200, -95))
pen.closePath()
pen = None

glyph_dot_below.width = 0
print("  ✓ 아랫점 완성 (글자에 바로 붙임)")

# 3. 아랫물결 (U+032B) - 경구개 비음
print("3. 아랫물결 (̫) 디자인...")
glyph_tilde_below = font[COMBINING_TILDE_BELOW]
glyph_tilde_below.clear()

# ~ 문자와 완전히 같은 모양 (글자에 바로 붙임)
pen = glyph_tilde_below.glyphPen()
# 왼쪽 위로 올라가는 곡선
pen.moveTo((80, -40))
pen.curveTo((100, -10), (130, 0), (160, -10))
# 오른쪽 아래로 내려가는 곡선
pen.curveTo((190, -20), (220, -10), (250, 0))
pen.curveTo((280, 10), (300, 0), (320, -20))
# 아래쪽 경로 (두께 만들기)
pen.lineTo((310, -30))
pen.curveTo((290, -15), (270, -20), (250, -25))
pen.curveTo((220, -35), (190, -45), (160, -35))
pen.curveTo((130, -25), (100, -35), (80, -40))
pen.closePath()
pen = None

glyph_tilde_below.width = 0
print("  ✓ 아랫물결 완성 (~ 모양, 글자에 바로 붙임)")

# 4. 장음표 (U+1DC7) - 장모음 표시
print("4. 장음표 (᷇) 디자인...")
glyph_macron = font[COMBINING_MACRON]
glyph_macron.clear()

# 얇은 직선 (다᷇ 처럼, 글자에 바로 붙임)
pen = glyph_macron.glyphPen()
pen.moveTo((100, 630))  # 글자 바로 위
pen.lineTo((300, 630))   # 가로 직선
pen.lineTo((300, 660))   # 얇은 두께
pen.lineTo((100, 660))
pen.closePath()
pen = None

glyph_macron.width = 0
print("  ✓ 장음표 완성 (얇은 직선, 글자에 바로 붙임)")

print("\n결합 문자 디자인 개선 완료!\n")

# 폰트 저장
print("폰트 저장 중...")
output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
sfd_path = f"{output_dir}/PaliHangul-Regular.sfd"
otf_path = f"{output_dir}/PaliHangul-Regular.otf"

font.save(sfd_path)
print(f"  ✓ SFD: {sfd_path}")

font.generate(otf_path)
print(f"  ✓ OTF: {otf_path}")

font.close()

print("\n✅ 결합 문자 디자인 개선 완료!")
print("\n개선 사항:")
print("  • 윗점: 속이 빈 원형 ○ (글자에 바로 붙임)")
print("  • 아랫점: 속이 빈 원형 ○ (글자에 바로 붙임)")
print("  • 아랫물결: ~ 문자와 같은 모양 (글자에 바로 붙임)")
print("  • 장음표: 얇은 직선 ─ (글자에 바로 붙임)")
print("\nFontForge에서 확인:")
print(f"  open -a FontForge {sfd_path}")
print("\n또는 HTML 테스트:")
print("  open /tmp/pali_full_test.html")

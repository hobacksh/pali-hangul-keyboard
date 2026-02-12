#!/usr/bin/env python3
"""
PaliHangul 결합 문자 개선 버전
더 나은 가독성을 위한 글리프 디자인
"""

import fontforge
import math

# 기존 폰트 열기
font = fontforge.open("/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-Regular.sfd")

print("결합 문자 글리프 개선 중...\n")

# 1. 장음표 (᷇ U+1DC7) - 작은 수평선
print("1. 장음표 (᷇) 디자인 개선...")
if 0x1DC7 in font:
    glyph = font[0x1DC7]
else:
    glyph = font.createChar(0x1DC7, "combiningsupplementtop")
    glyph.glyphclass = "mark"

glyph.clear()
pen = glyph.glyphPen()

# 부드러운 수평선 (둥근 끝)
pen.moveTo((450, 770))
pen.lineTo((550, 770))
pen.curveTo((570, 770), (580, 775), (580, 785))
pen.curveTo((580, 795), (570, 800), (550, 800))
pen.lineTo((450, 800))
pen.curveTo((430, 800), (420, 795), (420, 785))
pen.curveTo((420, 775), (430, 770), (450, 770))
pen.closePath()

glyph.width = 0
print("  ✓ 부드러운 수평선 형태")

# 2. 윗점 (〬 U+302C) - 원형 점
print("\n2. 윗점 (〬) 디자인 개선...")
if 0x302C in font:
    glyph = font[0x302C]
else:
    glyph = font.createChar(0x302C, "ideographicenteringtonemark")
    glyph.glyphclass = "mark"

glyph.clear()
pen = glyph.glyphPen()

# 완전한 원 (베지어 곡선으로)
radius = 35
cx, cy = 500, 820

# 원을 4개의 베지어 곡선으로 표현
kappa = 0.5522847498  # 원을 베지어로 그리는 매직 넘버

# 상단 (12시)
pen.moveTo((cx, cy + radius))
# 오른쪽 (3시)
pen.curveTo((cx + radius * kappa, cy + radius), 
            (cx + radius, cy + radius * kappa), 
            (cx + radius, cy))
# 하단 (6시)
pen.curveTo((cx + radius, cy - radius * kappa), 
            (cx + radius * kappa, cy - radius), 
            (cx, cy - radius))
# 왼쪽 (9시)
pen.curveTo((cx - radius * kappa, cy - radius), 
            (cx - radius, cy - radius * kappa), 
            (cx - radius, cy))
# 상단으로 복귀
pen.curveTo((cx - radius, cy + radius * kappa), 
            (cx - radius * kappa, cy + radius), 
            (cx, cy + radius))
pen.closePath()

glyph.width = 0
print("  ✓ 완벽한 원형")

# 3. 아랫점 (〭 U+302D) - 원형 점 (아래)
print("\n3. 아랫점 (〭) 디자인 개선...")
if 0x302D in font:
    glyph = font[0x302D]
else:
    glyph = font.createChar(0x302D, "ideographicleavingtonemark")
    glyph.glyphclass = "mark"

glyph.clear()
pen = glyph.glyphPen()

# 윗점과 동일한 크기의 원 (위치만 아래로)
radius = 35
cx, cy = 500, -70

pen.moveTo((cx, cy + radius))
pen.curveTo((cx + radius * kappa, cy + radius), 
            (cx + radius, cy + radius * kappa), 
            (cx + radius, cy))
pen.curveTo((cx + radius, cy - radius * kappa), 
            (cx + radius * kappa, cy - radius), 
            (cx, cy - radius))
pen.curveTo((cx - radius * kappa, cy - radius), 
            (cx - radius, cy - radius * kappa), 
            (cx - radius, cy))
pen.curveTo((cx - radius, cy + radius * kappa), 
            (cx - radius * kappa, cy + radius), 
            (cx, cy + radius))
pen.closePath()

glyph.width = 0
print("  ✓ 완벽한 원형 (아래)")

# 4. 아랫물결 (̫ U+032B) - 부드러운 물결
print("\n4. 아랫물결 (̫) 디자인 개선...")
if 0x032B in font:
    glyph = font[0x032B]
else:
    glyph = font.createChar(0x032B, "combininginverteddoublearc")
    glyph.glyphclass = "mark"

glyph.clear()
pen = glyph.glyphPen()

# 부드러운 물결 곡선 (베지어)
# 시작점 (왼쪽)
pen.moveTo((300, -110))

# 첫 번째 파도 (올라감)
pen.curveTo((350, -90), (400, -85), (450, -95))

# 정점
pen.curveTo((470, -100), (480, -100), (500, -100))

# 두 번째 파도 (내려감)
pen.curveTo((520, -100), (530, -100), (550, -95))

# 끝 (오른쪽)
pen.curveTo((600, -85), (650, -90), (700, -110))

# 두께를 위해 반대 방향으로
pen.lineTo((700, -125))
pen.curveTo((650, -105), (600, -100), (550, -110))
pen.curveTo((530, -115), (520, -115), (500, -115))
pen.curveTo((480, -115), (470, -115), (450, -110))
pen.curveTo((400, -100), (350, -105), (300, -125))
pen.closePath()

glyph.width = 0
print("  ✓ 부드러운 물결 곡선")

# 한글 글리프도 조금 더 나은 형태로 개선
print("\n한글 기본 글리프 개선 중...")

hangul_chars = [
    (0xAC00, "가"),
    (0xB098, "나"),
    (0xB2E4, "다"),
    (0xB77C, "라"),
    (0xB9C8, "마"),
    (0xBC14, "바"),
    (0xC0AC, "사"),
    (0xC544, "아"),
    (0xC790, "자"),
    (0xCE74, "카"),
]

for code, char in hangul_chars:
    if code in font:
        glyph = font[code]
    else:
        glyph = font.createChar(code, char)
    
    glyph.clear()
    pen = glyph.glyphPen()
    
    # 둥근 모서리 사각형 (플레이스홀더지만 더 나은 형태)
    corner_radius = 50
    
    # 좌하단부터 시계방향
    pen.moveTo((100, corner_radius))
    # 좌측 하단 코너
    pen.curveTo((100, 0), (100, 0), (100 + corner_radius, 0))
    # 하단
    pen.lineTo((900 - corner_radius, 0))
    # 우측 하단 코너
    pen.curveTo((900, 0), (900, 0), (900, corner_radius))
    # 우측
    pen.lineTo((900, 700 - corner_radius))
    # 우측 상단 코너
    pen.curveTo((900, 700), (900, 700), (900 - corner_radius, 700))
    # 상단
    pen.lineTo((100 + corner_radius, 700))
    # 좌측 상단 코너
    pen.curveTo((100, 700), (100, 700), (100, 700 - corner_radius))
    # 좌측으로 복귀
    pen.closePath()
    
    glyph.width = 1000

print("  ✓ 10개 한글 글리프 (둥근 모서리)")

# 폰트 저장
output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
sfd_path = f"{output_dir}/PaliHangul-Regular.sfd"
otf_path = f"{output_dir}/PaliHangul-Regular.otf"

print("\n폰트 저장 중...")
font.save(sfd_path)
print(f"  ✓ SFD: {sfd_path}")

font.generate(otf_path)
print(f"  ✓ OTF: {otf_path}")

font.close()

print("\n✅ PaliHangul 결합 문자 개선 완료!")
print("\n개선 사항:")
print("  • 장음표: 부드러운 수평선 (둥근 끝)")
print("  • 윗점/아랫점: 완벽한 원형 (베지어 곡선)")
print("  • 아랫물결: 자연스러운 물결 모양")
print("  • 한글: 둥근 모서리 사각형")
print("\n테스트: 폰트를 재설치하고 확인하세요!")
print("예시: 가᷇ 나〬 다〭 라̫")

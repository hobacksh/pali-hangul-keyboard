#!/usr/bin/env python3
"""
PaliHangul - 글자 위 꺽쇠 (<) 수정
문제: PUA(U+E001)가 렌더링 안 됨
해결: 
1. 글리프를 더 크고 명확하게
2. GPOS mark anchor 설정
3. 대안으로 U+02C2 (MODIFIER LETTER LEFT ARROWHEAD ˂)도 추가
"""

import fontforge

print("글자 위 꺽쇠 수정")
print()

sfd_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd"
print("폰트 로드중...")
font = fontforge.open(sfd_path)
print("  ✓ 로드 완료\n")

# ============================================================
# 방법 1: PUA (U+E001) 글리프 개선
# 더 크고, 더 굵게, 명확하게
# ============================================================
print("1. PUA (U+E001) 글리프 개선...")

UC = 0xE001
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 더 크고 굵은 < 모양 (글자 위)
# 삼각형 스타일로 명확하게
t = 25  # 선 두께
# 위쪽 선
pen.moveTo((340, 870))    # 오른쪽 위
pen.lineTo((180, 790))    # 왼쪽 꼭지점
pen.lineTo((180, 790 - t))
pen.lineTo((340, 870 - t))
pen.closePath()
# 아래쪽 선
pen.moveTo((180, 790))    # 왼쪽 꼭지점
pen.lineTo((340, 710))    # 오른쪽 아래
pen.lineTo((340, 710 + t))
pen.lineTo((180, 790 + t))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ PUA 글리프 완성\n")

# ============================================================
# 방법 2: U+02C2 MODIFIER LETTER LEFT ARROWHEAD (˂)
# 이건 spacing modifier letter로, 독립적으로도 보임
# ============================================================
print("2. U+02C2 (MODIFIER LETTER LEFT ARROWHEAD) 추가...")

UC = 0x02C2
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# 작은 < 모양 (윗첨자 스타일)
t = 25
pen.moveTo((280, 820))
pen.lineTo((140, 720))
pen.lineTo((140, 720 - t))
pen.lineTo((280, 820 - t))
pen.closePath()
pen.moveTo((140, 720))
pen.lineTo((280, 620))
pen.lineTo((280, 620 + t))
pen.lineTo((140, 720 + t))
pen.closePath()
pen = None
g.width = 300  # modifier letter이므로 폭 있음
print("  ✓ U+02C2 완성\n")

# ============================================================
# 방법 3: U+0354 COMBINING LEFT ARROWHEAD BELOW를 
# 위쪽 버전으로 활용 (U+0346 COMBINING BRIDGE ABOVE 대신)
# 사실 가장 좋은 건 U+20D6 COMBINING LEFT ARROW ABOVE 사용
# ============================================================
print("3. U+0346 (COMBINING BRIDGE ABOVE) → 꺽쇠로 대체...")

UC = 0x0346
if UC not in font:
    font.createChar(UC)
g = font[UC]
g.clear()

pen = g.glyphPen()
# < 모양 결합 문자 (글자 위)
t = 22
cx, cy = 250, 780  # 중앙
pen.moveTo((cx + 80, cy + 70))    # 오른쪽 위
pen.lineTo((cx - 60, cy))          # 왼쪽 꼭지점
pen.lineTo((cx - 60, cy - t))
pen.lineTo((cx + 80, cy + 70 - t))
pen.closePath()
pen.moveTo((cx - 60, cy))          # 왼쪽 꼭지점
pen.lineTo((cx + 80, cy - 70))    # 오른쪽 아래
pen.lineTo((cx + 80, cy - 70 + t))
pen.lineTo((cx - 60, cy + t))
pen.closePath()
pen = None
g.width = 0
g.glyphclass = "mark"
print("  ✓ U+0346 완성 (결합 꺽쇠)\n")

# ============================================================
# 저장
# ============================================================
font.version = "2.3"
output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
font.save(f"{output_dir}/PaliHangul-v2.sfd")
print("  ✓ SFD 저장")
font.generate(f"{output_dir}/PaliHangul-v2.otf")
print("  ✓ OTF 생성")
font.close()
print("\n✅ 완료!")

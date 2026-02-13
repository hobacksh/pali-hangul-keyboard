#!/usr/bin/env python3
"""
PaliHangul - 꺽쇠(U+0346) 수정
문제: 두 개의 닫힌 경로가 겹쳐서 사각형으로 보임
해결: 하나의 경로로 < 모양을 그림
"""

import fontforge

print("꺽쇠 수정")

sfd_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-v2.sfd"
print("폰트 로드중...")
font = fontforge.open(sfd_path)
print("  ✓ 로드 완료\n")

# ============================================================
# 꺽쇠 (U+0346) - 하나의 경로로 < 모양
# 한글 상단 798 바로 위에 자연스럽게
# ============================================================
print("꺽쇠 (U+0346) 수정...")

g = font[0x0346]
g.clear()
pen = g.glyphPen()

# < 모양을 하나의 닫힌 경로로 (외곽선)
# 글자 바로 위 (y 중심 = 860)
t = 18  # 선 두께
cx = 250  # 수평 중심
cy = 860  # 수직 중심
arm = 55  # 팔 길이 (위아래)
depth = 50  # 꺽쇠 깊이 (왼쪽으로)

# 바깥쪽 (시계방향)
# 오른쪽 위 → 왼쪽 꼭지점 → 오른쪽 아래 → (안쪽으로 돌아감)
pen.moveTo((cx + depth, cy + arm))          # 오른쪽 위 (바깥)
pen.lineTo((cx - depth, cy))                 # 왼쪽 꼭지점 (바깥)
pen.lineTo((cx + depth, cy - arm))          # 오른쪽 아래 (바깥)
pen.lineTo((cx + depth, cy - arm + t))      # 오른쪽 아래 (안쪽)
pen.lineTo((cx - depth + t*2, cy))          # 왼쪽 꼭지점 (안쪽)
pen.lineTo((cx + depth, cy + arm - t))      # 오른쪽 위 (안쪽)
pen.closePath()
pen = None

g.width = 0
g.glyphclass = "mark"
print("  ✓ 완성\n")

# 저장
font.fontname = "PaliHangulV25"
font.familyname = "PaliHangul V25"
font.fullname = "PaliHangul V2.5"
font.version = "2.5"

output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
font.save(f"{output_dir}/PaliHangul-v2.sfd")
print("  ✓ SFD 저장")

import os
# 이전 폰트 삭제
for f in os.listdir(os.path.expanduser("~/Library/Fonts")):
    if f.startswith("PaliHangul"):
        os.remove(os.path.expanduser(f"~/Library/Fonts/{f}"))
        print(f"  삭제: {f}")

otf_path = os.path.expanduser("~/Library/Fonts/PaliHangulV25.otf")
font.generate(otf_path)
print(f"  ✓ OTF 설치: {otf_path}")

font.close()
print("\n✅ 완료!")

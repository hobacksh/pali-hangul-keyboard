#!/usr/bin/env python3
"""
PaliHangul 폰트 - 나눔명조 베이스 병합
"""

import fontforge
import os

print("나눔명조 폰트 병합 시작...\n")

# 나눔명조 Regular 열기
nanum_path = os.path.expanduser("~/Library/Fonts/NanumMyeongjo-Regular.ttf")
if not os.path.exists(nanum_path):
    print(f"❌ 나눔명조 파일을 찾을 수 없습니다: {nanum_path}")
    exit(1)

print(f"✓ 나눔명조 로드: {nanum_path}")
nanum = fontforge.open(nanum_path)

# PaliHangul 폰트 열기
pali_path = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-Regular.sfd"
print(f"✓ PaliHangul 로드: {pali_path}")
pali = fontforge.open(pali_path)

# 폰트 정보 업데이트
pali.fontname = "PaliHangul-Regular"
pali.familyname = "PaliHangul"
pali.fullname = "PaliHangul Regular"
pali.copyright = "Based on Nanum Myeongjo (Naver). Copyright (c) 2026 JB Park for PaliHangul modifications."
pali.version = "0.2.0"

print("\n한글 글리프 병합 중...")

# 한글 음절 전체 범위 (11,172자)
hangul_start = 0xAC00  # 가
hangul_end = 0xD7A3    # 힣

# PaliHangul 폰트 인코딩 확장
pali.encoding = "UnicodeFull"

copied_count = 0
for code in range(hangul_start, hangul_end + 1):
    if code in nanum:
        # 나눔명조의 글리프를 PaliHangul로 복사
        nanum.selection.select(code)
        nanum.copy()
        
        # PaliHangul에 글리프가 없으면 생성
        if code not in pali:
            pali.createChar(code)
        
        pali.selection.select(code)
        pali.paste()
        copied_count += 1
        
        if copied_count % 1000 == 0:
            print(f"  ... {copied_count}개 복사 완료")

print(f"✓ 총 {copied_count}개 한글 글리프 복사 완료")

# 기본 라틴 문자 복사
print("\n라틴 문자 복사 중...")
latin_ranges = [
    (0x0020, 0x007E),  # Basic Latin
    (0x00A0, 0x00FF),  # Latin-1 Supplement
]

latin_count = 0
for start, end in latin_ranges:
    for code in range(start, end + 1):
        if code in nanum:
            nanum.selection.select(code)
            nanum.copy()
            
            if code not in pali:
                pali.createChar(code)
            
            pali.selection.select(code)
            pali.paste()
            latin_count += 1

print(f"✓ {latin_count}개 라틴 문자 복사 완료")

# 기존 결합 문자는 유지 (이미 디자인 완료)
print("\n결합 문자 확인 중...")
combining_marks = [0x1DC7, 0x302C, 0x302D, 0x032B]
for code in combining_marks:
    if code in pali:
        print(f"  ✓ U+{code:04X} 유지")

print("\n폰트 저장 중...")
output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
sfd_path = f"{output_dir}/PaliHangul-Regular.sfd"
otf_path = f"{output_dir}/PaliHangul-Regular.otf"

pali.save(sfd_path)
print(f"  ✓ SFD: {sfd_path}")

pali.generate(otf_path)
print(f"  ✓ OTF: {otf_path}")

# 파일 크기 확인
otf_size = os.path.getsize(otf_path)
print(f"\n폰트 크기: {otf_size / 1024 / 1024:.1f} MB")

nanum.close()
pali.close()

print("\n✅ 나눔명조 베이스 병합 완료!")
print("\nPaliHangul 폰트 구성:")
print(f"  • 한글: {copied_count}자 (나눔명조)")
print(f"  • 라틴: {latin_count}자 (나눔명조)")
print("  • 결합 문자: 4개 (커스텀 디자인)")
print("\nFontForge에서 다시 열어서 확인하세요!")

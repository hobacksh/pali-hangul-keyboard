#!/usr/bin/env python3
"""
PaliHangul 폰트 프로토타입 생성기
FontForge Python 스크립트

기본 한글 10개 + 결합 문자 4개 테스트 폰트
"""

import fontforge
import os

# 폰트 생성
font = fontforge.font()
font.fontname = "PaliHangul-Regular"
font.familyname = "PaliHangul"
font.fullname = "PaliHangul Regular"
font.weight = "Regular"
font.copyright = "Copyright (c) 2026 JB Park. Licensed under SIL Open Font License 1.1"
font.version = "0.1.0"

# Em 크기 설정
font.em = 1000
font.ascent = 800
font.descent = 200

print("PaliHangul 폰트 생성 시작...")

# 기본 한글 10개 글리프 (프로토타입)
hangul_chars = [
    (0xAC00, "가"),  # U+AC00
    (0xB098, "나"),  # U+B098
    (0xB2E4, "다"),  # U+B2E4
    (0xB77C, "라"),  # U+B77C
    (0xB9C8, "마"),  # U+B9C8
    (0xBC14, "바"),  # U+BC14
    (0xC0AC, "사"),  # U+C0AC
    (0xC544, "아"),  # U+C544
    (0xC790, "자"),  # U+C790
    (0xCE74, "카"),  # U+CE74
]

print("한글 기본 글리프 생성 중...")
for code, char in hangul_chars:
    glyph = font.createChar(code, char)
    # 간단한 사각형 플레이스홀더 (나중에 실제 글리프로 대체)
    pen = glyph.glyphPen()
    pen.moveTo((100, 0))
    pen.lineTo((900, 0))
    pen.lineTo((900, 700))
    pen.lineTo((100, 700))
    pen.closePath()
    glyph.width = 1000
    print(f"  ✓ {char} (U+{code:04X})")

# 결합 문자 (Combining Diacritics)
combining_marks = [
    (0x1DC7, "장음표", "combiningsupplementtop"),
    (0x302C, "윗점", "ideographicenteringtonemark"),
    (0x302D, "아랫점", "ideographicleavingtonemark"),
    (0x032B, "아랫물결", "combininginverteddoublearc"),
]

print("\n결합 문자 생성 중...")
for code, name, glyph_name in combining_marks:
    glyph = font.createChar(code, glyph_name)
    glyph.glyphclass = "mark"  # Mark 클래스 설정
    
    pen = glyph.glyphPen()
    
    if "장음표" in name:
        # 장음표: 작은 수평선
        pen.moveTo((400, 750))
        pen.lineTo((600, 750))
        pen.lineTo((600, 780))
        pen.lineTo((400, 780))
        pen.closePath()
    
    elif "윗점" in name:
        # 윗점: 작은 원
        pen.moveTo((500, 820))
        pen.lineTo((520, 820))
        pen.lineTo((520, 840))
        pen.lineTo((500, 840))
        pen.closePath()
    
    elif "아랫점" in name:
        # 아랫점: 작은 원 (아래)
        pen.moveTo((500, -80))
        pen.lineTo((520, -80))
        pen.lineTo((520, -60))
        pen.lineTo((500, -60))
        pen.closePath()
    
    elif "아랫물결" in name:
        # 아랫물결: 물결 모양
        pen.moveTo((300, -120))
        pen.lineTo((500, -140))
        pen.lineTo((700, -120))
        pen.lineTo((700, -110))
        pen.lineTo((500, -130))
        pen.lineTo((300, -110))
        pen.closePath()
    
    glyph.width = 0  # 결합 문자는 폭 0
    print(f"  ✓ {name} (U+{code:04X})")

# OpenType GPOS Feature 추가
print("\nOpenType Features 추가 중...")
font.addLookup("mark", "gpos_mark2base", (), (("mark", (("DFLT", ("dflt",)),)),))
font.addLookupSubtable("mark", "mark-subtable")

# 각 한글 글리프에 anchor 추가
print("  ✓ 한글 글리프에 anchor 추가")
for code, char in hangul_chars:
    try:
        glyph = font[code]
        glyph.addAnchorPoint("top", "base", 500, 750)      # 장음표/윗점
        glyph.addAnchorPoint("bottom", "base", 500, -100)  # 아랫점/아랫물결
    except:
        print(f"    ! {char} anchor 추가 실패")

# 결합 문자에 anchor 추가
print("  ✓ 결합 문자에 anchor 추가")
for code, name, glyph_name in combining_marks:
    try:
        glyph = font[code]
        if "윗" in name or "장음" in name:
            glyph.addAnchorPoint("_top", "mark", 0, 0)
        else:
            glyph.addAnchorPoint("_bottom", "mark", 0, 0)
    except:
        print(f"    ! {name} anchor 추가 실패")

print("  ✓ GPOS mark positioning")

# 폰트 저장
output_dir = "/Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font"
os.makedirs(output_dir, exist_ok=True)

sfd_path = os.path.join(output_dir, "PaliHangul-Regular.sfd")
otf_path = os.path.join(output_dir, "PaliHangul-Regular.otf")

print(f"\n폰트 저장 중...")
font.save(sfd_path)
print(f"  ✓ SFD: {sfd_path}")

font.generate(otf_path)
print(f"  ✓ OTF: {otf_path}")

print("\n✅ PaliHangul 프로토타입 폰트 생성 완료!")
print(f"\n테스트: {otf_path} 를 설치하고 텍스트 편집기에서 확인하세요.")
print("예시 텍스트: 가᷇ 나〬 다〭 라̫")

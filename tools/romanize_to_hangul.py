#!/usr/bin/env python3
"""
빠알리어 로마자 → 한글 정밀 표기 변환기
결합 문자를 포함한 정확한 한글 표기 생성
"""

import re

# 유니코드 결합 문자
COMBINING_DOT_ABOVE = '\u302C'      # 〬 윗점
COMBINING_DOT_BELOW = '\u302D'      # 〭 아랫점
COMBINING_TILDE_BELOW = '\u032B'    # ̫ 아랫물결
COMBINING_MACRON = '\u1DC7'         # ᷇ 장음표

class PaliRomanToHangul:
    def __init__(self):
        # 다중 문자 패턴 (긴 것부터 먼저 매칭)
        self.multi_patterns = {
            # 권설음 (아랫점)
            'ṭṭh': ('땅', COMBINING_DOT_BELOW),
            'ṭṭ': ('땃', COMBINING_DOT_BELOW),
            'ṭh': ('탕', COMBINING_DOT_BELOW),
            'ṭa': ('따', COMBINING_DOT_BELOW),
            'ḍḍh': ('당', COMBINING_DOT_BELOW),
            'ḍḍ': ('땋', COMBINING_DOT_BELOW),
            'ḍh': ('당', COMBINING_DOT_BELOW),
            'ḍa': ('다', COMBINING_DOT_BELOW),
            'ṇṇ': ('난', COMBINING_DOT_BELOW),
            'ṇa': ('나', COMBINING_DOT_BELOW),
            
            # 이중 자음
            'ddh': '다',
            'dd': '땃',
            'kh': '카',
            'gh': '가',
            'ch': '차',
            'jh': '자',
            'th': '탕',
            'dh': '당',
            'ph': '파',
            'bh': '방',
            
            # 경구개 비음 (아랫물결)
            'ñña': ('냐', COMBINING_TILDE_BELOW),
            'ñ': ('냐', COMBINING_TILDE_BELOW),
            
            # 연구개 비음 (윗점)
            'ṅa': ('앙', COMBINING_DOT_ABOVE),
            
            # 니깔라 (윗점)
            'ṃ': (COMBINING_DOT_ABOVE,),  # 앞 글자 받침 ㅁ에 붙음
        }
        
        # 장모음
        self.long_vowels = {
            'ā': ('ㅏ', COMBINING_MACRON),
            'ī': ('ㅣ', COMBINING_MACRON),
            'ū': ('ㅜ', COMBINING_MACRON),
        }
        
        # 단일 자음
        self.consonants = {
            'k': 'ㄱ', 'g': 'ㄱ',
            'c': 'ㅈ', 'j': 'ㅈ',
            't': 'ㄷ', 'd': 'ㄷ',
            'n': 'ㄴ',
            'p': 'ㅂ', 'b': 'ㅂ',
            'm': 'ㅁ',
            'y': 'ㅇ',
            'r': 'ㄹ', 'l': 'ㄹ',
            'v': 'ㅂ',  # 또는 'ㅗ' (문맥 의존)
            's': 'ㅅ',
            'h': 'ㅎ',
        }
        
        # 모음
        self.vowels = {
            'a': 'ㅏ',
            'i': 'ㅣ',
            'u': 'ㅜ',
            'e': 'ㅔ',
            'o': 'ㅗ',
        }
    
    def convert(self, text: str) -> str:
        """로마자 → 한글 정밀 표기"""
        result = []
        i = 0
        
        while i < len(text):
            matched = False
            
            # 1. 다중 문자 패턴 매칭 (긴 것부터)
            for length in range(min(5, len(text) - i), 0, -1):
                substr = text[i:i+length]
                
                if substr in self.multi_patterns:
                    pattern = self.multi_patterns[substr]
                    if isinstance(pattern, tuple):
                        result.append(pattern[0])
                        if len(pattern) > 1:
                            result.append(pattern[1])
                    else:
                        result.append(pattern)
                    
                    i += length
                    matched = True
                    break
            
            if matched:
                continue
            
            # 2. 장모음
            if text[i:i+1] in self.long_vowels:
                vowel, macron = self.long_vowels[text[i]]
                # 이전 글자가 있으면 그 글자에 장음표 붙이기
                if result:
                    result.append(macron)
                i += 1
                continue
            
            # 3. 단일 자음
            if text[i] in self.consonants:
                result.append(self.consonants[text[i]])
                i += 1
                continue
            
            # 4. 모음
            if text[i] in self.vowels:
                result.append(self.vowels[text[i]])
                i += 1
                continue
            
            # 5. 기타 문자 (공백, 구두점 등)
            result.append(text[i])
            i += 1
        
        return ''.join(result)

# 테스트
if __name__ == '__main__':
    converter = PaliRomanToHangul()
    
    test_cases = [
        "Buddhānaṃ",
        "sabbaññutaññāṇassa",
        "catunnaṃ paccayānaṃ",
        "Nāññatra bojjhā tapasā",
        "sotthiṃ passāmi pāṇinaṃ",
    ]
    
    print("빠알리어 로마자 → 한글 정밀 표기 변환 테스트\n")
    print("=" * 60)
    
    for pali in test_cases:
        hangul = converter.convert(pali)
        print(f"\n로마자: {pali}")
        print(f"한글:   {hangul}")
    
    print("\n" + "=" * 60)
    print("\n✅ 변환 완료!")
    print("\nPaliHangul 폰트로 확인하세요:")
    print("open /Users/hailie/.openclaw/workspace/projects/pali-hangul-keyboard/font/PaliHangul-Regular.otf")

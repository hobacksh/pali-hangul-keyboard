# Pali Hangul Keyboard (빠알리어 한글 자판)

빠알리어 로마자를 한글 자판으로 편리하게 입력할 수 있는 IME(Input Method Editor)와 전용 폰트 개발 프로젝트

## 프로젝트 개요

### 목표
- **한글 자판 → 빠알리어 로마자 입력**: 한국인이 익숙한 한글 자판으로 빠알리어 특수 문자 입력
- **전용 폰트 개발**: 빠알리어 로마자 특수 문자를 아름답게 표현하는 OTF 폰트

### 빠알리어 특수 문자
빠알리어 로마자는 라틴 알파벳에 다음과 같은 특수 문자를 사용합니다:

| 문자 | 유니코드 | 설명 |
|------|----------|------|
| ā | U+0101 | a + macron (장음) |
| ī | U+012B | i + macron (장음) |
| ū | U+016B | u + macron (장음) |
| ṃ | U+1E43 | m + dot below (니깔라) |
| ṅ | U+1E45 | n + dot above (웅까) |
| ñ | U+00F1 | n + tilde (냐) |
| ḍ | U+1E0D | d + dot below (따) |
| ḷ | U+1E37 | l + dot below (라) |
| ṭ | U+1E6D | t + dot below (따) |
| ṇ | U+1E47 | n + dot below (나) |

## 프로젝트 구조

```
pali-hangul-keyboard/
├── README.md           # 이 파일
├── docs/               # 문서 (설계, 연구)
├── ime/                # IME 개발 (macOS/Windows)
├── font/               # 폰트 개발 (OTF)
└── assets/             # 디자인 리소스
```

## 개발 계획

### Phase 1: 연구 및 설계
- [ ] 빠알리어 로마자 특수 문자 목록 정리
- [ ] 한글 자판 → 빠알리어 매핑 설계
- [ ] IME 개발 방법 연구 (macOS: InputMethodKit, Windows: TSF)
- [ ] 폰트 디자인 스케치

### Phase 2: 폰트 개발
- [ ] 기본 라틴 알파벳 디자인
- [ ] 빠알리어 특수 문자 글리프 디자인
- [ ] OTF 파일 생성 (FontForge/Glyphs)
- [ ] 테스트 및 최적화

### Phase 3: IME 개발
- [ ] macOS IME 개발
- [ ] Windows IME 개발
- [ ] 키 매핑 커스터마이징 기능
- [ ] 설치 패키지 제작

### Phase 4: 배포
- [ ] GitHub Release
- [ ] 사용 가이드 문서 작성
- [ ] 커뮤니티 피드백 수집

## 기술 스택

### IME
- **macOS**: Swift + InputMethodKit
- **Windows**: C++ / C# + Text Services Framework (TSF)
- **Cross-platform option**: Rust (experimental)

### 폰트
- **포맷**: OpenType Font (OTF)
- **도구**: FontForge, Glyphs App, or FontLab
- **유니코드**: Unicode 15.0

## 참고 자료

- [빠알리어 로마자 표기법 (Wikipedia)](https://en.wikipedia.org/wiki/Pali_language#Romanization)
- [Unicode Diacritics](https://en.wikipedia.org/wiki/Combining_character)
- [macOS InputMethodKit](https://developer.apple.com/documentation/inputmethodkit)
- [Windows TSF](https://docs.microsoft.com/en-us/windows/win32/tsf/text-services-framework)
- [FontForge](https://fontforge.org/)

## 라이선스

TBD (MIT / OFL 검토 필요)

---

_프로젝트 시작: 2026-02-12_

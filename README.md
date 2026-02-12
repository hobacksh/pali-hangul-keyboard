# Pali Hangul Keyboard (빠알리어 한글 자판)

**한글로 빠알리어를 표기하는 전용 문자 시스템**과 IME(Input Method Editor), 전용 폰트 개발 프로젝트

## 프로젝트 개요

### 목표
- **한글 빠알리 표기 문자 세트**: 빠알리어 음가를 정확히 표현하는 한글 전용 문자 시스템
- **전용 IME 개발**: 한글 빠알리 문자를 쉽게 입력할 수 있는 자판
- **전용 폰트 개발**: 한글 빠알리 문자를 아름답게 표현하는 OTF 폰트

### 한글 빠알리 표기란?
빠알리어는 인도의 고대 언어로, 보통 로마자(Romanization)로 표기하지만, 한국인에게는 한글 표기가 더 직관적입니다.

**예시**:
- 로마자: `Namo tassa bhagavato arahato sammāsambuddhassa`
- 한글 빠알리: `나모 땃사 바가와토 아라하토 삼마삼붓닷사`

이 프로젝트는 **표준화된 한글 빠알리 표기 문자 세트**를 정의하고, 이를 쉽게 입력/표시할 수 있는 도구를 만듭니다.

## 한글 빠알리 문자 세트

이미지 참고: `assets/character_chart.jpg`

### 문자 분류

#### 1. 자음 (Consonants)
빠알리어 자음을 한글 초성/종성으로 표기

#### 2. 모음 (Vowels)
빠알리어 모음을 한글 중성으로 표기

#### 3. 장음/단음 구분
한글 받침 또는 별도 문자로 장음 표시

### 참고 자료
- KoPub바탕체 Bold 14pt 기준 문자표
- 전통적인 한글 빠알리 표기법 (한국 테라와다 불교 전통)

---

## 프로젝트 구조

```
pali-hangul-keyboard/
├── README.md           # 이 파일
├── docs/               # 문서 (설계, 연구)
│   ├── CHARACTER_SET.md  # 한글 빠알리 문자 세트 정의
│   └── RESEARCH.md       # 빠알리어 음운론 연구
├── ime/                # IME 개발 (macOS/Windows)
├── font/               # 폰트 개발 (OTF)
└── assets/             # 디자인 리소스 (문자표 이미지 등)
```

## 개발 계획

### Phase 1: 문자 세트 정의
- [x] 기존 한글 빠알리 표기 문자표 수집
- [ ] 모든 빠알리어 음가를 한글로 매핑
- [ ] 표준 문자 세트 확정
- [ ] 유니코드 호환성 검토

### Phase 2: 폰트 개발
- [ ] 한글 빠알리 전용 글리프 디자인
- [ ] 가독성 최적화 (경전 독송용)
- [ ] OTF 파일 생성
- [ ] 테스트 및 최적화

### Phase 3: IME 개발
- [ ] 표준 한글 자판 → 빠알리 문자 변환 로직
- [ ] macOS IME 개발
- [ ] Windows IME 개발
- [ ] 설치 패키지 제작

### Phase 4: 배포
- [ ] GitHub Release
- [ ] 사용 가이드 문서 작성
- [ ] 한국 테라와다 불교 커뮤니티 배포
- [ ] 피드백 수집

## 기술 스택

### IME
- **macOS**: Swift + InputMethodKit
- **Windows**: C++ / C# + Text Services Framework (TSF)

### 폰트
- **포맷**: OpenType Font (OTF)
- **도구**: FontForge, Glyphs App, or FontLab
- **기반**: 한글 유니코드 (U+AC00 ~ U+D7A3)

## 참고 자료

- [빠알리어 음운론 (Wikipedia)](https://en.wikipedia.org/wiki/Pali_language)
- [한국 테라와다 불교 협회](http://www.theravada.kr)
- [한글 빠알리 삼장](https://tipitaka.fount.app)
- [macOS InputMethodKit](https://developer.apple.com/documentation/inputmethodkit)
- [Windows TSF](https://docs.microsoft.com/en-us/windows/win32/tsf/text-services-framework)

## 라이선스

TBD (MIT / OFL 검토 필요)

---

_프로젝트 시작: 2026-02-12_

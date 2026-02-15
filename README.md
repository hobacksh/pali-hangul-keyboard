# Pali Hangul Keyboard (빠알리어 한글 자판)

**한글로 빠알리어를 표기하는 전용 입력기(IME)와 폰트 개발 프로젝트**

## 프로젝트 개요

### 라이선스 체크리스트
- OFL 준수 체크: [`LICENSE_CHECKLIST.md`](./LICENSE_CHECKLIST.md)

### 목표
- **한글 빠알리 표기 시스템**: 빠알리어 음가를 정확히 표현하는 한글 표기법 (결합 문자 기반)
- **전용 IME 개발**: 한글 자판으로 빠알리어 결합 문자를 쉽게 입력
- **전용 폰트 개발**: 권설음 아랫점과 장모음 마크론을 지원하는 OTF 폰트

### 한글 빠알리 표기란?
빠알리어는 인도의 고대 언어로, 보통 로마자(Romanization)로 표기하지만, 한국인에게는 한글 표기가 더 직관적입니다.

**예시**:
- 로마자: `Namo tassa bhagavato arahato sammāsambuddhassa`
- 한글 빠알리: `나모 땃사 바가와토 아라하토 삼마̄삼붇닷사`

이 프로젝트는 **"뿌라베다숫따 법문" 부록의 표기법**을 기반으로,  
**Romanized Pali 입력에 최적화된 한글 표기 시스템**을 만듭니다.

## 표기 철학

### 기반: "뿌라베다숫따 법문" 부록 7
한국 테라와다 불교계의 표준 표기법을 따르되,  
Myanmar Pali가 아닌 **Romanized Pali 입력**에 맞게 단순화합니다.

### 핵심 원칙
- ✅ **권설음 구별**: ṭ/ḍ/ṇ → 따̣/다̣/나̣ (아랫점 ◌̣)
- ✅ **장모음 명시**: ā/ī/ū → 가̄/기̄/구̄ (마크론 ◌̄)
- ✅ **5단 자음 체계**: 후음/구개음/권설음/치음/순음
- ❌ **Myanmar 전용 기호 생략**: 자음 중복(◌̎), yi/vo 구별(◌̊/◌̆) 불필요

### 결합 문자 2종
1. **◌̣ (아랫점, U+0323)**: 권설음 표시 - `Option + D`
2. **◌̄ (마크론, U+0304)**: 장모음 표시 - `Option + M`

---

## 표기 예시

### 기본 자음 5단 체계

| 조음 위치 | 무성무기 | 무성유기 | 유성무기 | 유성유기 | 비음 |
|----------|----------|----------|----------|----------|------|
| 후음 | k 까 | kh 카 | g 가 | gh 가̎ | ṅ 앙 |
| 구개음 | c 짜 | ch 차 | j 자 | jh 자̎ | ñ 냐 |
| 권설음 | ṭ 따̣ | ṭh 타̣ | ḍ 다̣ | ḍh 다̣̎ | ṇ 나̣ |
| 치음 | t 따 | th 타 | d 다 | dh 다̎ | n 나 |
| 순음 | p 빠 | ph 파 | b 바 | bh 바̎ | m 마 |

### 실제 단어 예시

#### Buddha (붓다̎)
- `b` → 바 (순음 유성무기)
- `u` → ㅜ (단모음)
- `ddh` → 다̎ (치음 유성유기, 받침 'ㄷ')
- `a` → ㅏ (단모음)

#### Dhamma (담마)
- `dh` → 다̎ (치음 유성유기)
- `a` → ㅏ (단모음)
- `mm` → ㅁ (순음 비음, 받침)
- `a` → ㅏ (단모음)

#### Nibbāṇa (닙바̄나̣)
- `n` → 나 (치음 비음)
- `i` → ㅣ (단모음)
- `bb` → ㅂ (순음 무성무기, 겹자음)
- `ā` → ㅏ̄ (장모음!)
- `ṇ` → 나̣ (권설음 비음!)
- `a` → ㅏ (단모음)

---

## 프로젝트 구조

```
pali-hangul-keyboard/
├── README.md                   # 이 파일
├── PDF_NOTATION_ANALYSIS.md    # "뿌라베다숫따 법문" 표기법 분석
├── docs/                       # 문서 (설계, 연구)
│   ├── CHARACTER_SET.md        # 한글 빠알리 문자 세트 정의
│   ├── FONT_DESIGN.md          # 폰트 디자인 문서
│   ├── INPUT_METHOD.md         # IME 설계 문서
│   ├── KEYBOARD_MAPPING.md     # 키보드 매핑 규칙
│   ├── MAPPING_TABLE.md        # Pali → 한글 변환 테이블
│   └── RESEARCH.md             # 빠알리어 음운론 연구
├── ime/                        # IME 개발 (macOS/Windows)
├── font/                       # 폰트 개발 (OTF)
│   ├── PaliHangul-Regular.otf  # 완성된 폰트
│   └── build/                  # 빌드 스크립트
└── assets/                     # 디자인 리소스
    └── character_chart.jpg     # 문자표 이미지
```

---

## 개발 계획

### Phase 1: 문자 세트 정의 ✅
- [x] "뿌라베다숫따 법문" 표기법 분석
- [x] Pali → 한글 매핑 규칙 확정
- [x] 결합 문자 2종 선택 (아랫점, 마크론)
- [x] 표준 문자 세트 확정

### Phase 2: 폰트 개발 ✅
- [x] 나눔명조 기반 폰트 생성
- [x] 한글 11,172자 + 결합문자 4개
- [x] OTF 파일 생성 (`PaliHangul-Regular.otf`)
- [ ] 필요시 권설음 아랫점 위치 조정

### Phase 3: IME 개발 🔄
- [x] 키 매핑 설계 (Option+D, Option+M, Option+U, Option+T)
- [ ] macOS IME 개발 (Swift + InputMethodKit)
- [ ] 실제 입력 테스트
- [ ] 설치 패키지 제작

### Phase 4: Windows IME ⏳
- [ ] Windows 키 매핑 설계
- [ ] Windows IME 개발 (C++ / C# + TSF)
- [ ] 설치 패키지 제작

### Phase 5: 배포 ⏳
- [ ] GitHub Release
- [ ] 사용 가이드 문서 작성
- [ ] 한국 테라와다 불교 커뮤니티 배포
- [ ] 피드백 수집

---

## 기술 스택

### IME
- **macOS**: Swift + InputMethodKit
- **Windows**: C++ / C# + Text Services Framework (TSF)

### 폰트
- **포맷**: OpenType Font (OTF)
- **도구**: FontForge + Python
- **기반**: 나눔명조 (OFL 라이선스)

### 개발 환경
- **OS**: macOS (주 개발)
- **언어**: Swift (macOS IME), Python (폰트 빌드)
- **VCS**: Git + GitHub

---

## 참고 자료

### 표기법
- **"뿌라베다숫따 법문" 부록 7** - 빠알리어의 발음과 표기 (p.314-321)
- 상세 분석: `PDF_NOTATION_ANALYSIS.md`

### 빠알리어
- [빠알리어 음운론 (Wikipedia)](https://en.wikipedia.org/wiki/Pali_language)
- [한국 테라와다 불교 협회](http://www.theravada.kr)
- [한글 빠알리 삼장](https://tipitaka.fount.app)

### 기술 문서
- [macOS InputMethodKit](https://developer.apple.com/documentation/inputmethodkit)
- [Windows TSF](https://docs.microsoft.com/en-us/windows/win32/tsf/text-services-framework)
- [Unicode Combining Characters](https://unicode.org/charts/PDF/U0300.pdf)

---

## 라이선스

- **폰트**: OFL 1.1 (나눔명조 기반)
- **코드**: MIT (예정)

---

## GitHub

https://github.com/hobacksh/pali-hangul-keyboard

---

_프로젝트 시작: 2026-02-12_  
_표기 체계 확정: 2026-02-13_ ✅

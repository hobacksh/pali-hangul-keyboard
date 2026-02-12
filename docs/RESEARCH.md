# Pali Hangul Keyboard - 연구 노트

## 빠알리어 로마자 특수 문자 완전 목록

### 모음 (Vowels) - 장음 표시

| 한글 발음 | 짧은 소리 | 긴 소리 | Unicode |
|-----------|-----------|---------|---------|
| 아 | a | ā | U+0101 |
| 이 | i | ī | U+012B |
| 우 | u | ū | U+016B |

### 자음 (Consonants)

#### 1. Dot Above (위에 점)
| 문자 | 발음 | Unicode | 설명 |
|------|------|---------|------|
| ṅ | 웅 | U+1E45 | velar nasal (후음 비음) |

#### 2. Dot Below (아래 점)
| 문자 | 발음 | Unicode | 설명 |
|------|------|---------|------|
| ṃ | ㅁ (니깔라) | U+1E43 | niggahīta (비음화) |
| ḍ | 드 (경구개음) | U+1E0D | retroflex d |
| ḷ | 르 (경구개음) | U+1E37 | retroflex l |
| ṭ | 트 (경구개음) | U+1E6D | retroflex t |
| ṇ | 느 (경구개음) | U+1E47 | retroflex n |

#### 3. Tilde (물결표)
| 문자 | 발음 | Unicode | 설명 |
|------|------|---------|------|
| ñ | 냐 | U+00F1 | palatal nasal (경구개 비음) |

---

## 한글 자판 매핑 아이디어

### 옵션 1: 받침 활용
- 장음: `ㅏ + ㄱ` → `ā`, `ㅣ + ㄱ` → `ī`
- 점 아래: `ㅁ + ㅂ` → `ṃ`, `ㄷ + ㅂ` → `ḍ`
- 점 위: `ㅇ + ㄱ` → `ṅ`
- 물결: `ㄴ + ㅁ` → `ñ`

### 옵션 2: 쌍자음 활용
- 장음: `ㅏㅏ` → `ā`, `ㅣㅣ` → `ī`
- 특수: `ㄷㄷ` → `ḍ`, `ㅌㅌ` → `ṭ`

### 옵션 3: 조합키 (가장 직관적)
- `Option + a` → `ā`
- `Option + i` → `ī`
- `Option + m` → `ṃ`
- `Option + n` → `ṅ`
- `Option + Shift + n` → `ñ`

**추천**: 옵션 3 (조합키)가 배우기 쉽고 타이핑 속도가 빠름

---

## IME 개발 방법론

### macOS
- **Framework**: InputMethodKit (Objective-C / Swift)
- **구조**:
  ```
  IMEController
  ├── handleEvent() - 키보드 입력 처리
  ├── composedString() - 조합 중인 문자열
  └── commitComposition() - 최종 문자 입력
  ```
- **설치**: `/Library/Input Methods/` 또는 `~/Library/Input Methods/`

### Windows
- **Framework**: Text Services Framework (TSF) - C++ or C#
- **구조**:
  ```
  ITfTextInputProcessor
  ├── Activate() - IME 활성화
  ├── OnSetFocus() - 포커스 획득
  └── OnKeyDown() - 키 입력 처리
  ```
- **설치**: Registry 등록 + DLL 배포

---

## 폰트 개발 로드맵

### 1단계: 기본 글리프 디자인
- [ ] 라틴 알파벳 a-z, A-Z (52개)
- [ ] 숫자 0-9 (10개)
- [ ] 기본 기호 (.,!? 등)

### 2단계: 빠알리어 특수 문자
- [ ] ā, ī, ū (장음)
- [ ] ṃ, ṅ, ñ, ḍ, ḷ, ṭ, ṇ (특수 자음)

### 3단계: OpenType Features
- [ ] Ligatures (연결 글자)
- [ ] Kerning (자간 조정)
- [ ] Stylistic Alternates (대체 글리프)

### 도구 선택
- **FontForge**: 무료, 오픈소스, 학습 곡선 있음
- **Glyphs**: 유료 (€299), macOS 전용, 디자이너 친화적
- **FontLab**: 유료 ($459), 전문가용

**추천**: FontForge로 시작 (무료이고 충분히 강력함)

---

## 참고 기존 프로젝트

- **Velthuis Romanization**: 빠알리어 ASCII 기반 입력 방식
- **SIL Fonts**: 언어학 연구용 유니코드 폰트 (Charis SIL, Gentium)
- **Keyman**: 다국어 키보드 플랫폼 (참고용)

---

_마지막 업데이트: 2026-02-12_

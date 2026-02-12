# 한글 빠알리 입력 방법 분석

## 개요

이 문서는 기존 아래아한글 빠알리어 입력 시스템을 분석하고, 이를 독립적인 IME로 발전시키기 위한 연구 내용입니다.

**참고 자료**: `../assets/hangul_input_guide.pdf`

---

## 기존 시스템 (아래아한글 상용구)

### 입력 방법
1. 준말(shortcut) 입력
2. `Alt + I` 키 조합
3. 본말(full form)로 자동 변환

**예시**:
- 준말 입력: `강`
- `Alt + I` 누름
- 변환 결과: `sa〬ṅgha` (상가)

---

## 유니코드 결합 문자 체계

### 1. 장음 표시
- **문자**: ā, ī, ū
- **유니코드**: U+1DC7 (᷇) - Combining Kavyka Above Right
- **용도**: 한글 모음 위에 장음 표시

### 2. 윗점 (Dot Above)
- **문자**: ṅ (velar nasal), ṁ (niggahīta)
- **유니코드**: 
  - U+302C (〬) - Ideographic Entering Tone Mark
  - U+02D1 (ˑ) - Modifier Letter Half Triangular Colon
- **용도**: 비음 표시

### 3. 아랫점 (Dot Below)
- **문자**: ṇ (retroflex n), ṭ, ḍ, ḷ
- **유니코드**: U+302D (〭) - Ideographic Leaving Tone Mark
- **용도**: 권설음(retroflex) 표시

### 4. 아랫물결 (Tilde Below)
- **문자**: ñ (palatal nasal)
- **유니코드**: U+032B (̫) - Combining Inverted Double Arch Below
- **용도**: 경구개 비음 표시

### 5. 구두점
- **쉼표**: U+0F0801 (󰠁) - Private Use Area
- **마침표**: U+0F0307 (󰠁) - Private Use Area
- **Note**: 전용 폰트 필요 (PUA 사용)

### 6. 특수 표시

#### L 로마항소 (lomahaṁso)
- **유니코드**: U+034C (͌) - Combining Almost Equal To Above
- **용도**: ㄹ 앞에서 ㄹ임을 명시

#### v와 y 구분
- **v**: U+1DC3 (᷃) - Combining Suspension Mark
- **y**: U+1DFE (᷾) - Combining Left Arrowhead and Down Arrowhead Below
- **용도**: 중복 자음 구분 (예: miccheyya̿)

#### 중복 표시
- **유니코드**: U+033F (̿) - Combining Double Overline
- **대체**: U+0342 (͂) - Combining Greek Perispomeni
- **용도**: 나눔체/끄레도체에서 위치 조정

#### 아랫점 위치 명시
- **수난뚜 (sunaṇtu)**: U+02D5 (˕) - Modifier Letter Down Arrowhead
- **용도**: 아랫점이 위의 ㄴ임을 밝힘

#### 윗점 위치 명시
- **아밥바 (abhabba)**: U+02D4 (˔) - Modifier Letter Up Arrowhead
- **용도**: 윗점이 위의 ㅂ임을 밝힘

---

## 폰트 요구사항

### 필수 글리프
1. **한글 기본 음절**: 11,172개 (U+AC00 ~ U+D7A3)
2. **결합 문자 (Combining Diacritics)**: 
   - 장음: U+1DC7
   - 윗점: U+302C, U+02D1
   - 아랫점: U+302D
   - 아랫물결: U+032B
   - 기타 특수 기호: U+034C, U+1DC3, U+1DFE, U+033F, U+0342, U+02D5, U+02D4
3. **Private Use Area (PUA)**: U+0F0801, U+0F0307 (구두점)

### 위치 조정 (Vertical Positioning)
- **PDF 편집**: 나눔체/끄레도체에서 미세 조정 가능
- **아래아한글**: 제한적 조정만 가능
- **목표**: 폰트 자체에서 올바른 위치 렌더링

---

## IME 요구사항

### 기능
1. **상용구 자동 완성**: 준말 → 본말 변환
2. **단축키**: `Alt + I` 또는 커스터마이징 가능
3. **실시간 미리보기**: 입력 중 변환 결과 표시
4. **사용자 사전**: 자주 쓰는 단어 등록

### 입력 방식 예시

#### 예시 1: saṅgha (상가)
1. 입력: `강`
2. `Alt + I`
3. 출력: `sa〬ṅgha`

#### 예시 2: sunaṇtu (수난뚜)
1. 입력: `수난뚜`
2. `Alt + I`
3. 출력: `su〭na〭ṇtu` (아랫점 자동 배치)

---

## 다음 단계

### Phase 1: 문자 세트 완성
- [ ] 모든 준말 → 본말 매핑 테이블 작성
- [ ] 유니코드 결합 규칙 정의
- [ ] 테스트 문장 작성

### Phase 2: 폰트 개발
- [ ] 한글 기본 글리프 디자인
- [ ] 결합 문자 위치 최적화
- [ ] PUA 구두점 디자인
- [ ] 테스트 빌드 (나눔체/끄레도체 참고)

### Phase 3: IME 프로토타입
- [ ] macOS: 상용구 자동 완성 엔진
- [ ] Windows: TSF 기반 변환 로직
- [ ] 사용자 사전 관리
- [ ] 설정 UI

---

## 참고 폰트
- **나눔체**: 결합 문자 위치 조정 양호
- **끄레도체 (Kredo)**: 빠알리어 전용 최적화
- **목표**: 나눔체/끄레도체 수준의 렌더링 품질

---

_마지막 업데이트: 2026-02-12_
_출처: 아래아한글 빠알리어 입력 도우미 (PDF)_

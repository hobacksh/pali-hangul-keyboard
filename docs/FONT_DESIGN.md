# 한글 빠알리 폰트 설계 문서

## 개요

이 문서는 한글 빠알리 전용 폰트의 설계 철학과 기술 사양을 정의합니다.

**폰트명 (가칭)**: PaliHangul (빠알리한글)

---

## 설계 목표

### 1. 가독성 (Readability)
- **경전 독송용**: 장시간 읽어도 눈이 피로하지 않아야 함
- **명확한 구분**: 비슷한 문자들 (다/따, 나/라) 확실히 구분
- **적절한 자간**: 결합 문자가 겹치지 않도록

### 2. 정확성 (Accuracy)
- **결합 문자 위치**: 장음표, 윗점, 아랫점, 아랫물결 정확히 배치
- **유니코드 표준**: Unicode 15.0 준수
- **크로스 플랫폼**: macOS, Windows, Linux 모두 동일하게 렌더링

### 3. 아름다움 (Aesthetics)
- **조화로운 디자인**: 한글 본연의 미학 유지
- **우아한 곡선**: 부드럽고 차분한 느낌
- **균형잡힌 비율**: 초성, 중성, 종성의 균형

---

## 기술 사양

### 폰트 포맷
- **포맷**: OpenType Font (OTF)
- **이유**: 
  - 65,536개 이상 글리프 지원
  - 고급 타이포그래피 기능 (Ligatures, GPOS/GSUB)
  - 결합 문자(Combining Diacritics) 위치 조정 최적화

### 글리프 목록

#### 필수 글리프 (Phase 1)
1. **한글 기본 음절**: 11,172개 (U+AC00 ~ U+D7A3)
2. **결합 문자 (Combining Diacritics)**: 
   - U+1DC7 (᷇) - 장음표
   - U+302C (〬) - 윗점
   - U+302D (〭) - 아랫점
   - U+032B (̫) - 아랫물결
   - U+034C (͌) - L 로마항소
   - U+1DC3 (᷃) - v 표시
   - U+1DFE (᷾) - y 표시
   - U+033F (̿) - 중복 표시
   - U+0342 (͂) - 대체 중복
   - U+02D5 (˕) - 아랫점 위치 표시
   - U+02D4 (˔) - 윗점 위치 표시

3. **구두점 (Private Use Area)**:
   - U+0F0801 (󰠁) - 빠알리 쉼표
   - U+0F0307 (󰠁) - 빠알리 마침표

4. **기본 라틴/숫자**:
   - a-z, A-Z (52개)
   - 0-9 (10개)
   - .,!?;:'"() 등 기본 기호

#### 확장 글리프 (Phase 2)
- 로마자 빠알리 특수 문자 (ā, ī, ū, ṃ, ṅ, ñ, ḍ, ḷ, ṭ, ṇ)
- 영문 폰트 확장
- 타이 문자 (선택사항)

---

## 디자인 가이드라인

### 참고 폰트
1. **나눔체 (Nanum)**: 결합 문자 위치 조정 양호
2. **끄레도체 (Kredo)**: 빠알리어 전용 최적화 (참고용)
3. **본고딕 (Noto Sans KR)**: 크로스 플랫폼 호환성

### 폰트 스타일
- **굵기 (Weight)**: Regular (400), Bold (700)
- **스타일 (Style)**: Upright (정자체)
- **자간 (Tracking)**: 약간 넓게 (경전 독서 최적화)

### 글리프 디자인 원칙

#### 1. 한글 기본 음절
- **기준 폰트**: 나눔명조/나눔바탕 스타일 차용
- **크기**: 1000 em (표준)
- **Baseline**: 200
- **Cap Height**: 700
- **X-Height**: 500

#### 2. 결합 문자 (Combining Diacritics)

##### 장음표 (᷇ U+1DC7)
- **위치**: 모음 중심 위, 약간 오른쪽
- **크기**: 기본 글자의 20% 크기
- **색상**: 본문과 동일 (검정)

##### 윗점 (〬 U+302C)
- **위치**: 자음 상단 중앙
- **크기**: 원형, 반지름 50 em
- **정렬**: 수직 중앙 정렬

##### 아랫점 (〭 U+302D)
- **위치**: 자음 하단 중앙
- **크기**: 원형, 반지름 50 em
- **정렬**: 수직 중앙 정렬

##### 아랫물결 (̫ U+032B)
- **위치**: 자음 하단, 아랫점보다 아래
- **크기**: 물결 폭 300 em
- **스타일**: 부드러운 곡선 (Bézier)

#### 3. 구두점 (Private Use Area)
- **쉼표 (U+0F0801)**: 한글 쉼표(、) 스타일 + 약간 크게
- **마침표 (U+0F0807)**: 한글 마침표(。) 스타일

---

## OpenType Features

### GPOS (Glyph Positioning)
결합 문자의 정확한 위치 조정:

```
feature mark {
  # 장음표 위치 조정
  pos base [가-힣] <anchor 500 750> mark @장음표 <anchor 0 0>;
  
  # 윗점 위치 조정
  pos base [가-힣] <anchor 500 800> mark @윗점 <anchor 0 0>;
  
  # 아랫점 위치 조정
  pos base [가-힣] <anchor 500 -100> mark @아랫점 <anchor 0 0>;
  
  # 아랫물결 위치 조정
  pos base [가-힣] <anchor 500 -150> mark @아랫물결 <anchor 0 0>;
} mark;
```

### GSUB (Glyph Substitution)
특수한 문자 조합 처리 (필요 시):

```
feature liga {
  # 예: 특정 조합에서 Ligature 생성
  sub 가 ᷇ by 가᷇.liga;
} liga;
```

---

## 개발 로드맵

### Phase 1: 프로토타입 (2주)
- [x] FontForge 설치
- [ ] 기본 한글 10개 글리프 디자인 (가, 나, 다, 라, 마, 바, 사, 아, 자, 카)
- [ ] 결합 문자 4개 디자인 (장음표, 윗점, 아랫점, 아랫물결)
- [ ] GPOS 기능 테스트

### Phase 2: 기본 폰트 (1개월)
- [ ] 한글 기본 음절 완성 (11,172개)
- [ ] 모든 결합 문자 완성 (11개)
- [ ] 구두점 디자인 (2개)
- [ ] 기본 라틴/숫자 (62개)

### Phase 3: 최적화 (2주)
- [ ] 결합 문자 위치 미세 조정
- [ ] 자간/행간 최적화
- [ ] 다양한 환경에서 테스트 (macOS, Windows, Linux)

### Phase 4: Bold 버전 (2주)
- [ ] Bold 글리프 디자인
- [ ] Weight 조정
- [ ] 동일한 결합 문자 위치 유지

---

## 도구 및 환경

### 폰트 편집 도구
- **FontForge**: 메인 개발 도구 (오픈소스, 무료)
- **Glyphs App**: 대안 (유료, macOS 전용)

### 테스트 환경
- **macOS**: Pages, TextEdit
- **Windows**: Word, Notepad
- **웹**: Chrome, Firefox, Safari
- **리눅스**: LibreOffice

### 버전 관리
- **Git**: 폰트 파일 버전 관리
- **GitHub Releases**: OTF 파일 배포

---

## 참고 자료

### 유니코드 표준
- [Unicode 15.0 - Combining Diacritical Marks](https://unicode.org/charts/PDF/U0300.pdf)
- [Unicode Hangul Syllables](https://unicode.org/charts/PDF/UAC00.pdf)

### 폰트 개발 가이드
- [FontForge 튜토리얼](https://fontforge.org/docs/tutorial.html)
- [OpenType Feature 가이드](https://docs.microsoft.com/en-us/typography/opentype/spec/)

### 빠알리어 폰트 참고
- **Kredo Font**: 빠알리어 전용 (Myanmar/Thai/Romanized)
- **Gentium Plus**: SIL 언어학 폰트 (특수 문자 지원)

---

_마지막 업데이트: 2026-02-12_
_상태: 초안 (FontForge 설치 후 작업 시작)_

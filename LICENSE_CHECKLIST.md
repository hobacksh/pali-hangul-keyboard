# LICENSE CHECKLIST (NanumMyeongjo / OFL)

PaliHangul 배포 전 확인용 체크리스트

## 1) 라이선스 파일 동봉
- [ ] 배포 패키지에 `OFL.txt`(또는 동일 내용의 OFL 라이선스 문서) 포함
- [ ] 저장소/배포 페이지에 라이선스 출처 명시

## 2) 수정본 폰트명 분리
- [ ] 수정본은 원본과 다른 폰트명 사용
- [ ] 내부 이름(`fontname/familyname/fullname`)이 원본과 충돌하지 않음
- [ ] 버전별로 고유 이름 유지(캐시/혼동 방지)

## 3) Reserved Font Name(RFN) 확인
- [ ] 원본에 RFN 조건이 있는지 확인
- [ ] RFN이 있으면 수정본에 원본 이름 사용하지 않음

## 4) 재배포 방식
- [ ] 폰트 파일 단독 판매 형태가 아님
- [ ] 앱/웹/프로젝트 결과물 포함 배포는 허용 범위 내
- [ ] 재배포 시 OFL 고지 제거/변조 없음

## 5) 문서화
- [ ] README에 "기반 폰트: NanumMyeongjo (OFL)" 명시
- [ ] 변경 사항(수정/추가한 glyph, GSUB 로직) 기록
- [ ] 배포 버전/빌드 스크립트 경로 기록

## 6) 실무 권장
- [ ] 배포 아카이브에 `LICENSES/` 폴더 생성
- [ ] `LICENSES/OFL-NanumMyeongjo.txt` 포함
- [ ] `NOTICE.md`에 다음 항목 기재
  - 기반 폰트명
  - 라이선스명(OFL)
  - 수정 여부(Modified)
  - 프로젝트 링크

---

## 배포 전 최종 확인 문구(복붙용)

- 기반 서체: NanumMyeongjo
- 라이선스: SIL Open Font License (OFL)
- 본 배포본은 수정본이며, 원본 라이선스 고지를 포함합니다.
- 수정본 폰트명은 원본과 구분되는 이름을 사용합니다.

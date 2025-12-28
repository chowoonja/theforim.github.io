# 서희테마파크 QR 팩

## 구성
- /index.html : 공원 선택
- /parks/서희테마파크/index.html : 서희테마파크 수목조사표(검색 가능)
- /parks/서희테마파크/trees/*.html : 수목 상세(현장 기록 입력 버튼 포함)
- /parks/서희테마파크/qrcodes/*.png : QR 이미지(각 상세페이지 URL)

## 1) 배포
GitHub Pages(또는 기존 theforim.com)로 배포하세요.
- 현재 QR URL 기준: https://theforim.github.io/parks/서희테마파크/trees/<CODE>.html

## 2) Google Form 연결
수목 상세페이지에는 아래 플레이스홀더가 있습니다.
- __PASTE_GOOGLE_FORM_PREFILL_URL_HERE__

Google Form에서 **미리 채우기 링크**를 만든 뒤, 해당 URL로 일괄 교체하면 됩니다.

### 일괄 교체(윈도우)
- VS Code에서 폴더 열기 → 검색(Ctrl+Shift+F) → 플레이스홀더 검색 → Replace All

## 3) 엑셀 업데이트
엑셀의 QR_URL은 배포 주소에 맞춰서 수정하는 것을 권장합니다.

import os
from bs4 import BeautifulSoup

# 템플릿 파일 위치
TEMPLATE_PATH = "parks/안흥유원지/tree_template.html"

# 대상 폴더
TARGET_DIR = "trees"

# 트리 코드 목록 자동 추출 (파일 이름 기반)
tree_files = [f for f in os.listdir(TARGET_DIR) if f.startswith("DT") and f.endswith(".html")]

# 템플릿 불러오기
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template_html = f.read()

for filename in tree_files:
    tree_code = filename.replace(".html", "")

    soup = BeautifulSoup(template_html, "html.parser")

    # 조사번호 부분 수정
    code_tag = soup.find("dd", id="treeCodeText")
    if code_tag:
        code_tag.string = tree_code

    # hidden input 내 treeCode 값 수정
    hidden = soup.find("input", {"id": "treeCode"})
    if hidden:
        hidden["value"] = tree_code

    # QR 이미지 주소 수정
    qr_img = soup.find("img", {"id": "treeQr"})
    if qr_img:
        qr_img["src"] = f"/qr/{tree_code}.png"

    # 출력 파일 저장
    output_path = os.path.join(TARGET_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

print("템플릿 적용 완료!")


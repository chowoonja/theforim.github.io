import os
import pandas as pd
from bs4 import BeautifulSoup

# 안흥유원지에서 쓰던 템플릿 재사용
TEMPLATE_PATH = "parks/안흥유원지/tree_template.html"

# QR이 찾는 위치 = 루트 /trees
TARGET_DIR = "trees"
os.makedirs(TARGET_DIR, exist_ok=True)

# 복하천 엑셀
XLSX = "Bokha2_trees.xlsx"

df = pd.read_excel(XLSX)
df.columns = [str(c).strip() for c in df.columns]

if "수목코드" not in df.columns:
    raise ValueError(f"'수목코드' 컬럼이 없습니다. 현재 컬럼: {list(df.columns)}")

codes = []
for _, row in df.iterrows():
    code = str(row.get("수목코드", "")).strip()
    url  = str(row.get("QR_URL", "")).strip()
    if code and url.startswith("http"):
        codes.append(code)

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template_html = f.read()

for tree_code in codes:
    soup = BeautifulSoup(template_html, "html.parser")

    # 조사번호 표시
    code_tag = soup.find("dd", id="treeCodeText")
    if code_tag:
        code_tag.string = tree_code

    # hidden input
    hidden = soup.find("input", id="treeCode")
    if hidden:
        hidden["value"] = tree_code

    # QR 이미지
    qr_img = soup.find("img", id="qrImage")
    if qr_img:
        qr_img["src"] = f"/qr/{tree_code}.png"
        qr_img["alt"] = f"{tree_code} QR 코드"

    # 페이지 URL
    page_url_tag = soup.find("code", id="pageUrl")
    if page_url_tag:
        page_url_tag.string = f"https://theforim.com/trees/{tree_code}.html"

    # 저장
    out_path = os.path.join(TARGET_DIR, f"{tree_code}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

print(f"✅ 완료: {len(codes)}개 HTML 생성")
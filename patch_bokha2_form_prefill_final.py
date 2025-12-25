import os
import urllib.parse
from bs4 import BeautifulSoup

TREE_DIR = "trees"

# ✅ 구글폼 base URL (viewform까지만)
FORM_BASE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSxxxxxxxxxxxx/viewform"
# ↑ ⚠️ 여기 'xxxxxxxxxxxx' 부분을 네 실제 폼 ID로 바꿔줘
# (Network 캡처에서 viewform? 앞까지 복사하면 됨)

# ✅ 방금 Network에서 찾은 entry 번호
ENTRY_PARK = "entry.939121262"   # 공원명
ENTRY_TREE = "entry.253024248"   # 수목코드

PARK_NAME = "복하천 제2수변공원"

def make_prefill_url(tree_code: str) -> str:
    params = {
        "usp": "pp_url",
        ENTRY_PARK: PARK_NAME,
        ENTRY_TREE: tree_code,
    }
    return FORM_BASE_URL + "?" + urllib.parse.urlencode(params)

patched = 0

for fn in os.listdir(TREE_DIR):
    if not fn.startswith("B2-") or not fn.endswith(".html"):
        continue

    tree_code = fn.replace(".html", "")
    path = os.path.join(TREE_DIR, fn)

    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    target_url = make_prefill_url(tree_code)
    changed = False

    # <a href="..."> 형태
    for a in soup.find_all("a"):
        txt = a.get_text(" ", strip=True)
        if txt == "조사 기록":
            a["href"] = target_url
            a["target"] = "_blank"
            changed = True

    # <button onclick="..."> 형태 대비
    for btn in soup.find_all("button"):
        txt = btn.get_text(" ", strip=True)
        if txt == "조사 기록":
            btn["onclick"] = f"window.open('{target_url}','_blank')"
            changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        patched += 1

print(f"✅ 조사기록 버튼 프리필 링크 적용 완료: {patched}개")

import os
import urllib.parse
from bs4 import BeautifulSoup

TREE_DIR = "trees"

# 구글폼 base URL (entry 없이 viewform 까지)
FORM_BASE = "https://docs.google.com/forms/d/e/1FAIpQLSdgujOIV9bKAUyOAot7AoysT4UWBrrIKkQbIgWirDtZjaapQA/viewform"

ENTRY_PARK = "entry.1291403664"
ENTRY_TREE = "entry.1870322508"
PARK_NAME = "복하천 제2수변공원"

def build_url(tree_code):
    params = {
        ENTRY_PARK: PARK_NAME,
        ENTRY_TREE: tree_code,
    }
    return FORM_BASE + "?" + urllib.parse.urlencode(params)

patched = 0

for fname in os.listdir(TREE_DIR):
    if not fname.startswith("B2-") or not fname.endswith(".html"):
        continue
    tree_code = fname[:-5]
    path = os.path.join(TREE_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    new_link = build_url(tree_code)
    changed = False

    # 모든 <a> 링크에서 docs.google.com/forms 발견되면 교체
    for a in soup.find_all("a", href=True):
        if "docs.google.com/forms" in a["href"]:
            a["href"] = new_link
            a["target"] = "_blank"
            changed = True

    # onclick으로 폼 열면 그 것도 교체
    for tag in soup.find_all(True):
        onclick = tag.get("onclick", "")
        if "docs.google.com/forms" in onclick:
            tag["onclick"] = f"window.open('{new_link}','_blank')"
            changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        patched += 1

print(f"✅ 자동입력 링크 적용 완료: {patched}개")
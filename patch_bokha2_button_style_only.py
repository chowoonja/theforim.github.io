import os
from bs4 import BeautifulSoup

TREE_DIR = "trees"
patched = 0

for fn in os.listdir(TREE_DIR):
    if not fn.startswith("B2-") or not fn.endswith(".html"):
        continue

    path = os.path.join(TREE_DIR, fn)
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    changed = False

    # a, button 모두 대상
    for btn in soup.find_all(["a", "button"]):
        txt = btn.get_text(" ", strip=True)
        if txt == "조사 기록":
            cls = btn.get("class", [])
            if "btn-old-record" not in cls:
                cls.append("btn-old-record")
                btn["class"] = cls
                changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        patched += 1

print(f"✅ 옛 스타일 버튼 클래스 적용 완료: {patched}개")
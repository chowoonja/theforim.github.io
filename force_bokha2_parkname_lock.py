import os, re

TREES_DIR = os.path.join("parks", "bokha2", "trees")
PARK_NAME = "복하천 제2수변공원"

def patch(html: str) -> str:
    out = html

    # (A) 공원명 input을 강제 고정값 + readonly로 만들기
    # 기존 <input id="parkName" ...> 태그를 통째로 교체
    out = re.sub(
        r'<input\b[^>]*\bid\s*=\s*"parkName"[^>]*>',
        f'<input id="parkName" type="text" value="{PARK_NAME}" readonly '
        f'style="width:200px; margin:6px; background:#fff; border:1px solid #ddd; border-radius:6px;"/>',
        out,
        flags=re.IGNORECASE
    )

    # (B) loadHeaderInfo()가 parkName을 빈칸으로 덮어쓰는 걸 막기:
    # parkName 라인 자체를 "항상 PARK_NAME"으로 강제
    out = re.sub(
        r'document\.getElementById\("parkName"\)\.value\s*=\s*localStorage\.getItem\([^)]*\)\s*\|\|\s*""\s*;',
        f'document.getElementById("parkName").value = "{PARK_NAME}";',
        out,
        flags=re.IGNORECASE
    )

    # (C) 키가 파일별로 park-<code> 라면, 페이지 로딩 시에도 무조건 저장해서 다음에도 안 비게
    # saveHeaderInfo() 안에 park 저장 부분을 PARK_NAME으로 강제
    out = re.sub(
        r'localStorage\.setItem\(\s*KEY_PARK\s*,\s*document\.getElementById\("parkName"\)\.value\s*\)\s*;',
        f'localStorage.setItem(KEY_PARK, "{PARK_NAME}");',
        out,
        flags=re.IGNORECASE
    )

    return out

def main():
    changed = 0
    total = 0
    for fn in os.listdir(TREES_DIR):
        if not fn.lower().endswith(".html"):
            continue
        total += 1
        path = os.path.join(TREES_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            old = f.read()
        new = patch(old)
        if new != old:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
            changed += 1

    print(f"✅ bokha2 공원명 하드락 완료 | 변경 {changed} | 총 {total}")

if __name__ == "__main__":
    main()
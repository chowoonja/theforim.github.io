import os

TREES_DIR = os.path.join("parks", "bokha2", "trees")

OLD = "// DT0001 → DT코드 추출"
NEW = "// 파일명에서 수목 코드 추출"

def main():
    changed = 0
    total = 0

    for fn in os.listdir(TREES_DIR):
        if not fn.lower().endswith(".html"):
            continue
        total += 1
        path = os.path.join(TREES_DIR, fn)

        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        if OLD in html:
            html = html.replace(OLD, NEW)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(html)
            changed += 1

    print(f"✅ bokha2 주석 정리 완료 | 변경 {changed} | 총 {total}")

if __name__ == "__main__":
    main()
import os
import pandas as pd
from pathlib import Path

# ✅ 입력 엑셀 파일명 (루트에 있는 파일)
XLSX = "Bokha2_trees.xlsx"

# ✅ 출력 폴더 (루트의 trees)
OUT_DIR = Path("trees")
OUT_DIR.mkdir(exist_ok=True)

# ✅ 템플릿 생성 함수(기존 파일을 그대로 사용)
from apply_tree_template import render_tree_html  # apply_tree_template.py 안에 이 함수가 있다고 가정

def main():
    df = pd.read_excel(XLSX)
    df.columns = [str(c).strip() for c in df.columns]

    # 컬럼명 확인(복하천 엑셀은 수목코드 사용)
    required = ["관리번호", "수목코드", "QR_URL"]
    for c in required:
        if c not in df.columns:
            raise ValueError(f"엑셀에 '{c}' 컬럼이 없습니다. 현재 컬럼: {list(df.columns)}")

    ok = 0
    for _, row in df.iterrows():
        code = str(row.get("수목코드", "")).strip()
        url  = str(row.get("QR_URL", "")).strip()

        # URL이 비어있거나 코드가 없으면 스킵
        if not code or not url.startswith("http"):
            continue

        # 템플릿에 넣을 데이터(필요하면 컬럼 더 추가 가능)
        data = {
            "park_name": "복하천제2수변공원",
            "관리번호": str(row.get("관리번호","")).strip(),
            "수목코드": code,
            "QR_URL": url,
            "수종명": str(row.get("수종명","")).strip(),
            "규격": str(row.get("규격","")).strip(),
            "성상": str(row.get("성상","")).strip(),
        }

        html = render_tree_html(data)  # apply_tree_template.py의 함수가 HTML 문자열을 돌려줘야 함
        out_path = OUT_DIR / f"{code}.html"
        out_path.write_text(html, encoding="utf-8")
        ok += 1

    print(f"✅ 생성 완료: {ok}개 HTML → {OUT_DIR.resolve()}")

if __name__ == "__main__":
    main()
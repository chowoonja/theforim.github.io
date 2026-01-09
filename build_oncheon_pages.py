# -*- coding: utf-8 -*-
import os
import re
import pandas as pd

PARK_NAME = "온천공원"

FORM_BASE = "https://docs.google.com/forms/d/1gGJU8_ifBXOKEjuSEzPnZjvQ_mnBpHECPtf-GlAVDYM/viewform"
ENTRY_PARK = "entry.939121262"
ENTRY_CODE = "entry.253024248"

EXCEL_PATH = "Oncheon_MASTER_trees.xlsx"   # 레포 루트에 두면 됨
SHEET_NAME = "Trees"                       # 우리가 만든 마스터 시트명
CODE_COL = "수목코드"

OUT_DIR = os.path.join(".", "trees")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{code} · {park} · THE FORIM</title>
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <main class="container">
    <div class="logo-mark">THE FORIM</div>
    <h1>{park}</h1>
    <p>수목코드: <strong id="code">{code}</strong></p>

    <button id="goForm">현장기록 입력</button>
  </main>

  <script>
    const FORM_BASE = "{form_base}";
    const ENTRY_PARK = "{entry_park}";
    const ENTRY_CODE = "{entry_code}";
    const PARK_NAME = "{park}";
    const CODE = "{code}";

    document.getElementById("goForm").onclick = () => {{
      const url =
        `${{FORM_BASE}}?${{ENTRY_PARK}}=${{encodeURIComponent(PARK_NAME)}}&` +
        `${{ENTRY_CODE}}=${{encodeURIComponent(CODE)}}`;
      window.location.href = url;
    }};
  </script>
</body>
</html>
"""

def sanitize_code(code: str) -> str:
    code = str(code).strip()
    code = code.replace("\u00A0", " ")
    return code

def is_valid_code(code: str) -> bool:
    # 예: O2-DTJP016, O1-ETPS015 등 대문자/숫자/하이픈 형식
    return bool(re.match(r"^[A-Z]\d-[A-Z0-9]{2,10}\d{3}$", code))

def main():
    if not os.path.exists(EXCEL_PATH):
        raise FileNotFoundError(f"엑셀 파일을 찾을 수 없음: {EXCEL_PATH} (레포 루트에 두거나 EXCEL_PATH 수정)")

    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

    if CODE_COL not in df.columns:
        raise KeyError(f"'{CODE_COL}' 컬럼이 없음. 현재 컬럼: {list(df.columns)}")

    codes = []
    for v in df[CODE_COL].tolist():
        if pd.isna(v):
            continue
        c = sanitize_code(v)
        if not c:
            continue
        codes.append(c)

    # 중복 제거(순서 유지)
    seen = set()
    unique = []
    for c in codes:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    created = 0
    skipped = 0

    for code in unique:
        if not is_valid_code(code):
            # 형식이 다른 값이 섞였을 때 안전하게 스킵
            skipped += 1
            continue

        path = os.path.join(OUT_DIR, f"{code}.html")
        html = HTML_TEMPLATE.format(
            code=code,
            park=PARK_NAME,
            form_base=FORM_BASE,
            entry_park=ENTRY_PARK,
            entry_code=ENTRY_CODE
        )

        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        created += 1

    print(f"완료: 생성 {created}개 / 스킵 {skipped}개")
    print(f"폴더: {os.path.abspath(OUT_DIR)}")

if __name__ == "__main__":
    main()
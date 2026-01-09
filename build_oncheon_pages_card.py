# -*- coding: utf-8 -*-
import os
import re
import pandas as pd

# ===== 설정 =====
PARK_NAME = "온천공원"

FORM_BASE  = "https://docs.google.com/forms/d/1gGJU8_ifBXOKEjuSEzPnZjvQ_mnBpHECPtf-GlAVDYM/viewform"
ENTRY_PARK = "entry.939121262"
ENTRY_CODE = "entry.253024248"

EXCEL_PATH = "Oncheon_MASTER_trees.xlsx"
SHEET_NAME = "Trees"
CODE_COL   = "수목코드"

OUT_DIR = os.path.join(".", "trees")

# ===== 카드형 HTML (복하천 스타일) =====
HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{code} · {park} · THE FORIM</title>
  <link rel="stylesheet" href="/assets/style.css">
  <style>
    .container {{ max-width: 980px; margin: 0 auto; padding: 24px; }}
    .brandbar {{ margin: 10px 0 16px; }}
    .brandbar .logo {{ font-weight: 800; letter-spacing: 0.08em; }}
    .hero {{ color:#fff; background:#0b0f16; padding:22px 24px; border-radius:14px; }}
    .hero h1 {{ margin:0; font-size:22px; }}
    .hero .sub {{ margin-top:6px; opacity:.9; font-size:14px; }}
    .card {{ background:#fff; border-radius:18px; padding:18px 18px 14px;
            box-shadow:0 6px 18px rgba(0,0,0,0.06); margin-top:18px; }}
    table.meta {{ width:100%; border-collapse:collapse; }}
    table.meta th {{ text-align:left; width:18%; padding:10px; color:#333; font-weight:700; }}
    table.meta td {{ padding:10px; color:#111; }}
    table.meta tr {{ border-bottom:1px solid #eee; }}
    table.meta tr:last-child {{ border-bottom:none; }}
    .btnrow {{ display:flex; gap:10px; margin-top:14px; }}
    .btn {{ display:inline-block; padding:10px 14px; border-radius:10px; border:1px solid #111;
           background:#111; color:#fff; font-weight:700; text-decoration:none; cursor:pointer; }}
    .btn.secondary {{ background:#fff; color:#111; }}
    .hint {{ margin-top:10px; font-size:12px; color:#666; }}
    .section-title {{ margin:14px 0 6px; font-weight:800; }}
    .note {{ white-space:pre-wrap; color:#111; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="brandbar"><div class="logo">THE FORIM</div></div>

    <div class="hero">
      <h1>수목 상세 정보</h1>
      <div class="sub">조사번호: {code} · {park}</div>
    </div>

    <div class="card">
      <table class="meta">
        <tr><th>공원명</th><td>{park}</td><th>수목코드</th><td>{code}</td></tr>
        <tr><th>수종명</th><td>{species}</td><th>성상</th><td>{type}</td></tr>
        <tr><th>규격</th><td>{spec}</td><th>단위</th><td>{unit}</td></tr>
        <tr><th>수량(설계)</th><td>{qty_plan}</td><th>수량(현장)</th><td>{qty_field}</td></tr>
        <tr><th>관리번호</th><td>{manage_no}</td><th>사진ID</th><td>{photo_id}</td></tr>
      </table>

      <div class="btnrow">
        <button class="btn" id="goForm">현장기록 입력</button>
        <a class="btn secondary" id="qrPng" href="/qr/{code}.png" target="_blank" rel="noopener">QR PNG</a>
      </div>

      <div class="hint">※ 버튼을 누르면 Google Form이 열리고, 공원명/수목코드가 자동 입력됩니다.</div>

      <div class="section-title">필요 관리 내용</div>
      <div class="note">{need}</div>
    </div>
  </div>

  <script>
    const FORM_BASE  = "{form_base}";
    const ENTRY_PARK = "{entry_park}";
    const ENTRY_CODE = "{entry_code}";
    const PARK_NAME  = "{park}";
    const CODE       = "{code}";

    document.getElementById("goForm").onclick = () => {{
      const url = `${{FORM_BASE}}?${{ENTRY_PARK}}=${{encodeURIComponent(PARK_NAME)}}&${{ENTRY_CODE}}=${{encodeURIComponent(CODE)}}`;
      window.location.href = url;
    }};
  </script>
</body>
</html>
"""

# ===== 유틸 =====
def clean(v):
    if v is None:
        return ""
    s = str(v).strip()
    if s.lower() == "nan":
        return ""
    return s

def pick(row, candidates):
    """row에서 후보 컬럼명 중 먼저 존재하는 값을 반환"""
    for c in candidates:
        if c in row and pd.notna(row[c]):
            return clean(row[c])
    return ""

def is_valid_code(code: str) -> bool:
    return bool(re.match(r"^[A-Z]\d-[A-Z0-9]{2,10}\d{3}$", code))

def main():
    if not os.path.exists(EXCEL_PATH):
        raise FileNotFoundError(f"엑셀 없음: {EXCEL_PATH}")

    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    if CODE_COL not in df.columns:
        raise KeyError(f"'{CODE_COL}' 컬럼 없음. 현재 컬럼: {list(df.columns)}")

    created = 0
    skipped = 0

    for _, row in df.iterrows():
        code = clean(row.get(CODE_COL, ""))
        if not code or not is_valid_code(code):
            skipped += 1
            continue

        data = {
            "park": PARK_NAME,
            "code": code,
            "species": pick(row, ["수종명","수목명","수종","수목이름","tree_name","species"]),
            "type":    pick(row, ["성상","형태","수형","type"]),
            "spec":    pick(row, ["규격","규격/수고흉고","규격(수고*흉고)","spec"]),
            "unit":    pick(row, ["단위","unit"]),
            "qty_plan":  pick(row, ["수량(설계)","설계수량","수량_설계","qty_plan"]),
            "qty_field": pick(row, ["수량(현장)","현장수량","수량_현장","qty_field"]),
            "manage_no": pick(row, ["관리번호","관리No","관리번호(현장)","manage_no"]),
            "photo_id":  pick(row, ["사진ID","사진Id","사진아이디","photo_id"]),
            "need":      pick(row, ["필요 관리 내용","관리내용","필요관리","비고","need"]),
            "form_base": FORM_BASE,
            "entry_park": ENTRY_PARK,
            "entry_code": ENTRY_CODE,
        }

        path = os.path.join(OUT_DIR, f"{code}.html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(HTML.format(**data))
        created += 1

    print(f"완료: 생성 {created}개 / 스킵 {skipped}개")
    print(f"폴더: {os.path.abspath(OUT_DIR)}")

if __name__ == "__main__":
    main()
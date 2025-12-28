import os, re

TREES_DIR = os.path.join("parks", "bokha2", "trees")

FORM_ID = "1FAIpQLSdgujOIV9bKAUyOAot7AoysT4UWBrrIKkQbIgWirDtZjaapQA"
FORM_BASE = f"https://docs.google.com/forms/d/e/{FORM_ID}/viewform?usp=pp_url"

ENTRY_PARK_NAME   = "entry.1291403664"
ENTRY_SURVEYOR    = "entry.2066724387"
ENTRY_SURVEY_DATE = "entry.2016295766"
ENTRY_TREE_CODE   = "entry.1870322508"

def extract_code_from_filename(fn: str) -> str:
    base = os.path.splitext(fn)[0]
    return base

def patch_form_js(html: str) -> str:
    out = html

    # 1) FORM_BASE_URL을 usp=pp_url 포함된 것으로 고정
    out = re.sub(
        r"const\s+FORM_BASE_URL\s*=\s*['\"][^'\"]*viewform[^'\"]*['\"];",
        f"const FORM_BASE_URL = '{FORM_BASE}';",
        out
    )

    # 혹시 공백/이중공백 버전도 잡기
    out = re.sub(
        r"const\s+FORM_BASE_URL\s*=\s*['\"][^'\"]*['\"];",
        lambda m: m.group(0) if "FORM_BASE_URL" not in m.group(0) else f"const FORM_BASE_URL = '{FORM_BASE}';",
        out
    )

    # 2) finalUrl 만들 때 '?' → '&' 로 (base에 이미 ?usp=pp_url 있으므로)
    out = out.replace("const finalUrl = FORM_BASE_URL + '?' + params.toString();",
                      "const finalUrl = FORM_BASE_URL + '&' + params.toString();")

    return out

def patch_qr_block(html: str, code: str) -> str:
    out = html

    # DT0001 잔재(가장 문제되는 부분) 직접 제거
    out = out.replace('/qr/DT0001.png', f'/qr/{code}.png')
    out = re.sub(r'alt\s*=\s*"DT0001\s*QR\s*코드"', f'alt="{code} QR 코드"', out, flags=re.IGNORECASE)

    # QR 이미지가 이미 있어도 안전하게 alt/src를 코드로 통일
    out = re.sub(
        r'(<img\b[^>]*\balt\s*=\s*")[^"]*(")([^>]*\bsrc\s*=\s*")[^"]*(")',
        lambda m: f'{m.group(1)}{code} QR 코드{m.group(2)}{m.group(3)}/qr/{code}.png{m.group(4)}',
        out,
        flags=re.IGNORECASE
    )

    # "파일 위치" 표기 통일
    out = re.sub(
        r'파일 위치:\s*<code>/qr/[^<]+</code>',
        f'파일 위치: <code>/qr/{code}.png</code>',
        out
    )

    # "페이지 URL" 표기 통일 (bokha2 경로)
    out = re.sub(
        r'페이지 URL:\s*<code>https?://theforim\.com/[^<]+</code>',
        f'페이지 URL: <code>https://theforim.com/parks/bokha2/trees/{code}.html</code>',
        out,
        flags=re.IGNORECASE
    )

    return out

def patch_openFormBtn_href(html: str, code: str) -> str:
    # href는 예비용이지만, 일관되게 만들어 둠
    from urllib.parse import quote
    park_q = quote("복하천 제2수변공원", safe="")
    code_q = quote(code, safe="")
    href = f"{FORM_BASE}&{ENTRY_PARK_NAME}={park_q}&{ENTRY_TREE_CODE}={code_q}"

    def repl(match):
        tag = match.group(0)
        tag2 = re.sub(r'href\s*=\s*"[^"]*"', f'href="{href}"', tag, flags=re.IGNORECASE)
        return tag2

    new_html, _ = re.subn(
        r'<a\b[^>]*\bid\s*=\s*"openFormBtn"[^>]*>',
        repl,
        html,
        flags=re.IGNORECASE
    )
    return new_html

def main():
    if not os.path.isdir(TREES_DIR):
        raise SystemExit(f"[ERROR] 폴더를 찾을 수 없음: {TREES_DIR}")

    changed = 0
    total = 0

    for fn in os.listdir(TREES_DIR):
        if not fn.lower().endswith(".html"):
            continue
        total += 1
        code = extract_code_from_filename(fn)
        path = os.path.join(TREES_DIR, fn)

        with open(path, "r", encoding="utf-8") as f:
            old = f.read()

        new = old
        new = patch_form_js(new)
        new = patch_qr_block(new, code)
        new = patch_openFormBtn_href(new, code)

        if new != old:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
            changed += 1

    print(f"✅ bokha2 최종 일괄 패치 완료 | 변경 {changed} | 총 {total}")
    print(f"대상 폴더: {TREES_DIR}")

if __name__ == "__main__":
    main()
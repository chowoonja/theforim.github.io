import pandas as pd, html, pathlib

root = pathlib.Path('.')
xlsx = root / 'Oncheon_MASTER_trees.xlsx'
out_html = root / 'parks/oncheonpark/trees/index.html'

df = pd.read_excel(xlsx, sheet_name='Trees')
df = df[df['수목코드'].notna()]

items = list(zip(df['수목코드'].astype(str), df['수종명'].astype(str)))

lines = []
lines.append('<!doctype html>')
lines.append('<html lang="ko"><head>')
lines.append('<meta charset="utf-8">')
lines.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
lines.append('<title>온천공원 수목목록  THE FORIM</title>')
lines.append('<link rel="stylesheet" href="/assets/style.css">')
lines.append('</head><body>')
lines.append('<header class="site-header"><div class="logo-mark">THE FORIM</div>')
lines.append(f'<div class="brand-text"><h1>온천공원 수목목록</h1><p>총 {len(items)}주</p></div></header>')
lines.append('<main class="container"><section class="card"><ul>')

for code, name in items:
    lines.append(f'<li><a href="/parks/oncheonpark/trees/{html.escape(code)}.html">{html.escape(code)}  {html.escape(name)}</a></li>')

lines.append('</ul></section></main></body></html>')

out_html.write_text('\n'.join(lines), encoding='utf-8')
print('OK: wrote', len(items), 'items')

import re

with open('sell.html', 'r', encoding='utf-8') as f:
    sell_html = f.read()

# 1. Reduce padding between text and header
sell_html = sell_html.replace('.sell-hero{max-width:1280px;margin:30px auto 30px;', '.sell-hero{max-width:1280px;margin:10px auto 20px;')

# 2. Separate cards
sell_html = sell_html.replace(
    '.portal-box{background:var(--white);border-radius:16px;border:1px solid var(--border);box-shadow:0 10px 40px rgba(0,0,0,0.03);display:grid;grid-template-columns:280px 1fr 280px;min-height:600px;}',
    '.portal-box{display:grid;grid-template-columns:280px 1fr 280px;gap:24px;min-height:600px;}'
)

sell_html = sell_html.replace(
    '.p-left{padding:40px 30px;border-right:1px solid var(--border);background:#FAFAFB;border-top-left-radius:16px;border-bottom-left-radius:16px;}',
    '.p-left{padding:40px 30px;background:var(--white);border-radius:16px;border:1px solid var(--border);box-shadow:0 10px 40px rgba(0,0,0,0.03);}'
)

sell_html = sell_html.replace(
    '.p-mid{padding:40px 60px;}',
    '.p-mid{padding:40px 60px;background:var(--white);border-radius:16px;border:1px solid var(--border);box-shadow:0 10px 40px rgba(0,0,0,0.03);}'
)

sell_html = sell_html.replace(
    '.p-right{padding:40px 30px;background:#FFFBF0;border-left:1px solid #FEF3C7;border-top-right-radius:16px;border-bottom-right-radius:16px;}',
    '.p-right{padding:40px 30px;background:#FFFBF0;border-radius:16px;border:1px solid #FEF3C7;box-shadow:0 10px 40px rgba(0,0,0,0.03);}'
)

# 3. "dont attach footer" -> Remove footer from this page
footer_match = re.search(r'<footer class="footer">.*?</footer>', sell_html, re.DOTALL)
if footer_match:
    sell_html = sell_html.replace(footer_match.group(0), '')

# Also remove the flex from body so it doesn't try to stretch
sell_html = sell_html.replace('body{font-family:\'Inter\',sans-serif;color:var(--text);background:var(--silver); display:flex; flex-direction:column; min-height:100vh;}', 'body{font-family:\'Inter\',sans-serif;color:var(--text);background:var(--silver);}')

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(sell_html)

print("Modifications complete.")

import re

with open('login.html', 'r', encoding='utf-8') as f:
    login_html = f.read()

html_start = login_html.find('<div class="tabs">')
html_end = login_html.find('</div>\\n    </div>\\n  </div>\\n</div>', html_start)
html_content = login_html[html_start:html_end].strip()

# Inject HTML into index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

pattern = re.compile(r'asBody\.innerHTML = \\s*<div class="as-login-view">.*?</div>\\s*;', re.DOTALL)
html_content_escaped = html_content.replace('', '\\\\').replace('$', '\\\\$')
new_block = f'asBody.innerHTML = \\n{html_content_escaped}\\n;'

index_html = pattern.sub(new_block, index_html)

# Also change asTitle
index_html = index_html.replace("asTitle.textContent = 'Welcome to Market Guru HP';", "asTitle.textContent = 'Login or Register';")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print('Replaced HTML block')

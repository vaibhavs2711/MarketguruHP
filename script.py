import re
with open('login.html', 'r', encoding='utf-8') as f: login_html = f.read()
html_start = login_html.find('<div class="tabs">')
html_end = login_html.find('</div>\n    </div>\n  </div>\n</div>', html_start)
html_content = login_html[html_start:html_end].strip()
with open('index.html', 'r', encoding='utf-8') as f: index_html = f.read()
old_block = '          <div class="as-login-view">\n            <p>Login to manage your car listings, view analytics, and save your favourite cars.</p>\n            <a href="login.html" class="as-btn">Login / Register</a>\n          </div>'
if old_block in index_html:
    index_html = index_html.replace(old_block, html_content)
    index_html = index_html.replace("asTitle.textContent = 'Welcome to Market Guru HP';", "asTitle.textContent = 'Login or Register';")
    with open('index.html', 'w', encoding='utf-8') as f: f.write(index_html)
    print('Replaced HTML block')
else: print('Block not found')

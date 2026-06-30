import re

with open('login.html', 'r', encoding='utf-8') as f:
    login_html = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# 1. Extract CSS
css_start = login_html.find('/* TABS */')
css_end = login_html.find('.login-footer {')
if css_start == -1 or css_end == -1:
    print('Failed to find CSS boundaries')
css_content = login_html[css_start:css_end].strip()
css_content = css_content.replace('.form-panel.active {\\n    display: block;\\n  }', '.form-panel.active {\\n    display: block;\\n  }\\n\\n  .account-sidebar .form-panel {\\n    padding-bottom: 20px;\\n  }')


# 2. Extract HTML
html_start = login_html.find('<div class="tabs">')
html_end = login_html.find('<!-- FULL WIDTH BOTTOM FOOTER -->')
if html_start == -1 or html_end == -1:
    print('Failed to find HTML boundaries')
html_content = login_html[html_start:html_end].strip()
# Remove the closing divs for login-card, login-right-section, etc.
# The html_end is before FULL WIDTH BOTTOM FOOTER, let's just find the end of panel-register.
html_end = login_html.find('</div>\\n    </div>\\n  </div>\\n</div>', html_start)
if html_end != -1:
    html_content = login_html[html_start:html_end].strip()

# 3. Extract JS
js_start = login_html.find('function switchTab(tab) {')
js_end = login_html.find('// Update profile logic')
if js_end == -1:
    js_end = login_html.find('</script>', js_start)

js_content = login_html[js_start:js_end].strip()
# Remove any closing script tag if included accidentally
js_content = js_content.replace('</script>', '')

# Now inject into index.html

# Inject CSS before </style>
css_injection = f"\\n\\n{css_content}\\n"
index_html = index_html.replace('</style>', css_injection + '</style>', 1)

# Inject JS before </script> at the end
js_injection = f"\\n\\n{js_content}\\n"
# Find the last </script> in body
last_script_idx = index_html.rfind('</script>\\n</body>')
if last_script_idx != -1:
    index_html = index_html[:last_script_idx] + js_injection + index_html[last_script_idx:]
else:
    # try just the last </script>
    last_script_idx = index_html.rfind('</script>')
    index_html = index_html[:last_script_idx] + js_injection + index_html[last_script_idx:]


# Inject HTML into renderSidebar
html_content_escaped = html_content.replace('', '\\\\').replace('$', '\\\\$')
# We need to replace the else block in renderSidebar
old_else_block = '''      } else {
        asTitle.textContent = 'Welcome to Market Guru HP';
        asBody.innerHTML = 
          <div class="as-login-view">
            <p>Login to manage your car listings, view analytics, and save your favourite cars.</p>
            <a href="login.html" class="as-btn">Login / Register</a>
          </div>
        ;
      }'''

new_else_block = f'''      }} else {{
        asTitle.textContent = 'Login or Register';
        asBody.innerHTML = 
{html_content_escaped}
        ;
      }}'''

index_html = index_html.replace(old_else_block, new_else_block)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print('Successfully injected login logic into index.html')

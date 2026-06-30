import re

with open('login.html', 'r', encoding='utf-8') as f:
    login_html = f.read()

with open('buy-cars.html', 'r', encoding='utf-8') as f:
    buy_html = f.read()

# 1. Extract CSS
css_start = login_html.find('/* TABS */')
css_end = login_html.find('.login-footer {')
if css_start == -1 or css_end == -1:
    print('Failed to find CSS boundaries')
css_content = login_html[css_start:css_end].strip()
css_content = css_content.replace('.form-panel.active {\n    display: block;\n  }', '.form-panel.active {\n    display: block;\n  }\n\n  .account-sidebar .form-panel {\n    padding-bottom: 20px;\n  }')

# 2. Extract HTML
html_start = login_html.find('<div class="tabs">')
html_end = login_html.find('<!-- FULL WIDTH BOTTOM FOOTER -->')
if html_start == -1 or html_end == -1:
    print('Failed to find HTML boundaries')
html_end = login_html.find('</div>\n    </div>\n  </div>\n</div>', html_start)
html_content = login_html[html_start:html_end].strip()

# 3. Extract JS
js_start = login_html.find('function switchTab(tab) {')
js_end = login_html.find('// Update profile logic')
if js_end == -1:
    js_end = login_html.find('</script>', js_start)

js_content = login_html[js_start:js_end].strip()
js_content = js_content.replace('</script>', '')

# 4. Modify buy-cars.html
# Inject CSS
css_injection = f'\n\n{css_content}\n'
if '/* TABS */' not in buy_html:
    buy_html = buy_html.replace('</style>', css_injection + '</style>', 1)

# Inject JS before last </script>
js_injection = f'\n\n{js_content}\n'
if 'function switchTab(tab)' not in buy_html:
    last_script_idx = buy_html.rfind('</script>\n</body>')
    if last_script_idx != -1:
        buy_html = buy_html[:last_script_idx] + js_injection + buy_html[last_script_idx:]
    else:
        last_script_idx = buy_html.rfind('</script>')
        buy_html = buy_html[:last_script_idx] + js_injection + buy_html[last_script_idx:]

# 5. Fix checkLoginState overwrite
nav_action_block = """  if (navActions) {
    if (currentUser) {
      let initials = '👤';
      try {
        const userObj = JSON.parse(currentUser);
        const name = userObj.name || '';
        if (name) {
          const parts = name.split(' ');
          if (parts.length > 1) {
            initials = (parts[0][0] + parts[1][0]).toUpperCase();
          } else {
            initials = name.substring(0, 2).toUpperCase();
          }
        }
      } catch(e) {}
      navActions.innerHTML = `
        <a href="customer-dashboard.html" title="My Profile" style="text-decoration:none; display:block;">
          <div style="width: 42px; height: 42px; border-radius: 50%; background: rgba(249, 115, 22, 0.15); border: 2px solid var(--primary); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: var(--primary); text-transform: uppercase; transition: all 0.2s;">
            ${initials}
          </div>
        </a>
      `;
    } else {
      navActions.innerHTML = `
        <a href="login.html" class="nav-login" id="nav-login-link">
          <button class="btn-login" id="nav-login-btn">
            Login / Register
          </button>
        </a>
      `;
    }
  }"""
buy_html = buy_html.replace(nav_action_block, '  // Removed navActions overwrite for sliding sidebar')

# 6. Fix renderSidebar inside buy-cars.html
initials_injection = """
        let initials = '👤';
        try {
          const parts = currentUser.split(' ');
          if (parts.length > 1) {
            initials = (parts[0][0] + parts[1][0]).toUpperCase();
          } else {
            initials = currentUser.substring(0, 2).toUpperCase();
          }
        } catch (e) { }
        if (accountBtn) {
          accountBtn.innerHTML = initials;
          accountBtn.style.fontWeight = '700';
          accountBtn.style.fontSize = '16px';
        }
"""
buy_html = buy_html.replace("if (currentUser && currentUser !== 'Guest User') {", "if (currentUser && currentUser !== 'Guest User') {" + initials_injection)

# Replace the else block with form
html_content_escaped = html_content.replace('\\', '\\\\')
old_else_block = """      } else {
        asTitle.textContent = 'Welcome to Market Guru HP';
        asBody.innerHTML = `
          <div class="as-login-view">
            <p>Login to manage your car listings, view analytics, and save your favourite cars.</p>
            <a href="login.html" class="as-btn">Login / Register</a>
          </div>
        `;
      }"""
new_else_block = f"""      }} else {{
        asTitle.textContent = 'Login or Register';
        asBody.innerHTML = `
{html_content_escaped}
        `;
      }}"""

buy_html = buy_html.replace(old_else_block, new_else_block)

with open('buy-cars.html', 'w', encoding='utf-8') as f:
    f.write(buy_html)
print('Injected!')

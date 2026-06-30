import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('buy-cars.html', 'r', encoding='utf-8') as f:
    buy_html = f.read()

# 1. Extract renderSidebar from index.html
rs_start = index_html.find('function renderSidebar() {')
rs_end = index_html.find('  });\n\n  //', rs_start)
if rs_end == -1:
    rs_end = index_html.find('  });\n', rs_start)

if rs_start == -1 or rs_end == -1:
    print('Failed to find renderSidebar in index.html')
else:
    # Need to include the closing '  });' for the event listener?
    # Wait, renderSidebar ends with '}'
    # Let's find the closing brace of renderSidebar
    # Actually, in index.html it is:
    # function renderSidebar() { ... }
    rs_end = index_html.find('\n      function switchTab', rs_start)
    if rs_end == -1:
        rs_end = index_html.find('    // ── Check Login State', rs_start)
    
    if rs_end != -1:
        # Go back to the closing brace
        rs_end = index_html.rfind('}', rs_start, rs_end) + 1
        
        index_rs = index_html[rs_start:rs_end]
        
        # Now find renderSidebar in buy-cars.html
        buy_rs_start = buy_html.find('function renderSidebar() {')
        buy_rs_end = buy_html.find('\n    }', buy_rs_start) + 6 # find the closing brace
        if buy_rs_start != -1 and buy_rs_end != -1:
            buy_html = buy_html[:buy_rs_start] + index_rs + buy_html[buy_rs_end:]
            print('Replaced renderSidebar')
        else:
            print('Failed to find renderSidebar in buy-cars.html')

# 2. Fix checkLoginState in buy-cars.html
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

# 3. Extract CSS and JS from login.html and inject
with open('login.html', 'r', encoding='utf-8') as f:
    login_html = f.read()

css_start = login_html.find('/* TABS */')
css_end = login_html.find('.login-footer {')
if css_start != -1 and css_end != -1:
    css_content = login_html[css_start:css_end].strip()
    css_content = css_content.replace('.form-panel.active {\n    display: block;\n  }', '.form-panel.active {\n    display: block;\n  }\n\n  .account-sidebar .form-panel {\n    padding-bottom: 20px;\n  }')
    
    if '/* TABS */' not in buy_html:
        buy_html = buy_html.replace('</style>', '\\n\\n' + css_content + '\\n</style>', 1)
        print('Injected CSS')

# We also need the JS (switchTab etc) which was injected by inject_login.py into index.html
# Let's extract it from index.html since it's already perfectly formed there!
js_start = index_html.find('function switchTab(tab)')
js_end = index_html.find('</script>\n</body>')
if js_end == -1:
    js_end = index_html.find('</script>\n</html>')
if js_end == -1:
    js_end = index_html.rfind('</script>')

if js_start != -1 and js_end != -1:
    js_content = index_html[js_start:js_end].strip()
    
    if 'function switchTab(tab)' not in buy_html:
        # insert right before the LAST script tag
        last_script_idx = buy_html.rfind('</script>\n</body>')
        if last_script_idx == -1:
            last_script_idx = buy_html.rfind('</script>')
            
        buy_html = buy_html[:last_script_idx] + '\\n\\n' + js_content + '\\n' + buy_html[last_script_idx:]
        print('Injected JS')

with open('buy-cars.html', 'w', encoding='utf-8') as f:
    f.write(buy_html)
print('Done!')

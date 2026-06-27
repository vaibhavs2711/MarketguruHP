import re

with open('buy-cars.html', 'r', encoding='utf-8') as f:
    buy_cars_html = f.read()

# Extract Navbar
nav_match = re.search(r'<nav class="navbar">.*?</nav>', buy_cars_html, re.DOTALL)
navbar_html = nav_match.group(0)
# Fix Sell Vehicles active class
navbar_html = navbar_html.replace('<a href="buy-cars.html" class="active">Buy Vehicle</a>', '<a href="buy-cars.html">Buy Vehicle</a>')
navbar_html = navbar_html.replace('<a href="sell.html">Sell Vehicles</a>', '<a href="sell.html" class="active">Sell Vehicles</a>')

# Extract Footer
footer_match = re.search(r'<footer class="footer">.*?</footer>', buy_cars_html, re.DOTALL)
footer_html = footer_match.group(0)

# Extract Nav and Footer CSS
nav_css = """  .navbar{background:var(--charcoal);position:sticky;top:0;z-index:100;}
  .nav-main{max-width:1280px;margin:0 auto;display:flex;align-items:center;padding:0 20px;height:80px;gap:0;}
  .logo{display:flex;align-items:center;margin-right:40px;height:60px;}
  .logo img{height:100%;width:auto;display:block;}
  .nav-links{display:flex;gap:4px;flex:1; align-items: center; position:static; transform:none; justify-content:flex-start;}
  .nav-links a{color:#ccd;font-size:14px;font-weight:500;padding:8px 14px;border-radius:6px; transition:all 0.2s; height:auto; display:inline-block; border-bottom: none;}
  .nav-links a:hover,.nav-links a.active{color:#fff;background:rgba(255,255,255,0.08);}
  .nav-links a.active{background:rgba(255,204,0,0.15);}
  .btn-outline-white{border:none;color:#1A1A2E;padding:8px 18px;border-radius:6px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.2s;background:var(--red);box-shadow:0 4px 10px rgba(255,204,0,0.2);}
  .btn-outline-white:hover{background:var(--red-dark);transform:translateY(-1px);box-shadow:0 6px 12px rgba(255,204,0,0.4);}
  .nav-actions{display:flex;gap:10px;align-items:center;margin-left:auto;}
"""

footer_css = """
  /* FOOTER */
  .footer { background: var(--charcoal); padding: 20px 20px; border-top: 1px solid rgba(255,255,255,0.05); margin-top: auto; }
  .footer-inner { max-width: 1280px; margin: 0 auto; }
  .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 40px; margin-bottom: 20px; }
  .footer-col-brand .logo { display: block; margin-bottom: 10px; height: 60px; }
  .footer-col-brand .logo img { height: 100%; width: auto; display: block; }
  .footer-copyright { font-size: 13px; line-height: 1.8; color: #8a9abf; font-weight: 500; margin-top: 10px; }
  .footer-col h4 { font-size: 16px; font-weight: 600; color: var(--red); margin-bottom: 15px; font-family: 'Inter', sans-serif; }
  .footer-col a { display: block; font-size: 14px; color: #e0e5eb; margin-bottom: 8px; transition: color 0.2s; font-weight: 500; }
  .footer-col a:hover { color: var(--red); }
  .quick-links-split { display: flex; gap: 30px; }
  .ql-divider { width: 1px; background: var(--red); opacity: 0.5; }
  .ql-col { display: flex; flex-direction: column; }
  .footer-contact .contact-item { display: flex; align-items: center; gap: 14px; margin-bottom: 12px; }
  .footer-contact .contact-icon { width: 18px; height: 18px; stroke: var(--red); flex-shrink: 0; }
  .footer-contact .contact-item a { margin-bottom: 0; font-size: 14px; color: #fff; font-weight: 500; letter-spacing: 0.5px; }
  .footer-bottom-bar { background: #333; border-radius: 40px; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; color: #bbb; font-size: 13px; font-weight: 500; }
  .fbb-left { display: flex; align-items: center; gap: 16px; }
  .fbb-connect-text { font-size: 14px; font-weight: 500; color: #fff; font-family: 'Inter', sans-serif; letter-spacing: 0.5px; }
  .fbb-socials { display: flex; gap: 10px; }
  .fbb-socials a { display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; background: #fff; color: #111; transition: all 0.3s ease; }
  .fbb-socials a:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
  .fbb-socials svg { width: 14px !important; height: 14px !important; fill: currentColor; }
  .fbb-links { display: flex; gap: 8px; align-items: center; }
  .fbb-links a { color: #bbb; text-decoration: none; transition: color 0.2s; font-size: 13px; font-weight: 600; }
  .fbb-links a:hover { color: var(--white); }
  .menu-toggle { display: none; }
"""

with open('sell.html', 'r', encoding='utf-8') as f:
    sell_html = f.read()

sell_html = re.sub(r'/\* NAVBAR \*/.*?/\* HERO \*/', '/* NAVBAR */\n' + nav_css + '\n/* HERO */', sell_html, flags=re.DOTALL)
sell_html = re.sub(r'</style>', footer_css + '\n</style>', sell_html)

sell_html = re.sub(r'<nav class="navbar">.*?</nav>', navbar_html, sell_html, flags=re.DOTALL)
sell_html = sell_html.replace('<div class="toast" id="toast"></div>', footer_html + '\n<div class="toast" id="toast"></div>')

# Replace image
sell_html = sell_html.replace('<div class="hero-img">🤝🚗</div>', '<div class="hero-img" style="height:150px; width:350px;"><img src="sell-illustration.png" alt="Sell Car Illustration" style="height:100%; width:100%; object-fit:contain;"></div>')

# Make the portal fit without scrolling
sell_html = sell_html.replace('.portal-box{background:var(--white);border-radius:16px;border:1px solid var(--border);box-shadow:0 10px 40px rgba(0,0,0,0.03);display:grid;grid-template-columns:280px 1fr 280px;min-height:600px;}', '.portal-box{background:var(--white);border-radius:16px;border:1px solid var(--border);box-shadow:0 10px 40px rgba(0,0,0,0.03);display:grid;grid-template-columns:280px 1fr 280px;height:480px;}')
sell_html = sell_html.replace('max-height:350px;', 'max-height:180px;')
sell_html = sell_html.replace('.p-mid{padding:40px 60px;}', '.p-mid{padding:20px 40px; display:flex; flex-direction:column; justify-content:center;}')
sell_html = sell_html.replace('.v-step{display:flex;gap:16px;margin-bottom:40px;position:relative;}', '.v-step{display:flex;gap:16px;margin-bottom:20px;position:relative;}')
sell_html = sell_html.replace('.v-step:not(:last-child)::after{content:\'\';position:absolute;left:16px;top:40px;bottom:-30px;width:1px;background:var(--border);z-index:1;}', '.v-step:not(:last-child)::after{content:\'\';position:absolute;left:16px;top:40px;bottom:-10px;width:1px;background:var(--border);z-index:1;}')
sell_html = sell_html.replace('.sell-hero{max-width:1280px;margin:40px auto 30px;', '.sell-hero{max-width:1280px;margin:10px auto 10px;')
sell_html = sell_html.replace('.portal-container{max-width:1280px;margin:0 auto 60px;padding:0 20px;}', '.portal-container{max-width:1280px;margin:0 auto 20px;padding:0 20px;}')
sell_html = sell_html.replace('.p-left{padding:40px 30px;', '.p-left{padding:20px 30px;')
sell_html = sell_html.replace('.p-right{padding:40px 30px;', '.p-right{padding:20px 30px;')

# Make body flex so footer stays at bottom
sell_html = sell_html.replace('body{font-family:\'Inter\',sans-serif;color:var(--text);background:var(--silver);}', 'body{font-family:\'Inter\',sans-serif;color:var(--text);background:var(--silver); display:flex; flex-direction:column; min-height:100vh; overflow-y: hidden;}')
sell_html = sell_html.replace('overflow-y: hidden;', 'overflow-y: hidden; /* Prevent scrolling */')

# Add missing JS checkLoginState to populate the user dropdown since the header is back
login_script = """
function checkLoginState() {
  const currentUser = localStorage.getItem('mg_current_user');
  const navActions = document.getElementById('nav-actions');
  if (navActions) {
    if (currentUser) {
      let initials = '👤';
      try {
        const userObj = JSON.parse(currentUser);
        const name = userObj.name || '';
        if (name) {
          const parts = name.split(' ');
          initials = parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : name.substring(0, 2).toUpperCase();
        }
      } catch(e) {}
      navActions.innerHTML = `
        <a href="customer-dashboard.html" title="My Profile" style="text-decoration:none; display:block;">
          <div style="width: 42px; height: 42px; border-radius: 50%; background: rgba(255, 204, 0, 0.15); border: 2px solid var(--red); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: var(--red); text-transform: uppercase; transition: all 0.2s;">
            ${initials}
          </div>
        </a>
      `;
    } else {
      navActions.innerHTML = `<a href="login.html" style="text-decoration:none;"><button class="btn-outline-white">Login</button></a>`;
    }
  }
}
checkLoginState();
"""
sell_html = sell_html.replace('</script>\n</body>', login_script + '\n</script>\n</body>')

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(sell_html)

print("Restored original dark header & footer, replaced illustration, and adjusted portal fit.")

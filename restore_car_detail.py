import re
import sys

try:
    with open('car-detail.html.orig', 'r', encoding='utf-8') as f:
        car = f.read()
        
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()

    # 1. Extract combined navbar CSS from index.html
    nav_start_1 = idx.find('/* NAVBAR */')
    nav_end_1 = idx.find('/* FOOTER */', nav_start_1)
    
    nav_start_2 = idx.find('/* NAVBAR */', nav_start_1 + 10)
    nav_end_2 = idx.find('/* Account Sidebar Styles */', nav_start_2)
    
    # We also need the Account Sidebar Styles!
    sidebar_css_start = idx.find('/* Account Sidebar Styles */')
    sidebar_css_end = idx.find('</style>', sidebar_css_start)
    
    block_1 = idx[nav_start_1:nav_end_1]
    block_2 = idx[nav_start_2:nav_end_2]
    sidebar_css = idx[sidebar_css_start:sidebar_css_end]
    
    combined_css = block_1 + "\n" + block_2 + "\n" + sidebar_css

    # 2. Extract navbar HTML and Sidebar HTML/JS from index.html
    nav_html_start = idx.find('<nav class="navbar">')
    nav_html_end = idx.find('</nav>', nav_html_start) + 6
    nav_html = idx[nav_html_start:nav_html_end]
    nav_html = nav_html.replace('class="nav-link-home active"', 'class="nav-link-home"')

    sidebar_html_start = idx.find('<!-- ACCOUNT SIDEBAR -->')
    sidebar_html_end = idx.find('<script>', sidebar_html_start)
    sidebar_html = idx[sidebar_html_start:sidebar_html_end]

    js_match = re.search(r'(document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*const accountBtn.*?\}\);)', idx, re.DOTALL)
    sidebar_js = js_match.group(1)

    # 3. Replace CSS in car-detail.html
    car_css_start = car.find('/* NAVBAR */')
    car_css_end = car.find('/* FOOTER CSS FIXED */')
    if car_css_start == -1 or car_css_end == -1:
        print("Could not find CSS boundaries in car")
        sys.exit(1)
        
    car = car[:car_css_start] + combined_css + "\n" + car[car_css_end:]

    # 4. Replace Nav HTML in car-detail.html
    car_nav_start = car.find('<nav class="navbar">')
    car_nav_end = car.find('</nav>', car_nav_start) + 6
    if car_nav_start == -1 or car_nav_end == -1:
        print("Could not find nav HTML boundaries in car")
        sys.exit(1)
        
    car = car[:car_nav_start] + nav_html + car[car_nav_end:]

    # 5. Fix checkContactVerification in car-detail.html
    check_contact = '''function checkContactVerification() {
  // We no longer show masked number or auto-redirect to login here.
  // The user must click "Get Seller Details" and fill the lead form.
}'''
    car = re.sub(r'function checkContactVerification\(\) \{.*?\n\}', check_contact, car, flags=re.DOTALL)
    
    # 6. Fix checkLoginState in car-detail.html
    new_login_state = '''function checkLoginState() {
  const currentUser = localStorage.getItem('mg_current_user');
  if (currentUser) {
    const loginLinks = document.querySelectorAll('a[href="login.html"]');
    loginLinks.forEach(link => {
      link.href = 'customer-dashboard.html';
      const btn = link.querySelector('button');
      if (btn) {
        if (btn.textContent.trim().toLowerCase() === 'login') {
          btn.textContent = 'Dashboard';
        }
      } else {
        if (link.textContent.includes('Login / Register')) {
          link.textContent = 'My Dashboard';
        }
      }
    });
  }
}'''
    car = re.sub(r'function checkLoginState\(\) \{.*?\n\}', new_login_state, car, flags=re.DOTALL)
    
    # 7. Append Sidebar HTML/JS to car-detail.html
    injection = f'{sidebar_html}\n<script>\n{sidebar_js}\n</script>\n</body>'
    car = car.replace('</body>', injection)

    with open('car-detail.html', 'w', encoding='utf-8') as f:
        f.write(car)
        
    print("Successfully restored and synced car-detail.html")
except Exception as e:
    print(f"Error: {e}")

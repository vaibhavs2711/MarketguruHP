import re

with open('sell.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_login_state = """function checkLoginState() {
  const currentUser = localStorage.getItem('mg_current_user');
  const navAccountBtn = document.getElementById('nav-account-btn');
  if (navAccountBtn) {
    if (currentUser) {
      let initials = '??';
      try {
        const userObj = JSON.parse(currentUser);
        const name = userObj.name || '';
        if (name) {
          const parts = name.split(' ');
          initials = parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : name.substring(0, 2).toUpperCase();
        } else {
           initials = currentUser.substring(0,2).toUpperCase();
        }
      } catch (e) { 
         initials = currentUser.substring(0,2).toUpperCase();
      }
      navAccountBtn.textContent = initials;
      navAccountBtn.style.fontWeight = '700';
      navAccountBtn.style.fontSize = '16px';
    } else {
      navAccountBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';
    }
  }
}
"""

html = re.sub(r'function checkLoginState\(\) \{.*?\n\}', new_login_state, html, flags=re.DOTALL)

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(html)

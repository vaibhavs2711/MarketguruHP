import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html_nav_new = '''
  <!-- NAVBAR -->
  <nav class="navbar">
    <div class="nav-main">
      <a href="index.html" class="logo" id="brand-logo">
        <img src="logo.png" alt="Market Guru HP Logo">
      </a>
      <div class="nav-links">
        <a href="index.html" class="active">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          Home
        </a>
        <a href="buy-cars.html">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
          Buy Vehicle
        </a>
        <a href="sell.html">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>
          Sell Vehicles
        </a>
        <a href="about.html">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
          About
        </a>
        <a href="compare.html">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v18"></path><rect x="3" y="11" width="6" height="10" rx="1"></rect><rect x="15" y="7" width="6" height="14" rx="1"></rect></svg>
          Compare
        </a>
      </div>
      <div class="nav-actions">
        <a href="login.html" class="nav-account-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          My Account
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </a>
      </div>
      <button class="menu-toggle" id="menu-toggle" aria-label="Toggle Navigation">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
'''

pattern_html = re.compile(r'<!-- NAVBAR -->.*?<!-- HERO -->', re.DOTALL)
html = pattern_html.sub(html_nav_new + '\\n\\n  <!-- HERO -->', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

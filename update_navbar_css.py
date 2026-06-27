import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_nav_new = '''
    /* NAVBAR */
    .navbar {
      background: var(--white);
      position: sticky;
      top: 0;
      z-index: 100;
      border-bottom: 1px solid var(--border);
    }
    .nav-main {
      max-width: 1320px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      height: 85px;
    }
    .logo {
      height: 60px;
    }
    .logo img {
      height: 100%;
      width: auto;
    }
    .nav-links {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .nav-links a {
      color: var(--charcoal);
      font-size: 15px;
      font-weight: 700;
      padding: 10px 20px;
      border-radius: 50px;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .nav-links a svg {
      width: 18px; height: 18px;
      color: var(--muted);
    }
    .nav-links a:hover {
      background: var(--blue-light);
    }
    .nav-links a:hover svg {
      color: var(--primary);
    }
    .nav-links a.active {
      background: var(--navy);
      color: var(--white);
    }
    .nav-links a.active svg {
      color: var(--primary);
    }
    .nav-actions {
      display: flex;
      align-items: center;
    }
    .nav-account-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      border: 1.5px solid var(--border);
      border-radius: 50px;
      padding: 10px 20px;
      font-weight: 700;
      font-size: 15px;
      color: var(--charcoal);
      transition: all 0.2s;
      background: var(--white);
    }
    .nav-account-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }
'''

html = html.replace('</style>', css_nav_new + '\\n</style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

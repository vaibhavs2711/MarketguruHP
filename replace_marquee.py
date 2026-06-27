import re

with open('e:/MarketguruHP/MarketguruHP/MarketguruHP/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# CSS replacement
banner_css = """
  /* STATIC SOCIAL BANNER */
  .social-banner-container {
    display: flex;
    background: #0B0E14;
    border-top: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    width: 100%;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
  }
  .sb-left-wrap {
    position: relative;
    display: flex; align-items: center; gap: 14px;
    padding: 24px 60px 24px 40px;
    z-index: 1;
  }
  .sb-left-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: -50px; right: 0; bottom: 0;
    background: linear-gradient(90deg, #131826 0%, #0d111c 100%);
    transform: skewX(-20deg);
    transform-origin: bottom right;
    border-right: 2px solid var(--red);
    box-shadow: 4px 0 15px rgba(255,204,0,0.15);
    z-index: -1;
  }
  .sb-left-icon svg { width: 36px; height: 36px; stroke: var(--red); }
  .sb-left-text { display: flex; flex-direction: column; }
  .sb-left-text h4 { color: var(--red); font-size: 15px; font-weight: 800; margin: 0 0 2px; letter-spacing: 0.5px; }
  .sb-left-text p { color: #fff; font-size: 12px; margin: 0; font-weight: 500; }

  .sb-links {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 10px;
  }
  .sb-link-block {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 20px;
    text-decoration: none;
    transition: transform 0.2s;
  }
  .sb-link-block:hover {
    transform: translateY(-2px);
  }
  .sb-divider {
    width: 1px;
    height: 40px;
    background: rgba(255,255,255,0.1);
  }
  .sb-logo svg {
    width: 44px; height: 44px;
  }
  .sb-info {
    display: flex; flex-direction: column;
  }
  .sb-info h5 {
    font-size: 16px; font-weight: 800; color: #fff; margin: 0 0 2px 0; letter-spacing: 0.5px;
  }
  .sb-info span {
    font-size: 13px; font-weight: 600; color: var(--red);
  }
  .sb-btn {
    margin-left: 10px;
    border: 1.5px solid var(--red);
    border-radius: 20px;
    color: var(--red);
    font-size: 11px;
    font-weight: 800;
    padding: 6px 16px;
    letter-spacing: 0.5px;
    transition: all 0.2s;
  }
  .sb-link-block:hover .sb-btn {
    background: var(--red); color: #000;
  }

  .sb-right-wrap {
    position: relative;
    display: flex; align-items: center; justify-content: center; gap: 8px;
    padding: 24px 40px 24px 60px;
    z-index: 1;
    margin-left: auto;
  }
  .sb-right-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: -50px; bottom: 0;
    background: linear-gradient(90deg, #0d111c 0%, #131826 100%);
    transform: skewX(-20deg);
    transform-origin: bottom left;
    border-left: 2px solid var(--red);
    box-shadow: -4px 0 15px rgba(255,204,0,0.15);
    z-index: -1;
  }
  .sb-right-text { text-align: right; }
  .sb-right-text h4 { font-size: 15px; font-weight: 700; color: #fff; margin: 0; line-height: 1.2; }
  .sb-right-text h4.yellow { color: var(--red); font-weight: 900; font-size: 18px; }
  
  @media(max-width: 1100px) {
    .sb-left-wrap, .sb-right-wrap { display: none; }
    .sb-links { flex-wrap: wrap; padding: 20px 0; }
    .sb-divider { display: none; }
  }
"""

banner_html = """<!-- STATIC SOCIAL BANNER -->
<div class="social-banner-container">
  <div class="sb-left-wrap">
    <div class="sb-left-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </div>
    <div class="sb-left-text">
      <h4>STAY CONNECTED</h4>
      <p>Follow us on social media</p>
    </div>
  </div>
  
  <div class="sb-links">
    <!-- Instagram -->
    <a href="https://www.instagram.com/marketguruhp" target="_blank" class="sb-link-block">
      <div class="sb-logo">
        <svg viewBox="0 0 24 24">
          <defs>
            <linearGradient id="ig-grad" x1="15%" y1="100%" x2="85%" y2="0%">
              <stop offset="0%" stop-color="#fdf497"/>
              <stop offset="25%" stop-color="#fd5946"/>
              <stop offset="50%" stop-color="#d6249f"/>
              <stop offset="100%" stop-color="#285AEB"/>
            </linearGradient>
          </defs>
          <rect x="1" y="1" width="22" height="22" rx="6" fill="url(#ig-grad)" />
          <circle cx="12" cy="12" r="5" fill="none" stroke="#fff" stroke-width="2" />
          <circle cx="16.5" cy="7.5" r="1.2" fill="#fff" />
        </svg>
      </div>
      <div class="sb-info">
         <h5>INSTAGRAM</h5>
         <span>@marketguru.hp</span>
      </div>
      <div class="sb-btn">FOLLOW &rarr;</div>
    </a>
    
    <div class="sb-divider"></div>
    
    <!-- YouTube -->
    <a href="https://www.youtube.com/@marketguruhp" target="_blank" class="sb-link-block">
      <div class="sb-logo">
        <svg viewBox="0 0 24 24">
          <path fill="#FF0000" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.016 3.016 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.872.505 9.377.505 9.377.505s7.505 0 9.377-.505a3.016 3.016 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/>
          <path fill="#FFFFFF" d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
        </svg>
      </div>
      <div class="sb-info">
         <h5>YOUTUBE</h5>
         <span>Market Guru HP</span>
      </div>
      <div class="sb-btn">SUBSCRIBE &rarr;</div>
    </a>
    
    <div class="sb-divider"></div>
    
    <!-- Facebook -->
    <a href="https://www.facebook.com/marketguruhp" target="_blank" class="sb-link-block">
      <div class="sb-logo">
        <svg viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="12" fill="#1877F2"/>
          <path fill="#FFFFFF" d="M15.4 12H13v8h-3v-8H8v-2.8h2V7.4c0-2.2 1-3.4 3.6-3.4h2.4v2.8h-1.5c-1.1 0-1.2.4-1.2 1.3v1.1h2.9l-.2 2.8z"/>
        </svg>
      </div>
      <div class="sb-info">
         <h5>FACEBOOK</h5>
         <span>@marketguru.hp</span>
      </div>
      <div class="sb-btn">FOLLOW &rarr;</div>
    </a>
  </div>
  
  <div class="sb-right-wrap">
    <div class="sb-right-text">
      <h4>✨ Join Our</h4>
      <h4 class="yellow">Community!</h4>
    </div>
  </div>
</div>

<!-- FEATURED CARS -->"""

# Remove old marquee CSS
content = re.sub(r'  /\* SOCIAL MARQUEE \*/.*?} \n', '', content, flags=re.DOTALL)
content = re.sub(r'  /\* SOCIAL MARQUEE \*/.*?\n</style>', banner_css + '\n</style>', content, flags=re.DOTALL)

if '/* STATIC SOCIAL BANNER */' not in content:
    content = content.replace('</style>', banner_css + '\n</style>')

# Remove old marquee HTML
content = re.sub(r'<!-- SOCIAL MARQUEE -->.*?<!-- FEATURED CARS -->', banner_html, content, flags=re.DOTALL)

with open('e:/MarketguruHP/MarketguruHP/MarketguruHP/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Static banner added.")

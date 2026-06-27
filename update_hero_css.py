import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Hero CSS
hero_css_new = '''
    /* HERO SECTION REFRESH */
    .hero-new {
      background: linear-gradient(135deg, var(--bg) 0%, #ffffff 100%);
      position: relative;
      padding: 60px 20px 120px 20px;
      overflow: hidden;
      min-height: calc(100vh - 85px);
    }
    .hero-bg-trails {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background-image: radial-gradient(circle at 70% 50%, rgba(249, 115, 22, 0.08) 0%, transparent 60%);
      pointer-events: none;
      z-index: 1;
    }
    .hero-new-inner {
      max-width: 1320px;
      margin: 0 auto;
      position: relative;
      z-index: 2;
    }
    .hero-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
      align-items: center;
      margin-bottom: 60px;
    }
    .hero-content-left h1 {
      font-size: clamp(40px, 4.5vw, 64px);
      font-weight: 900;
      color: var(--navy);
      line-height: 1.1;
      letter-spacing: -1px;
      margin-bottom: 20px;
    }
    .hero-content-left h1 span.highlight { color: var(--primary); }
    .hero-checks { display: flex; gap: 24px; margin-bottom: 20px; flex-wrap: wrap; }
    .hero-checks span { display: flex; align-items: center; gap: 8px; font-weight: 700; color: var(--charcoal); font-size: 15px; }
    .hero-checks svg { color: var(--primary); background: rgba(249, 115, 22, 0.1); border-radius: 50%; padding: 2px; }
    .hero-content-left p { color: var(--muted); font-size: 17px; line-height: 1.6; max-width: 90%; margin-bottom: 30px; }
    .hero-social-stats { display: flex; gap: 16px; flex-wrap: wrap; }
    .hs-card { display: flex; align-items: center; gap: 12px; background: var(--white); border: 1px solid var(--border); border-radius: 50px; padding: 8px 20px 8px 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    .hs-icon { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--white); }
    .hs-icon.ig { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
    .hs-icon.fb { background: #1877F2; }
    .hs-icon.yt { background: #FF0000; }
    .hs-info { display: flex; flex-direction: column; }
    .hs-info strong { color: var(--primary); font-size: 18px; font-weight: 900; line-height: 1; }
    .hs-info span { font-size: 10px; font-weight: 800; color: var(--muted); letter-spacing: 0.5px; }
    .hero-content-right { position: relative; height: 100%; min-height: 400px; }
    .hero-map { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 120%; opacity: 0.15; z-index: -1; filter: sepia(1) hue-rotate(340deg) saturate(3); }
    .hero-car { width: 120%; max-width: 800px; position: absolute; top: 50%; left: 50%; transform: translate(-40%, -40%); }
    .hero-search-box { background: var(--white); border-radius: 60px; padding: 12px 12px 12px 30px; display: flex; align-items: center; gap: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border: 1px solid var(--border); max-width: 1100px; margin: 0 auto 30px auto; z-index: 10; position: relative; }
    .h-search-field { flex: 1; display: flex; flex-direction: column; border-right: 1px solid var(--border); padding-right: 20px; }
    .h-search-field:last-of-type { border-right: none; }
    .h-search-field label { font-size: 11px; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .h-search-field select { border: none; font-size: 16px; font-weight: 700; color: var(--charcoal); outline: none; background: transparent; width: 100%; cursor: pointer; }
    .btn-search-primary { background: var(--secondary); color: var(--white); border: none; border-radius: 50px; padding: 16px 36px; font-size: 16px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }
    .btn-search-primary:hover { background: var(--primary-hover); transform: translateY(-2px); box-shadow: 0 6px 15px rgba(234, 88, 12, 0.3); }
    .hero-features-bar { display: flex; justify-content: center; gap: 40px; background: var(--white); padding: 20px; border-radius: 20px; max-width: 1100px; margin: 0 auto; border: 1px solid var(--border); flex-wrap: wrap; }
    .hf-item { display: flex; align-items: center; gap: 12px; font-size: 13px; color: var(--muted); font-weight: 600; }
    .hf-item strong { color: var(--charcoal); font-size: 16px; font-weight: 900; }
    .hf-icon { width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; color: var(--charcoal); }
'''

# Find the start of HERO SECTION CSS and end of it.
pattern_css = re.compile(r'/\* HERO SECTION \*/.*?/\* CATEGORIES \*/', re.DOTALL)
html = pattern_css.sub(hero_css_new + '\\n\\n/* CATEGORIES */', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

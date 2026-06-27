import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_car_css = '''
    /* FEATURED CARS CSS */
    .car-card {
      background: var(--white);
      border-radius: 12px;
      border: 1px solid var(--border);
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
      display: flex;
      flex-direction: column;
      opacity: 1;
      transform: translateY(0);
      transition: all 0.3s ease;
      cursor: pointer;
    }
    .car-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
      border-color: var(--primary);
    }
    .car-img {
      width: 100%;
      height: 180px;
      object-fit: cover;
      position: relative;
    }
    .car-badge {
      position: absolute;
      top: 12px; left: 12px;
      background: var(--primary);
      color: var(--white);
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .car-wishlist {
      position: absolute;
      top: 12px; right: 12px;
      color: var(--muted);
      background: var(--white);
      width: 28px; height: 28px;
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer;
    }
    .car-info {
      padding: 16px;
    }
    .car-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--navy);
      margin-bottom: 6px;
    }
    .car-specs {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
      font-weight: 600;
    }
    .car-price {
      font-size: 20px;
      font-weight: 900;
      color: var(--primary);
    }
'''

new_trending_html = '''
  <!-- TRENDING TODAY -->
  <section class="section" style="padding-bottom: 80px;">
    <div class="section-inner" style="max-width: 1320px; margin: 0 auto; padding: 0 20px;">
      <div class="section-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;">
        <div class="section-title" style="font-size: 24px; font-family:'Inter', sans-serif; display:flex; align-items:center; gap:8px;">
          <span style="font-size:28px;">🔥</span> <span style="color:var(--navy); font-weight:900;">Trending Today</span>
        </div>
        <a href="buy-cars.html" class="view-all" style="color:var(--primary); font-weight:700; font-size:14px;">View All →</a>
      </div>
      
      <div class="cars-grid" id="featuredCars" style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
        <!-- Javascript will populate this -->
      </div>
      
      <!-- PROMO BANNER -->
      <div class="promo-banner" style="background: var(--secondary); border-radius: 12px; padding: 24px 32px; display: flex; justify-content: space-between; align-items: center; margin-top: 40px; color: var(--white);">
         <div style="display:flex; align-items:center; gap: 20px;">
            <div style="font-size: 40px;">🚀</div>
            <div>
               <h3 style="font-size: 22px; font-weight: 800; margin-bottom: 4px;">List Unlimited Cars & Grow Your Business</h3>
               <p style="font-size: 14px; opacity: 0.9; font-weight: 500;">You can list 1 car for free. Upgrade your plan to list unlimited cars and get more visibility.</p>
            </div>
         </div>
         <div style="display:flex; align-items:center; gap: 24px;">
            <div style="text-align: right;">
               <div style="font-size: 13px; font-weight: 600; opacity: 0.9;">Only</div>
               <div style="font-size: 24px; font-weight: 900;">₹499/-</div>
            </div>
            <a href="login.html" style="background: var(--white); color: var(--secondary); font-weight: 800; padding: 12px 24px; border-radius: 50px; display:flex; align-items:center; gap:8px;">UPGRADE NOW →</a>
         </div>
      </div>
    </div>
  </section>
'''

new_render = '''    function renderCars() {
      const grid = document.getElementById('featuredCars');
      if(!grid) return;
      const featured = mgDB.getUsedCars().slice(0, 4);

      grid.innerHTML = featured.map(c => `
    <div class="car-card" onclick="window.location='car-detail.html?id=${c.id}'">
      <div class="car-img" style="background:var(--bg);">
        <div class="car-badge">🔥 Hot Deal</div>
        <div class="car-wishlist" onclick="event.stopPropagation();wishlist(${c.id})">
           <svg width="16" height="16" viewBox="0 0 24 24" fill="${mgDB.isWishlisted(c.id) ? 'var(--danger)' : 'none'}" stroke="${mgDB.isWishlisted(c.id) ? 'var(--danger)' : 'currentColor'}" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
        </div>
        ${c.image ? `<img src="${c.image}" style="width:100%;height:100%;object-fit:cover;" />` : `<div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:80px;">${c.emoji || '🚗'}</div>`}
      </div>
      <div class="car-info">
        <div class="car-title">${c.name}</div>
        <div class="car-specs">${c.year} · ${c.fuel} · ${c.km} km</div>
        <div class="car-price">₹${c.price} Lakh</div>
      </div>
    </div>
      `).join('');
    }'''

# Replace CSS
pattern_css = re.compile(r'\.car-card \{.*?(?=/\* BRAND LIST \*/|/\* RECOMMENDED \*/|/\* RESPONSIVE \*/)', re.DOTALL)
if pattern_css.search(html):
    html = pattern_css.sub(new_car_css + '\n\n', html)
else:
    print("CSS replace failed")

# Replace HTML
pattern_html = re.compile(r'<!-- FEATURED CARS -->.*?<!-- TRUST / WHY US — 3D Carousel -->', re.DOTALL)
if pattern_html.search(html):
    html = pattern_html.sub(new_trending_html + '\n\n  <!-- TRUST / WHY US — 3D Carousel -->', html)
else:
    print("HTML replace failed")
    
# Replace renderCars
pattern_js = re.compile(r'function renderCars\(\)\s*\{.*?\}\s*\}\s*', re.DOTALL)
if pattern_js.search(html):
    html = pattern_js.sub(new_render + '\n\n', html)
else:
    print("JS replace failed")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html elements")

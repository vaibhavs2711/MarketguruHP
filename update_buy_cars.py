import re

with open('buy-cars.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS for card navigation buttons
css_nav = """  /* CARD NAVIGATION BUTTONS */
  .card-nav-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0, 0, 0, 0.4);
    color: white;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    border-radius: 50%;
    cursor: pointer;
    z-index: 10;
    transition: background 0.2s, transform 0.2s;
    user-select: none;
    opacity: 0;
  }
  .car-card:hover .card-nav-btn {
    opacity: 1;
  }
  .card-nav-btn:hover {
    background: rgba(0, 0, 0, 0.8);
    transform: translateY(-50%) scale(1.1);
  }
  .card-nav-btn.prev {
    left: 8px;
  }
  .card-nav-btn.next {
    right: 8px;
  }
"""
html = html.replace('/* BREADCRUMB */', css_nav + '\n  /* BREADCRUMB */')

# Add nextCardImg JS function
js_nav = """function nextCardImg(e, cardId, direction, imgStr) {
  if (e) e.stopPropagation();
  try {
    const imgs = JSON.parse(imgStr);
    if (!imgs || imgs.length <= 1) return;
    
    const imgEl = document.getElementById('card-img-' + cardId);
    if (!imgEl) return;
    
    let currentIndex = parseInt(imgEl.getAttribute('data-index') || '0');
    currentIndex = (currentIndex + direction + imgs.length) % imgs.length;
    
    imgEl.src = imgs[currentIndex];
    imgEl.setAttribute('data-index', currentIndex);
  } catch (err) {
    console.error('Error changing card image:', err);
  }
}

function renderCars"""
html = html.replace('function renderCars', js_nav)

# Replace the list.innerHTML mapping inside renderCars
old_render = """  list.innerHTML = visibleCars.map(c => `
    <div class="car-card" onclick="window.location='car-detail.html?id=${c.id}'">
      <div class="car-img-wrap" style="background:linear-gradient(135deg,${c.color || '#e8eef5'},#ccd4e0)">
        ${c.image ? `<img src="${c.image}" />` : `<span style="font-size:80px">${c.emoji || '🚗'}</span>`}
        ${c.verified ? '<div class="car-badge-featured">Featured</div>' : ''}
      </div>"""

new_render = """  list.innerHTML = visibleCars.map(c => {
    let imgs = [];
    if (c.images && Array.isArray(c.images) && c.images.length > 0) imgs = c.images;
    else if (c.image) imgs = [c.image];
    
    let imgStr = JSON.stringify(imgs).replace(/"/g, '&quot;');
    let hasImgs = imgs.length > 0;
    
    return `
    <div class="car-card" onclick="window.location='car-detail.html?id=${c.id}'">
      <div class="car-img-wrap" style="background:linear-gradient(135deg,${c.color || '#e8eef5'},#ccd4e0)">
        <img src="${hasImgs ? imgs[0] : ''}" style="${hasImgs ? '' : 'display:none;'}" id="card-img-${c.id}" data-index="0" />
        <span style="font-size:80px; ${hasImgs ? 'display:none;' : ''}" id="card-emoji-${c.id}">${c.emoji || '🚗'}</span>
        ${c.verified ? '<div class="car-badge-featured">Featured</div>' : ''}
        
        ${imgs.length > 1 ? `
          <div class="card-nav-btn prev" onclick="event.stopPropagation(); nextCardImg(event, ${c.id}, -1, '${imgStr}')">❮</div>
          <div class="card-nav-btn next" onclick="event.stopPropagation(); nextCardImg(event, ${c.id}, 1, '${imgStr}')">❯</div>
        ` : ''}
      </div>"""

html = html.replace(old_render, new_render)
html = html.replace("    </div>\n  `).join('');", "    </div>\n  `;\n  }).join('');")

with open('buy-cars.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated buy-cars.html")

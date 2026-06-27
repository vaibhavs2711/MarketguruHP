import re

with open('sell.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update loadStep(4)
old_step4 = """  else if (stepNum === 4) {
    const grid = document.getElementById('grid-container');
    grid.style.display = 'grid';
    grid.innerHTML = `
      <div class="grid-opt" onclick="sellData.trans='Manual'; setSelection('fuel', 'Petrol', null, event)">Petrol Manual</div>
      <div class="grid-opt" onclick="sellData.trans='Automatic'; setSelection('fuel', 'Petrol', null, event)">Petrol Auto</div>
      <div class="grid-opt" onclick="sellData.trans='Manual'; setSelection('fuel', 'Diesel', null, event)">Diesel Manual</div>
      <div class="grid-opt" onclick="sellData.trans='Automatic'; setSelection('fuel', 'Diesel', null, event)">Diesel Auto</div>
      <div class="grid-opt" onclick="sellData.trans='Manual'; setSelection('fuel', 'CNG', null, event)">CNG Manual</div>
      <div class="grid-opt" onclick="sellData.trans='Automatic'; setSelection('fuel', 'Electric', null, event)">Electric Auto</div>
    `;
  }"""

new_step4 = """  else if (stepNum === 4) {
    document.getElementById('grid-container').style.display = 'none';
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    
    // SVG icons
    const svgAuto = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-8"></path><text x="12" y="6" font-size="4" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="currentColor" stroke="none">P</text><text x="8" y="11" font-size="4" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="currentColor" stroke="none">R</text><text x="16" y="11" font-size="4" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="currentColor" stroke="none">N</text><text x="12" y="21" font-size="4" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="currentColor" stroke="none">D</text></svg>`;
    const svgManual = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M7 6v12"></path><path d="M12 6v12"></path><path d="M17 6v12"></path><path d="M5 12h14"></path><circle cx="7" cy="5" r="1.5"></circle><circle cx="12" cy="5" r="1.5"></circle><circle cx="17" cy="5" r="1.5"></circle><circle cx="7" cy="19" r="1.5"></circle><circle cx="12" cy="19" r="1.5"></circle><circle cx="17" cy="19" r="1.5"></circle></svg>`;
    const svgClutchless = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M7 6v12"></path><path d="M12 6v12"></path><path d="M17 6v12"></path><path d="M5 12h14"></path><circle cx="7" cy="5" r="1.5"></circle><circle cx="12" cy="5" r="1.5"></circle><circle cx="17" cy="5" r="1.5"></circle><circle cx="12" cy="19" r="1.5"></circle><circle cx="17" cy="19" r="1.5"></circle></svg>`;

    const svgFuel = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="15" y2="22"></line><line x1="4" y1="9" x2="14" y2="9"></line><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"></path><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 2 2h0a2 2 0 0 0 2-2V9.83a2 2 0 0 0-.59-1.42L18 5"></path></svg>`;
    const svgElectric = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>`;
    const svgHybrid = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path></svg>`;

    inp.innerHTML = `
      <style>
        .vf-section { margin-bottom: 28px; }
        .vf-title { font-size: 16px; font-weight: 700; color: var(--charcoal); margin-bottom: 12px; }
        .vf-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }
        .vf-card {
          border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px;
          display: flex; align-items: center; gap: 12px; background: var(--white);
          cursor: pointer; transition: all 0.2s; font-weight: 600; font-size: 14px; color: var(--charcoal);
        }
        .vf-card:hover { border-color: var(--primary); background: #f8fafc; }
        .vf-card.selected { border-color: var(--primary); background: var(--primary-light); color: var(--primary); }
      </style>
      
      <div class="vf-section">
        <div class="vf-title">Transmission</div>
        <div class="vf-grid">
          <div class="vf-card trans-card ${sellData.trans === 'Automatic' ? 'selected' : ''}" onclick="selectVariantOpt('trans', 'Automatic', this)">
            <span style="color:#333;">${svgAuto}</span> Automatic
          </div>
          <div class="vf-card trans-card ${sellData.trans === 'Manual' ? 'selected' : ''}" onclick="selectVariantOpt('trans', 'Manual', this)">
            <span style="color:#333;">${svgManual}</span> Manual
          </div>
          <div class="vf-card trans-card ${sellData.trans === 'Clutchless Manual' ? 'selected' : ''}" onclick="selectVariantOpt('trans', 'Clutchless Manual', this)">
            <span style="color:#333;">${svgClutchless}</span> Clutchless Manual
          </div>
        </div>
      </div>
      
      <div class="vf-section">
        <div class="vf-title">Fuel Type</div>
        <div class="vf-grid">
          <div class="vf-card fuel-card ${sellData.fuel === 'Petrol' ? 'selected' : ''}" onclick="selectVariantOpt('fuel', 'Petrol', this)">
            <span style="color:#f97316;">${svgFuel}</span> Petrol
          </div>
          <div class="vf-card fuel-card ${sellData.fuel === 'Diesel' ? 'selected' : ''}" onclick="selectVariantOpt('fuel', 'Diesel', this)">
            <span style="color:#3b82f6;">${svgFuel}</span> Diesel
          </div>
          <div class="vf-card fuel-card ${sellData.fuel === 'CNG' ? 'selected' : ''}" onclick="selectVariantOpt('fuel', 'CNG', this)">
            <span style="color:#10b981;">${svgFuel}</span> CNG
          </div>
          <div class="vf-card fuel-card ${sellData.fuel === 'Hybrid' ? 'selected' : ''}" onclick="selectVariantOpt('fuel', 'Hybrid', this)">
            <span style="color:#10b981;">${svgHybrid}</span> Hybrid
          </div>
          <div class="vf-card fuel-card ${sellData.fuel === 'Electric' ? 'selected' : ''}" onclick="selectVariantOpt('fuel', 'Electric', this)">
            <span style="color:#8b5cf6;">${svgElectric}</span> Electric
          </div>
        </div>
      </div>
    `;
    
    const btn = document.getElementById('btn-continue');
    btn.style.display = 'flex';
    if (sellData.trans && sellData.fuel) {
      btn.disabled = false;
    } else {
      btn.disabled = true;
    }
  }"""
html = html.replace(old_step4, new_step4)

# 2. Add selectVariantOpt JS function
js_func = """
function selectVariantOpt(type, value, el) {
  sellData[type] = value;
  
  // Visual selection
  const cls = type === 'trans' ? 'trans-card' : 'fuel-card';
  const siblings = document.querySelectorAll('.' + cls);
  siblings.forEach(s => s.classList.remove('selected'));
  el.classList.add('selected');
  
  // Enable continue button if both selected
  if (sellData.trans && sellData.fuel) {
    const btn = document.getElementById('btn-continue');
    btn.disabled = false;
    // Don't auto-advance instantly so they see the selection
    if (type === 'fuel' || sellData.fuel) {
        setTimeout(nextStep, 400);
    }
  }
}

function loadStep"""
html = html.replace('function loadStep', js_func)

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated sell.html variant section")

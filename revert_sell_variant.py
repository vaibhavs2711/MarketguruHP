import re

with open('sell.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update STEPS array
old_steps = """const STEPS = [
  { id: 1, label: 'Brand', title: 'Select brand' },
  { id: 2, label: 'Model', title: 'Select model' },
  { id: 3, label: 'Year', title: 'Select year' },
  { id: 4, label: 'Transmission', title: 'Select transmission' },
  { id: 5, label: 'Fuel', title: 'Select fuel type' },
  { id: 6, label: 'State', title: 'Select city' },
  { id: 7, label: 'Photos', title: 'Upload photos' },
  { id: 8, label: 'Details', title: 'Final Details' }
];"""

new_steps = """const STEPS = [
  { id: 1, label: 'Brand', title: 'Select brand' },
  { id: 2, label: 'Model', title: 'Select model' },
  { id: 3, label: 'Year', title: 'Select year' },
  { id: 4, label: 'Variant', title: 'Select variant & fuel' },
  { id: 5, label: 'State', title: 'Select city' },
  { id: 6, label: 'Photos', title: 'Upload photos' },
  { id: 7, label: 'Details', title: 'Final Details' }
];"""

html = html.replace(old_steps, new_steps)

# 2. Update step selection resets in goToStep
old_resets = """  if(num <= 1) sellData.brand = sellData.brandId = null;
  if(num <= 2) sellData.model = sellData.modelId = null;
  if(num <= 3) sellData.year = null;
  if(num <= 4) sellData.trans = null;
  if(num <= 5) sellData.fuel = null;
  if(num <= 6) sellData.city = null;
  if(num <= 7) { sellData.photosUploaded = false; uploadedPhotos = []; }"""

new_resets = """  if(num <= 1) sellData.brand = sellData.brandId = null;
  if(num <= 2) sellData.model = sellData.modelId = null;
  if(num <= 3) sellData.year = null;
  if(num <= 4) sellData.fuel = sellData.trans = null;
  if(num <= 5) sellData.city = null;
  if(num <= 6) { sellData.photosUploaded = false; uploadedPhotos = []; }"""

html = html.replace(old_resets, new_resets)

# 3. Update breadcrumbs
old_breadcrumbs = """  if (sellData.year) bHTML += `<div class="bc-pill">${sellData.year} <span onclick="goToStep(3)">×</span></div>`;
  if (sellData.trans) bHTML += `<div class="bc-pill">${sellData.trans} <span onclick="goToStep(4)">×</span></div>`;
  if (sellData.fuel) bHTML += `<div class="bc-pill">${sellData.fuel} <span onclick="goToStep(5)">×</span></div>`;
  if (sellData.city) bHTML += `<div class="bc-pill">${sellData.city} <span onclick="goToStep(6)">×</span></div>`;"""

new_breadcrumbs = """  if (sellData.year) bHTML += `<div class="bc-pill">${sellData.year} <span onclick="goToStep(3)">×</span></div>`;
  if (sellData.fuel) bHTML += `<div class="bc-pill">${sellData.fuel} ${sellData.trans||''} <span onclick="goToStep(4)">×</span></div>`;
  if (sellData.city) bHTML += `<div class="bc-pill">${sellData.city} <span onclick="goToStep(5)">×</span></div>`;"""

html = html.replace(old_breadcrumbs, new_breadcrumbs)

# 4. Update loadStep block
old_loadStep_regex = r"  else if \(stepNum === 4\) \{.*?  \} else if \(stepNum === 6\) \{"

new_loadStep4_5 = """  else if (stepNum === 4) {
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
  }
  else if (stepNum === 5) {"""

html = re.sub(old_loadStep_regex, new_loadStep4_5, html, flags=re.DOTALL)

old_step7 = "  else if (stepNum === 7) {"
new_step6 = "  else if (stepNum === 6) {"
html = html.replace(old_step7, new_step6)

old_step8 = "  else if (stepNum === 8) {"
new_step7 = "  else if (stepNum === 7) {"
html = html.replace(old_step8, new_step7)

old_next_step = """function nextStep() {
  if (currentStep === 8) {"""

new_next_step = """function nextStep() {
  if (currentStep === 7) {"""
  
html = html.replace(old_next_step, new_next_step)

old_select_variant = """function selectVariantOpt(type, value, el) {
  sellData[type] = value;
  
  // Visual selection
  const cls = type === 'trans' ? 'trans-card' : 'fuel-card';
  const siblings = document.querySelectorAll('.' + cls);
  siblings.forEach(s => s.classList.remove('selected'));
  el.classList.add('selected');
  
  // Auto advance to next step
  setTimeout(nextStep, 200);
}"""

new_select_variant = """function selectVariantOpt(type, value, el) {
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
}"""

html = html.replace(old_select_variant, new_select_variant)

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Reverted to 7 steps")

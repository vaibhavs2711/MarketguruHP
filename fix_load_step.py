import re

with open('sell.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will replace the ENTIRE loadStep function.
new_load_step = """function loadStep(stepNum) {
  resetContainers();
  const title = document.getElementById('step-title');
  title.textContent = STEPS[stepNum-1].title;
  
  if (stepNum === 1) {
    document.getElementById('search-box').style.display = 'block';
    const list = document.getElementById('list-container');
    list.style.display = 'block';
    list.innerHTML = '<div style="padding:20px;text-align:center;color:#666;">Loading brands...</div>';
    
    fetch(API_BASE + '/api/car-makes')
      .then(r => r.json())
      .then(data => {
        currentList = data;
        renderList(data, 'brandId', 'brand');
      });
  } 
  else if (stepNum === 2) {
    document.getElementById('search-box').style.display = 'block';
    const list = document.getElementById('list-container');
    list.style.display = 'block';
    list.innerHTML = '<div style="padding:20px;text-align:center;color:#666;">Loading models...</div>';
    
    fetch(API_BASE + '/api/car-models?makeId=' + sellData.brandId)
      .then(r => r.json())
      .then(data => {
        currentList = data;
        renderList(data, 'modelId', 'model');
      });
  }
  else if (stepNum === 3) {
    const grid = document.getElementById('grid-container');
    grid.style.display = 'grid';
    let yHTML = '';
    for(let y=2026; y>=2010; y--) {
      yHTML += `<div class="grid-opt" onclick="setSelection('year', '${y}', null, event)">${y}</div>`;
    }
    grid.innerHTML = yHTML;
  }
  else if (stepNum === 4) {
    document.getElementById('grid-container').style.display = 'none';
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    
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
  else if (stepNum === 5) {
    const grid = document.getElementById('grid-container');
    grid.style.display = 'grid';
    grid.innerHTML = `
      <div class="grid-opt" onclick="setSelection('city', 'Vadodara', null, event)">Vadodara</div>
      <div class="grid-opt" onclick="setSelection('city', 'Ahmedabad', null, event)">Ahmedabad</div>
      <div class="grid-opt" onclick="setSelection('city', 'Surat', null, event)">Surat</div>
      <div class="grid-opt" onclick="setSelection('city', 'Rajkot', null, event)">Rajkot</div>
      <div class="grid-opt" onclick="setSelection('city', 'Gandhinagar', null, event)">Gandhinagar</div>
    `;
  }
  else if (stepNum === 6) {
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    
    inp.innerHTML = `
      <div style="margin-bottom:24px;">
        <h2 style="font-size:20px;font-weight:800;color:var(--charcoal);margin-bottom:8px;">Upload photos</h2>
        <p style="font-size:14px;color:var(--muted);">Add clear and accurate photos to get better offers from buyers.</p>
      </div>

      <div class="photo-upload-grid">
        <label class="photo-card" for="inp-photos">
          <div class="photo-icon" style="color:var(--primary);">☁️</div>
          <h3>Upload from device</h3>
          <p>Choose photos from your device</p>
          <div class="btn-upload-blue">↑ Choose Files</div>
          <p style="font-size:11px;color:var(--muted);margin-top:12px;margin-bottom:0;">Supports JPG, PNG • Up to 10MB per photo</p>
        </label>
        
        <div class="photo-divider">OR</div>
        
        <div class="photo-card" style="background:#fff;">
          <div class="photo-icon" style="color:#10B981;">📱</div>
          <h3>Upload from phone</h3>
          <p>Scan QR to upload instantly</p>
          <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=marketguru" alt="QR Code" style="width:100px;height:100px;margin-top:8px;border-radius:8px;">
        </div>
      </div>
      <input type="file" id="inp-photos" multiple accept="image/*" style="display:none;" onchange="handlePhotoSelect(event)">
      
      <div class="photo-info-box">
        <div class="photo-info-header">
          <div class="pi-icon">i</div>
          <div class="pi-text-container">
            <div class="pi-title">Upload up to 15 photos (Front, Back, Interior, Engine, RC, etc.)</div>
            <div class="pi-subtitle">More photos help you get better and faster offers.</div>
          </div>
        </div>
        <div class="photo-preview-track" id="photo-preview-track">
        </div>
      </div>
      
      <label class="drop-zone" id="drop-zone" for="inp-photos">
        ✥ You can also drag and drop photos here to upload
      </label>
    `;
    const btn = document.getElementById('btn-continue');
    btn.style.display = 'flex';
    btn.disabled = uploadedPhotos.length === 0;
    btn.innerHTML = 'CONTINUE <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
    
    // Initial render of already uploaded photos
    const track = document.getElementById('photo-preview-track');
    if (track && uploadedPhotos.length > 0) {
      uploadedPhotos.forEach((file, i) => {
        const url = URL.createObjectURL(file);
        track.innerHTML += `<div class="photo-slot" id="slot-${i}"><img src="${url}" alt="Photo ${i+1}"></div>`;
      });
    }
    
    // Setup Drag & Drop
    setTimeout(() => {
        const dz = document.getElementById('drop-zone');
        if(dz) {
            dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('dragover'); });
            dz.addEventListener('dragleave', e => dz.classList.remove('dragover'));
            dz.addEventListener('drop', e => {
              e.preventDefault();
              dz.classList.remove('dragover');
              if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                handlePhotoSelect({ target: { files: e.dataTransfer.files } });
              }
            });
        }
    }, 100);
  }
  else if (stepNum === 7) {
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    inp.innerHTML = `
      <input type="number" id="inp-km" class="input-field" placeholder="KMs Driven (e.g. 45000)" required>
      <input type="number" step="0.1" id="inp-price" class="input-field" placeholder="Expected Price in Lakhs (e.g. 5.5)" required>
      <input type="tel" id="inp-mob" class="input-field" placeholder="Your Mobile Number" required>
    `;
    const btn = document.getElementById('btn-continue');
    btn.style.display = 'flex';
    btn.disabled = false;
    btn.innerHTML = 'SUBMIT LISTING 🚀';
    
    // Auto fill mobile if logged in
    const m = localStorage.getItem('mg_current_user_mobile');
    if(m) document.getElementById('inp-mob').value = m;
  }
}
"""

start_str = "function loadStep(stepNum) {"
end_str = "function renderList(data, key, textKey) {"

start_idx = html.find(start_str)
end_idx = html.find(end_str)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_load_step + "\n" + html[end_idx:]

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully replaced loadStep")

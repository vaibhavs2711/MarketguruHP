import re

with open('sell.html', 'r', encoding='utf-8') as f:
    sell_html = f.read()

# 1. Add CSS
css_to_add = """
  /* PHOTO UPLOAD STEP */
  .photo-upload-grid { display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center; margin-bottom: 20px; }
  .photo-card { border: 1px solid var(--border); border-radius: 12px; padding: 30px 20px; text-align: center; background: var(--white); cursor: pointer; transition: all 0.2s; display:block; }
  .photo-card:hover { border-color: var(--primary); box-shadow: 0 4px 12px rgba(37,99,235,0.05); }
  .photo-card.yellow-border { border-color: #FEF3C7; }
  .photo-card.yellow-border:hover { border-color: var(--red); }
  .photo-icon { font-size: 48px; margin-bottom: 16px; display: inline-block; }
  .photo-card h3 { font-size: 16px; font-weight: 700; color: var(--charcoal); margin-bottom: 8px; }
  .photo-card p { font-size: 13px; color: var(--muted); margin-bottom: 20px; }
  .btn-upload-blue { background: var(--primary); color: var(--white); border: none; padding: 10px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; width: 100%; transition: all 0.2s; }
  .btn-upload-blue:hover { background: #1D4ED8; }
  .btn-upload-yellow { background: var(--white); color: #B45309; border: 1px solid var(--red); padding: 10px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; width: 100%; transition: all 0.2s; }
  .btn-upload-yellow:hover { background: #FFFBEB; }
  .photo-divider { font-size: 12px; font-weight: 700; color: var(--muted); position: relative; }
  .photo-divider::before, .photo-divider::after { content: ''; position: absolute; left: 50%; transform: translateX(-50%); width: 1px; height: 60px; background: var(--border); }
  .photo-divider::before { top: -70px; }
  .photo-divider::after { bottom: -70px; }
  
  .photo-info-box { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px 20px; display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }
  .pi-icon { width: 24px; height: 24px; border-radius: 50%; background: var(--primary); color: var(--white); display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; font-size:12px; }
  .pi-text-container { flex: 1; }
  .pi-title { font-size: 14px; font-weight: 700; color: var(--charcoal); margin-bottom: 4px; }
  .pi-subtitle { font-size: 12px; color: var(--muted); }
  
  .photo-preview-track { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px; }
  .photo-preview-track::-webkit-scrollbar { height: 4px; }
  .photo-preview-track::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
  .photo-slot { width: 40px; height: 40px; border: 1px dashed var(--border); border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 10px; color: var(--muted); flex-shrink: 0; position: relative; overflow: hidden; background: var(--white); }
  .photo-slot img { width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; }
  .photo-slot-icon { font-size: 12px; margin-bottom: 2px; }
  
  .drop-zone { border: 1px dashed var(--border); border-radius: 8px; padding: 16px; text-align: center; font-size: 13px; color: var(--muted); background: #FAFAFB; cursor: pointer; transition: all 0.2s; margin-bottom: 24px; display:block; }
  .drop-zone:hover, .drop-zone.dragover { border-color: var(--primary); background: var(--primary-light); color: var(--primary); }

  @media(max-width: 640px) {
    .photo-upload-grid { grid-template-columns: 1fr; gap: 10px; }
    .photo-divider { display: none; }
    .photo-info-box { flex-direction: column; align-items: flex-start; }
    .photo-preview-track { width: 100%; margin-top: 10px; }
  }
</style>
"""
sell_html = sell_html.replace('</style>', css_to_add)

# 2. Global variable and function
js_to_add = """let currentList = [];
let uploadedPhotos = [];

function handlePhotoSelect(event) {
  const files = Array.from(event.target.files || (event.dataTransfer && event.dataTransfer.files));
  if (!files || !files.length) return;
  
  sellData.photosUploaded = true;
  const btn = document.getElementById('btn-continue');
  if(btn) btn.disabled = false;
  
  uploadedPhotos = [...uploadedPhotos, ...files].slice(0, 15);
  
  for (let i = 0; i < 15; i++) {
    const slot = document.getElementById(`slot-${i}`);
    if (slot && uploadedPhotos[i]) {
      const url = URL.createObjectURL(uploadedPhotos[i]);
      slot.innerHTML = `<img src="${url}" alt="Photo ${i+1}">`;
      slot.style.border = 'none';
    } else if (slot) {
      slot.innerHTML = `<div class="photo-slot-icon">📷</div>${i+1}`;
      slot.style.border = '1px dashed var(--border)';
    }
  }
}
"""
sell_html = sell_html.replace('let currentList = [];', js_to_add)

# 3. Update loadStep 6
old_step_6 = """  else if (stepNum === 6) {
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    inp.innerHTML = `
      <label style="display:block;margin-bottom:12px;font-size:14px;font-weight:600;color:var(--charcoal);">Upload Car Photos</label>
      <input type="file" id="inp-photos" class="input-field" multiple accept="image/*" style="padding:10px; background:#fafafb; border:2px dashed var(--border);" onchange="sellData.photosUploaded = true; document.getElementById('btn-continue').disabled = false;">
      <p style="font-size:12px;color:var(--muted);margin-top:-16px;margin-bottom:24px;">Upload up to 5 photos (Front, Back, Interior, etc.)</p>
    `;
    const btn = document.getElementById('btn-continue');
    btn.style.display = 'flex';
    btn.disabled = true; // Wait for upload
    btn.innerHTML = 'CONTINUE <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
  }"""

new_step_6 = """  else if (stepNum === 6) {
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    
    let slotsHTML = '';
    for(let i=0; i<15; i++) {
      if(uploadedPhotos[i]) {
        const url = URL.createObjectURL(uploadedPhotos[i]);
        slotsHTML += `<div class="photo-slot" id="slot-${i}" style="border:none;"><img src="${url}" alt="Photo ${i+1}"></div>`;
      } else {
        slotsHTML += `<div class="photo-slot" id="slot-${i}"><div class="photo-slot-icon">📷</div>${i+1}</div>`;
      }
    }

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
        
        <label class="photo-card yellow-border" for="inp-camera">
          <div class="photo-icon">📷</div>
          <h3>Click photos</h3>
          <p>Take photos using your camera</p>
          <div class="btn-upload-yellow">📷 Open Camera</div>
        </label>
      </div>
      
      <input type="file" id="inp-photos" multiple accept="image/*" style="display:none;" onchange="handlePhotoSelect(event)">
      <input type="file" id="inp-camera" accept="image/*" capture="environment" style="display:none;" onchange="handlePhotoSelect(event)">

      <div class="photo-info-box">
        <div class="pi-icon">i</div>
        <div class="pi-text-container">
          <div class="pi-title">Upload up to 15 photos (Front, Back, Interior, Engine, RC, etc.)</div>
          <div class="pi-subtitle">More photos help you get better and faster offers.</div>
        </div>
        <div class="photo-preview-track" id="photo-preview-track">
          ${slotsHTML}
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
  }"""
sell_html = sell_html.replace(old_step_6, new_step_6)

# 4. Clear photos on reset if going back
sell_html = sell_html.replace('if(num <= 6) sellData.photosUploaded = false;', 'if(num <= 6) { sellData.photosUploaded = false; uploadedPhotos = []; }')

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(sell_html)

print("Redesigned photo upload step.")

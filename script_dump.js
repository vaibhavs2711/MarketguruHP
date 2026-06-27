
    const API_BASE = window.location.protocol === 'file:' ? 'http://localhost:5000' : '';

    const STEPS = [
      { id: 1, label: 'Brand', title: 'Select brand' },
      { id: 2, label: 'Model', title: 'Select model' },
      { id: 3, label: 'Year', title: 'Select year' },
      { id: 4, label: 'Variant', title: 'Select variant & fuel' },
      { id: 5, label: 'State', title: 'Select city' },
      { id: 6, label: 'Photos', title: 'Upload photos' },
      { id: 7, label: 'Details', title: 'Final Details' }
    ];

    let currentStep = 1;
    let sellData = { brandId: null, brand: null, modelId: null, model: null, year: null, fuel: null, trans: null, city: null, kms: null, ask: null, mobile: null };

    let currentList = [];
    let uploadedPhotos = [];

    function handlePhotoSelect(event) {
      const files = Array.from(event.target.files || (event.dataTransfer && event.dataTransfer.files));
      if (!files || !files.length) return;

      sellData.photosUploaded = true;
      const btn = document.getElementById('btn-continue');
      if (btn) btn.disabled = false;

      uploadedPhotos = [...uploadedPhotos, ...files].slice(0, 15);

      const track = document.getElementById('photo-preview-track');
      if (track) {
        track.innerHTML = '';
        uploadedPhotos.forEach((file, i) => {
          const url = URL.createObjectURL(file);
          track.innerHTML += `<div class="photo-slot" id="slot-${i}"><img src="${url}" alt="Photo ${i + 1}"></div>`;
        });
      }
    }


    document.addEventListener('DOMContentLoaded', () => {
      renderStepper();
      loadStep(currentStep);
    });

    function renderStepper() {
      const container = document.getElementById('h-stepper');
      container.innerHTML = STEPS.map(s => {
        let cls = 'h-step';
        if (s.id < currentStep) cls += ' done';
        if (s.id === currentStep) cls += ' active';
        return `<div class="h-step ${cls}" onclick="goToStep(${s.id})">
      <div class="h-step-num">${s.id}</div>
      <div class="h-step-label">${s.label}</div>
    </div>`;
      }).join('');

      // Breadcrumbs
      const bc = document.getElementById('breadcrumbs');
      let bHTML = '';
      if (sellData.brand) bHTML += `<div class="bc-pill">${sellData.brand} <span onclick="goToStep(1)">×</span></div>`;
      if (sellData.model) bHTML += `<div class="bc-pill">${sellData.model} <span onclick="goToStep(2)">×</span></div>`;
      if (sellData.year) bHTML += `<div class="bc-pill">${sellData.year} <span onclick="goToStep(3)">×</span></div>`;
      if (sellData.fuel) bHTML += `<div class="bc-pill">${sellData.fuel} ${sellData.trans || ''} <span onclick="goToStep(4)">×</span></div>`;
      if (sellData.city) bHTML += `<div class="bc-pill">${sellData.city} <span onclick="goToStep(5)">×</span></div>`;
      bc.innerHTML = bHTML;

      // Left Vertical Stepper Updates (visual sync)
      document.getElementById('v2').classList.toggle('pending', currentStep < 2);
      document.getElementById('v3').classList.toggle('pending', currentStep < 4);
      document.getElementById('v4').classList.toggle('pending', currentStep < 5);
      document.getElementById('v5').classList.toggle('pending', currentStep < 7);
    }

    function goToStep(num) {
      // Prevent jumping forward if previous steps are incomplete
      if (num > 1 && !sellData.brandId) return;
      if (num > 2 && !sellData.modelId) return;
      if (num > 3 && !sellData.year) return;
      if (num > 4 && !sellData.fuel) return;
      if (num > 5 && !sellData.city) return;
      if (num > 6 && !sellData.photosUploaded) return;

      currentStep = num;
      // Reset future data
      if (num <= 1) sellData.brand = sellData.brandId = null;
      if (num <= 2) sellData.model = sellData.modelId = null;
      if (num <= 3) sellData.year = null;
      if (num <= 4) sellData.fuel = sellData.trans = null;
      if (num <= 5) sellData.city = null;
      if (num <= 6) { sellData.photosUploaded = false; uploadedPhotos = []; }

      renderStepper();
      loadStep(currentStep);
    }

    function resetContainers() {
      document.getElementById('list-container').style.display = 'none';
      document.getElementById('grid-container').style.display = 'none';
      document.getElementById('input-container').style.display = 'none';
      document.getElementById('search-box').style.display = 'none';
      document.getElementById('search-input').value = '';
      document.getElementById('search-input').placeholder = 'Search...';
      const btn = document.getElementById('btn-continue');
      btn.style.display = 'none';
      btn.disabled = true;
      btn.innerHTML = 'CONTINUE <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
    }

    function setSelection(key, val, text, e) {
      sellData[key] = val;
      if (text) sellData[text] = e.currentTarget.getAttribute('data-name') || val;

      // Add visual selection
      const siblings = e.currentTarget.parentElement.children;
      for (let s of siblings) s.classList.remove('selected');
      e.currentTarget.classList.add('selected');

      // Auto-advance to next step
      setTimeout(nextStep, 200);
    }


    function selectVariantOpt(type, value, el) {
      sellData[type] = value;

      // Visual selection
      const cls = type === 'trans' ? 'trans-card' : 'fuel-card';
      const siblings = document.querySelectorAll('.' + cls);
      siblings.forEach(s => s.classList.remove('selected'));
      el.classList.add('selected');

      // Auto-advance if both selected
      if (sellData.trans && sellData.fuel) {
        if (type === 'fuel' || sellData.fuel) {
          setTimeout(nextStep, 400);
        }
      }
    }

    function loadStep(stepNum) {
      resetContainers();
      const title = document.getElementById('step-title');
      title.textContent = STEPS[stepNum - 1].title;

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
        for (let y = 2026; y >= 2010; y--) {
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
      }
      else if (stepNum === 5) {
        document.getElementById('search-box').style.display = 'block';
        document.getElementById('search-input').placeholder = 'Search City...';

        const grid = document.getElementById('grid-container');
        grid.style.display = 'grid';
        grid.innerHTML = `
      <div class="grid-opt" onclick="setSelection('city', 'Ahmedabad', null, event)">Ahmedabad</div>
      <div class="grid-opt" onclick="setSelection('city', 'Amreli', null, event)">Amreli</div>
      <div class="grid-opt" onclick="setSelection('city', 'Anand', null, event)">Anand</div>
      <div class="grid-opt" onclick="setSelection('city', 'Anjar', null, event)">Anjar</div>
      <div class="grid-opt" onclick="setSelection('city', 'Bharuch', null, event)">Bharuch</div>
      <div class="grid-opt" onclick="setSelection('city', 'Bhavnagar', null, event)">Bhavnagar</div>
      <div class="grid-opt" onclick="setSelection('city', 'Bhuj', null, event)">Bhuj</div>
      <div class="grid-opt" onclick="setSelection('city', 'Botad', null, event)">Botad</div>
      <div class="grid-opt" onclick="setSelection('city', 'Dahod', null, event)">Dahod</div>
      <div class="grid-opt" onclick="setSelection('city', 'Deesa', null, event)">Deesa</div>
      <div class="grid-opt" onclick="setSelection('city', 'Dholka', null, event)">Dholka</div>
      <div class="grid-opt" onclick="setSelection('city', 'Dwarka', null, event)">Dwarka</div>
      <div class="grid-opt" onclick="setSelection('city', 'Gandhidham', null, event)">Gandhidham</div>
      <div class="grid-opt" onclick="setSelection('city', 'Gandhinagar', null, event)">Gandhinagar</div>
      <div class="grid-opt" onclick="setSelection('city', 'Godhra', null, event)">Godhra</div>
      <div class="grid-opt" onclick="setSelection('city', 'Jamnagar', null, event)">Jamnagar</div>
      <div class="grid-opt" onclick="setSelection('city', 'Jetpur', null, event)">Jetpur</div>
      <div class="grid-opt" onclick="setSelection('city', 'Junagadh', null, event)">Junagadh</div>
      <div class="grid-opt" onclick="setSelection('city', 'Kalol', null, event)">Kalol</div>
      <div class="grid-opt" onclick="setSelection('city', 'Lunawada', null, event)">Lunawada</div>
      <div class="grid-opt" onclick="setSelection('city', 'Mehsana', null, event)">Mehsana</div>
      <div class="grid-opt" onclick="setSelection('city', 'Modasa', null, event)">Modasa</div>
      <div class="grid-opt" onclick="setSelection('city', 'Morbi', null, event)">Morbi</div>
      <div class="grid-opt" onclick="setSelection('city', 'Mundra', null, event)">Mundra</div>
      <div class="grid-opt" onclick="setSelection('city', 'Nadiad', null, event)">Nadiad</div>
      <div class="grid-opt" onclick="setSelection('city', 'Navsari', null, event)">Navsari</div>
      <div class="grid-opt" onclick="setSelection('city', 'Palanpur', null, event)">Palanpur</div>
      <div class="grid-opt" onclick="setSelection('city', 'Patan', null, event)">Patan</div>
      <div class="grid-opt" onclick="setSelection('city', 'Porbandar', null, event)">Porbandar</div>
      <div class="grid-opt" onclick="setSelection('city', 'Rajkot', null, event)">Rajkot</div>
      <div class="grid-opt" onclick="setSelection('city', 'Somnath', null, event)">Somnath</div>
      <div class="grid-opt" onclick="setSelection('city', 'Surat', null, event)">Surat</div>
      <div class="grid-opt" onclick="setSelection('city', 'Surendranagar', null, event)">Surendranagar</div>
      <div class="grid-opt" onclick="setSelection('city', 'Vadodara', null, event)">Vadodara</div>
      <div class="grid-opt" onclick="setSelection('city', 'Valsad', null, event)">Valsad</div>
      <div class="grid-opt" onclick="setSelection('city', 'Vapi', null, event)">Vapi</div>
      <div class="grid-opt" onclick="setSelection('city', 'Veraval', null, event)">Veraval</div>
      <div class="grid-opt" onclick="setSelection('city', 'Visnagar', null, event)">Visnagar</div>
      <div class="grid-opt" onclick="setSelection('city', 'Vyara', null, event)">Vyara</div>
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
            track.innerHTML += `<div class="photo-slot" id="slot-${i}"><img src="${url}" alt="Photo ${i + 1}"></div>`;
          });
        }

        // Setup Drag & Drop
        setTimeout(() => {
          const dz = document.getElementById('drop-zone');
          if (dz) {
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
        if (m) document.getElementById('inp-mob').value = m;
      }
    }

    function renderList(data, key, textKey) {
      const list = document.getElementById('list-container');
      if (!data.length) {
        list.innerHTML = '<div style="padding:20px;text-align:center;color:#666;">No results found.</div>';
        return;
      }

      const fileMap = {
        'marutisuzuki': 'marutisuzuki.png',
        'hyundai': 'hyundai.png',
        'tata': 'tata.png',
        'mahindra': 'mahindra.webp',
        'honda': 'honda.png',
        'toyota': 'toyota.png',
        'kia': 'Kia.png',
        'mg': 'MG.png',
        'renault': 'renault.png',
        'skoda': 'skoda.png',
        'volkswagen': 'volkswagon.png',
        'ford': 'fird.png',
        'nissan': 'Nissan.png',
        'jeep': 'Jeep.png',
        'citroen': 'citroen.png',
        'byd': 'BYD.png',
        'forcemotors': 'forcemotors.jpg',
        'bmw': 'bmw.png',
        'mercedesbenz': 'mercedes-benz.png',
        'audi': 'audi.png',
        'volvo': 'volvo.png',
        'jaguar': 'jaguar.png',
        'landrover': 'Landrover.png',
        'lexus': 'lexus.png',
        'mini': 'minicooper.png',
        'porsche': 'Porsche.png',
        'astonmartin': 'astonmartin.png',
        'ferrari': 'ferrari.png',
        'lamborghini': 'lamborghini.png',
        'bentley': 'bentley.png',
        'rollsroyce': 'rolls-royce.png',
        'maserati': 'maserati.png',
        'mclaren': 'maclaren.png',
        'chevrolet': 'chevrolet.png',
        'fiat': 'fiat.png',
        'datsun': 'datsun.png',
        'mitsubishi': 'Mitsubishi.png',
        'hindustanmotors': 'hindustanmotors.webp',
        'isuzu': 'isuzu.png'
      };

      list.innerHTML = data.map(item => {
        let imgHTML = `<div class="item-img">${key === 'brandId' ? '🚙' : '🚗'}</div>`;

        if (key === 'brandId') {
          const brandStr = item.name.toLowerCase().replace(/[\s-]/g, '');
          const fileName = fileMap[brandStr];
          if (fileName) {
            imgHTML = `<div class="item-img"><img src="car_make_logo_images/${fileName}" alt="${item.name}" style="width:36px;height:36px;object-fit:contain;" onerror="this.outerHTML='🚙'"></div>`;
          }
        }

        return `
      <div class="list-item" data-name="${item.name}" onclick="setSelection('${key}', ${item.id}, '${textKey}', event)">
        ${imgHTML}
        <div class="item-name">${item.name}</div>
        <div class="item-arrow">›</div>
      </div>
    `;
      }).join('');
    }

    function filterList() {
      const q = document.getElementById('search-input').value.toLowerCase();

      if (currentStep === 5) {
        const opts = document.querySelectorAll('#grid-container .grid-opt');
        opts.forEach(opt => {
          if (opt.textContent.toLowerCase().includes(q)) {
            opt.style.display = 'block';
          } else {
            opt.style.display = 'none';
          }
        });
        return;
      }

      const filtered = currentList.filter(i => i.name.toLowerCase().includes(q));
      const key = currentStep === 1 ? 'brandId' : 'modelId';
      const textKey = currentStep === 1 ? 'brand' : 'model';
      renderList(filtered, key, textKey);
    }

    function nextStep() {
      if (currentStep === 7) {
        submitListing();
        return;
      }
      currentStep++;
      renderStepper();
      loadStep(currentStep);
    }

    function submitListing() {
      const km = document.getElementById('inp-km').value;
      const price = document.getElementById('inp-price').value;
      const mob = document.getElementById('inp-mob').value;

      if (!km || !price || !mob) {
        showToast('⚠️ Please fill all fields.');
        return;
      }

      let userType = 'private';
      try {
        const user = JSON.parse(localStorage.getItem('mg_current_user'));
        if (user && user.role) userType = user.role;
      } catch (e) { }

      const payload = {
        name: sellData.brand + ' ' + sellData.model,
        year: parseInt(sellData.year),
        price: parseFloat(price).toFixed(2),
        priceN: Math.round(parseFloat(price) * 100000),
        km: parseInt(km).toLocaleString('en-IN'),
        fuel: sellData.fuel,
        trans: sellData.trans,
        owner: '1st Owner',
        color: '#e8eef5',
        emoji: '🚗',
        image: '',
        city: sellData.city,
        desc: `Clean ${sellData.brand} ${sellData.model}`,
        features: ['Power Windows', 'Airbags', 'ABS'],
        listed_by: mob,
        user_type: userType
      };

      if (uploadedPhotos && uploadedPhotos.length > 0) {
        const promises = uploadedPhotos.map(file => {
          return new Promise((resolve) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => resolve(null);
          });
        });

        Promise.all(promises).then(results => {
          const validImages = results.filter(r => r !== null);
          if (validImages.length > 0) {
            payload.image = validImages[0]; // Set first as main image
            payload.images = validImages;   // Set all as array
          }
          sendPayload(payload, mob);
        });
      } else {
        sendPayload(payload, mob);
      }
    }

    function sendPayload(payload, mob) {
      fetch(API_BASE + '/api/cars', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(r => r.json())
        .then(data => {
          if (data.status === 'error') {
            if (data.message.includes('limited to exactly 1 car')) {
              showUpgradeModal();
            } else {
              showToast('❌ ' + data.message);
            }
            return;
          }
          localStorage.setItem('mg_current_user_mobile', mob);
          if (!localStorage.getItem('mg_current_user')) {
            localStorage.setItem('mg_current_user', JSON.stringify({ id: 999, name: 'Guest', mobile: mob, role: 'customer' }));
          }
          showToast('🎉 Listing submitted successfully!');
          setTimeout(() => {
            window.location.href = 'customer-dashboard.html';
          }, 2000);
        })
        .catch(err => {
          console.error(err);
          showToast('❌ Error submitting listing.');
        });
    }

    function showUpgradeModal() {
      const overlay = document.getElementById('upgradeModal');
      if (overlay) overlay.classList.add('show');
    }

    function hideUpgradeModal() {
      const overlay = document.getElementById('upgradeModal');
      if (overlay) overlay.classList.remove('show');
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2500);
    }

    function checkLoginState() {
      const currentUser = localStorage.getItem('mg_current_user');
      const navActions = document.getElementById('nav-actions');
      if (navActions) {
        if (currentUser) {
          let initials = '👤';
          try {
            const userObj = JSON.parse(currentUser);
            const name = userObj.name || '';
            if (name) {
              const parts = name.split(' ');
              initials = parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : name.substring(0, 2).toUpperCase();
            }
          } catch (e) { }
          navActions.innerHTML = `
        <a href="customer-dashboard.html" title="My Profile" style="text-decoration:none; display:block;">
          <div style="width: 42px; height: 42px; border-radius: 50%; background: rgba(255, 204, 0, 0.15); border: 2px solid var(--red); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: var(--red); text-transform: uppercase; transition: all 0.2s;">
            ${initials}
          </div>
        </a>
      `;
        } else {
          navActions.innerHTML = `<a href="login.html" style="text-decoration:none;"><button class="btn-outline-white">Login</button></a>`;
        }
      }
    }
    checkLoginState();

  
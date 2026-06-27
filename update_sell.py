import json

# Define the HTML content
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<script>
  if (!localStorage.getItem('mg_current_user')) {
    window.location.replace('login.html?redirect=sell.html');
  }
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sell Your Car - Market Guru HP</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --red: #FFCC00; 
    --red-dark: #F59E0B; 
    --charcoal: #1A1A2E; 
    --silver: #F9FAFB; 
    --white: #FFFFFF; 
    --text: #1F2937; 
    --muted: #6B7A99; 
    --border: #E5E7EB; 
    --primary: #2563EB;
    --primary-light: #EFF6FF;
    --primary-hover: #DBEAFE;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  body{font-family:'Inter',sans-serif;color:var(--text);background:var(--silver);}
  a{text-decoration:none;color:inherit;}

  /* NAVBAR */
  .navbar{background:var(--white);position:sticky;top:0;z-index:100;}
  .nav-main{max-width:1280px;margin:0 auto;display:flex;align-items:center;padding:0 20px;height:80px;}
  .logo{height:60px;margin-right:auto;}
  .logo img{height:100%;width:auto;display:block;}
  .nav-links{display:flex;gap:32px;align-items:center;position:absolute;left:50%;transform:translateX(-50%);height:100%;}
  .nav-links a{color:#4B5563;font-size:15px;font-weight:600;height:100%;display:flex;align-items:center;border-bottom:3px solid transparent;transition:all 0.2s;}
  .nav-links a:hover{color:var(--charcoal);}
  .nav-links a.active{color:var(--red);border-bottom-color:var(--red);}
  .nav-user{width:42px;height:42px;border-radius:50%;border:2px solid var(--primary-light);color:var(--primary);display:flex;align-items:center;justify-content:center;font-size:20px;margin-left:auto;cursor:pointer;}

  /* HERO */
  .sell-hero{max-width:1280px;margin:40px auto 30px;padding:0 20px;display:flex;justify-content:space-between;align-items:center;}
  .hero-text h1{font-size:42px;font-weight:800;color:var(--charcoal);margin-bottom:12px;letter-spacing:-0.5px;}
  .hero-text h1 span{color:var(--red);}
  .hero-text p{color:var(--muted);font-size:16px;font-weight:500;}
  .hero-img{height:130px;display:flex;align-items:flex-end;font-size:80px;line-height:1;}

  /* PORTAL */
  .portal-container{max-width:1280px;margin:0 auto 60px;padding:0 20px;}
  .portal-box{background:var(--white);border-radius:16px;border:1px solid var(--border);box-shadow:0 10px 40px rgba(0,0,0,0.03);display:grid;grid-template-columns:280px 1fr 280px;min-height:600px;}
  
  /* LEFT VERTICAL STEPS */
  .p-left{padding:40px 30px;border-right:1px solid var(--border);background:#FAFAFB;border-top-left-radius:16px;border-bottom-left-radius:16px;}
  .v-step{display:flex;gap:16px;margin-bottom:40px;position:relative;}
  .v-step:not(:last-child)::after{content:'';position:absolute;left:16px;top:40px;bottom:-30px;width:1px;background:var(--border);z-index:1;}
  .v-step-num{width:32px;height:32px;border-radius:50%;background:var(--primary);color:var(--white);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;z-index:2;position:relative;flex-shrink:0;}
  .v-step.pending .v-step-num{background:var(--white);color:var(--muted);border:1px solid var(--border);}
  .v-step-icon{width:40px;height:40px;border-radius:50%;background:var(--white);border:1px solid var(--primary-light);display:flex;align-items:center;justify-content:center;color:var(--primary);font-size:18px;margin-top:-4px;box-shadow:0 4px 10px rgba(37,99,235,0.1);flex-shrink:0;}
  .v-step.pending .v-step-icon{border-color:var(--border);color:var(--muted);box-shadow:none;}
  .v-step-text{padding-top:2px;}
  .v-step-title{font-size:14px;font-weight:700;color:var(--charcoal);margin-bottom:4px;}
  .v-step-sub{font-size:12px;color:var(--muted);}

  /* MIDDLE HORIZONTAL STEPS & FORMS */
  .p-mid{padding:40px 60px;}
  .h-stepper{display:flex;align-items:center;justify-content:space-between;margin-bottom:30px;position:relative;}
  .h-stepper::before{content:'';position:absolute;left:20px;right:20px;top:16px;height:1.5px;background:var(--border);z-index:1;}
  .h-step{display:flex;flex-direction:column;align-items:center;gap:8px;position:relative;z-index:2;background:var(--white);padding:0 10px;}
  .h-step-num{width:32px;height:32px;border-radius:50%;background:var(--silver);color:var(--muted);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;border:1px solid var(--border);transition:all 0.2s;}
  .h-step.active .h-step-num{background:var(--primary);color:var(--white);border-color:var(--primary);}
  .h-step.done .h-step-num{background:var(--charcoal);color:var(--white);border-color:var(--charcoal);}
  .h-step-label{font-size:12px;font-weight:600;color:var(--muted);}
  .h-step.active .h-step-label{color:var(--charcoal);}

  .breadcrumbs{display:flex;gap:10px;margin-bottom:24px;flex-wrap:wrap;min-height:30px;}
  .bc-pill{background:var(--primary-light);color:var(--primary);padding:6px 14px;border-radius:20px;font-size:13px;font-weight:600;display:flex;align-items:center;gap:6px;}
  .bc-pill span{cursor:pointer;opacity:0.6;}
  .bc-pill span:hover{opacity:1;}

  .step-title{font-size:18px;font-weight:700;margin-bottom:16px;}
  
  .search-bar{position:relative;margin-bottom:20px;}
  .search-bar input{width:100%;padding:14px 14px 14px 44px;border:1px solid var(--border);border-radius:8px;font-size:14px;color:var(--text);font-family:'Inter',sans-serif;}
  .search-bar input:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,0.1);}
  .search-bar svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--primary);width:18px;height:18px;}

  .list-container{border:1px solid var(--border);border-radius:8px;max-height:350px;overflow-y:auto;margin-bottom:24px;background:var(--white);}
  .list-item{display:flex;align-items:center;padding:12px 16px;border-bottom:1px solid var(--border);cursor:pointer;transition:all 0.2s;}
  .list-item:last-child{border-bottom:none;}
  .list-item:hover{background:var(--primary-hover);}
  .list-item.selected{background:var(--primary-light);border-left:3px solid var(--primary);}
  .item-img{font-size:24px;margin-right:16px;width:30px;text-align:center;}
  .item-name{font-size:14px;font-weight:600;flex:1;}
  .item-arrow{color:var(--primary);font-size:18px;}

  /* GRID FOR NON-LIST OPTIONS */
  .grid-options{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px;}
  .grid-opt{border:1px solid var(--border);border-radius:8px;padding:16px;text-align:center;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.2s;}
  .grid-opt:hover{background:var(--primary-hover);border-color:var(--primary);}
  .grid-opt.selected{background:var(--primary-light);border-color:var(--primary);color:var(--primary);}

  .input-field{width:100%;padding:14px;border:1px solid var(--border);border-radius:8px;font-size:15px;margin-bottom:24px;font-family:'Inter',sans-serif;}
  .input-field:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,0.1);}

  .btn-continue{width:100%;padding:16px;background:var(--red);color:var(--charcoal);border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;transition:all 0.2s;}
  .btn-continue:hover{background:var(--red-dark);transform:translateY(-1px);}
  .btn-continue:disabled{opacity:0.5;cursor:not-allowed;transform:none;}
  
  .secure-text{text-align:center;font-size:12px;color:var(--muted);margin-top:20px;display:flex;align-items:center;justify-content:center;gap:6px;}

  /* RIGHT FEATURES */
  .p-right{padding:40px 30px;background:#FFFBF0;border-left:1px solid #FEF3C7;border-top-right-radius:16px;border-bottom-right-radius:16px;}
  .feature-card{background:var(--white);border-radius:12px;padding:20px;display:flex;align-items:center;gap:16px;margin-bottom:16px;box-shadow:0 4px 12px rgba(0,0,0,0.02);border:1px solid #FEF3C7;}
  .f-icon{width:48px;height:48px;border-radius:50%;background:#FFFBEB;display:flex;align-items:center;justify-content:center;color:var(--red-dark);font-size:20px;flex-shrink:0;}
  .f-icon.blue{background:var(--primary-light);color:var(--primary);}
  .f-text{font-size:14px;font-weight:700;color:var(--charcoal);line-height:1.4;}

  /* Toast */
  .toast{position:fixed;bottom:24px;right:24px;z-index:9999;background:var(--charcoal);color:#fff;padding:14px 20px;border-radius:10px;font-size:14px;font-weight:500;box-shadow:0 8px 24px rgba(0,0,0,0.3);transform:translateY(100px);transition:transform 0.3s ease;border-left:4px solid var(--red);}
  .toast.show{transform:translateY(0);}

  @media(max-width: 1024px) {
    .portal-box{grid-template-columns:1fr;display:flex;flex-direction:column;}
    .p-left, .p-right{display:none;}
    .nav-links{display:none;}
  }
  @media(max-width: 640px) {
    .h-stepper { overflow-x: auto; padding-bottom: 10px; }
    .grid-options { grid-template-columns: repeat(2,1fr); }
  }
</style>
</head>
<body>

<nav class="navbar">
  <div class="nav-main">
    <a href="index.html" class="logo">
      <img src="logo.png" alt="Market Guru HP Logo">
    </a>
    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="buy-cars.html">Buy Vehicle</a>
      <a href="sell.html" class="active">Sell Vehicle</a>
      <a href="about.html">About</a>
    </div>
    <a href="customer-dashboard.html" class="nav-user" id="nav-user">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
    </a>
  </div>
</nav>

<div class="sell-hero">
  <div class="hero-text">
    <h1>Sell Your Car, Get the <span>Best Price</span></h1>
    <p>List your car in 4 simple steps and get the best value with complete peace of mind.</p>
  </div>
  <div class="hero-img">🤝🚗</div>
</div>

<div class="portal-container">
  <div class="portal-box">
    
    <!-- LEFT -->
    <div class="p-left">
      <div class="v-step" id="v1">
        <div class="v-step-num">1</div><div class="v-step-icon">🚗</div>
        <div class="v-step-text"><div class="v-step-title">Tell us about your car</div><div class="v-step-sub">Provide basic details</div></div>
      </div>
      <div class="v-step pending" id="v2">
        <div class="v-step-num">2</div><div class="v-step-icon">📄</div>
        <div class="v-step-text"><div class="v-step-title">List your first car for free</div><div class="v-step-sub">Create your listing</div></div>
      </div>
      <div class="v-step pending" id="v3">
        <div class="v-step-num">3</div><div class="v-step-icon">₹</div>
        <div class="v-step-text"><div class="v-step-title">Get the best deal</div><div class="v-step-sub">Receive the highest offers</div></div>
      </div>
      <div class="v-step pending" id="v4">
        <div class="v-step-num">4</div><div class="v-step-icon">👥</div>
        <div class="v-step-text"><div class="v-step-title">Find the perfect buyer</div><div class="v-step-sub">We connect you directly</div></div>
      </div>
      <div class="v-step pending" id="v5">
        <div class="v-step-num">5</div><div class="v-step-icon">🛡️</div>
        <div class="v-step-text"><div class="v-step-title">Sell hassle free</div><div class="v-step-sub">Complete the sale easily</div></div>
      </div>
    </div>

    <!-- MIDDLE -->
    <div class="p-mid">
      <div class="h-stepper" id="h-stepper">
        <!-- Generated by JS -->
      </div>
      
      <div class="breadcrumbs" id="breadcrumbs">
        <!-- Generated by JS -->
      </div>

      <div class="step-title" id="step-title">Loading...</div>
      
      <div class="search-bar" id="search-box" style="display:none;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="search-input" placeholder="Search..." oninput="filterList()">
      </div>

      <div class="list-container" id="list-container" style="display:none;"></div>
      <div class="grid-options" id="grid-container" style="display:none;"></div>
      <div id="input-container" style="display:none;"></div>

      <button class="btn-continue" id="btn-continue" onclick="nextStep()" disabled>
        CONTINUE <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
      </button>
      
      <div class="secure-text">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
        Your information is safe with us and will never be shared.
      </div>
    </div>

    <!-- RIGHT -->
    <div class="p-right">
      <div class="feature-card"><div class="f-icon">🤝</div><div class="f-text">Direct Connect</div></div>
      <div class="feature-card"><div class="f-icon blue">🛡️</div><div class="f-text">Transparent Info</div></div>
      <div class="feature-card"><div class="f-icon">₹</div><div class="f-text">Zero Broker Fee</div></div>
      <div class="feature-card"><div class="f-icon blue">📍</div><div class="f-text">All Gujarat,<br>One Platform</div></div>
    </div>

  </div>
</div>
<div class="toast" id="toast"></div>

<!-- JS -->
<script src="db.js"></script>
<script>
const API_BASE = window.location.protocol === 'file:' ? 'http://localhost:5000' : '';

const STEPS = [
  { id: 1, label: 'Brand', title: 'Select brand' },
  { id: 2, label: 'Model', title: 'Select model' },
  { id: 3, label: 'Year', title: 'Select year' },
  { id: 4, label: 'Variant', title: 'Select variant & fuel' },
  { id: 5, label: 'State', title: 'Select city' },
  { id: 6, label: 'Details', title: 'Final Details' }
];

let currentStep = 1;
let sellData = { brandId: null, brand: null, modelId: null, model: null, year: null, fuel: null, trans: null, city: null, kms: null, ask: null, mobile: null };

let currentList = [];

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
    return `<div class="h-step ${cls}">
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
  if (sellData.fuel) bHTML += `<div class="bc-pill">${sellData.fuel} ${sellData.trans||''} <span onclick="goToStep(4)">×</span></div>`;
  if (sellData.city) bHTML += `<div class="bc-pill">${sellData.city} <span onclick="goToStep(5)">×</span></div>`;
  bc.innerHTML = bHTML;
  
  // Left Vertical Stepper Updates (visual sync)
  if(currentStep >= 2) { document.getElementById('v2').classList.remove('pending'); }
  if(currentStep >= 4) { document.getElementById('v3').classList.remove('pending'); }
  if(currentStep >= 5) { document.getElementById('v4').classList.remove('pending'); }
  if(currentStep >= 6) { document.getElementById('v5').classList.remove('pending'); }
}

function goToStep(num) {
  currentStep = num;
  // Reset future data
  if(num <= 1) sellData.brand = sellData.brandId = null;
  if(num <= 2) sellData.model = sellData.modelId = null;
  if(num <= 3) sellData.year = null;
  if(num <= 4) sellData.fuel = sellData.trans = null;
  if(num <= 5) sellData.city = null;
  
  renderStepper();
  loadStep(currentStep);
}

function resetContainers() {
  document.getElementById('list-container').style.display = 'none';
  document.getElementById('grid-container').style.display = 'none';
  document.getElementById('input-container').style.display = 'none';
  document.getElementById('search-box').style.display = 'none';
  document.getElementById('search-input').value = '';
  document.getElementById('btn-continue').disabled = true;
  document.getElementById('btn-continue').innerHTML = 'CONTINUE <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
}

function setSelection(key, val, text, e) {
  sellData[key] = val;
  if(text) sellData[text] = e.currentTarget.getAttribute('data-name') || val;
  
  // Add visual selection
  const siblings = e.currentTarget.parentElement.children;
  for(let s of siblings) s.classList.remove('selected');
  e.currentTarget.classList.add('selected');
  
  document.getElementById('btn-continue').disabled = false;
}

function loadStep(stepNum) {
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
    for(let y=2024; y>=2010; y--) {
      yHTML += `<div class="grid-opt" onclick="setSelection('year', '${y}', null, event)">${y}</div>`;
    }
    grid.innerHTML = yHTML;
  }
  else if (stepNum === 4) {
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
      <input type="number" id="inp-km" class="input-field" placeholder="KMs Driven (e.g. 45000)" required>
      <input type="number" step="0.1" id="inp-price" class="input-field" placeholder="Expected Price in Lakhs (e.g. 5.5)" required>
      <input type="tel" id="inp-mob" class="input-field" placeholder="Your Mobile Number" required>
    `;
    const btn = document.getElementById('btn-continue');
    btn.disabled = false;
    btn.innerHTML = 'SUBMIT LISTING 🚀';
    
    // Auto fill mobile if logged in
    const m = localStorage.getItem('mg_current_user_mobile');
    if(m) document.getElementById('inp-mob').value = m;
  }
}

function renderList(data, key, textKey) {
  const list = document.getElementById('list-container');
  if(!data.length) {
    list.innerHTML = '<div style="padding:20px;text-align:center;color:#666;">No results found.</div>';
    return;
  }
  list.innerHTML = data.map(item => `
    <div class="list-item" data-name="${item.name}" onclick="setSelection('${key}', ${item.id}, '${textKey}', event)">
      <div class="item-img">${key==='brandId' ? '🚙' : '🚗'}</div>
      <div class="item-name">${item.name}</div>
      <div class="item-arrow">›</div>
    </div>
  `).join('');
}

function filterList() {
  const q = document.getElementById('search-input').value.toLowerCase();
  const filtered = currentList.filter(i => i.name.toLowerCase().includes(q));
  const key = currentStep === 1 ? 'brandId' : 'modelId';
  const textKey = currentStep === 1 ? 'brand' : 'model';
  renderList(filtered, key, textKey);
}

function nextStep() {
  if (currentStep === 6) {
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
  
  if(!km || !price || !mob) {
    showToast('⚠️ Please fill all fields.');
    return;
  }
  
  // Submit to DB
  mgDB.addUserCar({
    name: sellData.brand + ' ' + sellData.model,
    year: parseInt(sellData.year),
    price: parseFloat(price).toFixed(2),
    priceN: Math.round(parseFloat(price) * 100000),
    km: parseInt(km).toLocaleString('en-IN'),
    fuel: sellData.fuel,
    trans: sellData.trans,
    owner: '1st Owner', // Default
    color: '#e8eef5',
    emoji: '🚗',
    image: '',
    city: sellData.city,
    desc: `Clean ${sellData.brand} ${sellData.model}`,
    features: ['Power Windows', 'Airbags', 'ABS']
  });
  
  localStorage.setItem('mg_current_user_mobile', mob);
  if (!localStorage.getItem('mg_current_user')) {
    localStorage.setItem('mg_current_user', 'Guest');
  }

  showToast('🎉 Listing submitted successfully!');
  setTimeout(() => {
    window.location.href = 'customer-dashboard.html';
  }, 2000);
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 2500);
}
</script>
</body>
</html>"""

with open("sell.html", "w", encoding="utf-8") as f:
    f.write(html_content)

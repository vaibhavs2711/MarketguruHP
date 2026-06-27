
// Responsive Navbar Toggle
document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  const navActions = document.querySelector('.nav-actions');
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      menuToggle.classList.toggle('active');
      if (navLinks) navLinks.classList.toggle('active');
      if (navActions) navActions.classList.toggle('active');
    });
  }
});

let allCars = [];
let filteredCars = [];
let currentPage = 1;
const carsPerPage = 4;

function initPage() {
  allCars = mgDB.getUsedCars();
  parseQueryParams();
  applyFilters();
}

function parseQueryParams() {
  const params = new URLSearchParams(window.location.search);
  
  // Brand
  const brand = params.get('brand');
  if (brand) {
    const brandLower = brand.toLowerCase();
    let targetMake = '';
    if (brandLower.includes('maruti')) targetMake = 'maruti suzuki';
    else if (brandLower.includes('hyundai')) targetMake = 'hyundai';
    else if (brandLower.includes('honda')) targetMake = 'honda';
    else if (brandLower.includes('toyota')) targetMake = 'toyota';
    else if (brandLower.includes('tata')) targetMake = 'tata';
    else if (brandLower.includes('mahindra')) targetMake = 'mahindra';
    else if (brandLower.includes('kia')) targetMake = 'kia';

    if (targetMake) {
      document.querySelectorAll('.make-checkbox').forEach(cb => {
        if (cb.value.toLowerCase() === targetMake) {
          cb.checked = true;
        }
      });
    }
  }

  // Budget
  const budget = params.get('budget');
  if (budget) {
    const priceSel = document.getElementById('priceSelect');
    if (budget.includes('1-2') || budget.includes('1 to 2') || budget.includes('1to2')) {
      priceSel.value = '1-2';
    } else if (budget.includes('2-3') || budget.includes('2 to 3') || budget.includes('2to3')) {
      priceSel.value = '2-3';
    } else if (budget.includes('3-5') || budget.includes('3 to 5') || budget.includes('3to5')) {
      priceSel.value = '3-5';
    } else if (budget.includes('5-7') || budget.includes('5 to 7') || budget.includes('5to7')) {
      priceSel.value = '5-7';
    } else if (budget.includes('7+') || budget.includes('7 plus')) {
      priceSel.value = '7+';
    }
  }
}

function renderCars() {
  const list = document.getElementById('carList');
  document.getElementById('count').textContent = filteredCars.length;

  if (filteredCars.length === 0) {
    list.innerHTML = `
      <div style="padding:40px; text-align:center; background:#fff; border-radius:12px; border:1.5px solid var(--border)">
        <h3>No cars match your criteria</h3>
        <p style="color:var(--muted); margin-top:8px">Try clearing filters or search query to find more options.</p>
      </div>`;
    renderPagination(0);
    return;
  }

  // Pagination slice
  const startIndex = (currentPage - 1) * carsPerPage;
  const endIndex = startIndex + carsPerPage;
  const visibleCars = filteredCars.slice(startIndex, endIndex);

  list.innerHTML = visibleCars.map(c => `
    <div class="car-list-item" onclick="window.location='car-detail.html?id=${c.id}'">
      <div class="car-list-img" style="background:linear-gradient(135deg,${c.color || '#e8eef5'},#ccd4e0)">
        ${c.image ? `<img src="${c.image}" style="width:100%;height:100%;object-fit:contain;" />` : `<span style="font-size:80px">${c.emoji || '🚗'}</span>`}
      </div>
      <div class="car-list-info">
        <div class="car-list-name">${c.name}</div>
        <div class="car-list-sub">${c.year} · ${c.km} km · ${c.owner || '1st Owner'} · ${c.city || 'Vadodara'}</div>
        <div class="car-specs">
          <div class="spec-item"><span class="spec-icon">⛽</span>${c.fuel}</div>
          <div class="spec-item"><span class="spec-icon">⚙️</span>${c.trans}</div>
          <div class="spec-item"><span class="spec-icon">👤</span>${c.owner || '1st Owner'}</div>
          <div class="spec-item"><span class="spec-icon">📍</span>${c.city || 'Vadodara'}</div>
        </div>
        <div class="car-features">
          ${(c.features || []).slice(0, 4).map(f => `<span class="feature-tag">${f}</span>`).join('')}
        </div>
        <p style="font-size:12px;color:var(--muted);margin-top:10px">${c.desc || ''}</p>
      </div>
      <div class="car-list-action">
        <div>
          <div class="car-price-big">₹${c.price}L</div>
        </div>
        <div style="width:100%">
          <button class="btn-details" onclick="event.stopPropagation();window.location='car-detail.html?id=${c.id}'">View Details</button>
          <button class="btn-call" onclick="event.stopPropagation();contactSeller(${c.id})">📞 Contact</button>
          <div class="compare-check" onclick="event.stopPropagation()">
            <input type="checkbox" id="comp-${c.id}" onchange="toggleCompare(${c.id})">
            <label for="comp-${c.id}">Add to Compare</label>
          </div>
        </div>
      </div>
    </div>
  `).join('');

  renderPagination(filteredCars.length);
}

function renderPagination(totalCount) {
  const totalPages = Math.ceil(totalCount / carsPerPage);
  const container = document.querySelector('.pagination');
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  let html = `<button class="page-btn" onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled style="opacity:0.5; cursor:default"' : ''}>‹</button>`;
  
  for (let i = 1; i <= totalPages; i++) {
    html += `<button class="page-btn ${currentPage === i ? 'active' : ''}" onclick="changePage(${i})">${i}</button>`;
  }
  
  html += `<button class="page-btn" onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled style="opacity:0.5; cursor:default"' : ''}>›</button>`;
  
  container.innerHTML = html;
}

function changePage(p) {
  const totalPages = Math.ceil(filteredCars.length / carsPerPage);
  if (p < 1 || p > totalPages) return;
  currentPage = p;
  renderCars();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function applyFilters() {
  let list = [...allCars];

  // Budget Select Filter
  const priceRange = document.getElementById('priceSelect').value;
  if (priceRange) {
    if (priceRange === '1-2') {
      list = list.filter(c => parseFloat(c.price) >= 1.0 && parseFloat(c.price) <= 2.0);
    } else if (priceRange === '2-3') {
      list = list.filter(c => parseFloat(c.price) >= 2.0 && parseFloat(c.price) <= 3.0);
    } else if (priceRange === '3-5') {
      list = list.filter(c => parseFloat(c.price) >= 3.0 && parseFloat(c.price) <= 5.0);
    } else if (priceRange === '5-7') {
      list = list.filter(c => parseFloat(c.price) >= 5.0 && parseFloat(c.price) <= 7.0);
    } else if (priceRange === '7+') {
      list = list.filter(c => parseFloat(c.price) >= 7.0);
    }
  }

  // Gather selected Makes & Models
  const checkedMakes = Array.from(document.querySelectorAll('.make-checkbox:checked')).map(cb => cb.value);
  const checkedModels = Array.from(document.querySelectorAll('.model-checkbox:checked')).map(cb => cb.value);

  const dropdownText = document.getElementById('brandDropdownText');
  if (dropdownText) {
    if (checkedMakes.length === 0 && checkedModels.length === 0) {
      dropdownText.textContent = 'All Brands';
    } else {
      const total = checkedMakes.length + checkedModels.length;
      dropdownText.textContent = total + ' Selected';
    }
  }

  if (checkedMakes.length > 0 || checkedModels.length > 0) {
    list = list.filter(c => {
      const isMakeMatched = checkedMakes.some(make => {
          let searchMake = make.toLowerCase();
          if(searchMake === 'maruti suzuki') searchMake = 'maruti';
          return c.name.toLowerCase().includes(searchMake);
      });
      const isModelMatched = checkedModels.some(model => c.name.toLowerCase().includes(model.toLowerCase()));
      
      if (checkedMakes.length > 0 && checkedModels.length === 0) return isMakeMatched;
      else if (checkedMakes.length === 0 && checkedModels.length > 0) return isModelMatched;
      else return isMakeMatched || isModelMatched;
    });
  }

  // Fuel Filter
  const checkedFuels = Array.from(document.querySelectorAll('.fuel-cb:checked')).map(cb => cb.value);
  if (checkedFuels.length > 0) {
    list = list.filter(c => checkedFuels.includes((c.fuel || '').toLowerCase()));
  }

  // Transmission Filter
  const checkedTrans = Array.from(document.querySelectorAll('.trans-cb:checked')).map(cb => cb.value);
  if (checkedTrans.length > 0) {
    list = list.filter(c => checkedTrans.includes((c.trans || '').toLowerCase()));
  }

  // Body Type Filter
  const checkedBody = Array.from(document.querySelectorAll('.body-cb:checked')).map(cb => cb.value);
  if (checkedBody.length > 0) {
    // Attempt to match body type. Our dummy data usually has it inside name or we can skip if not explicitly present.
    // Assuming body type is somewhere in the description or just returning all if dummy data doesn't have it cleanly mapped.
    // For now, let's just search the name and desc for the body type keywords since c.bodyType might not exist.
    list = list.filter(c => {
        let text = (c.name + " " + (c.desc||"")).toLowerCase();
        return checkedBody.some(b => text.includes(b));
    });
  }

  // Owners Filter
  const checkedOwners = Array.from(document.querySelectorAll('.owner-cb:checked')).map(cb => cb.value);
  if (checkedOwners.length > 0) {
    list = list.filter(c => {
        return checkedOwners.some(o => (c.owner || '').toLowerCase().includes(o));
    });
  }

  // City Filter
  const cityVal = document.getElementById('citySelect').value;
  if (cityVal) list = list.filter(c => (c.city || '').toLowerCase() === cityVal.toLowerCase());

  // Car Age Filter
  const ageMin = parseInt(document.getElementById('ageMinRange').value);
  const ageMax = parseInt(document.getElementById('ageMaxRange').value);
  const currentYear = new Date().getFullYear();
  if (ageMin > 0 || ageMax < 15) {
    list = list.filter(c => {
      const age = currentYear - c.year;
      if (ageMax === 15) return age >= ageMin; // 15 means 15+ years
      return age >= ageMin && age <= ageMax;
    });
  }

  // Kilometer Filter
  const kmMin = parseInt(document.getElementById('kmMinRange').value);
  const kmMax = parseInt(document.getElementById('kmMaxRange').value);
  if (kmMin > 0 || kmMax < 80000) {
    list = list.filter(c => {
      const km = parseInt(String(c.km).replace(/[^0-9]/g, ''));
      if (kmMax === 80000) return km >= kmMin; 
      return km >= kmMin && km <= kmMax;
    });
  }

  // Seller Type
  const dealerChecked = document.getElementById('sellerDealer').checked;
  const ownerChecked = document.getElementById('sellerOwner').checked;
  if (dealerChecked || ownerChecked) {
    list = list.filter(c => {
      if (dealerChecked && ownerChecked) return true;
      if (dealerChecked) return c.verified === true;
      if (ownerChecked) return c.verified === false;
      return true;
    });
  }

  filteredCars = list;
  currentPage = 1;
  renderActiveFilters();
  renderCars();
}

function clearAll() {
  document.getElementById('priceSelect').value = '';
  document.getElementById('fuelSelect').value = '';
  document.getElementById('transSelect').value = '';
  document.getElementById('yearSelect').value = '';
  document.getElementById('conditionSelect').value = '';
  
  // Uncheck all tree checkboxes
  document.querySelectorAll('.make-checkbox, .model-checkbox').forEach(cb => cb.checked = false);
  document.getElementById('brandDropdownText').textContent = 'All Brands';

  applyFilters();
  showToast('✅ All filters cleared');
}

function sortCars(sel) {
  const val = sel.value;
  if (val === 'Price: Low to High') {
    filteredCars.sort((a,b) => parseFloat(a.price) - parseFloat(b.price));
  } else if (val === 'Price: High to Low') {
    filteredCars.sort((a,b) => parseFloat(b.price) - parseFloat(a.price));
  } else if (val === 'Newest First') {
    filteredCars.sort((a,b) => b.year - a.year);
  } else if (val === 'Lowest KM') {
    filteredCars.sort((a,b) => parseInt(String(a.km).replace(/[^\d]/g,'')) - parseInt(String(b.km).replace(/[^\d]/g,'')));
  } else {
    // Relevance (default load order)
    applyFilters();
    return;
  }
  currentPage = 1;
  renderCars();
  showToast('↕️ Sorted cars list');
}

function toggleCompare(id) {
  showToast(`📊 Car Added to comparison panel!`);
}

function contactSeller(id) {
  showToast('📞 Redirecting to contact seller details...');
  setTimeout(() => window.location = 'login.html', 1200);
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

window.onload = function() {
  initPage();
  checkLoginState();
};

// Dynamic login state update
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
          if (parts.length > 1) {
            initials = (parts[0][0] + parts[1][0]).toUpperCase();
          } else {
            initials = name.substring(0, 2).toUpperCase();
          }
        }
      } catch(e) {}
      navActions.innerHTML = `
        <a href="customer-dashboard.html" title="My Profile" style="text-decoration:none; display:block;">
          <div style="width: 42px; height: 42px; border-radius: 50%; background: rgba(255, 204, 0, 0.15); border: 2px solid var(--red); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: var(--red); text-transform: uppercase; transition: all 0.2s;">
            ${initials}
          </div>
        </a>
      `;
    } else {
      navActions.innerHTML = `
        <a href="login.html" style="text-decoration:none;"><button class="btn-outline-white">Login</button></a>
      `;
    }
  }

  if (currentUser) {
    const loginLinks = document.querySelectorAll('a[href="login.html"]');
    loginLinks.forEach(link => {
      link.href = 'customer-dashboard.html';
      const btn = link.querySelector('button');
      if (btn) {
        if (btn.textContent.trim().toLowerCase() === 'login') {
          btn.textContent = 'Dashboard';
        }
      } else {
        if (link.textContent.includes('Login / Register')) {
          link.textContent = 'My Dashboard';
        }
      }
    });
  }
}

// Toggle custom dropdown
function toggleDropdown(id) {
  const el = document.getElementById(id);
  const header = el.querySelector('.dropdown-header');
  el.classList.toggle('open');
  header.classList.toggle('open');
}

// Close dropdown on outside click
document.addEventListener('click', function(event) {
  const dropdown = document.getElementById('brandDropdown');
  if (dropdown && dropdown.classList.contains('open') && !dropdown.contains(event.target)) {
    dropdown.classList.remove('open');
    dropdown.querySelector('.dropdown-header').classList.remove('open');
  }
});

// Toggle models list
function toggleModels(makeId) {
  const modelsDiv = document.getElementById('models_' + makeId);
  const toggleBtn = modelsDiv.previousElementSibling.querySelector('.tree-toggle');
  modelsDiv.classList.toggle('open');
  toggleBtn.textContent = modelsDiv.classList.contains('open') ? '-' : '+';
}

// Filter tree based on search
function filterMakeModelTree() {
  const searchTerm = document.getElementById('makeModelSearch').value.toLowerCase();
  const makes = document.querySelectorAll('.tree-make');

  makes.forEach(make => {
    const makeName = make.getAttribute('data-name');
    const modelsDiv = make.querySelector('.tree-models');
    const modelItems = make.querySelectorAll('.tree-model-item');
    let hasVisibleModel = false;

    modelItems.forEach(item => {
      const modelName = item.getAttribute('data-name');
      if (modelName.includes(searchTerm) || makeName.includes(searchTerm)) {
        item.style.display = 'flex';
        hasVisibleModel = true;
      } else {
        item.style.display = 'none';
      }
    });

    if (hasVisibleModel || makeName.includes(searchTerm)) {
      make.style.display = 'block';
      if (searchTerm) {
        modelsDiv.classList.add('open');
        make.querySelector('.tree-toggle').textContent = '-';
      }
    } else {
      make.style.display = 'none';
    }
    
    if (!searchTerm) {
      modelsDiv.classList.remove('open');
      make.querySelector('.tree-toggle').textContent = '+';
    }
  });
}


function updateAgeSlider() {
  let minR = document.getElementById('ageMinRange');
  let maxR = document.getElementById('ageMaxRange');
  if (parseInt(minR.value) > parseInt(maxR.value)) { let tmp = minR.value; minR.value = maxR.value; maxR.value = tmp; }
  document.getElementById('ageMinInput').value = minR.value;
  document.getElementById('ageMaxInput').value = maxR.value;
  applyFilters();
}
function syncAgeInputs() {
  let minI = document.getElementById('ageMinInput');
  let maxI = document.getElementById('ageMaxInput');
  document.getElementById('ageMinRange').value = minI.value;
  document.getElementById('ageMaxRange').value = maxI.value;
  updateAgeSlider();
}

function updateKmSlider() {
  let minR = document.getElementById('kmMinRange');
  let maxR = document.getElementById('kmMaxRange');
  if (parseInt(minR.value) > parseInt(maxR.value)) { let tmp = minR.value; minR.value = maxR.value; maxR.value = tmp; }
  document.getElementById('kmMinInput').value = (minR.value / 1000) + ' K';
  document.getElementById('kmMaxInput').value = (maxR.value / 1000) + ' K';
  applyFilters();
}
function syncKmInputs() {
  let minI = document.getElementById('kmMinInput').value.replace(/[^0-9]/g, '');
  let maxI = document.getElementById('kmMaxInput').value.replace(/[^0-9]/g, '');
  if(!minI) minI = 0; if(!maxI) maxI = 80;
  document.getElementById('kmMinRange').value = minI * 1000;
  document.getElementById('kmMaxRange').value = maxI * 1000;
  updateKmSlider();
}


function toggleFilter(el) {
  el.classList.toggle('collapsed');
  const body = el.nextElementSibling;
  if (body) {
    body.classList.toggle('collapsed');
  }
}


function toggleAccordion(el) {
  el.classList.toggle('active');
  const body = el.nextElementSibling;
  if (body.classList.contains('open')) {
    body.style.maxHeight = '0';
    body.style.overflow = 'hidden';
    body.classList.remove('open');
  } else {
    body.classList.add('open');
    body.style.maxHeight = '1000px';
    // After animation, allow overflow if it's the brand tree
    setTimeout(() => { if(body.classList.contains('open')) body.style.overflow = 'visible'; }, 300);
  }
}


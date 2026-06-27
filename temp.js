

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
const carsPerPage = 9;

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
    const makeCb = Array.from(document.querySelectorAll('.make-cb')).find(cb => cb.value.toLowerCase() === brandLower || cb.value.toLowerCase().includes(brandLower));
    if (makeCb) makeCb.checked = true;
  }
  
  // Model
  const model = params.get('model');
  if (model) {
    const modelLower = model.toLowerCase();
    const modelCb = Array.from(document.querySelectorAll('.model-cb')).find(cb => cb.value.toLowerCase() === modelLower);
    if (modelCb) modelCb.checked = true;
  }

  // Budget
  const budget = params.get('budget');
  if (budget) {
    let targetBudget = '';
    if (budget.includes('1-2') || budget.includes('1 to 2') || budget.includes('1to2')) targetBudget = '1-2';
    else if (budget.includes('2-3') || budget.includes('2 to 3') || budget.includes('2to3')) targetBudget = '2-3';
    else if (budget.includes('3-5') || budget.includes('3 to 5') || budget.includes('3to5')) targetBudget = '3-5';
    else if (budget.includes('5-7') || budget.includes('5 to 7') || budget.includes('5to7')) targetBudget = '5-7';
    else if (budget.includes('7+') || budget.includes('7 plus')) targetBudget = '7+';

    if (targetBudget) {
      const budgetCb = document.querySelector(`.budget-cb[value="${targetBudget}"]`);
      if (budgetCb) budgetCb.checked = true;
    }
  }
  
  applyFilters();
}

function nextCardImg(e, cardId, direction, imgStr) {
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

function renderCars() {
  const list = document.getElementById('carList');
  if(!list) return;
  // Make sure it uses cars-grid class
  list.className = 'cars-grid';
  
  const countEl = document.getElementById('count');
  if (countEl) countEl.textContent = filteredCars.length;

  if (filteredCars.length === 0) {
    list.className = '';
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

  list.innerHTML = visibleCars.map(c => {
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
      </div>
      <div class="car-body">
        <div class="car-title">${c.year} ${c.name}</div>
        <div class="car-specs-text">${c.km} km | ${c.fuel} | ${c.city || 'Vadodara'}</div>
        
        <div class="car-price-row">
          <div class="car-price">Rs. ${c.price} Lakh</div>
        </div>
        
        <div class="car-action-buttons">
          <button class="btn-save" onclick="event.stopPropagation(); toggleSave(${c.id}, this)">
            <span>🤍</span> Save
          </button>
          <button class="btn-view" onclick="event.stopPropagation(); window.location='car-detail.html?id=${c.id}'">
            <span>👁️</span> VIEW
          </button>
        </div>
      </div>
      <div class="car-footer">
        ✨ ${(c.features && c.features.length > 0) ? c.features[0] : 'Premium Variant'}
      </div>
    </div>
  `;
  }).join('');

  renderPagination(filteredCars.length);
}


function changeImage(id, dir) {
  const imgEl = document.getElementById(`img-${id}`);
  if (!imgEl) return;
  const images = JSON.parse(imgEl.getAttribute('data-images') || '[]');
  if (images.length <= 1) return;
  
  let idx = parseInt(imgEl.getAttribute('data-index') || '0');
  idx += dir;
  if (idx < 0) idx = images.length - 1;
  if (idx >= images.length) idx = 0;
  
  imgEl.style.opacity = 0.5;
  setTimeout(() => {
    imgEl.src = images[idx];
    imgEl.setAttribute('data-index', idx);
    imgEl.style.opacity = 1;
  }, 150);
}

function renderPagination(totalCount) {
  const totalPages = Math.ceil(totalCount / carsPerPage);
  const container = document.querySelector('.pagination');
  if(!container) return;
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

  // Budget
  const checkedBudgets = Array.from(document.querySelectorAll('.budget-cb:checked')).map(cb => cb.value);
  if (checkedBudgets.length > 0) {
    list = list.filter(c => {
      const p = parseFloat(c.price);
      return checkedBudgets.some(b => {
        if (b === '1-2') return p >= 1.0 && p <= 2.0;
        if (b === '2-3') return p >= 2.0 && p <= 3.0;
        if (b === '3-5') return p >= 3.0 && p <= 5.0;
        if (b === '5-7') return p >= 5.0 && p <= 7.0;
        if (b === '7+') return p >= 7.0;
        return false;
      });
    });
  }

  // Brand / Model
  const checkedMakes = Array.from(document.querySelectorAll('.make-cb:checked')).map(cb => cb.value.toLowerCase());
  const checkedModels = Array.from(document.querySelectorAll('.model-cb:checked')).map(cb => cb.value.toLowerCase());
  
  if (checkedMakes.length > 0 || checkedModels.length > 0) {
    list = list.filter(c => {
      let cname = (c.name || '').toLowerCase();
      let matchMake = false;
      let matchModel = false;
      
      if (checkedMakes.length > 0) {
        matchMake = checkedMakes.some(make => {
          let sm = make === 'maruti suzuki' ? 'maruti' : make;
          return cname.includes(sm);
        });
      }
      
      if (checkedModels.length > 0) {
        matchModel = checkedModels.some(model => cname.includes(model));
      }
      
      if (checkedMakes.length > 0 && checkedModels.length === 0) return matchMake;
      if (checkedMakes.length === 0 && checkedModels.length > 0) return matchModel;
      return matchMake || matchModel;
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
    list = list.filter(c => {
        let text = ((c.name || '') + " " + (c.desc || '')).toLowerCase();
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
  const checkedCities = Array.from(document.querySelectorAll('.city-cb:checked')).map(cb => cb.value.toLowerCase());
  if (checkedCities.length > 0) {
    list = list.filter(c => checkedCities.includes((c.city || '').toLowerCase()));
  }

  // Car Age Filter
  const ageMinEl = document.getElementById('ageMinRange');
  const ageMaxEl = document.getElementById('ageMaxRange');
  const ageMin = ageMinEl ? parseInt(ageMinEl.value) || 0 : 0;
  const ageMax = ageMaxEl ? parseInt(ageMaxEl.value) || 15 : 15;
  const currentYear = new Date().getFullYear();
  if (ageMin > 0 || ageMax < 15) {
    list = list.filter(c => {
      const age = currentYear - (c.year || currentYear);
      if (ageMax === 15) return age >= ageMin; 
      return age >= ageMin && age <= ageMax;
    });
  }

  // Kilometer Filter
  const kmMinEl = document.getElementById('kmMinRange');
  const kmMaxEl = document.getElementById('kmMaxRange');
  const kmMin = kmMinEl ? parseInt(kmMinEl.value) || 0 : 0;
  const kmMax = kmMaxEl ? parseInt(kmMaxEl.value) || 80000 : 80000;
  if (kmMin > 0 || kmMax < 80000) {
    list = list.filter(c => {
      const km = parseInt(String(c.km || '0').replace(/[^0-9]/g, '')) || 0;
      if (kmMax === 80000) return km >= kmMin; 
      return km >= kmMin && km <= kmMax;
    });
  }

  // Seller Type
  const checkedSellers = Array.from(document.querySelectorAll('.seller-cb:checked')).map(cb => cb.value);
  if (checkedSellers.length > 0) {
    list = list.filter(c => {
      if (checkedSellers.includes('Dealer') && checkedSellers.includes('Owner')) return true;
      if (checkedSellers.includes('Dealer')) return c.verified === true;
      if (checkedSellers.includes('Owner')) return c.verified === false;
      return true;
    });
  }

  filteredCars = list;
  currentPage = 1;
  renderActiveFilters();
  renderCars();
}

function renderActiveFilters() {
  const container = document.getElementById('activeFilters');
  if(!container) return;
  const items = [];

  const checkedBudgets = Array.from(document.querySelectorAll('.budget-cb:checked')).map(cb => cb.value);
  if (checkedBudgets.length > 0) items.push(`Budget: ${checkedBudgets.join(', ')} Lakh`);

  const checkedMakes = Array.from(document.querySelectorAll('.make-cb:checked')).map(cb => cb.value);
  if (checkedMakes.length > 0) items.push(`Brand: ${checkedMakes.join(', ')}`);
  
  const checkedModels = Array.from(document.querySelectorAll('.model-cb:checked')).map(cb => cb.value);
  if (checkedModels.length > 0) items.push(`Model: ${checkedModels.join(', ')}`);

  const checkedFuels = Array.from(document.querySelectorAll('.fuel-cb:checked')).map(cb => cb.value);
  if (checkedFuels.length > 0) items.push(`Fuel: ${checkedFuels.join(', ')}`);

  const checkedTrans = Array.from(document.querySelectorAll('.trans-cb:checked')).map(cb => cb.value);
  if (checkedTrans.length > 0) items.push(`Trans: ${checkedTrans.join(', ')}`);

  const checkedCities = Array.from(document.querySelectorAll('.city-cb:checked')).map(cb => cb.value);
  if (checkedCities.length > 0) items.push(`City: ${checkedCities.join(', ')}`);

  const checkedSellers = Array.from(document.querySelectorAll('.seller-cb:checked')).map(cb => cb.value);
  if (checkedSellers.length > 0) items.push(`Seller: ${checkedSellers.join(', ')}`);

  const ageMinEl = document.getElementById('ageMinRange');
  const ageMaxEl = document.getElementById('ageMaxRange');
  const ageMin = ageMinEl ? parseInt(ageMinEl.value) || 0 : 0;
  const ageMax = ageMaxEl ? parseInt(ageMaxEl.value) || 15 : 15;
  if (ageMin > 0 || ageMax < 15) {
    items.push(`Age: ${ageMin} - ${ageMax === 15 ? '15+' : ageMax} Years`);
  }

  const kmMinEl = document.getElementById('kmMinRange');
  const kmMaxEl = document.getElementById('kmMaxRange');
  const kmMin = kmMinEl ? parseInt(kmMinEl.value) || 0 : 0;
  const kmMax = kmMaxEl ? parseInt(kmMaxEl.value) || 80000 : 80000;
  if (kmMin > 0 || kmMax < 80000) {
    items.push(`Kms: ${kmMin/1000}K - ${kmMax === 80000 ? '80K+' : kmMax/1000 + 'K'}`);
  }

  container.innerHTML = items.map(f => `
    <div class="filter-tag">
      ${f}
    </div>
  `;
  }).join('');
}

function clearAll() {
  const ageMinEl = document.getElementById('ageMinRange');
  const ageMaxEl = document.getElementById('ageMaxRange');
  if(ageMinEl) ageMinEl.value = '0';
  if(ageMaxEl) ageMaxEl.value = '15';
  updateAgeSlider();

  const kmMinEl = document.getElementById('kmMinRange');
  const kmMaxEl = document.getElementById('kmMaxRange');
  if(kmMinEl) kmMinEl.value = '0';
  if(kmMaxEl) kmMaxEl.value = '80000';
  updateKmSlider();

  document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);

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

function updateAgeSlider() {
  let minR = document.getElementById('ageMinRange');
  let maxR = document.getElementById('ageMaxRange');
  if(!minR || !maxR) return;
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
  if(!minR || !maxR) return;
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


function toggleTree(el) {
  const node = el.closest('.tree-node');
  node.classList.toggle('active');
  const children = node.querySelector('.tree-children');
  if (children.classList.contains('open')) {
    children.classList.remove('open');
  } else {
    children.classList.add('open');
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
    setTimeout(() => { if(body.classList.contains('open')) body.style.overflow = 'visible'; }, 300);
  }
}

function contactSeller(id) {
  showToast('📞 Redirecting to contact seller details...');
  setTimeout(() => window.location = 'login.html', 1200);
}


function toggleSave(id, btn) {
  const isSaved = btn.textContent.includes('Saved');
  if (isSaved) {
    btn.innerHTML = '<span>🤍</span> Save';
    showToast('Removed from favorites');
  } else {
    btn.innerHTML = '<span>🤍</span> Save';
    showToast('Added to favorites');
  }
}

function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

window.onload = function() {
  initPage();
  checkLoginState();
};

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
        <a href="login.html" class="nav-login" id="nav-login-link">
          <button class="btn-login" id="nav-login-btn">
            Login / Register
          </button>
        </a>
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



// Dynamic Automotive Tree Rendering
document.addEventListener('DOMContentLoaded', () => {
  fetch((window.location.protocol === 'file:' ? 'http://localhost:5000' : '') + '/api/car-hierarchy')
    .then(r => r.json())
    .then(makes => {
      const treeContainer = document.getElementById('dynamic-tree-list');
      if (!treeContainer) return;
      treeContainer.innerHTML = '';
      
      makes.forEach(make => {
        if (!make.models || make.models.length === 0) return; // Skip empty makes
        
        const node = document.createElement('div');
        node.className = 'tree-node';
        
        const parentHtml = `
          <div class="tree-parent" onclick="toggleTree(this)">
            <div class="tree-parent-left">
              <input type="checkbox" class="make-cb" value="${make.name}" onchange="applyFilters()" onclick="event.stopPropagation()">
              <label>${make.name}</label>
            </div>
            <span class="tree-toggle">+</span>
          </div>
        `;
        
        let childrenHtml = '<div class="tree-children">';
        make.models.forEach(model => {
          childrenHtml += `
            <div class="checkbox-item">
              <input type="checkbox" class="model-cb" value="${model.name}" onchange="applyFilters()">
              <label>${model.name}</label>
            </div>
          `;
        });
        childrenHtml += '</div>';
        
        node.innerHTML = parentHtml + childrenHtml;
        treeContainer.appendChild(node);
      });
      
      // Call setFiltersFromUrl to apply URL parameters to newly created DOM elements
      if (typeof setFiltersFromUrl === 'function') {
         setTimeout(setFiltersFromUrl, 50);
      }
    })
    .catch(e => {
      console.error("Error loading hierarchy:", e);
      const tc = document.getElementById('dynamic-tree-list');
      if(tc) tc.innerHTML = 'Error loading filters.';
    });
});

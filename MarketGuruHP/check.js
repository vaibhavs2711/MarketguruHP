

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

  list.innerHTML = visibleCars.map(c => `
    <div class="car-card" onclick="window.location='car-detail.html?id=${c.id}'">
      <div class="car-img-wrap" style="background:linear-gradient(135deg,${c.color || '#e8eef5'},#ccd4e0)">
        ${c.image ? `<img src="${c.image}" />` : `<span style="font-size:80px">${c.emoji || '🚗'}</span>`}
        ${c.verified ? '<div class="car-badge-featured">Featured</div>' : ''}
      </div>
      <div class="car-body">
        <div class="car-title">${c.year} ${c.name}</div>
        <div class="car-specs-text">${c.km} km | ${c.fuel} | ${c.city || 'Vadodara'}</div>
        
        <div class="car-price-row">
          <div class="car-price">Rs. ${c.price} Lakh</div>
          <div class="car-emi">EMI at <strong>Rs.${c.emi || '12,500'}</strong></div>
        </div>
        
        <div class="car-offer-row">
          <div class="make-offer">Make Offer</div>
        </div>
        
        <button class="btn-seller" onclick="event.stopPropagation(); contactSeller(${c.id})">Get Seller Details</button>
      </div>
      <div class="car-footer">
        ✨ ${(c.features && c.features.length > 0) ? c.features[0] : 'Premium Variant'}
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


function toggleTree(el) {
  const children = el.nextElementSibling;
  if (!children) return;
  const isExpanded = children.classList.contains('expanded');
  
  if (isExpanded) {
    children.classList.remove('expanded');
    el.querySelector('.tree-toggle').textContent = '+';
  } else {
    children.classList.add('expanded');
    el.querySelector('.tree-toggle').textContent = '-';
  }
}

function toggleMake(makeCb) {
  const node = makeCb.closest('.tree-node');
  const children = node.querySelectorAll('.model-checkbox, .variant-checkbox');
  children.forEach(cb => cb.checked = makeCb.checked);
}

function toggleModel(modelCb) {
  const node = modelCb.closest('.tree-node');
  // Check/uncheck all its variants
  const variants = node.querySelectorAll('.variant-checkbox');
  variants.forEach(cb => cb.checked = modelCb.checked);

  // Update parent make
  const makeNode = node.parentElement.closest('.tree-node');
  if (makeNode) {
    const makeCb = makeNode.querySelector('.make-checkbox');
    const allModels = makeNode.querySelectorAll('.model-checkbox');
    const anyChecked = Array.from(allModels).some(cb => cb.checked);
    makeCb.checked = anyChecked;
  }
}

function toggleVariant(variantCb) {
  const modelNode = variantCb.closest('.tree-children.variant-children').parentElement;
  const modelCb = modelNode.querySelector('.model-checkbox');
  const allVariants = modelNode.querySelectorAll('.variant-checkbox');
  const anyVarChecked = Array.from(allVariants).some(cb => cb.checked);
  
  modelCb.checked = anyVarChecked;

  // Update parent make
  const makeNode = modelNode.parentElement.closest('.tree-node');
  if (makeNode) {
    const makeCb = makeNode.querySelector('.make-checkbox');
    const allModels = makeNode.querySelectorAll('.model-checkbox');
    const anyModelChecked = Array.from(allModels).some(cb => cb.checked);
    makeCb.checked = anyModelChecked;
  }
}

function filterBrands() {
  const term = document.getElementById('brandSearch').value.toLowerCase();
  const makes = document.querySelectorAll('.tree-node');
  
  makes.forEach(makeNode => {
    // Only process top-level makes
    if(!makeNode.parentElement.classList.contains('dropdown-list')) return;

    let makeMatch = makeNode.getAttribute('data-name').includes(term);
    let anyModelMatch = false;
    
    const models = makeNode.querySelectorAll(':scope > .tree-children > .tree-node, :scope > .tree-children > .tree-leaf');
    models.forEach(modelNode => {
      let modelMatch = modelNode.getAttribute('data-name').includes(term);
      let anyVariantMatch = false;

      const variants = modelNode.querySelectorAll('.variant-row');
      variants.forEach(varNode => {
        let varMatch = varNode.getAttribute('data-name').includes(term);
        if (varMatch || modelMatch || makeMatch) {
          varNode.style.display = 'flex';
          anyVariantMatch = true;
        } else {
          varNode.style.display = 'none';
        }
      });

      if (modelMatch || makeMatch || anyVariantMatch) {
        modelNode.style.display = 'block';
        anyModelMatch = true;
        // Auto-expand model if searching
        const varChildren = modelNode.querySelector('.variant-children');
        if (term && anyVariantMatch && varChildren) {
           varChildren.classList.add('expanded');
           const toggle = modelNode.querySelector('.tree-toggle');
           if (toggle) toggle.textContent = '-';
        } else if (!term && varChildren) {
           varChildren.classList.remove('expanded');
           const toggle = modelNode.querySelector('.tree-toggle');
           if (toggle) toggle.textContent = '+';
        }
      } else {
        modelNode.style.display = 'none';
      }
    });
    
    if (makeMatch || anyModelMatch) {
      makeNode.style.display = 'block';
      // Auto-expand make if searching
      const makeChildren = makeNode.querySelector(':scope > .tree-children');
      if (term && anyModelMatch && makeChildren) {
         makeChildren.classList.add('expanded');
         const toggle = makeNode.querySelector(':scope > .tree-parent > .tree-toggle');
         if (toggle) toggle.textContent = '-';
      } else if (!term && makeChildren) {
         makeChildren.classList.remove('expanded');
         const toggle = makeNode.querySelector(':scope > .tree-parent > .tree-toggle');
         if (toggle) toggle.textContent = '+';
      }
    } else {
      makeNode.style.display = 'none';
    }
  });
}
\n
function applyFilters() {
  let list = [...allCars];

  // Budget
  const priceRange = document.getElementById('priceSelect').value;
  if (priceRange) {
    if (priceRange === '1-2') list = list.filter(c => parseFloat(c.price) >= 1.0 && parseFloat(c.price) <= 2.0);
    else if (priceRange === '2-3') list = list.filter(c => parseFloat(c.price) >= 2.0 && parseFloat(c.price) <= 3.0);
    else if (priceRange === '3-5') list = list.filter(c => parseFloat(c.price) >= 3.0 && parseFloat(c.price) <= 5.0);
    else if (priceRange === '5-7') list = list.filter(c => parseFloat(c.price) >= 5.0 && parseFloat(c.price) <= 7.0);
    else if (priceRange === '7+') list = list.filter(c => parseFloat(c.price) >= 7.0);
  }

  // Brands & Models & Variants
  const checkedMakes = Array.from(document.querySelectorAll('.make-checkbox:checked')).map(cb => cb.value);
  const checkedModels = Array.from(document.querySelectorAll('.model-checkbox:checked')).map(cb => cb.value);
  const checkedVariants = Array.from(document.querySelectorAll('.variant-checkbox:checked')).map(cb => cb.value);

  const dropdownText = document.getElementById('brandDropdownText');
  if (dropdownText) {
    if (checkedMakes.length === 0 && checkedModels.length === 0 && checkedVariants.length === 0) dropdownText.textContent = 'All Brands';
    else dropdownText.textContent = (checkedMakes.length + checkedModels.length + checkedVariants.length) + ' Selected';
  }

  if (checkedMakes.length > 0 || checkedModels.length > 0 || checkedVariants.length > 0) {
    list = list.filter(c => {
      const isMakeMatched = checkedMakes.some(make => {
          let searchMake = make.toLowerCase();
          if(searchMake === 'maruti suzuki') searchMake = 'maruti';
          return (c.name || '').toLowerCase().includes(searchMake);
      });
      const isModelMatched = checkedModels.some(model => (c.name || '').toLowerCase().includes(model.toLowerCase()));
      const isVariantMatched = checkedVariants.some(variant => (c.name || '').toLowerCase().includes(variant.toLowerCase()));
      
      return isMakeMatched || isModelMatched || isVariantMatched;
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
  const citySelect = document.getElementById('citySelect');
  const cityVal = citySelect ? citySelect.value : '';
  if (cityVal) list = list.filter(c => (c.city || '').toLowerCase() === cityVal.toLowerCase());

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
  const dealerChecked = document.getElementById('sellerDealer')?.checked || false;
  const ownerChecked = document.getElementById('sellerOwner')?.checked || false;
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
  if(typeof renderActiveFilters === 'function') renderActiveFilters();
  if(typeof renderCars === 'function') renderCars();
}

function renderActiveFilters() {
  const container = document.getElementById('activeFilters');
  if(!container) return;
  const items = [];

  const priceSelect = document.getElementById('priceSelect');
  const priceVal = priceSelect ? priceSelect.value : '';
  if (priceVal) items.push(`Budget: ${priceVal} Lakh`);

  const checkedMakes = Array.from(document.querySelectorAll('.make-checkbox:checked')).map(cb => cb.value);
  const checkedModels = Array.from(document.querySelectorAll('.model-checkbox:checked')).map(cb => cb.value);
  const checkedVariants = Array.from(document.querySelectorAll('.variant-checkbox:checked')).map(cb => cb.value);
  
  if (checkedMakes.length > 0) items.push(`Brand: ${checkedMakes.join(', ')}`);
  if (checkedModels.length > 0) items.push(`Model: ${checkedModels.join(', ')}`);
  if (checkedVariants.length > 0) items.push(`Variant: ${checkedVariants.join(', ')}`);

  const checkedFuels = Array.from(document.querySelectorAll('.fuel-cb:checked')).map(cb => cb.value);
  if (checkedFuels.length > 0) items.push(`Fuel: ${checkedFuels.join(', ')}`);

  const checkedTrans = Array.from(document.querySelectorAll('.trans-cb:checked')).map(cb => cb.value);
  if (checkedTrans.length > 0) items.push(`Trans: ${checkedTrans.join(', ')}`);

  const citySelect = document.getElementById('citySelect');
  const cityVal = citySelect ? citySelect.value : '';
  if (cityVal) items.push(`City: ${cityVal}`);

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

  const dealerChecked = document.getElementById('sellerDealer')?.checked || false;
  const ownerChecked = document.getElementById('sellerOwner')?.checked || false;
  if (dealerChecked) items.push('Dealer Cars');
  if (ownerChecked) items.push('Direct Owner');

  container.innerHTML = items.map(f => `
    <div class="filter-tag">
      ${f}
    </div>
  `).join('');
}

function clearAll() {
  const priceSelect = document.getElementById('priceSelect');
  if(priceSelect) priceSelect.value = '';
  
  const citySelect = document.getElementById('citySelect');
  if(citySelect) citySelect.value = '';
  
  const ageMinEl = document.getElementById('ageMinRange');
  const ageMaxEl = document.getElementById('ageMaxRange');
  if(ageMinEl) ageMinEl.value = '0';
  if(ageMaxEl) ageMaxEl.value = '15';
  if(typeof updateAgeSlider === 'function') updateAgeSlider();

  const kmMinEl = document.getElementById('kmMinRange');
  const kmMaxEl = document.getElementById('kmMaxRange');
  if(kmMinEl) kmMinEl.value = '0';
  if(kmMaxEl) kmMaxEl.value = '80000';
  if(typeof updateKmSlider === 'function') updateKmSlider();

  document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
  const brandDropdownText = document.getElementById('brandDropdownText');
  if(brandDropdownText) brandDropdownText.textContent = 'All Brands';

  applyFilters();
  if(typeof showToast === 'function') showToast('✅ All filters cleared');
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
  if(typeof showToast === 'function') showToast('↕️ Sorted cars list');
}




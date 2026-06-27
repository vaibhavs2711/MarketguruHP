import re

with open('customer-dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add API_BASE and global state
html = html.replace('let currentUser = ', "const API_BASE = window.location.protocol === 'file:' ? 'http://localhost:5000' : '';\n    let globalCars = [];\n    let globalWishlist = [];\n    let currentUser = ")

# 2. Update initDashboard
old_init = """    function initDashboard() {
      currentUser = localStorage.getItem('mg_current_user') || 'Guest User';
      currentUserMobile = localStorage.getItem('mg_current_user_mobile') || '';

      document.getElementById('welcomeName').textContent = currentUser;

      const parts = currentUser.split(' ');
      const initials = parts.map(p => p[0]).join('').substring(0, 2).toUpperCase();
      document.getElementById('headerAvatar').textContent = initials || 'U';

      // Dealer Customizations
      if (userType === 'dealer') {
        document.getElementById('dashboardTitle').textContent = 'DEALER PARTNER CONSOLE';
        document.getElementById('userBadge').textContent = 'Dealer Partner';
        document.getElementById('listingsKpiLabel').textContent = 'Dealership Cars Listed';

        const listingsHeader = document.querySelector('#pg-listings .card-title');
        if (listingsHeader) listingsHeader.textContent = '🚗 Dealership Active Inventory';
      } else {
        document.getElementById('dashboardTitle').textContent = 'CUSTOMER DASHBOARD';
        document.getElementById('userBadge').textContent = 'Member Client';
        document.getElementById('listingsKpiLabel').textContent = 'My Cars Listed for Sale';

        const listingsHeader = document.querySelector('#pg-listings .card-title');
        if (listingsHeader) listingsHeader.textContent = '🚗 My Cars Listed for Sale';
      }

      renderStats();
      renderWishlist();
      renderUserListings();
    }"""

new_init = """    function initDashboard() {
      currentUser = localStorage.getItem('mg_current_user') || 'Guest User';
      currentUserMobile = localStorage.getItem('mg_current_user_mobile') || '';
      try {
          const userObj = JSON.parse(currentUser);
          document.getElementById('welcomeName').textContent = userObj.name || 'Guest User';
          const parts = (userObj.name || '').split(' ');
          const initials = parts.map(p => p[0]).join('').substring(0, 2).toUpperCase();
          document.getElementById('headerAvatar').textContent = initials || 'U';
      } catch(e) {
          document.getElementById('welcomeName').textContent = currentUser;
          document.getElementById('headerAvatar').textContent = 'U';
      }

      // Dealer Customizations
      if (userType === 'dealer') {
        document.getElementById('dashboardTitle').textContent = 'DEALER PARTNER CONSOLE';
        document.getElementById('userBadge').textContent = 'Dealer Partner';
        document.getElementById('listingsKpiLabel').textContent = 'Dealership Cars Listed';
        const listingsHeader = document.querySelector('#pg-listings .card-title');
        if (listingsHeader) listingsHeader.textContent = '🚗 Dealership Active Inventory';
      } else {
        document.getElementById('dashboardTitle').textContent = 'CUSTOMER DASHBOARD';
        document.getElementById('userBadge').textContent = 'Member Client';
        document.getElementById('listingsKpiLabel').textContent = 'My Cars Listed for Sale';
        const listingsHeader = document.querySelector('#pg-listings .card-title');
        if (listingsHeader) listingsHeader.textContent = '🚗 My Cars Listed for Sale';
      }

      fetch(API_BASE + '/api/init')
        .then(r => r.json())
        .then(data => {
            if(data.status === 'success') {
                globalCars = data.cars || [];
                try {
                    globalWishlist = JSON.parse(localStorage.getItem('mg_wishlist') || '[]');
                } catch(e) { globalWishlist = []; }
                renderStats();
                renderWishlist();
                renderUserListings();
            }
        }).catch(err => console.error(err));
    }"""
html = html.replace(old_init, new_init)

# 3. Update renderStats
html = html.replace('const wishlist = mgDB.getWishlist();', '')
html = html.replace('const userCars = mgDB.getUserListings(currentUserMobile);', "const userCars = globalCars.filter(c => c.listed_by === currentUserMobile);")
html = html.replace("document.getElementById('statWishlist').textContent = wishlist.length;", "document.getElementById('statWishlist').textContent = globalWishlist.length;")

# 4. Update renderWishlist
old_rw = """    function renderWishlist() {
      const list = mgDB.getWishlist();
      const grid = document.getElementById('wishlistGrid');

      if (list.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--muted)">No saved cars yet. Browse our catalog and click "Save"!</div>`;
        return;
      }

      grid.innerHTML = list.map(id => {
        const c = mgDB.getCarById(id);
        if (!c) return '';"""
new_rw = """    function renderWishlist() {
      const list = globalWishlist;
      const grid = document.getElementById('wishlistGrid');

      if (list.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--muted)">No saved cars yet. Browse our catalog and click "Save"!</div>`;
        return;
      }

      grid.innerHTML = list.map(id => {
        const c = globalCars.find(car => car.id === id);
        if (!c) return '';"""
html = html.replace(old_rw, new_rw)

# 5. Update removeSaved
old_rs = """    function removeSaved(id) {
      mgDB.toggleWishlist(id);
      showToast('❌ Removed from saved list');
      renderStats();
      renderWishlist();
    }"""
new_rs = """    function removeSaved(id) {
      globalWishlist = globalWishlist.filter(x => x !== id);
      localStorage.setItem('mg_wishlist', JSON.stringify(globalWishlist));
      showToast('❌ Removed from saved list');
      renderStats();
      renderWishlist();
    }"""
html = html.replace(old_rs, new_rs)

# 6. Update renderUserListings
old_rul = """    function renderUserListings() {
      const userCars = mgDB.getUserListings(currentUserMobile);
      const tbody = document.getElementById('listingsTable');"""
new_rul = """    function renderUserListings() {
      const userCars = globalCars.filter(c => c.listed_by === currentUserMobile);
      const tbody = document.getElementById('listingsTable');"""
html = html.replace(old_rul, new_rul)

# 7. Update checkSellPermissions
old_csp = """    function checkSellPermissions() {
      if (userType === 'private') {
        const userCars = mgDB.getUserListings(currentUserMobile);
        if (userCars && userCars.length >= 1) {
          showToast('⚠️ Individual sellers are restricted to exactly 1 car listing!');
          return;
        }
      }
      window.location.href = 'sell.html';
    }"""
new_csp = """    function checkSellPermissions() {
      if (userType === 'private') {
        const userCars = globalCars.filter(c => c.listed_by === currentUserMobile);
        if (userCars && userCars.length >= 1) {
          showToast('⚠️ Individual sellers are restricted to exactly 1 car listing!');
          return;
        }
      }
      window.location.href = 'sell.html';
    }"""
html = html.replace(old_csp, new_csp)

# 8. Modal Handlers
old_oem = """    function openEditModal(carId) {
      const car = mgDB.getCarById(carId);"""
new_oem = """    function openEditModal(carId) {
      const car = globalCars.find(c => c.id === carId);"""
html = html.replace(old_oem, new_oem)

old_sep = """      showToast('💾 Saving changes...');
      const success = mgDB.updateListing(carId, updates, currentUserMobile);
      if (success) {
        closeModal('editPriceModal');
        showToast('✅ Listing updated successfully!');
        renderUserListings();
        renderStats();
      } else {
        showToast('❌ Failed to save. Please try again.');
      }
    }"""
new_sep = """      showToast('💾 Saving changes...');
      // Simple mock update until backend endpoint exists for editing
      const car = globalCars.find(c => c.id === carId);
      if(car) {
          Object.assign(car, updates);
          closeModal('editPriceModal');
          showToast('✅ Listing updated successfully!');
          renderUserListings();
          renderStats();
      } else {
          showToast('❌ Failed to save. Please try again.');
      }
    }"""
html = html.replace(old_sep, new_sep)

old_drl = """    function doRemoveListing(isSold) {
      const carId = parseInt(document.getElementById('removeCarId').value);
      const success = mgDB.removeListing(carId, currentUserMobile);
      if (success) {
        closeModal('confirmRemoveModal');
        showToast(isSold ? '🎉 Marked as Sold & Removed!' : '🗑️ Listing Removed successfully!');
        renderStats();
        renderUserListings();
      } else {
        showToast('❌ Failed to remove listing.');
      }
    }"""
new_drl = """    function doRemoveListing(isSold) {
      const carId = parseInt(document.getElementById('removeCarId').value);
      globalCars = globalCars.filter(c => c.id !== carId);
      closeModal('confirmRemoveModal');
      showToast(isSold ? '🎉 Marked as Sold & Removed!' : '🗑️ Listing Removed successfully!');
      renderStats();
      renderUserListings();
    }"""
html = html.replace(old_drl, new_drl)

# Fix init call
html = html.replace('// INIT', 'initDashboard();')
html = html.replace('document.addEventListener("DOMContentLoaded", () => {', 'document.addEventListener("DOMContentLoaded", () => {\n  initDashboard();')

with open('customer-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated customer-dashboard.html")

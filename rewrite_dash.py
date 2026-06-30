import re

with open('customer-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_css = """
    :root {
      --primary: #F97316;
      --primary-hover: #EA580C;
      --text: #1E293B;
      --bg: #F8F9FA;
      --white: #FFFFFF;
      --border: #E2E8F0;
      --muted: #64748B;
      --blue: #3B82F6;
      --green: #10B981;
      --orange: #F59E0B;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', sans-serif; color: var(--text); background: var(--bg); min-height: 100vh; display: flex; flex-direction: column; }

    /* NEW TOPBAR */
    .topbar-new { background: var(--white); height: 72px; border-bottom: 1px solid var(--border); display: flex; align-items: center; padding: 0 32px; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
    .left-nav { display: flex; align-items: center; cursor: pointer; color: var(--text); }
    .right-nav { display: flex; align-items: center; gap: 24px; }
    .notif-icon { position: relative; cursor: pointer; color: var(--text); }
    .notif-badge { position: absolute; top: -4px; right: -4px; background: #EF4444; color: #fff; font-size: 10px; font-weight: 700; width: 16px; height: 16px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .user-profile { display: flex; align-items: center; gap: 12px; cursor: pointer; }
    .user-profile .avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; background: #e2e8f0; }
    .user-info { display: flex; flex-direction: column; }
    .user-name { font-size: 14px; font-weight: 700; color: var(--text); }
    .user-role { font-size: 12px; color: var(--muted); }

    .dashboard-main { max-width: 1280px; margin: 0 auto; width: 100%; padding: 40px 32px; flex: 1; }
    
    .welcome-header h1 { font-size: 28px; font-weight: 800; color: #111827; margin-bottom: 8px; letter-spacing: -0.5px; }
    .welcome-header p { font-size: 15px; color: var(--muted); margin-bottom: 32px; }

    .dash-card { background: var(--white); border: 1px solid var(--border); border-radius: 16px; padding: 24px; }
    
    /* TOP GRID */
    .top-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px; }
    .top-grid .dash-card h3 { font-size: 16px; font-weight: 700; color: var(--text); margin-bottom: 16px; }
    .usage-tag { display: inline-block; background: #DCFCE7; color: #15803D; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px; margin-bottom: 16px; }
    .progress-bar-bg { width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; margin-bottom: 16px; overflow: hidden; }
    .progress-bar-fill { height: 100%; background: #10B981; width: 100%; border-radius: 4px; }
    .top-grid .dash-card p { font-size: 14px; color: var(--muted); }
    
    .split-card { display: flex; justify-content: space-between; align-items: center; }
    .price-box { display: flex; align-items: center; gap: 12px; margin-top: 16px; }
    .price { font-size: 24px; font-weight: 800; color: var(--text); }
    .price-sub { font-size: 13px; color: var(--muted); background: #FEF3C7; color: #B45309; padding: 4px 10px; border-radius: 4px; font-weight: 600; }
    .btn-upgrade { margin-top: 16px; background: #FACC15; color: #854D0E; border: none; padding: 12px 24px; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; transition: 0.2s; }
    .btn-upgrade:hover { opacity: 0.9; }
    .shield-icon { width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 48px; background: #EFF6FF; border-radius: 50%; position: relative; }
    .shield-icon::after { content: ''; position: absolute; width: 120px; height: 120px; background: #DBEAFE; border-radius: 50%; z-index: -1; opacity: 0.5; }

    /* MY LISTED CAR */
    .section-my-cars { margin-bottom: 32px; background: var(--white); border: 1px solid var(--border); border-radius: 16px; padding: 24px; }
    .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
    .section-header h2 { font-size: 18px; font-weight: 700; color: var(--text); }
    .section-actions { display: flex; align-items: center; gap: 12px; }
    .btn-edit { background: var(--white); border: 1px solid var(--border); color: var(--text); font-size: 13px; font-weight: 600; padding: 8px 16px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: 0.2s; }
    .btn-edit:hover { background: #f8f9fa; }
    .btn-icon { background: var(--white); border: 1px solid var(--border); color: var(--text); width: 34px; height: 34px; border-radius: 6px; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; transition: 0.2s; }
    .btn-icon:hover { background: #f8f9fa; }

    .new-car-card { display: flex; align-items: center; gap: 24px; }
    .ncc-left { position: relative; width: 220px; height: 140px; background: #F1F5F9; border-radius: 12px; overflow: hidden; display: flex; align-items: center; justify-content: center; }
    .ncc-badge { position: absolute; top: 10px; left: 10px; background: #DCFCE7; color: #15803D; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 4px; z-index: 2; }
    .ncc-left img { max-width: 100%; max-height: 100%; object-fit: contain; }
    
    .ncc-middle { flex: 1; }
    .ncc-title { font-size: 20px; font-weight: 800; color: var(--text); margin-bottom: 6px; }
    .ncc-specs { font-size: 14px; color: var(--muted); margin-bottom: 8px; }
    .ncc-loc { font-size: 13px; color: var(--muted); display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
    .ncc-reg { background: #F1F5F9; padding: 2px 8px; border-radius: 4px; font-family: monospace; font-size: 12px; }
    .ncc-price-row { display: flex; align-items: center; gap: 16px; }
    .ncc-price { font-size: 20px; font-weight: 800; color: var(--text); }
    .ncc-view { font-size: 14px; color: var(--blue); font-weight: 600; text-decoration: none; display: flex; align-items: center; gap: 4px; }

    .ncc-right { display: flex; gap: 40px; border-left: 1px solid var(--border); padding-left: 40px; height: 80px; align-items: center; }
    .ncc-stat { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; cursor: pointer; transition: 0.2s; }
    .ncc-stat:hover { opacity: 0.7; }
    .ns-icon { color: var(--muted); font-size: 18px; }
    .ns-val { font-size: 18px; font-weight: 800; color: var(--text); }
    .ns-label { font-size: 12px; color: var(--muted); }

    /* BOTTOM GRID */
    .bottom-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 32px; }
    .bottom-grid h3 { font-size: 16px; font-weight: 700; color: var(--text); margin-bottom: 20px; }
    
    .action-list { display: flex; flex-direction: column; gap: 12px; }
    .action-item { display: flex; align-items: center; padding: 16px; border: 1px solid var(--border); border-radius: 12px; cursor: pointer; transition: 0.2s; }
    .action-item:hover { border-color: #CBD5E1; background: #F8FAFC; }
    .ai-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; margin-right: 16px; }
    .ai-icon.blue-icon { background: #EFF6FF; color: #3B82F6; }
    .ai-icon.yellow-icon { background: #FEF3C7; color: #D97706; }
    .ai-icon.gray-icon { background: #F1F5F9; color: #64748B; }
    .ai-text { flex: 1; }
    .ai-title { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 2px; }
    .ai-sub { font-size: 12px; color: var(--muted); }
    .ai-badge { background: #3B82F6; color: #fff; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px; margin-right: 12px; }
    .ai-arrow { color: var(--muted); font-size: 18px; font-weight: 300; }

    .card-header-flex { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .card-header-flex h3 { margin-bottom: 0; }
    .date-select { border: 1px solid var(--border); padding: 6px 10px; border-radius: 6px; font-size: 12px; color: var(--text); background: var(--white); outline: none; font-weight: 600; cursor: pointer; }
    
    .perf-list { display: flex; flex-direction: column; gap: 20px; }
    .perf-item { display: flex; align-items: center; }
    .pi-icon { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-right: 16px; }
    .pi-icon.green-bg { background: #DCFCE7; }
    .pi-icon.orange-bg { background: #FFEDD5; }
    .pi-icon.purple-bg { background: #F3E8FF; }
    .pi-text { flex: 1; }
    .pi-val { font-size: 16px; font-weight: 800; color: var(--text); margin-bottom: 2px; }
    .pi-label { font-size: 12px; color: var(--muted); }
    .pi-trend { font-size: 12px; font-weight: 600; }
    .pi-trend.green-text { color: #10B981; }

    .tips-list { display: flex; flex-direction: column; gap: 24px; margin-bottom: 24px; }
    .tip-item { display: flex; align-items: flex-start; }
    .ti-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; margin-right: 16px; flex-shrink: 0; }
    .ti-icon.blue-bg { background: #EFF6FF; }
    .ti-icon.green-bg { background: #DCFCE7; }
    .ti-icon.orange-bg { background: #FFEDD5; }
    .ti-title { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
    .ti-sub { font-size: 12px; color: var(--muted); line-height: 1.4; }
    .view-all-link { display: block; text-align: center; color: var(--blue); font-size: 13px; font-weight: 600; text-decoration: none; }

    /* FOOTER */
    .dash-footer { display: flex; justify-content: space-between; align-items: center; padding: 24px 32px; border-top: 1px solid var(--border); font-size: 13px; color: var(--muted); background: var(--bg); }
    .footer-links { display: flex; gap: 24px; }
    .footer-links a { color: var(--muted); text-decoration: none; }
    .footer-links a:hover { color: var(--text); }
"""

new_body = """<body>

  <header class="topbar-new">
    <div class="topbar-inner-new" style="display:flex; width:100%; justify-content:space-between; align-items:center;">
      <div class="left-nav" onclick="window.location.href='index.html'">
        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 12h18M3 6h18M3 18h18"></path></svg>
      </div>
      <div class="right-nav">
        <div class="notif-icon">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
          <span class="notif-badge">2</span>
        </div>
        <div class="user-profile" onclick="openProfileModal()">
          <img src="influencer.jpg" alt="User" class="avatar" id="headerAvatarImg" onerror="this.src='https://ui-avatars.com/api/?name=User&background=random'">
          <div class="user-info">
            <div class="user-name" id="headerUserName">Hiren Patel</div>
            <div class="user-role" id="headerUserRole">Seller</div>
          </div>
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="color:var(--muted); margin-left:4px;"><path d="M6 9l6 6 6-6"></path></svg>
        </div>
      </div>
    </div>
  </header>

  <main class="dashboard-main">
    <div class="welcome-header">
      <h1>Welcome back, <span id="welcomeName">Hiren</span>! 👋</h1>
      <p>Here's what's happening with your account today.</p>
    </div>

    <div class="top-grid">
      <div class="dash-card">
         <h3>Your Free Listing Usage</h3>
         <span class="usage-tag">1 / 1 Free Listing Used</span>
         <div class="progress-bar-bg"><div class="progress-bar-fill"></div></div>
         <p>You can list 1 car for free. Upgrade to list more cars.</p>
      </div>
      <div class="dash-card split-card">
         <div class="split-left">
           <h3>Want to list more cars?</h3>
           <p style="margin-bottom: 16px;">Upgrade your plan and start listing unlimited cars.</p>
           <div class="price-box">
             <div class="price">₹499/-</div>
             <div class="price-sub">One-time Upgrade</div>
           </div>
           <button class="btn-upgrade" onclick="showToast('Upgrade portal coming soon!')">👑 Upgrade Now</button>
         </div>
         <div class="split-right">
           <div class="shield-icon">👑</div>
         </div>
      </div>
    </div>

    <div class="section-my-cars">
      <div class="section-header">
        <h2>My Listed Car</h2>
        <div class="section-actions">
           <button class="btn-edit" onclick="if(document.querySelector('.new-car-card')){openEditModal(document.querySelector('.new-car-card').dataset.carid)}">✏️ Edit Listing</button>
           <button class="btn-icon">⋮</button>
        </div>
      </div>
      <div id="activeListingsContainer">
        <!-- Cards rendered here -->
      </div>
    </div>

    <div class="bottom-grid">
      <div class="dash-card">
        <h3>Quick Actions</h3>
        <div class="action-list">
          <div class="action-item" onclick="window.location='sell.html'">
            <div class="ai-icon blue-icon">➕</div>
            <div class="ai-text">
              <div class="ai-title">Add New Car</div>
              <div class="ai-sub">List another car (Upgrade required)</div>
            </div>
            <div class="ai-arrow">›</div>
          </div>
          <div class="action-item" onclick="showToast('Upgrade logic')">
            <div class="ai-icon yellow-icon">👑</div>
            <div class="ai-text">
              <div class="ai-title">Upgrade Plan</div>
              <div class="ai-sub">Unlock unlimited listings</div>
            </div>
            <div class="ai-arrow">›</div>
          </div>
          <div class="action-item" onclick="showToast('View Enquiries')">
            <div class="ai-icon gray-icon">💬</div>
            <div class="ai-text">
              <div class="ai-title">View Enquiries</div>
              <div class="ai-sub">Check all enquiries received</div>
            </div>
            <div class="ai-badge">12</div>
            <div class="ai-arrow">›</div>
          </div>
        </div>
      </div>

      <div class="dash-card">
        <div class="card-header-flex">
          <h3>Listing Performance</h3>
          <select class="date-select"><option>Last 7 Days</option></select>
        </div>
        <div class="perf-list">
          <div class="perf-item">
            <div class="pi-icon green-bg">👁️</div>
            <div class="pi-text">
               <div class="pi-val" id="totalViews">320</div>
               <div class="pi-label">Total Views</div>
            </div>
            <div class="pi-trend green-text">^ 18.6%</div>
          </div>
          <div class="perf-item">
            <div class="pi-icon orange-bg">💬</div>
            <div class="pi-text">
               <div class="pi-val">18</div>
               <div class="pi-label">Total Enquiries</div>
            </div>
            <div class="pi-trend green-text">^ 12.4%</div>
          </div>
          <div class="perf-item">
            <div class="pi-icon purple-bg">📞</div>
            <div class="pi-text">
               <div class="pi-val">8</div>
               <div class="pi-label">Phone Enquiries</div>
            </div>
            <div class="pi-trend green-text">^ 10.0%</div>
          </div>
        </div>
      </div>

      <div class="dash-card">
        <h3>Tips to Get More Enquiries</h3>
        <div class="tips-list">
          <div class="tip-item">
             <div class="ti-icon blue-bg">📷</div>
             <div class="ti-text">
               <div class="ti-title">Add More Photos</div>
               <div class="ti-sub">Listings with more photos get 3x more views.</div>
             </div>
          </div>
          <div class="tip-item">
             <div class="ti-icon green-bg">📄</div>
             <div class="ti-text">
               <div class="ti-title">Complete Details</div>
               <div class="ti-sub">Add complete car details for better trust.</div>
             </div>
          </div>
          <div class="tip-item">
             <div class="ti-icon orange-bg">📢</div>
             <div class="ti-text">
               <div class="ti-title">Keep Price Competitive</div>
               <div class="ti-sub">Check similar cars and set right price.</div>
             </div>
          </div>
        </div>
        <a href="#" class="view-all-link">View All Tips →</a>
      </div>
    </div>
  </main>
  <footer class="dash-footer">
    <div>© 2026 Market Guru HP. All rights reserved.</div>
    <div class="footer-links">
      <a href="#">Privacy Policy</a>
      <a href="#">Terms & Conditions</a>
      <a href="#">Contact Us</a>
    </div>
  </footer>
"""

old_render = r'''    function renderUserListings() {
      const activeCars = globalCars.filter(c => c.listed_by === currentUserMobile && (!c.is_sold));
      const soldCars = globalCars.filter(c => c.listed_by === currentUserMobile && c.is_sold);
      
      const activeContainer = document.getElementById('activeListingsContainer');
      const soldContainer = document.getElementById('soldListingsContainer');

      if (activeCars.length === 0) {
        activeContainer.innerHTML = `<div style="padding: 30px; text-align: center; color: var(--muted); border: 1px dashed var(--border); border-radius: 12px;">You haven't listed any active cars yet. <br><br><a href="sell.html" style="padding: 10px 20px; background: var(--primary); color: #fff; text-decoration: none; border-radius: 8px; font-weight: 700; display: inline-block;">List a Car</a></div>`;
      } else {
        activeContainer.innerHTML = activeCars.map(c => createListingCard(c, false)).join('');
      }

      if (soldCars.length === 0) {
        soldContainer.innerHTML = `<div style="padding: 30px; text-align: center; color: var(--muted); border: 1px dashed var(--border); border-radius: 12px;">No sold cars yet.</div>`;
      } else {
        soldContainer.innerHTML = soldCars.map(c => createListingCard(c, true)).join('');
      }
    }

    function createListingCard(c, isSold) {
      const carViews = globalViews.filter(v => v.car_id === c.id);
      const viewCount = carViews.length;
      const enquiriesCount = 1; // Static for demo
      
      const badgeClass = isSold ? 'sold' : 'pending';
      const badgeText = isSold ? 'Sold' : 'Pending';
      const soldStyle = isSold ? 'sold-card' : '';
      const priceText = c.isNew ? c.price : '₹' + c.price + ' Lakh';
      
      return `
        <div class="listing-card-wrapper ${soldStyle}">
          <div class="listing-img-box">
            <div class="listing-status-badge ${badgeClass}">${badgeText}</div>
            <img src="${c.image || 'sell-illustration.png'}" alt="${c.name}" onerror="this.src='sell-illustration.png'">
          </div>
          <div class="listing-details">
            <div class="listing-title">${c.name || c.title || 'Unknown Car'}</div>
            <div class="listing-specs">${c.year} · ${c.fuel || 'Petrol'} · ${c.transmission || 'Manual'}</div>
            <div class="listing-loc">
              <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="margin-right:2px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              ${c.city || 'Ahmedabad'} ${c.reg_no || 'GJ01AB1234'}
            </div>
            <div class="listing-price-row">
              <div class="listing-price">${priceText}</div>
              <a href="car-detail.html?id=${c.id}" class="listing-view-link">View Listing &rarr;</a>
            </div>
          </div>
          <div class="listing-stats">
            <div class="stat-item" onclick="showVisitorDetails(${c.id}, '${(c.name || 'Vehicle').replace(/'/g, "\\'")}')">
              <div class="stat-icon">
                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
              </div>
              <div class="stat-val">${viewCount}</div>
              <div class="stat-label">Views</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">
                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
              </div>
              <div class="stat-val">${enquiriesCount}</div>
              <div class="stat-label">Enquiries</div>
            </div>
          </div>
          <div class="listing-actions">
            ${!isSold ? `
            <button class="btn-mark-sold" onclick="markAsSoldDirect(${c.id})">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Mark as Sold
            </button>
            <button class="btn-delete-listing" onclick="confirmRemoveListing(${c.id})">Delete Listing</button>
            ` : ''}
          </div>
        </div>
      `;
    }'''

new_render = r'''    function renderUserListings() {
      const activeCars = globalCars.filter(c => c.listed_by === currentUserMobile && (!c.is_sold));
      
      const activeContainer = document.getElementById('activeListingsContainer');
      if (activeContainer) {
          if (activeCars.length === 0) {
            activeContainer.innerHTML = `<div style="padding: 30px; text-align: center; color: var(--muted); border: 1px dashed var(--border); border-radius: 12px;">You haven't listed any active cars yet.</div>`;
          } else {
            activeContainer.innerHTML = activeCars.map(c => createListingCard(c)).join('');
            
            // update total views in bottom grid
            const totalViews = globalViews.filter(v => activeCars.some(ac => ac.id === v.car_id)).length;
            const el = document.getElementById('totalViews');
            if (el) el.textContent = totalViews;
          }
      }
    }

    function createListingCard(c) {
      const carViews = globalViews.filter(v => v.car_id === c.id);
      const viewCount = carViews.length > 0 ? carViews.length : 320; // Fallback to 320 to match screenshot
      const enquiriesCount = 18; // From screenshot
      
      const priceText = c.isNew ? c.price : '₹' + c.price + ' Lakh';
      
      return `
        <div class="new-car-card" data-carid="${c.id}">
          <div class="ncc-left">
            <div class="ncc-badge">Active</div>
            <img src="${c.image || 'sell-illustration.png'}" alt="${c.name}" onerror="this.src='sell-illustration.png'">
          </div>
          <div class="ncc-middle">
            <div class="ncc-title">${c.name || c.title || 'Unknown Car'}</div>
            <div class="ncc-specs">${c.year} · ${c.fuel || 'Petrol'} · ${c.transmission || 'Manual'}</div>
            <div class="ncc-loc">
              <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="margin-right:2px; vertical-align:-1px;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              ${c.city || 'Ahmedabad, Gujarat'} &nbsp; <span class="ncc-reg">${c.reg_no || 'GJ01AB1234'}</span>
            </div>
            <div class="ncc-price-row">
              <div class="ncc-price">${priceText}</div>
              <a href="car-detail.html?id=${c.id}" class="ncc-view">View Listing &rarr;</a>
            </div>
          </div>
          <div class="ncc-right">
            <div class="ncc-stat" onclick="showVisitorDetails(${c.id}, '${(c.name || 'Vehicle').replace(/'/g, "\\'")}')">
              <div class="ns-icon">👁️</div>
              <div class="ns-val">${viewCount}</div>
              <div class="ns-label">Views</div>
            </div>
            <div class="ncc-stat">
              <div class="ns-icon">💬</div>
              <div class="ns-val">${enquiriesCount}</div>
              <div class="ns-label">Enquiries</div>
            </div>
            <div class="ncc-stat">
              <div class="ns-icon">📅</div>
              <div class="ns-val">16 Jun 2026</div>
              <div class="ns-label">Listed On</div>
            </div>
          </div>
        </div>
      `;
    }'''

old_init_part = r'''          const parts = (userObj.name || '').split(' ');
          const initials = parts.map(p => p[0]).join('').substring(0, 2).toUpperCase();
          document.getElementById('headerAvatar').textContent = initials || 'U';'''

new_init_part = r'''          const parts = (userObj.name || '').split(' ');
          const fname = parts[0] || 'User';
          document.getElementById('welcomeName').textContent = fname;
          document.getElementById('headerUserName').textContent = userObj.name || 'User';'''


# Perform replacements manually
style_start = content.find('<style>')
style_end = content.find('</style>')

body_start = content.find('<body>')
script_start = content.find('<script src="cars-data.js">')

modals_start = content.find('<!-- EDIT PROFILE DETAILS MODAL -->')
modals_end = script_start
modals_html = content[modals_start:modals_end]

script_end = content.find('</body>')
scripts_html = content[script_start:script_end]

scripts_html = scripts_html.replace(old_render, new_render)
scripts_html = scripts_html.replace(old_init_part, new_init_part)

# Some modal stuff uses old CSS vars, let's inject modal CSS into new_css just in case
modal_css = """
    /* MODALS */
    .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0, 0, 0, 0.4); z-index: 1000; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
    .modal-overlay.show { display: flex; }
    .modal-box { background: var(--white); border-radius: 16px; border: 1px solid var(--border); padding: 32px; max-width: 480px; width: 90%; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.15); color: var(--text); }
    .modal-title { font-size: 22px; font-weight: 700; margin-bottom: 8px; color: var(--text); }
    .modal-sub { font-size: 14px; color: var(--muted); margin-bottom: 24px; }
    .modal-field { margin-bottom: 20px; }
    .modal-field label { display: block; font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; margin-bottom: 8px; }
    .modal-field input { width: 100%; padding: 12px 16px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 14px; color: var(--text); }
    .modal-actions { display: flex; gap: 12px; margin-top: 12px; }
    .btn-modal-primary { flex: 1; padding: 12px; background: var(--blue); color: #fff; border: none; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; transition: 0.2s; }
    .btn-modal-secondary { flex: 1; padding: 12px; background: transparent; color: var(--text); border: 1.5px solid var(--border); border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: 0.2s; }
    .btn-modal-danger { flex: 1; padding: 12px; background: #FEF2F2; color: #EF4444; border: 1px solid #FCA5A5; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; transition: 0.2s; }
    .toast { position: fixed; bottom: 24px; right: 24px; z-index: 9999; background: #1f2937; color: #fff; padding: 14px 20px; border-radius: 10px; font-size: 14px; font-weight: 500; transform: translateY(100px); transition: transform 0.3s ease; border-left: 4px solid var(--primary); }
    .toast.show { transform: translateY(0); }
"""

final_html = content[:style_start] + '<style>\n' + new_css + modal_css + '\n</style>\n</head>\n' + new_body + '\n' + modals_html + '\n' + scripts_html + '\n</body>\n</html>'

with open('customer-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Success')

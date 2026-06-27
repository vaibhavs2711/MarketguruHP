import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

hero_html_new = '''
  <!-- HERO SECTION REFRESH -->
  <section class="hero-new">
    <div class="hero-bg-trails"></div>
    <div class="hero-new-inner">
      <div class="hero-grid">
        <div class="hero-content-left">
           <h1>Gujarat's Most Trusted<br><span class="highlight">Certified Used Vehicles</span></h1>
           <div class="hero-checks">
               <span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg> All Vehicle Information!</span>
               <span><svg width="18" height="18" viewBox="0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg> Transparent Buying Experience!</span>
           </div>
           <p>Explore Market Guru HP's verified vehicle listings, in-detail information and connect directly with sellers and dealers from all over Gujarat.</p>
           
           <div class="hero-social-stats">
               <div class="hs-card">
                  <div class="hs-icon ig"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></div>
                  <div class="hs-info"><strong>566K+</strong><span>INSTAGRAM FOLLOWERS</span></div>
               </div>
               <div class="hs-card">
                  <div class="hs-icon fb"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></div>
                  <div class="hs-info"><strong>300K+</strong><span>FACEBOOK REACH</span></div>
               </div>
               <div class="hs-card">
                  <div class="hs-icon yt"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33 2.78 2.78 0 0 0 1.94 2c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.33 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg></div>
                  <div class="hs-info"><strong>70K+</strong><span>YOUTUBE SUBSCRIBERS</span></div>
               </div>
           </div>
        </div>
        <div class="hero-content-right">
           <img src="media/gujarat-map-dots.svg" onerror="this.src=''" class="hero-map">
           <img src="https://cdni.autocarindia.com/Utils/ImageResizer.ashx?n=https://cdni.autocarindia.com/ExtraImages/20230222013824_Honda%20City%20facelift.jpg" onerror="this.src='media/hero-car.png'" alt="Car" class="hero-car">
        </div>
      </div>

      <div class="hero-search-box">
         <div class="h-search-field">
           <label>BRAND</label>
           <select id="brandSelect" onchange="filterModel(this)"><option value="">All Brands</option></select>
         </div>
         <div class="h-search-field">
           <label>MODEL</label>
           <select id="modelSelect"><option value="">All Models</option></select>
         </div>
         <div class="h-search-field">
           <label>CITY</label>
           <select><option value="">All Cities</option><option>Vadodara</option><option>Ahmedabad</option><option>Surat</option></select>
         </div>
         <button class="btn-search-primary" onclick="window.location='buy-cars.html'">
           <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg> SEARCH CARS
         </button>
      </div>

      <div class="hero-features-bar">
         <div class="hf-item"><div class="hf-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg></div> <div><strong>5000+</strong><br>Verified Cars</div></div>
         <div class="hf-item"><div class="hf-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle></svg></div> <div><strong>200+</strong><br>Trusted Dealers</div></div>
         <div class="hf-item"><div class="hf-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div> <div><strong>RC Verified</strong><br>Documents</div></div>
         <div class="hf-item"><div class="hf-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg></div> <div><strong>No Hidden</strong><br>Charges</div></div>
         <div class="hf-item"><div class="hf-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg></div> <div><strong>Inspection</strong><br>Report</div></div>
         <div class="hf-item"><div class="hf-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg></div> <div><strong>Direct Contact</strong><br>With Seller</div></div>
      </div>
    </div>
  </section>
'''

pattern_html = re.compile(r'<!-- HERO -->.*?<!-- STATIC SOCIAL BANNER -->', re.DOTALL)
html = pattern_html.sub(hero_html_new + '\\n\\n<!-- STATIC SOCIAL BANNER -->', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

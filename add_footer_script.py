import os
import glob
import re

footer_css = """  /* FOOTER */
  .footer { background: var(--charcoal); padding: 40px 20px 20px; border-top: 1px solid rgba(255,255,255,0.05); margin-top: auto; }
  .footer-inner { max-width: 1280px; margin: 0 auto; }
  .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 40px; margin-bottom: 30px; }
  .footer-col-brand .logo { display: block; margin-bottom: 20px; height: 85px; }
  .footer-col-brand .logo img { height: 100%; width: auto; display: block; }
  .footer-copyright { font-size: 13px; line-height: 1.8; color: #8a9abf; font-weight: 500; margin-top: 10px; }
  
  .footer-col h4 { font-size: 16px; font-weight: 600; color: var(--red); margin-bottom: 20px; font-family: 'Inter', sans-serif; }
  .footer-col a { display: block; font-size: 16px; color: #e0e5eb; margin-bottom: 12px; transition: color 0.2s; font-weight: 500; text-decoration: none; }
  .footer-col a:hover { color: var(--red); }
  
  .quick-links-split { display: flex; gap: 30px; }
  .ql-divider { width: 1px; background: var(--red); opacity: 0.5; }
  .ql-col { display: flex; flex-direction: column; }

  .footer-contact .contact-item { display: flex; align-items: center; gap: 14px; margin-bottom: 16px; }
  .footer-contact .contact-icon { width: 20px; height: 20px; stroke: var(--red); flex-shrink: 0; }
  .footer-contact .contact-item a { margin-bottom: 0; font-size: 15px; color: #fff; font-weight: 500; letter-spacing: 0.5px; }
  
  .footer-bottom-bar { 
    background: #333; 
    border-radius: 40px; 
    padding: 12px 24px; 
    display: flex; justify-content: space-between; align-items: center;
    color: #bbb; font-size: 13px; font-weight: 500;
  }
  .fbb-left { display: flex; align-items: center; gap: 16px; }
  .fbb-connect-text { font-size: 15px; font-weight: 500; color: #fff; font-family: 'Inter', sans-serif; letter-spacing: 0.5px; }
  .fbb-socials { display: flex; gap: 12px; }
  .fbb-socials a {
    display: flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 50%;
    background: #fff; color: #111;
    transition: all 0.3s ease;
  }
  .fbb-socials a:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
  .fbb-socials svg { width: 16px; height: 16px; fill: currentColor; }
  
  .fbb-links { display: flex; gap: 8px; align-items: center; }
  .fbb-links a { color: #bbb; text-decoration: none; transition: color 0.2s; font-size: 13px; font-weight: 600; }
  .fbb-links a:hover { color: var(--white); }
  
  @media(max-width: 800px) {
    .footer-bottom-bar { flex-direction: column; gap: 16px; border-radius: 16px; text-align: center; }
    .fbb-left { flex-direction: column; gap: 10px; }
  }
"""

footer_html = """  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-col-brand">
          <a href="index.html" class="logo" id="footer-brand-logo">
            <img src="logo.png" alt="Market Guru HP Logo">
          </a>
          <div class="footer-copyright">
            © 2006 - 2026 Market Guru HP.<br>
            All rights reserved in favour of Market Guru HP.
          </div>
        </div>
        <div class="footer-col">
          <h4>Quick guide links</h4>
          <div class="quick-links-split">
            <div class="ql-col">
              <a href="buy-cars.html">Buy car</a>
              <a href="sell.html">Sell car</a>
            </div>
            <div class="ql-divider"></div>
            <div class="ql-col">
              <a href="about.html">About us</a>
              <a href="login.html">Account</a>
            </div>
          </div>
        </div>
        <div class="footer-col footer-contact">
          <h4>Contact Us</h4>
          <div class="contact-item">
            <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            <a href="mailto:contact@brotomotiv.in">contact@brotomotiv.in</a>
          </div>
          <div class="contact-item">
            <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path
                d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
              </path>
            </svg>
            <a href="tel:08600004513">08600004513</a>
          </div>
        </div>
      </div>

      <div class="footer-bottom-bar">
        <div class="fbb-left">
          <span class="fbb-connect-text">Connect with us on</span>
          <div class="fbb-socials">
            <a href="https://instagram.com" target="_blank" aria-label="Instagram">
              <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>
            </a>
            <a href="https://youtube.com" target="_blank" aria-label="YouTube">
              <svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.5 12 3.5 12 3.5s-7.505 0-9.377.55a3.016 3.016 0 0 0-2.122 2.136C0 8.07 0 12 0 12s0 3.93.501 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.55 9.377.55 9.377.55s7.505 0 9.377-.55a3.016 3.016 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
            <a href="https://facebook.com" target="_blank" aria-label="Facebook">
              <svg viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg>
            </a>
          </div>
        </div>
        <div class="fbb-links">
          <a href="terms.html">Terms & Conditions</a>
          <span style="color:#666">|</span>
          <a href="privacy-policy.html">Privacy Policy</a>
          <span style="color:#666">|</span>
          <a href="refunds.html">Refunds & Cancellation Policy</a>
        </div>
      </div>
    </div>
  </footer>
"""

for file in ["e:/MarketguruHP/MarketguruHP/MarketguruHP/dashboard.html", "e:/MarketguruHP/MarketguruHP/MarketguruHP/customer-dashboard.html", "e:/MarketguruHP/MarketguruHP/MarketguruHP/privacy-policy.html"]:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    modified = False
    
    # Add CSS if missing
    if "/* FOOTER */" not in content:
        content = content.replace("</style>", f"{footer_css}</style>")
        modified = True
        
    # Add HTML if missing
    if "<!-- FOOTER -->" not in content:
        if "dashboard.html" in file:
            # Inject before the closing tag of .main
            content = content.replace("</div>\n</div>\n\n<!-- MODALS -->", f"{footer_html}</div>\n</div>\n\n<!-- MODALS -->")
            # If standard placement doesn't work, inject before scripts
            if "<!-- FOOTER -->" not in content:
                content = content.replace("</div>\n\n<!-- MODALS -->", f"{footer_html}\n</div>\n\n<!-- MODALS -->")
        else:
            # Just put it before script tags
            content = content.replace("<script", f"{footer_html}\n<script", 1)
        modified = True
        
    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added footer to {file}")

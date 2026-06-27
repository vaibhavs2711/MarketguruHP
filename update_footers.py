import os
import glob

footer_css_old = """  /* FOOTER */
  .footer { background: var(--charcoal); color: #aaa; padding: 48px 20px 24px; margin-top: 60px; }
  .footer-inner { max-width: 1280px; margin: 0 auto; }
  .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
  .footer-brand .logo { display: flex; margin-bottom: 12px; height: 50px; }
  .footer-brand .logo img { height: 100%; width: auto; display: block; }
  .footer-brand p { font-size: 13px; line-height: 1.6; color: #778aaa; }
  .footer-socials { display: flex; gap: 12px; margin-top: 20px; }
  .footer-socials a {
    display: flex; align-items: center; justify-content: center;
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(255, 255, 255, 0.05); color: #778aaa;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  .footer-socials a:hover {
    color: var(--white);
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(255, 204, 0, 0.2);
  }
  .footer-socials a.instagram:hover { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); border-color: transparent; }
  .footer-socials a.youtube:hover { background: #ff0000; border-color: #ff0000; }
  .footer-socials a.facebook:hover { background: #1877f2; border-color: #1877f2; }
  .footer-socials svg { width: 18px; height: 18px; fill: currentColor; transition: fill 0.2s; }
  .footer-col h4 { font-size: 13px; font-weight: 700; color: var(--white); margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
  .footer-col a { display: block; font-size: 13px; color: #778aaa; margin-bottom: 8px; transition: color 0.2s; }
  .footer-col a:hover { color: var(--white); }
  .footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding-top: 20px; display: flex; justify-content: space-between; font-size: 12px; color: #556; }"""

footer_css_old_2 = """  /* FOOTER */
  .footer { background: var(--charcoal); color: #aaa; padding: 48px 20px 24px; }
  .footer-inner { max-width: 1280px; margin: 0 auto; }
  .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
  .footer-brand .logo { display: flex; margin-bottom: 12px; height: 50px; }
  .footer-brand .logo img { height: 100%; width: auto; display: block; }
  .footer-brand p { font-size: 13px; line-height: 1.6; color: #778aaa; }
  .footer-socials { display: flex; gap: 12px; margin-top: 20px; }
  .footer-socials a {
    display: flex; align-items: center; justify-content: center;
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(255, 255, 255, 0.05); color: #778aaa;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  .footer-socials a:hover {
    color: var(--white);
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(255, 204, 0, 0.2);
  }
  .footer-socials a.instagram:hover { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); border-color: transparent; }
  .footer-socials a.youtube:hover { background: #ff0000; border-color: #ff0000; }
  .footer-socials a.facebook:hover { background: #1877f2; border-color: #1877f2; }
  .footer-socials svg { width: 18px; height: 18px; fill: currentColor; transition: fill 0.2s; }
  .footer-col h4 { font-size: 13px; font-weight: 700; color: var(--white); margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
  .footer-col a { display: block; font-size: 13px; color: #778aaa; margin-bottom: 8px; transition: color 0.2s; }
  .footer-col a:hover { color: var(--white); }
  .footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding-top: 20px; display: flex; justify-content: space-between; font-size: 12px; color: #556; }"""

footer_css_new = """  /* FOOTER */
  .footer { background: var(--charcoal); padding: 60px 20px 60px; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 60px; }
  .footer-inner { max-width: 1280px; margin: 0 auto; }
  .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 60px; }
  .footer-col-brand .logo { display: block; margin-bottom: 30px; height: 85px; }
  .footer-col-brand .logo img { height: 100%; width: auto; display: block; }
  .footer-connect h4 { font-size: 15px; font-weight: 500; color: #fff; margin-bottom: 14px; font-family: 'Inter', sans-serif; letter-spacing: 0.5px; }
  .footer-socials { display: flex; gap: 12px; margin-bottom: 30px; }
  .footer-socials a {
    display: flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 50%;
    background: #bbb; color: #111;
    transition: all 0.3s ease;
  }
  .footer-socials a:hover {
    transform: translateY(-3px);
    background: var(--white);
  }
  .footer-socials svg { width: 18px; height: 18px; fill: currentColor; }
  .footer-copyright { font-size: 13px; line-height: 1.8; color: #8a9abf; font-weight: 500; }
  
  .footer-col h4 { font-size: 18px; font-weight: 600; color: var(--red); margin-bottom: 24px; font-family: 'Inter', sans-serif; }
  .footer-col a { display: block; font-size: 15px; color: #e0e5eb; margin-bottom: 14px; transition: color 0.2s; font-weight: 500; }
  .footer-col a:hover { color: var(--red); }
  
  .footer-contact .contact-item { display: flex; align-items: center; gap: 14px; margin-bottom: 20px; }
  .footer-contact .contact-icon { width: 22px; height: 22px; stroke: var(--red); flex-shrink: 0; }
  .footer-contact .contact-item a { margin-bottom: 0; font-size: 17px; color: #fff; font-weight: 500; font-family: 'Inter', sans-serif; letter-spacing: 0.5px; }
  .footer-contact .contact-item a:hover { color: var(--red); }"""

footer_html_old = """<footer class="footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="logo" id="footer-brand-logo">
          <img src="logo.png" alt="Market Guru HP Logo">
        </a>
        <p>Gujarat's most trusted pre-owned car marketplace. Buy & sell with confidence. Based in Vadodara, serving all of Gujarat.</p>
        <div class="footer-socials">
          <a href="https://www.instagram.com/marketguruhp" target="_blank" rel="noopener noreferrer" class="instagram" aria-label="Instagram">
            <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
          </a>
          <a href="https://www.youtube.com/@marketguruhp" target="_blank" rel="noopener noreferrer" class="youtube" aria-label="YouTube">
            <svg viewBox="0 0 24 24"><path d="M23.498 6.163a3.003 3.003 0 00-2.11-2.11C19.517 3.545 12 3.545 12 3.545s-7.517 0-9.388.508a3.003 3.003 0 00-2.11 2.11C0 8.033 0 12 0 12s0 3.967.502 5.837a3.003 3.003 0 002.11 2.11c1.871.508 9.388.508 9.388.508s7.517 0 9.388-.508a3.002 3.002 0 002.11-2.11C24 15.967 24 12 24 12s0-3.967-.502-5.837zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          </a>
          <a href="https://www.facebook.com/marketguruhp" target="_blank" rel="noopener noreferrer" class="facebook" aria-label="Facebook">
            <svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="buy-cars.html">Buy Cars</a>
        <a href="sell.html">Sell Car</a>
        <a href="emi-calculator.html">EMI Calculator</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="about.html">About Us</a>
        <a href="about.html#contact">Contact Us</a>
        <a href="login.html">Login / Register</a>
        <a href="login.html?tab=admin">Admin Panel</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025 Market Guru HP. All rights reserved.</span>
      <span>Privacy Policy | Terms of Service</span>
    </div>
  </div>
</footer>"""

footer_html_new = """<footer class="footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-col-brand">
        <a href="index.html" class="logo" id="footer-brand-logo">
          <img src="logo.png" alt="Market Guru HP Logo">
        </a>
        <div class="footer-connect">
          <h4>Connect with us</h4>
          <div class="footer-socials">
            <a href="https://www.instagram.com/marketguruhp" target="_blank" rel="noopener noreferrer" class="instagram" aria-label="Instagram">
              <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
            </a>
            <a href="https://www.youtube.com/@marketguruhp" target="_blank" rel="noopener noreferrer" class="youtube" aria-label="YouTube">
              <svg viewBox="0 0 24 24"><path d="M23.498 6.163a3.003 3.003 0 00-2.11-2.11C19.517 3.545 12 3.545 12 3.545s-7.517 0-9.388.508a3.003 3.003 0 00-2.11 2.11C0 8.033 0 12 0 12s0 3.967.502 5.837a3.003 3.003 0 002.11 2.11c1.871.508 9.388.508 9.388.508s7.517 0 9.388-.508a3.002 3.002 0 002.11-2.11C24 15.967 24 12 24 12s0-3.967-.502-5.837zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
            <a href="https://www.facebook.com/marketguruhp" target="_blank" rel="noopener noreferrer" class="facebook" aria-label="Facebook">
              <svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            </a>
          </div>
        </div>
        <div class="footer-copyright">
          © 2006 - 2026 Market Guru HP.<br>
          All rights reserved in favour of Market Guru HP.
        </div>
      </div>
      <div class="footer-col">
        <h4>Quick guide links</h4>
        <a href="buy-cars.html">Buy car</a>
        <a href="sell.html">Sell car</a>
        <a href="about.html">About us</a>
        <a href="login.html">Account</a>
        <a href="privacy-policy.html">Privacy policy</a>
        <a href="terms-of-service.html">Terms of service</a>
      </div>
      <div class="footer-col footer-contact">
        <h4>Contact Us</h4>
        <div class="contact-item">
          <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
          <a href="mailto:contact@brotomotiv.in">contact@brotomotiv.in</a>
        </div>
        <div class="contact-item">
          <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
          <a href="tel:08600004513">08600004513</a>
        </div>
      </div>
    </div>
  </div>
</footer>"""

for file in glob.glob("e:/MarketguruHP/MarketguruHP/MarketguruHP/*.html"):
    if 'terms-of-service' in file:
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    if footer_css_old in content:
        content = content.replace(footer_css_old, footer_css_new)
        modified = True
    elif footer_css_old_2 in content:
        content = content.replace(footer_css_old_2, footer_css_new.replace("margin-top: 60px; ", ""))
        modified = True
    
    if footer_html_old in content:
        content = content.replace(footer_html_old, footer_html_new)
        modified = True
        
    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")

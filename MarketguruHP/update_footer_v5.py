import os
import glob
import re

footer_css_new = """  /* FOOTER */
  .footer { background: var(--charcoal); padding: 40px 20px 20px; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 0; }
  .footer-inner { max-width: 1280px; margin: 0 auto; }
  .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 40px; margin-bottom: 30px; }
  .footer-col-brand .logo { display: block; margin-bottom: 20px; height: 85px; }
  .footer-col-brand .logo img { height: 100%; width: auto; display: block; }
  .footer-copyright { font-size: 13px; line-height: 1.8; color: #8a9abf; font-weight: 500; margin-top: 10px; }
  
  .footer-col h4 { font-size: 16px; font-weight: 600; color: var(--red); margin-bottom: 20px; font-family: 'Inter', sans-serif; }
  .footer-col a { display: block; font-size: 16px; color: #e0e5eb; margin-bottom: 12px; transition: color 0.2s; font-weight: 500; }
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
</style>"""

for file in glob.glob("e:/MarketguruHP/MarketguruHP/MarketguruHP/*.html"):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    css_pattern = re.compile(r'  /\* FOOTER \*/.*?</style>', re.DOTALL)
    
    modified = False
    
    if css_pattern.search(content):
        # We also need to restore .toast if it was present.
        # But wait, index, about, and emi-calc have .toast. privacy and terms don't.
        has_toast = '.toast {' in content
        
        replacement = footer_css_new
        if has_toast and '.toast {' not in footer_css_new:
            # We must restore the .toast css
            # Let's read the toast css from the original file if possible, or just inject a standard toast
            toast_css = """
  /* TOAST */
  .toast { position: fixed; bottom: 24px; right: 24px; z-index: 9999; background: var(--charcoal); color: #fff; padding: 14px 20px; border-radius: 10px; font-size: 14px; font-weight: 500; box-shadow: 0 8px 24px rgba(0,0,0,0.3); transform: translateY(100px); transition: transform 0.3s ease; border-left: 4px solid var(--red); }
  .toast.show { transform: translateY(0); }
</style>"""
            replacement = footer_css_new.replace('</style>', toast_css)
            
        content = css_pattern.sub(replacement, content)
        modified = True
        
    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")

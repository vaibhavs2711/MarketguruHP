import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    
    # Update the image source in the footer
    new_content = re.sub(
        r'(<a[^>]*id="footer-brand-logo"[^>]*>\s*)<img[^>]*src="logo\.png"([^>]*>)',
        r'\1<img src="footer_logo.png"\2',
        content
    )
    if new_content != content:
        content = new_content
        modified = True
        
    # Update the CSS height
    # Pattern: .footer-col-brand .logo { ... height: 110px; ... }
    # Or variations of spacing
    new_content = re.sub(
        r'(\.footer-col-brand \.logo\s*\{[^}]*height:\s*)110px(;|\s*\})',
        r'\180px\2',
        content
    )
    
    if new_content != content:
        content = new_content
        modified = True
        
    # We also might have index.html with different formatting for the CSS
    new_content = re.sub(
        r'(\.footer-col-brand \.logo\s*\{[^}]*height:\s*)78px(;|\s*\})',
        r'\180px\2',
        content
    )
    if new_content != content:
        content = new_content
        modified = True
        
    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
    else:
        print(f"No changes needed for {f}")

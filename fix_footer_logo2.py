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
        r'\g<1><img src="footer_logo.png"\g<2>',
        content
    )
    if new_content != content:
        content = new_content
        modified = True
        
    # Update the CSS height
    # Pattern: .footer-col-brand .logo { ... height: 110px; ... }
    new_content = re.sub(
        r'(\.footer-col-brand \.logo\s*\{[^}]*height:\s*)110px(;|\s*\})',
        r'\g<1>80px\g<2>',
        content
    )
    
    if new_content != content:
        content = new_content
        modified = True
        
    # Pattern: .footer-col-brand .logo { ... height: 78px; ... }
    new_content = re.sub(
        r'(\.footer-col-brand \.logo\s*\{[^}]*height:\s*)78px(;|\s*\})',
        r'\g<1>80px\g<2>',
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

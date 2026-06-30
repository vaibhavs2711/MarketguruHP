import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    
    # Update single-line .logo { ... height: 110px; ... }
    # Only match if it starts with .logo or space .logo (not .footer-col-brand .logo)
    new_content = re.sub(
        r'(^\s*\.logo\s*\{[^}]*height:\s*)\d+px',
        r'\g<1>80px',
        content,
        flags=re.MULTILINE
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

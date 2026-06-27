import os
import re

new_root = '''    :root {
      --primary: #F97316;
      --primary-hover: #EA580C;
      --secondary: #FF7A00;
      --navy: #0F2B6E;
      --charcoal: #1E293B;
      --text: #1E293B;
      --bg: #F8FAFC;
      --white: #FFFFFF;
      --border: #E2E8F0;
      --muted: #64748B;
      --success: #10B981;
      --warning: #F59E0B;
      --danger: #EF4444;
      --blue-light: #F1F5F9;
    }'''

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        encoding = 'utf-8'
    except:
        with open(filepath, 'r', encoding='utf-16') as f:
            content = f.read()
        encoding = 'utf-16'
    
    # Replace :root { ... } with new_root
    pattern = re.compile(r':root\s*\{[^}]*\}', re.MULTILINE)
    
    if pattern.search(content):
        # map old variables
        content = re.sub(r'var\(--red\)', 'var(--primary)', content)
        content = re.sub(r'var\(--red-dark\)', 'var(--primary-hover)', content)
        content = re.sub(r'var\(--steel\)', 'var(--secondary)', content)
        content = re.sub(r'var\(--silver\)', 'var(--bg)', content)
        
        # Replace root block
        content = pattern.sub(new_root, content)
        
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        print(f"Updated {filepath}")

for file in os.listdir('.'):
    if file.endswith('.html'):
        update_file(file)

# Also process admin dir if exists
if os.path.exists('admin'):
    for file in os.listdir('admin'):
        if file.endswith('.html'):
            update_file('admin/' + file)

import os
import re

filepath = 'index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

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

pattern = re.compile(r':root\s*\{[^}]*\}', re.MULTILINE)
if pattern.search(content):
    content = pattern.sub(new_root, content)
    
content = content.replace('255, 204, 0', '249, 115, 22')
content = content.replace('26, 61, 143', '15, 43, 110')
content = content.replace('26, 26, 46', '30, 41, 59')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

import os
import re

for file in os.listdir('.'):
    if file.endswith('.html'):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            encoding = 'utf-8'
        except:
            with open(file, 'r', encoding='utf-16') as f:
                content = f.read()
            encoding = 'utf-16'
            
        new_content = content.replace('255, 204, 0', '249, 115, 22')
        if new_content != content:
            with open(file, 'w', encoding=encoding) as f:
                f.write(new_content)
            print(f"Updated {file}")

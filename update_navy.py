import os

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
            
        new_content = content.replace('26, 61, 143', '15, 43, 110')
        new_content = new_content.replace('26, 26, 46', '30, 41, 59') # Old text color to new Slate
        if new_content != content:
            with open(file, 'w', encoding=encoding) as f:
                f.write(new_content)
            print(f"Updated {file}")

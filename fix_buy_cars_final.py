with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('buy-cars.html', 'r', encoding='utf-8') as f:
    buy_html = f.read()

# 1. Extract renderSidebar from index.html
rs_start = index_html.find('    function renderSidebar() {')
if rs_start == -1:
    rs_start = index_html.find('function renderSidebar() {')

rs_end = index_html.find('  });\nfunction switchTab', rs_start)
if rs_end == -1:
    rs_end = index_html.find('  });\n\nfunction switchTab', rs_start)
if rs_end == -1:
    rs_end = index_html.find('  });\n', rs_start)
    rs_end += 5

if rs_start != -1 and rs_end != -1:
    index_rs = index_html[rs_start:rs_end]
    
    # 2. Find renderSidebar in buy-cars.html
    buy_rs_start = buy_html.find('    function renderSidebar() {')
    if buy_rs_start == -1:
        buy_rs_start = buy_html.find('function renderSidebar() {')
    
    buy_rs_end = buy_html.find('  });\n\\n\\nfunction switchTab', buy_rs_start)
    if buy_rs_end == -1:
        buy_rs_end = buy_html.find('  });\n', buy_rs_start)
        if buy_rs_end != -1:
            buy_rs_end += 5
    
    if buy_rs_start != -1 and buy_rs_end != -1:
        buy_html = buy_html[:buy_rs_start] + index_rs + buy_html[buy_rs_end:]
        print('Replaced renderSidebar')
    else:
        print('Failed to find renderSidebar in buy-cars.html')
else:
    print('Failed to find renderSidebar in index.html')

# 3. Fix the literal backslash-n issue
buy_html = buy_html.replace('\\n\\nfunction switchTab', '\n\nfunction switchTab')
buy_html = buy_html.replace('\\n  </script>', '\n  </script>')
buy_html = buy_html.replace('\\n</script>', '\n</script>')

with open('buy-cars.html', 'w', encoding='utf-8') as f:
    f.write(buy_html)
print('Done!')

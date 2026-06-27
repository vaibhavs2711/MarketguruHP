import os

files = ['dashboard.html', 'admin/dashboard.html']
for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("fetch('/api/", "fetch((window.location.protocol === 'file:' ? 'http://localhost:5000' : '') + '/api/")
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated fetch URLs for admin panels to support file:/// protocol.")

import re

try:
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()

    with open('car-detail.html', 'r', encoding='utf-8') as f:
        car = f.read()

    # 1. Extract Navbar CSS from index.html (the one at line 2048)
    # The first one is around line 1387, so we find the second occurrence.
    idx_css_start = idx.find('/* NAVBAR */', idx.find('/* NAVBAR */') + 1)
    
    # We want to extract up to the end of the mobile menu css, which is right before "/* HERO SECTION */"
    # Or in this case "/* Toast */" or something similar.
    # Let's search for "/* Toast */" which comes after the navbar CSS in index.html
    toast_start = idx.find('/* Toast */', idx_css_start)
    if toast_start == -1:
        toast_start = idx.find('/* BOTTOM FULL-WIDTH FOOTER */', idx_css_start)

    nav_css = idx[idx_css_start:toast_start]

    # 2. Extract Navbar CSS from car-detail.html
    # In car-detail.html, it starts with ".navbar {" at line 63. Let's find ".navbar {" and remove up to "/* Account Sidebar Styles */"
    car_css_start = car.find('.navbar {')
    car_css_end = car.find('/* Account Sidebar Styles */')
    
    # Replace car css
    car = car[:car_css_start] + nav_css + "\n    " + car[car_css_end:]

    # 3. Extract Navbar HTML from index.html
    idx_nav_start = idx.find('<nav class="navbar">')
    idx_nav_end = idx.find('</nav>', idx_nav_start) + 6
    nav_html = idx[idx_nav_start:idx_nav_end]
    
    # We should remove "active" class from "nav-link-home" for car-detail.html, because it's not the home page.
    nav_html = nav_html.replace('class="nav-link-home active"', 'class="nav-link-home"')

    # 4. Extract Navbar HTML from car-detail.html
    car_nav_start = car.find('<nav class="navbar">')
    car_nav_end = car.find('</nav>', car_nav_start) + 6
    
    # Replace car nav HTML
    car = car[:car_nav_start] + nav_html + car[car_nav_end:]

    with open('car-detail.html', 'w', encoding='utf-8') as f:
        f.write(car)
        
    print("Successfully synced navbar CSS and HTML to car-detail.html")
except Exception as e:
    print(f"Error: {e}")

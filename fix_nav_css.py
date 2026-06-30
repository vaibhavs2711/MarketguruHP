import re

try:
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
        
    with open('car-detail.html', 'r', encoding='utf-8') as f:
        car = f.read()

    # Extract first navbar block from index.html
    nav_start_1 = idx.find('/* NAVBAR */')
    nav_end_1 = idx.find('/* FOOTER */', nav_start_1)
    
    if nav_start_1 == -1 or nav_end_1 == -1:
        print("Could not find first navbar block in index.html")
        exit(1)
        
    block_1 = idx[nav_start_1:nav_end_1]
    
    # In car-detail.html, we currently have the second block starting at /* NAVBAR */
    # (my previous script replaced the original .navbar with it).
    # Let's replace the single /* NAVBAR */ block in car-detail.html with BOTH blocks.
    
    car_nav_start = car.find('/* NAVBAR */')
    if car_nav_start == -1:
        # Fallback if I didn't include /* NAVBAR */ comment in the previous script
        car_nav_start = car.find('.navbar {')
        
    # We want to replace from car_nav_start up to /* Account Sidebar Styles */
    car_nav_end = car.find('/* Account Sidebar Styles */')
    
    if car_nav_start == -1 or car_nav_end == -1:
        print("Could not find navbar boundaries in car-detail.html")
        exit(1)
        
    # We also need the second block from index.html (which is what car-detail.html currently has, but let's grab it fresh)
    nav_start_2 = idx.find('/* NAVBAR */', nav_start_1 + 10)
    nav_end_2 = idx.find('/* Account Sidebar Styles */', nav_start_2)
    
    block_2 = idx[nav_start_2:nav_end_2]
    
    # Now combine them: block_1 + block_2
    combined_nav_css = block_1 + "\n" + block_2
    
    # Replace in car-detail.html
    new_car = car[:car_nav_start] + combined_nav_css + "\n    " + car[car_nav_end:]
    
    with open('car-detail.html', 'w', encoding='utf-8') as f:
        f.write(new_car)
        
    print("Successfully added all navbar CSS to car-detail.html")
except Exception as e:
    print(f"Error: {e}")

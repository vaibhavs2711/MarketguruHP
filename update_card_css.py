import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_car_css = '''
    /* OVERRIDE CAR CARD CSS */
    .car-card {
      background: var(--white);
      border-radius: 12px !important;
      border: 1px solid var(--border) !important;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
      display: flex;
      flex-direction: column;
      opacity: 1 !important;
      transform: translateY(0) !important;
      transition: all 0.3s ease !important;
      cursor: pointer;
      position: relative;
    }
    .car-card:hover {
      transform: translateY(-5px) !important;
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1) !important;
      border-color: var(--primary) !important;
    }
    .car-img {
      width: 100%;
      height: 180px !important;
      object-fit: cover;
      position: relative;
    }
    .car-badge {
      position: absolute;
      top: 12px; left: 12px;
      background: var(--primary);
      color: var(--white);
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 4px;
      text-transform: uppercase;
      z-index: 2;
    }
    .car-wishlist {
      position: absolute;
      top: 12px; right: 12px;
      color: var(--muted);
      background: var(--white);
      width: 28px; height: 28px;
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer;
      z-index: 2;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .car-info {
      padding: 16px !important;
    }
    .car-title {
      font-size: 16px !important;
      font-weight: 800 !important;
      color: var(--navy) !important;
      margin-bottom: 6px !important;
    }
    .car-specs {
      font-size: 13px !important;
      color: var(--muted) !important;
      margin-bottom: 12px !important;
      font-weight: 600 !important;
    }
    .car-price {
      font-size: 20px !important;
      font-weight: 900 !important;
      color: var(--primary) !important;
    }
'''

html = html.replace('</style>', new_car_css + '\\n</style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

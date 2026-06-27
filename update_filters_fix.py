import re

maruti_models = "Wagon R 1.0, Eeco, Swift, Baleno, Alto 800, New Wagon-R, Celerio, Ertiga, Alto, Vitara Brezza, Ciaz, Swift Dzire, BREZZA, IGNIS, XL6, FRONX, S Cross, Grand Vitara, Dzire, SX4, Zen Estilo, S PRESSO, Ritz, Wagon R Stingray, Alto K10, A Star, Celerio X, Invicto, Wagon R, OMNI E, 800, JIMNY, Victoris, Zen, Esteem, Omni, Kizashi, Wagon R Duo".split(", ")
hyundai_models = "Creta, Grand i10, i10, Eon, Elite i20, Verna, Venue, i20, Grand i10 Nios, i20 Active, Xcent, Santa Fe, Venue N Line, New Santro, Santro Xing, Accent, New i20, New Elantra, Kona Electric, Xcent Prime, Getz Prime, Grand i10 Prime, Getz, Tucson, Aura, Sonata, New i20 N Line, Ioniq 5, Creta N Line, Alcazar, Creta Electric, Exter".split(", ")
tata_models = "Tiago, Nexon, Altroz, Tigor, Punch, Harrier, Hexa, Indica Vista, Indigo ECS, Indigo CS, Manza, Safari, Tiago NRG, Zest, Tiago JTP, Nano, Indica, Sumo, Aria, Bolt, Safari Storme, Harrier EV, Nexon EV, Tigor EV, Punch EV, Curvv, Curvv EV".split(", ")
honda_models = "Amaze, City, WR-V, Brio, Jazz, BR-V, Elevate, Accord, Civic, CR-V, Mobilio".split(", ")

models_dict = {
    "Maruti Suzuki": maruti_models,
    "Hyundai": hyundai_models,
    "Tata": tata_models,
    "Honda": honda_models
}

file_path = "buy-cars.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

for make, models in models_dict.items():
    models = sorted(models)
    
    replacement = ""
    for model in models:
        replacement += f'''
                <div class="checkbox-item">
                  <input type="checkbox" class="model-cb" value="{model}" onchange="applyFilters()">
                  <label>{model}</label>
                </div>'''

    # Match the tree-parent, tree-children start, then any content, then the 3 closing divs
    # We replace with group 1 + replacement + group 3.
    pattern = re.compile(rf'(<input type="checkbox" class="make-cb" value="{make}".*?onclick="event\.stopPropagation\(\)".*?>\s*<label>{make}</label>\s*</div>\s*<span class="tree-toggle">\+</span>\s*</div>\s*<div class="tree-children">\s*)(.*?)\s*(</div>\s*</div>\s*<div class="tree-node">|</div>\s*</div>\s*</div>)', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub(rf'\g<1>{replacement}\n                \g<3>', content)
    else:
        print(f"Could not find pattern for {make}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated buy-cars.html correctly!")

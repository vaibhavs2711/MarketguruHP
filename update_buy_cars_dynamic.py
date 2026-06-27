import re

file_path = "buy-cars.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Empty the static HTML of `.tree-list.scrollable-list`
pattern_tree = re.compile(r'(<div class="tree-list scrollable-list">).*?(</div>\s*</div>\s*</div>\s*<div class="accordion-item">)', re.DOTALL)
content = pattern_tree.sub(r'\1\n              <div id="dynamic-tree-list" style="padding: 10px; font-size: 13px; color: #888;">Loading...</div>\n            \2', content)

# Inject JS for dynamic tree list
js_injection = """
// Dynamic Automotive Tree Rendering
document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/car-hierarchy')
    .then(r => r.json())
    .then(makes => {
      const treeContainer = document.getElementById('dynamic-tree-list');
      if (!treeContainer) return;
      treeContainer.innerHTML = '';
      
      makes.forEach(make => {
        if (!make.models || make.models.length === 0) return; // Skip empty makes
        
        const node = document.createElement('div');
        node.className = 'tree-node';
        
        const fileMap = {
          'marutisuzuki': 'marutisuzuki.png',
          'hyundai': 'hyundai.png',
          'tata': 'tata.png',
          'mahindra': 'mahindra.webp',
          'honda': 'honda.png',
          'toyota': 'toyota.png',
          'kia': 'Kia.png',
          'mg': 'MG.png',
          'renault': 'renault.png',
          'skoda': 'skoda.png',
          'volkswagen': 'volkswagon.png',
          'ford': 'fird.png',
          'nissan': 'Nissan.png',
          'jeep': 'Jeep.png',
          'citroen': 'citroen.png',
          'byd': 'BYD.png',
          'forcemotors': 'forcemotors.jpg',
          'bmw': 'bmw.png',
          'mercedesbenz': 'mercedes-benz.png',
          'audi': 'audi.png',
          'volvo': 'volvo.png',
          'jaguar': 'jaguar.png',
          'landrover': 'Landrover.png',
          'lexus': 'lexus.png',
          'mini': 'minicooper.png',
          'porsche': 'Porsche.png',
          'astonmartin': 'astonmartin.png',
          'ferrari': 'ferrari.png',
          'lamborghini': 'lamborghini.png',
          'bentley': 'bentley.png',
          'rollsroyce': 'rolls-royce.png',
          'maserati': 'maserati.png',
          'mclaren': 'maclaren.png',
          'chevrolet': 'chevrolet.png',
          'fiat': 'fiat.png',
          'datsun': 'datsun.png',
          'mitsubishi': 'Mitsubishi.png',
          'hindustanmotors': 'hindustanmotors.webp',
          'isuzu': 'isuzu.png'
        };

        const brandStr = make.name.toLowerCase().replace(/[\s-]/g, '');
        const fileName = fileMap[brandStr];
        let imgHtml = `<span style="font-size:16px; margin-right:6px;">🚙</span>`;
        if (fileName) {
          imgHtml = `<img src="logo_images/${fileName}" alt="${make.name}" style="width:20px;height:20px;object-fit:contain;margin-right:6px;" onerror="this.outerHTML='<span style=\\'font-size:16px; margin-right:6px;\\'>🚙</span>'">`;
        }

        const parentHtml = `
          <div class="tree-parent" onclick="toggleTree(this)">
            <div class="tree-parent-left">
              <input type="checkbox" class="make-cb" value="${make.name}" onchange="applyFilters()" onclick="event.stopPropagation()">
              ${imgHtml}
              <label>${make.name}</label>
            </div>
            <span class="tree-toggle">+</span>
          </div>
        `;
        
        let childrenHtml = '<div class="tree-children">';
        make.models.forEach(model => {
          childrenHtml += `
            <div class="checkbox-item">
              <input type="checkbox" class="model-cb" value="${model.name}" onchange="applyFilters()">
              <label>${model.name}</label>
            </div>
          `;
        });
        childrenHtml += '</div>';
        
        node.innerHTML = parentHtml + childrenHtml;
        treeContainer.appendChild(node);
      });
      
      // Call setFiltersFromUrl to apply URL parameters to newly created DOM elements
      if (typeof setFiltersFromUrl === 'function') {
         setTimeout(setFiltersFromUrl, 50);
      }
    })
    .catch(e => {
      console.error("Error loading hierarchy:", e);
      const tc = document.getElementById('dynamic-tree-list');
      if(tc) tc.innerHTML = 'Error loading filters.';
    });
});
"""

# Insert JS before </script>
pattern_script = re.compile(r'(</script>\s*</body>)', re.DOTALL)
content = pattern_script.sub(lambda m: "\n" + js_injection + m.group(1), content)

# Note: we need to replace `function applyFilters()` logic if it relies on DOM structure, but it usually uses `.make-cb` and `.model-cb` selectors.
# Let's check if the URL parsing is inside `DOMContentLoaded`.
# If `buy-cars.html` sets filters from URL on DOMContentLoaded, we need to call it AFTER API is loaded. I did `setTimeout(setFiltersFromUrl, 50);`.

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("buy-cars.html updated for dynamic filters!")

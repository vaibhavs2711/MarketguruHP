import re

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace hardcoded options in the select tags
pattern_brand_select = re.compile(r'(<select\s+id="brandSelect".*?>|<select\s+onchange="filterModel\(this\)".*?>)\s*<option value="">All Brands</option>.*?</select>', re.DOTALL)
content = pattern_brand_select.sub(r'<select id="brandSelect" onchange="filterModel(this)">\n                  <option value="">All Brands</option>\n                </select>', content)

js_replacement = """
// Dynamic Automotive API Fetching
document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/car-makes')
    .then(r => r.json())
    .then(makes => {
      const brandSel = document.getElementById('brandSelect');
      if (!brandSel) return;
      makes.forEach(m => {
        const o = document.createElement('option');
        o.value = m.id;
        o.textContent = m.name;
        brandSel.appendChild(o);
      });
    })
    .catch(e => console.error("Error loading makes:", e));
});

function filterModel(sel) {
  const makeId = sel.value;
  const m = document.getElementById('modelSelect');
  m.innerHTML = '<option value="">All Models</option>';
  m.disabled = true;
  
  if (!makeId) {
      m.disabled = false;
      return;
  }
  
  m.innerHTML = '<option value="">Loading...</option>';
  fetch('/api/car-models?makeId=' + makeId)
    .then(r => r.json())
    .then(models => {
      m.innerHTML = '<option value="">All Models</option>';
      m.disabled = false;
      models.forEach(v => {
        const o = document.createElement('option');
        o.value = v.id;
        o.textContent = v.name;
        m.appendChild(o);
      });
    })
    .catch(e => {
      console.error("Error loading models:", e);
      m.innerHTML = '<option value="">Error Loading</option>';
    });
}
"""

# Find `const models = {...};` and `function filterModel(sel) { ... }`
pattern_js = re.compile(r'const models = \{.*?\};\s*function filterModel\(sel\) \{.*?\n    \}', re.DOTALL)
if pattern_js.search(content):
    content = pattern_js.sub(js_replacement, content)
else:
    print("Could not find JS pattern in index.html")

# In searchCars(), brand and model should be sent as text for search query (or ID if we update search, but buy-cars.html expects string usually?)
# Let's check how searchCars passes params.
pattern_search = re.compile(r'const brand = brandSel \? brandSel\.value : \'\';\n\s*const model = document\.getElementById\(\'modelSelect\'\)\.value;')
search_repl = """const brand = brandSel && brandSel.value ? brandSel.options[brandSel.selectedIndex].text : '';
      const modelSel = document.getElementById('modelSelect');
      const model = modelSel && modelSel.value ? modelSel.options[modelSel.selectedIndex].text : '';"""
content = pattern_search.sub(search_repl, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("index.html updated successfully!")

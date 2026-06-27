import re

file_path = "buy-cars.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# I need to insert a </div> right before the Budget accordion-item
pattern = re.compile(r'(<div id="dynamic-tree-list".*?</div>\s*</div>\s*</div>\s*</div>\s*)<div class="accordion-item">\s*<div class="accordion-header".*?<span>Budget</span>', re.DOTALL)
if pattern.search(content):
    pass
else:
    pattern2 = re.compile(r'(<div id="dynamic-tree-list".*?</div>\s*</div>\s*</div>\s*)<div class="accordion-item">\s*<div class="accordion-header".*?<span>Budget</span>', re.DOTALL)
    if pattern2.search(content):
        content = pattern2.sub(r'\1  </div>\n      <div class="accordion-item">\n        <div class="accordion-header" onclick="toggleAccordion(this)">\n          <span>Budget</span>', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed buy-cars.html closing tags.")

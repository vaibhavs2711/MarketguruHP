import re

with open('sell.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Currently step 6 is City, but we also have an 'else if (stepNum === 8)' which was originally step 6 (Photos) and another 'else if (stepNum === 8)' which was originally step 7 (Details).
# Let's fix the numbering.

# First, find the first 'else if (stepNum === 8) {' which is followed by 'inp.innerHTML = `\\n      <div style="margin-bottom:24px;">\\n        <h2 style="font-size:20px;font-weight:800;'
photos_block_start = "else if (stepNum === 8) {\\n    const inp = document.getElementById('input-container');\\n    inp.style.display = 'block';\\n    \\n    inp.innerHTML = `\\n      <div style=\"margin-bottom:24px;\">\\n        <h2 style=\"font-size:20px;font-weight:800;color:var(--charcoal);margin-bottom:8px;\">Upload photos</h2>"

fixed_photos = photos_block_start.replace("else if (stepNum === 8)", "else if (stepNum === 7)")

html = html.replace(photos_block_start, fixed_photos)

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed stepNum for Photos")

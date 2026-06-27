import re

with open('car-detail.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clear static thumbnails, replace with empty container having an id
html = html.replace('<div class="thumb-row">', '<div class="thumb-row" id="galleryThumbs">')
static_thumbs = """        <div class="thumb active" onclick="selectThumb(this,'🚗')">🚗</div>
        <div class="thumb" onclick="selectThumb(this,'🪟')">🪟</div>
        <div class="thumb" onclick="selectThumb(this,'🛞')">🛞</div>
        <div class="thumb" onclick="selectThumb(this,'🪑')">🪑</div>
        <div class="thumb" onclick="selectThumb(this,'⚙️')">⚙️</div>
        <div class="thumb" onclick="selectThumb(this,'📋')">📋</div>"""
html = html.replace(static_thumbs, "")

# 2. Update renderCarDetails to populate galleryThumbs dynamically
old_img_handling = """  // Gallery Image / Emoji handling
  const mainImg = document.getElementById('mainImg');
  const emojiEl = document.getElementById('galleryEmoji');
  const thumbs = document.querySelectorAll('.thumb');
  
  // Remove any previously added uploaded-car-image to avoid duplicates
  const existingImg = mainImg.querySelector('img.uploaded-car-image');
  if (existingImg) {
    existingImg.remove();
  }

  if (currentCar.image) {
    // Create an img element
    const imgEl = document.createElement('img');
    imgEl.src = currentCar.image;
    imgEl.className = 'uploaded-car-image';
    imgEl.style.width = '100%';
    imgEl.style.height = '100%';
    imgEl.style.objectFit = 'cover';
    imgEl.style.position = 'absolute';
    imgEl.style.top = '0';
    imgEl.style.left = '0';
    imgEl.style.zIndex = '1';
    
    // Insert imgEl as the first child of mainImg (so badges stay on top of it)
    mainImg.insertBefore(imgEl, mainImg.firstChild);
    
    // Hide emoji element
    if (emojiEl) emojiEl.style.display = 'none';
    
    // Update first thumbnail to show the custom image
    if (thumbs.length > 0) {
      thumbs[0].innerHTML = `<img src="${currentCar.image}" style="width:100%;height:100%;object-fit:cover;border-radius:4px;" />`;
    }
  } else {
    if (emojiEl) {
      emojiEl.style.display = 'block';
      emojiEl.textContent = currentCar.emoji || '🚗';
    }
    if (thumbs.length > 0) {
      thumbs[0].textContent = currentCar.emoji || '🚗';
    }
  }"""

new_img_handling = """  // Gallery Image / Emoji handling
  const mainImg = document.getElementById('mainImg');
  const emojiEl = document.getElementById('galleryEmoji');
  const thumbsContainer = document.getElementById('galleryThumbs');
  
  // Gather images
  let imagesToDisplay = [];
  if (currentCar.images && Array.isArray(currentCar.images) && currentCar.images.length > 0) {
      imagesToDisplay = currentCar.images;
  } else if (currentCar.image) {
      imagesToDisplay = [currentCar.image];
  }

  // Generate Thumbnails
  thumbsContainer.innerHTML = '';
  if (imagesToDisplay.length > 0) {
      imagesToDisplay.forEach((imgSrc, idx) => {
          const thumb = document.createElement('div');
          thumb.className = idx === 0 ? 'thumb active' : 'thumb';
          thumb.innerHTML = `<img src="${imgSrc}" style="width:100%;height:100%;object-fit:cover;border-radius:4px;" />`;
          thumb.onclick = () => selectThumb(thumb, null, imgSrc, idx);
          thumbsContainer.appendChild(thumb);
      });
  } else {
      // Fallback emojis
      const emojis = [currentCar.emoji || '🚗', '🪟', '🛞', '🪑', '⚙️', '📋'];
      emojis.forEach((em, idx) => {
          const thumb = document.createElement('div');
          thumb.className = idx === 0 ? 'thumb active' : 'thumb';
          thumb.textContent = em;
          thumb.onclick = () => selectThumb(thumb, em, null, idx);
          thumbsContainer.appendChild(thumb);
      });
  }
  
  // Set main image initially
  if (imagesToDisplay.length > 0) {
      setMainImage(imagesToDisplay[0]);
      if (emojiEl) emojiEl.style.display = 'none';
  } else {
      setMainImage(null);
      if (emojiEl) {
          emojiEl.style.display = 'block';
          emojiEl.textContent = currentCar.emoji || '🚗';
      }
  }"""
html = html.replace(old_img_handling, new_img_handling)

# 3. Add setMainImage and fix selectThumb
old_select_thumb = """function selectThumb(el, emoji) {
  document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  
  // Toggle overlay insights: only show for the first main image thumbnail
  const thumbs = Array.from(document.querySelectorAll('.thumb'));
  const idx = thumbs.indexOf(el);
  const insights = document.getElementById('galleryInsights');
  
  const mainImg = document.getElementById('mainImg');
  const mainImageEl = mainImg.querySelector('img.uploaded-car-image');
  const emojiEl = document.getElementById('galleryEmoji');
  
  if (idx === 0 && currentCar && currentCar.image) {
    if (mainImageEl) mainImageEl.style.display = 'block';
    if (emojiEl) {
      if (emojiEl) emojiEl.style.display = 'none';
    }
  } else {
    if (mainImageEl) mainImageEl.style.display = 'none';
    if (emojiEl) {
      emojiEl.style.display = 'block';
      emojiEl.textContent = emoji;
    }
  }
}"""

new_select_thumb = """function setMainImage(imgSrc) {
  const mainImg = document.getElementById('mainImg');
  const existingImg = mainImg.querySelector('img.uploaded-car-image');
  if (existingImg) {
      if (imgSrc) {
          existingImg.src = imgSrc;
          existingImg.style.display = 'block';
      } else {
          existingImg.remove();
      }
  } else if (imgSrc) {
      const imgEl = document.createElement('img');
      imgEl.src = imgSrc;
      imgEl.className = 'uploaded-car-image';
      imgEl.style.width = '100%';
      imgEl.style.height = '100%';
      imgEl.style.objectFit = 'cover';
      imgEl.style.position = 'absolute';
      imgEl.style.top = '0';
      imgEl.style.left = '0';
      imgEl.style.zIndex = '1';
      mainImg.insertBefore(imgEl, mainImg.firstChild);
  }
}

function selectThumb(el, emoji, imgSrc, idx) {
  document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  
  const emojiEl = document.getElementById('galleryEmoji');
  
  if (imgSrc) {
      setMainImage(imgSrc);
      if (emojiEl) emojiEl.style.display = 'none';
  } else {
      setMainImage(null);
      if (emojiEl) {
          emojiEl.style.display = 'block';
          emojiEl.textContent = emoji || '🚗';
      }
  }
}"""
html = html.replace(old_select_thumb, new_select_thumb)

# Update scroll thumb-row for 15 items
html = html.replace('.thumb-row{display:flex;gap:12px;padding:12px;}', '.thumb-row{display:flex;gap:12px;padding:12px;overflow-x:auto;scrollbar-width:none;} .thumb-row::-webkit-scrollbar { display: none; } .thumb{flex-shrink:0;}')

with open('car-detail.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated car-detail.html")

import re

with open('car-detail.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS for navigation buttons
css_nav = """  /* GALLERY NAVIGATION BUTTONS */
  .img-nav-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0, 0, 0, 0.4);
    color: white;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    border-radius: 50%;
    cursor: pointer;
    z-index: 20;
    transition: background 0.2s, transform 0.2s;
    user-select: none;
  }
  .img-nav-btn:hover {
    background: rgba(0, 0, 0, 0.7);
    transform: translateY(-50%) scale(1.1);
  }
  .img-nav-btn.prev {
    left: 16px;
  }
  .img-nav-btn.next {
    right: 350px; /* Offset to avoid price insights card */
  }
  @media (max-width: 800px) {
    .img-nav-btn.next {
      right: 16px;
    }
  }
"""
html = html.replace('/* TABS SYSTEM */', css_nav + '\n  /* TABS SYSTEM */')

# Add the navigation buttons to mainImg
main_img_old = """        <div class="main-img" id="mainImg" style="width: 100%;">
          <span class="gallery-car-emoji" id="galleryEmoji">🚗</span>
          <div class="img-badges">
            <span class="img-badge badge-hot">🔥 Hot Deal</span>
          </div>
        </div>"""
main_img_new = """        <div class="main-img" id="mainImg" style="width: 100%;">
          <div class="img-nav-btn prev" id="imgPrevBtn" style="display:none;" onclick="prevImage(event)">❮</div>
          <div class="img-nav-btn next" id="imgNextBtn" style="display:none;" onclick="nextImage(event)">❯</div>
          <span class="gallery-car-emoji" id="galleryEmoji">🚗</span>
          <div class="img-badges">
            <span class="img-badge badge-hot">🔥 Hot Deal</span>
          </div>
        </div>"""
html = html.replace(main_img_old, main_img_new)

# Update the JS logic to handle images array and navigation
js_old = """  // Gather images
  let imagesToDisplay = [];
  if (currentCar.images && Array.isArray(currentCar.images) && currentCar.images.length > 0) {
      imagesToDisplay = currentCar.images;
  } else if (currentCar.image) {
      imagesToDisplay = [currentCar.image];
  }"""
js_new = """  // Gather images
  window.galleryImages = [];
  window.currentImageIndex = 0;
  if (currentCar.images && Array.isArray(currentCar.images) && currentCar.images.length > 0) {
      window.galleryImages = currentCar.images;
  } else if (currentCar.image) {
      window.galleryImages = [currentCar.image];
  }
  let imagesToDisplay = window.galleryImages;
  
  // Show/hide navigation buttons
  const prevBtn = document.getElementById('imgPrevBtn');
  const nextBtn = document.getElementById('imgNextBtn');
  if (imagesToDisplay.length > 1) {
      if(prevBtn) prevBtn.style.display = 'flex';
      if(nextBtn) nextBtn.style.display = 'flex';
  } else {
      if(prevBtn) prevBtn.style.display = 'none';
      if(nextBtn) nextBtn.style.display = 'none';
  }"""
html = html.replace(js_old, js_new)

js_funcs = """function selectThumb(el, emoji, imgSrc, idx) {
  document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  
  const emojiEl = document.getElementById('galleryEmoji');
  window.currentImageIndex = idx || 0;
  
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
}

function nextImage(e) {
    if(e) e.stopPropagation();
    if (!window.galleryImages || window.galleryImages.length <= 1) return;
    window.currentImageIndex = (window.currentImageIndex + 1) % window.galleryImages.length;
    const nextImgSrc = window.galleryImages[window.currentImageIndex];
    const thumbEls = document.querySelectorAll('.thumb');
    const targetThumb = thumbEls[window.currentImageIndex] || null;
    selectThumb(targetThumb, null, nextImgSrc, window.currentImageIndex);
}

function prevImage(e) {
    if(e) e.stopPropagation();
    if (!window.galleryImages || window.galleryImages.length <= 1) return;
    window.currentImageIndex = (window.currentImageIndex - 1 + window.galleryImages.length) % window.galleryImages.length;
    const prevImgSrc = window.galleryImages[window.currentImageIndex];
    const thumbEls = document.querySelectorAll('.thumb');
    const targetThumb = thumbEls[window.currentImageIndex] || null;
    selectThumb(targetThumb, null, prevImgSrc, window.currentImageIndex);
}"""

# Replace selectThumb
html = re.sub(r'function selectThumb\(el, emoji, imgSrc, idx\) \{.*?\n\}', js_funcs, html, flags=re.DOTALL)

with open('car-detail.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated car-detail.html")

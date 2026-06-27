import re

with open('sell.html', 'r', encoding='utf-8') as f:
    sell_html = f.read()

# 1. Update STEPS array
old_steps = """const STEPS = [
  { id: 1, label: 'Brand', title: 'Select brand' },
  { id: 2, label: 'Model', title: 'Select model' },
  { id: 3, label: 'Year', title: 'Select year' },
  { id: 4, label: 'Variant', title: 'Select variant & fuel' },
  { id: 5, label: 'State', title: 'Select city' },
  { id: 6, label: 'Details', title: 'Final Details' }
];"""
new_steps = """const STEPS = [
  { id: 1, label: 'Brand', title: 'Select brand' },
  { id: 2, label: 'Model', title: 'Select model' },
  { id: 3, label: 'Year', title: 'Select year' },
  { id: 4, label: 'Variant', title: 'Select variant & fuel' },
  { id: 5, label: 'State', title: 'Select city' },
  { id: 6, label: 'Photos', title: 'Upload photos' },
  { id: 7, label: 'Details', title: 'Final Details' }
];"""
sell_html = sell_html.replace(old_steps, new_steps)

# 2. Update goToStep logic
old_go_to_step = """function goToStep(num) {
  // Prevent jumping forward if previous steps are incomplete
  if (num > 1 && !sellData.brandId) return;
  if (num > 2 && !sellData.modelId) return;
  if (num > 3 && !sellData.year) return;
  if (num > 4 && !sellData.fuel) return;
  if (num > 5 && !sellData.city) return;"""
new_go_to_step = """function goToStep(num) {
  // Prevent jumping forward if previous steps are incomplete
  if (num > 1 && !sellData.brandId) return;
  if (num > 2 && !sellData.modelId) return;
  if (num > 3 && !sellData.year) return;
  if (num > 4 && !sellData.fuel) return;
  if (num > 5 && !sellData.city) return;
  if (num > 6 && !sellData.photosUploaded) return;"""
sell_html = sell_html.replace(old_go_to_step, new_go_to_step)

# Reset logic
old_reset = """  if(num <= 1) sellData.brand = sellData.brandId = null;
  if(num <= 2) sellData.model = sellData.modelId = null;
  if(num <= 3) sellData.year = null;
  if(num <= 4) sellData.fuel = sellData.trans = null;
  if(num <= 5) sellData.city = null;"""
new_reset = """  if(num <= 1) sellData.brand = sellData.brandId = null;
  if(num <= 2) sellData.model = sellData.modelId = null;
  if(num <= 3) sellData.year = null;
  if(num <= 4) sellData.fuel = sellData.trans = null;
  if(num <= 5) sellData.city = null;
  if(num <= 6) sellData.photosUploaded = false;"""
sell_html = sell_html.replace(old_reset, new_reset)


# 3. Update loadStep to handle step 6 (Photos) and step 7 (Details)
old_load_step_6 = """  else if (stepNum === 6) {
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    inp.innerHTML = `
      <input type="number" id="inp-km" class="input-field" placeholder="KMs Driven (e.g. 45000)" required>
      <input type="number" step="0.1" id="inp-price" class="input-field" placeholder="Expected Price in Lakhs (e.g. 5.5)" required>
      <input type="tel" id="inp-mob" class="input-field" placeholder="Your Mobile Number" required>
    `;
    const btn = document.getElementById('btn-continue');
    btn.style.display = 'flex';
    btn.disabled = false;
    btn.innerHTML = 'SUBMIT LISTING 🚀';
    
    // Auto fill mobile if logged in
    const m = localStorage.getItem('mg_current_user_mobile');
    if(m) document.getElementById('inp-mob').value = m;
  }"""

new_load_step_6 = """  else if (stepNum === 6) {
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    inp.innerHTML = `
      <label style="display:block;margin-bottom:12px;font-size:14px;font-weight:600;color:var(--charcoal);">Upload Car Photos</label>
      <input type="file" id="inp-photos" class="input-field" multiple accept="image/*" style="padding:10px; background:#fafafb; border:2px dashed var(--border);" onchange="sellData.photosUploaded = true; document.getElementById('btn-continue').disabled = false;">
      <p style="font-size:12px;color:var(--muted);margin-top:-16px;margin-bottom:24px;">Upload up to 5 photos (Front, Back, Interior, etc.)</p>
    `;
    const btn = document.getElementById('btn-continue');
    btn.style.display = 'flex';
    btn.disabled = true; // Wait for upload
    btn.innerHTML = 'CONTINUE <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
  }
  else if (stepNum === 7) {
    const inp = document.getElementById('input-container');
    inp.style.display = 'block';
    inp.innerHTML = `
      <input type="number" id="inp-km" class="input-field" placeholder="KMs Driven (e.g. 45000)" required>
      <input type="number" step="0.1" id="inp-price" class="input-field" placeholder="Expected Price in Lakhs (e.g. 5.5)" required>
      <input type="tel" id="inp-mob" class="input-field" placeholder="Your Mobile Number" required>
    `;
    const btn = document.getElementById('btn-continue');
    btn.style.display = 'flex';
    btn.disabled = false;
    btn.innerHTML = 'SUBMIT LISTING 🚀';
    
    // Auto fill mobile if logged in
    const m = localStorage.getItem('mg_current_user_mobile');
    if(m) document.getElementById('inp-mob').value = m;
  }"""
sell_html = sell_html.replace(old_load_step_6, new_load_step_6)

# 4. Update nextStep
old_next_step = """function nextStep() {
  if (currentStep === 6) {
    submitListing();
    return;
  }
  currentStep++;
  renderStepper();
  loadStep(currentStep);
}"""
new_next_step = """function nextStep() {
  if (currentStep === 7) {
    submitListing();
    return;
  }
  currentStep++;
  renderStepper();
  loadStep(currentStep);
}"""
sell_html = sell_html.replace(old_next_step, new_next_step)

with open('sell.html', 'w', encoding='utf-8') as f:
    f.write(sell_html)

print("Added step 6 for Photos.")

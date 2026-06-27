import re

def update_sell():
    with open('sell.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update STEPS
    old_steps = """    const STEPS = [
      { id: 1, label: 'Brand', title: 'Select brand' },
      { id: 2, label: 'Model', title: 'Select model' },
      { id: 3, label: 'Year', title: 'Select year' },
      { id: 4, label: 'Variant', title: 'Select variant & fuel' },
      { id: 5, label: 'State', title: 'Select city' },
      { id: 6, label: 'Photos', title: 'Upload photos' },
      { id: 7, label: 'Details', title: 'Final Details' }
    ];"""
    new_steps = """    const STEPS = [
      { id: 1, label: 'Brand', title: 'Select brand' },
      { id: 2, label: 'Model', title: 'Select model' },
      { id: 3, label: 'Variant', title: 'Select variant' },
      { id: 4, label: 'Year', title: 'Select year' },
      { id: 5, label: 'Specs', title: 'Select trans & fuel' },
      { id: 6, label: 'State', title: 'Select city' },
      { id: 7, label: 'Photos', title: 'Upload photos' },
      { id: 8, label: 'Details', title: 'Final Details' }
    ];"""
    content = content.replace(old_steps, new_steps)

    # 2. Update sellData init
    content = content.replace(
        "let sellData = { brandId: null, brand: null, modelId: null, model: null, year: null, fuel: null, trans: null, city: null, kms: null, ask: null, mobile: null };",
        "let sellData = { brandId: null, brand: null, modelId: null, model: null, variant: null, year: null, fuel: null, trans: null, city: null, kms: null, ask: null, mobile: null };"
    )

    # 3. Breadcrumbs
    old_breadcrumbs = """      if (sellData.brand) bHTML += `<div class="bc-pill">${sellData.brand} <span onclick="goToStep(1)">×</span></div>`;
      if (sellData.model) bHTML += `<div class="bc-pill">${sellData.model} <span onclick="goToStep(2)">×</span></div>`;
      if (sellData.year) bHTML += `<div class="bc-pill">${sellData.year} <span onclick="goToStep(3)">×</span></div>`;
      if (sellData.fuel) bHTML += `<div class="bc-pill">${sellData.fuel} ${sellData.trans || ''} <span onclick="goToStep(4)">×</span></div>`;
      if (sellData.city) bHTML += `<div class="bc-pill">${sellData.city} <span onclick="goToStep(5)">×</span></div>`;"""
    new_breadcrumbs = """      if (sellData.brand) bHTML += `<div class="bc-pill">${sellData.brand} <span onclick="goToStep(1)">×</span></div>`;
      if (sellData.model) bHTML += `<div class="bc-pill">${sellData.model} <span onclick="goToStep(2)">×</span></div>`;
      if (sellData.variant) bHTML += `<div class="bc-pill">${sellData.variant} <span onclick="goToStep(3)">×</span></div>`;
      if (sellData.year) bHTML += `<div class="bc-pill">${sellData.year} <span onclick="goToStep(4)">×</span></div>`;
      if (sellData.fuel) bHTML += `<div class="bc-pill">${sellData.fuel} ${sellData.trans || ''} <span onclick="goToStep(5)">×</span></div>`;
      if (sellData.city) bHTML += `<div class="bc-pill">${sellData.city} <span onclick="goToStep(6)">×</span></div>`;"""
    content = content.replace(old_breadcrumbs, new_breadcrumbs)

    # 3.1. Sidebar Indicators
    content = content.replace(
        """      document.getElementById('v2').classList.toggle('pending', currentStep < 2);
      document.getElementById('v3').classList.toggle('pending', currentStep < 4);
      document.getElementById('v4').classList.toggle('pending', currentStep < 5);
      document.getElementById('v5').classList.toggle('pending', currentStep < 7);""",
        """      document.getElementById('v2').classList.toggle('pending', currentStep < 2);
      document.getElementById('v3').classList.toggle('pending', currentStep < 5);
      document.getElementById('v4').classList.toggle('pending', currentStep < 6);
      document.getElementById('v5').classList.toggle('pending', currentStep < 8);"""
    )

    # 4. goToStep
    old_goto = """      if (num > 1 && !sellData.brandId) return;
      if (num > 2 && !sellData.modelId) return;
      if (num > 3 && !sellData.year) return;
      if (num > 4 && !sellData.fuel) return;
      if (num > 5 && !sellData.city) return;
      if (num > 6 && !sellData.photosUploaded) return;

      currentStep = num;
      // Reset future data
      if (num <= 1) sellData.brand = sellData.brandId = null;
      if (num <= 2) sellData.model = sellData.modelId = null;
      if (num <= 3) sellData.year = null;
      if (num <= 4) sellData.fuel = sellData.trans = null;
      if (num <= 5) sellData.city = null;
      if (num <= 6) { sellData.photosUploaded = false; uploadedPhotos = []; }"""
    new_goto = """      if (num > 1 && !sellData.brandId) return;
      if (num > 2 && !sellData.modelId) return;
      if (num > 3 && !sellData.variant) return;
      if (num > 4 && !sellData.year) return;
      if (num > 5 && !sellData.fuel) return;
      if (num > 6 && !sellData.city) return;
      if (num > 7 && !sellData.photosUploaded) return;

      currentStep = num;
      // Reset future data
      if (num <= 1) sellData.brand = sellData.brandId = null;
      if (num <= 2) sellData.model = sellData.modelId = null;
      if (num <= 3) sellData.variant = null;
      if (num <= 4) sellData.year = null;
      if (num <= 5) sellData.fuel = sellData.trans = null;
      if (num <= 6) sellData.city = null;
      if (num <= 7) { sellData.photosUploaded = false; uploadedPhotos = []; }"""
    content = content.replace(old_goto, new_goto)

    # 5. loadStep mappings
    content = content.replace("else if (stepNum === 7)", "else if (stepNum === 8)")
    content = content.replace("else if (stepNum === 6)", "else if (stepNum === 7)")
    content = content.replace("else if (stepNum === 5)", "else if (stepNum === 6)")
    content = content.replace("else if (stepNum === 4)", "else if (stepNum === 5)")
    content = content.replace("else if (stepNum === 3)", "else if (stepNum === 4)")

    # 5.1 Add step 3 (Variant)
    new_step_3 = """      else if (stepNum === 3) {
        document.getElementById('search-box').style.display = 'block';
        document.getElementById('search-input').placeholder = 'Search Variant...';
        const list = document.getElementById('list-container');
        list.style.display = 'block';
        list.innerHTML = '<div style="padding:20px;text-align:center;color:#666;">Loading variants...</div>';

        fetch(API_BASE + '/api/car-variants?modelId=' + sellData.modelId)
          .then(r => r.json())
          .then(data => {
            currentList = data.map(v => ({ id: v, name: v }));
            renderList(currentList, 'variant', 'variant');
          });
      }
      else if (stepNum === 4) {"""
    content = content.replace("else if (stepNum === 4) {", new_step_3)

    # 6. renderList quotes
    content = content.replace(
        """onclick="setSelection('${key}', ${item.id}, '${textKey}', event)""",
        """onclick="setSelection('${key}', '${item.id.toString().replace("'", "\\'")}', '${textKey}', event)\""""
    )

    # 7. filterList updates
    content = content.replace("if (currentStep === 5) {", "if (currentStep === 6) {")
    content = content.replace(
        "const key = currentStep === 1 ? 'brandId' : 'modelId';",
        "const key = currentStep === 1 ? 'brandId' : (currentStep === 2 ? 'modelId' : 'variant');"
    )
    content = content.replace(
        "const textKey = currentStep === 1 ? 'brand' : 'model';",
        "const textKey = currentStep === 1 ? 'brand' : (currentStep === 2 ? 'model' : 'variant');"
    )

    # 8. submitListing next step
    content = content.replace("if (currentStep === 7) {", "if (currentStep === 8) {")
    
    # 9. submitListing payload name
    content = content.replace(
        "name: sellData.brand + ' ' + sellData.model,",
        "name: sellData.brand + ' ' + sellData.model + (sellData.variant ? ' ' + sellData.variant : ''),"
    )

    with open('sell.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("sell.html updated successfully!")

if __name__ == "__main__":
    update_sell()

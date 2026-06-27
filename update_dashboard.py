import re

file_path = "dashboard.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add nav-item
nav_item = """
    <div class="nav-item" onclick="showPage('makesmodels',this)">
      <span class="icon">🏷️</span> Makes & Models
    </div>"""

pattern_nav = re.compile(r'(<div class="nav-section-title">Admin</div>\s*<div class="nav-item" onclick="showPage\(\'users\',this\)">)')
if pattern_nav.search(content):
    content = pattern_nav.sub(r'<div class="nav-section-title">Admin</div>\n    <div class="nav-item" onclick="showPage(\'makesmodels\',this)">\n      <span class="icon">🏷️</span> Makes & Models\n    </div>\n    <div class="nav-item" onclick="showPage(\'users\',this)">', content)

# Add page section
page_section = """
    <!-- ===== MAKES & MODELS PAGE ===== -->
    <div class="page-section" id="pg-makesmodels">
      <div class="grid2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">🏷️ Car Makes</div>
            <button class="btn-sm btn-red-sm" onclick="showAddMakeModal()">+ Add Make</button>
          </div>
          <table id="makesTable">
            <thead>
              <tr><th>Make</th><th>Slug</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
        
        <div class="card">
          <div class="card-header">
            <div class="card-title">🚗 Car Models</div>
            <button class="btn-sm btn-red-sm" onclick="showAddModelModal()">+ Add Model</button>
          </div>
          <table id="modelsTable">
            <thead>
              <tr><th>Model</th><th>Make</th><th>Slug</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>
"""

pattern_page = re.compile(r'(<!-- ===== REPORTS PAGE ===== -->)')
if pattern_page.search(content):
    content = pattern_page.sub(page_section + r'\n    \1', content)

# Add Javascript logic for admin CRUD
js_crud = """
// --- Admin Car Makes & Models ---
let allAdminMakes = [];
let allAdminModels = [];

function loadAdminCarData() {
  fetch('/api/car-hierarchy')
    .then(r => r.json())
    .then(makes => {
      allAdminMakes = makes;
      allAdminModels = makes.flatMap(m => m.models || []);
      renderAdminMakes();
      renderAdminModels();
    });
}

function renderAdminMakes() {
  const tbody = document.querySelector('#makesTable tbody');
  if(!tbody) return;
  tbody.innerHTML = allAdminMakes.map(m => `
    <tr>
      <td>${m.name}</td>
      <td>${m.slug}</td>
      <td><span class="status-badge s-active">Active</span></td>
      <td>
        <button class="btn-sm btn-outline-sm" onclick="editMake(${m.id}, '${m.name}')">Edit</button>
      </td>
    </tr>
  `).join('');
}

function renderAdminModels() {
  const tbody = document.querySelector('#modelsTable tbody');
  if(!tbody) return;
  tbody.innerHTML = allAdminModels.map(m => {
     const make = allAdminMakes.find(mk => mk.id === m.make_id);
     return `
    <tr>
      <td>${m.name}</td>
      <td>${make ? make.name : m.make_id}</td>
      <td>${m.slug}</td>
      <td><span class="status-badge s-active">Active</span></td>
      <td>
        <button class="btn-sm btn-outline-sm" onclick="editModel(${m.id}, ${m.make_id}, '${m.name}')">Edit</button>
      </td>
    </tr>
  `}).join('');
}

function showAddMakeModal() {
   const name = prompt("Enter new Make name:");
   if(name) {
      fetch('/api/admin/car-makes', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ name })
      }).then(r=>r.json()).then(res=>{
         if(res.status==='success') { showToast('✅ Make Added'); loadAdminCarData(); }
      });
   }
}

function editMake(id, oldName) {
   const name = prompt("Edit Make name:", oldName);
   if(name && name !== oldName) {
      fetch('/api/admin/car-makes', {
         method: 'PUT',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ id, name })
      }).then(r=>r.json()).then(res=>{
         if(res.status==='success') { showToast('✅ Make Updated'); loadAdminCarData(); }
      });
   }
}

function showAddModelModal() {
   let makesOptions = allAdminMakes.map(m => `${m.id}: ${m.name}`).join('\\n');
   const makeIdStr = prompt(`Enter Make ID:\\n${makesOptions}`);
   if(!makeIdStr) return;
   const make_id = parseInt(makeIdStr);
   const name = prompt("Enter new Model name:");
   if(name) {
      fetch('/api/admin/car-models', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ make_id, name })
      }).then(r=>r.json()).then(res=>{
         if(res.status==='success') { showToast('✅ Model Added'); loadAdminCarData(); }
      });
   }
}

function editModel(id, make_id, oldName) {
   const name = prompt("Edit Model name:", oldName);
   if(name && name !== oldName) {
      fetch('/api/admin/car-models', {
         method: 'PUT',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ id, make_id, name })
      }).then(r=>r.json()).then(res=>{
         if(res.status==='success') { showToast('✅ Model Updated'); loadAdminCarData(); }
      });
   }
}

document.addEventListener('DOMContentLoaded', loadAdminCarData);
"""

pattern_script = re.compile(r'(</script>\s*</body>)', re.DOTALL)
if pattern_script.search(content):
    content = pattern_script.sub(lambda m: "\n<script>\n" + js_crud + "\n</script>\n" + m.group(1), content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("dashboard.html updated with Makes & Models admin panel!")

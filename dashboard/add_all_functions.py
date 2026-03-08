#!/usr/bin/env python3
"""
Script to add tab functions and sidebar entries for all new modules
"""

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add tab functions
tab_functions = '''
// Finance Tab Switcher
window.finTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('fin-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.finTab = finTab;

// DMS Tab Switcher
window.dmsTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('dms-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.dmsTab = dmsTab;

// BI Tab Switcher
window.biTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('bi-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.biTab = biTab;

'''

# Add after invTab
old_invTab_end = '''window.invTab = invTab;
'''

content = content.replace(old_invTab_end, old_invTab_end + tab_functions)

# Write back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Tab functions added!")

# Now add sidebar entries to index.html
with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    sidebar_content = f.read()

# Add sidebar entries
sidebar_entries = '''
                    <div class="menu-item" data-page="finance2">
                        <div class="nav-icon">💰</div>
                        <div class="nav-label">Finance & Accts</div>
                    </div>
                    <div class="menu-item" data-page="dms">
                        <div class="nav-icon">📁</div>
                        <div class="nav-label">Documents</div>
                    </div>
                    <div class="menu-item" data-page="bi">
                        <div class="nav-icon">📊</div>
                        <div class="nav-label">BI & Analytics</div>
                    </div>'''

# Add after inventory
old_inventory = '''                    <div class="menu-item" data-page="inventory">
                        <div class="nav-icon">📦</div>
                        <div class="nav-label">Inventory</div>
                    </div>'''

sidebar_content = sidebar_content.replace(old_inventory, old_inventory + sidebar_entries)

with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(sidebar_content)

print("Sidebar entries added!")
print("All done!")

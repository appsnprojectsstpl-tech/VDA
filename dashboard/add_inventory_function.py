#!/usr/bin/env python3
"""
Script to add Inventory tab switching function and sidebar entry
"""

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add invTab function after hrmTab function
invTab_function = '''
// Inventory Tab Switcher
window.invTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('inv-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.invTab = invTab;

'''

# Find hrmTab and add after it
old_hrmTab_end = '''window.hrmTab = hrmTab;
'''

content = content.replace(old_hrmTab_end, old_hrmTab_end + invTab_function)

# Write the modified content back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Inventory function added successfully!")

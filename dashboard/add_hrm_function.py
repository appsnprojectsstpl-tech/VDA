#!/usr/bin/env python3
"""
Script to add HRM tab switching function and sidebar entry
"""

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add hrmTab function after crmTab function
hrmTab_function = '''
// HRM Tab Switcher
window.hrmTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('hrm-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.hrmTab = hrmTab;

'''

# Find crmTab and add after it
old_crmTab_end = '''window.crmTab = crmTab;
'''

content = content.replace(old_crmTab_end, old_crmTab_end + hrmTab_function)

# Write the modified content back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("HRM function added successfully!")

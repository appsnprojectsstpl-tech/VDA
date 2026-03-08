#!/usr/bin/env python3
"""
Script to add HRM sidebar navigation entry
"""

# Read the index.html file
with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add HRM menu item after CRM
hrm_menu = '''                    <div class="menu-item" data-page="hrm">
                        <div class="nav-icon">👥</div>
                        <span class="nav-label">HRM & Payroll</span>
                    </div>'''

# Find CRM menu item and add HRM after it
old_crm = '''                    <div class="menu-item" data-page="crm">
                        <div class="nav-icon">🤝</div>
                        <span class="nav-label">CRM & Contracts</span>
                    </div>'''

content = content.replace(old_crm, old_crm + '\n' + hrm_menu)

# Write the modified content back
with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HRM sidebar entry added successfully!")

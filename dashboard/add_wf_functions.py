#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add workflow and ticketing functions
"""
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add functions
old_bi = "window.biTab = biTab;"
new_funcs = """window.biTab = biTab;

// Workflow Tab Switcher
window.wfTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('wf-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.wfTab = wfTab;

// Ticketing Tab Switcher
window.ticketTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('ticket-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.ticketTab = ticketTab;
"""

content = content.replace(old_bi, new_funcs)

with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Functions added!")

# Add sidebar
with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    sidebar = f.read()

old_bi_sidebar = '''                    <div class="menu-item" data-page="bi">
                        <div class="nav-icon">📊</div>
                        <div class="nav-label">BI & Analytics</div>
                    </div>'''

new_sidebar = '''                    <div class="menu-item" data-page="bi">
                        <div class="nav-icon">📊</div>
                        <div class="nav-label">BI & Analytics</div>
                    </div>
                    <div class="menu-item" data-page="workflow">
                        <div class="nav-icon">✅</div>
                        <div class="nav-label">Workflow</div>
                    </div>
                    <div class="menu-item" data-page="ticketing">
                        <div class="nav-icon">🎫</div>
                        <div class="nav-label">Helpdesk</div>
                    </div>'''

sidebar = sidebar.replace(old_bi_sidebar, new_sidebar)

with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(sidebar)

print("Sidebar added!")
print("Done!")

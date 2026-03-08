#!/usr/bin/env python3
"""
Add Sidebar Navigation & Tab Functions for Tier 3 Modules
"""

def add_sidebar_and_functions():
    with open('dashboard/app.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add sidebar entries (find where other nav items are and add after ticketing)
    sidebar_entries = '''
        <li class="nav-item" data-page="booking" onclick="showPage('booking')">
            <span class="nav-icon">📅</span>
            <span class="nav-text">Booking</span>
        </li>
        <li class="nav-item" data-page="lms" onclick="showPage('lms')">
            <span class="nav-icon">🎓</span>
            <span class="nav-text">Learning</span>
        </li>
        <li class="nav-item" data-page="fieldservice" onclick="showPage('fieldservice')">
            <span class="nav-icon">🚜</span>
            <span class="nav-text">Field Service</span>
        </li>
        <li class="nav-item" data-page="farmerportal" onclick="showPage('farmerportal')">
            <span class="nav-icon">👨‍🌾</span>
            <span class="nav-text">Farmer Portal</span>
        </li>
        <li class="nav-item" data-page="survey" onclick="showPage('survey')">
            <span class="nav-icon">📋</span>
            <span class="nav-text">Surveys</span>
        </li>
        <li class="nav-item" data-page="schemes" onclick="showPage('schemes')">
            <span class="nav-icon">🏛️</span>
            <span class="nav-text">Schemes</span>
        </li>'''
    
    # Add sidebar entries after ticketing nav item
    if 'data-page="ticketing"' in content:
        insert_pos = content.find('data-page="ticketing"')
        # Find end of this nav item
        end_pos = content.find('</li>', insert_pos) + 5
        content = content[:end_pos] + '\n' + sidebar_entries + content[end_pos:]
        print("Added sidebar entries")
    
    # Add tab switching functions
    tab_functions = '''
// ============================================
// TIER 3 TAB FUNCTIONS
// ============================================

// Booking Tab Switching
window.bookingTab = function(id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('#booking-page .crm-tab-content').forEach(function(e) { e.classList.remove('active'); });
    container.querySelectorAll('#booking-page .crm-tab-btn').forEach(function(e) { e.classList.remove('active'); });
    var target = document.getElementById('booking-' + id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};

// LMS Tab Switching
window.lmsTab = function(id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('#lms-page .crm-tab-content').forEach(function(e) { e.classList.remove('active'); });
    container.querySelectorAll('#lms-page .crm-tab-btn').forEach(function(e) { e.classList.remove('active'); });
    var target = document.getElementById('lms-' + id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};

// Field Service Tab Switching
window.fsTab = function(id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('#fieldservice-page .crm-tab-content').forEach(function(e) { e.classList.remove('active'); });
    container.querySelectorAll('#fieldservice-page .crm-tab-btn').forEach(function(e) { e.classList.remove('active'); });
    var target = document.getElementById('fs-' + id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};

// Farmer Portal Tab Switching
window.fpTab = function(id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('#farmerportal-page .crm-tab-content').forEach(function(e) { e.classList.remove('active'); });
    container.querySelectorAll('#farmerportal-page .crm-tab-btn').forEach(function(e) { e.classList.remove('active'); });
    var target = document.getElementById('fp-' + id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};

// Survey Tab Switching
window.surveyTab = function(id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('#survey-page .crm-tab-content').forEach(function(e) { e.classList.remove('active'); });
    container.querySelectorAll('#survey-page .crm-tab-btn').forEach(function(e) { e.classList.remove('active'); });
    var target = document.getElementById('survey-' + id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};

// Schemes Tab Switching
window.schemeTab = function(id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('#schemes-page .crm-tab-content').forEach(function(e) { e.classList.remove('active'); });
    container.querySelectorAll('#schemes-page .crm-tab-btn').forEach(function(e) { e.classList.remove('active'); });
    var target = document.getElementById('scheme-' + id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
'''
    
    # Find a good place to add functions - before the closing of a script block
    # or at end of file
    content = content + '\n' + tab_functions
    
    with open('dashboard/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Added tab functions")

if __name__ == "__main__":
    add_sidebar_and_functions()

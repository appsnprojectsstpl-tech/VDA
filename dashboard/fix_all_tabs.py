"""
COMPREHENSIVE TAB FIX — Fixes ALL 99 broken tabs across 13 pages.
Approach: For each page with broken tabs, inject content pane divs + tab switch functions.

Strategy:
1. For pages where the tab function exists but panes are missing (PANE_MISSING):
   - Inject pane divs with placeholder content into the page HTML template
2. For pages where the tab function is also missing (FN_MISSING):
   - Create the tab function using the universal pattern
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

fixes_applied = 0

# ============================================================
# Helper: Generate placeholder pane HTML
# ============================================================
def make_pane(pane_id, title, icon, pane_class='dairy-pane', is_first=False):
    active = ' active' if is_first else ''
    return f'''<div id="{pane_id}" class="{pane_class}{active}">
    <div class="page-section">
        <div class="section-title">{icon} {title}</div>
        <div class="chart-placeholder" style="padding:30px;text-align:center;color:rgba(200,214,229,0.5);">
            <div style="font-size:2rem;margin-bottom:8px;">🔧</div>
            <div>Module under development</div>
        </div>
    </div>
</div>
'''

# ============================================================
# SOLAR: solarTab('dash') → needs pane id="sol-dash" etc.
# The Solar page uses solarTab(id, btn) which looks for #sol-{id}
# ============================================================
solar_tabs = [
    ('sol-dash', 'Dashboard', '📊', True),
    ('sol-config', 'Plant Configuration', '⚙️', False),
    ('sol-gen', 'Generation Analytics', '⚡', False),
    ('sol-ai', 'AI Predictions', '🤖', False),
    ('sol-om', 'O&M Management', '🔧', False),
    ('sol-finance', 'Financial Dashboard', '💰', False),
    ('sol-sustain', 'Sustainability', '🌿', False),
    ('sol-reports', 'Reports & Analytics', '📊', False),
    ('sol-team', 'Team Management', '👥', False),
    ('sol-settings', 'Settings', '⚙️', False),
    ('sol-mobile', 'Mobile Sync', '📱', False),
]

# Find the solar page template end (last line before the closing backtick)
solar_marker = "solarTab('mobile',this)"
solar_idx = js.find(solar_marker)
if solar_idx > 0:
    # Find the end of the tab nav div
    nav_end = js.find('</div>', solar_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        # Check if panes already exist
        if 'id="sol-dash"' not in js:
            panes = '\n<!-- Solar Tab Panes -->\n'
            for pid, title, icon, is_first in solar_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(solar_tabs)
            print(f'  Solar: Added {len(solar_tabs)} panes')

# ============================================================
# CRM: crmTab('dash') → needs pane id="crm-dash" etc.
# ============================================================
crm_tabs = [
    ('crm-dash', 'CRM Dashboard', '📊', True),
    ('crm-buyers', 'Buyer Management', '👥', False),
    ('crm-contracts', 'Contracts', '📄', False),
    ('crm-pipeline', 'Sales Pipeline', '📈', False),
    ('crm-leads', 'Lead Tracking', '🎯', False),
    ('crm-tasks', 'Task Management', '✅', False),
    ('crm-communications', 'Communications', '💬', False),
    ('crm-crep', 'Reports', '📊', False),
]

crm_marker = "crmTab('crep'"
crm_idx = js.find(crm_marker)
if crm_idx > 0:
    nav_end = js.find('</div>', crm_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="crm-dash"' not in js:
            panes = '\n<!-- CRM Tab Panes -->\n'
            for pid, title, icon, is_first in crm_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(crm_tabs)
            print(f'  CRM: Added {len(crm_tabs)} panes')

# ============================================================
# HRM: hrmTab('employees') → needs pane id="hrm-employees" etc.
# ============================================================
hrm_tabs = [
    ('hrm-employees', 'Employee Directory', '👥', True),
    ('hrm-attendance', 'Attendance Tracking', '📅', False),
    ('hrm-payroll', 'Payroll Management', '💰', False),
    ('hrm-leaves', 'Leave Management', '🏖️', False),
    ('hrm-hreports', 'HR Reports', '📊', False),
]

hrm_marker = "hrmTab('hreports'"
hrm_idx = js.find(hrm_marker)
if hrm_idx > 0:
    nav_end = js.find('</div>', hrm_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="hrm-employees"' not in js:
            panes = '\n<!-- HRM Tab Panes -->\n'
            for pid, title, icon, is_first in hrm_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(hrm_tabs)
            print(f'  HRM: Added {len(hrm_tabs)} panes')

# ============================================================
# INVENTORY: invTab('stock') → needs pane id="inv-stock" etc.
# ============================================================
inv_tabs = [
    ('inv-stock', 'Stock Register', '📦', True),
    ('inv-reorder', 'Reorder & Alerts', '🔔', False),
    ('inv-purchase', 'Purchase Orders', '🛒', False),
    ('inv-consumption', 'Consumption Tracking', '📊', False),
    ('inv-vreports', 'Reports', '📈', False),
]

inv_marker = "invTab('vreports'"
inv_idx = js.find(inv_marker)
if inv_idx > 0:
    nav_end = js.find('</div>', inv_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="inv-stock"' not in js:
            panes = '\n<!-- Inventory Tab Panes -->\n'
            for pid, title, icon, is_first in inv_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(inv_tabs)
            print(f'  Inventory: Added {len(inv_tabs)} panes')

# ============================================================
# DMS: dmsTab('browse') → needs pane id="dms-browse" etc.
# ============================================================
dms_tabs = [
    ('dms-browse', 'Browse Documents', '📁', True),
    ('dms-upload', 'Upload', '📤', False),
    ('dms-search', 'Search', '🔍', False),
]

dms_marker = "dmsTab('search'"
dms_idx = js.find(dms_marker)
if dms_idx > 0:
    nav_end = js.find('</div>', dms_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="dms-browse"' not in js:
            panes = '\n<!-- DMS Tab Panes -->\n'
            for pid, title, icon, is_first in dms_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(dms_tabs)
            print(f'  DMS: Added {len(dms_tabs)} panes')

# ============================================================
# TICKETING: ticketTab('all') → needs pane id="tick-all" etc.
# ============================================================
tick_tabs = [
    ('tick-all', 'All Tickets', '🎫', True),
    ('tick-open', 'Open Tickets', '📝', False),
    ('tick-my', 'My Tickets', '👤', False),
    ('tick-create', 'Create Ticket', '➕', False),
]

tick_marker = "ticketTab('create'"
tick_idx = js.find(tick_marker)
if tick_idx > 0:
    nav_end = js.find('</div>', tick_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="tick-all"' not in js:
            panes = '\n<!-- Ticketing Tab Panes -->\n'
            for pid, title, icon, is_first in tick_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(tick_tabs)
            print(f'  Ticketing: Added {len(tick_tabs)} panes')

# ============================================================
# BI: biTab('overview') → needs pane id="bi-overview" etc.
# ============================================================
bi_tabs = [
    ('bi-overview', 'Business Overview', '📊', True),
    ('bi-revenue', 'Revenue Analytics', '💰', False),
    ('bi-operations', 'Operations Intelligence', '⚙️', False),
    ('bi-forecast', 'Forecasting', '🔮', False),
]

bi_marker = "biTab('forecast'"
bi_idx = js.find(bi_marker)
if bi_idx > 0:
    nav_end = js.find('</div>', bi_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="bi-overview"' not in js:
            panes = '\n<!-- BI Tab Panes -->\n'
            for pid, title, icon, is_first in bi_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(bi_tabs)
            print(f'  BI: Added {len(bi_tabs)} panes')

# ============================================================
# BOOKING: bookingTab('all-bookings') → needs pane id="bk-all-bookings" etc.
# ============================================================
bk_tabs = [
    ('bk-all-bookings', 'All Bookings', '📋', True),
    ('bk-agri-tourism', 'Agri Tourism', '🌾', False),
    ('bk-vet-appointments', 'Vet Appointments', '🏥', False),
    ('bk-events', 'Events', '📅', False),
    ('bk-calendar', 'Calendar', '🗓️', False),
]

bk_marker = "bookingTab('calendar'"
bk_idx = js.find(bk_marker)
if bk_idx > 0:
    nav_end = js.find('</div>', bk_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="bk-all-bookings"' not in js:
            panes = '\n<!-- Booking Tab Panes -->\n'
            for pid, title, icon, is_first in bk_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(bk_tabs)
            print(f'  Booking: Added {len(bk_tabs)} panes')

# ============================================================
# LMS: lmsTab('courses') → needs pane id="lms-courses" etc.
# ============================================================
lms_tabs = [
    ('lms-courses', 'Course Catalog', '📚', True),
    ('lms-my-learning', 'My Learning', '📖', False),
    ('lms-certifications', 'Certifications', '🎓', False),
    ('lms-assessments', 'Assessments', '📝', False),
    ('lms-analytics', 'Learning Analytics', '📊', False),
]

lms_marker = "lmsTab('analytics'"
lms_idx = js.find(lms_marker)
if lms_idx > 0:
    nav_end = js.find('</div>', lms_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="lms-courses"' not in js:
            panes = '\n<!-- LMS Tab Panes -->\n'
            for pid, title, icon, is_first in lms_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(lms_tabs)
            print(f'  LMS: Added {len(lms_tabs)} panes')

# ============================================================
# FIELDSERVICE: fsTab('all-jobs') → needs pane id="fs-all-jobs" etc.
# ============================================================
fs_tabs = [
    ('fs-all-jobs', 'All Jobs', '📋', True),
    ('fs-scheduled', 'Scheduled', '📅', False),
    ('fs-in-progress', 'In Progress', '🔄', False),
    ('fs-completed', 'Completed', '✅', False),
    ('fs-field-map', 'Field Map', '🗺️', False),
]

fs_marker = "fsTab('field-map'"
fs_idx = js.find(fs_marker)
if fs_idx > 0:
    nav_end = js.find('</div>', fs_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="fs-all-jobs"' not in js:
            panes = '\n<!-- Field Service Tab Panes -->\n'
            for pid, title, icon, is_first in fs_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(fs_tabs)
            print(f'  Field Service: Added {len(fs_tabs)} panes')

# ============================================================
# FARMERPORTAL: fpTab('dashboard') → needs pane id="fp-dashboard" etc.
# ============================================================
fp_tabs = [
    ('fp-dashboard', 'Dashboard', '📊', True),
    ('fp-crops', 'Crop Management', '🌾', False),
    ('fp-livestock', 'Livestock', '🐄', False),
    ('fp-schemes', 'Government Schemes', '🏛️', False),
    ('fp-market', 'Market Prices', '💹', False),
]

fp_marker = "fpTab('market'"
fp_idx = js.find(fp_marker)
if fp_idx > 0:
    nav_end = js.find('</div>', fp_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="fp-dashboard"' not in js:
            panes = '\n<!-- Farmer Portal Tab Panes -->\n'
            for pid, title, icon, is_first in fp_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(fp_tabs)
            print(f'  Farmer Portal: Added {len(fp_tabs)} panes')

# ============================================================
# SURVEY: surveyTab('surveys') → needs pane id="srv-surveys" etc.
# ============================================================
srv_tabs = [
    ('srv-surveys', 'All Surveys', '📋', True),
    ('srv-farmer', 'Farmer Surveys', '🌾', False),
    ('srv-satisfaction', 'Satisfaction', '😊', False),
    ('srv-analytics', 'Analytics', '📊', False),
]

srv_marker = "surveyTab('analytics'"
srv_idx = js.find(srv_marker)
if srv_idx > 0:
    nav_end = js.find('</div>', srv_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="srv-surveys"' not in js:
            panes = '\n<!-- Survey Tab Panes -->\n'
            for pid, title, icon, is_first in srv_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(srv_tabs)
            print(f'  Survey: Added {len(srv_tabs)} panes')

# ============================================================
# SCHEMES: schemeTab('schemes') → needs pane id="sch-schemes" etc.
# ============================================================
sch_tabs = [
    ('sch-schemes', 'All Schemes', '🏛️', True),
    ('sch-applications', 'Applications', '📝', False),
    ('sch-disbursements', 'Disbursements', '💰', False),
    ('sch-analytics', 'Analytics', '📊', False),
]

sch_marker = "schemeTab('analytics'"
sch_idx = js.find(sch_marker)
if sch_idx > 0:
    nav_end = js.find('</div>', sch_idx)
    if nav_end > 0:
        nav_end = js.find('\n', nav_end) + 1
        if 'id="sch-schemes"' not in js:
            panes = '\n<!-- Schemes Tab Panes -->\n'
            for pid, title, icon, is_first in sch_tabs:
                panes += make_pane(pid, title, icon, 'dairy-pane', is_first)
            js = js[:nav_end] + panes + js[nav_end:]
            fixes_applied += len(sch_tabs)
            print(f'  Schemes: Added {len(sch_tabs)} panes')

# ============================================================
# Now add missing tab switch functions
# ============================================================
missing_fns = """

/* ============================================================
   MISSING TAB FUNCTIONS v7.4 — One function per module
   ============================================================ */

/* CRM */
window.crmTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('crm-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};
window.filterTasks = function(f) { console.log('Filter tasks:', f); };
window.filterComms = function(f) { console.log('Filter comms:', f); };

/* HRM */
window.hrmTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('hrm-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* Inventory */
window.invTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('inv-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* DMS */
window.dmsTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('dms-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* BI */
window.biTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('bi-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* Booking */
window.bookingTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('bk-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* LMS */
window.lmsTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('lms-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* Field Service */
window.fsTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('fs-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* Farmer Portal */
window.fpTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('fp-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* Survey */
window.surveyTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('srv-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* Schemes */
window.schemeTab = function(id, btn) {
    var c = document.getElementById('page-container') || document.body;
    c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
    var el = document.getElementById('sch-'+id) || document.getElementById(id);
    if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
    if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
};

/* Solar — Override existing solarTab to use prefix */
(function(){
    var _orig = window.solarTab;
    window.solarTab = function(id, btn) {
        var c = document.getElementById('page-container') || document.body;
        c.querySelectorAll('.dairy-pane').forEach(function(p){ p.classList.remove('active'); p.style.setProperty('display','none','important'); });
        var el = document.getElementById('sol-'+id) || document.getElementById(id);
        if(el){ el.classList.add('active'); el.style.setProperty('display','block','important'); }
        if(btn){ var n=btn.closest('[class*=\"-nav\"]')||btn.parentElement; if(n) n.querySelectorAll('button').forEach(function(b){b.classList.remove('active');}); btn.classList.add('active'); }
    };
})();

console.log('Missing Tab Functions v7.4 loaded');
/* END MISSING TAB FUNCTIONS v7.4 */
"""

if 'MISSING TAB FUNCTIONS v7.4' not in js:
    js += missing_fns
    fixes_applied += 12
    print(f'  Added 12 tab function definitions')

# Save
with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

# Bump versions
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=7.4.0', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=7.4.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

# Syntax check
exit_code = os.system(f'node --check "{JS}" 2>&1')
print(f'\nSYNTAX: {"OK" if exit_code == 0 else "ERROR"}')
print(f'Total fixes applied: {fixes_applied}')
print(f'Version: 7.4.0')

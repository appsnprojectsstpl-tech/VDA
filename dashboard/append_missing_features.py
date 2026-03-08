import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
CSS = r'e:\Vedavathi\dashboard\index.css'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# Only append what's missing
missing_js = ''

if 'applyMoreDropdown' not in js:
    missing_js += r'''

/* --- TAB "MORE" DROPDOWN (v6.7 supplement) --- */
(function() {
    var MAX_VISIBLE = 7;

    function applyMoreDropdown() {
        document.querySelectorAll('.dairy-nav, .vet-nav, .en-nav, .crm-nav, .vermi-nav, .tree-nav, .aqua-nav, .paint-nav, .biogas-nav, .wind-nav, .solar-nav, .carbon-nav, .fin-nav').forEach(function(nav) {
            if (nav.dataset.moreApplied) return;
            var btns = Array.from(nav.querySelectorAll('button'));
            if (btns.length <= MAX_VISIBLE) return;

            nav.dataset.moreApplied = '1';
            var hidden = btns.slice(MAX_VISIBLE);

            var moreWrap = document.createElement('div');
            moreWrap.className = 'hub-more-container';
            moreWrap.style.cssText = 'position:relative;display:inline-flex;flex-shrink:0;';

            var moreBtn = document.createElement('button');
            moreBtn.type = 'button';
            moreBtn.className = 'dairy-tab-btn hub-more-btn';
            moreBtn.innerHTML = 'More \u25BC <span style="background:rgba(0,176,255,0.2);color:#42caff;padding:1px 6px;border-radius:99px;font-size:0.65rem;margin-left:4px">' + hidden.length + '</span>';

            var dropdown = document.createElement('div');
            dropdown.className = 'hub-more-dropdown';
            dropdown.style.cssText = 'position:absolute;top:calc(100% + 6px);right:0;background:#1a2035;border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:6px;display:none;flex-direction:column;gap:3px;min-width:200px;z-index:200;box-shadow:0 8px 32px rgba(0,0,0,0.5);max-height:300px;overflow-y:auto;';

            hidden.forEach(function(btn) {
                var clone = btn.cloneNode(true);
                clone.style.cssText += 'width:100%;justify-content:flex-start;border-radius:8px;padding:7px 12px;display:flex;';
                clone.addEventListener('click', function() {
                    btn.click();
                    dropdown.style.display = 'none';
                });
                dropdown.appendChild(clone);
                btn.style.display = 'none';
            });

            moreBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                var isOpen = dropdown.style.display === 'flex';
                dropdown.style.display = isOpen ? 'none' : 'flex';
            });

            document.addEventListener('click', function() { dropdown.style.display = 'none'; });

            moreWrap.appendChild(moreBtn);
            moreWrap.appendChild(dropdown);
            nav.appendChild(moreWrap);
        });
    }
    window.applyMoreDropdown = applyMoreDropdown;
    setTimeout(applyMoreDropdown, 600);
    var pc = document.getElementById('page-container');
    if (pc) {
        new MutationObserver(function() { setTimeout(applyMoreDropdown, 300); }).observe(pc, { childList: true });
    }
})();
'''
    print('Added: applyMoreDropdown')

if 'updateBreadcrumb' not in js:
    missing_js += r'''

/* --- BREADCRUMB AUTO-UPDATE (v6.7 supplement) --- */
(function() {
    var pageNames = {
        overview:'Global Overview', cattle:'Cattle Management', poultry:'Poultry Hub',
        solar:'Solar Capacity', wind:'Wind Generation', biogas:'Biogas Plants',
        hydrogen:'Green Hydrogen', hydro:'Hydropower', kinetic:'Kinetic Energy',
        grid:'Smart Grid AI', tourism:'Agri-Tourism', carbon:'Carbon Hub',
        paint:'Bio-Paints', crm:'CRM & Contracts', vermi:'Vermicompost',
        tree:'TreeSwasthya AI', aqua:'Aquaculture Hub', vet:'Veterinary Hosp.',
        vedic:'Vedic Hub', logistics:'Logistics', water:'Water Mgmt',
        trust:'Vedavathi Trust', command:'Command Center', finance:'Finance & Accts',
        finance2:'Finance & ROI', hrm:'HRM & Payroll', dms:'Documents',
        bi:'BI & Analytics', workflow:'Workflow', ticketing:'Helpdesk',
        inventory:'Inventory', booking:'Bookings', lms:'LMS',
        survey:'Survey', fieldservice:'Field Service', farmerportal:'Farmer Portal'
    };
    var pageGroups = {
        solar:'Energy', wind:'Energy', biogas:'Energy', hydrogen:'Energy',
        hydro:'Energy', kinetic:'Energy', grid:'Energy',
        cattle:'Agri & Animal', poultry:'Agri & Animal', aqua:'Agri & Animal',
        vermi:'Agri & Animal', tree:'Agri & Animal', carbon:'Agri & Animal',
        paint:'Agri & Animal', vet:'Institutional', vedic:'Institutional',
        trust:'Institutional', crm:'Sales', tourism:'Sales', booking:'Sales',
        hrm:'Admin', finance:'Admin', finance2:'Admin', dms:'Admin',
        bi:'Admin', workflow:'Admin', ticketing:'Admin',
        logistics:'Operations', water:'Operations', command:'Operations',
        inventory:'Operations', fieldservice:'Services', lms:'Services',
        survey:'Services', farmerportal:'Portals'
    };

    function updateBreadcrumb(key) {
        var breadcrumbs = document.getElementById('breadcrumbs');
        if (!breadcrumbs) return;
        var group = pageGroups[key] || '';
        var name = pageNames[key] || key;
        if (group) {
            breadcrumbs.innerHTML = '<span class="breadcrumb-home" onclick="showPage(\'overview\')" style="cursor:pointer;color:rgba(200,214,229,0.5)">Home</span>' +
                '<span class="breadcrumb-sep" style="color:rgba(200,214,229,0.3)"> \u203A </span>' +
                '<span style="color:rgba(200,214,229,0.5);font-size:0.82rem">' + group + '</span>' +
                '<span class="breadcrumb-sep" style="color:rgba(200,214,229,0.3)"> \u203A </span>' +
                '<span id="bc-current" style="color:rgba(200,214,229,0.9);font-weight:600">' + name + '</span>';
        } else {
            breadcrumbs.innerHTML = '<span class="breadcrumb-home" onclick="showPage(\'overview\')" style="cursor:pointer;color:rgba(200,214,229,0.5)">Home</span>' +
                '<span class="breadcrumb-sep" style="color:rgba(200,214,229,0.3)"> \u203A </span>' +
                '<span id="bc-current" style="color:rgba(200,214,229,0.9);font-weight:600">' + name + '</span>';
        }
    }
    window.updateBreadcrumb = updateBreadcrumb;

    // Patch showPage to update breadcrumbs
    var _sp = window.showPage;
    if (_sp) {
        window.showPage = function(key) {
            _sp(key);
            updateBreadcrumb(key);
            localStorage.setItem('vedavathi_lastPage', key);
            // Highlight active sidebar
            document.querySelectorAll('.menu-item').forEach(function(mi) {
                mi.classList.remove('active');
                var oc = mi.getAttribute('onclick') || '';
                if (oc.includes("'" + key + "'")) mi.classList.add('active');
            });
        };
    }
})();
'''
    print('Added: updateBreadcrumb')

if missing_js:
    with open(JS, 'a', encoding='utf-8') as f:
        f.write(missing_js)
    print('Appended missing JS')
else:
    print('All JS already present')

# CSS supplements
with open(CSS, encoding='utf-8', errors='replace') as f:
    css = f.read()

missing_css = ''
if 'toastIn' not in css:
    missing_css += '''

@keyframes toastIn {
    from { opacity: 0; transform: translateX(40px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes toastOut {
    from { opacity: 1; transform: translateX(0); }
    to   { opacity: 0; transform: translateX(40px); }
}
'''
    print('Added: toast animations CSS')

if missing_css:
    with open(CSS, 'a', encoding='utf-8') as f:
        f.write(missing_css)

# Syntax check
print('\nSyntax check...')
exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=6.7.1', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=6.7.1', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)
print('Bumped to v6.7.1')

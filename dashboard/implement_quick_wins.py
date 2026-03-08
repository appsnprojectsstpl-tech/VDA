"""
IMPLEMENT QUICK WIN IMPROVEMENTS
1. Toast notification system
2. safeFetch() wrapper
3. Tab "More" dropdown for 8+ tabs
4. Breadcrumb updates on navigation
5. Persist sidebar state in localStorage
6. Skeleton loading CSS
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'e:\Vedavathi\dashboard'
JS = os.path.join(BASE, 'app.js')
CSS = os.path.join(BASE, 'index.css')
HTML = os.path.join(BASE, 'index.html')

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# ==================================================================
# JS IMPROVEMENTS
# ==================================================================

improvements_js = r'''

/* ============================================================
   QUICK WIN IMPROVEMENTS — v6.7.0
   1. Toast notifications
   2. safeFetch wrapper
   3. Tab "More" dropdown
   4. Breadcrumb updates
   5. LocalStorage persistence
   ============================================================ */

/* --- 1. TOAST NOTIFICATION SYSTEM --- */
(function() {
    // Create toast container
    var container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = 'position:fixed;top:72px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:8px;pointer-events:none;';
    document.body.appendChild(container);

    window.showToast = function(message, type, duration) {
        type = type || 'info';
        duration = duration || 3500;
        var toast = document.createElement('div');
        toast.className = 'toast toast-' + type;
        var icons = { success: '\u2705', error: '\u274C', warning: '\u26A0\uFE0F', info: '\u2139\uFE0F' };
        toast.innerHTML = '<span class="toast-icon">' + (icons[type] || icons.info) + '</span><span class="toast-msg">' + message + '</span>';
        toast.style.cssText = 'pointer-events:auto;display:flex;align-items:center;gap:10px;padding:12px 20px;border-radius:10px;font-size:0.85rem;font-weight:500;color:#e0eaf4;backdrop-filter:blur(16px);box-shadow:0 8px 32px rgba(0,0,0,0.4);animation:toastIn 0.3s ease;max-width:380px;border:1px solid rgba(255,255,255,0.08);font-family:Inter,sans-serif;';
        var bgMap = { success: 'rgba(0,200,83,0.15)', error: 'rgba(255,82,82,0.15)', warning: 'rgba(255,171,0,0.15)', info: 'rgba(0,176,255,0.15)' };
        toast.style.background = bgMap[type] || bgMap.info;
        container.appendChild(toast);
        setTimeout(function() {
            toast.style.animation = 'toastOut 0.3s ease forwards';
            setTimeout(function() { toast.remove(); }, 300);
        }, duration);
    };

    // Override alert() with toast
    var _origAlert = window.alert;
    window.alert = function(msg) {
        if (typeof msg === 'string' && (msg.includes('Coming soon') || msg.includes('form') || msg.includes('saved') || msg.includes('success'))) {
            window.showToast(msg, msg.toLowerCase().includes('error') ? 'error' : 'info');
        } else {
            window.showToast(String(msg), 'info');
        }
    };
})();

/* --- 2. safeFetch WRAPPER --- */
window.safeFetch = async function(url, options, fallbackMsg) {
    try {
        var res = await fetch(url, options || {});
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return await res.json();
    } catch(e) {
        console.warn('safeFetch failed:', url, e.message);
        window.showToast(fallbackMsg || 'Failed to load data — check your connection', 'error', 5000);
        return null;
    }
};

/* --- 3. TAB "MORE" DROPDOWN --- */
(function() {
    var MAX_VISIBLE = 7;

    function applyMoreDropdown() {
        document.querySelectorAll('.dairy-nav, .vet-nav, .en-nav, .crm-nav, .vermi-nav, .tree-nav, .aqua-nav, .paint-nav, .biogas-nav, .wind-nav, .solar-nav, .carbon-nav, .fin-nav').forEach(function(nav) {
            if (nav.dataset.moreApplied) return;
            var btns = Array.from(nav.querySelectorAll('button, .dairy-tab-btn, .en-tbtn, .vermi-tbtn, .tree-tbtn'));
            if (btns.length <= MAX_VISIBLE) return;

            nav.dataset.moreApplied = '1';
            var visible = btns.slice(0, MAX_VISIBLE);
            var hidden = btns.slice(MAX_VISIBLE);

            // Create More wrapper
            var moreWrap = document.createElement('div');
            moreWrap.className = 'hub-more-container';
            moreWrap.style.cssText = 'position:relative;display:inline-flex;flex-shrink:0;';

            var moreBtn = document.createElement('button');
            moreBtn.type = 'button';
            moreBtn.className = 'dairy-tab-btn hub-more-btn';
            moreBtn.innerHTML = 'More \u25BC <span class="more-count">' + hidden.length + '</span>';
            moreBtn.style.cssText = 'white-space:nowrap;';

            var dropdown = document.createElement('div');
            dropdown.className = 'hub-more-dropdown';
            dropdown.style.cssText = 'position:absolute;top:calc(100% + 6px);right:0;background:#1a2035;border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:6px;display:none;flex-direction:column;gap:3px;min-width:200px;z-index:200;box-shadow:0 8px 32px rgba(0,0,0,0.5);max-height:300px;overflow-y:auto;';

            hidden.forEach(function(btn) {
                var clone = btn.cloneNode(true);
                clone.style.cssText += 'width:100%;justify-content:flex-start;border-radius:8px;padding:7px 12px;';
                // When clicked in dropdown, also activate in main nav
                clone.addEventListener('click', function(e) {
                    // Trigger the original button click
                    btn.click();
                    // Move this button to visible area and swap
                    dropdown.style.display = 'none';
                    moreBtn.classList.remove('active');
                });
                dropdown.appendChild(clone);
            });

            // Hide overflow buttons
            hidden.forEach(function(btn) { btn.style.display = 'none'; });

            moreBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                var isOpen = dropdown.style.display === 'flex';
                dropdown.style.display = isOpen ? 'none' : 'flex';
                moreBtn.classList.toggle('active', !isOpen);
            });

            // Close on outside click
            document.addEventListener('click', function() {
                dropdown.style.display = 'none';
                moreBtn.classList.remove('active');
            });

            moreWrap.appendChild(moreBtn);
            moreWrap.appendChild(dropdown);
            nav.appendChild(moreWrap);
        });
    }

    // Apply on page load and on page switches
    setTimeout(applyMoreDropdown, 500);

    // Re-apply when page content changes
    var observer = new MutationObserver(function() { setTimeout(applyMoreDropdown, 200); });
    var pc = document.getElementById('page-container');
    if (pc) observer.observe(pc, { childList: true });
})();

/* --- 4. BREADCRUMB UPDATES --- */
(function() {
    var pageNames = {
        overview: 'Global Overview', cattle: 'Cattle Management', poultry: 'Poultry Hub',
        solar: 'Solar Capacity', wind: 'Wind Generation', biogas: 'Biogas Plants',
        hydrogen: 'Green Hydrogen', hydro: 'Hydropower', kinetic: 'Kinetic Energy',
        grid: 'Smart Grid AI', tourism: 'Agri-Tourism', carbon: 'Carbon Hub',
        paint: 'Bio-Paints', crm: 'CRM & Contracts', vermi: 'Vermicompost',
        tree: 'TreeSwasthya AI', aqua: 'Aquaculture Hub', vet: 'Veterinary Hosp.',
        vedic: 'Vedic Hub', logistics: 'Logistics', water: 'Water Mgmt',
        trust: 'Vedavathi Trust', command: 'Command Center', finance: 'Finance & Accts',
        finance2: 'Finance & ROI', hrm: 'HRM & Payroll', dms: 'Documents',
        bi: 'BI & Analytics', workflow: 'Workflow', ticketing: 'Helpdesk',
        inventory: 'Inventory', booking: 'Bookings', lms: 'LMS',
        survey: 'Survey', fieldservice: 'Field Service', farmerportal: 'Farmer Portal'
    };

    // Groups
    var pageGroups = {
        solar: 'Energy', wind: 'Energy', biogas: 'Energy', hydrogen: 'Energy',
        hydro: 'Energy', kinetic: 'Energy', grid: 'Energy',
        cattle: 'Agri & Animal', poultry: 'Agri & Animal', aqua: 'Agri & Animal',
        vermi: 'Agri & Animal', tree: 'Agri & Animal', carbon: 'Agri & Animal',
        paint: 'Agri & Animal', vet: 'Institutional',
        crm: 'Sales & Commerce', tourism: 'Sales & Commerce', booking: 'Sales & Commerce',
        hrm: 'Admin & Mgmt', finance: 'Admin & Mgmt', finance2: 'Admin & Mgmt',
        dms: 'Admin & Mgmt', bi: 'Admin & Mgmt', workflow: 'Admin & Mgmt',
        ticketing: 'Admin & Mgmt', trust: 'Institutional', vedic: 'Institutional',
        logistics: 'Operations', water: 'Operations', command: 'Operations',
        inventory: 'Operations', fieldservice: 'Services', lms: 'Services',
        survey: 'Services', farmerportal: 'Portals'
    };

    var _origShowPage = window.showPage;
    if (_origShowPage) {
        window.showPage = function(key) {
            _origShowPage(key);
            updateBreadcrumb(key);
            localStorage.setItem('vedavathi_lastPage', key);
        };
    }

    function updateBreadcrumb(key) {
        var bc = document.getElementById('bc-current');
        if (!bc) return;
        var group = pageGroups[key] || '';
        var name = pageNames[key] || key;
        var breadcrumbs = document.getElementById('breadcrumbs');
        if (breadcrumbs) {
            if (group) {
                breadcrumbs.innerHTML = '<span class="breadcrumb-home" onclick="showPage(\'overview\')" style="cursor:pointer">Home</span>' +
                    '<span class="breadcrumb-sep"> \u203A </span>' +
                    '<span class="breadcrumb-group" style="color:rgba(200,214,229,0.5)">' + group + '</span>' +
                    '<span class="breadcrumb-sep"> \u203A </span>' +
                    '<span id="bc-current" style="color:rgba(200,214,229,0.9);font-weight:600">' + name + '</span>';
            } else {
                breadcrumbs.innerHTML = '<span class="breadcrumb-home" onclick="showPage(\'overview\')" style="cursor:pointer">Home</span>' +
                    '<span class="breadcrumb-sep"> \u203A </span>' +
                    '<span id="bc-current" style="color:rgba(200,214,229,0.9);font-weight:600">' + name + '</span>';
            }
        }
    }
    window.updateBreadcrumb = updateBreadcrumb;
})();

/* --- 5. PERSIST SIDEBAR STATE --- */
(function() {
    // Restore last page on load
    var lastPage = localStorage.getItem('vedavathi_lastPage');
    if (lastPage && lastPage !== 'overview' && window.showPage) {
        setTimeout(function() {
            try { window.showPage(lastPage); } catch(e) {}
        }, 300);
    }

    // Restore collapsed groups
    var collapsed = JSON.parse(localStorage.getItem('vedavathi_collapsed') || '[]');
    collapsed.forEach(function(groupId) {
        var header = document.querySelector('[data-group="' + groupId + '"]');
        if (header) {
            var list = header.nextElementSibling;
            if (list) list.style.display = 'none';
            header.classList.add('collapsed');
        }
    });

    // Save collapsed state when toggling
    var _origToggle = window.toggleSidebarGroup;
    if (_origToggle) {
        window.toggleSidebarGroup = function(el) {
            _origToggle(el);
            // Save state
            setTimeout(function() {
                var allHeaders = document.querySelectorAll('.menu-group-header');
                var hidden = [];
                allHeaders.forEach(function(h) {
                    var list = h.nextElementSibling;
                    if (list && list.style.display === 'none') {
                        var g = h.getAttribute('data-group') || h.textContent.trim();
                        hidden.push(g);
                    }
                });
                localStorage.setItem('vedavathi_collapsed', JSON.stringify(hidden));
            }, 100);
        };
    }

    // Highlight active sidebar item
    var _origShowPage2 = window.showPage;
    if (_origShowPage2) {
        var __showPage = window.showPage;
        window.showPage = function(key) {
            __showPage(key);
            document.querySelectorAll('.menu-item').forEach(function(mi) {
                mi.classList.remove('active');
                var pk = mi.getAttribute('data-page') || mi.getAttribute('onclick');
                if (pk && pk.includes("'" + key + "'")) {
                    mi.classList.add('active');
                }
            });
        };
    }
})();

/* END QUICK WIN IMPROVEMENTS */
'''

# Check not already appended
if 'QUICK WIN IMPROVEMENTS' not in js:
    with open(JS, 'a', encoding='utf-8') as f:
        f.write(improvements_js)
    print('JS improvements appended')
else:
    print('JS improvements already present')

# ==================================================================
# CSS: Toast + Skeleton + More dropdown
# ==================================================================
print('\nAdding CSS...')

with open(CSS, encoding='utf-8') as f:
    css = f.read()

improvements_css = '''

/* ============================================================
   QUICK WIN CSS — v6.7.0
   Toast, Skeleton, More dropdown, Breadcrumb
   ============================================================ */

/* Toast animations */
@keyframes toastIn {
    from { opacity: 0; transform: translateX(40px); }
    to   { opacity: 1; transform: translateX(0); }
}

@keyframes toastOut {
    from { opacity: 1; transform: translateX(0); }
    to   { opacity: 0; transform: translateX(40px); }
}

.toast {
    pointer-events: auto !important;
}

.toast-icon {
    font-size: 1rem;
    flex-shrink: 0;
}

.toast-msg {
    flex: 1;
    line-height: 1.4;
}

/* Skeleton loading shimmer */
@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.skeleton {
    background: linear-gradient(90deg,
        rgba(255,255,255,0.03) 0%,
        rgba(255,255,255,0.07) 50%,
        rgba(255,255,255,0.03) 100%) !important;
    background-size: 200% 100% !important;
    animation: shimmer 1.8s ease infinite !important;
    border-radius: 6px !important;
    color: transparent !important;
    pointer-events: none !important;
    min-height: 16px;
}

.skeleton-card {
    min-height: 120px;
}

.skeleton-row {
    height: 40px;
    margin-bottom: 6px;
}

/* More dropdown styling */
.hub-more-container {
    position: relative !important;
    display: inline-flex !important;
    flex-shrink: 0 !important;
}

.hub-more-btn .more-count {
    background: rgba(0,176,255,0.2) !important;
    color: #42caff !important;
    padding: 1px 6px !important;
    border-radius: 99px !important;
    font-size: 0.65rem !important;
    margin-left: 4px !important;
}

/* Breadcrumb interactive */
.breadcrumb-home {
    cursor: pointer !important;
    transition: color 0.15s ease !important;
}

.breadcrumb-home:hover {
    color: #42caff !important;
}

.breadcrumb-group {
    font-size: 0.82rem !important;
}

/* Active sidebar item highlight */
.menu-item.active {
    background: rgba(0,176,255,0.08) !important;
    color: #42caff !important;
    border-left: 3px solid #42caff !important;
    font-weight: 600 !important;
}

/* END QUICK WIN CSS */
'''

if 'QUICK WIN CSS' not in css:
    with open(CSS, 'a', encoding='utf-8') as f:
        f.write(improvements_css)
    print('CSS improvements appended')
else:
    print('CSS improvements already present')

# Bump versions
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=6.7.0', h)
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=6.7.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)
print('Versions bumped to v6.7.0')

# Syntax check
print('\nSyntax check...')
exit_code = os.system(f'node --check "{JS}" 2>&1')
if exit_code == 0:
    print('SYNTAX OK')
else:
    print('SYNTAX ERROR — needs fix')

print('\nDone.')

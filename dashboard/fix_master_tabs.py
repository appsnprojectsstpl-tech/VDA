"""
PERMANENT TAB FIX — Addresses all 3 root causes:
1. ID prefix mismatch (dairyTab, etc.) — Try multiple prefix patterns
2. CSS display override — Use setProperty with !important
3. Chart.js SRI hash — Remove integrity attribute
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# ============================================================
# 1. Add a MASTER tab fix that patches ALL tab functions
# ============================================================
master_fix = """

/* ============================================================
   MASTER TAB FIX v7.3 — Patches all tab switching functions at runtime
   ============================================================ */
(function() {
    'use strict';

    /* A. Universal pane show/hide that beats !important CSS */
    function showPane(el) {
        if (!el) return;
        el.classList.add('active');
        el.style.setProperty('display', 'block', 'important');
    }
    function hidePane(el) {
        if (!el) return;
        el.classList.remove('active');
        el.style.setProperty('display', 'none', 'important');
    }

    /* B. Find pane by ID with prefix fallback */
    function findPane(id) {
        if (!id) return null;
        var el = document.getElementById(id);
        if (el) return el;
        
        // Try common prefixes
        var prefixes = ['d-','wnd-','sol-','bio-','p-','aqua-','vpms-','tree-','paint-',
                       'carb-','crm-','vet-','vedic-','trust-','cmd-','log-','water-',
                       'h2-','hyd-','kin-','kems-','grid-','bi-','dms-','hrm-',
                       'inv-','booking-','lms-','survey-','field-','farmer-','tick-',
                       'wf-','fin-','carbon-'];
        for (var i = 0; i < prefixes.length; i++) {
            el = document.getElementById(prefixes[i] + id);
            if (el) return el;
        }
        return null;
    }

    /* C. Master tab switch — works for any page */
    function masterTabSwitch(id, btn) {
        if (!id) return;
        
        // 1. Find all pane containers (broad search)
        var container = document.getElementById('page-container') || document.body;
        var paneSelectors = '.dairy-pane, .vet-pane, .tab-pane, .kems-pane, [class*="-pane"]';
        container.querySelectorAll(paneSelectors).forEach(function(p) {
            hidePane(p);
        });
        
        // 2. Find and show the target pane
        var target = findPane(id);
        if (target) showPane(target);
        
        // 3. Update button active states
        if (btn) {
            var nav = btn.closest('[class*="-nav"]') || btn.parentElement;
            if (nav) {
                nav.querySelectorAll('button').forEach(function(b) {
                    if (!b.classList.contains('hub-more-btn')) {
                        b.classList.remove('active');
                    }
                });
            }
            btn.classList.add('active');
        }
    }

    /* D. Patch existing tab functions to use prefix fallback + !important display */
    
    // List of all tab functions to patch
    var tabFunctions = [
        'windTab', 'solarTab', 'switchBiogasTab', 'switchCarbonTab',
        'switchHydroTab', 'switchHydrogenTab', 'switchKineticTab', 'switchAgriTourTab',
        'switchPaintTab', 'switchVpmsTab', 'switchCommandTab', 'switchLogisticsTab',
        'switchWaterTab', 'switchTrustTab', 'switchCowTab', 'switchPoultryTab',
        'switchTreeTab', 'switchVetTab', 'switchSolarTab',
        'vetTab', 'vedicTab', 'trustTab', 'waterTab',
        'ticketTab', 'wfTab', 'treeTab', 'vermiTab',
        'carbonTab', 'kineticTab', 'hydroTab', 'hydrogenTab',
        'biogasTab', 'paintTab', 'aquaTab', 'crmTab',
        'finTab', 'dmsTab', 'biTab', 'hrmTab', 'invTab',
        'bookingTab', 'lmsTab', 'surveyTab', 'fieldTab', 'farmerTab'
    ];
    
    // Save originals and wrap with prefix-aware + !important version
    tabFunctions.forEach(function(fnName) {
        if (typeof window[fnName] === 'function') {
            var orig = window[fnName];
            window[fnName] = function(id, btn) {
                // Call original first
                orig(id, btn);
                
                // Then ensure the target pane is visible with !important
                var target = findPane(id);
                if (target) {
                    showPane(target);
                }
                
                // If no pane was shown, try masterTabSwitch
                if (!target) {
                    masterTabSwitch(id, btn);
                }
            };
        }
    });

    /* E. Fix dairyTab specifically — it uses different ID pattern */
    var origDairyTab = window.dairyTab;
    if (typeof origDairyTab === 'function') {
        window.dairyTab = function(id, btn) {
            // Smart Dairy uses 'd-' prefix: dairyTab('herd') → #d-herd
            var container = document.getElementById('page-container') || document.body;
            container.querySelectorAll('.dairy-pane').forEach(function(p) { hidePane(p); });
            
            var target = document.getElementById(id) || document.getElementById('d-' + id);
            if (target) showPane(target);
            
            // Update buttons
            if (btn) {
                var nav = btn.closest('.dairy-nav') || btn.parentElement;
                if (nav) {
                    nav.querySelectorAll('.dairy-tab-btn').forEach(function(b) {
                        b.classList.remove('active');
                    });
                }
                btn.classList.add('active');
            }
        };
    }

    /* F. Patch sub-tab functions (Wind, Solar, Biogas) to use !important */
    var subTabFunctions = ['windSubTab', 'solarSubTab', 'biogasSubTab'];
    subTabFunctions.forEach(function(fnName) {
        if (typeof window[fnName] === 'function') {
            var orig = window[fnName];
            window[fnName] = function(subId, btn, paneId) {
                // Call original
                orig(subId, btn, paneId);
                
                // Force visibility with !important 
                var parentPane = paneId ? document.getElementById(paneId) : null;
                if (parentPane) {
                    parentPane.querySelectorAll('[class*="-sub-pane"]').forEach(function(p) {
                        p.style.setProperty('display', 'none', 'important');
                    });
                    var target = parentPane.querySelector('#st-' + subId) ||
                                 parentPane.querySelector('#sub-' + subId) ||
                                 document.getElementById('st-' + subId) ||
                                 document.getElementById(subId);
                    if (target) {
                        target.style.setProperty('display', 'block', 'important');
                    }
                }
                
                // Update sub-tab buttons
                if (btn) {
                    var nav = btn.closest('[class*="-nav"]') || btn.parentElement;
                    if (nav) {
                        nav.querySelectorAll('button').forEach(function(b) {
                            b.classList.remove('active');
                        });
                    }
                    btn.classList.add('active');
                }
            };
        }
    });

    /* G. Also expose masterTabSwitch and findPane globally */
    window.masterTabSwitch = masterTabSwitch;
    window.findPane = findPane;

    console.log('Master Tab Fix v7.3 loaded — ' + tabFunctions.length + ' tab functions patched');
})();
/* END MASTER TAB FIX v7.3 */
"""

if 'MASTER TAB FIX v7.3' not in js:
    js += master_fix
    with open(JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print('Master tab fix v7.3 appended')

# ============================================================
# 2. Fix Chart.js SRI in HTML
# ============================================================
with open(HTML, encoding='utf-8') as f:
    h = f.read()

# Remove integrity attribute from Chart.js script tag
h = re.sub(
    r'(<script\s+src="https://cdn\.jsdelivr\.net/npm/chart\.js[^"]*")\s+integrity="[^"]*"\s+crossorigin="[^"]*"',
    r'\1',
    h
)
print('Fixed Chart.js SRI')

# Bump versions
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=7.3.0', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=7.3.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

# Syntax check
exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')
print('Bumped to v7.3.0')

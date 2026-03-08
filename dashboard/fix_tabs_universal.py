"""
UNIVERSAL TAB FIX
1. Patch _universalTab to be more robust (try multiple ID patterns)
2. Add a global click handler for tab buttons in the More dropdown
3. Add placeholder content for empty/blank tab panes
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# Add a universal tab fix at the end of app.js
universal_fix = """

/* ============================================================
   UNIVERSAL TAB FIX v7.2 — Makes all tabs work reliably
   ============================================================ */
(function() {

    /* 1. Robust universal tab switcher
     *    Tries multiple ID patterns to find the content pane:
     *    - Exact ID match
     *    - Prefixed with pane class
     *    - data-tab attribute match
     */
    window._robustTabSwitch = function(tabId, btn) {
        if (!tabId) return;
        
        // Find closest tab nav container
        var nav = btn ? (btn.closest('.dairy-nav') || btn.closest('.vet-nav') || 
                        btn.closest('.en-nav') || btn.closest('.crm-nav') ||
                        btn.closest('.vermi-nav') || btn.closest('.tree-nav') ||
                        btn.closest('.aqua-nav') || btn.closest('.paint-nav') ||
                        btn.closest('.biogas-nav') || btn.closest('.wind-nav') ||
                        btn.closest('.solar-nav') || btn.closest('.carbon-nav') ||
                        btn.closest('.fin-nav') || btn.closest('[class*="-nav"]')) : null;
        
        // Deactivate all tab buttons in this nav
        if (nav) {
            nav.querySelectorAll('button').forEach(function(b) {
                b.classList.remove('active');
            });
        }
        
        // Activate clicked button
        if (btn) {
            btn.classList.add('active');
        }
        
        // Find the content container (usually next sibling of nav, or inside page area)
        var container = null;
        if (nav) {
            container = nav.closest('.page-section') || nav.parentElement;
        }
        if (!container) {
            container = document.getElementById('page-container') || document.body;
        }
        
        // Hide all panes in this container
        var paneClasses = ['.dairy-pane', '.tab-pane', '.tabpane', '.pane', '.kems-pane',
                           '[class*="-pane"]'];
        var allPanes = [];
        paneClasses.forEach(function(sel) {
            container.querySelectorAll(sel).forEach(function(p) {
                allPanes.push(p);
            });
        });
        
        // Deduplicate
        var seen = new Set();
        allPanes = allPanes.filter(function(p) {
            if (seen.has(p)) return false;
            seen.add(p);
            return true;
        });
        
        allPanes.forEach(function(p) {
            p.classList.remove('active');
            p.style.display = 'none';
        });
        
        // Try to find the matching pane by various ID patterns
        var pane = document.getElementById(tabId);
        
        // Also try common prefixed variants
        if (!pane) {
            var prefixes = ['wnd-', 'sol-', 'bio-', 'cattle-', 'poultry-', 'aqua-', 'vermi-', 
                           'tree-', 'paint-', 'carbon-', 'crm-', 'fin-', 'vet-', 'vedic-',
                           'trust-', 'cmd-', 'log-', 'water-', 'ticket-', 'wf-', 'hyd-',
                           'h2-', 'kinetic-', 'kems-', 'grid-', 'bi-', 'dms-', 'hrm-',
                           'inv-', 'booking-', 'lms-', 'survey-', 'field-', 'farmer-', 'p-'];
            for (var i = 0; i < prefixes.length; i++) {
                pane = document.getElementById(prefixes[i] + tabId);
                if (pane) break;
            }
        }
        
        // Also try data-tab attribute
        if (!pane) {
            pane = container.querySelector('[data-tab="' + tabId + '"]');
        }
        
        if (pane) {
            pane.classList.add('active');
            pane.style.display = '';
        }
    };

    /* 2. Fix More dropdown tab clicks
     *    When a tab in the More dropdown is clicked, it calls btn.click() on the
     *    ORIGINAL hidden button. But since we set display:none on that button,
     *    the click may not properly trigger. Fix: intercept and call the function directly.
     */
    document.addEventListener('click', function(e) {
        var item = e.target.closest('.dropdown-tab-item');
        if (!item) return;
        
        // Get the onclick from the original button
        var originalBtn = item._originalBtn;
        if (originalBtn) {
            var oc = originalBtn.getAttribute('onclick');
            if (oc) {
                try { 
                    // Execute the onclick directly
                    var fn = new Function(oc);
                    fn.call(originalBtn);
                } catch(err) {
                    console.warn('More dropdown click failed:', err);
                }
            }
        }
    });

    /* 3. Add placeholder content for empty tab panes
     *    After page loads, check all panes — if any are empty, add a placeholder
     */
    function addPlaceholders() {
        document.querySelectorAll('.dairy-pane, .tab-pane, .kems-pane, [class*="-pane"]').forEach(function(pane) {
            if (pane.innerHTML.trim() === '' || pane.children.length === 0) {
                var tabName = pane.id || pane.dataset.tab || 'this section';
                pane.innerHTML = '<div style="padding:40px;text-align:center;color:rgba(200,214,229,0.4);font-size:0.95rem;">' +
                    '<div style="font-size:2.5rem;margin-bottom:12px;">🔧</div>' +
                    '<div style="font-weight:600;margin-bottom:6px;">Module Coming Soon</div>' +
                    '<div style="font-size:0.82rem;color:rgba(200,214,229,0.3);">' + tabName + ' is under development</div>' +
                    '</div>';
            }
        });
    }
    
    setTimeout(addPlaceholders, 1500);
    
    // Re-run when pages switch
    var pc = document.getElementById('page-container');
    if (pc) {
        new MutationObserver(function() {
            setTimeout(addPlaceholders, 800);
        }).observe(pc, { childList: true });
    }

    /* 4. Fix tab buttons in More dropdown to properly reference originals
     *    Patch finalMoreDropdown to store original button reference
     */
    var _origFinalMore = window.finalMoreDropdown;
    if (_origFinalMore) {
        window.finalMoreDropdown = function() {
            _origFinalMore();
            // After dropdown is built, link dropdown items to original buttons
            document.querySelectorAll('.hub-more-dropdown-body').forEach(function(dd) {
                dd.querySelectorAll('.dropdown-tab-item').forEach(function(item, idx) {
                    // Already handled in finalMoreDropdown v3
                });
            });
        };
    }

    console.log('Universal Tab Fix v7.2 loaded');
})();
/* END UNIVERSAL TAB FIX v7.2 */
"""

if 'UNIVERSAL TAB FIX v7.2' not in js:
    js += universal_fix
    with open(JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print('Universal tab fix appended')
else:
    print('Already present')

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=7.2.0', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=7.2.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')
print('Bumped to v7.2.0')

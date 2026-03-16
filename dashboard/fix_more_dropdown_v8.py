"""
CLEAN MORE DROPDOWN REWRITE v8
- Removes ALL old More dropdown code (v3, FORCE_NO_SCROLL, old smartMoreDropdown)
- Replaces with one single clean implementation  
- Uses showPage hook + periodic check to guarantee execution on every page switch
- Handles inline overflow-x:auto removal
- Works on EVERY nav across ALL pages
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

original_len = len(js)

# ============================================================
# STEP 1: Remove ALL old More dropdown / overflow code blocks
# ============================================================
blocks_to_remove = [
    ('/* FINAL MORE DROPDOWN v3 */', '/* END FINAL MORE DROPDOWN v3 */'),
    ('/* FORCE_NO_SCROLL_FIX_v6_8', '/* END FORCE_NO_SCROLL_FIX_v6_8 */'),
    ('/* UNIVERSAL TAB FIX v7.2', '/* END UNIVERSAL TAB FIX v7.2 */'),
]

for start_marker, end_marker in blocks_to_remove:
    s = js.find(start_marker)
    e = js.find(end_marker)
    if s >= 0 and e >= 0:
        e += len(end_marker)
        js = js[:s] + js[e:]
        print(f"  Removed: {start_marker[:40]}...")

# Also remove the old disabled smartMoreDropdown if present
s = js.find('/* DISABLED */ function _old_smartMoreDropdown')
if s >= 0:
    # Find the closing of this block
    e = js.find('/* END _old_smartMoreDropdown */', s)
    if e < 0:
        # Try to find the next block marker
        e = js.find('\n/* ', s + 100)
    if e > s:
        js = js[:s] + js[e:]
        print("  Removed: _old_smartMoreDropdown")

# Remove inline overflow-x:auto from ALL nav divs
count = 0
for pattern in ['overflow-x: auto;', 'overflow-x:auto;']:
    while pattern in js:
        # Only replace in nav-related contexts
        idx = js.find(pattern)
        if idx >= 0:
            # Check context — within ~200 chars before, is there a "dairy-nav" or "nav" class?
            ctx = js[max(0, idx-200):idx]
            if 'nav' in ctx.lower() or 'dairy-nav' in ctx:
                js = js[:idx] + js[idx+len(pattern):]
                count += 1
            else:
                # Not a nav context, leave it but move past
                js = js[:idx] + 'overflow-x:hidden;' + js[idx+len(pattern):]
                count += 1

if count:
    print(f"  Fixed {count} inline overflow-x:auto")

print(f"  JS reduced from {original_len} to {len(js)} chars ({original_len - len(js)} removed)")

# ============================================================
# STEP 2: Add the new clean implementation
# ============================================================
new_more_dropdown = """

/* ============================================================
   MORE DROPDOWN v8 — Single clean implementation
   ============================================================ */
(function() {
    'use strict';
    
    var MAX_VISIBLE = 7;
    
    function applyMoreDropdown() {
        // Find ALL tab navs in the page
        var navs = document.querySelectorAll(
            '.dairy-nav, .vet-nav, .en-nav, .crm-nav, .vermi-nav, .tree-nav, ' +
            '.aqua-nav, .paint-nav, .biogas-nav, .wind-nav, .solar-nav, ' +
            '.carbon-nav, .fin-nav, .trust-nav, .cmd-nav, .log-nav, ' +
            '.water-nav, .vedic-nav, [class*="-nav"]'
        );
        
        navs.forEach(function(nav) {
            // Force no horizontal overflow
            nav.style.setProperty('overflow', 'hidden', 'important');
            nav.style.setProperty('overflow-x', 'hidden', 'important');
            nav.style.setProperty('display', 'flex', 'important');
            nav.style.setProperty('flex-wrap', 'nowrap', 'important');
            nav.style.setProperty('align-items', 'center', 'important');
            
            // Get all tab buttons (exclude More buttons and dropdown items)
            var allBtns = Array.from(nav.querySelectorAll('button')).filter(function(b) {
                return !b.classList.contains('hub-more-btn') && 
                       !b.classList.contains('dropdown-tab-item');
            });
            
            if (allBtns.length <= MAX_VISIBLE) {
                // Few enough tabs — show all, remove any existing More
                allBtns.forEach(function(b) { b.style.removeProperty('display'); });
                nav.querySelectorAll('.hub-more-btn').forEach(function(b) { b.remove(); });
                return;
            }
            
            // Already processed and nothing changed? Skip.
            if (nav._moreCount === allBtns.length) return;
            nav._moreCount = allBtns.length;
            
            // Remove any old More button and dropdown
            nav.querySelectorAll('.hub-more-btn').forEach(function(b) { b.remove(); });
            document.querySelectorAll('.hub-more-dropdown-body').forEach(function(d) {
                if (d._parentNav === nav) d.remove();
            });
            
            // Reset all buttons first
            allBtns.forEach(function(b) { b.style.removeProperty('display'); });
            
            // Calculate how many fit
            var navW = nav.offsetWidth || nav.clientWidth || 900;
            var moreW = 130;
            var available = navW - moreW - 20;
            var perTab = 120;
            var maxVis = Math.max(3, Math.min(MAX_VISIBLE, Math.floor(available / perTab)));
            
            var visible = allBtns.slice(0, maxVis);
            var hidden = allBtns.slice(maxVis);
            
            if (hidden.length === 0) return;
            
            // Hide overflow tabs
            hidden.forEach(function(btn) {
                btn.style.setProperty('display', 'none', 'important');
            });
            
            // Create More button
            var moreBtn = document.createElement('button');
            moreBtn.type = 'button';
            moreBtn.className = 'dairy-tab-btn hub-more-btn';
            moreBtn.style.cssText = 'white-space:nowrap;flex-shrink:0;margin-left:auto;';
            moreBtn.innerHTML = 'More &#9660; <span style="background:rgba(0,176,255,0.25);color:#42caff;padding:1px 7px;border-radius:99px;font-size:0.65rem;margin-left:5px;font-weight:700">' + hidden.length + '</span>';
            
            // Create dropdown on BODY to avoid clipping
            var dropdown = document.createElement('div');
            dropdown.className = 'hub-more-dropdown-body';
            dropdown._parentNav = nav;
            dropdown.style.cssText = 'position:fixed;display:none;flex-direction:column;gap:3px;min-width:220px;z-index:99999;background:rgba(18,28,50,0.98);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:6px;box-shadow:0 12px 48px rgba(0,0,0,0.7);max-height:350px;overflow-y:auto;backdrop-filter:blur(20px);';
            
            hidden.forEach(function(btn, i) {
                var item = document.createElement('button');
                item.type = 'button';
                item.className = 'dropdown-tab-item';
                item.innerHTML = btn.innerHTML;
                item.style.cssText = 'width:100%;justify-content:flex-start;border-radius:8px;padding:8px 14px;display:flex;align-items:center;gap:6px;background:transparent;border:1px solid transparent;color:rgba(200,214,229,0.75);font-size:0.78rem;cursor:pointer;transition:background 0.15s ease;text-align:left;white-space:nowrap;font-family:Inter,sans-serif;';
                item.onmouseenter = function() { item.style.background = 'rgba(255,255,255,0.06)'; item.style.color = '#e0eaf4'; };
                item.onmouseleave = function() { item.style.background = 'transparent'; item.style.color = 'rgba(200,214,229,0.75)'; };
                item.addEventListener('click', function(e) {
                    e.stopPropagation();
                    // Execute the original button's onclick
                    var onclick = btn.getAttribute('onclick');
                    if (onclick) {
                        try { new Function(onclick).call(btn); } catch(err) { btn.click(); }
                    } else {
                        btn.click();
                    }
                    dropdown.style.display = 'none';
                });
                dropdown.appendChild(item);
            });
            
            document.body.appendChild(dropdown);
            
            // Toggle dropdown
            moreBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                document.querySelectorAll('.hub-more-dropdown-body').forEach(function(d) {
                    if (d !== dropdown) d.style.display = 'none';
                });
                var isOpen = dropdown.style.display === 'flex';
                if (isOpen) {
                    dropdown.style.display = 'none';
                } else {
                    var rect = moreBtn.getBoundingClientRect();
                    dropdown.style.top = (rect.bottom + 4) + 'px';
                    dropdown.style.left = Math.max(10, rect.right - 240) + 'px';
                    dropdown.style.display = 'flex';
                }
            });
            
            // Append More button to nav
            nav.appendChild(moreBtn);
        });
    }
    
    // Close dropdowns on outside click
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.hub-more-btn') && !e.target.closest('.hub-more-dropdown-body')) {
            document.querySelectorAll('.hub-more-dropdown-body').forEach(function(d) {
                d.style.display = 'none';
            });
        }
    });
    
    // Hook into showPage to run after every page navigation
    function hookShowPage() {
        if (window._moreDropdownHooked) return;
        
        // Try to hook the showPage function
        if (typeof window.showPage === 'function') {
            var _origShowPage = window.showPage;
            window.showPage = function() {
                _origShowPage.apply(this, arguments);
                // Clean up old dropdowns and re-apply
                document.querySelectorAll('.hub-more-dropdown-body').forEach(function(d) { d.remove(); });
                // Reset ALL nav._moreCount so they get re-processed
                document.querySelectorAll('[class*="-nav"]').forEach(function(n) { delete n._moreCount; });
                setTimeout(applyMoreDropdown, 300);
                setTimeout(applyMoreDropdown, 800); // Double check
            };
            window._moreDropdownHooked = true;
            console.log('More Dropdown v8: Hooked into showPage');
        }
    }
    
    // Also watch for page-container mutations
    function watchPageContainer() {
        var pc = document.getElementById('page-container');
        if (pc && !pc._moreObserver) {
            pc._moreObserver = new MutationObserver(function() {
                // Clean old dropdowns
                document.querySelectorAll('.hub-more-dropdown-body').forEach(function(d) { d.remove(); });
                document.querySelectorAll('[class*="-nav"]').forEach(function(n) { delete n._moreCount; });
                setTimeout(applyMoreDropdown, 300);
            });
            pc._moreObserver.observe(pc, { childList: true });
            console.log('More Dropdown v8: Watching page-container');
        }
    }
    
    // Initial setup
    function init() {
        hookShowPage();
        watchPageContainer();
        applyMoreDropdown();
    }
    
    // Run at various stages to guarantee it works
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(init, 500);
            setTimeout(init, 1500);
        });
    } else {
        setTimeout(init, 300);
        setTimeout(init, 1000);
    }
    
    // Also run periodically for the first 10 seconds (catches late page loads)
    var checks = 0;
    var interval = setInterval(function() {
        init();
        if (++checks >= 5) clearInterval(interval);
    }, 2000);
    
    window.applyMoreDropdown = applyMoreDropdown;
    console.log('More Dropdown v8 loaded');
})();
/* END MORE DROPDOWN v8 */
"""

js += new_more_dropdown

# Save
with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

# Bump versions
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=8.0.0', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=8.0.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

# Syntax check
exit_code = os.system(f'node --check "{JS}" 2>&1')
print(f'SYNTAX: {"OK" if exit_code == 0 else "ERROR"}')
print(f'Version: 8.0.0')

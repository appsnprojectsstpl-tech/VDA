"""
Fix the More dropdown visibility issue:
- The problem: On pages with many tabs, even 7 visible tabs + More button 
  exceed the nav width, so the More button gets clipped by overflow:hidden.
- The fix: Reduce MAX_VISIBLE to 5, and use a smarter approach where
  the More button is placed FIRST (position: sticky/absolute right) so
  it's always visible, or we dynamically calculate how many tabs fit.
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# Replace the existing applyMoreDropdown with a better version
# that uses dynamic width calculation

new_more_fn = """

/* ============================================================
   SMART MORE DROPDOWN v2 — Always visible, dynamic tab count
   ============================================================ */
(function() {
    function smartMoreDropdown() {
        var navSelectors = '.dairy-nav,.vet-nav,.en-nav,.crm-nav,.vermi-nav,.tree-nav,.aqua-nav,.paint-nav,.biogas-nav,.wind-nav,.solar-nav,.carbon-nav,.fin-nav';
        document.querySelectorAll(navSelectors).forEach(function(nav) {
            if (nav.dataset.smartMore === '1') return;
            
            var allBtns = Array.from(nav.querySelectorAll('button:not(.hub-more-btn)'));
            if (allBtns.length <= 5) return;
            
            nav.dataset.smartMore = '1';
            
            // Remove any OLD More containers first
            nav.querySelectorAll('.hub-more-container').forEach(function(c) { c.remove(); });
            
            // Calculate how many tabs can fit
            var navWidth = nav.offsetWidth || nav.clientWidth || 800;
            var moreBtnWidth = 110; // reserve space for More button
            var availableWidth = navWidth - moreBtnWidth - 40; // 40px for padding
            var avgBtnWidth = 120; // approximate tab button width
            var maxVisible = Math.max(3, Math.min(7, Math.floor(availableWidth / avgBtnWidth)));
            
            var visibleBtns = allBtns.slice(0, maxVisible);
            var hiddenBtns = allBtns.slice(maxVisible);
            
            if (hiddenBtns.length === 0) return;
            
            // Hide overflow tabs
            hiddenBtns.forEach(function(btn) {
                btn.style.display = 'none';
            });
            
            // Create More button (positioned within nav, not after all buttons)
            var moreWrap = document.createElement('div');
            moreWrap.className = 'hub-more-container';
            moreWrap.style.cssText = 'position:relative;display:inline-flex;flex-shrink:0;z-index:100;margin-left:auto;';
            
            var moreBtn = document.createElement('button');
            moreBtn.type = 'button';
            moreBtn.className = 'dairy-tab-btn hub-more-btn';
            moreBtn.style.cssText = 'white-space:nowrap;flex-shrink:0;';
            moreBtn.innerHTML = 'More \\u25BC <span style="background:rgba(0,176,255,0.25);color:#42caff;padding:1px 7px;border-radius:99px;font-size:0.65rem;margin-left:5px;font-weight:700">' + hiddenBtns.length + '</span>';
            
            var dropdown = document.createElement('div');
            dropdown.className = 'hub-more-dropdown';
            dropdown.style.cssText = 'position:absolute;top:calc(100% + 6px);right:0;background:rgba(18,28,50,0.98);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:6px;display:none;flex-direction:column;gap:3px;min-width:220px;z-index:9000;box-shadow:0 12px 48px rgba(0,0,0,0.6);max-height:350px;overflow-y:auto;backdrop-filter:blur(20px);';
            
            hiddenBtns.forEach(function(btn) {
                var item = document.createElement('button');
                item.type = 'button';
                item.className = btn.className;
                item.innerHTML = btn.innerHTML;
                item.style.cssText = 'width:100%;justify-content:flex-start;border-radius:8px;padding:8px 14px;display:flex;align-items:center;gap:6px;background:transparent;border:1px solid transparent;color:rgba(200,214,229,0.75);font-size:0.78rem;cursor:pointer;transition:all 0.15s ease;text-align:left;white-space:nowrap;';
                
                // Hover effect
                item.onmouseenter = function() { item.style.background = 'rgba(255,255,255,0.06)'; item.style.color = '#e0eaf4'; };
                item.onmouseleave = function() { item.style.background = 'transparent'; item.style.color = 'rgba(200,214,229,0.75)'; };
                
                item.addEventListener('click', function(e) {
                    e.stopPropagation();
                    btn.click(); // Trigger the original hidden button
                    dropdown.style.display = 'none';
                    
                    // Update active state visual on the More button
                    moreBtn.innerHTML = '\\u2713 ' + (btn.textContent || '').trim() + ' \\u25BC <span style=\"background:rgba(0,176,255,0.25);color:#42caff;padding:1px 7px;border-radius:99px;font-size:0.65rem;margin-left:5px;font-weight:700\">' + hiddenBtns.length + '</span>';
                });
                dropdown.appendChild(item);
            });
            
            // Toggle dropdown
            moreBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                var isOpen = dropdown.style.display === 'flex';
                // Close all other dropdowns first
                document.querySelectorAll('.hub-more-dropdown').forEach(function(d) { d.style.display = 'none'; });
                dropdown.style.display = isOpen ? 'none' : 'flex';
            });
            
            // Close on outside click
            document.addEventListener('click', function(e) {
                if (!moreWrap.contains(e.target)) {
                    dropdown.style.display = 'none';
                }
            });
            
            moreWrap.appendChild(moreBtn);
            moreWrap.appendChild(dropdown);
            
            // Insert MORE button right after the last visible button
            var lastVisible = visibleBtns[visibleBtns.length - 1];
            if (lastVisible && lastVisible.nextSibling) {
                nav.insertBefore(moreWrap, lastVisible.nextSibling);
            } else {
                nav.appendChild(moreWrap);
            }
        });
    }
    
    window.smartMoreDropdown = smartMoreDropdown;
    
    // Run after DOM is ready and pages load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() { setTimeout(smartMoreDropdown, 600); });
    } else {
        setTimeout(smartMoreDropdown, 600);
    }
    
    // Re-run when page container changes (page switches)
    var pc = document.getElementById('page-container');
    if (pc) {
        new MutationObserver(function() {
            setTimeout(smartMoreDropdown, 400);
        }).observe(pc, { childList: true });
    }
})();
/* END SMART MORE DROPDOWN v2 */
"""

# Disable old applyMoreDropdown
if 'function applyMoreDropdown' in js and 'SMART MORE DROPDOWN v2' not in js:
    # Comment out the old one
    js = js.replace('function applyMoreDropdown()', '/* DISABLED */ function _old_applyMoreDropdown()')
    js = js.replace('window.applyMoreDropdown = applyMoreDropdown', '// window.applyMoreDropdown = _old_applyMoreDropdown')
    js = js.replace("setTimeout(applyMoreDropdown, 600)", "// setTimeout(applyMoreDropdown, 600) // disabled")
    js = js.replace("setTimeout(applyMoreDropdown, 300)", "// setTimeout(applyMoreDropdown, 300) // disabled")
    print('Disabled old applyMoreDropdown')

# Append new version
if 'SMART MORE DROPDOWN v2' not in js:
    js += new_more_fn
    print('Added smartMoreDropdown v2')

# Write
with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=6.9.0', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=6.9.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

# Syntax check
exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')
print('Bumped to v6.9.0')

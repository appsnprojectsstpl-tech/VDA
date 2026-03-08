"""
Final fix for More dropdown:
1. Remove old SMART MORE DROPDOWN v2 
2. Add new version that appends dropdown to document.body (not inside nav)
3. Ensure hidden tabs get display:none
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# Disable old smartMoreDropdown v2
if 'function smartMoreDropdown()' in js:
    js = js.replace('function smartMoreDropdown()', '/* DISABLED */ function _old_smartMoreDropdown()')
    js = js.replace('window.smartMoreDropdown = smartMoreDropdown', '// disabled')
    js = js.replace('setTimeout(smartMoreDropdown, 600)', '// disabled2')
    js = js.replace('setTimeout(smartMoreDropdown, 400)', '// disabled3')
    print('Disabled old smartMoreDropdown v2')

new_code = """

/* ============================================================
   FINAL MORE DROPDOWN v3 — Dropdown on document.body, tabs hidden
   ============================================================ */
(function() {
    function finalMoreDropdown() {
        var navSelectors = '.dairy-nav,.vet-nav,.en-nav,.crm-nav,.vermi-nav,.tree-nav,.aqua-nav,.paint-nav,.biogas-nav,.wind-nav,.solar-nav,.carbon-nav,.fin-nav';
        document.querySelectorAll(navSelectors).forEach(function(nav) {
            if (nav.dataset.finalMore === 'done') return;

            var allBtns = Array.from(nav.querySelectorAll('button:not(.hub-more-btn)'));
            if (allBtns.length <= 5) return;

            nav.dataset.finalMore = 'done';

            // Remove any existing More containers inside nav
            nav.querySelectorAll('.hub-more-container').forEach(function(c) { c.remove(); });

            // Calculate how many tabs fit
            var navW = nav.clientWidth || 800;
            var reserveForMore = 130;
            var available = navW - reserveForMore - 32;
            var perTab = 115;
            var maxVis = Math.max(3, Math.min(7, Math.floor(available / perTab)));

            var visibleBtns = allBtns.slice(0, maxVis);
            var hiddenBtns = allBtns.slice(maxVis);
            if (hiddenBtns.length === 0) return;

            // HIDE overflow tabs
            hiddenBtns.forEach(function(btn) {
                btn.style.setProperty('display', 'none', 'important');
            });

            // Create More button INSIDE the nav
            var moreBtn = document.createElement('button');
            moreBtn.type = 'button';
            moreBtn.className = 'dairy-tab-btn hub-more-btn';
            moreBtn.style.cssText = 'white-space:nowrap;flex-shrink:0;margin-left:auto;';
            moreBtn.innerHTML = 'More \\u25BC <span style=\"background:rgba(0,176,255,0.25);color:#42caff;padding:1px 7px;border-radius:99px;font-size:0.65rem;margin-left:5px;font-weight:700\">' + hiddenBtns.length + '</span>';

            // Create dropdown on BODY (not inside nav — avoids overflow:hidden clipping)
            var dropdown = document.createElement('div');
            dropdown.className = 'hub-more-dropdown-body';
            dropdown.style.cssText = 'position:fixed;display:none;flex-direction:column;gap:3px;min-width:220px;z-index:99999;background:rgba(18,28,50,0.98);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:6px;box-shadow:0 12px 48px rgba(0,0,0,0.7);max-height:350px;overflow-y:auto;backdrop-filter:blur(20px);';

            hiddenBtns.forEach(function(btn) {
                var item = document.createElement('button');
                item.type = 'button';
                item.className = 'dropdown-tab-item';
                item.innerHTML = btn.innerHTML;
                item.style.cssText = 'width:100%;justify-content:flex-start;border-radius:8px;padding:8px 14px;display:flex;align-items:center;gap:6px;background:transparent;border:1px solid transparent;color:rgba(200,214,229,0.75);font-size:0.78rem;cursor:pointer;transition:background 0.15s ease;text-align:left;white-space:nowrap;font-family:Inter,sans-serif;';
                item.onmouseenter = function() { item.style.background = 'rgba(255,255,255,0.06)'; item.style.color = '#e0eaf4'; };
                item.onmouseleave = function() { item.style.background = 'transparent'; item.style.color = 'rgba(200,214,229,0.75)'; };
                item.addEventListener('click', function(e) {
                    e.stopPropagation();
                    btn.click();
                    dropdown.style.display = 'none';
                });
                dropdown.appendChild(item);
            });

            document.body.appendChild(dropdown);

            // Position dropdown below the More button
            moreBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                // Close all other dropdowns
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

            // Close on outside click
            document.addEventListener('click', function(e) {
                if (!moreBtn.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.style.display = 'none';
                }
            });

            // Insert More button right after last visible tab
            var lastVis = visibleBtns[visibleBtns.length - 1];
            if (lastVis && lastVis.nextSibling) {
                nav.insertBefore(moreBtn, lastVis.nextSibling);
            } else {
                nav.appendChild(moreBtn);
            }
        });
    }

    // Run after DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() { setTimeout(finalMoreDropdown, 700); });
    } else {
        setTimeout(finalMoreDropdown, 700);
    }

    // Re-run on page switches
    var pc = document.getElementById('page-container');
    if (pc) {
        new MutationObserver(function() {
            setTimeout(finalMoreDropdown, 500);
        }).observe(pc, { childList: true });
    }

    window.finalMoreDropdown = finalMoreDropdown;
})();
/* END FINAL MORE DROPDOWN v3 */
"""

if 'FINAL MORE DROPDOWN v3' not in js:
    js += new_code
    print('Added finalMoreDropdown v3')

with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=7.0.0', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=7.0.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')
print('Bumped to v7.0.0')

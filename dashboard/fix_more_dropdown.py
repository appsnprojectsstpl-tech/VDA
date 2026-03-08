"""
Clean fix for More dropdown:
1. Disable the TWO old More dropdown implementations (L14531-14758)
2. Keep only the newest one (L19956) 
3. Fix dropdown z-index
4. Force overflow:hidden on all navs via JS runtime (since CSS cascade keeps losing)
"""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
CSS = r'e:\Vedavathi\dashboard\index.css'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

changes = 0

# 1. Disable old setupHubMoreDropdown by wrapping it
# Find the function block starting with "const HUB_TAB_LIMIT"
# and comment out everything until applyAllHubMoreDropdowns
if 'HUB_TAB_LIMIT = 6' in js and '/* OLD_MORE_DISABLED' not in js:
    # Find the start
    start = js.find('const HUB_TAB_LIMIT = 6')
    # Find the end (window.applyAllHubMoreDropdowns = ...)
    end = js.find('window.applyAllHubMoreDropdowns = applyAllHubMoreDropdowns;')
    if start > 0 and end > start:
        end = js.find(';', end) + 1
        old_block = js[start:end]
        # Replace with a disabled version
        js = js[:start] + '/* OLD_MORE_DISABLED */\n// Original More dropdown disabled — replaced by v6.7 implementation\n' + js[end:]
        changes += 1
        print(f'Disabled old More dropdown (chars {start}-{end})')

# 2. Also disable the second old implementation (setupHubMoreDropdown function)
if 'function setupHubMoreDropdown(navEl)' in js:
    idx = js.find('function setupHubMoreDropdown(navEl)')
    # Find the end of this function
    # Look for the closing brace at the right depth
    brace_count = 0
    end = idx
    started = False
    for i in range(idx, min(idx + 5000, len(js))):
        if js[i] == '{':
            brace_count += 1
            started = True
        elif js[i] == '}':
            brace_count -= 1
            if started and brace_count == 0:
                end = i + 1
                break
    if end > idx and '/* OLD_MORE2_DISABLED' not in js[idx-30:idx]:
        js = js[:idx] + '/* OLD_MORE2_DISABLED */\n' + js[end:]
        changes += 1
        print(f'Disabled second old setupHubMoreDropdown')

# 3. Disable the old applyAllHubMoreDropdowns calls
if 'applyAllHubMoreDropdowns' in js:
    # Replace all calls and timeouts
    js = js.replace('setTimeout(applyAllHubMoreDropdowns, 200);', '// setTimeout(applyAllHubMoreDropdowns, 200); // disabled')
    js = js.replace('window.applyAllHubMoreDropdowns = applyAllHubMoreDropdowns;', '// window.applyAllHubMoreDropdowns = applyAllHubMoreDropdowns; // disabled')
    changes += 1
    print('Disabled applyAllHubMoreDropdowns calls')

# 4. Add JS runtime fix at the very end to:
#    - Force overflow:hidden on all navs (CSS cascade keeps losing)
#    - Fix More dropdown z-index
#    - Remove any old duplicate More buttons

runtime_fix = '''

/* ============================================================
   RUNTIME FIX — Force no-scroll + fix More dropdown (v6.8.1)
   ============================================================ */
document.addEventListener('DOMContentLoaded', function() {
    // Give a moment for page to render
    setTimeout(function() {
        // 1. Force overflow:hidden on ALL navs (CSS cascade fix)
        var navSelectors = '.dairy-nav,.vet-nav,.en-nav,.crm-nav,.vermi-nav,.tree-nav,.aqua-nav,.paint-nav,.biogas-nav,.wind-nav,.solar-nav,.carbon-nav,.fin-nav,.trust-nav,.cmd-nav,.log-nav,.water-nav,.vedic-nav,.agri-nav';
        document.querySelectorAll(navSelectors).forEach(function(nav) {
            nav.style.overflowX = 'hidden';
            nav.style.overflowY = 'hidden';
            nav.style.overflow = 'hidden';
            nav.style.flexWrap = 'nowrap';
            nav.style.maxWidth = '100%';
        });

        // 2. Remove OLD duplicate More buttons (keep only newest per nav)
        document.querySelectorAll(navSelectors).forEach(function(nav) {
            var moreBtns = nav.querySelectorAll('.hub-more-btn, .hub-more-container');
            if (moreBtns.length > 1) {
                // Keep only the last one, remove earlier duplicates
                for (var i = 0; i < moreBtns.length - 1; i++) {
                    moreBtns[i].remove();
                }
            }
        });

        // 3. Fix z-index on all More dropdowns so they appear ABOVE content
        document.querySelectorAll('.hub-more-dropdown').forEach(function(dd) {
            dd.style.zIndex = '9000';
        });
        document.querySelectorAll('.hub-more-container').forEach(function(c) {
            c.style.zIndex = '100';
        });

    }, 800);

    // Re-apply when pages switch
    var pc = document.getElementById('page-container');
    if (pc) {
        new MutationObserver(function() {
            setTimeout(function() {
                var navSelectors = '.dairy-nav,.vet-nav,.en-nav,.crm-nav,.vermi-nav,.tree-nav,.aqua-nav,.paint-nav,.biogas-nav,.wind-nav,.solar-nav,.carbon-nav';
                document.querySelectorAll(navSelectors).forEach(function(nav) {
                    nav.style.overflowX = 'hidden';
                    nav.style.overflow = 'hidden';
                    nav.style.flexWrap = 'nowrap';
                    nav.style.maxWidth = '100%';
                    // Remove duplicate more buttons
                    var moreBtns = nav.querySelectorAll('.hub-more-btn, .hub-more-container');
                    if (moreBtns.length > 1) {
                        for (var i = 0; i < moreBtns.length - 1; i++) {
                            moreBtns[i].remove();
                        }
                    }
                    // Fix z-index
                    nav.querySelectorAll('.hub-more-dropdown').forEach(function(dd) {
                        dd.style.zIndex = '9000';
                    });
                });
            }, 400);
        }).observe(pc, { childList: true });
    }
});

/* END RUNTIME FIX v6.8.1 */
'''

if 'RUNTIME FIX' not in js:
    js += runtime_fix
    changes += 1
    print('Added runtime fix for overflow + z-index + duplicate removal')

# Write back
with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'\nTotal changes: {changes}')

# Bump 
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=6.8.1', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=6.8.1', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

# Syntax check
import os
print('\nSyntax check...')
exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')
print('Bumped to v6.8.1')

import re, os, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

marker = 'FORCE_NO_SCROLL_FIX_v6_8'
if marker not in js:
    fix = """

/* ============================================================
   FORCE_NO_SCROLL_FIX_v6_8 - Runtime overflow + z-index fix
   ============================================================ */
document.addEventListener('DOMContentLoaded', function() {
    function forceNoScroll() {
        var sels = '.dairy-nav,.vet-nav,.en-nav,.crm-nav,.vermi-nav,.tree-nav,.aqua-nav,.paint-nav,.biogas-nav,.wind-nav,.solar-nav,.carbon-nav,.fin-nav,.trust-nav,.cmd-nav,.log-nav,.water-nav,.vedic-nav,.agri-nav';
        document.querySelectorAll(sels).forEach(function(nav) {
            nav.style.setProperty('overflow-x', 'hidden', 'important');
            nav.style.setProperty('overflow', 'hidden', 'important');
            nav.style.setProperty('flex-wrap', 'nowrap', 'important');
            nav.style.setProperty('max-width', '100%', 'important');
            var moreContainers = nav.querySelectorAll('.hub-more-container');
            if (moreContainers.length > 1) {
                for (var i = 0; i < moreContainers.length - 1; i++) moreContainers[i].remove();
            }
            nav.querySelectorAll('.hub-more-dropdown').forEach(function(dd) {
                dd.style.setProperty('z-index', '9000', 'important');
            });
            nav.querySelectorAll('.hub-more-container').forEach(function(c) {
                c.style.setProperty('z-index', '100', 'important');
                c.style.setProperty('position', 'relative', 'important');
            });
        });
    }
    setTimeout(forceNoScroll, 500);
    setTimeout(forceNoScroll, 2000);
    var pc = document.getElementById('page-container');
    if (pc) {
        new MutationObserver(function() {
            setTimeout(forceNoScroll, 300);
        }).observe(pc, { childList: true });
    }
});
/* END FORCE_NO_SCROLL_FIX_v6_8 */
"""
    with open(JS, 'a', encoding='utf-8') as f:
        f.write(fix)
    print('Appended force-no-scroll fix')
else:
    print('Already present')

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=6.8.2', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=6.8.2', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)
print('Bumped to v6.8.2')

exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')

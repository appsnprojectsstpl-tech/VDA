"""
COMPLETE UI/UX AUDIT — Entire Vedavathi Dashboard
Scans: app.js (pages HTML + JS functions), index.css, index.html
Output: Categorized report to uiux_full_audit_report.txt
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'e:\Vedavathi\dashboard'
JS = os.path.join(BASE, 'app.js')
CSS = os.path.join(BASE, 'index.css')
HTML = os.path.join(BASE, 'index.html')
OUT = os.path.join(BASE, 'uiux_full_audit_report.txt')

with open(JS, encoding='utf-8', errors='replace') as f: js = f.read()
with open(CSS, encoding='utf-8', errors='replace') as f: css = f.read()
with open(HTML, encoding='utf-8', errors='replace') as f: html = f.read()

R = []  # report lines

def section(title):
    R.append('')
    R.append('=' * 70)
    R.append(f'  {title}')
    R.append('=' * 70)

def issue(severity, category, msg):
    R.append(f'  [{severity}] [{category}] {msg}')

# ============================================================
# 1. EXTRACT ALL PAGES FROM app.js
# ============================================================
section('1. PAGE EXTRACTION')

pages_match = re.search(r'(?:const|var|let)\s+pages\s*=\s*\{(.*?)\n\};', js, re.DOTALL)
pages_content = pages_match.group(1) if pages_match else ''

# Find individual page blocks
page_pattern = re.compile(r'^\s{2,6}(\w+):\s*`(.*?)`\s*[,}]', re.DOTALL | re.MULTILINE)
pages = {}
for m in page_pattern.finditer(pages_content):
    pages[m.group(1)] = m.group(2)

R.append(f'  Found {len(pages)} pages: {sorted(pages.keys())}')

# ============================================================
# 2. PER-PAGE AUDIT
# ============================================================
section('2. PER-PAGE AUDIT')

all_issues = {}

for key, pg_html in sorted(pages.items()):
    issues = []

    # --- TAB OVERFLOW ---
    tab_btns = (
        len(re.findall(r'dairy-tab-btn', pg_html)) +
        len(re.findall(r'vet-tab-btn', pg_html)) +
        len(re.findall(r'en-tbtn', pg_html)) +
        len(re.findall(r'crm-tab-btn', pg_html)) +
        len(re.findall(r'vermi-tbtn', pg_html)) +
        len(re.findall(r'tree-tbtn', pg_html)) +
        len(re.findall(r'carbon-tab-btn', pg_html)) +
        len(re.findall(r'paint-tab-btn', pg_html)) +
        len(re.findall(r'solar-tab-btn', pg_html)) +
        len(re.findall(r'hub-more-btn', pg_html))
    )
    if tab_btns >= 12:
        issues.append(('CRITICAL', 'TAB_OVERFLOW', f'{tab_btns} tab buttons - will clip on small screens'))
    elif tab_btns >= 8:
        issues.append(('HIGH', 'TAB_OVERFLOW', f'{tab_btns} tab buttons - may overflow'))

    # --- NAV CLASSES USED ---
    nav_classes = set(re.findall(r'class="([a-zA-Z0-9_-]+-nav)"', pg_html))
    for nc in nav_classes:
        if not re.search(r'\.' + re.escape(nc) + r'\s*[,{]', css):
            issues.append(('HIGH', 'MISSING_CSS', f'.{nc} has NO CSS rule'))

    # --- STUCK LOADING TEXT ---
    loadings = set(re.findall(r'Loading [^<]{2,60}\.\.\.', pg_html))
    for l in loadings:
        issues.append(('MEDIUM', 'STUCK_LOADING', f'"{l}" - no timeout/fallback'))

    # --- BUTTONS WITHOUT type= ---
    btns_no_type = re.findall(r'<button(?![^>]*type=)[^>]*>', pg_html)
    if btns_no_type:
        issues.append(('LOW', 'BTN_NO_TYPE', f'{len(btns_no_type)} buttons missing type= attribute'))

    # --- CLICKABLE ELEMENTS WITHOUT cursor:pointer ---
    onclick_els = re.findall(r'<(?:div|span|td|tr|li)[^>]+onclick[^>]+>', pg_html)
    no_cursor = [d for d in onclick_els if 'cursor' not in d]
    if no_cursor:
        issues.append(('HIGH', 'NO_CURSOR', f'{len(no_cursor)} clickable elements missing cursor:pointer'))

    # --- INPUTS WITHOUT id/aria-label ---
    inputs = re.findall(r'<input[^>]*>', pg_html)
    unlabelled = [i for i in inputs
                  if 'id=' not in i and 'aria-label' not in i
                  and 'type="hidden"' not in i and "type='hidden'" not in i]
    if unlabelled:
        issues.append(('MEDIUM', 'A11Y_INPUT', f'{len(unlabelled)} inputs without id or aria-label'))

    # --- SELECTS WITHOUT id ---
    selects = re.findall(r'<select[^>]*>', pg_html)
    no_id_sel = [s for s in selects if 'id=' not in s]
    if no_id_sel:
        issues.append(('MEDIUM', 'A11Y_SELECT', f'{len(no_id_sel)} selects without id'))

    # --- EMPTY STATE HANDLING ---
    has_table = '<table' in pg_html or '<tbody' in pg_html
    has_empty = any(x in pg_html.lower() for x in ['no data', 'no records', 'empty-state', 'no items'])
    if has_table and not has_empty:
        issues.append(('MEDIUM', 'NO_EMPTY_STATE', 'Tables with no empty-state fallback'))

    # --- LONG INLINE STYLES ---
    long_inline = re.findall(r'style="[^"]{80,}"', pg_html)
    if len(long_inline) > 10:
        issues.append(('LOW', 'INLINE_STYLE', f'{len(long_inline)} long inline style attrs (should be CSS classes)'))

    # --- HEADING OVERUSE ---
    h_tags = re.findall(r'<h[23][^>]*>', pg_html)
    if len(h_tags) > 15:
        issues.append(('LOW', 'HEADING_CLUTTER', f'{len(h_tags)} h2/h3 headings in one page'))

    # --- FORM WITHOUT LABELS ---
    form_rows = re.findall(r'<div[^>]*form[^>]*>(.*?)</div>', pg_html, re.DOTALL)
    for row in form_rows:
        if '<input' in row and '<label' not in row:
            issues.append(('MEDIUM', 'FORM_NO_LABEL', 'Form row has input without <label>'))
            break

    # --- IMAGE ALT TEXT ---
    imgs = re.findall(r'<img[^>]*>', pg_html)
    no_alt = [i for i in imgs if 'alt=' not in i]
    if no_alt:
        issues.append(('MEDIUM', 'A11Y_IMG', f'{len(no_alt)} images without alt text'))

    # --- BROKEN onclick REFERENCES ---
    onclick_fns = re.findall(r'onclick="(\w+)\(', pg_html)
    for fn in set(onclick_fns):
        # Check if function is defined or exposed to window
        if f'function {fn}' not in js and f'window.{fn}' not in js and f'{fn} =' not in js:
            issues.append(('CRITICAL', 'BROKEN_FN', f'onclick calls {fn}() but function not found in app.js'))

    if issues:
        all_issues[key] = issues
        R.append(f'\n--- PAGE: {key.upper()} ({len(issues)} issues) ---')
        for sev, cat, msg in issues:
            R.append(f'  [{sev}] [{cat}] {msg}')

# ============================================================
# 3. INDEX.HTML AUDIT
# ============================================================
section('3. INDEX.HTML AUDIT')

# Meta tags
if '<meta name="description"' not in html:
    issue('MEDIUM', 'SEO', 'Missing meta description')
if '<meta name="viewport"' not in html:
    issue('CRITICAL', 'RESPONSIVE', 'Missing viewport meta tag')
else:
    issue('OK', 'RESPONSIVE', 'Viewport meta present')

# Lang attribute
if 'lang=' not in html[:200]:
    issue('MEDIUM', 'A11Y', '<html> missing lang attribute')

# Favicon
if 'favicon' not in html and 'icon' not in html[:500]:
    issue('LOW', 'UX', 'No favicon defined')

# Script loading
script_tags = re.findall(r'<script[^>]*>', html)
defer_count = sum(1 for s in script_tags if 'defer' in s or 'async' in s)
R.append(f'  Scripts: {len(script_tags)} total, {defer_count} with defer/async')

# CSS version
css_ver = re.search(r'index\.css\?v=([\d.]+)', html)
if css_ver:
    R.append(f'  CSS version: {css_ver.group(1)}')
js_ver = re.search(r'app\.js\?v=([\d.]+)', html)
if js_ver:
    R.append(f'  JS version: {js_ver.group(1)}')

# ============================================================
# 4. CSS AUDIT
# ============================================================
section('4. CSS AUDIT')

css_lines = css.split('\n')
R.append(f'  Total CSS lines: {len(css_lines)}')

# Duplicate rule blocks
rule_counts = {}
for m in re.finditer(r'(\.[\w-]+)\s*\{', css):
    sel = m.group(1)
    rule_counts[sel] = rule_counts.get(sel, 0) + 1

duplicates = {k: v for k, v in rule_counts.items() if v >= 4}
if duplicates:
    issue('HIGH', 'CSS_DUPLICATION', f'{len(duplicates)} selectors defined 4+ times:')
    for sel, count in sorted(duplicates.items(), key=lambda x: -x[1])[:15]:
        R.append(f'    {sel}: {count} times')

# !important overuse
important_count = css.count('!important')
R.append(f'  !important usage: {important_count} occurrences')
if important_count > 200:
    issue('HIGH', 'CSS_SPECIFICITY', f'{important_count} !important declarations - specificity war')

# Missing key CSS classes
missing_css = []
for cls in ['.form-control', '.empty-state', '.loading-state', '.error-state',
            '.skeleton', '.tooltip', '.dropdown-menu']:
    if cls + ' ' not in css and cls + '{' not in css and cls + ',' not in css:
        missing_css.append(cls)
if missing_css:
    issue('MEDIUM', 'MISSING_CSS', f'Missing utility classes: {missing_css}')

# overflow:hidden on nav containers (THE CRITICAL BUG)
for m in re.finditer(r'overflow\s*:\s*hidden\s*!important', css):
    ctx_start = max(0, m.start() - 300)
    ctx = css[ctx_start:m.end()]
    if any(x in ctx.lower() for x in ['dairy-nav', 'vet-nav', 'en-nav', 'nav {']):
        line_no = css[:m.start()].count('\n') + 1
        issue('CRITICAL', 'TAB_OVERFLOW_CSS', f'overflow:hidden!important at L{line_no} may clip tab navs')

# Check nav scroll fix is present at end of file
last_2000 = css[-2000:]
if 'overflow-x: auto' in last_2000 and 'dairy-nav' in last_2000:
    R.append('  [OK] Tab overflow-x:auto fix present at end of CSS')
else:
    issue('CRITICAL', 'TAB_FIX_MISSING', 'No overflow-x:auto fix found at end of CSS for dairy-nav')

# Check parent constraint fix
if 'max-width: 100%' in last_2000 and 'page-container' in last_2000:
    R.append('  [OK] Parent constraint fix for page-container present')
else:
    issue('CRITICAL', 'PARENT_FIX_MISSING', 'Parent width constraint fix missing for #page-container')

# ============================================================
# 5. JAVASCRIPT FUNCTION AUDIT
# ============================================================
section('5. JAVASCRIPT FUNCTION AUDIT')

# Find all window-exposed functions
window_fns = set(re.findall(r'window\.(\w+)\s*=', js))
R.append(f'  Window-exposed functions: {len(window_fns)}')

# Find all onclick references in pages HTML
onclick_fns_all = set()
for pg_html in pages.values():
    onclick_fns_all.update(re.findall(r'onclick="(\w+)\(', pg_html))

# Also check index.html
onclick_fns_all.update(re.findall(r'onclick="(\w+)\(', html))

# Check which onclick fns are NOT in window scope or defined
missing_fns = []
for fn in sorted(onclick_fns_all):
    if fn not in window_fns and f'function {fn}' not in js:
        missing_fns.append(fn)

if missing_fns:
    issue('CRITICAL', 'BROKEN_ONCLICK', f'{len(missing_fns)} onclick functions not found/exposed:')
    for fn in missing_fns[:20]:
        R.append(f'    {fn}()')
else:
    R.append(f'  [OK] All {len(onclick_fns_all)} onclick functions are defined or window-exposed')

# Tab switcher functions
tab_fns = set(re.findall(r'onclick="(\w+Tab)\(', js))
R.append(f'  Tab switcher functions called: {sorted(tab_fns)}')
for fn in tab_fns:
    if f'function {fn}' not in js and f'window.{fn}' not in js and f'{fn} =' not in js:
        issue('HIGH', 'MISSING_TAB_FN', f'{fn}() called in onclick but not defined')

# ============================================================
# 6. ACCESSIBILITY AUDIT
# ============================================================
section('6. ACCESSIBILITY AUDIT')

# Focus styles
if ':focus-visible' in css or ':focus' in css:
    R.append('  [OK] Focus styles defined in CSS')
else:
    issue('CRITICAL', 'A11Y', 'No :focus or :focus-visible styles in CSS')

# Skip link
if 'skip' in html.lower() and 'main' in html.lower():
    R.append('  [OK] Skip-to-main link present')
else:
    issue('LOW', 'A11Y', 'No skip-to-main-content link in index.html')

# ARIA landmarks
if 'role="navigation"' in html or '<nav' in html:
    R.append('  [OK] Navigation landmark present')
else:
    issue('MEDIUM', 'A11Y', 'No <nav> or role=navigation landmark')

if 'role="main"' in html or '<main' in html:
    R.append('  [OK] Main landmark present')
else:
    issue('MEDIUM', 'A11Y', 'No <main> or role=main landmark')

# prefers-reduced-motion
if 'prefers-reduced-motion' in css:
    R.append('  [OK] prefers-reduced-motion respected')
else:
    issue('MEDIUM', 'A11Y', 'No prefers-reduced-motion media query')

# Color contrast check (approximation)
if 'prefers-contrast' in css:
    R.append('  [OK] prefers-contrast media query present')

# ============================================================
# 7. RESPONSIVE DESIGN AUDIT
# ============================================================
section('7. RESPONSIVE DESIGN')

media_queries = re.findall(r'@media\s*\([^)]+\)', css)
R.append(f'  Media queries found: {len(media_queries)}')

breakpoints = set()
for mq in media_queries:
    bp = re.findall(r'(\d+)px', mq)
    breakpoints.update(bp)
R.append(f'  Breakpoints used: {sorted(breakpoints, key=int)}')

# Check sidebar responsive
if 'sidebar' in css and '480' in str(breakpoints):
    R.append('  [OK] Sidebar has mobile breakpoint')

# ============================================================
# 8. PERFORMANCE
# ============================================================
section('8. PERFORMANCE')

R.append(f'  app.js size: {len(js):,} chars ({len(js)//1024}KB)')
R.append(f'  index.css size: {len(css):,} chars ({len(css)//1024}KB)')
R.append(f'  index.html size: {len(html):,} chars ({len(html)//1024}KB)')

# Count Chart.js instances
chart_instances = len(re.findall(r'new Chart\(', js))
R.append(f'  Chart.js instances created: {chart_instances}')

# Count event listeners
event_listeners = len(re.findall(r'addEventListener', js))
R.append(f'  addEventListener calls: {event_listeners}')

# ============================================================
# 9. SUMMARY
# ============================================================
section('9. SUMMARY')

# Count by severity
all_flat = []
for pi in all_issues.values():
    all_flat.extend(pi)

sev_counts = {}
cat_counts = {}
for sev, cat, _ in all_flat:
    sev_counts[sev] = sev_counts.get(sev, 0) + 1
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

R.append(f'  Total page issues: {len(all_flat)} across {len(all_issues)} pages')
R.append(f'  By severity:')
for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    R.append(f'    {sev}: {sev_counts.get(sev, 0)}')
R.append(f'  By category:')
for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
    R.append(f'    {cat}: {count}')

R.append('')
R.append(f'  Pages with most issues:')
for key, iss in sorted(all_issues.items(), key=lambda x: -len(x[1]))[:10]:
    crits = sum(1 for s, _, _ in iss if s == 'CRITICAL')
    R.append(f'    {key}: {len(iss)} issues ({crits} critical)')

# Write report
report = '\n'.join(R)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(report)

print(f'Full audit complete. {len(all_flat)} issues found across {len(all_issues)} pages.')
print(f'Report: {OUT}')

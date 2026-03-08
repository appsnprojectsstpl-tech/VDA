"""
FULL TAB AUDIT v2 — Find ALL pages, ALL tabs, check ALL content panes.
Uses a different approach: find the pages object, extract page keys,
then check each page's HTML for tab buttons and target panes.
"""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# Strategy: Find all page keys by looking for patterns like:
#   pageKey: `...HTML...`, 
# These appear in the pages object

# Step 1: Find ALL page key names
# Match pattern: word followed by colon then backtick (template literal)
page_keys = []
for m in re.finditer(r'\n\s{2,8}(\w+)\s*:\s*`', js):
    key = m.group(1)
    pos = m.start()
    # Check this is inside the pages object (roughly between position 20000-end)
    if pos > 15000:  
        page_keys.append((key, pos))

print(f"Found {len(page_keys)} potential page templates")
print("=" * 80)

total_tabs = 0
broken_tabs = []

for page_key, page_pos in page_keys:
    # Extract the page HTML template (from backtick to next closing backtick)
    tmpl_start = js.index('`', page_pos)
    
    # Find matching closing backtick (handle nested backticks carefully)
    depth = 0
    i = tmpl_start + 1
    tmpl_end = -1
    while i < len(js) and i < tmpl_start + 200000:
        ch = js[i]
        if ch == '`' and js[i-1:i] != '\\':
            tmpl_end = i
            break
        i += 1
    
    if tmpl_end < 0:
        continue
    
    html = js[tmpl_start+1:tmpl_end]
    
    # Skip if too short (not a real page)
    if len(html) < 100:
        continue
    
    # Find all tab buttons with onclick
    tab_buttons = re.findall(
        r'onclick=["\'](\w+)\s*\(\s*[\'"]([^"\']+)[\'"](?:\s*,\s*this)?\s*\)["\']',
        html
    )
    
    if not tab_buttons:
        # Also try onclick with double-escaped quotes
        tab_buttons = re.findall(
            r'onclick=["\'](\w+)\s*\(\s*\\[\'"]([^\\]+)\\[\'"](?:\s*,\s*this)?\s*\)',
            html
        )
    
    if not tab_buttons:
        continue
    
    print(f"\n{'='*60}")
    print(f"PAGE: {page_key} ({len(tab_buttons)} tabs, HTML size: {len(html)} chars)")
    print(f"{'='*60}")
    
    page_broken = []
    
    for fn_name, tab_id in tab_buttons:
        total_tabs += 1
        
        # Check 1: Does the function exist globally?
        fn_exists = any(p in js for p in [
            f'function {fn_name}(', f'function {fn_name} (',
            f'window.{fn_name} = function', f'window.{fn_name}=function',
        ])
        
        # Check 2: Does the target content pane exist in the page HTML?
        # First try exact ID
        pane_found = f'id="{tab_id}"' in html or f"id='{tab_id}'" in html
        found_id = tab_id if pane_found else None
        
        # Try with prefixes
        if not pane_found:
            prefix_map = {
                'windTab': 'wnd-', 'switchWindTab': 'wnd-',
                'solarTab': 'sol-', 'switchSolarTab': 'sol-',
                'switchBiogasTab': 'bio-', 'biogasTab': 'bio-',
                'dairyTab': 'd-', 'switchCowTab': 'd-',
                'switchPoultryTab': 'p-',
                'switchCarbonTab': 'carb-', 'carbonTab': 'carb-',
                'switchPaintTab': 'paint-', 'paintTab': 'paint-',
                'switchVpmsTab': 'vpms-', 'vermiTab': 'vpms-',
                'switchTreeTab': 'tree-', 'treeTab': 'tree-',
                'aquaTab': 'aqua-',
                'switchHydrogenTab': 'h2-', 'hydrogenTab': 'h2-',
                'switchHydroTab': 'hyd-', 'hydroTab': 'hyd-',
                'switchKineticTab': 'kems-', 'kineticTab': 'kin-',
                'vetTab': 'vet-', 'switchVetTab': 'vet-',
                'vedicTab': 'vedic-',
                'trustTab': 'trust-', 'switchTrustTab': 'trust-',
                'switchCommandTab': 'cmd-',
                'switchLogisticsTab': 'log-',
                'switchWaterTab': 'wat-', 'waterTab': 'wat-',
                'crmTab': 'crm-',
                'switchAgriTourTab': 'agri-',
                'ticketTab': 'tick-',
                'wfTab': 'wf-',
                'finTab': 'fin-',
                'gridTab': 'grid-',
                'solarSubTab': 'st-',
                'windSubTab': 'st-',
            }
            prefix = prefix_map.get(fn_name, '')
            if prefix:
                prefixed = prefix + tab_id
                if f'id="{prefixed}"' in html or f"id='{prefixed}'" in html:
                    pane_found = True
                    found_id = prefixed
        
        # Check 3: Is the pane content blank/empty?
        pane_blank = False
        if found_id:
            pane_match = re.search(
                rf'id=["\']' + re.escape(found_id) + r'["\'][^>]*>\s*\n?\s*</div>',
                html
            )
            if pane_match:
                pane_blank = True
        
        issues = []
        if not fn_exists: issues.append('FN_MISSING')
        if not pane_found: issues.append('PANE_MISSING')
        if pane_blank: issues.append('PANE_EMPTY')
        
        icon = 'OK' if not issues else 'BROKEN'
        if issues:
            print(f"  BROKEN: {fn_name}('{tab_id}') => pane:{found_id or '???'} [{', '.join(issues)}]")
            page_broken.append({'fn': fn_name, 'tab_id': tab_id, 'pane_id': found_id, 'issues': issues})
        else:
            print(f"  OK: {fn_name}('{tab_id}') => {found_id}")
    
    if page_broken:
        broken_tabs.extend([(page_key, b) for b in page_broken])

# ============================================================
# FINAL SUMMARY
# ============================================================
print(f"\n{'='*80}")
print(f"FINAL SUMMARY")
print(f"{'='*80}")
print(f"  Total pages scanned: {len([p for p,pos in page_keys if True])}")
print(f"  Total tab buttons:   {total_tabs}")
print(f"  BROKEN tabs:         {len(broken_tabs)}")

if broken_tabs:
    print(f"\nBROKEN TABS BY PAGE:")
    current_page = None
    for page, bt in broken_tabs:
        if page != current_page:
            print(f"\n  PAGE: {page}")
            current_page = page
        print(f"    {bt['fn']}('{bt['tab_id']}') => pane:{bt['pane_id'] or '???'} [{', '.join(bt['issues'])}]")

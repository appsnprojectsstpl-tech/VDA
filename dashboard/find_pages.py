"""Find the exact HTML locations for missing pages so we can inject panes."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

pages = ['hrm', 'inventory', 'dms', 'bi', 'lms', 'fieldservice', 'farmerportal']

for page in pages:
    # Try various patterns to find the page template key
    for pattern in [f'    {page}: `', f'    {page}:`', f'  {page}: `', f'{page}: `']:
        idx = js.find(pattern)
        if idx >= 0:
            break
    
    if idx < 0:
        print(f"PAGE '{page}': NOT FOUND in pages object")
        continue
    
    # Get template content (up to 3000 chars)
    segment = js[idx:idx+3000]
    
    # Find all tab buttons in this template
    btns = re.findall(r"onclick=\"(\w+)\('([^']+)'", segment)
    if not btns:
        btns = re.findall(r'onclick="(\w+)\(\'([^\']+)\'', segment)
    
    print(f"\nPAGE '{page}' at pos {idx}:")
    print(f"  Tab buttons found: {len(btns)}")
    for fn, tid in btns:
        print(f"    {fn}('{tid}')")
    
    # Find closing </div> of nav section
    nav_close = segment.find('</div>', segment.find('dairy-nav') if 'dairy-nav' in segment else 0)
    if nav_close > 0:
        print(f"  Nav close at offset: {nav_close}")
        print(f"  Context: ...{segment[nav_close-20:nav_close+30]}...")
    
    # Check if panes already exist
    for fn, tid in btns[:1]:
        # Common prefixes
        prefix_map = {
            'hrmTab': 'hrm-', 'invTab': 'inv-', 'dmsTab': 'dms-',
            'biTab': 'bi-', 'lmsTab': 'lms-', 'fsTab': 'fs-',
            'fpTab': 'fp-',
        }
        prefix = prefix_map.get(fn, '')
        pane_id = prefix + tid
        exists = pane_id in js
        print(f"  Pane '{pane_id}' exists in JS: {exists}")

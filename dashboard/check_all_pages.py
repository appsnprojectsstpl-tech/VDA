"""Check user's specific pages: Hydropower, Green Hydrogen, Kinetic, Vermicompost"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

pages_to_check = ['hydro', 'hydrogen', 'kinetic', 'vermi', 'solar', 'poultry', 
                   'aqua', 'tree', 'paint', 'carbon', 'crm', 'vedic', 'trust',
                   'water', 'command', 'logistics', 'cattle', 'wind', 'biogas',
                   'grid', 'hrm', 'inventory', 'dms', 'bi', 'ticketing',
                   'booking', 'lms', 'fieldservice', 'farmerportal', 'survey', 'schemes',
                   'finance', 'finance2', 'workflow']

for page in pages_to_check:
    # Find the page template
    found = False
    for pattern in [f'    {page}: `', f'    {page}:`', f'  {page}: `', f'{page}: `']:
        idx = js.find(pattern)
        if idx >= 0:
            found = True
            break
    
    if not found:
        print(f"  MISSING_PAGE: {page}")
        continue
    
    # Get template
    segment = js[idx:idx+5000]
    
    # Find tab buttons
    btns = re.findall(r"onclick=\"(\w+)\('([^']+)'", segment)
    
    # Check each button has a pane
    pane_issues = 0
    fn_issues = 0
    total = len(btns)
    
    for fn, tid in btns:
        # Check function exists
        fn_exists = f'function {fn}(' in js or f'window.{fn} = function' in js or f'window.{fn}=function' in js
        if not fn_exists:
            fn_issues += 1
        
        # Check pane exists (try ID directly and with prefix)
        prefix_map = {
            'hydroTab': 'hyd-', 'switchHydroTab': 'hyd-',
            'hydrogenTab': 'h2-', 'switchHydrogenTab': 'h2-',
            'kineticTab': 'kin-', 'switchKineticTab': 'kems-',
            'vermiTab': 'vpms-', 'switchVpmsTab': 'vpms-',
            'solarTab': 'sol-', 'switchSolarTab': 'sol-',
            'switchPoultryTab': 'p-',
            'aquaTab': 'aqua-',
            'treeTab': 'tree-', 'switchTreeTab': 'tree-',
            'switchPaintTab': 'paint-', 'paintTab': 'paint-',
            'switchCarbonTab': 'carb-', 'carbonTab': 'carb-',
            'crmTab': 'crm-',
            'vedicTab': 'vedic-',
            'trustTab': 'trust-', 'switchTrustTab': 'trust-',
            'waterTab': 'wat-', 'switchWaterTab': 'wat-',
            'switchCommandTab': 'cmd-',
            'switchLogisticsTab': 'log-',
            'dairyTab': 'd-', 'switchCowTab': 'd-',
            'windTab': 'wnd-',
            'switchBiogasTab': 'bio-',
            'gridTab': 'grid-',
            'hrmTab': 'hrm-',
            'invTab': 'inv-',
            'dmsTab': 'dms-',
            'biTab': 'bi-',
            'ticketTab': 'tick-',
            'bookingTab': 'bk-',
            'lmsTab': 'lms-',
            'fsTab': 'fs-',
            'fpTab': 'fp-',
            'surveyTab': 'srv-',
            'schemeTab': 'sch-',
            'wfTab': 'wf-',
            'finTab': 'fin-',
            'switchAgriTourTab': 'agri-',
        }
        
        prefix = prefix_map.get(fn, '')
        pane_id = prefix + tid if prefix else tid
        
        pane_exists = (f'id="{pane_id}"' in js or f"id='{pane_id}'" in js or 
                      f'id="{tid}"' in js or f"id='{tid}'" in js)
        
        if not pane_exists:
            pane_issues += 1
            print(f"    PANE_MISSING: {fn}('{tid}') => expected '{pane_id}'")
        
        if not fn_exists:
            print(f"    FN_MISSING: {fn}")
    
    status = 'OK' if (pane_issues == 0 and fn_issues == 0) else f'{pane_issues} panes + {fn_issues} fns missing'
    icon = 'OK' if status == 'OK' else 'BROKEN'
    print(f"  {icon}: {page} ({total} tabs) — {status}")

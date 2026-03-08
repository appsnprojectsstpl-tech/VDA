"""Fix the last 4 missing panes: p-broiler, windSubTab farmlist/farmperf, bg-sup"""
import re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

fixes = 0

# 1. Poultry: switchPoultryTab('p-broiler') looks for #p-broiler
# But the onclick passes 'p-broiler' which already has the prefix!
# So the pane ID is just 'p-broiler' (not 'p-p-broiler')
# Check if it exists
if 'id="p-broiler"' not in js:
    # Find where poultry page panes are and add it
    marker = 'id="p-health"'
    idx = js.find(marker)
    if idx > 0:
        # Find the end of that div
        insert_point = js.find('</div>', idx)
        insert_point = js.find('\n', insert_point) + 1
        pane = '''<div id="p-broiler" class="dairy-pane">
    <div class="page-section">
        <div class="section-title">🍗 Broiler Management</div>
        <div class="chart-placeholder" style="padding:30px;text-align:center;color:rgba(200,214,229,0.5);">
            <div style="font-size:2rem;margin-bottom:8px;">🍗</div>
            <div>Broiler operations management module</div>
        </div>
    </div>
</div>
'''
        js = js[:insert_point] + pane + js[insert_point:]
        fixes += 1
        print('Added p-broiler pane')

# 2. Wind sub-tabs: windSubTab('farmlist', btn, 'wnd-farms') looks for #st-farmlist
if 'id="st-farmlist"' not in js:
    marker = 'id="wnd-farms"'
    idx = js.find(marker)
    if idx > 0:
        # Find close of the sub-tab nav and add panes
        sub_nav_end = js.find('</div>', idx + 200)  # skip past sub-nav buttons
        sub_nav_end = js.find('\n', sub_nav_end) + 1
        panes = '''
<div id="st-farmlist" class="wind-sub-pane" style="display:block;">
    <div class="page-section">
        <div class="section-title">📋 Farm Registry</div>
        <table class="data-table"><thead><tr><th>Farm Name</th><th>Location</th><th>Capacity (MW)</th><th>Status</th></tr></thead>
        <tbody><tr><td>Bellary Wind Park</td><td>Bellary, KA</td><td>350 MW</td><td><span class="badge-success">Active</span></td></tr>
        <tr><td>Gadwal Wind Cluster</td><td>Gadwal, TS</td><td>280 MW</td><td><span class="badge-success">Active</span></td></tr>
        <tr><td>Kurnool Ridge</td><td>Kurnool, AP</td><td>212 MW</td><td><span class="badge-success">Active</span></td></tr></tbody></table>
    </div>
</div>
<div id="st-farmperf" class="wind-sub-pane" style="display:none;">
    <div class="page-section">
        <div class="section-title">📊 Performance Metrics</div>
        <div class="kpi-grid">
            <div class="kpi-card teal"><div class="kpi-value">92.1%</div><div class="kpi-label">Avg Capacity Factor</div></div>
            <div class="kpi-card blue"><div class="kpi-value">98.7%</div><div class="kpi-label">Availability</div></div>
            <div class="kpi-card emerald"><div class="kpi-value">1.2 GWh</div><div class="kpi-label">Today Output</div></div>
        </div>
    </div>
</div>
<div id="st-farmlease" class="wind-sub-pane" style="display:none;">
    <div class="page-section">
        <div class="section-title">📄 Lease & Land</div>
        <div class="chart-placeholder" style="padding:30px;text-align:center;color:rgba(200,214,229,0.5);">
            <div style="font-size:2rem;margin-bottom:8px;">📄</div>
            <div>Land lease and agreement management</div>
        </div>
    </div>
</div>
'''
        js = js[:sub_nav_end] + panes + js[sub_nav_end:]
        fixes += 2
        print('Added st-farmlist, st-farmperf, st-farmlease panes')

# 3. Biogas: switchBiogasTab('bg-sup') → pane id should be 'bg-sup'
# The function is switchBiogasTab which uses _universalTab — that hides all .dairy-pane 
# and shows #bio-{id} per prefix. But 'bg-sup' already starts with 'bg-' not 'bio-'
# So it's looking for 'bio-bg-sup' which doesn't exist.
# Fix: The actual ID should be 'bg-sup' — we just need to add it to the Master Tab Fix's findPane
# Or simply add a pane with id="bg-sup"
if 'id="bg-sup"' not in js:
    marker = 'id="bio-thermal"'
    if marker not in js:
        marker = 'id="bio-bellary"'
    idx = js.find(marker)
    if idx > 0:
        insert_point = js.find('</div>', idx)
        insert_point = js.find('\n', insert_point) + 1
        pane = '''<div id="bg-sup" class="dairy-pane">
    <div class="page-section">
        <div class="section-title">🔋 Supply Chain & Distribution</div>
        <div class="chart-placeholder" style="padding:30px;text-align:center;color:rgba(200,214,229,0.5);">
            <div style="font-size:2rem;margin-bottom:8px;">🔋</div>
            <div>Biogas supply chain and distribution management</div>
        </div>
    </div>
</div>
'''
        js = js[:insert_point] + pane + js[insert_point:]
        fixes += 1
        print('Added bg-sup pane')

# Save
with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=7.4.1', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=7.4.1', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

exit_code = os.system(f'node --check "{JS}" 2>&1')
print(f'SYNTAX: {"OK" if exit_code == 0 else "ERROR"}')
print(f'Fixes: {fixes}')
print(f'Version: 7.4.1')

#!/usr/bin/env python3
"""
Script to add Workflow and Ticketing modules
"""

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Workflow module template
workflow_module = '''
    workflow: `
    <div class="page-header"><div class="page-title">✅ Workflow & Approvals</div><div class="page-subtitle">24 Pending · 8 Approved Today · 3 Rejected</div></div>
   <div class="crm-nav">
     <button type="button"  class="crm-tab-btn active"onclick="wfTab('pending',this)">⏳ Pending</button>
     <button type="button"  class="crm-tab-btn"onclick="wfTab('approved',this)">✅ Approved</button>
     <button type="button"  class="crm-tab-btn"onclick="wfTab('rejected',this)">❌ Rejected</button>
     <button type="button"  class="crm-tab-btn"onclick="wfTab('templates',this)">📝 Templates</button>
    </div>

    <div class="crm-pn active"id="wf-pending">
        <div class="card"><div class="card-title">⏳ Pending Approvals</div>
        <table class="data-table">
            <tr><th>Request</th><th>Type</th><th>Requested By</th><th>Date</th><th>Amount</th><th>Priority</th><th>Actions</th></tr>
            <tr><td>PO-2026-0150</td><td>Purchase Order</td><td>Rajesh Kumar</td><td>2026-02-27</td><td>₹2,50,000</td><td><span class="pill pill-red">High</span></td><td><button class="clean-btn">Approve</button></td></tr>
            <tr><td>LEV-2026-0089</td><td>Leave Request</td><td>Anita Devi</td><td>2026-02-26</td><td>-</td><td><span class="pill pill-amber">Medium</span></td><td><button class="clean-btn">Review</button></td></tr>
            <tr><td>EXP-2026-0045</td><td>Expense Claim</td><td>Mahendra Singh</td><td>2026-02-25</td><td>₹45,000</td><td><span class="pill pill-amber">Medium</span></td><td><button class="clean-btn">Approve</button></td></tr>
            <tr><td>CAPEX-001</td><td>Capital Expenditure</td><td>Finance Team</td><td>2026-02-24</td><td>₹15,00,000</td><td><span class="pill pill-red">High</span></td><td><button class="clean-btn">Review</button></td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="wf-approved">
        <div class="card"><div class="card-title">✅ Recently Approved</div>
        <table class="data-table">
            <tr><th>Request</th><th>Type</th><th>Requested By</th><th>Approved By</th><th>Date</th></tr>
            <tr><td>PO-2026-0148</td><td>Purchase Order</td><td>Sunita Rao</td><td>Manager</td><td>2026-02-28</td></tr>
            <tr><td>LEV-2026-0085</td><td>Leave Request</td><td>Prakash Reddy</td><td>HR</td><td>2026-02-28</td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="wf-rejected">
        <div class="card"><div class="card-title">❌ Recently Rejected</div>
        <table class="data-table">
            <tr><th>Request</th><th>Type</th><th>Requested By</th><th>Reason</th><th>Date</th></tr>
            <tr><td>EXP-2026-0042</td><td>Expense Claim</td><td>John Doe</td><td>Missing receipts</td><td>2026-02-27</td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="wf-templates">
        <div class="card"><div class="card-title">📝 Workflow Templates</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:15px;">
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;"><strong>Purchase Order</strong><br><small>Up to ₹50K - Auto approved<br>Above ₹50K - Manager approval</small></div>
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;"><strong>Leave Request</strong><br><small>Auto approved if leave balance available</small></div>
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;"><strong>Expense Claim</strong><br><small>Up to ₹10K - Manager<br>Above ₹10K - Finance approval</small></div>
        </div>
    </div>

    `,

    ticketing: `
    <div class="page-header"><div class="page-title">🎫 Ticketing & Helpdesk</div><div class="page-subtitle">15 Open Tickets · 3 Critical · High Priority SLA</div></div>
   <div class="crm-nav">
     <button type="button"  class="crm-tab-btn active"onclick="ticketTab('all',this)">🎫 All Tickets</button>
     <button type="button"  class="crm-tab-btn"onclick="ticketTab('open',this)">📬 Open</button>
     <button type="button"  class="crm-tab-btn"onclick="ticketTab('my',this)">👤 My Tickets</button>
     <button type="button"  class="crm-tab-btn"onclick="ticketTab('create',this)">➕ New Ticket</button>
    </div>

    <div class="crm-pn active"id="ticket-all">
        <div class="card"><div class="card-title">🎫 All Tickets</div>
        <table class="data-table">
            <tr><th>Ticket ID</th><th>Subject</th><th>Category</th><th>Priority</th><th>Status</th><th>Assigned To</th><th>Created</th></tr>
            <tr><td>TKT-001</td><td>Solar panel damage - Zone A</td><td>Equipment</td><td><span class="pill pill-red">Critical</span></td><td><span class="pill pill-amber">In Progress</span></td><td>Tech Team A</td><td>2026-02-27</td></tr>
            <tr><td>TKT-002</td><td>Cattle health concern - Block 5</td><td>Animal Health</td><td><span class="pill pill-red">High</span></td><td><span class="pill pill-blue">Assigned</span></td><td>Dr. Lakshmi</td><td>2026-02-26</td></tr>
            <tr><td>TKT-003</td><td>Water pump malfunction</td><td>Infrastructure</td><td><span class="pill pill-amber">Medium</span></td><td><span class="pill pill-green">Resolved</span></td><td>Maintenance</td><td>2026-02-25</td></tr>
            <tr><td>TKT-004</td><td>Employee ID card issue</td><td>HR</td><td><span class="pill pill-green">Low</span></td><td><span class="pill pill-amber">In Progress</span></td><td>HR Team</td><td>2026-02-24</td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="ticket-open">
        <div class="card"><div class="card-title">📬 Open Tickets</div>
        <div class="kpi-grid" style="margin-bottom:15px;">
            <div class="kpi-card" style="background:#ff5252;color:white;"><div class="kpi-value">3</div><div class="kpi-label">Critical</div></div>
            <div class="kpi-card" style="background:#ff9800;color:white;"><div class="kpi-value">5</div><div class="kpi-label">High</div></div>
            <div class="kpi-card" style="background:#ffc107;color:black;"><div class="kpi-value">7</div><div class="kpi-label">Medium</div></div>
        </div>
        <table class="data-table"><tr><th>ID</th><th>Subject</th><th>Priority</th><th>Age</th></tr>
            <tr><td>TKT-001</td><td>Solar panel damage - Zone A</td><td><span class="pill pill-red">Critical</span></td><td>2 days</td></tr>
            <tr><td>TKT-002</td><td>Cattle health concern</td><td><span class="pill pill-red">High</span></td><td>3 days</td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="ticket-my">
        <div class="card"><div class="card-title">👤 My Tickets</div>
        <table class="data-table"><tr><th>ID</th><th>Subject</th><th>Status</th><th>Last Update</th></tr>
            <tr><td>TKT-005</td><td>Network issue - Office</td><td><span class="pill pill-green">Resolved</span></td><td>2026-02-28</td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="ticket-create">
        <div class="card"><div class="card-title">➕ Create New Ticket</div>
        <div style="max-width:600px;">
            <div><label>Subject:</label><input type="text" style="width:100%;padding:10px;margin:5px 0;"></div>
            <div><label>Category:</label><select style="width:100%;padding:10px;margin:5px 0;"><option>Equipment</option><option>Animal Health</option><option>Infrastructure</option><option>HR</option><option>IT</option></select></div>
            <div><label>Priority:</label><select style="width:100%;padding:10px;margin:5px 0;"><option>Critical</option><option>High</option><option>Medium</option><option>Low</option></select></div>
            <div><label>Description:</label><textarea style="width:100%;padding:10px;margin:5px 0;" rows="5"></textarea></div>
            <button type="button" class="clean-btn">🎫 Create Ticket</button>
        </div>
    </div>

    `,
'''

# Add to app.js before bi module
old_bi = '''    bi: `
    <div class="page-header"><div class="page-title">📊 Business Intelligence</div>'''

content = content.replace(old_bi, workflow_module + '\n' + old_bi, 1)

# Write back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Workflow and Ticketing modules added!")

# Add tab functions
with open('dashboard/app.js', 'r') as f:
    content = f.read()

# Add functions after biTab
wf_functions = '''
// Workflow Tab Switcher
window.wfTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('wf-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.wfTab = wfTab;

// Ticketing Tab Switcher
window.ticketTab = function (id, btn) {
    var container = document.getElementById('page-container') || document.body;
    container.querySelectorAll('.crm-pn').forEach(function (e) { e.classList.remove('active'); });
    container.querySelectorAll('.crm-tab-btn').forEach(function (e) { e.classList.remove('active'); });
    const target = document.getElementById('ticket-' + id) || document.getElementById(id);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
};
window.ticketTab = ticketTab;

'''

old_biTab_end = '''window.biTab = biTab;
'''
content = content.replace(old_biTab_end, old_biTab_end + wf_functions)

with open('dashboard/app.js', 'w') as f:
    f.write(content)

print("Tab functions added!")

# Add sidebar entries
with open('dashboard/index.html', 'r') as f:
    sidebar = f.read()

sidebar_entries = '''
                    <div class="menu-item" data-page="workflow">
                        <div class="nav-icon">✅</div>
                        <div class="nav-label">Workflow</div>
                    </div>
                    <div class="menu-item" data-page="ticketing">
                        <div class="nav-icon">🎫</div>
                        <div class="nav-label">Helpdesk</div>
                    </div>'''

old_bi_entry = '''                    <div class="menu-item" data-page="bi">
                        <div class="nav-icon">📊</div>
                        <div class="nav-label">BI & Analytics</div>
                    </div>'''

sidebar = sidebar.replace(old_bi_entry, old_bi_entry + sidebar_entries)

with open('dashboard/index.html', 'w') as f:
    f.write(sidebar)

print("Sidebar entries added!")
print("All Tier 2 modules complete!")

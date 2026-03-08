#!/usr/bin/env python3
"""
Script to add new CRM tabs (Leads, Tasks, Communications) to app.js
"""

import re

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# New tab navigation buttons to add
nav_buttons = """     <button type="button"  class="crm-tab-btn"onclick="crmTab('leads',this)">🎯 Leads</button>
     <button type="button"  class="crm-tab-btn"onclick="crmTab('tasks',this)">✅ Tasks</button>
     <button type="button"  class="crm-tab-btn"onclick="crmTab('communications',this)">💬 Communications</button>"""

# Add new buttons before Reports button
old_nav = """     <button type="button"  class="crm-tab-btn"onclick="crmTab('crep',this)">📋 Reports</button>"""
new_nav = nav_buttons + """
     <button type="button"  class="crm-tab-btn"onclick="crmTab('crep',this)">📋 Reports</button>"""

content = content.replace(old_nav, new_nav)

# New tab content to add before crm-delivery
new_tabs = '''
    <!-- LEADS TAB -->
    <div class="crm-pn"id="cm-leads">
        <div class="card"><div class="card-title">🎯 Lead Management</div>
        <div style="margin-bottom:15px;"><button type="button" class="clean-btn" onclick="showAddLeadForm()">➕ Add New Lead</button></div>
      <table class="data-table">
          <tr><th>Lead Name</th><th>Company</th><th>Source</th><th>Value</th><th>Status</th><th>Assigned To</th><th>Actions</th></tr>
          <tr><td>Rajesh Kumar</td><td>ITC Ltd</td><td>Referral</td><td>₹8 Cr</td><td><span class="pill pill-amber">Negotiation</span></td><td>Sales Team A</td><td><button>View</button></td></tr>
          <tr><td>Priya Sharma</td><td>Tesla Energy</td><td>Website</td><td>₹12 Cr</td><td><span class="pill pill-blue">Proposal</span></td><td>Sales Team B</td><td><button>View</button></td></tr>
          <tr><td>Ajay Singh</td><td>Reliance Retail</td><td>Trade Show</td><td>₹6 Cr</td><td><span class="pill pill-green">Qualified</span></td><td>Sales Team A</td><td><button>View</button></td></tr>
          <tr><td>Sunita Devi</td><td>Adani Green</td><td>Cold Call</td><td>₹15 Cr</td><td><span class="pill pill-gray">New</span></td><td>Unassigned</td><td><button>View</button></td></tr>
          <tr><td>Mahendra Reddy</td><td>Fortune Foods</td><td>Referral</td><td>₹3.5 Cr</td><td><span class="pill pill-amber">Negotiation</span></td><td>Sales Team C</td><td><button>View</button></td></tr>
      </table></div>
    </div>

    <!-- TASKS TAB -->
    <div class="crm-pn"id="cm-tasks">
        <div class="card"><div class="card-title">✅ Task Management</div>
        <div style="display:flex;gap:10px;margin-bottom:15px;">
            <button type="button" class="clean-btn" onclick="filterTasks('all')">All</button>
            <button type="button" class="clean-btn" onclick="filterTasks('pending')">Pending</button>
            <button type="button" class="clean-btn" onclick="filterTasks('in_progress')">In Progress</button>
            <button type="button" class="clean-btn" onclick="filterTasks('completed')">Completed</button>
        </div>
      <table class="data-table">
          <tr><th>Task</th><th>Related To</th><th>Due Date</th><th>Priority</th><th>Status</th><th>Assigned To</th></tr>
          <tr><td>Follow up with ITC contract</td><td>ITC Ltd - Deal</td><td>2026-03-01</td><td><span class="pill pill-red">High</span></td><td><span class="pill pill-amber">Pending</span></td><td>John Doe</td></tr>
          <tr><td>Prepare quote for Tesla</td><td>Tesla Energy - Deal</td><td>2026-03-05</td><td><span class="pill pill-red">High</span></td><td><span class="pill pill-blue">In Progress</span></td><td>Jane Smith</td></tr>
          <tr><td>Site visit - Reliance</td><td>Reliance Retail - Deal</td><td>2026-03-10</td><td><span class="pill pill-amber">Medium</span></td><td><span class="pill pill-gray">Pending</span></td><td>Mike Johnson</td></tr>
          <tr><td>Send proposal - Adani</td><td>Adani Green - Deal</td><td>2026-02-28</td><td><span class="pill pill-red">High</span></td><td><span class="pill pill-green">Completed</span></td><td>John Doe</td></tr>
          <tr><td>Contract review - Heritage</td><td>Heritage Foods - Contract</td><td>2026-03-15</td><td><span class="pill pill-amber">Medium</span></td><td><span class="pill pill-amber">Pending</span></td><td>Legal Team</td></tr>
      </table></div>
    </div>

    <!-- COMMUNICATIONS TAB -->
    <div class="crm-pn"id="cm-communications">
        <div class="card"><div class="card-title">💬 Communications & Activity Log</div>
        <div style="display:flex;gap:10px;margin-bottom:15px;">
            <button type="button" class="clean-btn" onclick="filterComms('all')">All</button>
            <button type="button" class="clean-btn" onclick="filterComms('call')">📞</button>
            <button type="button" class="clean-btn" onclick="filterComms('email')">✉️</button>
            <button type="button" class="clean-btn" onclick="filterComms('meeting')">🤝</button>
            <button type="button" class="clean-btn" onclick="filterComms('note')">📝</button>
        </div>
      <table class="data-table">
          <tr><th>Date</th><th>Type</th><th>Contact</th><th>Subject</th><th>Summary</th><th>User</th></tr>
          <tr><td>2026-02-27</td><td>📞</td><td>ITC Ltd</td><td>Contract discussion</td><td>Discussed pricing terms, client requested 10% discount</td><td>John Doe</td></tr>
          <tr><td>2026-02-26</td><td>✉️</td><td>Tesla Energy</td><td>Proposal sent</td><td>Sent revised proposal for 25MW solar PPA</td><td>Jane Smith</td></tr>
          <tr><td>2026-02-25</td><td>🤝</td><td>Reliance Retail</td><td>Site visit</td><td>Visited warehouse, discussed logistics requirements</td><td>Mike Johnson</td></tr>
          <tr><td>2026-02-24</td><td>📝</td><td>Heritage Foods</td><td>Contract renewal</td><td>Note: Renewal due in 6 months, schedule meeting</td><td>John Doe</td></tr>
          <tr><td>2026-02-23</td><td>📞</td><td>Adani Green</td><td>Initial call</td><td>Introduction call, interested in wind power</td><td>Jane Smith</td></tr>
      </table></div>
    </div>
'''

# Add new tabs before crm-delivery
old_delivery = '<div class="crm-pn" id="crm-delivery">'
content = content.replace(old_delivery, new_tabs + old_delivery)

# Write the modified content back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("CRM tabs added successfully!")

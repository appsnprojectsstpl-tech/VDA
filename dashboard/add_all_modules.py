#!/usr/bin/env python3
"""
Script to add Finance, DMS, and BI modules to app.js
"""

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Finance module template
finance_module = '''
    finance2: `
    <div class="page-header"><div class="page-title">💰 Finance & Accounting</div><div class="page-subtitle">₹82 Cr Revenue · ₹45 Cr Expenses · ₹37 Cr Net Profit</div></div>
   <div class="crm-nav">
     <button type="button"  class="crm-tab-btn active"onclick="finTab('dashboard',this)">📊 Dashboard</button>
     <button type="button"  class="crm-tab-btn"onclick="finTab('invoices',this)">📄 Invoices</button>
     <button type="button"  class="crm-tab-btn"onclick="finTab('expenses',this)">💸 Expenses</button>
     <button type="button"  class="crm-tab-btn"onclick="finTab('pl',this)">📈 P&L Statement</button>
     <button type="button"  class="crm-tab-btn"onclick="finTab('freports',this)">📋 Reports</button>
    </div>

    <div class="crm-pn active"id="fin-dashboard">
        <div class="kpi-grid">
            <div class="kpi-card teal"><div class="kpi-top"><div class="kpi-icon">💰</div></div><div><div class="kpi-value">₹82 Cr</div><div class="kpi-label">Total Revenue</div></div></div>
            <div class="kpi-card green"><div class="kpi-top"><div class="kpi-icon">📉</div></div><div><div class="kpi-value">₹45 Cr</div><div class="kpi-label">Total Expenses</div></div></div>
            <div class="kpi-card emerald"><div class="kpi-top"><div class="kpi-icon">📈</div></div><div><div class="kpi-value">₹37 Cr</div><div class="kpi-label">Net Profit</div></div></div>
            <div class="kpi-card orange"><div class="kpi-top"><div class="kpi-icon">📥</div></div><div><div class="kpi-value">₹4.2 Cr</div><div class="kpi-label">Receivables</div></div></div>
        </div>
    </div>

    <div class="crm-pn"id="fin-invoices">
        <div class="card"><div class="card-title">📄 Invoice Management</div>
        <div style="margin-bottom:15px;"><button type="button" class="clean-btn" onclick="showCreateInvoice()">➕ Create Invoice</button></div>
        <table class="data-table"><tr><th>Invoice #</th><th>Customer</th><th>Amount</th><th>Date</th><thDue Date</th><th>Status</th></tr>
            <tr><td>INV-2026-0145</td><td>Heritage Foods</td><td>₹18,00,000</td><td>2026-02-01</td><td>2026-03-01</td><td><span class="pill pill-amber">Pending</span></td></tr>
            <tr><td>INV-2026-0144</td><td>AP DISCOM</td><td>₹14,00,000</td><td>2026-02-05</td><td>2026-03-05</td><td><span class="pill pill-green">Paid</span></td></tr>
            <tr><td>INV-2026-0143</td><td>ClimatePartner</td><td>€90,000</td><td>2026-02-10</td><td>2026-03-10</td><td><span class="pill pill-amber">Pending</span></td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="fin-expenses">
        <div class="card"><div class="card-title">💸 Expense Claims</div>
        <div style="margin-bottom:15px;"><button type="button" class="clean-btn">➕ New Expense</button></div>
        <table class="data-table"><tr><th>Claim #</th><th>Employee</th><th>Category</th><th>Amount</th><th>Date</th><th>Status</th></tr>
            <tr><td>EXP-001</td><td>Rajesh Kumar</td><td>Travel</td><td>₹45,000</td><td>2026-02-25</td><td><span class="pill pill-amber">Pending</span></td></tr>
            <tr><td>EXP-002</td><td>Lakshmi Devi</td><td>Medical Supplies</td><td>₹1,20,000</td><td>2026-02-20</td><td><span class="pill pill-green">Approved</span></td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="fin-pl">
        <div class="card"><div class="card-title">📈 Profit & Loss Statement - FY 2025-26</div>
        <table class="data-table">
            <tr><th>Revenue Sources</th><th>Amount (₹)</th></tr>
            <tr><td>Milk Sales</td><td>₹45,00,00,000</td></tr>
            <tr><td>Solar Power Export</td><td>₹18,00,00,000</td></tr>
            <tr><td>Carbon Credits</td><td>₹8,00,00,000</td></tr>
            <tr><td>Bio-Paints</td><td>₹4,00,00,000</td></tr>
            <tr><td><strong>Total Revenue</strong></td><td><strong>₹82,00,00,000</strong></td></tr>
            <tr><th>Expenses</th><th>Amount (₹)</th></tr>
            <tr><td>Cattle Feed</td><td>₹15,00,00,000</td></tr>
            <tr><td>Payroll</td><td>₹12,00,00,000</td></tr>
            <tr><td>Utilities</td><td>₹8,00,00,000</td></tr>
            <tr><td>Maintenance</td><td>₹5,00,00,000</td></tr>
            <tr><td>Other Expenses</td><td>₹5,00,00,000</td></tr>
            <tr><td><strong>Total Expenses</strong></td><td><strong>₹45,00,00,000</strong></td></tr>
            <tr><td><strong>Net Profit</strong></td><td><strong>₹37,00,00,000</strong></td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="fin-freports">
        <div class="card"><div class="card-title">📋 Financial Reports</div>
        <div class="kpi-grid">
            <div class="kpi-card teal"><div><div class="kpi-value">45%</div><div class="kpi-label">Profit Margin</div></div></div>
            <div class="kpi-card green"><div><div class="kpi-value">₹2.1 Cr</div><div class="kpi-label">Monthly Cash Flow</div></div></div>
            <div class="kpi-card emerald"><div><div class="kpi-value">1.8</div><div class="kpi-label">Current Ratio</div></div></div>
            <div class="kpi-card orange"><div><div class="kpi-value">₹4.2 Cr</div><div class="kpi-label">Outstanding</div></div></div>
        </div>
    </div>

    `,

    dms: `
    <div class="page-header"><div class="page-title">📁 Document Management</div><div class="page-subtitle">245 Documents · 15 Categories · Secure Storage</div></div>
   <div class="crm-nav">
     <button type="button"  class="crm-tab-btn active"onclick="dmsTab('browse',this)">📂 Browse</button>
     <button type="button"  class="crm-tab-btn"onclick="dmsTab('upload',this)">⬆️ Upload</button>
     <button type="button"  class="crm-tab-btn"onclick="dmsTab('search',this)">🔍 Search</button>
    </div>

    <div class="crm-pn active"id="dms-browse">
        <div class="card"><div class="card-title">📂 Document Library</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-top:15px;">
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;text-align:center;">
                <div style="font-size:2rem;">📄</div>
                <div>Implementation Guides</div>
                <div style="color:var(--text-muted);font-size:0.8rem;">12 files</div>
            </div>
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;text-align:center;">
                <div style="font-size:2rem;">📋</div>
                <div>Contracts</div>
                <div style="color:var(--text-muted);font-size:0.8rem;">48 files</div>
            </div>
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;text-align:center;">
                <div style="font-size:2rem;">🛠️</div>
                <div>Technical Specs</div>
                <div style="color:var(--text-muted);font-size:0.8rem;">35 files</div>
            </div>
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;text-align:center;">
                <div style="font-size:2rem;">📊</div>
                <div>Reports</div>
                <div style="color:var(--text-muted);font-size:0.8rem;">67 files</div>
            </div>
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;text-align:center;">
                <div style="font-size:2rem;">⚖️</div>
                <div>Legal</div>
                <div style="color:var(--text-muted);font-size:0.8rem;">23 files</div>
            </div>
            <div style="background:var(--panel-bg);padding:15px;border-radius:8px;text-align:center;">
                <div style="font-size:2rem;">🎓</div>
                <div>Training</div>
                <div style="color:var(--text-muted);font-size:0.8rem;">18 files</div>
            </div>
        </div>
    </div>

    <div class="crm-pn"id="dms-upload">
        <div class="card"><div class="card-title">⬆️ Upload Documents</div>
        <div style="border:2px dashed #ddd;padding:40px;text-align:center;border-radius:8px;margin:20px 0;">
            <div style="font-size:3rem;">📤</div>
            <div>Drag and drop files here</div>
            <div style="color:var(--text-muted);">or</div>
            <button type="button" class="clean-btn" style="margin-top:10px;">Browse Files</button>
        </div>
        <div><label>Category:</label><select style="width:100%;padding:10px;margin:10px 0;"><option>Implementation Guides</option><option>Contracts</option><option>Technical Specs</option></select></div>
        <div><label>Description:</label><textarea style="width:100%;padding:10px;margin:10px 0;" rows="3"></textarea></div>
        <button type="button" class="clean-btn">💾 Upload</button>
    </div>

    <div class="crm-pn"id="dms-search">
        <div class="card"><div class="card-title">🔍 Advanced Search</div>
        <input type="text" placeholder="Search documents by name, content, or tags..." style="width:100%;padding:12px;margin:10px 0;">
        <div style="display:flex;gap:10px;margin-bottom:15px;">
            <select><option>All Categories</option><option>Implementation Guides</option><option>Contracts</option></select>
            <select><option>All Dates</option><option>Last 7 days</option><option>Last 30 days</option></select>
            <button type="button" class="clean-btn">Search</button>
        </div>
        <table class="data-table"><tr><th>Document</th><th>Category</th><th>Size</th><th>Date</th></tr>
            <tr><td>Vedavathi-Biogas-Implementation-Strategy.pdf</td><td>Implementation Guides</td><td>7.9 MB</td><td>2026-01-15</td></tr>
            <tr><td>Vedavathi-Solar-Panel-Implementation-Strategy.pdf</td><td>Implementation Guides</td><td>7.2 MB</td><td>2026-01-10</td></tr>
        </table></div>
    </div>

    `,

    bi: `
    <div class="page-header"><div class="page-title">📊 Business Intelligence</div><div class="page-subtitle">Cross-Module Analytics · Real-Time Dashboards</div></div>
   <div class="crm-nav">
     <button type="button"  class="crm-tab-btn active"onclick="biTab('overview',this)">🎯 Overview</button>
     <button type="button"  class="crm-tab-btn"onclick="biTab('revenue',this)">💰 Revenue</button>
     <button type="button"  class="crm-tab-btn"onclick="biTab('operations',this)">⚙️ Operations</button>
     <button type="button"  class="crm-tab-btn"onclick="biTab('forecast',this)">🔮 Forecast</button>
    </div>

    <div class="crm-pn active"id="bi-overview">
        <div class="kpi-grid">
            <div class="kpi-card teal"><div><div class="kpi-value">₹82 Cr</div><div class="kpi-label">Total Revenue</div></div></div>
            <div class="kpi-card green"><div><div class="kpi-value">247</div><div class="kpi-label">Employees</div></div></div>
            <div class="kpi-card emerald"><div><div class="kpi-value">1,247</div><div class="kpi-label">Inventory Items</div></div></div>
            <div class="kpi-card orange"><div><div class="kpi-value">48</div><div class="kpi-label">Active Deals</div></div></div>
        </div>
        <div class="card" style="margin-top:15px;"><div class="card-title">📈 Revenue by Zone</div>
        <div class="silo-wrap">
            <div class="silo-row"><div class="silo-label">Bellary</div><div class="silo-bar-bg"><div class="silo-fill"style="width:45%;background:#00b0ff;"></div></div><div class="silo-val">₹36.9 Cr</div></div>
            <div class="silo-row"><div class="silo-label">Kurnool</div><div class="silo-bar-bg"><div class="silo-fill"style="width:25%;background:#00c853;"></div></div><div class="silo-val">₹20.5 Cr</div></div>
            <div class="silo-row"><div class="silo-label">Hyderabad</div><div class="silo-bar-bg"><div class="silo-fill"style="width:20%;background:#ffd600;"></div></div><div class="silo-val">₹16.4 Cr</div></div>
            <div class="silo-row"><div class="silo-label">Gadwal</div><div class="silo-bar-bg"><div class="silo-fill"style="width:10%;background:#e040fb;"></div></div><div class="silo-val">₹8.2 Cr</div></div>
        </div></div>
    </div>

    <div class="crm-pn"id="bi-revenue">
        <div class="card"><div class="card-title">💰 Revenue Analytics</div>
        <table class="data-table"><tr><th>Product/Service</th><th>Revenue</th><th>% of Total</th><th>Growth</th></tr>
            <tr><td>Milk Sales</td><td>₹45 Cr</td><td>55%</td><td><span style="color:green">↑ 12%</span></td></tr>
            <tr><td>Solar Power</td><td>₹18 Cr</td><td>22%</td><td><span style="color:green">↑ 8%</span></td></tr>
            <tr><td>Carbon Credits</td><td>₹8 Cr</td><td>10%</td><td><span style="color:green">↑ 25%</span></td></tr>
            <tr><td>Bio-Paints</td><td>₹4 Cr</td><td>5%</td><td><span style="color:green">↑ 15%</span></td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="bi-operations">
        <div class="card"><div class="card-title">⚙️ Operations Metrics</div>
        <table class="data-table"><tr><th>Metric</th><th>Value</th><th>Target</th><th>Status</th></tr>
            <tr><td>Attendance Rate</td><td>98%</td><td>95%</td><td><span class="pill pill-green">On Track</span></td></tr>
            <tr><td>Inventory Turnover</td><td>4.2x</td><td>4.0x</td><td><span class="pill pill-green">On Track</span></td></tr>
            <tr><td>Contract Renewal Rate</td><td>96%</td><td>90%</td><td><span class="pill pill-green">On Track</span></td></tr>
        </table></div>
    </div>

    <div class="crm-pn"id="bi-forecast">
        <div class="card"><div class="card-title">🔮 Revenue Forecast</div>
        <div style="padding:20px;background:var(--panel-bg);border-radius:8px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;"><span>Q1 2026</span><span>₹22 Cr</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;"><span>Q2 2026</span><span>₹24 Cr</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;"><span>Q3 2026</span><span>₹26 Cr</span></div>
            <div style="display:flex;justify-content:space-between;"><span>Q4 2026</span><span>₹28 Cr</span></div>
        </div>
    </div>

    `,
'''

# Find a good place to insert - look for end of finance
# The existing finance: ` ends somewhere, we'll insert before it
old_finance_start = '''    finance: `
    <div class="page-header">'''

content = content.replace(old_finance_start, finance_module + '\n' + old_finance_start, 1)

# Write the modified content back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("All modules added successfully!")

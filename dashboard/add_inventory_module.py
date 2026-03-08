#!/usr/bin/env python3
"""
Script to add Inventory Management module to app.js
"""

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Inventory module template
inventory_module = '''
    inventory: `
    <div class="page-header"><div class="page-title">📦 Inventory Management</div><div class="page-subtitle">1,247 Items · ₹4.2 Cr Stock Value · 18 Reorder Alerts</div></div>
   <div class="crm-nav">
     <button type="button"  class="crm-tab-btn active"onclick="invTab('stock',this)">📦 Stock Levels</button>
     <button type="button"  class="crm-tab-btn"onclick="invTab('reorder',this)">⚠️ Reorder Alerts</button>
     <button type="button"  class="crm-tab-btn"onclick="invTab('purchase',this)">🛒 Purchase Orders</button>
     <button type="button"  class="crm-tab-btn"onclick="invTab('consumption',this)">📉 Consumption</button>
     <button type="button"  class="crm-tab-btn"onclick="invTab('vreports',this)">📊 Reports</button>
    </div>

    <!-- STOCK LEVELS TAB -->
    <div class="crm-pn active"id="inv-stock">
        <div class="card"><div class="card-title">📦 Current Stock Levels by Zone</div>
        <div style="margin-bottom:15px;display:flex;gap:10px;">
            <button type="button" class="clean-btn" onclick="showAddItemForm()">➕ Add Item</button>
            <input type="text" placeholder="Search items..." style="padding:8px;border:1px solid #ddd;border-radius:4px;">
            <select style="padding:8px;"><option>All Zones</option><option>Bellary</option><option>Kurnool</option><option>Gadwal</option><option>Hyderabad</option></select>
        </div>
      <table class="data-table">
          <tr><th>Item Code</th><th>Item Name</th><th>Category</th><th>Zone</th><th>Current Stock</th><th>Unit</th><th>Min Level</th><th>Status</th></tr>
          <tr><td>FD001</td><td>Cattle Feed (Molasses)</td><td>Cattle Feed</td><td>Bellary</td><td>450</td><td>kg</td><td>200</td><td><span class="pill pill-green">OK</span></td></tr>
          <tr><td>FD002</td><td>Poultry Feed Layer</td><td>Poultry Feed</td><td>Kurnool</td><td>120</td><td>kg</td><td>150</td><td><span class="pill pill-red">Low</span></td></tr>
          <tr><td>MED001</td><td>Foot & Mouth Vaccine</td><td>Medicines</td><td>Gadwal</td><td>500</td><td>doses</td><td>100</td><td><span class="pill pill-green">OK</span></td></tr>
          <tr><td>MED002</td><td>Antibiotic Injection</td><td>Medicines</td><td>Bellary</td><td>45</td><td>units</td><td>50</td><td><span class="pill pill-red">Low</span></td></tr>
          <tr><td>RAW001</td><td>Turpentine Oil</td><td>Raw Materials</td><td>Hyderabad</td><td>200</td><td>liters</td><td>100</td><td><span class="pill pill-green">OK</span></td></tr>
          <tr><td>RAW002</td><td>Natural Pigment</td><td>Raw Materials</td><td>Hyderabad</td><td>25</td><td>kg</td><td>30</td><td><span class="pill pill-red">Low</span></td></tr>
          <tr><td>VER001</td><td>Vermicompost Ready</td><td>Output</td><td>Bellary</td><td>2500</td><td>kg</td><td>500</td><td><span class="pill pill-green">OK</span></td></tr>
      </table></div>
    </div>

    <!-- REORDER ALERTS TAB -->
    <div class="crm-pn"id="inv-reorder">
        <div class="card"><div class="card-title">⚠️ Reorder Alerts</div>
        <div style="display:flex;gap:10px;margin-bottom:15px;">
            <button type="button" class="clean-btn" style="background:#ff5252;color:white;">⚡ Create PO</button>
            <button type="button" class="clean-btn">✅ Mark as Ordered</button>
        </div>
      <table class="data-table">
          <tr><th>Alert</th><th>Item</th><th>Current</th><th>Minimum</th><th>Shortage</th><th>Zone</th><th>Suggested Vendor</th><th>Priority</th></tr>
          <tr><td>🔴 Critical</td><td>Poultry Feed Layer</td><td>120 kg</td><td>150 kg</td><td>-30 kg</td><td>Kurnool</td><td>FeedCo Ltd</td><td><span class="pill pill-red">High</span></td></tr>
          <tr><td>🔴 Critical</td><td>Antibiotic Injection</td><td>45 units</td><td>50 units</td><td>-5 units</td><td>Bellary</td><td>VetPharma Inc</td><td><span class="pill pill-red">High</span></td></tr>
          <tr><td>🟠 Warning</td><td>Natural Pigment</td><td>25 kg</td><td>30 kg</td><td>-5 kg</td><td>Hyderabad</td><td>ChemSupplies</td><td><span class="pill pill-amber">Medium</span></td></tr>
          <tr><td>🟠 Warning</td><td>Vitamin Premix</td><td>80 kg</td><td>100 kg</td><td>-20 kg</td><td>Gadwal</td><td>AgriVet Corp</td><td><span class="pill pill-amber">Medium</span></td></tr>
          <tr><td>🟡 Info</td><td>Poultry Feed Broiler</td><td>200 kg</td><td>250 kg</td><td>-50 kg</td><td>Bellary</td><td>FeedCo Ltd</td><td><span class="pill pill-green">Low</span></td></tr>
      </table></div>
    </div>

    <!-- PURCHASE ORDERS TAB -->
    <div class="crm-pn"id="inv-purchase">
        <div class="card"><div class="card-title">🛒 Purchase Orders</div>
        <div style="margin-bottom:15px;"><button type="button" class="clean-btn" onclick="showCreatePOForm()">➕ Create New PO</button></div>
      <table class="data-table">
          <tr><th>PO Number</th><th>Vendor</th><th>Items</th><th>Total Value</th><th>Date</th><th>Expected Delivery</th><th>Status</th></tr>
          <tr><td>PO-2026-0145</td><td>FeedCo Ltd</td><td>Poultry Feed Layer: 500kg</td><td>₹1,25,000</td><td>2026-02-25</td><td>2026-03-05</td><td><span class="pill pill-blue">In Transit</span></td></tr>
          <tr><td>PO-2026-0144</td><td>VetPharma Inc</td><td>Antibiotic: 200 units</td><td>₹45,000</td><td>2026-02-24</td><td>2026-03-01</td><td><span class="pill pill-green">Delivered</span></td></tr>
          <tr><td>PO-2026-0143</td><td>ChemSupplies</td><td>Natural Pigment: 50kg</td><td>₹75,000</td><td>2026-02-20</td><td>2026-02-28</td><td><span class="pill pill-amber">Pending</span></td></tr>
          <tr><td>PO-2026-0142</td><td>AgriVet Corp</td><td>Vitamin Premix: 200kg</td><td>₹60,000</td><td>2026-02-15</td><td>2026-02-22</td><td><span class="pill pill-green">Delivered</span></td></tr>
      </table></div>
    </div>

    <!-- CONSUMPTION TAB -->
    <div class="crm-pn"id="inv-consumption">
        <div class="card"><div class="card-title">📉 Consumption Trends</div>
        <div style="display:flex;gap:10px;margin-bottom:15px;">
            <select><option>Last 30 Days</option><option>Last 90 Days</option><option>Last 1 Year</option></select>
            <select><option>All Categories</option><option>Cattle Feed</option><option>Poultry Feed</option><option>Medicines</option></select>
        </div>
      <table class="data-table">
          <tr><th>Item</th><th>Opening Stock</th><th>Received</th><th>Consumed</th><th>Closing Stock</th><th>Daily Avg</th><th>Trend</th></tr>
          <tr><td>Cattle Feed (Molasses)</td><td>350 kg</td><td>400 kg</td><td>300 kg</td><td>450 kg</td><td>10 kg</td><td>📈 +15%</td></tr>
          <tr><td>Poultry Feed Layer</td><td>200 kg</td><td>150 kg</td><td>230 kg</td><td>120 kg</td><td>7.7 kg</td><td>📈 +25%</td></tr>
          <tr><td>Foot & Mouth Vaccine</td><td>400 doses</td><td>300 doses</td><td>200 doses</td><td>500 doses</td><td>6.7 doses</td><td>📉 -10%</td></tr>
          <tr><td>Vitamin Premix</td><td>120 kg</td><td>80 kg</td><td>120 kg</td><td>80 kg</td><td>4 kg</td><td>📊 Stable</td></tr>
      </table></div>
    </div>

    <!-- REPORTS TAB -->
    <div class="crm-pn"id="inv-vreports">
        <div class="card"><div class="card-title">📊 Inventory Reports</div>
        <div class="kpi-grid">
            <div class="kpi-card teal"><div class="kpi-top"><div class="kpi-icon">📦</div></div><div><div class="kpi-value">1,247</div><div class="kpi-label">Total Items</div></div></div>
            <div class="kpi-card green"><div class="kpi-top"><div class="kpi-icon">💰</div></div><div><div class="kpi-value">₹4.2Cr</div><div class="kpi-label">Stock Value</div></div></div>
            <div class="kpi-card emerald"><div class="kpi-top"><div class="kpi-icon">⚠️</div></div><div><div class="kpi-value">18</div><div class="kpi-label">Reorder Alerts</div></div></div>
            <div class="kpi-card orange"><div class="kpi-top"><div class="kpi-icon">📋</div></div><div><div class="kpi-value">₹12.5L</div><div class="kpi-label">Pending POs</div></div></div>
        </div>
    </div>

    `,
'''

# Find a good place to insert - after hrm module, before finance
# Look for finance: `
old_finance = '''    finance: `
    <div class="page-header">'''

content = content.replace(old_finance, inventory_module + old_finance)

# Write the modified content back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Inventory module added successfully!")

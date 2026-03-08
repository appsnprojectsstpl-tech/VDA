import sys
import re

file_path = "e:/Vedavathi/dashboard/app.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

vermi_start_idx = content.find("    vermi: `")
if vermi_start_idx == -1:
    print("Cannot find 'vermi: `'")
    sys.exit(1)

tree_start_idx = content.find("    tree: `", vermi_start_idx)
if tree_start_idx == -1:
    print("Cannot find 'tree: `'")
    sys.exit(1)

# The full correct VPMS HTML
vpms_html = r'''
    <div class="page-header">
       <div class="page-title">🌿 Vermicompost Plant Management</div>       
       <div class="page-subtitle">From Waste to Wealth - Complete Plant Control</div>
   </div>
   <div class="dairy-nav">
     <button class="dairy-tab-btn active" onclick="switchVpmsTab('vpms-dash',this)">🏠 Dashboard</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-worm',this)">🐛 Worms</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-beds',this)">🛏️ Beds</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-raw',this)">🌾 Raw Mat.</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-prod',this)">🏭 Production</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-qc',this)">🔬 QC</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-sales',this)">💰 Sales</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-fin',this)">💵 Finance</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-hr',this)">👷 Workers</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-equip',this)">🔧 Equipment</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-env',this)">🌡️ Environment</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-analy',this)">📊 Reports</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-cfg',this)">⚙️ Settings</button>
     <button class="dairy-tab-btn" onclick="switchVpmsTab('vpms-app',this)">📱 App</button>
   </div>

   <!-- TAB 1: DASHBOARD -->
   <div id="vpms-dash" class="dairy-pane active">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🌿 Dashboard Overview</h3>
             <span class="pill pill-green">📅 Today: 15 Mar 2025</span>
         </div>
         <div class="kpi-grid" style="margin-top:20px;">
             <div class="kpi-card teal"><div class="kpi-top"><div class="kpi-icon">🛏️</div></div><div><div class="kpi-value">48</div><div class="kpi-label">Active Beds</div></div></div>
             <div class="kpi-card blue"><div class="kpi-top"><div class="kpi-icon">🐛</div></div><div><div class="kpi-value">850 Kg</div><div class="kpi-label">Worm Stock</div></div></div>
             <div class="kpi-card orange"><div class="kpi-top"><div class="kpi-icon">🟡</div></div><div><div class="kpi-value">12</div><div class="kpi-label">Ready to Harvest</div></div></div>
             <div class="kpi-card emerald"><div class="kpi-top"><div class="kpi-icon">💰</div></div><div><div class="kpi-value">₹24,500</div><div class="kpi-label">Today's Revenue</div></div></div>
             
             <div class="kpi-card amber"><div class="kpi-top"><div class="kpi-icon">🌾</div></div><div><div class="kpi-value">12 Ton</div><div class="kpi-label">Raw Mat. Stock</div></div></div>
             <div class="kpi-card green"><div class="kpi-top"><div class="kpi-icon">📦</div></div><div><div class="kpi-value">8.5 Ton</div><div class="kpi-label">Finished Product</div></div></div>
             <div class="kpi-card red"><div class="kpi-top"><div class="kpi-icon">📦</div></div><div><div class="kpi-value">15</div><div class="kpi-label">Pending Orders</div></div></div>
             <div class="kpi-card purple"><div class="kpi-top"><div class="kpi-icon">👷</div></div><div><div class="kpi-value">22/25</div><div class="kpi-label">Workers Present</div></div></div>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>🔔 Alerts & Reminders</h4>
                 <div style="background:rgba(255,165,0,0.1); border-left:4px solid var(--orange); padding:10px; margin-bottom:10px; border-radius:4px;">
                     <b>Action Required</b><br><span style="font-size:0.85rem;">Bed #12 ready for harvest.</span>
                 </div>
                 <div style="background:rgba(255,0,0,0.1); border-left:4px solid var(--red); padding:10px; margin-bottom:10px; border-radius:4px;">
                     <b>Low Stock Alert</b><br><span style="font-size:0.85rem;">Low cow dung stock detected in Yard A.</span>
                 </div>
                 <div style="background:rgba(0,188,212,0.1); border-left:4px solid var(--teal); padding:10px; border-radius:4px;">
                     <b>Payment Due</b><br><span style="font-size:0.85rem;">Payment due from Sharma Agri.</span>
                 </div>
             </div>
             <div class="card">
                 <h4>🌡️ Environmental (Live)</h4>
                 <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px dashed rgba(255,255,255,0.1);">
                     <span>Temperature (Zone A)</span><span style="color:var(--green); font-weight:bold;">28°C ✅</span>
                 </div>
                 <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px dashed rgba(255,255,255,0.1);">
                     <span>Moisture Level</span><span style="color:var(--green); font-weight:bold;">65% ✅</span>
                 </div>
                 <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px dashed rgba(255,255,255,0.1);">
                     <span>pH Level</span><span style="color:var(--green); font-weight:bold;">7.2 ✅</span>
                 </div>
                 <div style="display:flex; justify-content:space-between; padding:10px 0;">
                     <span>Humidity</span><span style="color:var(--green); font-weight:bold;">70% ✅</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 2: WORM MANAGEMENT -->
   <div id="vpms-worm" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🐛 Worm Species & Inventory</h3>
             <button class="clean-btn">Record Health Check</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Worm Stock Distribution</h4>
                 <table class="data-table">
                     <tr><th>Species Name</th><th>Zone/Bed</th><th>Stock (Kg)</th><th>Health</th></tr>
                     <tr><td>Eisenia fetida (Red Wiggler)</td><td>Zone A</td><td>450 Kg</td><td><span class="pill pill-green">Excellent</span></td></tr>
                     <tr><td>Eudrilus eugeniae (Nightcrawler)</td><td>Zone B</td><td>200 Kg</td><td><span class="pill pill-green">Good</span></td></tr>
                     <tr><td>Perionyx excavatus (Indian Blue)</td><td>Zone C</td><td>150 Kg</td><td><span class="pill pill-amber">Monitor</span></td></tr>
                     <tr><td>Lumbricus rubellus (Red Worm)</td><td>Breeding</td><td>50 Kg</td><td><span class="pill pill-green">Growing</span></td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Breeding & Health Dynamics</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--teal);">
                     <b>Breeding Activity Focus</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Bed #1-5: High cocoon count recorded yesterday. Reproduction rate nominal (+12%).</span>
                 </div>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border-left:4px solid var(--orange);">
                     <b>Pest/Predator Log</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Red Ants detected near Bed #18. Organic repellent application scheduled.</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 3: BED MANAGEMENT -->
   <div id="vpms-beds" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🛏️ Bed / Cycle Management</h3>
             <button class="clean-btn">+ Start New Bed Cycle</button>
         </div>
         <div class="card" style="margin-top:20px;">
             <h4>Active Composting Cycles</h4>
             <table class="data-table">
                 <tr><th>Bed ID</th><th>Type</th><th>Cycle Stage</th><th>Days Elapsed</th><th>Temp/Moisture</th><th>Status</th></tr>
                 <tr><td>B-101</td><td>Raised Tank</td><td>Stage 4: Active Compost</td><td>22/45 Days</td><td>28°C / 65%</td><td><span class="pill pill-green">Processing</span></td></tr>
                 <tr><td>B-102</td><td>Raised Tank</td><td>Stage 5: Maturation</td><td>38/45 Days</td><td>26°C / 60%</td><td><span class="pill pill-amber">Ready Soon</span></td></tr>
                 <tr><td>B-103</td><td>Ground Heap</td><td>Stage 6: Harvesting</td><td>45/45 Days</td><td>25°C / 55%</td><td><span class="pill pill-blue">Harvesting</span></td></tr>
                 <tr><td>B-104</td><td>Bin System</td><td>Stage 2: Worm Intro</td><td>03/45 Days</td><td>29°C / 70%</td><td><span class="pill pill-green">Processing</span></td></tr>
             </table>
         </div>
      </div>
   </div>

   <!-- TAB 4: RAW MATERIAL MANAGEMENT -->
   <div id="vpms-raw" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🌾 Raw Material Procurement</h3>
             <button class="clean-btn">+ Log Material Inward</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Current Yard Stock</h4>
                 <table class="data-table">
                     <tr><th>Material Type</th><th>Category</th><th>Current Stock</th><th>Quality</th></tr>
                     <tr><td>Fresh Cow Dung</td><td>Primary</td><td>8 Ton</td><td><span class="pill pill-green">Good</span></td></tr>
                     <tr><td>Sugarcane Bagasse</td><td>Agri Waste</td><td>2.5 Ton</td><td><span class="pill pill-green">Good</span></td></tr>
                     <tr><td>Dry Leaves/Grass</td><td>Green Waste</td><td>1.5 Ton</td><td><span class="pill pill-green">Good</span></td></tr>
                     <tr><td>Neem Cake Additive</td><td>Amendment</td><td>200 Kg</td><td><span class="pill pill-green">Good</span></td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Pre-Processing & Supply Chain</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--blue);">
                     <b>Pre-Composting Yard 1</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Batch #82: Cow Dung + Bagasse mix. Aerobic decomposition day 12 (Target: 15).</span>
                 </div>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border-left:4px solid var(--teal);">
                     <b>Upcoming Deliveries</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">4 Tons cow dung expected today 16:00 Hrs via Supplier "Sharma Dairy".</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 5: PRODUCTION & HARVESTING -->
   <div id="vpms-prod" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🏭 Production & Harvesting</h3>
             <button class="clean-btn">Log Yield/Harvest</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Yield Records (Last 7 Days)</h4>
                 <table class="data-table">
                     <tr><th>Date</th><th>Bed ID</th><th>Gross Yield</th><th>Net Vermicompost</th><th>Vermiwash (L)</th></tr>
                     <tr><td>15 Mar</td><td>B-042</td><td>220 Kg</td><td>190 Kg</td><td>15 L</td></tr>
                     <tr><td>14 Mar</td><td>B-015</td><td>250 Kg</td><td>210 Kg</td><td>18 L</td></tr>
                     <tr><td>13 Mar</td><td>B-088</td><td>190 Kg</td><td>160 Kg</td><td>10 L</td></tr>
                     <tr><td>12 Mar</td><td>B-003</td><td>210 Kg</td><td>185 Kg</td><td>12 L</td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Sifting, Grading & Packaging</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--teal);">
                     <b>Sifting Unit Status</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Machine S-1 is active. Currently processing B-042 yield. Est. completion: 14:00.</span>
                 </div>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border-left:4px solid var(--green);">
                     <b>Packaging Status</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Packed 150 bags of 50Kg today. 80 bags of 5Kg premium pack.</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 6: QUALITY CONTROL & TESTING -->
   <div id="vpms-qc" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🔬 Quality Control & Testing</h3>
             <button class="clean-btn">Enter Lab Results</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Recent Batch Analysis</h4>
                 <table class="data-table">
                     <tr><th>Batch ID</th><th>N-P-K Ratio</th><th>pH Profile</th><th>Status</th></tr>
                     <tr><td>VP-302</td><td>1.5 : 0.8 : 0.8</td><td>7.1</td><td><span class="pill pill-green">Passed</span></td></tr>
                     <tr><td>VP-301</td><td>1.4 : 0.7 : 0.8</td><td>6.9</td><td><span class="pill pill-green">Passed</span></td></tr>
                     <tr><td>VP-300</td><td>1.0 : 0.5 : 0.5</td><td>6.5</td><td><span class="pill pill-amber">Sub-Par</span></td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Moisture & Pathogen Reports</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--blue);">
                     <b>Final Moisture Control</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Batch VP-302 moisture levels stable at 25% (Target < 30%). Ideal for shelf life.</span>
                 </div>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border-left:4px solid var(--green);">
                     <b>Pathogen Clearance</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">E.coli and Salmonella tests negative for VP-301 & VP-302. FCO Standards met.</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 7: SALES & DISTRIBUTION -->
   <div id="vpms-sales" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">💰 Sales & Distribution</h3>
             <button class="clean-btn">+ New Order</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Active Orders & Dispatch</h4>
                 <table class="data-table">
                     <tr><th>Order ID</th><th>Customer</th><th>Product</th><th>Qty</th><th>Status</th></tr>
                     <tr><td>ORD-092</td><td>GreenTech Farms</td><td>Bulk Vermi</td><td>2 Ton</td><td><span class="pill pill-green">Dispatched</span></td></tr>
                     <tr><td>ORD-093</td><td>Local Nursery</td><td>50Kg Bags</td><td>20 Bags</td><td><span class="pill pill-amber">Packing</span></td></tr>
                     <tr><td>ORD-094</td><td>Eco Gardeners</td><td>5Kg Premium</td><td>50 Bags</td><td><span class="pill pill-blue">Confirmed</span></td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Pricing & Analytics</h4>
                 <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
                     <div style="display:flex; justify-content:space-between; padding:10px; background:rgba(255,255,255,0.02); border-left:3px solid var(--teal);">
                         <span>B2B Bulk Price</span><strong>₹5.00 / Kg</strong>
                     </div>
                     <div style="display:flex; justify-content:space-between; padding:10px; background:rgba(255,255,255,0.02); border-left:3px solid var(--blue);">
                         <span>Retail 50Kg Bag Price</span><strong>₹300.00 / Bag</strong>
                     </div>
                     <div style="display:flex; justify-content:space-between; padding:10px; background:rgba(255,255,255,0.02); border-left:3px solid var(--green);">
                         <span>Margin per Ton</span><strong style="color:var(--green)">~35%</strong>
                     </div>
                     <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:4px; margin-top:10px; font-size:0.9rem; color:var(--text-muted);">
                         This month, top product is "Bulk Vermi B2B". Highest demand from local organic farms.
                     </div>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 8: FINANCE & ACCOUNTING -->
   <div id="vpms-fin" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">💵 Finance & Accounting</h3>
             <button class="clean-btn">Add Transaction</button>
         </div>
         <div class="kpi-grid" style="margin-top:20px;">
             <div class="kpi-card green"><div class="kpi-top"><div class="kpi-icon">💰</div></div><div><div class="kpi-value">₹4.2L</div><div class="kpi-label">Revenue (MTD)</div></div></div>
             <div class="kpi-card red"><div class="kpi-top"><div class="kpi-icon">📉</div></div><div><div class="kpi-value">₹1.5L</div><div class="kpi-label">Expenses (MTD)</div></div></div>
             <div class="kpi-card emerald"><div class="kpi-top"><div class="kpi-icon">📈</div></div><div><div class="kpi-value">₹2.7L</div><div class="kpi-label">Net Profit (MTD)</div></div></div>
             <div class="kpi-card orange"><div class="kpi-top"><div class="kpi-icon">⏳</div></div><div><div class="kpi-value">₹45k</div><div class="kpi-label">Receivables</div></div></div>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Recent Transactions</h4>
                 <table class="data-table">
                     <tr><th>Date</th><th>Type</th><th>Category</th><th>Amount</th></tr>
                     <tr><td>15 Mar</td><td><span style="color:var(--green)">Income</span></td><td>Sales - ORD-092</td><td>₹30,000</td></tr>
                     <tr><td>14 Mar</td><td><span style="color:var(--red)">Expense</span></td><td>Raw Mat - Cow Dung</td><td>₹12,000</td></tr>
                     <tr><td>14 Mar</td><td><span style="color:var(--green)">Income</span></td><td>Sales - Retail</td><td>₹8,000</td></tr>
                     <tr><td>12 Mar</td><td><span style="color:var(--red)">Expense</span></td><td>Equipment Maint.</td><td>₹4,500</td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Cost Breakdown</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--orange);">
                     <b>Major Expense Headers</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">劳 Labor: 45% | 🚜 Raw Material: 30% | ⚡ Utilities: 15% | 📦 Packaging: 10%</span>
                 </div>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border-left:4px solid var(--teal);">
                     <b>Cash Flow Alert</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Payroll clearing scheduled for 1st of next month (Est. ₹85,000). Ensure adequate liquidity.</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 9: WORKER MANAGEMENT (HR) -->
   <div id="vpms-hr" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">👷 Worker / Labor Management</h3>
             <button class="clean-btn">Mark Attendance</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Today's Shift Roster</h4>
                 <table class="data-table">
                     <tr><th>Worker ID</th><th>Name</th><th>Role</th><th>Shift Area</th><th>Clock-in</th></tr>
                     <tr><td>W-102</td><td>Raju T.</td><td>Sifting Operator</td><td>Processing Unit</td><td><span class="pill pill-green">08:00 AM</span></td></tr>
                     <tr><td>W-105</td><td>Suresh K.</td><td>Bed Maintenance</td><td>Zone A</td><td><span class="pill pill-green">08:15 AM</span></td></tr>
                     <tr><td>W-112</td><td>Mahesh M.</td><td>Loading/Unloading</td><td>Yard</td><td><span class="pill pill-red">Absent</span></td></tr>
                     <tr><td>W-115</td><td>Sunita P.</td><td>Packaging</td><td>Packing Unit</td><td><span class="pill pill-green">08:05 AM</span></td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Performance & Safety</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--teal);">
                     <b>Shift Analytics</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Overall attendance 88% this week. Productivity metrics meeting targets in Sifting unit.</span>
                 </div>
                 <div style="background:rgba(255,165,0,0.1); padding:10px; border-radius:8px; border-left:4px solid var(--orange);">
                     <b>Safety Briefing</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Mandatory PPE check for loaders scheduled after lunch. Gloves & masks supply replenished.</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 10: EQUIPMENT & INFRASTRUCTURE -->
   <div id="vpms-equip" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🔧 Equipment & Infrastructure</h3>
             <button class="clean-btn">Log Maintenance Incident</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Machinery Status</h4>
                 <table class="data-table">
                     <tr><th>Machine ID</th><th>Type</th><th>Status</th><th>Last Service</th><th>Next Due</th></tr>
                     <tr><td>TRC-01</td><td>Tractor Loader</td><td><span class="pill pill-green">Active</span></td><td>01 Mar 25</td><td>01 Jun 25</td></tr>
                     <tr><td>SIFT-01</td><td>Rotary Sifter A</td><td><span class="pill pill-green">Active</span></td><td>15 Feb 25</td><td>15 Apr 25</td></tr>
                     <tr><td>SIFT-02</td><td>Rotary Sifter B</td><td><span class="pill pill-amber">Maintenance</span></td><td>--</td><td>Today</td></tr>
                     <tr><td>PACK-01</td><td>Bagging Machine</td><td><span class="pill pill-green">Active</span></td><td>10 Mar 25</td><td>10 May 25</td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Infrastructure Upkeep</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--blue);">
                     <b>Shed / Roof Status</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Zone C shading nets repaired yesterday. Micro-sprinkler system lines flushed.</span>
                 </div>
                 <div style="background:rgba(255,0,0,0.1); padding:10px; border-radius:8px; border-left:4px solid var(--red);">
                     <b>Alerts</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Water Pump 2 (Yard B) showing abnormal pressure drop. Technician notified.</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 11: ENVIRONMENTAL MONITORING -->
   <div id="vpms-env" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">🌡️ IoT Environmental Monitoring</h3>
         </div>
         <div class="kpi-grid" style="margin-top:20px;">
             <div class="kpi-card teal"><div class="kpi-top"><div class="kpi-icon">🌡️</div></div><div><div class="kpi-value">26.5°C</div><div class="kpi-label">Ambient Temp</div></div></div>
             <div class="kpi-card blue"><div class="kpi-top"><div class="kpi-icon">💧</div></div><div><div class="kpi-value">68%</div><div class="kpi-label">Ambient Humidity</div></div></div>
             <div class="kpi-card orange"><div class="kpi-top"><div class="kpi-icon">☀️</div></div><div><div class="kpi-value">Normal</div><div class="kpi-label">Light Exposure</div></div></div>
             <div class="kpi-card green"><div class="kpi-top"><div class="kpi-icon">🌬️</div></div><div><div class="kpi-value">Good</div><div class="kpi-label">Aeration/Wind</div></div></div>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Zone Heatmap Overview</h4>
                 <table class="data-table">
                     <tr><th>Sensor ID</th><th>Zone</th><th>Local Temp</th><th>Local Moisture</th><th>Status</th></tr>
                     <tr><td>SN-Z1</td><td>Zone A</td><td>28°C</td><td>70%</td><td><span class="pill pill-green">Optimal</span></td></tr>
                     <tr><td>SN-Z2</td><td>Zone B</td><td>29°C</td><td>65%</td><td><span class="pill pill-green">Optimal</span></td></tr>
                     <tr><td>SN-Z3</td><td>Zone C</td><td>31°C</td><td>50%</td><td><span class="pill pill-orange">Warning</span></td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>Automated Actuators</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--teal);">
                     <b>Sprinkler System</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Zone C sprinklers automatically triggered at 11:30 AM due to low moisture threshold.</span>
                 </div>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border-left:4px solid var(--blue);">
                     <b>Ventilation Fans</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Main shed ventilation activated. Running on normal duty cycle (15 min/hr).</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 12: REPORTS & ANALYTICS -->
   <div id="vpms-analy" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">📊 Reports & Analytics</h3>
             <div><button class="clean-btn">Export PDF</button> <button class="clean-btn">Export Excel</button></div>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Yield vs Goal (Monthly)</h4>
                 <div style="height:200px; display:flex; align-items:flex-end; gap:10px; padding-top:20px;">
                     <!-- Simulated Bar Chart -->
                     <div style="width:15%; background:var(--teal); height:60%; border-radius:4px 4px 0 0; text-align:center; color:#fff; font-size:10px; padding-top:5px;">Oct<br>28T</div>
                     <div style="width:15%; background:var(--teal); height:65%; border-radius:4px 4px 0 0; text-align:center; color:#fff; font-size:10px; padding-top:5px;">Nov<br>31T</div>
                     <div style="width:15%; background:var(--teal); height:80%; border-radius:4px 4px 0 0; text-align:center; color:#fff; font-size:10px; padding-top:5px;">Dec<br>38T</div>
                     <div style="width:15%; background:var(--teal); height:85%; border-radius:4px 4px 0 0; text-align:center; color:#fff; font-size:10px; padding-top:5px;">Jan<br>41T</div>
                     <div style="width:15%; background:var(--teal); height:95%; border-radius:4px 4px 0 0; text-align:center; color:#fff; font-size:10px; padding-top:5px;">Feb<br>45T</div>
                     <div style="width:15%; background:var(--green); height:40%; border-radius:4px 4px 0 0; text-align:center; color:#fff; font-size:10px; padding-top:5px;">Mar<br>20T</div>
                 </div>
             </div>
             <div class="card">
                 <h4>System Analytics</h4>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid var(--blue);">
                     <b>Conversion Efficiency</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Current raw material to finished compost conversion ratio: 42% (Industry Avg is 35-40%).</span>
                 </div>
                 <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border-left:4px solid var(--teal);">
                     <b>Cost per Kg Analysis</b><br>
                     <span style="font-size:0.85rem; color:var(--text-muted);">Production Cost: ₹2.40/Kg | Selling Price (Avg): ₹5.80/Kg | Margin: ₹3.40/Kg.</span>
                 </div>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 13: SETTINGS & ADMINISTRATION -->
   <div id="vpms-cfg" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">⚙️ Settings & Administration</h3>
             <button class="clean-btn">Save Configuration</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>IoT Sensor Thresholds</h4>
                 <div class="form-grid">
                     <label>Max Bed Temp (°C) <input type="number" value="32" style="width:100%; padding:8px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1); color:#fff; border-radius:4px;"></label>
                     <label>Min Bed Temp (°C) <input type="number" value="20" style="width:100%; padding:8px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1); color:#fff; border-radius:4px;"></label>
                     <label>Target Moisture (%) <input type="number" value="65" style="width:100%; padding:8px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1); color:#fff; border-radius:4px;"></label>
                     <label>Sprinkler Duration (Min) <input type="number" value="15" style="width:100%; padding:8px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1); color:#fff; border-radius:4px;"></label>
                 </div>
             </div>
             <div class="card">
                 <h4>User Access & Roles</h4>
                 <table class="data-table">
                     <tr><th>User</th><th>Role</th><th>Access Level</th><th>Action</th></tr>
                     <tr><td>Ravi Kumar</td><td>Plant Manager</td><td>Full Access</td><td><button class="clean-btn" style="padding:2px 8px; font-size:0.8rem;">Edit</button></td></tr>
                     <tr><td>Anita M.</td><td>Lab/QC Tech</td><td>QC, Harvest</td><td><button class="clean-btn" style="padding:2px 8px; font-size:0.8rem;">Edit</button></td></tr>
                     <tr><td>Sunil P.</td><td>Sales Agent</td><td>Sales Only</td><td><button class="clean-btn" style="padding:2px 8px; font-size:0.8rem;">Edit</button></td></tr>
                 </table>
             </div>
         </div>
      </div>
   </div>

   <!-- TAB 14: MOBILE APP / FIELD LOGGING -->
   <div id="vpms-app" class="dairy-pane" style="display:none;">
      <div class="glass-dark" style="padding: 20px; border-radius:12px;">
         <div style="display:flex; justify-content:space-between; align-items:center;">
             <h3 style="margin-top:0;">📱 Mobile App Integration</h3>
             <button class="clean-btn">Push Update to Devices</button>
         </div>
         <div class="chart-grid" style="margin-top:20px;">
             <div class="card">
                 <h4>Connected Devices (Field App)</h4>
                 <table class="data-table">
                     <tr><th>Device ID</th><th>Assigned To</th><th>Sync Status</th><th>Last Seen</th></tr>
                     <tr><td>TAB-A1 (Tablet)</td><td>QC Department</td><td><span class="pill pill-green">Synced</span></td><td>10 mins ago</td></tr>
                     <tr><td>TAB-A2 (Tablet)</td><td>Sifting Unit</td><td><span class="pill pill-green">Synced</span></td><td>2 mins ago</td></tr>
                     <tr><td>MOB-05 (Phone)</td><td>Yard Supervisor</td><td><span class="pill pill-amber">Syncing...</span></td><td>Just now</td></tr>
                 </table>
             </div>
             <div class="card">
                 <h4>App Feature Module Status</h4>
                 <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px dashed rgba(255,255,255,0.1);">
                     <span>QR Code Bed Scanning</span><span style="color:var(--green); font-weight:bold;">Enabled</span>
                 </div>
                 <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px dashed rgba(255,255,255,0.1);">
                     <span>Offline Offline Logging</span><span style="color:var(--green); font-weight:bold;">Enabled</span>
                 </div>
                 <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px dashed rgba(255,255,255,0.1);">
                     <span>Push Notifications</span><span style="color:var(--green); font-weight:bold;">Enabled</span>
                 </div>
                 <div style="display:flex; justify-content:space-between; padding:10px 0;">
                     <span>GPS Yard Tracking</span><span style="color:var(--blue); font-weight:bold;">Beta Version</span>
                 </div>
             </div>
         </div>
      </div>
   </div>
`
'''

new_content = content[:vermi_start_idx] + "    vermi: `" + vpms_html + ",\n" + content[tree_start_idx:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("SUCCESS - VPMS block rebuilt completely.")

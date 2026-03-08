const fs = require('fs');
const filePath = 'e:/Vedavathi/dashboard/app.js';
let content = fs.readFileSync(filePath, 'utf8');

const replacement = '    vermi: \\n' +
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
   \,
;

const startIndex = content.indexOf('    vermi: ');
const endIndex = content.indexOf('    tree: ');

if (startIndex !== -1 && endIndex !== -1) {
    content = content.substring(0, startIndex) + replacement + content.substring(endIndex);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('SUCCESS');
} else {
    console.log('FAILED TO FIND MARKERS');
}

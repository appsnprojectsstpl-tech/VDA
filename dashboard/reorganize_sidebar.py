"""
Reorganize sidebar categories in index.html
Replaces the old category structure with a cleaner organization
"""

import re

# Read the current index.html
with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# New sidebar structure - organized by function
new_sidebar = '''            <div class="sidebar-nav" role="menubar">

                <div class="menu-item active" data-page="overview" role="menuitem" tabindex="0" aria-current="page">
                    <div class="nav-icon" aria-hidden="true">📊</div>
                    <div class="nav-label">Overview</div>
                </div>

                <!-- ═══ ENERGY ═══ -->
                <div class="menu-group-header" onclick="toggleSidebarGroup(this)" role="menuitem" tabindex="0"
                    aria-expanded="true" aria-controls="energy-menu">
                    <span class="nav-group-icon" aria-hidden="true">⚡</span>
                    <span class="nav-group-title">ENERGY</span>
                    <span class="nav-group-count">7</span>
                    <span class="nav-group-arrow">▼</span>
                </div>
                <div class="menu-group-items" id="energy-menu" role="menu">
                    <div class="menu-item" data-page="solar" role="menuitem" tabindex="0">
                        <div class="nav-icon">☀️</div>
                        <div class="nav-label">Solar Capacity</div>
                    </div>
                    <div class="menu-item" data-page="wind" role="menuitem" tabindex="0">
                        <div class="nav-icon">💨</div>
                        <div class="nav-label">Wind Generation</div>
                    </div>
                    <div class="menu-item" data-page="hydro" role="menuitem" tabindex="0">
                        <div class="nav-icon">🌊</div>
                        <div class="nav-label">Hydropower</div>
                    </div>
                    <div class="menu-item" data-page="biogas" role="menuitem" tabindex="0">
                        <div class="nav-icon">🔥</div>
                        <div class="nav-label">Biogas Plants</div>
                    </div>
                    <div class="menu-item" data-page="hydrogen" role="menuitem" tabindex="0">
                        <div class="nav-icon">🫧</div>
                        <div class="nav-label">Green Hydrogen</div>
                    </div>
                    <div class="menu-item" data-page="kinetic" role="menuitem" tabindex="0">
                        <div class="nav-icon">⚡</div>
                        <div class="nav-label">Kinetic Energy</div>
                    </div>
                    <div class="menu-item" data-page="grid" role="menuitem" tabindex="0">
                        <div class="nav-icon">🕸️</div>
                        <div class="nav-label">Smart Grid AI</div>
                    </div>
                </div>

                <!-- ═══ AGRICULTURE & ANIMAL HUSBANDRY ═══ -->
                <div class="menu-group-header" onclick="toggleSidebarGroup(this)" role="menuitem" tabindex="0"
                    aria-expanded="true" aria-controls="agri-menu">
                    <span class="nav-group-icon" aria-hidden="true">🌾</span>
                    <span class="nav-group-title">AGRI & ANIMAL</span>
                    <span class="nav-group-count">8</span>
                    <span class="nav-group-arrow">▼</span>
                </div>
                <div class="menu-group-items" id="agri-menu" role="menu">
                    <div class="menu-item" data-page="cattle" role="menuitem" tabindex="0">
                        <div class="nav-icon">🐄</div>
                        <div class="nav-label">Smart Dairy</div>
                        <div class="nav-badge">2</div>
                    </div>
                    <div class="menu-item" data-page="poultry" role="menuitem" tabindex="0">
                        <div class="nav-icon">🐔</div>
                        <div class="nav-label">Poultry Hub</div>
                    </div>
                    <div class="menu-item" data-page="aqua" role="menuitem" tabindex="0">
                        <div class="nav-icon">🐟</div>
                        <div class="nav-label">Aquaculture Hub</div>
                    </div>
                    <div class="menu-item" data-page="vermi" role="menuitem" tabindex="0">
                        <div class="nav-icon">🪱</div>
                        <div class="nav-label">Vermicompost</div>
                    </div>
                    <div class="menu-item" data-page="tree" role="menuitem" tabindex="0">
                        <div class="nav-icon">🌳</div>
                        <div class="nav-label">TreeSwasthya AI</div>
                    </div>
                    <div class="menu-item" data-page="carbon" role="menuitem" tabindex="0">
                        <div class="nav-icon">🌍</div>
                        <div class="nav-label">Carbon Hub</div>
                    </div>
                    <div class="menu-item" data-page="paint" role="menuitem" tabindex="0">
                        <div class="nav-icon">🎨</div>
                        <div class="nav-label">Bio-Paints</div>
                    </div>
                </div>

                <!-- ═══ SALES & COMMERCE ═══ -->
                <div class="menu-group-header collapsed" onclick="toggleSidebarGroup(this)" role="menuitem" tabindex="0"
                    aria-expanded="false" aria-controls="sales-menu">
                    <span class="nav-group-icon" aria-hidden="true">🤝</span>
                    <span class="nav-group-title">SALES & COMMERCE</span>
                    <span class="nav-group-count">3</span>
                    <span class="nav-group-arrow">▶</span>
                </div>
                <div class="menu-group-items" id="sales-menu" style="display:none" role="menu">
                    <div class="menu-item" data-page="crm" role="menuitem" tabindex="0">
                        <div class="nav-icon">🤝</div>
                        <div class="nav-label">CRM & Contracts</div>
                    </div>
                    <div class="menu-item" data-page="tourism" role="menuitem" tabindex="0">
                        <div class="nav-icon">🏕️</div>
                        <div class="nav-label">Agri-Tourism</div>
                    </div>
                    <div class="menu-item" data-page="booking" role="menuitem" tabindex="0">
                        <div class="nav-icon">📅</div>
                        <div class="nav-label">Bookings</div>
                    </div>
                </div>

                <!-- ═══ OPERATIONS ═══ -->
                <div class="menu-group-header collapsed" onclick="toggleSidebarGroup(this)" role="menuitem" tabindex="0"
                    aria-expanded="false" aria-controls="ops-menu">
                    <span class="nav-group-icon" aria-hidden="true">🛠️</span>
                    <span class="nav-group-title">OPERATIONS</span>
                    <span class="nav-group-count">5</span>
                    <span class="nav-group-arrow">▶</span>
                </div>
                <div class="menu-group-items" id="ops-menu" style="display:none" role="menu">
                    <div class="menu-item" data-page="logistics" role="menuitem" tabindex="0">
                        <div class="nav-icon">🚚</div>
                        <div class="nav-label">LogiTrack</div>
                    </div>
                    <div class="menu-item" data-page="water" role="menuitem" tabindex="0">
                        <div class="nav-icon">🚰</div>
                        <div class="nav-label">Hydrosphere</div>
                    </div>
                    <div class="menu-item" data-page="inventory" role="menuitem" tabindex="0">
                        <div class="nav-icon">📦</div>
                        <div class="nav-label">Inventory</div>
                    </div>
                    <div class="menu-item" data-page="fieldservice" role="menuitem" tabindex="0">
                        <div class="nav-icon">🚜</div>
                        <div class="nav-label">Field Service</div>
                    </div>
                    <div class="menu-item" data-page="command" role="menuitem" tabindex="0">
                        <div class="nav-icon">🛡️</div>
                        <div class="nav-label">Command 360</div>
                    </div>
                </div>

                <!-- ═══ ADMIN & MANAGEMENT ═══ -->
                <div class="menu-group-header" onclick="toggleSidebarGroup(this)" role="menuitem" tabindex="0"
                    aria-expanded="true" aria-controls="admin-menu">
                    <span class="nav-group-icon" aria-hidden="true">🏢</span>
                    <span class="nav-group-title">ADMIN & MGMT</span>
                    <span class="nav-group-count">7</span>
                    <span class="nav-group-arrow">▼</span>
                </div>
                <div class="menu-group-items" id="admin-menu" role="menu">
                    <div class="menu-item" data-page="hrm" role="menuitem" tabindex="0">
                        <div class="nav-icon">👥</div>
                        <div class="nav-label">HRM & Payroll</div>
                    </div>
                    <div class="menu-item" data-page="finance2" role="menuitem" tabindex="0">
                        <div class="nav-icon">💰</div>
                        <div class="nav-label">Finance & Accts</div>
                    </div>
                    <div class="menu-item" data-page="dms" role="menuitem" tabindex="0">
                        <div class="nav-icon">📁</div>
                        <div class="nav-label">Documents</div>
                    </div>
                    <div class="menu-item" data-page="bi" role="menuitem" tabindex="0">
                        <div class="nav-icon">📊</div>
                        <div class="nav-label">BI & Analytics</div>
                    </div>
                    <div class="menu-item" data-page="workflow" role="menuitem" tabindex="0">
                        <div class="nav-icon">✅</div>
                        <div class="nav-label">Workflow</div>
                    </div>
                    <div class="menu-item" data-page="ticketing" role="menuitem" tabindex="0">
                        <div class="nav-icon">🎫</div>
                        <div class="nav-label">Helpdesk</div>
                    </div>
                    <div class="menu-item" data-page="trust" role="menuitem" tabindex="0">
                        <div class="nav-icon">📜</div>
                        <div class="nav-label">Vedavathi Trust</div>
                    </div>
                </div>

                <!-- ═══ SERVICES ═══ -->
                <div class="menu-group-header collapsed" onclick="toggleSidebarGroup(this)" role="menuitem" tabindex="0"
                    aria-expanded="false" aria-controls="services-menu">
                    <span class="nav-group-icon" aria-hidden="true">🏥</span>
                    <span class="nav-group-title">SERVICES</span>
                    <span class="nav-group-count">4</span>
                    <span class="nav-group-arrow">▶</span>
                </div>
                <div class="menu-group-items" id="services-menu" style="display:none" role="menu">
                    <div class="menu-item" data-page="vet" role="menuitem" tabindex="0">
                        <div class="nav-icon">🏥</div>
                        <div class="nav-label">Veterinary Hosp.</div>
                    </div>
                    <div class="menu-item" data-page="vedic" role="menuitem" tabindex="0">
                        <div class="nav-icon">🕉️</div>
                        <div class="nav-label">Vedic Hub</div>
                    </div>
                    <div class="menu-item" data-page="lms" role="menuitem" tabindex="0">
                        <div class="nav-icon">🎓</div>
                        <div class="nav-label">Learning</div>
                    </div>
                    <div class="menu-item" data-page="survey" role="menuitem" tabindex="0">
                        <div class="nav-icon">📋</div>
                        <div class="nav-label">Surveys</div>
                    </div>
                </div>

                <!-- ═══ PORTALS ═══ -->
                <div class="menu-group-header collapsed" onclick="toggleSidebarGroup(this)" role="menuitem" tabindex="0"
                    aria-expanded="false" aria-controls="portals-menu">
                    <span class="nav-group-icon" aria-hidden="true">🌐</span>
                    <span class="nav-group-title">PORTALS</span>
                    <span class="nav-group-count">2</span>
                    <span class="nav-group-arrow">▶</span>
                </div>
                <div class="menu-group-items" id="portals-menu" style="display:none" role="menu">
                    <div class="menu-item" data-page="farmerportal" role="menuitem" tabindex="0">
                        <div class="nav-icon">👨‍🌾</div>
                        <div class="nav-label">Farmer Portal</div>
                    </div>
                    <div class="menu-item" data-page="schemes" role="menuitem" tabindex="0">
                        <div class="nav-icon">🏛️</div>
                        <div class="nav-label">Schemes</div>
                    </div>
                </div>

            </div>'''

# Pattern to match the sidebar-nav section (from <div class="sidebar-nav"> to </div>)
# This matches from sidebar-nav start to the end of all menu groups before the closing tag
pattern = r'<div class="sidebar-nav" role="menubar">.*?</div>\s*</nav>'

# Replace with new sidebar
replacement = new_sidebar + '\n        </nav>'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the updated content
with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Sidebar reorganization complete!")
print("""
New organization:
├── ENERGY (7): solar, wind, hydro, biogas, hydrogen, kinetic, grid
├── AGRI & ANIMAL (8): cattle, poultry, aqua, vermi, tree, carbon, paint
├── SALES & COMMERCE (3): crm, tourism, booking
├── OPERATIONS (5): logistics, water, inventory, fieldservice, command
├── ADMIN & MGMT (7): hrm, finance, dms, bi, workflow, ticketing, trust
├── SERVICES (4): vet, vedic, lms, survey
└── PORTALS (2): farmerportal, schemes
""")

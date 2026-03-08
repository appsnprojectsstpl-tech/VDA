"""
Add comprehensive light theme CSS to index.css
"""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CSS = r'e:\Vedavathi\dashboard\index.css'
HTML = r'e:\Vedavathi\dashboard\index.html'

light_theme_css = '''

/* ============================================================
   COMPREHENSIVE LIGHT THEME (v7.1)
   Covers ALL UI components for proper dark → light switching
   ============================================================ */

/* --- Base background and text --- */
body.light-theme,
:root[data-theme="light"] body {
    background: #f0f4f8 !important;
    color: #1e293b !important;
}

/* --- Top Header --- */
body.light-theme .top-header {
    background: #ffffff !important;
    border-bottom: 1px solid rgba(0,0,0,0.08) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}

body.light-theme .top-header,
body.light-theme .header-left,
body.light-theme .header-center,
body.light-theme .header-right {
    color: #1e293b !important;
}

body.light-theme .header-btn,
body.light-theme .icon-btn {
    color: #475569 !important;
    background: rgba(0,0,0,0.04) !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
}

body.light-theme .header-btn:hover,
body.light-theme .icon-btn:hover {
    background: rgba(0,0,0,0.08) !important;
}

body.light-theme .search-input,
body.light-theme #globalSearch {
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
}

body.light-theme .search-input::placeholder,
body.light-theme #globalSearch::placeholder {
    color: #94a3b8 !important;
}

/* --- Sidebar --- */
body.light-theme .sidebar {
    background: #ffffff !important;
    border-right: 1px solid rgba(0,0,0,0.08) !important;
    box-shadow: 2px 0 8px rgba(0,0,0,0.04) !important;
}

body.light-theme .sidebar-logo h1,
body.light-theme .sidebar .brand-name {
    color: #0f172a !important;
}

body.light-theme .sidebar .brand-tagline,
body.light-theme .sidebar .brand-subtitle {
    color: #64748b !important;
}

body.light-theme .menu-group-header {
    color: #94a3b8 !important;
    border-bottom: 1px solid rgba(0,0,0,0.05) !important;
}

body.light-theme .menu-item {
    color: #475569 !important;
}

body.light-theme .menu-item:hover {
    background: rgba(0,0,0,0.04) !important;
    color: #0284c7 !important;
}

body.light-theme .menu-item.active {
    background: rgba(2,132,199,0.08) !important;
    color: #0284c7 !important;
    border-left-color: #0284c7 !important;
}

body.light-theme .sidebar-search input,
body.light-theme .sidebar input[type="text"] {
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
}

/* --- Main Content Area --- */
body.light-theme .main-content,
body.light-theme .page-area,
body.light-theme #page-container {
    background: #f0f4f8 !important;
}

/* --- Breadcrumbs --- */
body.light-theme #breadcrumbs,
body.light-theme .breadcrumbs,
body.light-theme .breadcrumb-home {
    color: #64748b !important;
}

body.light-theme .breadcrumb-home:hover {
    color: #0284c7 !important;
}

/* --- Page Headings --- */
body.light-theme h1,
body.light-theme h2,
body.light-theme h3,
body.light-theme .page-title,
body.light-theme .section-title {
    color: #0f172a !important;
}

body.light-theme .page-subtitle,
body.light-theme .section-subtitle {
    color: #64748b !important;
}

/* --- Tab Navigation --- */
body.light-theme .dairy-nav,
body.light-theme .vet-nav,
body.light-theme .en-nav,
body.light-theme .crm-nav,
body.light-theme .vermi-nav,
body.light-theme .tree-nav,
body.light-theme .aqua-nav,
body.light-theme .paint-nav,
body.light-theme .biogas-nav,
body.light-theme .wind-nav,
body.light-theme .solar-nav,
body.light-theme .carbon-nav,
body.light-theme .fin-nav {
    background: #ffffff !important;
    border-bottom: 1px solid rgba(0,0,0,0.08) !important;
}

body.light-theme .dairy-tab-btn,
body.light-theme .en-tbtn,
body.light-theme .vermi-tbtn,
body.light-theme .tree-tbtn,
body.light-theme .hub-more-btn {
    background: transparent !important;
    color: #475569 !important;
    border: 1px solid transparent !important;
}

body.light-theme .dairy-tab-btn:hover,
body.light-theme .en-tbtn:hover,
body.light-theme .vermi-tbtn:hover,
body.light-theme .tree-tbtn:hover,
body.light-theme .hub-more-btn:hover {
    background: rgba(0,0,0,0.04) !important;
    color: #0284c7 !important;
}

body.light-theme .dairy-tab-btn.active,
body.light-theme .en-tbtn.active,
body.light-theme .vermi-tbtn.active,
body.light-theme .tree-tbtn.active {
    background: rgba(2,132,199,0.1) !important;
    color: #0284c7 !important;
    border-color: rgba(2,132,199,0.3) !important;
    font-weight: 600 !important;
}

/* --- Cards & Panels --- */
body.light-theme .kpi-card,
body.light-theme .glass-dark,
body.light-theme .stat-card,
body.light-theme .info-card,
body.light-theme .chart-card,
body.light-theme .data-card,
body.light-theme .overview-card,
body.light-theme .summary-card,
body.light-theme [class*="-card"],
body.light-theme .card {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    color: #1e293b !important;
}

body.light-theme .kpi-value,
body.light-theme .stat-value {
    color: #0f172a !important;
}

body.light-theme .kpi-label,
body.light-theme .stat-label,
body.light-theme .card-label {
    color: #64748b !important;
}

/* --- Tables --- */
body.light-theme table {
    background: #ffffff !important;
    color: #1e293b !important;
}

body.light-theme th {
    background: #f1f5f9 !important;
    color: #475569 !important;
    border-bottom: 2px solid rgba(0,0,0,0.1) !important;
}

body.light-theme td {
    border-bottom: 1px solid rgba(0,0,0,0.06) !important;
    color: #334155 !important;
}

body.light-theme tr:hover td {
    background: rgba(0,0,0,0.02) !important;
}

/* --- Forms & Inputs --- */
body.light-theme input,
body.light-theme select,
body.light-theme textarea {
    background: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid rgba(0,0,0,0.15) !important;
}

body.light-theme input:focus,
body.light-theme select:focus,
body.light-theme textarea:focus {
    border-color: #0284c7 !important;
    box-shadow: 0 0 0 3px rgba(2,132,199,0.15) !important;
}

body.light-theme label {
    color: #475569 !important;
}

/* --- Buttons --- */
body.light-theme button {
    color: #475569 !important;
}

body.light-theme .btn-primary,
body.light-theme .action-btn {
    background: #0284c7 !important;
    color: #ffffff !important;
}

/* --- Status Badges --- */
body.light-theme .badge-success,
body.light-theme .status-optimal,
body.light-theme .status-online {
    background: rgba(22,163,74,0.1) !important;
    color: #16a34a !important;
}

body.light-theme .badge-warning {
    background: rgba(234,179,8,0.1) !important;
    color: #ca8a04 !important;
}

body.light-theme .badge-danger,
body.light-theme .badge-critical {
    background: rgba(220,38,38,0.1) !important;
    color: #dc2626 !important;
}

/* --- Sections & Containers --- */
body.light-theme .page-section,
body.light-theme .content-section,
body.light-theme .dashboard-section {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    border-radius: 12px !important;
}

/* --- Chart areas --- */
body.light-theme .chart-container,
body.light-theme .chart-placeholder {
    background: #f8fafc !important;
    color: #64748b !important;
}

/* --- Scrollbar (light) --- */
body.light-theme ::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.15) !important;
}

body.light-theme ::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.03) !important;
}

/* --- More dropdown (light) --- */
body.light-theme .hub-more-dropdown-body {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.12) !important;
}

body.light-theme .dropdown-tab-item {
    color: #475569 !important;
}

body.light-theme .dropdown-tab-item:hover {
    background: rgba(0,0,0,0.04) !important;
    color: #0284c7 !important;
}

/* --- Text general --- */
body.light-theme p,
body.light-theme span,
body.light-theme div,
body.light-theme li {
    color: inherit !important;
}

/* --- Quick Actions + Favorites dropdowns --- */
body.light-theme .quick-actions-dropdown,
body.light-theme .favorites-dropdown {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
}

/* END COMPREHENSIVE LIGHT THEME */
'''

with open(CSS, 'a', encoding='utf-8') as f:
    f.write(light_theme_css)
print('Light theme CSS appended')

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=7.1.0', h)
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=7.1.0', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)
print('Bumped to v7.1.0')

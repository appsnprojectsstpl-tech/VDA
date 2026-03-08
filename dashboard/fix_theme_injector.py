"""
Fix theme switcher by injecting a high-specificity stylesheet as the LAST child of <head>
and using !important on every property. Also rewrite ThemeManager.apply() to add/remove
this stylesheet dynamically.
"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'e:\Vedavathi\dashboard\app.js'
HTML = r'e:\Vedavathi\dashboard\index.html'

with open(JS, encoding='utf-8', errors='replace') as f:
    js = f.read()

# Add a runtime theme injector that beats ALL existing CSS
theme_injector = """

/* ============================================================
   THEME INJECTOR v7.1 — Beats all !important via runtime <style>
   ============================================================ */
(function() {
    var LIGHT_CSS_ID = 'vedavathi-light-override';

    var lightCSS = `
        /* LIGHT THEME — injected as last stylesheet — wins all battles */
        body, html { background: #f0f4f8 !important; color: #1e293b !important; }
        .sidebar { background: #ffffff !important; border-right: 1px solid #e2e8f0 !important; }
        .sidebar * { color: #475569 !important; }
        .sidebar .menu-item:hover { background: #f1f5f9 !important; color: #0284c7 !important; }
        .sidebar .menu-item.active { background: rgba(2,132,199,0.08) !important; color: #0284c7 !important; }
        .sidebar input { background: #f1f5f9 !important; color: #1e293b !important; border: 1px solid #e2e8f0 !important; }
        .menu-group-header { color: #94a3b8 !important; }
        .menu-group-header .group-count { background: rgba(0,0,0,0.06) !important; color: #64748b !important; }

        .top-header { background: #ffffff !important; border-bottom: 1px solid #e2e8f0 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important; }
        .top-header * { color: #1e293b !important; }
        .header-btn, .icon-btn { background: #f1f5f9 !important; color: #475569 !important; border: 1px solid #e2e8f0 !important; }
        .header-btn:hover, .icon-btn:hover { background: #e2e8f0 !important; }
        .search-input, #globalSearch { background: #f1f5f9 !important; color: #1e293b !important; border: 1px solid #e2e8f0 !important; }

        .main-content, .page-area, #page-container { background: #f0f4f8 !important; }

        h1, h2, h3, h4, .page-title, .section-title { color: #0f172a !important; }
        p, span, div, li, td, th, label { color: #334155 !important; }

        .dairy-nav, .vet-nav, .en-nav, .crm-nav, .vermi-nav, .tree-nav, .aqua-nav,
        .paint-nav, .biogas-nav, .wind-nav, .solar-nav, .carbon-nav, .fin-nav,
        .trust-nav, .cmd-nav, .log-nav, .water-nav, .vedic-nav {
            background: #ffffff !important; border-bottom: 1px solid #e2e8f0 !important;
        }

        .dairy-tab-btn, .en-tbtn, .vermi-tbtn, .tree-tbtn, .hub-more-btn,
        button[class*="-tab-btn"] {
            background: transparent !important; color: #475569 !important; border: 1px solid transparent !important;
        }
        .dairy-tab-btn:hover, .en-tbtn:hover, .hub-more-btn:hover,
        button[class*="-tab-btn"]:hover { background: #f1f5f9 !important; color: #0284c7 !important; }
        .dairy-tab-btn.active, .en-tbtn.active, button[class*="-tab-btn"].active {
            background: rgba(2,132,199,0.1) !important; color: #0284c7 !important;
            border-color: rgba(2,132,199,0.3) !important; font-weight: 600 !important;
        }

        .kpi-card, .glass-dark, .stat-card, .info-card, .chart-card, .data-card,
        .overview-card, .summary-card, .card, [class*="-card"] {
            background: #ffffff !important; border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important; color: #1e293b !important;
        }

        table { background: #ffffff !important; }
        th { background: #f1f5f9 !important; color: #475569 !important; border-bottom: 2px solid #e2e8f0 !important; }
        td { border-bottom: 1px solid #f1f5f9 !important; }
        tr:hover td { background: #f8fafc !important; }

        input, select, textarea { background: #ffffff !important; color: #1e293b !important; border: 1px solid #cbd5e1 !important; }
        input:focus, select:focus, textarea:focus { border-color: #0284c7 !important; box-shadow: 0 0 0 3px rgba(2,132,199,0.15) !important; }

        .page-section, .content-section, .dashboard-section {
            background: #ffffff !important; border: 1px solid #e2e8f0 !important;
        }

        .chart-container, .chart-placeholder { background: #f8fafc !important; color: #64748b !important; }

        .hub-more-dropdown-body, .quick-actions-dropdown, .favorites-dropdown {
            background: #ffffff !important; border: 1px solid #e2e8f0 !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.12) !important;
        }

        .kpi-value, .stat-value { color: #0f172a !important; }
        .kpi-label, .stat-label { color: #64748b !important; }

        .badge-success, .status-optimal { background: rgba(22,163,74,0.1) !important; color: #16a34a !important; }
        .badge-warning { background: rgba(234,179,8,0.1) !important; color: #ca8a04 !important; }
        .badge-danger { background: rgba(220,38,38,0.1) !important; color: #dc2626 !important; }

        ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15) !important; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.03) !important; }
    `;

    // Patch ThemeManager.apply to inject/remove the light stylesheet
    var _origApply = null;
    function patchThemeManager() {
        if (!window.ThemeManager) return false;
        if (window.ThemeManager._patched) return true;

        _origApply = window.ThemeManager.apply.bind(window.ThemeManager);
        window.ThemeManager.apply = function() {
            _origApply();
            var existing = document.getElementById(LIGHT_CSS_ID);
            if (!this.isDark) {
                // LIGHT mode — inject stylesheet
                if (!existing) {
                    var style = document.createElement('style');
                    style.id = LIGHT_CSS_ID;
                    style.textContent = lightCSS;
                    document.head.appendChild(style);
                }
            } else {
                // DARK mode — remove injected stylesheet
                if (existing) existing.remove();
            }
        };
        window.ThemeManager._patched = true;

        // Re-apply current theme to ensure correct state
        window.ThemeManager.apply();
        return true;
    }

    // Try immediately, retry if ThemeManager not ready yet
    if (!patchThemeManager()) {
        var attempts = 0;
        var interval = setInterval(function() {
            if (patchThemeManager() || ++attempts > 30) clearInterval(interval);
        }, 200);
    }
})();
/* END THEME INJECTOR v7.1 */
"""

if 'THEME INJECTOR v7.1' not in js:
    js += theme_injector
    with open(JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print('Theme injector appended')
else:
    print('Already present')

# Bump
with open(HTML, encoding='utf-8') as f:
    h = f.read()
h = re.sub(r'app\.js\?v=[\d.]+', 'app.js?v=7.1.1', h)
h = re.sub(r'index\.css\?v=[\d.]+', 'index.css?v=7.1.1', h)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(h)

exit_code = os.system(f'node --check "{JS}" 2>&1')
print('SYNTAX OK' if exit_code == 0 else 'SYNTAX ERROR')
print('Bumped to v7.1.1')

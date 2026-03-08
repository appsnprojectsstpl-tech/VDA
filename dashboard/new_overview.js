/**
 * COMPLETE OVERVIEW REDESIGN
 * Fresh, modern design for the Vedavathi Dashboard Overview
 * 
 * Usage: This file replaces the overview page content
 * Just add <script src="new_overview.js"></script> to your HTML
 */

(function () {
    // The completely new overview template
    window.newOverviewTemplate = `
<div class="overview-new">

    <!-- Hero Banner -->
    <div class="new-hero">
        <div class="new-hero-content">
            <div class="new-brand">
                <span class="new-brand-icon">🌿</span>
                <div class="new-brand-text">
                    <span class="new-brand-name">VEDAVATHI</span>
                    <span class="new-brand-tag">Integrated Eco-Farm</span>
                </div>
            </div>
            <div class="new-hero-desc">World's most advanced 1M cattle capacity eco-industrial complex with complete energy autonomy and zero-waste circular operations.</div>
        </div>
        <div class="new-hero-badges">
            <div class="new-badge">
                <span class="badge-emoji">⚡</span>
                <span class="badge-text">3.5+ GW</span>
                <span class="badge-sub">Energy</span>
            </div>
            <div class="new-badge">
                <span class="badge-emoji">🐄</span>
                <span class="badge-text">1M</span>
                <span class="badge-sub">Cattle</span>
            </div>
            <div class="new-badge green">
                <span class="badge-emoji">📈</span>
                <span class="badge-text">6-8 Mo</span>
                <span class="badge-sub">ROI</span>
            </div>
        </div>
    </div>

    <!-- Stats Row -->
    <div class="new-stats-row">
        <div class="new-stat-card">
            <div class="stat-header">
                <span class="stat-icon">🐄</span>
                <span class="stat-trend up">+1.2%</span>
            </div>
            <div class="stat-body">
                <div class="stat-value">1,000,000</div>
                <div class="stat-label">Total Live Cattle</div>
            </div>
            <div class="stat-footer">Across 4 operational zones</div>
        </div>
        <div class="new-stat-card">
            <div class="stat-header">
                <span class="stat-icon">⚡</span>
                <span class="stat-trend up">+4.5%</span>
            </div>
            <div class="stat-body">
                <div class="stat-value">3,540 <span class="stat-unit">MW</span></div>
                <div class="stat-label">Energy Generation</div>
            </div>
            <div class="stat-footer">Current continuous output</div>
        </div>
        <div class="new-stat-card">
            <div class="stat-header">
                <span class="stat-icon">🪱</span>
                <span class="stat-trend up">+8.0%</span>
            </div>
            <div class="stat-body">
                <div class="stat-value">450 <span class="stat-unit">Tons</span></div>
                <div class="stat-label">Vermicompost</div>
            </div>
            <div class="stat-footer">Daily harvest projection</div>
        </div>
        <div class="new-stat-card">
            <div class="stat-header">
                <span class="stat-icon">💰</span>
                <span class="stat-trend">Optimal</span>
            </div>
            <div class="stat-body">
                <div class="stat-value">₹6.8M</div>
                <div class="stat-label">Avg ROI Tracking</div>
            </div>
            <div class="stat-footer">Blended across all verticals</div>
        </div>
    </div>

    <!-- Main Grid -->
    <div class="new-main-grid">
        
        <!-- Chart Area -->
        <div class="new-chart-area">
            <div class="new-section-header">
                <h3>📈 Energy Output Trends</h3>
                <div class="new-tabs">
                    <button class="new-tab active">Day</button>
                    <button class="new-tab">Week</button>
                    <button class="new-tab">Month</button>
                </div>
            </div>
            <div class="new-chart-box">
                <canvas id="overviewChart"></canvas>
            </div>
        </div>

        <!-- Zones -->
        <div class="new-zones-area">
            <div class="new-section-header">
                <h3>📍 Active Zones</h3>
            </div>
            <div class="new-zones-list">
                <div class="new-zone-row">
                    <div class="zone-dot green"></div>
                    <div class="zone-details">
                        <div class="zone-name">Bellary Hub</div>
                        <div class="zone-meta">100k cattle • Biogas/H2</div>
                    </div>
                    <div class="zone-perf">
                        <div class="perf-num">98%</div>
                        <div class="perf-label">Efficiency</div>
                    </div>
                </div>
                <div class="new-zone-row">
                    <div class="zone-dot green"></div>
                    <div class="zone-details">
                        <div class="zone-name">Kurnool Hub</div>
                        <div class="zone-meta">3 GW Solar • Agrivoltaic</div>
                    </div>
                    <div class="zone-perf">
                        <div class="perf-num">95%</div>
                        <div class="perf-label">Efficiency</div>
                    </div>
                </div>
                <div class="new-zone-row">
                    <div class="zone-dot green"></div>
                    <div class="zone-details">
                        <div class="zone-name">Gadwal Dairy</div>
                        <div class="zone-meta">80k L/day • Dairy/Hydro</div>
                    </div>
                    <div class="zone-perf">
                        <div class="perf-num">97%</div>
                        <div class="perf-label">Efficiency</div>
                    </div>
                </div>
                <div class="new-zone-row">
                    <div class="zone-dot green"></div>
                    <div class="zone-details">
                        <div class="zone-name">Hyderabad HQ</div>
                        <div class="zone-meta">Vertical Solar • Corp/Demo</div>
                    </div>
                    <div class="zone-perf">
                        <div class="perf-num">99%</div>
                        <div class="perf-label">Efficiency</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bottom Row -->
    <div class="new-bottom-row">
        
        <!-- Circular Economy -->
        <div class="new-eco-area">
            <div class="new-section-header">
                <h3>🔄 Circular Economy</h3>
            </div>
            <div class="new-eco-flow">
                <div class="eco-node-new">
                    <div class="node-icon">🐄</div>
                    <div class="node-title">Dairy Ops</div>
                    <div class="node-sub">1M Cattle</div>
                </div>
                <div class="eco-arrow-new">→</div>
                <div class="eco-node-new">
                    <div class="node-icon">🔥</div>
                    <div class="node-title">Biogas</div>
                    <div class="node-sub">500+ tons/day</div>
                </div>
                <div class="eco-arrow-new">→</div>
                <div class="eco-node-new">
                    <div class="node-icon">🪱</div>
                    <div class="node-title">Vermi</div>
                    <div class="node-sub">450t output</div>
                </div>
                <div class="eco-arrow-new">→</div>
                <div class="eco-node-new">
                    <div class="node-icon">💰</div>
                    <div class="node-title">Revenue</div>
                    <div class="node-sub">Export + Credits</div>
                </div>
            </div>
        </div>

        <!-- Activity -->
        <div class="new-activity-area">
            <div class="new-section-header">
                <h3>⚡ Live Activity</h3>
                <button class="new-view-all">View All →</button>
            </div>
            <div class="new-activity-list">
                <div class="new-activity-item">
                    <span class="activity-dot green"></span>
                    <span class="activity-text">Solar array peak reached</span>
                    <span class="activity-time">2m ago</span>
                </div>
                <div class="new-activity-item">
                    <span class="activity-dot yellow"></span>
                    <span class="activity-text">New cattle batch registered</span>
                    <span class="activity-time">15m ago</span>
                </div>
                <div class="new-activity-item">
                    <span class="activity-dot blue"></span>
                    <span class="activity-text">Milk collection completed</span>
                    <span class="activity-time">1h ago</span>
                </div>
                <div class="new-activity-item">
                    <span class="activity-dot red"></span>
                    <span class="activity-text">Maintenance alert: Turbine #3</span>
                    <span class="activity-time">2h ago</span>
                </div>
            </div>
        </div>
    </div>

</div>

<style>
/* Complete New Overview Styles */
.overview-new {
    padding: 24px;
    max-width: 1600px;
    margin: 0 auto;
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hero */
.new-hero {
    background: linear-gradient(135deg, rgba(0, 176, 255, 0.15), rgba(16, 185, 129, 0.1));
    border: 1px solid rgba(0, 176, 255, 0.25);
    border-radius: 24px;
    padding: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}

.new-hero-content {
    max-width: 600px;
}

.new-brand {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
}

.new-brand-icon {
    font-size: 3rem;
}

.new-brand-name {
    display: block;
    font-size: 2rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: 3px;
}

.new-brand-tag {
    display: block;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.6);
}

.new-hero-desc {
    color: rgba(255,255,255,0.7);
    font-size: 1rem;
    line-height: 1.5;
}

.new-hero-badges {
    display: flex;
    gap: 16px;
}

.new-badge {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 18px 28px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    min-width: 110px;
}

.new-badge.green {
    background: rgba(16, 185, 129, 0.15);
    border-color: rgba(16, 185, 129, 0.3);
}

.badge-emoji {
    font-size: 1.6rem;
    margin-bottom: 6px;
}

.badge-text {
    font-size: 1.3rem;
    font-weight: 700;
    color: #fff;
}

.badge-sub {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Stats Row */
.new-stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 28px;
}

.new-stat-card {
    background: #0d1629;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.new-stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.3);
}

.stat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 20px 0;
}

.stat-icon {
    font-size: 1.8rem;
}

.stat-trend {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 10px;
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    color: rgba(255,255,255,0.6);
}

.stat-trend.up {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
}

.stat-body {
    padding: 12px 20px;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
}

.stat-unit {
    font-size: 1rem;
    font-weight: 500;
    color: rgba(255,255,255,0.5);
}

.stat-label {
    font-size: 1rem;
    font-weight: 600;
    color: #fff;
    margin-top: 4px;
}

.stat-footer {
    padding: 14px 20px;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
    border-top: 1px solid rgba(255,255,255,0.05);
}

/* Main Grid */
.new-main-grid {
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    gap: 24px;
    margin-bottom: 28px;
}

.new-section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}

.new-section-header h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #fff;
    margin: 0;
}

.new-tabs {
    display: flex;
    gap: 4px;
    background: rgba(255,255,255,0.05);
    padding: 4px;
    border-radius: 10px;
}

.new-tab {
    padding: 8px 16px;
    border: none;
    background: transparent;
    color: rgba(255,255,255,0.5);
    font-size: 0.8rem;
    font-weight: 500;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.new-tab.active {
    background: #0ea5e9;
    color: #fff;
}

/* Chart */
.new-chart-area {
    background: #0d1629;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px;
}

.new-chart-box {
    height: 320px;
}

/* Zones */
.new-zones-area {
    background: #0d1629;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px;
}

.new-zones-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.new-zone-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px;
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
    transition: background 0.2s;
}

.new-zone-row:hover {
    background: rgba(255,255,255,0.06);
}

.zone-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 12px #10b981;
}

.zone-details {
    flex: 1;
}

.zone-name {
    font-size: 1rem;
    font-weight: 600;
    color: #fff;
}

.zone-meta {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.5);
    margin-top: 2px;
}

.zone-perf {
    text-align: right;
}

.perf-num {
    font-size: 1.2rem;
    font-weight: 700;
    color: #10b981;
}

.perf-label {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
}

/* Bottom Row */
.new-bottom-row {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 24px;
}

.new-eco-area,
.new-activity-area {
    background: #0d1629;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px;
}

/* Eco Flow */
.new-eco-flow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 0;
}

.eco-node-new {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    flex: 1;
}

.node-icon {
    font-size: 2.4rem;
    margin-bottom: 10px;
}

.node-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #fff;
}

.node-sub {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
}

.eco-arrow-new {
    font-size: 1.4rem;
    color: #0ea5e9;
    padding: 0 8px;
}

/* Activity */
.new-view-all {
    background: none;
    border: none;
    color: #0ea5e9;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
}

.new-activity-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.new-activity-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px;
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
}

.activity-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.activity-dot.green { background: #10b981; }
.activity-dot.yellow { background: #f59e0b; }
.activity-dot.blue { background: #3b82f6; }
.activity-dot.red { background: #ef4444; }

.activity-text {
    flex: 1;
    font-size: 0.9rem;
    color: #fff;
}

.activity-time {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
}

/* Responsive */
@media (max-width: 1200px) {
    .new-stats-row { grid-template-columns: repeat(2, 1fr); }
    .new-main-grid { grid-template-columns: 1fr; }
    .new-bottom-row { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
    .new-hero { flex-direction: column; text-align: center; gap: 24px; }
    .new-hero-badges { flex-wrap: wrap; justify-content: center; }
    .new-stats-row { grid-template-columns: 1fr; }
}
</style>
`;

    // Function to render the new overview
    window.renderNewOverview = function () {
        const container = document.getElementById('page-container');
        if (container) {
            container.innerHTML = window.newOverviewTemplate;
        }
    };

    console.log('New Overview template loaded. Use renderNewOverview() to display.');
})();

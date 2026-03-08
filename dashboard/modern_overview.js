/**
 * Modern Overview Dashboard Redesign
 * A cleaner, more modern design for the Vedavathi Dashboard overview
 */

window.modernOverview = {
    // Generate the modern overview HTML
    render: function () {
        return `
        <div class="overview-modern">
            
            <!-- Hero Stats Banner -->
            <div class="hero-stats-row">
                <div class="hero-main-stat">
                    <div class="hero-icon">🌿</div>
                    <div class="hero-text">
                        <div class="hero-title">Vedavathi</div>
                        <div class="hero-subtitle">Integrated Eco-Farm</div>
                    </div>
                </div>
                <div class="hero-badges">
                    <div class="hero-badge">
                        <span class="badge-icon">⚡</span>
                        <span class="badge-value">3.5+ GW</span>
                        <span class="badge-label">Energy</span>
                    </div>
                    <div class="hero-badge">
                        <span class="badge-icon">🐄</span>
                        <span class="badge-value">1M</span>
                        <span class="badge-label">Cattle</span>
                    </div>
                    <div class="hero-badge success">
                        <span class="badge-icon">📈</span>
                        <span class="badge-value">6-8 Mo</span>
                        <span class="badge-label">ROI</span>
                    </div>
                </div>
            </div>

            <!-- KPI Cards -->
            <div class="kpi-modern-grid">
                <div class="kpi-modern-card green">
                    <div class="kpi-modern-header">
                        <span class="kpi-modern-icon">🐄</span>
                        <span class="kpi-modern-trend up">+1.2%</span>
                    </div>
                    <div class="kpi-modern-value">1,000,000</div>
                    <div class="kpi-modern-label">Total Live Cattle</div>
                    <div class="kpi-modern-sub">Across 4 operational zones</div>
                </div>
                
                <div class="kpi-modern-card teal">
                    <div class="kpi-modern-header">
                        <span class="kpi-modern-icon">⚡</span>
                        <span class="kpi-modern-trend up">+4.5%</span>
                    </div>
                    <div class="kpi-modern-value">3,540 <span class="kpi-unit">MW</span></div>
                    <div class="kpi-modern-label">Energy Generation</div>
                    <div class="kpi-modern-sub">Current continuous output</div>
                </div>
                
                <div class="kpi-modern-card orange">
                    <div class="kpi-modern-header">
                        <span class="kpi-modern-icon">🪱</span>
                        <span class="kpi-modern-trend up">+8.0%</span>
                    </div>
                    <div class="kpi-modern-value">450 <span class="kpi-unit">Tons</span></div>
                    <div class="kpi-modern-label">Vermicompost</div>
                    <div class="kpi-modern-sub">Daily harvest projection</div>
                </div>
                
                <div class="kpi-modern-card purple">
                    <div class="kpi-modern-header">
                        <span class="kpi-modern-icon">💰</span>
                        <span class="kpi-modern-trend">Optimal</span>
                    </div>
                    <div class="kpi-modern-value">₹6.8M</div>
                    <div class="kpi-modern-label">Avg ROI Tracking</div>
                    <div class="kpi-modern-sub">Blended across all verticals</div>
                </div>
            </div>

            <!-- Main Content Grid -->
            <div class="overview-grid">
                
                <!-- Chart Section -->
                <div class="overview-chart-section">
                    <div class="section-header">
                        <h3>📈 Energy Output Trends</h3>
                        <div class="chart-period-selector">
                            <button class="period-btn active">Day</button>
                            <button class="period-btn">Week</button>
                            <button class="period-btn">Month</button>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="overviewChart"></canvas>
                    </div>
                </div>

                <!-- Zones Status -->
                <div class="overview-zones-section">
                    <div class="section-header">
                        <h3>📍 Zone Status</h3>
                    </div>
                    <div class="zones-modern-list">
                        <div class="zone-modern-item">
                            <div class="zone-status-dot online"></div>
                            <div class="zone-details">
                                <div class="zone-name">Bellary Hub</div>
                                <div class="zone-meta">100k cattle • Biogas/H2</div>
                            </div>
                            <div class="zone-efficiency">
                                <div class="eff-value">98%</div>
                                <div class="eff-label">Efficiency</div>
                            </div>
                        </div>
                        <div class="zone-modern-item">
                            <div class="zone-status-dot online"></div>
                            <div class="zone-details">
                                <div class="zone-name">Kurnool Hub</div>
                                <div class="zone-meta">3 GW Solar • Agrivoltaic</div>
                            </div>
                            <div class="zone-efficiency">
                                <div class="eff-value">95%</div>
                                <div class="eff-label">Efficiency</div>
                            </div>
                        </div>
                        <div class="zone-modern-item">
                            <div class="zone-status-dot online"></div>
                            <div class="zone-details">
                                <div class="zone-name">Gadwal Dairy</div>
                                <div class="zone-meta">80k L/day • Dairy/Hydro</div>
                            </div>
                            <div class="zone-efficiency">
                                <div class="eff-value">97%</div>
                                <div class="eff-label">Efficiency</div>
                            </div>
                        </div>
                        <div class="zone-modern-item">
                            <div class="zone-status-dot online"></div>
                            <div class="zone-details">
                                <div class="zone-name">Hyderabad HQ</div>
                                <div class="zone-meta">Vertical Solar • Corp/Demo</div>
                            </div>
                            <div class="zone-efficiency">
                                <div class="eff-value">99%</div>
                                <div class="eff-label">Efficiency</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Row -->
            <div class="overview-bottom-row">
                
                <!-- Circular Economy -->
                <div class="eco-modern-card">
                    <div class="section-header">
                        <h3>🔄 Circular Economy</h3>
                    </div>
                    <div class="eco-modern-flow">
                        <div class="eco-modern-node">
                            <div class="eco-node-icon">🐄</div>
                            <div class="eco-node-text">
                                <div class="eco-node-title">Dairy Ops</div>
                                <div class="eco-node-sub">1M Cattle</div>
                            </div>
                        </div>
                        <div class="eco-modern-arrow">→</div>
                        <div class="eco-modern-node">
                            <div class="eco-node-icon">🔥</div>
                            <div class="eco-node-text">
                                <div class="eco-node-title">Biogas</div>
                                <div class="eco-node-sub">500+ tons/day</div>
                            </div>
                        </div>
                        <div class="eco-modern-arrow">→</div>
                        <div class="eco-modern-node">
                            <div class="eco-node-icon">🪱</div>
                            <div class="eco-node-text">
                                <div class="eco-node-title">Vermi</div>
                                <div class="eco-node-sub">450t output</div>
                            </div>
                        </div>
                        <div class="eco-modern-arrow">→</div>
                        <div class="eco-modern-node">
                            <div class="eco-node-icon">💰</div>
                            <div class="eco-node-text">
                                <div class="eco-node-title">Revenue</div>
                                <div class="eco-node-sub">Export + Credits</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Activity Feed -->
                <div class="activity-modern-card">
                    <div class="section-header">
                        <h3>⚡ Live Activity</h3>
                        <button class="view-all-btn">View All →</button>
                    </div>
                    <div class="activity-modern-list">
                        <div class="activity-modern-item">
                            <div class="activity-indicator energy"></div>
                            <div class="activity-info">
                                <div class="activity-text">Solar array peak reached</div>
                                <div class="activity-time">2 min ago</div>
                            </div>
                        </div>
                        <div class="activity-modern-item">
                            <div class="activity-indicator cattle"></div>
                            <div class="activity-info">
                                <div class="activity-text">New cattle batch registered</div>
                                <div class="activity-time">15 min ago</div>
                            </div>
                        </div>
                        <div class="activity-modern-item">
                            <div class="activity-indicator milk"></div>
                            <div class="activity-info">
                                <div class="activity-text">Milk collection completed</div>
                                <div class="activity-time">1 hour ago</div>
                            </div>
                        </div>
                        <div class="activity-modern-item">
                            <div class="activity-indicator warning"></div>
                            <div class="activity-info">
                                <div class="activity-text">Maintenance alert: Turbine #3</div>
                                <div class="activity-time">2 hours ago</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
        `;
    },

    // Inject styles into the page
    injectStyles: function () {
        if (document.getElementById('modern-overview-styles')) return;

        const styles = `
        <style id="modern-overview-styles">
        .overview-modern {
            padding: 24px;
            max-width: 1600px;
            margin: 0 auto;
        }

        /* Hero Stats Row */
        .hero-stats-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, rgba(0, 176, 255, 0.15), rgba(16, 185, 129, 0.1));
            border: 1px solid rgba(0, 176, 255, 0.2);
            border-radius: 16px;
            padding: 20px 28px;
            margin-bottom: 24px;
        }

        .hero-main-stat {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .hero-icon {
            font-size: 2.5rem;
        }

        .hero-text .hero-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.5px;
        }

        .hero-text .hero-subtitle {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .hero-badges {
            display: flex;
            gap: 12px;
        }

        .hero-badge {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 12px 20px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            min-width: 90px;
        }

        .hero-badge.success {
            background: rgba(16, 185, 129, 0.15);
            border-color: rgba(16, 185, 129, 0.3);
        }

        .badge-icon {
            font-size: 1.25rem;
            margin-bottom: 4px;
        }

        .badge-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .badge-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* KPI Modern Grid */
        .kpi-modern-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .kpi-modern-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            transition: all 0.2s ease;
        }

        .kpi-modern-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }

        .kpi-modern-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .kpi-modern-icon {
            font-size: 1.5rem;
        }

        .kpi-modern-trend {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.08);
        }

        .kpi-modern-trend.up {
            color: #10b981;
            background: rgba(16, 185, 129, 0.15);
        }

        .kpi-modern-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .kpi-unit {
            font-size: 1rem;
            font-weight: 500;
            color: var(--text-secondary);
        }

        .kpi-modern-label {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 2px;
        }

        .kpi-modern-sub {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        /* Main Grid */
        .overview-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .section-header h3 {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }

        /* Chart Section */
        .overview-chart-section {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
        }

        .chart-period-selector {
            display: flex;
            gap: 4px;
            background: rgba(255, 255, 255, 0.05);
            padding: 4px;
            border-radius: 8px;
        }

        .period-btn {
            padding: 6px 14px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 500;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .period-btn.active {
            background: var(--primary);
            color: white;
        }

        .chart-container {
            height: 280px;
        }

        /* Zones Section */
        .overview-zones-section {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
        }

        .zones-modern-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .zone-modern-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            transition: background 0.2s;
        }

        .zone-modern-item:hover {
            background: rgba(255, 255, 255, 0.06);
        }

        .zone-status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
            flex-shrink: 0;
        }

        .zone-details {
            flex: 1;
        }

        .zone-name {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .zone-meta {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .zone-efficiency {
            text-align: right;
        }

        .eff-value {
            font-size: 1rem;
            font-weight: 700;
            color: #10b981;
        }

        .eff-label {
            font-size: 0.65rem;
            color: var(--text-secondary);
            text-transform: uppercase;
        }

        /* Bottom Row */
        .overview-bottom-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .eco-modern-card,
        .activity-modern-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
        }

        /* Eco Flow */
        .eco-modern-flow {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .eco-modern-node {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            flex: 1;
        }

        .eco-modern-node .eco-node-icon {
            font-size: 2rem;
            margin-bottom: 8px;
        }

        .eco-modern-node .eco-node-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .eco-modern-node .eco-node-sub {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }

        .eco-modern-arrow {
            font-size: 1.25rem;
            color: var(--primary);
            padding: 0 8px;
        }

        /* Activity */
        .view-all-btn {
            background: none;
            border: none;
            color: var(--primary);
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
        }

        .activity-modern-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .activity-modern-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.02);
        }

        .activity-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .activity-indicator.energy { background: #10b981; }
        .activity-indicator.cattle { background: #f59e0b; }
        .activity-indicator.milk { background: #3b82f6; }
        .activity-indicator.warning { background: #ef4444; }

        .activity-info {
            flex: 1;
        }

        .activity-text {
            font-size: 0.85rem;
            color: var(--text-primary);
        }

        .activity-time {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }

        /* Responsive */
        @media (max-width: 1200px) {
            .kpi-modern-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .overview-grid,
            .overview-bottom-row {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .hero-stats-row {
                flex-direction: column;
                gap: 16px;
            }
            .hero-badges {
                flex-wrap: wrap;
                justify-content: center;
            }
            .kpi-modern-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    },

    // Initialize the overview
    init: function () {
        this.injectStyles();

        // Replace the overview content
        const container = document.getElementById('page-container');
        if (container) {
            container.innerHTML = this.render();
        }
    }
};

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    // The overview will be rendered by the main app
});

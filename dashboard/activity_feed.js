// =========================================
// ACTIVITY FEED SYSTEM
// Real-time updates of farm activities
// =========================================

(function () {
    'use strict';

    const ActivityFeed = {
        activities: [],
        maxItems: 50,

        // Activity templates
        templates: {
            milk_record: { icon: '🥛', label: 'Milk Recorded', color: '#22c55e' },
            egg_record: { icon: '🥚', label: 'Eggs Recorded', color: '#f59e0b' },
            animal_added: { icon: '🐄', label: 'Animal Added', color: '#3b82f6' },
            booking: { icon: '📅', label: 'New Booking', color: '#8b5cf6' },
            alert: { icon: '🚨', label: 'Alert Triggered', color: '#ef4444' },
            login: { icon: '🔐', label: 'User Login', color: '#64748b' },
            report: { icon: '📊', label: 'Report Generated', color: '#06b6d4' },
            inventory: { icon: '📦', label: 'Inventory Update', color: '#84cc16' },
            expense: { icon: '💸', label: 'Expense Added', color: '#f43f5e' },
            invoice: { icon: '🧾', label: 'Invoice Created', color: '#10b981' },
            feed: { icon: '🌾', label: 'Feed Given', color: '#a3e635' },
            health: { icon: '💊', label: 'Health Check', color: '#ec4899' }
        },

        init() {
            this.loadFromStorage();
            this.createUI();
            this.addStyles();
            console.log('📋 Activity Feed Ready');
        },

        loadFromStorage() {
            const saved = localStorage.getItem('vedavathi-activities');
            if (saved) {
                try {
                    this.activities = JSON.parse(saved);
                } catch (e) {
                    this.activities = [];
                }
            }

            // Add some demo activities if empty
            if (this.activities.length === 0) {
                this.addDemoActivities();
            }
        },

        saveToStorage() {
            // Keep only maxItems
            if (this.activities.length > this.maxItems) {
                this.activities = this.activities.slice(0, this.maxItems);
            }
            localStorage.setItem('vedavathi-activities', JSON.stringify(this.activities));
        },

        addDemoActivities() {
            const now = Date.now();
            this.activities = [
                {
                    id: 1,
                    type: 'milk_record',
                    title: 'Morning Milk Recorded',
                    details: 'Zone A - 245 liters',
                    user: 'Admin',
                    time: new Date(now - 300000).toISOString(),
                    location: 'Bellary Hub'
                },
                {
                    id: 2,
                    type: 'alert',
                    title: 'Low Feed Alert',
                    details: 'Poultry Shed 2 - Feed below threshold',
                    user: 'System',
                    time: new Date(now - 900000).toISOString(),
                    location: 'Kurnool Hub'
                },
                {
                    id: 3,
                    type: 'booking',
                    title: 'New Booking',
                    details: 'Family Package - 4 guests',
                    user: 'Reception',
                    time: new Date(now - 1800000).toISOString(),
                    location: 'Agri-Tourism'
                },
                {
                    id: 4,
                    type: 'egg_record',
                    title: 'Egg Collection',
                    details: '1,240 eggs collected',
                    user: 'Poultry Team',
                    time: new Date(now - 3600000).toISOString(),
                    location: 'Hyderabad Poultry'
                },
                {
                    id: 5,
                    type: 'animal_added',
                    title: 'New Animal Registered',
                    details: 'Breed: HF Cross, Tag: AB123456',
                    user: 'Vet Dr. Rao',
                    time: new Date(now - 7200000).toISOString(),
                    location: 'Gadwal Dairy'
                }
            ];
            this.saveToStorage();
        },

        // Add new activity
        add(type, title, details, user = 'User', location = 'HQ') {
            const template = this.templates[type] || this.templates.info;

            const activity = {
                id: Date.now(),
                type,
                title,
                details,
                user,
                location,
                time: new Date().toISOString()
            };

            this.activities.unshift(activity);
            this.saveToStorage();
            this.updateFeed();

            return activity;
        },

        createUI() {
            // Create activity feed panel
            const panel = document.createElement('div');
            panel.id = 'activityFeedPanel';
            panel.className = 'activity-feed-panel';
            panel.innerHTML = `
                <div class="af-header">
                    <span class="af-title">📋 Activity Feed</span>
                    <div class="af-actions">
                        <button class="af-filter-btn" title="Filter">🔽</button>
                        <button class="af-close" onclick="ActivityFeed.togglePanel()">×</button>
                    </div>
                </div>
                <div class="af-filters">
                    <button class="af-filter active" data-filter="all">All</button>
                    <button class="af-filter" data-filter="alerts">🚨 Alerts</button>
                    <button class="af-filter" data-filter="records">📝 Records</button>
                    <button class="af-filter" data-filter="system">⚙️ System</button>
                </div>
                <div class="af-list" id="afList">
                    ${this.getActivitiesHTML()}
                </div>
                <div class="af-footer">
                    <button class="af-load-more" onclick="ActivityFeed.loadMore()">Load More</button>
                </div>
            `;

            // Add to page
            const mainContent = document.querySelector('.main-content');
            if (mainContent) {
                mainContent.appendChild(panel);
            }

            this.bindEvents();
        },

        bindEvents() {
            // Filter buttons
            document.querySelectorAll('.af-filter').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    document.querySelectorAll('.af-filter').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    this.filterActivities(e.target.dataset.filter);
                });
            });

            // Toggle with keyboard shortcut 'a'
            document.addEventListener('keydown', (e) => {
                if (e.key === 'a' && !e.ctrlKey && !e.metaKey &&
                    e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                    this.togglePanel();
                }
            });
        },

        getActivitiesHTML(activities = this.activities) {
            if (activities.length === 0) {
                return '<div class="af-empty">No activities to show</div>';
            }

            return activities.map(activity => {
                const template = this.templates[activity.type] || { icon: '📄', color: '#64748b' };
                const timeAgo = this.getTimeAgo(activity.time);

                return `
                    <div class="af-item" data-type="${activity.type}">
                        <div class="af-icon" style="background: ${template.color}20; color: ${template.color}">
                            ${template.icon}
                        </div>
                        <div class="af-content">
                            <div class="af-item-title">${activity.title}</div>
                            <div class="af-item-details">${activity.details}</div>
                            <div class="af-meta">
                                <span class="af-user">👤 ${activity.user}</span>
                                <span class="af-time">🕒 ${timeAgo}</span>
                                <span class="af-location">📍 ${activity.location}</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        },

        updateFeed(filtered = null) {
            const list = document.getElementById('afList');
            if (!list) return;

            const activities = filtered || this.activities;
            list.innerHTML = this.getActivitiesHTML(activities);
        },

        filterActivities(filter) {
            if (filter === 'all') {
                this.updateFeed();
                return;
            }

            const filterMap = {
                alerts: ['alert', 'health'],
                records: ['milk_record', 'egg_record', 'animal_added', 'inventory', 'expense', 'feed'],
                system: ['login', 'report', 'booking']
            };

            const types = filterMap[filter] || [];
            const filtered = this.activities.filter(a => types.includes(a.type));
            this.updateFeed(filtered);
        },

        loadMore() {
            // In real app, load from server
            PushNotifications.showToast('info', 'Loading...', 'Fetching more activities');
        },

        togglePanel() {
            const panel = document.getElementById('activityFeedPanel');
            if (!panel) return;

            panel.classList.toggle('open');

            // Add button to toggle if not exists
            this.ensureToggleButton();
        },

        ensureToggleButton() {
            if (document.getElementById('activityFeedToggle')) return;

            const header = document.querySelector('.header-actions');
            if (!header) return;

            const btn = document.createElement('button');
            btn.id = 'activityFeedToggle';
            btn.className = 'icon-btn';
            btn.innerHTML = '📋';
            btn.title = 'Activity Feed (Press A)';
            btn.onclick = () => this.togglePanel();

            // Add after alerts
            const alertBtn = document.getElementById('alert-bell-btn');
            if (alertBtn && alertBtn.nextSibling) {
                header.insertBefore(btn, alertBtn.nextSibling);
            } else {
                header.appendChild(btn);
            }
        },

        getTimeAgo(dateString) {
            const date = new Date(dateString);
            const now = new Date();
            const seconds = Math.floor((now - date) / 1000);

            if (seconds < 60) return 'Just now';
            if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
            if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
            if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;

            return date.toLocaleDateString();
        },

        addStyles() {
            if (document.getElementById('activity-feed-styles')) return;

            const style = document.createElement('style');
            style.id = 'activity-feed-styles';
            style.textContent = `
                /* Activity Feed Panel */
                .activity-feed-panel {
                    position: fixed;
                    top: 70px;
                    right: -400px;
                    width: 380px;
                    max-width: calc(100vw - 20px);
                    height: calc(100vh - 90px);
                    background: var(--panel-bg);
                    border: 1px solid var(--border);
                    border-radius: 16px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    z-index: 999;
                    display: flex;
                    flex-direction: column;
                    transition: right 0.3s ease;
                }
                
                .activity-feed-panel.open {
                    right: 20px;
                }
                
                .af-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 16px;
                    border-bottom: 1px solid var(--border);
                }
                
                .af-title {
                    font-weight: 600;
                    font-size: 1rem;
                }
                
                .af-actions {
                    display: flex;
                    gap: 8px;
                }
                
                .af-close,
                .af-filter-btn {
                    background: transparent;
                    border: none;
                    color: var(--text-muted);
                    font-size: 1.3rem;
                    cursor: pointer;
                    padding: 4px 8px;
                    border-radius: 6px;
                }
                
                .af-close:hover,
                .af-filter-btn:hover {
                    background: var(--bg-card-hover);
                }
                
                .af-filters {
                    display: flex;
                    gap: 8px;
                    padding: 12px 16px;
                    border-bottom: 1px solid var(--border);
                    overflow-x: auto;
                }
                
                .af-filter {
                    background: var(--bg-tertiary);
                    border: none;
                    color: var(--text-secondary);
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    cursor: pointer;
                    white-space: nowrap;
                    transition: all 0.2s;
                }
                
                .af-filter:hover {
                    background: var(--bg-card-hover);
                }
                
                .af-filter.active {
                    background: var(--primary);
                    color: white;
                }
                
                .af-list {
                    flex: 1;
                    overflow-y: auto;
                    padding: 12px;
                }
                
                .af-empty {
                    text-align: center;
                    padding: 40px 20px;
                    color: var(--text-muted);
                }
                
                .af-item {
                    display: flex;
                    gap: 12px;
                    padding: 12px;
                    border-radius: 12px;
                    margin-bottom: 8px;
                    transition: background 0.2s;
                }
                
                .af-item:hover {
                    background: var(--bg-card);
                }
                
                .af-icon {
                    width: 40px;
                    height: 40px;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.2rem;
                    flex-shrink: 0;
                }
                
                .af-content {
                    flex: 1;
                    min-width: 0;
                }
                
                .af-item-title {
                    font-weight: 600;
                    font-size: 0.9rem;
                    margin-bottom: 4px;
                }
                
                .af-item-details {
                    font-size: 0.85rem;
                    color: var(--text-secondary);
                    margin-bottom: 8px;
                }
                
                .af-meta {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    font-size: 0.75rem;
                    color: var(--text-muted);
                }
                
                .af-footer {
                    padding: 12px 16px;
                    border-top: 1px solid var(--border);
                }
                
                .af-load-more {
                    width: 100%;
                    padding: 10px;
                    background: var(--bg-tertiary);
                    border: none;
                    border-radius: 8px;
                    color: var(--text-secondary);
                    cursor: pointer;
                    font-size: 0.85rem;
                    transition: background 0.2s;
                }
                
                .af-load-more:hover {
                    background: var(--bg-card-hover);
                }
                
                @media (max-width: 480px) {
                    .activity-feed-panel.open {
                        right: 10px;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    };

    // Expose globally
    window.ActivityFeed = ActivityFeed;

    // Initialize
    function initActivityFeed() {
        ActivityFeed.init();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initActivityFeed);
    } else {
        initActivityFeed();
    }

})();

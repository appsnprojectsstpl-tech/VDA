// ============================================
// UX ENHANCEMENTS FOR VEDAVATHI DASHBOARD
// Phase 7: User Experience & Performance
// ============================================

(function () {
    'use strict';

    // ============================================
    // 1. DARK MODE TOGGLE
    // ============================================
    window.DarkMode = {
        isDark: false,

        init() {
            // Check saved preference or system preference
            const saved = localStorage.getItem('vedavathi_dark_mode');
            if (saved !== null) {
                this.isDark = saved === 'true';
            } else {
                this.isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            }
            this.apply();
            // Don't add duplicate toggle button - use existing ThemeManager from quick_wins.js
        },

        toggle() {
            // Delegate to ThemeManager from quick_wins.js if available
            if (window.ThemeManager) {
                window.ThemeManager.toggle();
                this.isDark = window.ThemeManager.isDark;
            } else {
                this.isDark = !this.isDark;
                localStorage.setItem('vedavathi_dark_mode', this.isDark);
                this.apply();
            }
        },

        apply() {
            document.body.classList.toggle('dark-mode', this.isDark);
        },

        addToggleButton() {
            // Add toggle to header
            const header = document.querySelector('.header-actions');
            if (!header) return;

            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'dark-mode-toggle';
            toggleBtn.innerHTML = this.isDark ? '☀️' : '🌙';
            toggleBtn.title = 'Toggle Dark Mode';
            toggleBtn.onclick = () => this.toggle();
            header.appendChild(toggleBtn);
        }
    };

    // ============================================
    // 2. KEYBOARD SHORTCUTS
    // ============================================
    window.KeyboardShortcuts = {
        shortcuts: {
            'mod+k': 'Open Quick Search',
            'mod+/': 'Show Shortcuts',
            'mod+d': 'Toggle Dark Mode',
            'mod+h': 'Go to Home',
            'mod+e': 'Go to Energy',
            'mod+f': 'Go to Finance',
            'Escape': 'Close Modal/Search'
        },

        init() {
            document.addEventListener('keydown', (e) => this.handleKeydown(e));
            this.showHints();
        },

        handleKeydown(e) {
            const key = [];
            if (e.metaKey || e.ctrlKey) key.push('mod');
            if (e.shiftKey) key.push('shift');
            if (e.altKey) key.push('alt');
            key.push(e.key.toLowerCase());

            const combo = key.join('+');

            switch (combo) {
                case 'mod+k':
                    e.preventDefault();
                    this.openQuickSearch();
                    break;
                case 'mod+/':
                    e.preventDefault();
                    this.showHelp();
                    break;
                case 'mod+d':
                    e.preventDefault();
                    window.DarkMode.toggle();
                    break;
                case 'mod+h':
                    e.preventDefault();
                    this.navigateTo('overview');
                    break;
                case 'mod+e':
                    e.preventDefault();
                    this.navigateTo('solar');
                    break;
                case 'mod+f':
                    e.preventDefault();
                    this.navigateTo('finance');
                    break;
                case 'escape':
                    this.closeQuickSearch();
                    break;
            }
        },

        navigateTo(page) {
            const btn = document.querySelector(`[data-page="${page}"]`);
            if (btn) btn.click();
        },

        openQuickSearch() {
            // Remove existing
            this.closeQuickSearch();

            const modal = document.createElement('div');
            modal.className = 'quick-search-modal';
            modal.innerHTML = `
                <div class="quick-search-overlay"></div>
                <div class="quick-search-container">
                    <input type="text" class="quick-search-input" 
                           placeholder="Search pages, actions... (⌘K)" 
                           autofocus>
                    <div class="quick-search-results"></div>
                    <div class="quick-search-hints">
                        <span>↑↓ Navigate</span>
                        <span>↵ Select</span>
                        <span>ESC Close</span>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);

            const input = modal.querySelector('input');
            const results = modal.querySelector('.results');

            input.addEventListener('input', (e) => this.search(e.target.value));
            input.addEventListener('keydown', (e) => this.handleSearchKey(e));

            // Close on overlay click
            modal.querySelector('.overlay').addEventListener('click', () => this.closeQuickSearch());

            setTimeout(() => input.focus(), 100);
        },

        closeQuickSearch() {
            const modal = document.querySelector('.quick-search-modal');
            if (modal) modal.remove();
        },

        search(query) {
            const results = document.querySelector('.quick-search-results');
            if (!query) {
                results.innerHTML = '<div class="quick-search-empty">Type to search...</div>';
                return;
            }

            const pages = [
                { name: 'Overview Dashboard', page: 'overview', icon: '📊' },
                { name: 'Smart Grid', page: 'smart-grid', icon: '⚡' },
                { name: 'Solar Energy', page: 'solar', icon: '☀️' },
                { name: 'Wind Energy', page: 'wind', icon: '💨' },
                { name: 'Biogas', page: 'biogas', icon: '🔥' },
                { name: 'Hydrogen', page: 'hydrogen', icon: '💧' },
                { name: 'Hydro Power', page: 'hydro', icon: '🌊' },
                { name: 'Dairy & Cattle', page: 'dairy', icon: '🐄' },
                { name: 'Poultry Hub', page: 'poultry', icon: '🐔' },
                { name: 'Aquaculture', page: 'aqua', icon: '🐟' },
                { name: 'Vermiculture', page: 'vermi', icon: '🪱' },
                { name: 'Tree Nursery', page: 'tree', icon: '🌳' },
                { name: 'Paint Manufacturing', page: 'paint', icon: '🎨' },
                { name: 'Carbon Credits', page: 'carbon', icon: '🌱' },
                { name: 'CRM', page: 'crm', icon: '🤝' },
                { name: 'Finance', page: 'finance', icon: '💰' },
                { name: 'HRM', page: 'hrm', icon: '👥' },
                { name: 'Inventory', page: 'inventory', icon: '📦' },
                { name: 'Booking', page: 'booking', icon: '📅' },
                { name: 'LMS', page: 'lms', icon: '📚' },
                { name: 'Field Service', page: 'fieldservice', icon: '🔧' },
                { name: 'Farmer Portal', page: 'farmerportal', icon: '👨‍🌾' },
                { name: 'Survey', page: 'survey', icon: '📝' },
                { name: 'Schemes', page: 'schemes', icon: '🏛️' },
                { name: 'Logistics', page: 'logistics', icon: '🚚' },
                { name: 'Water Management', page: 'water', icon: '💧' },
                { name: 'Command Center', page: 'command', icon: '🎯' }
            ];

            const filtered = pages.filter(p =>
                p.name.toLowerCase().includes(query.toLowerCase())
            ).slice(0, 8);

            if (filtered.length === 0) {
                results.innerHTML = '<div class="quick-search-empty">No results found</div>';
                return;
            }

            results.innerHTML = filtered.map((p, i) => `
                <div class="quick-search-item" data-page="${p.page}" data-index="${i}">
                    <span class="icon">${p.icon}</span>
                    <span class="name">${p.name}</span>
                </div>
            `).join('');

            // Add click handlers
            results.querySelectorAll('.item').forEach(item => {
                item.addEventListener('click', () => {
                    this.navigateTo(item.dataset.page);
                    this.closeQuickSearch();
                });
            });
        },

        handleSearchKey(e) {
            const items = document.querySelectorAll('.quick-search-item');
            const active = document.querySelector('.quick-search-item.active');
            const indices = Array.from(items).map(i => parseInt(i.dataset.index));

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const next = active ? parseInt(active.dataset.index) + 1 : 0;
                this.highlightItem(items, indices.includes(next) ? next : indices[0]);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prev = active ? parseInt(active.dataset.index) - 1 : indices.length - 1;
                this.highlightItem(items, indices.includes(prev) ? prev : indices[indices.length - 1]);
            } else if (e.key === 'Enter' && active) {
                e.preventDefault();
                this.navigateTo(active.dataset.page);
                this.closeQuickSearch();
            }
        },

        highlightItem(items, index) {
            items.forEach(i => i.classList.remove('active'));
            const target = document.querySelector(`.quick-search-item[data-index="${index}"]`);
            if (target) target.classList.add('active');
        },

        showHelp() {
            const help = document.createElement('div');
            help.className = 'shortcuts-modal';
            help.innerHTML = `
                <div class="shortcuts-content">
                    <h2>⌨️ Keyboard Shortcuts</h2>
                    <div class="shortcuts-list">
                        ${Object.entries(this.shortcuts).map(([key, desc]) => `
                            <div class="shortcut-item">
                                <kbd>${key.replace('mod', '⌘')}</kbd>
                                <span>${desc}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            document.body.appendChild(help);
            help.addEventListener('click', (e) => {
                if (e.target === help) help.remove();
            });
        },

        showHints() {
            // Add hint to UI
            const hint = document.createElement('div');
            hint.className = 'keyboard-hint';
            hint.innerHTML = 'Press ⌘K for quick search';
            document.body.appendChild(hint);
        }
    };

    // ============================================
    // 3. PERFORMANCE OPTIMIZATIONS
    // ============================================
    window.PerformanceUtils = {
        init() {
            this.addStyles();
            this.lazyLoadImages();
        },

        addStyles() {
            const style = document.createElement('style');
            style.textContent = `
                /* Dark Mode */
                body.dark-mode {
                    --bg-primary: #1a1a2e;
                    --bg-secondary: #16213e;
                    --bg-tertiary: #0f3460;
                    --text-primary: #eee;
                    --text-secondary: #aaa;
                    --border-color: #333;
                }
                body.dark-mode .sidebar { background: #16213e; }
                body.dark-mode .main-content { background: #1a1a2e; }
                body.dark-mode .card, body.dark-mode .ent-card {
                    background: #16213e;
                    border-color: #333;
                }
                
                /* Quick Search */
                .quick-search-modal {
                    position: fixed;
                    inset: 0;
                    z-index: 10000;
                    display: flex;
                    align-items: flex-start;
                    justify-content: center;
                    padding-top: 100px;
                }
                .quick-search-overlay {
                    position: absolute;
                    inset: 0;
                    background: rgba(0,0,0,0.5);
                }
                .quick-search-container {
                    position: relative;
                    width: 500px;
                    max-width: 90%;
                    background: var(--bg-primary);
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }
                .quick-search-input {
                    width: 100%;
                    padding: 16px 20px;
                    font-size: 18px;
                    border: none;
                    background: transparent;
                    color: var(--text-primary);
                    outline: none;
                }
                .quick-search-results {
                    max-height: 300px;
                    overflow-y: auto;
                }
                .quick-search-item {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 12px 20px;
                    cursor: pointer;
                    transition: background 0.1s;
                }
                .quick-search-item:hover, .quick-search-item.active {
                    background: var(--bg-tertiary);
                }
                .quick-search-item .icon { font-size: 20px; }
                .quick-search-item .name { font-size: 15px; }
                .quick-search-empty {
                    padding: 20px;
                    text-align: center;
                    color: var(--text-secondary);
                }
                .quick-search-hints {
                    display: flex;
                    gap: 20px;
                    padding: 12px 20px;
                    border-top: 1px solid var(--border-color);
                    font-size: 12px;
                    color: var(--text-secondary);
                }
                
                /* Shortcuts Modal */
                .shortcuts-modal {
                    position: fixed;
                    inset: 0;
                    background: rgba(0,0,0,0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10001;
                }
                .shortcuts-content {
                    background: var(--bg-primary);
                    padding: 30px;
                    border-radius: 12px;
                    max-width: 400px;
                }
                .shortcuts-content h2 { margin-top: 0; }
                .shortcut-item {
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                }
                kbd {
                    background: var(--bg-tertiary);
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-family: monospace;
                }
                
                /* Keyboard Hint */
                .keyboard-hint {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: var(--bg-tertiary);
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-size: 12px;
                    opacity: 0.7;
                    z-index: 100;
                }
            `;
            document.head.appendChild(style);
        },

        lazyLoadImages() {
            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src;
                            observer.unobserve(img);
                        }
                    });
                });

                document.querySelectorAll('img[data-src]').forEach(img => {
                    observer.observe(img);
                });
            }
        }
    };

    // ============================================
    // 4. INITIALIZE ON LOAD
    // ============================================
    document.addEventListener('DOMContentLoaded', () => {
        window.DarkMode.init();
        window.KeyboardShortcuts.init();
        window.PerformanceUtils.init();
    });

})();

console.log('✅ UX Enhancements loaded: Dark Mode, Keyboard Shortcuts, Quick Search');

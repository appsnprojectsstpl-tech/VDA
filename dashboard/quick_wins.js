// =========================================
// QUICK WINS - Instant Feature Enhancements
// Dark Mode, Quick Actions, Favorites
// =========================================

(function () {
    'use strict';

    // ========================================
    // 1. ENHANCED DARK/LIGHT MODE TOGGLE
    // ========================================

    const ThemeManager = {
        isDark: true,

        init() {
            // Check localStorage or system preference
            const saved = localStorage.getItem('vedavathi-theme');
            if (saved) {
                this.isDark = saved === 'dark';
            } else {
                this.isDark = !window.matchMedia('(prefers-color-scheme: light)').matches;
            }
            this.apply();
            this.updateToggleButton();
        },

        toggle() {
            this.isDark = !this.isDark;
            localStorage.setItem('vedavathi-theme', this.isDark ? 'dark' : 'light');
            this.apply();
            this.updateToggleButton();
        },

        apply() {
            document.documentElement.setAttribute('data-theme', this.isDark ? 'dark' : 'light');

            // Add/remove light class for CSS
            if (!this.isDark) {
                document.body.classList.add('light-theme');
            } else {
                document.body.classList.remove('light-theme');
            }
        },

        updateToggleButton() {
            const btn = document.getElementById('themeToggle');
            if (btn) {
                btn.innerHTML = this.isDark ? '☀️' : '🌙';
                btn.title = this.isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode';
            }
        }
    };

    // ========================================
    // 2. QUICK ACTIONS DROPDOWN
    // ========================================

    const QuickActions = {
        actions: [
            { id: 'add-milk', icon: '🥛', label: 'Add Milk Entry', page: 'cattle' },
            { id: 'add-egg', icon: '🥚', label: 'Record Eggs', page: 'poultry' },
            { id: 'add-animal', icon: '🐄', label: 'Register Animal', page: 'cattle' },
            { id: 'new-booking', icon: '📅', label: 'New Booking', page: 'booking' },
            { id: 'raise-alert', icon: '🚨', label: 'Raise Alert', page: 'command' },
            { id: 'view-reports', icon: '📊', label: 'View Reports', page: 'bi' },
            { id: 'add-expense', icon: '💸', label: 'Add Expense', page: 'finance2' },
            { id: 'inventory-check', icon: '📦', label: 'Inventory Check', page: 'inventory' }
        ],

        init() {
            this.createDropdown();
            this.bindEvents();
        },

        createDropdown() {
            const headerActions = document.querySelector('.header-actions');
            if (!headerActions) return;

            // Create Quick Actions button
            const btn = document.createElement('button');
            btn.id = 'quickActionsBtn';
            btn.className = 'icon-btn';
            btn.innerHTML = '⚡';
            btn.title = 'Quick Actions';
            btn.setAttribute('aria-label', 'Quick Actions menu');
            btn.setAttribute('aria-expanded', 'false');

            // Create dropdown menu
            const dropdown = document.createElement('div');
            dropdown.id = 'quickActionsDropdown';
            dropdown.className = 'quick-actions-dropdown';
            dropdown.innerHTML = `
                <div class="quick-actions-header">
                    <span>⚡ Quick Actions</span>
                </div>
                <div class="quick-actions-list">
                    ${this.actions.map(action => `
                        <button class="quick-action-item" data-action="${action.id}" data-page="${action.page}">
                            <span class="qa-icon">${action.icon}</span>
                            <span class="qa-label">${action.label}</span>
                        </button>
                    `).join('')}
                </div>
            `;

            // Insert after theme toggle
            const themeToggle = document.getElementById('themeToggle');
            if (themeToggle && themeToggle.nextSibling) {
                headerActions.insertBefore(btn, themeToggle.nextSibling);
            } else {
                headerActions.appendChild(btn);
            }
            headerActions.appendChild(dropdown);

            // Bind click events to actions
            dropdown.querySelectorAll('.quick-action-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    const page = e.currentTarget.dataset.page;
                    this.executeAction(page);
                });
            });
        },

        bindEvents() {
            const btn = document.getElementById('quickActionsBtn');
            const dropdown = document.getElementById('quickActionsDropdown');

            if (!btn || !dropdown) return;

            // Toggle dropdown
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = dropdown.classList.contains('open');
                this.closeAll();
                if (!isOpen) {
                    dropdown.classList.add('open');
                    btn.setAttribute('aria-expanded', 'true');
                }
            });

            // Close when clicking outside
            document.addEventListener('click', (e) => {
                if (!dropdown.contains(e.target) && e.target !== btn) {
                    this.closeAll();
                }
            });
        },

        closeAll() {
            document.querySelectorAll('.quick-actions-dropdown.open').forEach(d => {
                d.classList.remove('open');
            });
            const btn = document.getElementById('quickActionsBtn');
            if (btn) btn.setAttribute('aria-expanded', 'false');
        },

        executeAction(page) {
            this.closeAll();
            // Navigate to the page
            if (typeof navigateTo === 'function') {
                navigateTo(page);
            } else if (typeof loadPage === 'function') {
                loadPage(page);
            }
        }
    };

    // ========================================
    // 3. FAVORITES SYSTEM
    // ========================================

    const FavoritesManager = {
        favorites: [],

        init() {
            // Load from localStorage
            const saved = localStorage.getItem('vedavathi-favorites');
            if (saved) {
                this.favorites = JSON.parse(saved);
            }
            this.createUI();
            this.updateSidebarFavorites();
        },

        createUI() {
            const headerActions = document.querySelector('.header-actions');
            if (!headerActions) return;

            // Create Favorites button
            const btn = document.createElement('button');
            btn.id = 'favoritesBtn';
            btn.className = 'icon-btn';
            btn.innerHTML = '⭐';
            btn.title = 'Favorites';
            btn.setAttribute('aria-label', 'View Favorites');
            btn.setAttribute('aria-expanded', 'false');

            // Create favorites dropdown
            const dropdown = document.createElement('div');
            dropdown.id = 'favoritesDropdown';
            dropdown.className = 'favorites-dropdown';
            dropdown.innerHTML = `
                <div class="favorites-header">
                    <span>⭐ My Favorites</span>
                    <button class="manage-favs" onclick="FavoritesManager.openManager()">Manage</button>
                </div>
                <div class="favorites-list" id="favoritesList">
                    ${this.getFavoritesHTML()}
                </div>
            `;

            // Insert after Quick Actions
            const quickActions = document.getElementById('quickActionsBtn');
            if (quickActions && quickActions.nextSibling) {
                headerActions.insertBefore(btn, quickActions.nextSibling.nextSibling);
            }
            headerActions.appendChild(dropdown);

            // Bind events
            this.bindEvents();
        },

        bindEvents() {
            const btn = document.getElementById('favoritesBtn');
            const dropdown = document.getElementById('favoritesDropdown');

            if (!btn || !dropdown) return;

            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = dropdown.classList.contains('open');
                QuickActions.closeAll();
                if (!isOpen) {
                    dropdown.classList.add('open');
                    btn.setAttribute('aria-expanded', 'true');
                }
            });

            document.addEventListener('click', (e) => {
                if (!dropdown.contains(e.target) && e.target !== btn) {
                    dropdown.classList.remove('open');
                    btn.setAttribute('aria-expanded', 'false');
                }
            });
        },

        getFavoritesHTML() {
            if (this.favorites.length === 0) {
                return '<div class="no-favorites">No favorites yet. Star pages from sidebar!</div>';
            }

            return this.favorites.map(fav => `
                <button class="favorite-item" data-page="${fav.page}">
                    <span class="fav-icon">${fav.icon}</span>
                    <span class="fav-label">${fav.label}</span>
                    <span class="fav-remove" data-page="${fav.page}">×</span>
                </button>
            `).join('');
        },

        updateSidebarFavorites() {
            // Add star icons to sidebar menu items
            document.querySelectorAll('.menu-item[data-page]').forEach(item => {
                const page = item.dataset.page;
                const existingStar = item.querySelector('.favorite-star');

                const isFavorite = this.favorites.some(f => f.page === page);

                if (isFavorite && !existingStar) {
                    const star = document.createElement('span');
                    star.className = 'favorite-star';
                    star.innerHTML = '⭐';
                    star.title = 'Remove from favorites';
                    item.appendChild(star);
                } else if (!isFavorite && existingStar) {
                    existingStar.remove();
                }
            });

            // Add click handlers for favorites
            document.querySelectorAll('.favorite-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    if (e.target.classList.contains('fav-remove')) {
                        e.stopPropagation();
                        this.removeFavorite(e.target.dataset.page);
                    } else {
                        const page = item.dataset.page;
                        if (typeof navigateTo === 'function') navigateTo(page);
                        else if (typeof loadPage === 'function') loadPage(page);
                    }
                });
            });
        },

        addFavorite(page, icon, label) {
            if (this.favorites.some(f => f.page === page)) return;

            this.favorites.push({ page, icon, label });
            this.save();
            this.refresh();
        },

        removeFavorite(page) {
            this.favorites = this.favorites.filter(f => f.page !== page);
            this.save();
            this.refresh();
        },

        toggleFavorite(page, icon, label) {
            if (this.favorites.some(f => f.page === page)) {
                this.removeFavorite(page);
            } else {
                this.addFavorite(page, icon, label);
            }
        },

        save() {
            localStorage.setItem('vedavathi-favorites', JSON.stringify(this.favorites));
        },

        refresh() {
            const list = document.getElementById('favoritesList');
            if (list) {
                list.innerHTML = this.getFavoritesHTML();
            }
            this.updateSidebarFavorites();
        },

        openManager() {
            // Toggle all stars in sidebar
            QuickActions.closeAll();
            const dropdown = document.getElementById('favoritesDropdown');
            if (dropdown) dropdown.classList.remove('open');

            // Show sidebar favorites management mode
            document.body.classList.toggle('favorites-manage-mode');

            // Add click-to-favorite to sidebar items
            if (document.body.classList.contains('favorites-manage-mode')) {
                document.querySelectorAll('.menu-item[data-page]').forEach(item => {
                    item.style.cursor = 'pointer';
                    item.onclick = (e) => {
                        const page = item.dataset.page;
                        const iconEl = item.querySelector('.nav-icon');
                        const labelEl = item.querySelector('.nav-label');
                        const icon = iconEl ? iconEl.textContent : '📄';
                        const label = labelEl ? labelEl.textContent : page;
                        this.toggleFavorite(page, icon, label);
                    };
                });

                // Show instruction toast
                this.showToast('Click on pages to add/remove from favorites. Click again to exit manage mode.');
            } else {
                // Restore normal navigation
                document.querySelectorAll('.menu-item[data-page]').forEach(item => {
                    item.style.cursor = '';
                    item.onclick = null;
                });
            }
        },

        showToast(message) {
            const toast = document.createElement('div');
            toast.className = 'feature-toast';
            toast.innerHTML = `
                <span class="toast-icon">ℹ️</span>
                <span class="toast-message">${message}</span>
                <button class="toast-close" onclick="this.parentElement.remove()">×</button>
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.classList.add('show'), 100);
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 5000);
        }
    };

    // ========================================
    // 4. RECENTLY VIEWED
    // ========================================

    const RecentManager = {
        recent: [],
        maxItems: 5,

        init() {
            const saved = localStorage.getItem('vedavathi-recent');
            if (saved) {
                this.recent = JSON.parse(saved);
            }
        },

        add(page, icon, label) {
            // Remove if already exists
            this.recent = this.recent.filter(r => r.page !== page);

            // Add to beginning
            this.recent.unshift({ page, icon, label, time: Date.now() });

            // Keep only maxItems
            if (this.recent.length > this.maxItems) {
                this.recent = this.recent.slice(0, this.maxItems);
            }

            this.save();
        },

        save() {
            localStorage.setItem('vedavathi-recent', JSON.stringify(this.recent));
        }
    };

    // ========================================
    // 5. KEYBOARD SHORTCUTS
    // ========================================

    const KeyboardShortcuts = {
        shortcuts: {
            'd': 'Toggle Dark Mode',
            'f': 'Open Favorites',
            'q': 'Quick Actions',
            's': 'Focus Search',
            'Escape': 'Close Menus',
            '?': 'Show Shortcuts'
        },

        init() {
            document.addEventListener('keydown', (e) => {
                // Don't trigger if typing in input
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

                // Handle shortcuts
                switch (e.key.toLowerCase()) {
                    case 'd':
                        if (!e.ctrlKey && !e.metaKey) {
                            ThemeManager.toggle();
                        }
                        break;
                    case 'f':
                        if (!e.ctrlKey && !e.metaKey) {
                            const btn = document.getElementById('favoritesBtn');
                            if (btn) btn.click();
                        }
                        break;
                    case 'q':
                        if (!e.ctrlKey && !e.metaKey) {
                            const btn = document.getElementById('quickActionsBtn');
                            if (btn) btn.click();
                        }
                        break;
                    case 's':
                        if (!e.ctrlKey && !e.metaKey) {
                            e.preventDefault();
                            const search = document.getElementById('globalSearch');
                            if (search) search.focus();
                        }
                        break;
                    case 'escape':
                        QuickActions.closeAll();
                        document.getElementById('favoritesDropdown')?.classList.remove('open');
                        document.body.classList.remove('favorites-manage-mode');
                        break;
                    case '?':
                        this.showHelp();
                        break;
                }
            });
        },

        showHelp() {
            const helpHtml = `
                <div class="keyboard-help">
                    <h3>⌨️ Keyboard Shortcuts</h3>
                    <div class="shortcuts-grid">
                        ${Object.entries(this.shortcuts).map(([key, desc]) => `
                            <div class="shortcut-item">
                                <kbd>${key}</kbd>
                                <span>${desc}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;

            // Create modal
            const modal = document.createElement('div');
            modal.className = 'shortcuts-modal-overlay';
            modal.innerHTML = `
                <div class="shortcuts-modal">
                    <div class="shortcuts-modal-header">
                        <h2>⌨️ Keyboard Shortcuts</h2>
                        <button class="close-btn" onclick="this.closest('.shortcuts-modal-overlay').remove()">×</button>
                    </div>
                    <div class="shortcuts-modal-body">
                        ${Object.entries(this.shortcuts).map(([key, desc]) => `
                            <div class="shortcut-row">
                                <kbd>${key}</kbd>
                                <span>${desc}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;

            modal.addEventListener('click', (e) => {
                if (e.target === modal) modal.remove();
            });

            document.body.appendChild(modal);
        }
    };

    // ========================================
    // INITIALIZE ALL FEATURES
    // ========================================

    function initQuickWins() {
        ThemeManager.init();
        QuickActions.init();
        FavoritesManager.init();
        RecentManager.init();
        KeyboardShortcuts.init();

        // Add CSS for new features
        addQuickWinsStyles();

        console.log('✅ Quick Wins Features Loaded');
    }

    // Add CSS styles dynamically
    function addQuickWinsStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* ===== LIGHT THEME ===== */
            :root[data-theme="light"],
            body.light-theme {
                --bg-primary: #f8fafc;
                --bg-secondary: #ffffff;
                --bg-tertiary: #f1f5f9;
                --panel-bg: #ffffff;
                --bg-card: rgba(0, 0, 0, 0.03);
                --bg-card-hover: rgba(0, 0, 0, 0.06);
                --border: rgba(0, 0, 0, 0.1);
                --border-bright: rgba(0, 0, 0, 0.2);
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --text-muted: #94a3b8;
            }
            
            body.light-theme .sidebar {
                background: #ffffff !important;
                border-right: 1px solid rgba(0,0,0,0.1) !important;
            }
            
            body.light-theme .menu-item:hover,
            body.light-theme .menu-item.active {
                background: rgba(0, 0, 0, 0.05) !important;
            }
            
            body.light-theme .page-area,
            body.light-theme .main-content {
                background: #f8fafc !important;
            }
            
            body.light-theme .glass-dark,
            body.light-theme .kpi-card {
                background: #ffffff !important;
                border: 1px solid rgba(0,0,0,0.1) !important;
            }
            
            /* ===== QUICK ACTIONS DROPDOWN ===== */
            .quick-actions-dropdown {
                position: absolute;
                top: 100%;
                right: 0;
                width: 220px;
                background: var(--panel-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                z-index: 1000;
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                transition: all 0.2s ease;
                margin-top: 8px;
            }
            
            .quick-actions-dropdown.open {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
            
            .quick-actions-header {
                padding: 12px 16px;
                border-bottom: 1px solid var(--border);
                font-weight: 600;
                font-size: 0.85rem;
                color: var(--text-secondary);
            }
            
            .quick-actions-list {
                padding: 8px;
                max-height: 300px;
                overflow-y: auto;
            }
            
            .quick-action-item {
                display: flex;
                align-items: center;
                gap: 10px;
                width: 100%;
                padding: 10px 12px;
                background: transparent;
                border: none;
                border-radius: 8px;
                color: var(--text-primary);
                cursor: pointer;
                transition: background 0.15s;
                text-align: left;
            }
            
            .quick-action-item:hover {
                background: var(--bg-card-hover);
            }
            
            .qa-icon {
                font-size: 1.1rem;
            }
            
            .qa-label {
                font-size: 0.875rem;
            }
            
            /* ===== FAVORITES DROPDOWN ===== */
            .favorites-dropdown {
                position: absolute;
                top: 100%;
                right: 0;
                width: 240px;
                background: var(--panel-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                z-index: 1000;
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                transition: all 0.2s ease;
                margin-top: 8px;
            }
            
            .favorites-dropdown.open {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
            
            .favorites-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 16px;
                border-bottom: 1px solid var(--border);
            }
            
            .favorites-header span {
                font-weight: 600;
                font-size: 0.85rem;
                color: var(--text-secondary);
            }
            
            .manage-favs {
                background: transparent;
                border: none;
                color: var(--primary);
                font-size: 0.75rem;
                cursor: pointer;
                text-decoration: underline;
            }
            
            .favorites-list {
                padding: 8px;
                max-height: 250px;
                overflow-y: auto;
            }
            
            .no-favorites {
                padding: 20px;
                text-align: center;
                color: var(--text-muted);
                font-size: 0.85rem;
            }
            
            .favorite-item {
                display: flex;
                align-items: center;
                gap: 10px;
                width: 100%;
                padding: 10px 12px;
                background: transparent;
                border: none;
                border-radius: 8px;
                color: var(--text-primary);
                cursor: pointer;
                transition: background 0.15s;
                text-align: left;
            }
            
            .favorite-item:hover {
                background: var(--bg-card-hover);
            }
            
            .fav-icon {
                font-size: 1.1rem;
            }
            
            .fav-label {
                flex: 1;
                font-size: 0.875rem;
            }
            
            .fav-remove {
                opacity: 0;
                color: var(--red);
                font-size: 1.2rem;
                cursor: pointer;
                padding: 2px 6px;
            }
            
            .favorite-item:hover .fav-remove {
                opacity: 1;
            }
            
            .favorite-star {
                position: absolute;
                right: 10px;
                font-size: 0.8rem;
                cursor: pointer;
            }
            
            .menu-item {
                position: relative;
            }
            
            /* ===== TOAST NOTIFICATIONS ===== */
            .feature-toast {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%) translateY(100px);
                background: var(--panel-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 14px 20px;
                display: flex;
                align-items: center;
                gap: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.4);
                z-index: 9999;
                opacity: 0;
                transition: all 0.3s ease;
            }
            
            .feature-toast.show {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
            
            .toast-icon {
                font-size: 1.2rem;
            }
            
            .toast-message {
                font-size: 0.9rem;
                color: var(--text-primary);
            }
            
            .toast-close {
                background: transparent;
                border: none;
                color: var(--text-muted);
                font-size: 1.2rem;
                cursor: pointer;
                padding: 0 4px;
            }
            
            /* ===== KEYBOARD SHORTCUTS MODAL ===== */
            .shortcuts-modal-overlay {
                position: fixed;
                inset: 0;
                background: rgba(0,0,0,0.7);
                backdrop-filter: blur(4px);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
            }
            
            .shortcuts-modal {
                background: var(--panel-bg);
                border: 1px solid var(--border);
                border-radius: 16px;
                width: 90%;
                max-width: 400px;
                overflow: hidden;
            }
            
            .shortcuts-modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 16px 20px;
                border-bottom: 1px solid var(--border);
            }
            
            .shortcuts-modal-header h2 {
                font-size: 1.1rem;
                margin: 0;
            }
            
            .shortcuts-modal-header .close-btn {
                background: transparent;
                border: none;
                color: var(--text-muted);
                font-size: 1.5rem;
                cursor: pointer;
            }
            
            .shortcuts-modal-body {
                padding: 16px 20px;
            }
            
            .shortcut-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid var(--border);
            }
            
            .shortcut-row:last-child {
                border-bottom: none;
            }
            
            .shortcut-row kbd {
                background: var(--bg-tertiary);
                padding: 4px 10px;
                border-radius: 6px;
                font-family: var(--font-mono);
                font-size: 0.85rem;
            }
            
            .shortcut-row span {
                color: var(--text-secondary);
                font-size: 0.9rem;
            }
            
            /* ===== RESPONSIVE ===== */
            @media (max-width: 768px) {
                .quick-actions-dropdown,
                .favorites-dropdown {
                    width: calc(100vw - 40px);
                    right: -60px;
                }
            }
        `;

        document.head.appendChild(style);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initQuickWins);
    } else {
        initQuickWins();
    }

    // Expose globals for external access
    window.ThemeManager = ThemeManager;
    window.FavoritesManager = FavoritesManager;
    window.RecentManager = RecentManager;
    window.QuickActions = QuickActions;

})();

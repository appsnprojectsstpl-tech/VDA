// =========================================
// PUSH NOTIFICATIONS SYSTEM
// Farm Alerts, Reminders, Updates
// =========================================

(function () {
    'use strict';

    const PushNotifications = {
        permission: 'default',
        subscription: null,

        // Notification types
        types: {
            alert: { icon: '🚨', title: 'Alert', color: '#ef4444' },
            info: { icon: 'ℹ️', title: 'Info', color: '#3b82f6' },
            success: { icon: '✅', title: 'Success', color: '#22c55e' },
            warning: { icon: '⚠️', title: 'Warning', color: '#f59e0b' }
        },

        init() {
            this.checkPermission();
            this.setupServiceWorker();
            this.bindEvents();
            console.log('🔔 Push Notifications System Ready');
        },

        checkPermission() {
            if (!('Notification' in window)) {
                console.warn('Notifications not supported');
                return;
            }
            this.permission = Notification.permission;
        },

        async requestPermission() {
            if (!('Notification' in window)) {
                return false;
            }

            if (this.permission === 'granted') {
                return true;
            }

            if (this.permission === 'denied') {
                console.warn('Notification permission denied');
                return false;
            }

            try {
                const permission = await Notification.requestPermission();
                this.permission = permission;
                return permission === 'granted';
            } catch (e) {
                console.error('Error requesting notification permission:', e);
                return false;
            }
        },

        async setupServiceWorker() {
            if ('serviceWorker' in navigator) {
                try {
                    const registration = await navigator.serviceWorker.ready;
                    this.setupPushManager(registration);
                } catch (e) {
                    console.log('Service Worker not ready yet');
                }
            }
        },

        async setupPushManager(registration) {
            if (!('pushManager' in registration)) {
                return;
            }

            try {
                const subscription = await registration.pushManager.getSubscription();
                if (subscription) {
                    this.subscription = subscription;
                    this.sendSubscriptionToServer(subscription);
                }
            } catch (e) {
                console.error('Error setting up push:', e);
            }
        },

        async subscribe() {
            const granted = await this.requestPermission();
            if (!granted) {
                return false;
            }

            // For demo, just show a local notification
            this.show('info', 'Notifications Enabled', 'You will now receive farm alerts and updates!');
            return true;
        },

        sendSubscriptionToServer(subscription) {
            // In production, send to your server
            console.log('Push subscription:', subscription);
        },

        // Show a notification
        show(type, title, body, options = {}) {
            if (this.permission !== 'granted') {
                // Fallback to in-app toast
                this.showToast(type, title, body);
                return;
            }

            const config = this.types[type] || this.types.info;

            const notification = new Notification(`${config.icon} ${title}`, {
                body: body,
                icon: options.icon || '/icon-192.png',
                badge: '/icon-72.png',
                tag: options.tag || 'vedavathi-notification',
                requireInteraction: options.requireInteraction || false,
                data: options.data || {}
            });

            notification.onclick = () => {
                if (options.onClick) {
                    options.onClick();
                } else {
                    window.focus();
                    notification.close();
                }
            };

            // Auto close after delay
            if (!options.persistent) {
                setTimeout(() => notification.close(), options.duration || 5000);
            }

            return notification;
        },

        // Show in-app toast notification
        showToast(type, title, body) {
            const config = this.types[type] || this.types.info;

            const toast = document.createElement('div');
            toast.className = `push-toast push-toast-${type}`;
            toast.innerHTML = `
                <span class="push-toast-icon">${config.icon}</span>
                <div class="push-toast-content">
                    <strong>${title}</strong>
                    <p>${body}</p>
                </div>
                <button class="push-toast-close" onclick="this.parentElement.remove()">×</button>
            `;

            // Add styles if not exists
            if (!document.getElementById('push-toast-styles')) {
                this.addToastStyles();
            }

            document.body.appendChild(toast);

            // Animate in
            requestAnimationFrame(() => {
                toast.classList.add('show');
            });

            // Auto remove
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 6000);
        },

        addToastStyles() {
            const style = document.createElement('style');
            style.id = 'push-toast-styles';
            style.textContent = `
                .push-toast {
                    position: fixed;
                    top: 80px;
                    right: 20px;
                    width: 320px;
                    max-width: calc(100vw - 40px);
                    background: var(--panel-bg);
                    border: 1px solid var(--border);
                    border-radius: 12px;
                    padding: 14px;
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
                    z-index: 9998;
                    transform: translateX(120%);
                    transition: transform 0.3s ease;
                }
                
                .push-toast.show {
                    transform: translateX(0);
                }
                
                .push-toast-icon {
                    font-size: 1.5rem;
                    flex-shrink: 0;
                }
                
                .push-toast-content {
                    flex: 1;
                }
                
                .push-toast-content strong {
                    display: block;
                    margin-bottom: 4px;
                    color: var(--text-primary);
                }
                
                .push-toast-content p {
                    margin: 0;
                    font-size: 0.85rem;
                    color: var(--text-secondary);
                }
                
                .push-toast-close {
                    background: transparent;
                    border: none;
                    color: var(--text-muted);
                    font-size: 1.3rem;
                    cursor: pointer;
                    padding: 0;
                    line-height: 1;
                }
                
                .push-toast-alert {
                    border-left: 4px solid #ef4444;
                }
                
                .push-toast-warning {
                    border-left: 4px solid #f59e0b;
                }
                
                .push-toast-success {
                    border-left: 4px solid #22c55e;
                }
                
                .push-toast-info {
                    border-left: 4px solid #3b82f6;
                }
                
                @media (max-width: 480px) {
                    .push-toast {
                        right: 10px;
                        left: 10px;
                        width: auto;
                    }
                }
            `;
            document.head.appendChild(style);
        },

        bindEvents() {
            // Add notification bell click handler
            const alertBtn = document.getElementById('alert-bell-btn');
            if (alertBtn) {
                alertBtn.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    this.showNotificationSettings();
                });
            }
        },

        showNotificationSettings() {
            const modal = document.createElement('div');
            modal.className = 'notification-settings-modal';
            modal.innerHTML = `
                <div class="notification-settings">
                    <div class="ns-header">
                        <h2>🔔 Notification Settings</h2>
                        <button class="ns-close" onclick="this.closest('.notification-settings-modal').remove()">×</button>
                    </div>
                    <div class="ns-body">
                        <div class="ns-section">
                            <h3>Alert Types</h3>
                            <label class="ns-toggle">
                                <input type="checkbox" id="ns-alerts" checked>
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">🚨 Farm Alerts</span>
                            </label>
                            <label class="ns-toggle">
                                <input type="checkbox" id="ns-milk" checked>
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">🥛 Milk Production</span>
                            </label>
                            <label class="ns-toggle">
                                <input type="checkbox" id="ns-energy" checked>
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">⚡ Energy Updates</span>
                            </label>
                            <label class="ns-toggle">
                                <input type="checkbox" id="ns-health">
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">🏥 Animal Health</span>
                            </label>
                            <label class="ns-toggle">
                                <input type="checkbox" id="ns-finance">
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">💰 Financial Alerts</span>
                            </label>
                        </div>
                        <div class="ns-section">
                            <h3>Preferences</h3>
                            <label class="ns-toggle">
                                <input type="checkbox" id="ns-sound" checked>
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">🔊 Sound</span>
                            </label>
                            <label class="ns-toggle">
                                <input type="checkbox" id="ns-desktop">
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">🖥️ Desktop Notifications</span>
                            </label>
                        </div>
                        <button class="ns-enable-btn" id="enableNotificationsBtn">
                            ${this.permission === 'granted' ? '✅ Notifications Enabled' : '🔔 Enable Browser Notifications'}
                        </button>
                    </div>
                </div>
            `;

            modal.addEventListener('click', (e) => {
                if (e.target === modal) modal.remove();
            });

            document.body.appendChild(modal);

            // Add styles
            this.addSettingsStyles();

            // Bind enable button
            const enableBtn = document.getElementById('enableNotificationsBtn');
            if (enableBtn) {
                enableBtn.addEventListener('click', () => {
                    this.subscribe();
                    enableBtn.textContent = '✅ Notifications Enabled';
                    enableBtn.disabled = true;
                });
            }
        },

        addSettingsStyles() {
            if (document.getElementById('ns-styles')) return;

            const style = document.createElement('style');
            style.id = 'ns-styles';
            style.textContent = `
                .notification-settings-modal {
                    position: fixed;
                    inset: 0;
                    background: rgba(0,0,0,0.7);
                    backdrop-filter: blur(4px);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                }
                
                .notification-settings {
                    background: var(--panel-bg);
                    border: 1px solid var(--border);
                    border-radius: 16px;
                    width: 90%;
                    max-width: 400px;
                    max-height: 80vh;
                    overflow-y: auto;
                }
                
                .ns-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 16px 20px;
                    border-bottom: 1px solid var(--border);
                }
                
                .ns-header h2 {
                    font-size: 1.1rem;
                    margin: 0;
                }
                
                .ns-close {
                    background: transparent;
                    border: none;
                    color: var(--text-muted);
                    font-size: 1.5rem;
                    cursor: pointer;
                }
                
                .ns-body {
                    padding: 20px;
                }
                
                .ns-section {
                    margin-bottom: 24px;
                }
                
                .ns-section h3 {
                    font-size: 0.85rem;
                    color: var(--text-secondary);
                    margin-bottom: 12px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                
                .ns-toggle {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 10px 0;
                    cursor: pointer;
                }
                
                .ns-toggle input {
                    display: none;
                }
                
                .toggle-slider {
                    width: 44px;
                    height: 24px;
                    background: var(--bg-tertiary);
                    border-radius: 12px;
                    position: relative;
                    transition: background 0.2s;
                }
                
                .toggle-slider::after {
                    content: '';
                    position: absolute;
                    top: 2px;
                    left: 2px;
                    width: 20px;
                    height: 20px;
                    background: white;
                    border-radius: 50%;
                    transition: transform 0.2s;
                }
                
                .ns-toggle input:checked + .toggle-slider {
                    background: var(--primary);
                }
                
                .ns-toggle input:checked + .toggle-slider::after {
                    transform: translateX(20px);
                }
                
                .toggle-label {
                    flex: 1;
                    font-size: 0.95rem;
                }
                
                .ns-enable-btn {
                    width: 100%;
                    padding: 14px;
                    background: var(--primary);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 0.95rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: opacity 0.2s;
                }
                
                .ns-enable-btn:hover {
                    opacity: 0.9;
                }
                
                .ns-enable-btn:disabled {
                    background: var(--green);
                    cursor: default;
                }
            `;
            document.head.appendChild(style);
        }
    };

    // ========================================
    // FARM-SPECIFIC ALERTS
    // ========================================

    const FarmAlerts = {
        alerts: [],

        init() {
            this.setupDemoAlerts();
        },

        // Setup some demo farm alerts
        setupDemoAlerts() {
            this.alerts = [
                {
                    id: 1,
                    type: 'warning',
                    title: 'Low Milk Production',
                    message: 'Zone B milk production is 15% below target',
                    time: new Date(),
                    read: false
                },
                {
                    id: 2,
                    type: 'alert',
                    title: 'Temperature Alert',
                    message: 'Poultry shed 3 temperature above threshold',
                    time: new Date(Date.now() - 3600000),
                    read: false
                },
                {
                    id: 3,
                    type: 'info',
                    title: 'Vaccination Due',
                    message: '15 animals due for vaccination tomorrow',
                    time: new Date(Date.now() - 7200000),
                    read: true
                }
            ];

            this.updateBadge();
        },

        addAlert(alert) {
            const newAlert = {
                id: Date.now(),
                time: new Date(),
                read: false,
                ...alert
            };

            this.alerts.unshift(newAlert);
            this.updateBadge();

            // Show notification
            PushNotifications.show(alert.type, alert.title, alert.message);
        },

        updateBadge() {
            const badge = document.getElementById('alert-count-badge');
            if (!badge) return;

            const unread = this.alerts.filter(a => !a.read).length;

            if (unread > 0) {
                badge.textContent = unread > 9 ? '9+' : unread;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        },

        getUnreadCount() {
            return this.alerts.filter(a => !a.read).length;
        }
    };

    // Initialize
    function initPushNotifications() {
        PushNotifications.init();
        FarmAlerts.init();

        console.log('🔔 Push Notifications Module Loaded');
    }

    // Expose globals
    window.PushNotifications = PushNotifications;
    window.FarmAlerts = FarmAlerts;

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPushNotifications);
    } else {
        initPushNotifications();
    }

})();

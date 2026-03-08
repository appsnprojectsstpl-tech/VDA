// ============================================
// REST API WRAPPER FOR EXTERNAL INTEGRATIONS
// Phase 8: Mobile & Integration
// ============================================

/**
 * Vedavathi REST API
 * Provides external systems access to dashboard data
 * Use for: Zapier, Make.com, custom integrations, mobile apps
 */

window.VedavathiAPI = {
    baseUrl: null,
    apiKey: null,

    /**
     * Initialize API with credentials
     */
    init(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    },

    /**
     * Generic fetch wrapper with auth
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.apiKey}`,
            ...options.headers
        };

        try {
            const response = await fetch(url, { ...options, headers });
            if (!response.ok) throw new Error(`API Error: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    },

    // ============================================
    // ENERGY MODULES
    // ============================================
    energy: {
        async getSolarStats() {
            const { data } = await window.dbSolar.getEnergyStats();
            return data;
        },
        async getWindStats() {
            const { data: turbines } = await window.dbWind.getTurbines();
            const { data: readings } = await window.dbWind.getReadings();
            return { turbines: turbines?.length || 0, readings: readings?.length || 0 };
        },
        async getGridStatus() {
            const { data: readings } = await window.dbGrid.getReadings();
            const { data: alerts } = await window.dbGrid.getAlerts();
            return { readings: readings?.length || 0, alerts: alerts?.length || 0 };
        }
    },

    // ============================================
    // AGRICULTURE MODULES
    // ============================================
    agriculture: {
        async getDairyStats() {
            const { data: animals } = await window.dbCattle.getAnimals();
            const { data: milk } = await window.dbCattle.getMilk();
            return { animals: animals?.length || 0, records: milk?.length || 0 };
        },
        async getPoultryStats() {
            const { data: flocks } = await window.dbPoultry.getFlocks();
            const { data: batches } = await window.dbPoultry.getBatches();
            return { flocks: flocks?.length || 0, batches: batches?.length || 0 };
        },
        async getAquaStats() {
            const { data: ponds } = await window.dbAqua.getPonds();
            const { data: batches } = await window.dbAqua.getBatches();
            return { ponds: ponds?.length || 0, batches: batches?.length || 0 };
        }
    },

    // ============================================
    // ERP MODULES
    // ============================================
    erp: {
        async getFinanceSummary() {
            return await window.dbFinance.getFinancialSummary();
        },
        async getHRStats() {
            return await window.dbHRM.getEmployeeCount();
        },
        async getInventoryValue() {
            return await window.dbInventory.getInventoryValue();
        },
        async getCRMPipeline() {
            return await window.dbCRM.getSalesPipeline();
        }
    },

    // ============================================
    // CROSS-MODULE
    // ============================================
    dashboard: {
        /**
         * Get complete dashboard summary
         * Use for: Executive dashboards, KPIs
         */
        async getSummary() {
            const bi = await window.dbBI.getCrossModuleSummary();
            const finance = await window.dbFinance.getFinancialSummary();
            const hrm = await window.dbHRM.getEmployeeCount();

            return {
                timestamp: new Date().toISOString(),
                overview: bi.data,
                finance: finance.data,
                hrm: hrm.data
            };
        },

        /**
         * Get real-time alerts
         * Use for: Monitoring systems
         */
        async getAlerts() {
            const inv = await window.dbInventory.getStockAlerts();
            const workflow = await window.dbWorkflow.getPendingApprovals();
            const tickets = await window.dbTicketing.getTicketStats();

            return {
                lowStock: inv.data.lowStock,
                pendingApprovals: workflow.data?.length || 0,
                openTickets: tickets.data.open,
                timestamp: new Date().toISOString()
            };
        }
    },

    // ============================================
    // DATA EXPORT
    // ============================================
    export: {
        /**
         * Export data as JSON
         */
        async toJSON(table, filters = {}) {
            const data = await window.insforge.fetch(table);
            return JSON.stringify(data, null, 2);
        },

        /**
         * Export data as CSV
         */
        async toCSV(table) {
            const data = await window.insforge.fetch(table);
            if (!data?.length) return '';

            const headers = Object.keys(data[0]);
            const csvRows = [
                headers.join(','),
                ...data.map(row =>
                    headers.map(h => JSON.stringify(row[h] ?? '')).join(',')
                )
            ];
            return csvRows.join('\n');
        }
    },

    // ============================================
    // WEBHOOK INTEGRATION
    // ============================================
    webhooks: {
        /**
         * Register a webhook URL
         * Events: data_changed, alert_triggered, approval_needed
         */
        register(event, url) {
            const webhooks = JSON.parse(localStorage.getItem('vedavathi_webhooks') || '{}');
            webhooks[event] = url;
            localStorage.setItem('vedavathi_webhooks', JSON.stringify(webhooks));
        },

        /**
         * Trigger webhook for an event
         */
        async trigger(event, payload) {
            const webhooks = JSON.parse(localStorage.getItem('vedavathi_webhooks') || '{}');
            const url = webhooks[event];

            if (!url) return;

            try {
                await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ event, payload, timestamp: new Date().toISOString() })
                });
            } catch (error) {
                console.error('Webhook failed:', error);
            }
        }
    },

    // ============================================
    // MOBILE PUSH NOTIFICATIONS
    // ============================================
    notifications: {
        /**
         * Request notification permission
         */
        async requestPermission() {
            if (!('Notification' in window)) {
                console.warn('Notifications not supported');
                return false;
            }

            const permission = await Notification.requestPermission();
            return permission === 'granted';
        },

        /**
         * Show local notification
         */
        show(title, options = {}) {
            if (Notification.permission === 'granted') {
                new Notification(title, {
                    icon: '🌿',
                    badge: '🌿',
                    ...options
                });
            }
        },

        /**
         * Setup automatic alerts
         */
        setupAlerts() {
            // Check every 5 minutes
            setInterval(async () => {
                const alerts = await window.VedavathiAPI.dashboard.getAlerts();

                if (alerts.lowStock > 5) {
                    this.show('⚠️ Low Stock Alert', {
                        body: `${alerts.lowStock} products are low on stock`
                    });
                }

                if (alerts.pendingApprovals > 10) {
                    this.show('📋 Approvals Needed', {
                        body: `${alerts.pendingApprovals} items need your approval`
                    });
                }
            }, 5 * 60 * 1000);
        }
    }
};

// ============================================
// QUICK ACTION FUNCTIONS
// ============================================

/**
 * Quick action: Record milk entry
 */
window.recordMilk = async function (animalId, quantity, fat, rate) {
    return await window.dbCattle.recordMilk({
        animal_id: animalId,
        date: new Date().toISOString().split('T')[0],
        shift: new Date().getHours() < 12 ? 'morning' : 'evening',
        quantity_liters: quantity,
        fat_percent: fat,
        rate: rate
    });
};

/**
 * Quick action: Record egg production
 */
window.recordEggs = async function (batchId, total, broken, sold) {
    return await window.dbPoultry.recordEggs({
        batch_id: batchId,
        date: new Date().toISOString().split('T')[0],
        total_eggs: total,
        broken: broken || 0,
        sold: sold || 0
    });
};

/**
 * Quick action: Create expense
 */
window.createExpense = async function (category, amount, description) {
    return await window.dbFinance.addExpense({
        category,
        amount,
        description,
        date: new Date().toISOString().split('T')[0],
        status: 'approved'
    });
};

/**
 * Quick action: Mark attendance
 */
window.markAttendance = async function (employeeId, status = 'present') {
    return await window.dbHRM.markAttendance({
        employee_id: employeeId,
        date: new Date().toISOString().split('T')[0],
        check_in: new Date().toTimeString().split(' ')[0],
        status
    });
};

console.log('✅ REST API Wrapper loaded - Use window.VedavathiAPI for integrations');

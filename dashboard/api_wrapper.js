// ============================================
// REST API WRAPPER FOR EXTERNAL INTEGRATIONS
// Phase 8: Mobile & Integration
// ============================================

/**
 * Vedavathi REST API
 * Provides external systems access to dashboard data
 * Use for: Zapier, Make.com, custom integrations, mobile apps
 */

// Helper to get db module with fallback
function _getDb(module) {
    if (!window.db || !window.db[module]) {
        console.warn(`DB module '${module}' not initialized yet`);
        return null;
    }
    return window.db[module];
}

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
            const db = _getDb('solar');
            if (!db) return null;
            const { data } = await db.getEnergyStats();
            return data;
        },
        async getWindStats() {
            const db = _getDb('wind');
            if (!db) return { turbines: 0, readings: 0 };
            const { data: turbines } = await db.getTurbines();
            const { data: readings } = await db.getReadings();
            return { turbines: turbines?.length || 0, readings: readings?.length || 0 };
        },
        async getGridStatus() {
            const db = _getDb('grid');
            if (!db) return { readings: 0, alerts: 0 };
            const { data: readings } = await db.getReadings();
            const { data: alerts } = await db.getAlerts();
            return { readings: readings?.length || 0, alerts: alerts?.length || 0 };
        }
    },

    // ============================================
    // AGRICULTURE MODULES
    // ============================================
    agriculture: {
        async getDairyStats() {
            const db = _getDb('cattle');
            if (!db) return { animals: 0, records: 0 };
            const { data: animals } = await db.getAnimals();
            const { data: milk } = await db.getMilk();
            return { animals: animals?.length || 0, records: milk?.length || 0 };
        },
        async getPoultryStats() {
            const db = _getDb('poultry');
            if (!db) return { flocks: 0, batches: 0 };
            const { data: flocks } = await db.getFlocks();
            const { data: batches } = await db.getBatches();
            return { flocks: flocks?.length || 0, batches: batches?.length || 0 };
        },
        async getAquaStats() {
            const db = _getDb('aqua');
            if (!db) return { ponds: 0, batches: 0 };
            const { data: ponds } = await db.getPonds();
            const { data: batches } = await db.getBatches();
            return { ponds: ponds?.length || 0, batches: batches?.length || 0 };
        }
    },

    // ============================================
    // ERP MODULES
    // ============================================
    erp: {
        async getFinanceSummary() {
            const db = _getDb('finance');
            if (!db) return {};
            return await db.getFinancialSummary();
        },
        async getHRStats() {
            const db = _getDb('hrm');
            if (!db) return { count: 0 };
            return { count: await db.getEmployeeCount() };
        },
        async getInventoryValue() {
            const db = _getDb('inventory');
            if (!db) return 0;
            return await db.getInventoryValue();
        },
        async getCRMPipeline() {
            const db = _getDb('crm');
            if (!db) return [];
            return await db.getSalesPipeline();
        }
    },

    // ============================================
    // ANALYTICS
    // ============================================
    analytics: {
        async getSummary() {
            const bi = _getDb('bi');
            const finance = _getDb('finance');
            const hrm = _getDb('hrm');

            return {
                bi: bi ? await bi.getCrossModuleSummary() : {},
                finance: finance ? await finance.getFinancialSummary() : {},
                hrm: hrm ? await hrm.getEmployeeCount() : 0
            };
        },

        async getAlerts() {
            const inv = _getDb('inventory');
            const workflow = _getDb('workflow');
            const tickets = _getDb('ticketing');

            return {
                inventory: inv ? await inv.getStockAlerts() : [],
                workflow: workflow ? await workflow.getPendingApprovals() : [],
                tickets: tickets ? await tickets.getTicketStats() : {}
            };
        }
    },

    // ============================================
    // EXPORT UTILITIES
    // ============================================
    export: {
        async toJSON(table, filters = {}) {
            const data = await window.insforge.fetch(table);
            return JSON.stringify(data, null, 2);
        },

        async toCSV(table) {
            const data = await window.insforge.fetch(table);
            if (!data?.length) return '';

            const headers = Object.keys(data[0]);
            const rows = data.map(row => headers.map(h => row[h] ?? '').join(','));
            return [headers.join(','), ...rows].join('\n');
        }
    },

    // ============================================
    // WEBHOOK INTEGRATION
    // ============================================
    webhooks: {
        _handlers: {},

        register(event, url) {
            if (!this._handlers[event]) this._handlers[event] = [];
            this._handlers[event].push(url);
            console.log(`Webhook registered for event: ${event}`);
        },

        async trigger(event, payload) {
            const urls = this._handlers[event] || [];
            for (const url of urls) {
                try {
                    await fetch(url, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ event, payload, timestamp: new Date().toISOString() })
                    });
                } catch (e) {
                    console.error(`Webhook failed for ${event}:`, e);
                }
            }
        }
    }
};

// ============================================
// CONVENIENCE FUNCTIONS
// ============================================

/**
 * Record milk production (convenience wrapper)
 */
window.recordMilk = async function (animalId, quantity, fat, rate) {
    const db = _getDb('cattle');
    if (!db) return { error: 'Database not initialized' };
    return await db.recordMilk({
        animal_id: animalId,
        quantity,
        fat,
        rate,
        date: new Date().toISOString().split('T')[0]
    });
};

/**
 * Record egg collection (convenience wrapper)
 */
window.recordEggs = async function (batchId, total, broken, sold) {
    const db = _getDb('poultry');
    if (!db) return { error: 'Database not initialized' };
    return await db.recordEggs({
        batch_id: batchId,
        total,
        broken,
        sold,
        date: new Date().toISOString().split('T')[0]
    });
};

/**
 * Create expense record (convenience wrapper)
 */
window.createExpense = async function (category, amount, description) {
    const db = _getDb('finance');
    if (!db) return { error: 'Database not initialized' };
    return await db.addExpense({
        category,
        amount,
        description,
        date: new Date().toISOString().split('T')[0]
    });
};

/**
 * Mark employee attendance (convenience wrapper)
 */
window.markAttendance = async function (employeeId, status = 'present') {
    const db = _getDb('hrm');
    if (!db) return { error: 'Database not initialized' };
    return await db.markAttendance({
        employee_id: employeeId,
        status,
        date: new Date().toISOString().split('T')[0]
    });
};

console.log('✅ REST API Wrapper loaded - Use window.VedavathiAPI for integrations');

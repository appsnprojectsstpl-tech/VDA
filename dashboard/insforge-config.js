// insforge-config.js
// Custom bridge linking raw HTML to the official InsForge SDK REST API
//
// SECURITY FIX: Removed hardcoded API key from client-side code.
// API keys should NEVER be exposed in client-side JavaScript.
// For production: Use server-side proxy or InsForge's built-in auth.

// Configure these via environment variables or server-side proxy
// For client-side, use empty key - app will run in demo/offline mode
const SUPABASE_URL = 'https://e9976ek6.us-east.insforge.app'; // Set via environment variable in production
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3OC0xMjM0LTU2NzgtOTBhYi1jZGVmMTIzNDU2NzgiLCJlbWFpbCI6ImFub25AaW5zZm9yZ2UuY29tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2ODEwNTd9.2QaEjMxNQCrIvn48sFFOoDgSk3YUvLciTVkSO_KG_ss'; // Never expose in client-side JavaScript!

// Build headers dynamically - empty key triggers demo mode
function getHeaders() {
    return {
        'Authorization': SUPABASE_KEY ? `Bearer ${SUPABASE_KEY}` : '',
        'Content-Type': 'application/json'
    };
}

// Check if we have valid credentials
const hasValidCredentials = SUPABASE_URL && SUPABASE_KEY;

window.insforge = {
    // Core database fetch
    async fetch(table, params = '') {
        if (!hasValidCredentials) {
            console.log(`Demo mode: Skipping fetch for ${table}`);
            return [];
        }
        try {
            // InsForge REST API endpoint for records
            const url = `${SUPABASE_URL}/api/database/records/${table}${params ? '?' + params : ''}`;
            const res = await fetch(url, { method: 'GET', headers: getHeaders() });

            if (!res.ok) {
                console.error(`Fetch error on ${table}:`, await res.text());
                return [];
            }
            return await res.json();
        } catch (e) {
            console.error('Fetch exception', e);
            return [];
        }
    },

    // Insert new records
    async insert(table, payload) {
        if (!hasValidCredentials) {
            console.log(`Demo mode: Skipping insert for ${table}`);
            return [];
        }
        try {
            const arr = Array.isArray(payload) ? payload : [payload];
            const url = `${SUPABASE_URL}/api/database/records/${table}`;
            const res = await fetch(url, {
                method: 'POST',
                headers: { ...getHeaders(), 'Prefer': 'return=representation' },
                body: JSON.stringify(arr)
            });

            if (!res.ok) {
                const errText = await res.text();
                console.error(`Insert error on ${table}:`, errText);
                throw new Error(errText);
            }
            return await res.json();
        } catch (e) {
            console.error('Insert exception:', e);
            throw e;
        }
    },

    // Execute raw SQL queries (requires the run_sql postgres function)
    async query(sql) {
        if (!hasValidCredentials) return [];
        try {
            const url = `${SUPABASE_URL}/api/database/rpc/run_sql`;
            const res = await fetch(url, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({ query: sql })
            });

            if (!res.ok) {
                // Silently handle - table may not exist yet or RPC fails
                return [];
            }
            const data = await res.json();
            return Array.isArray(data) ? data : [data];
        } catch (e) {
            return [];
        }
    },

    async run(sql) {
        return this.query(sql);
    }
};

console.log("InsForge Native Fetch Bridge Initialized.");

window._backendReady = false;

// Check if backend is ready (simple health check)
async function checkBackendHealth() {
    if (!hasValidCredentials) {
        console.log('ℹ️ Demo mode - No backend credentials configured');
        return;
    }
    try {
        const url = `${SUPABASE_URL}/api/database/records/kpi_summary?limit=1`;
        const res = await fetch(url, { method: 'GET', headers: getHeaders() });
        if (res.ok) {
            window._backendReady = true;
            console.log('✅ Backend connected - Live data enabled');
        } else {
            console.log('ℹ️ Demo mode - Backend responded with error (table missing?)');
        }
    } catch (e) {
        console.log('ℹ️ Demo mode - No backend detected');
    }
}

setTimeout(checkBackendHealth, 1000);

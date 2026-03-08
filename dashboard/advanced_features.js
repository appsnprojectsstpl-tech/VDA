// ============================================
// ADVANCED FEATURES & CUSTOM REPORTS
// Phase 9: Advanced Analytics & Customization
// ============================================

(function () {
    'use strict';

    // ============================================
    // 1. CUSTOM REPORT BUILDER
    // ============================================
    window.ReportBuilder = {
        reports: [],

        init() {
            this.reports = JSON.parse(localStorage.getItem('custom_reports') || '[]');
        },

        /**
         * Create a custom report
         */
        create(config) {
            const report = {
                id: 'rpt_' + Date.now(),
                name: config.name,
                module: config.module,
                fields: config.fields || [],
                filters: config.filters || [],
                groupBy: config.groupBy,
                createdAt: new Date().toISOString()
            };

            this.reports.push(report);
            this.save();
            return report;
        },

        /**
         * Execute a report
         */
        async execute(reportId) {
            const report = this.reports.find(r => r.id === reportId);
            if (!report) throw new Error('Report not found');

            const tableName = this.getTableForModule(report.module);
            let data = await window.insforge.fetch(tableName);

            // Apply filters
            if (report.filters?.length) {
                data = data.filter(item => {
                    return report.filters.every(f => {
                        const value = item[f.field];
                        switch (f.operator) {
                            case 'equals': return value == f.value;
                            case 'contains': return String(value).toLowerCase().includes(f.value.toLowerCase());
                            case 'gt': return parseFloat(value) > parseFloat(f.value);
                            case 'lt': return parseFloat(value) < parseFloat(f.value);
                            default: return true;
                        }
                    });
                });
            }

            // Select specific fields
            if (report.fields?.length) {
                data = data.map(item => {
                    const result = {};
                    report.fields.forEach(f => result[f] = item[f]);
                    return result;
                });
            }

            // Group by
            if (report.groupBy) {
                const grouped = {};
                data.forEach(item => {
                    const key = item[report.groupBy] || 'Unknown';
                    grouped[key] = (grouped[key] || []).concat(item);
                });
                return { grouped, raw: data };
            }

            return { data };
        },

        getTableForModule(module) {
            const mapping = {
                'finance': 'fin_invoices',
                'hrm': 'hrm_employees',
                'inventory': 'inv_products',
                'crm': 'crm_leads',
                'dairy': 'cattle_animals',
                'poultry': 'poultry_flocks',
                'solar': 'solar_readings',
                'booking': 'bkg_bookings'
            };
            return mapping[module] || 'fin_invoices';
        },

        delete(reportId) {
            this.reports = this.reports.filter(r => r.id !== reportId);
            this.save();
        },

        save() {
            localStorage.setItem('custom_reports', JSON.stringify(this.reports));
        },

        /**
         * Show report builder UI
         */
        showBuilder() {
            const modal = document.createElement('div');
            modal.className = 'report-builder-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <h2>📊 Custom Report Builder</h2>
                    
                    <div class="form-group">
                        <label>Report Name</label>
                        <input type="text" id="reportName" placeholder="My Custom Report">
                    </div>
                    
                    <div class="form-group">
                        <label>Data Module</label>
                        <select id="reportModule">
                            <option value="finance">Finance</option>
                            <option value="hrm">HRM</option>
                            <option value="inventory">Inventory</option>
                            <option value="crm">CRM</option>
                            <option value="dairy">Dairy/Cattle</option>
                            <option value="poultry">Poultry</option>
                            <option value="solar">Solar Energy</option>
                            <option value="booking">Bookings</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Select Fields</label>
                        <div class="field-checkboxes" id="fieldCheckboxes"></div>
                    </div>
                    
                    <div class="form-group">
                        <label>Group By</label>
                        <select id="groupByField">
                            <option value="">None</option>
                        </select>
                    </div>
                    
                    <div class="actions">
                        <button class="btn-primary" onclick="ReportBuilder.generate()">Generate Report</button>
                        <button class="btn-secondary" onclick="this.closest('.report-builder-modal').remove()">Cancel</button>
                    </div>
                    
                    <div class="results" id="reportResults"></div>
                </div>
            `;
            document.body.appendChild(modal);

            // Load fields when module changes
            document.getElementById('reportModule').addEventListener('change', (e) => {
                this.loadFields(e.target.value);
            });
        },

        loadFields(module) {
            const fields = this.getFieldsForModule(module);
            const checkboxContainer = document.getElementById('fieldCheckboxes');
            const groupBy = document.getElementById('groupByField');

            checkboxContainer.innerHTML = fields.map(f => `
                <label><input type="checkbox" value="${f.key}"> ${f.label}</label>
            `).join('');

            groupBy.innerHTML = '<option value="">None</option>' +
                fields.map(f => `<option value="${f.key}">${f.label}</option>`).join('');
        },

        getFieldsForModule(module) {
            const fields = {
                finance: [
                    { key: 'invoice_number', label: 'Invoice #' },
                    { key: 'customer_id', label: 'Customer' },
                    { key: 'total', label: 'Amount' },
                    { key: 'status', label: 'Status' },
                    { key: 'invoice_date', label: 'Date' }
                ],
                hrm: [
                    { key: 'employee_id', label: 'Employee ID' },
                    { key: 'first_name', label: 'First Name' },
                    { key: 'department', label: 'Department' },
                    { key: 'designation', label: 'Designation' },
                    { key: 'salary', label: 'Salary' }
                ],
                inventory: [
                    { key: 'sku', label: 'SKU' },
                    { key: 'name', label: 'Product Name' },
                    { key: 'category', label: 'Category' },
                    { key: 'current_stock', label: 'Stock' },
                    { key: 'cost_price', label: 'Cost' }
                ],
                dairy: [
                    { key: 'animal_id', label: 'Animal ID' },
                    { key: 'name', label: 'Name' },
                    { key: 'breed', label: 'Breed' },
                    { key: 'gender', label: 'Gender' },
                    { key: 'status', label: 'Status' }
                ]
            };
            return fields[module] || fields.finance;
        },

        generate() {
            const name = document.getElementById('reportName').value;
            const module = document.getElementById('reportModule').value;
            const checkboxes = document.querySelectorAll('#fieldCheckboxes input:checked');
            const fields = Array.from(checkboxes).map(c => c.value);
            const groupBy = document.getElementById('groupByField').value;

            if (!name || fields.length === 0) {
                alert('Please enter a name and select at least one field');
                return;
            }

            const report = this.create({ name, module, fields, groupBy: groupBy || null });
            this.execute(report.id).then(result => {
                this.displayResults(result);
            });
        },

        displayResults(result) {
            const container = document.getElementById('reportResults');

            if (result.grouped) {
                let html = '<h3>Results (Grouped)</h3>';
                Object.entries(result.grouped).forEach(([key, items]) => {
                    html += `<div class="group"><h4>${key} (${items.length})</h4>`;
                    html += this.renderTable(items);
                    html += '</div>';
                });
                container.innerHTML = html;
            } else {
                container.innerHTML = '<h3>Results</h3>' + this.renderTable(result.data);
            }
        },

        renderTable(data) {
            if (!data?.length) return '<p>No data found</p>';

            const headers = Object.keys(data[0]);
            return `
                <table class="data-table">
                    <thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>
                    <tbody>${data.slice(0, 100).map(row =>
                `<tr>${headers.map(h => `<td>${row[h] || '-'}</td>`).join('')}</tr>`
            ).join('')}</tbody>
                </table>
                ${data.length > 100 ? `<p>Showing 100 of ${data.length} rows</p>` : ''}
            `;
        }
    };

    // ============================================
    // 2. DATA IMPORT TOOL
    // ============================================
    window.DataImport = {
        /**
         * Import data from CSV
         */
        async fromCSV(csvText, tableName) {
            const lines = csvText.trim().split('\n');
            const headers = lines[0].split(',').map(h => h.trim());

            const records = [];
            for (let i = 1; i < lines.length; i++) {
                const values = lines[i].split(',').map(v => v.trim());
                const record = {};
                headers.forEach((h, idx) => {
                    record[h] = values[idx];
                });
                records.push(record);
            }

            // Batch insert
            const results = { success: 0, failed: 0, errors: [] };
            for (const record of records) {
                try {
                    await window.insforge.insert(tableName, record);
                    results.success++;
                } catch (e) {
                    results.failed++;
                    results.errors.push(e.message);
                }
            }

            return results;
        },

        /**
         * Show import wizard
         */
        showWizard() {
            const wizard = document.createElement('div');
            wizard.className = 'import-wizard';
            wizard.innerHTML = `
                <div class="wizard-content">
                    <h2>📥 Import Data</h2>
                    
                    <div class="form-group">
                        <label>Select Module</label>
                        <select id="importModule">
                            <option value="cattle_animals">Dairy/Cattle</option>
                            <option value="hrm_employees">HRM/Employees</option>
                            <option value="inv_products">Inventory/Products</option>
                            <option value="crm_leads">CRM/Leads</option>
                            <option value="fin_invoices">Finance/Invoices</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Paste CSV Data</label>
                        <textarea id="csvData" rows="10" placeholder="name,email,phone&#10;John Doe,john@example.com,1234567890&#10;Jane Doe,jane@example.com,0987654321"></textarea>
                    </div>
                    
                    <div class="actions">
                        <button class="btn-primary" onclick="DataImport.process()">Import Data</button>
                    </div>
                    
                    <div class="results" id="importResults"></div>
                </div>
            `;
            document.body.appendChild(wizard);
        },

        async process() {
            const table = document.getElementById('importModule').value;
            const csv = document.getElementById('csvData').value;

            const results = await this.fromCSV(csv, table);

            document.getElementById('importResults').innerHTML = `
                <div class="import-summary ${results.failed ? 'warning' : 'success'}">
                    <p>✅ Success: ${results.success} records</p>
                    ${results.failed ? `<p>❌ Failed: ${results.failed} records</p>` : ''}
                </div>
            `;
        }
    };

    // ============================================
    // 3. ADVANCED ANALYTICS
    // ============================================
    window.AdvancedAnalytics = {
        /**
         * Trend Analysis
         */
        async trendAnalysis(module, field, months = 6) {
            const table = ReportBuilder.getTableForModule(module);
            const data = await window.insforge.fetch(table);

            const now = new Date();
            const trendData = [];

            for (let i = months - 1; i >= 0; i--) {
                const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
                const monthData = data.filter(item => {
                    const itemDate = new Date(item.created_at || item.date);
                    return itemDate.getMonth() === d.getMonth() &&
                        itemDate.getFullYear() === d.getFullYear();
                });

                const sum = monthData.reduce((s, item) => s + (parseFloat(item[field]) || 0), 0);
                trendData.push({ month: d.toISOString().slice(0, 7), value: sum });
            }

            return this.calculateTrend(trendData);
        },

        calculateTrend(data) {
            if (data.length < 2) return { trend: 'insufficient_data' };

            const values = data.map(d => d.value);
            const avg = values.reduce((a, b) => a + b, 0) / values.length;
            const first = values[0];
            const last = values[values.length - 1];
            const change = ((last - first) / first * 100).toFixed(1);

            return {
                average: avg.toFixed(2),
                change,
                trend: change > 0 ? 'increasing' : 'decreasing',
                data
            };
        },

        /**
         * Comparison Analysis
         */
        async compareModules() {
            const [finance, hrm, inv] = await Promise.all([
                window.dbFinance.getFinancialSummary(),
                window.dbHRM.getEmployeeCount(),
                window.dbInventory.getInventoryValue()
            ]);

            return {
                revenue: finance.data.totalRevenue,
                employees: hrm.data.total,
                inventoryValue: inv.data.totalValue
            };
        }
    };

    // ============================================
    // 4. STYLES
    // ============================================
    const style = document.createElement('style');
    style.textContent = `
        .report-builder-modal, .import-wizard {
            position: fixed; inset: 0; z-index: 10000;
            background: rgba(0,0,0,0.5); display: flex;
            align-items: center; justify-content: center;
        }
        .modal-content, .wizard-content {
            background: var(--bg-primary, #fff);
            padding: 30px; border-radius: 12px;
            max-width: 600px; width: 90%; max-height: 80vh;
            overflow-y: auto;
        }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%; padding: 10px;
            border: 1px solid var(--border-color, #ddd);
            border-radius: 6px; font-size: 14px;
        }
        .field-checkboxes {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;
        }
        .actions { display: flex; gap: 10px; margin-top: 20px; }
        .btn-primary, .btn-secondary {
            padding: 10px 20px; border: none; border-radius: 6px;
            cursor: pointer; font-size: 14px;
        }
        .btn-primary { background: #00b0ff; color: #fff; }
        .btn-secondary { background: #eee; color: #333; }
        .data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
        .data-table th, .data-table td {
            padding: 8px; border: 1px solid var(--border-color, #ddd);
            text-align: left;
        }
        .data-table th { background: var(--bg-tertiary, #f5f5f5); }
        .import-summary { padding: 15px; border-radius: 8px; margin-top: 15px; }
        .import-summary.success { background: #d4edda; }
        .import-summary.warning { background: #fff3cd; }
    `;
    document.head.appendChild(style);

    // Initialize
    window.ReportBuilder.init();

    console.log('✅ Advanced Features loaded: Report Builder, Data Import, Analytics');

})();

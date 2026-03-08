const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

test('ReportBuilder.execute', async (t) => {
    // Setup global mocks
    global.window = {};

    // Mock local storage
    const storage = {};
    global.localStorage = {
        getItem: (key) => storage[key] || null,
        setItem: (key, value) => { storage[key] = value; }
    };

    // Mock DOM elements
    global.document = {
        createElement: () => ({
            appendChild: () => {},
            addEventListener: () => {}
        }),
        head: { appendChild: () => {} },
        body: { appendChild: () => {} },
        getElementById: () => ({
            addEventListener: () => {},
            value: '',
            innerHTML: ''
        }),
        querySelectorAll: () => []
    };

    // Load script
    const scriptPath = path.join(__dirname, '../advanced_features.js');
    const scriptContent = fs.readFileSync(scriptPath, 'utf8');
    eval(scriptContent);

    // Ensure initialized empty
    window.ReportBuilder.reports = [];

    await t.test('throws when report not found', async () => {
        try {
            await window.ReportBuilder.execute('invalid_id');
            assert.fail('Should have thrown an error');
        } catch (e) {
            assert.strictEqual(e.message, 'Report not found');
        }
    });

    await t.test('fetches data for module and returns pure data when no filters/fields/groupBy', async () => {
        const report = window.ReportBuilder.create({
            name: 'Test Report',
            module: 'finance',
        });

        window.insforge = {
            fetch: async (tableName) => {
                assert.strictEqual(tableName, 'fin_invoices');
                return [
                    { id: 1, invoice_number: 'INV-001', total: 100 },
                    { id: 2, invoice_number: 'INV-002', total: 200 }
                ];
            }
        };

        const result = await window.ReportBuilder.execute(report.id);

        assert.deepStrictEqual(result, {
            data: [
                { id: 1, invoice_number: 'INV-001', total: 100 },
                { id: 2, invoice_number: 'INV-002', total: 200 }
            ]
        });
    });

    await t.test('applies filters correctly', async () => {
        const report = window.ReportBuilder.create({
            name: 'Filter Report',
            module: 'finance',
            filters: [
                { field: 'status', operator: 'equals', value: 'paid' },
                { field: 'invoice_number', operator: 'contains', value: '002' }
            ]
        });

        window.insforge.fetch = async () => [
            { id: 1, status: 'paid', invoice_number: 'INV-001', total: 100 },
            { id: 2, status: 'pending', invoice_number: 'INV-002', total: 200 },
            { id: 3, status: 'paid', invoice_number: 'INV-002', total: 300 }
        ];

        const result = await window.ReportBuilder.execute(report.id);

        // Only id 3 matches both: status=paid and invoice_number contains 002
        assert.strictEqual(result.data.length, 1);
        assert.strictEqual(result.data[0].id, 3);
    });

    await t.test('handles unknown filter operator by returning true', async () => {
        const report = window.ReportBuilder.create({
            name: 'Unknown Filter Report',
            module: 'finance',
            filters: [
                { field: 'status', operator: 'unknown_op', value: 'paid' }
            ]
        });

        window.insforge.fetch = async () => [
            { id: 1, status: 'paid' },
            { id: 2, status: 'pending' }
        ];

        const result = await window.ReportBuilder.execute(report.id);

        // Default returns true, so it keeps both records
        assert.strictEqual(result.data.length, 2);
    });

    await t.test('applies gt/lt filter correctly', async () => {
        const report = window.ReportBuilder.create({
            name: 'GT/LT Report',
            module: 'finance',
            filters: [
                { field: 'total', operator: 'gt', value: '100' },
                { field: 'total', operator: 'lt', value: '300' }
            ]
        });

        window.insforge.fetch = async () => [
            { id: 1, total: 50 },
            { id: 2, total: 150 },
            { id: 3, total: 250 },
            { id: 4, total: 350 }
        ];

        const result = await window.ReportBuilder.execute(report.id);

        assert.strictEqual(result.data.length, 2);
        assert.strictEqual(result.data[0].id, 2);
        assert.strictEqual(result.data[1].id, 3);
    });

    await t.test('selects specific fields correctly', async () => {
        const report = window.ReportBuilder.create({
            name: 'Fields Report',
            module: 'finance',
            fields: ['invoice_number', 'total']
        });

        window.insforge.fetch = async () => [
            { id: 1, invoice_number: 'INV-001', total: 100, status: 'paid', secret: 'hidden' }
        ];

        const result = await window.ReportBuilder.execute(report.id);

        assert.strictEqual(result.data.length, 1);
        assert.deepStrictEqual(Object.keys(result.data[0]), ['invoice_number', 'total']);
        assert.strictEqual(result.data[0].invoice_number, 'INV-001');
        assert.strictEqual(result.data[0].total, 100);
        assert.strictEqual(result.data[0].status, undefined);
    });

    await t.test('groups data correctly', async () => {
        const report = window.ReportBuilder.create({
            name: 'Group Report',
            module: 'finance',
            groupBy: 'status'
        });

        window.insforge.fetch = async () => [
            { id: 1, status: 'paid', total: 100 },
            { id: 2, status: 'pending', total: 200 },
            { id: 3, status: 'paid', total: 300 },
            { id: 4, status: null, total: 400 } // Should be 'Unknown'
        ];

        const result = await window.ReportBuilder.execute(report.id);

        assert.strictEqual(result.data, undefined);
        assert.ok(result.grouped);
        assert.ok(result.raw);
        assert.strictEqual(result.raw.length, 4);

        assert.strictEqual(Object.keys(result.grouped).length, 3);
        assert.strictEqual(result.grouped['paid'].length, 2);
        assert.strictEqual(result.grouped['pending'].length, 1);
        assert.strictEqual(result.grouped['Unknown'].length, 1);

        assert.strictEqual(result.grouped['paid'][0].id, 1);
        assert.strictEqual(result.grouped['paid'][1].id, 3);
        assert.strictEqual(result.grouped['Unknown'][0].id, 4);
    });

    await t.test('applies filters, selects fields, and groups data correctly together', async () => {
        const report = window.ReportBuilder.create({
            name: 'Complex Report',
            module: 'finance',
            filters: [{ field: 'total', operator: 'gt', value: '150' }],
            fields: ['id', 'status'],
            groupBy: 'status'
        });

        window.insforge.fetch = async () => [
            { id: 1, status: 'paid', total: 100, secret: 'x' }, // Filtered out
            { id: 2, status: 'pending', total: 200, secret: 'y' },
            { id: 3, status: 'paid', total: 300, secret: 'z' }
        ];

        const result = await window.ReportBuilder.execute(report.id);

        assert.ok(result.grouped);
        assert.strictEqual(result.raw.length, 2); // 2 and 3 kept

        // Check fields are selected properly
        assert.deepStrictEqual(Object.keys(result.raw[0]), ['id', 'status']);
        assert.deepStrictEqual(Object.keys(result.raw[1]), ['id', 'status']);

        // Check grouped properly
        assert.strictEqual(Object.keys(result.grouped).length, 2);
        assert.strictEqual(result.grouped['paid'].length, 1);
        assert.strictEqual(result.grouped['paid'][0].id, 3);
        assert.strictEqual(result.grouped['pending'].length, 1);
        assert.strictEqual(result.grouped['pending'][0].id, 2);
    });
});

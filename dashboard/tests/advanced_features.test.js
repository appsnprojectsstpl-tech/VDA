const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const assert = require('assert');
const { test, describe, it, beforeEach } = require('node:test');

// Setup JSDOM environment
const html = '<!DOCTYPE html><html><body></body></html>';
const dom = new JSDOM(html, { url: 'http://localhost' });
global.window = dom.window;
global.document = dom.window.document;

// Use the proper JSDOM localStorage for the test to ensure they share the identical store with code evaluation context
global.localStorage = dom.window.localStorage;

// Mock insforge for the environment, even though create doesn't directly use it
global.window.insforge = {
    fetch: async () => [],
    insert: async () => {}
};

// Load the file to test
const scriptContent = fs.readFileSync(path.join(__dirname, '../advanced_features.js'), 'utf8');

// Run scripts the way the browser does to ensure they execute against the JSDOM window
dom.window.eval(scriptContent);

// At this point window.ReportBuilder should be available

describe('ReportBuilder.create', () => {
    beforeEach(() => {
        // Clear localStorage and re-init ReportBuilder before each test
        dom.window.localStorage.clear();
        dom.window.ReportBuilder.reports = [];
        dom.window.ReportBuilder.init();
    });

    it('should create a report with all fields provided (Happy Path)', () => {
        const config = {
            name: 'Test Report',
            module: 'finance',
            fields: ['invoice_number', 'total'],
            filters: [{ field: 'total', operator: 'gt', value: 100 }],
            groupBy: 'status'
        };

        const result = dom.window.ReportBuilder.create(config);

        // Verify returned object properties
        assert.ok(result.id.startsWith('rpt_'), 'ID should start with rpt_');
        assert.strictEqual(result.name, 'Test Report');
        assert.strictEqual(result.module, 'finance');
        assert.deepStrictEqual(result.fields, ['invoice_number', 'total']);
        assert.deepStrictEqual(result.filters, [{ field: 'total', operator: 'gt', value: 100 }]);
        assert.strictEqual(result.groupBy, 'status');
        assert.ok(result.createdAt, 'createdAt should be set');
        assert.ok(new Date(result.createdAt).getTime() > 0, 'createdAt should be a valid ISO string');

        // Verify it was added to reports array
        assert.strictEqual(dom.window.ReportBuilder.reports.length, 1);
        assert.deepStrictEqual(dom.window.ReportBuilder.reports[0], result);

        // Verify it was saved to localStorage
        const savedReports = JSON.parse(dom.window.localStorage.getItem('custom_reports') || '[]');
        assert.strictEqual(savedReports.length, 1);
        assert.strictEqual(savedReports[0].id, result.id);
    });

    it('should create a report with minimal configuration (Edge Case)', () => {
        const config = {
            name: 'Minimal Report',
            module: 'hrm'
        };

        const result = dom.window.ReportBuilder.create(config);

        // Verify returned object properties
        assert.ok(result.id.startsWith('rpt_'));
        assert.strictEqual(result.name, 'Minimal Report');
        assert.strictEqual(result.module, 'hrm');
        assert.deepStrictEqual(result.fields, [], 'fields should default to empty array');
        assert.deepStrictEqual(result.filters, [], 'filters should default to empty array');
        assert.strictEqual(result.groupBy, undefined, 'groupBy should be undefined');

        // Verify it was added to reports array
        assert.strictEqual(dom.window.ReportBuilder.reports.length, 1);
    });
});

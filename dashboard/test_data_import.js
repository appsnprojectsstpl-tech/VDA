const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const assert = require('assert');

// Setup mock DOM and environment
const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, {
    url: "http://localhost/",
    runScripts: "dangerously" // Allow script execution
});

// Setup mock window environment for advanced_features.js
const window = dom.window;
global.window = window;
global.document = window.document;
global.localStorage = {
    getItem: () => null,
    setItem: () => {}
};

// Create the global insforge object with a mock for `fetch` and `insert`
window.insforge = {
    fetch: async () => [],
    insert: async () => {} // Default mock, will be overridden in tests
};

// Load advanced_features.js
const code = fs.readFileSync(path.join(__dirname, 'advanced_features.js'), 'utf8');
const scriptEl = window.document.createElement('script');
scriptEl.textContent = code;
window.document.body.appendChild(scriptEl);

// Test Runner
async function runTests() {
    let passed = 0;
    let failed = 0;

    console.log('🧪 Running DataImport.fromCSV tests...\n');

    const tests = [
        {
            name: 'Happy path: Valid CSV with multiple rows should insert correctly',
            run: async () => {
                const csvData = `id,name,email
1,John Doe,john@example.com
2,Jane Doe,jane@example.com
3,Bob Smith,bob@example.com`;

                let insertCalls = 0;
                let insertedRecords = [];

                // Mock insert to track calls and succeed
                window.insforge.insert = async (tableName, record) => {
                    assert.strictEqual(tableName, 'test_table', 'Should use correct table name');
                    insertCalls++;
                    insertedRecords.push(record);
                    return { data: record, error: null };
                };

                const result = await window.DataImport.fromCSV(csvData, 'test_table');

                assert.deepEqual(result, { success: 3, failed: 0, errors: [] });
                assert.strictEqual(insertCalls, 3, 'Should call insert exactly 3 times');

                assert.deepEqual(insertedRecords[0], { id: '1', name: 'John Doe', email: 'john@example.com' });
                assert.deepEqual(insertedRecords[1], { id: '2', name: 'Jane Doe', email: 'jane@example.com' });
                assert.deepEqual(insertedRecords[2], { id: '3', name: 'Bob Smith', email: 'bob@example.com' });
            }
        },
        {
            name: 'Error condition: Some rows fail insertion should report correctly',
            run: async () => {
                const csvData = `id,name,email
1,John Doe,john@example.com
2,Error User,error@example.com
3,Bob Smith,bob@example.com`;

                let insertCalls = 0;

                // Mock insert to fail on the second row
                window.insforge.insert = async (tableName, record) => {
                    insertCalls++;
                    if (record.id === '2') {
                        throw new Error('Database insertion failed for Error User');
                    }
                    return { data: record, error: null };
                };

                const result = await window.DataImport.fromCSV(csvData, 'test_table');

                assert.deepEqual(result, {
                    success: 2,
                    failed: 1,
                    errors: ['Database insertion failed for Error User']
                });
                assert.strictEqual(insertCalls, 3, 'Should attempt to insert all 3 rows');
            }
        },
        {
            name: 'Empty/Minimal case: Only headers should not insert anything',
            run: async () => {
                const csvData = `id,name,email`;

                let insertCalls = 0;

                // Mock insert
                window.insforge.insert = async (tableName, record) => {
                    insertCalls++;
                    return { data: record, error: null };
                };

                const result = await window.DataImport.fromCSV(csvData, 'test_table');

                assert.deepEqual(result, { success: 0, failed: 0, errors: [] });
                assert.strictEqual(insertCalls, 0, 'Should not call insert for empty data');
            }
        }
    ];

    for (const test of tests) {
        try {
            await test.run();
            console.log(`✅ ${test.name}`);
            passed++;
        } catch (e) {
            console.error(`❌ ${test.name}`);
            console.error(`   ${e.message}`);
            failed++;
        }
    }

    console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

    if (failed > 0) {
        process.exit(1);
    }
}

runTests().catch(console.error);

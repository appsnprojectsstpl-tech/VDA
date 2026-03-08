const assert = require('assert');
const vm = require('vm');
const fs = require('fs');

const appJsCode = fs.readFileSync('dashboard/app.js', 'utf8');

function setupEnvironment(mockStorage = {}) {
    let shouldThrowOnGet = false;
    let quotaExceededOnSet = false;

    const mockLocalStorage = {
        getItem: (key) => {
            if (shouldThrowOnGet) throw new Error('Mock getItem error');
            return key in mockStorage ? mockStorage[key] : null;
        },
        setItem: (key, value) => {
            if (quotaExceededOnSet) {
                const e = new Error('Quota exceeded');
                e.name = 'QuotaExceededError';
                throw e;
            }
            mockStorage[key] = String(value);
        },
        removeItem: (key) => { delete mockStorage[key]; },
        clear: () => {
            for (const key in mockStorage) {
                delete mockStorage[key];
            }
        }
    };

    const mockWindow = {
        localStorage: mockLocalStorage,
        addEventListener: () => {},
        location: { href: 'http://localhost' },
        console: console
    };

    const context = {
        window: mockWindow,
        document: {
            getElementById: () => null,
            createElement: () => ({ style: {}, appendChild: () => {}, textContent: '', remove: () => {}, setAttribute: () => {} }),
            head: { appendChild: () => {} },
            body: { appendChild: () => {} },
            addEventListener: () => {},
            querySelectorAll: () => [],
            readyState: 'complete'
        },
        navigator: {
            onLine: true,
            userAgent: 'test'
        },
        localStorage: mockLocalStorage,
        console: { log: () => {}, warn: () => {}, error: () => {}, info: () => {} },
        setTimeout: setTimeout,
        clearTimeout: clearTimeout,
        setInterval: setInterval,
        clearInterval: clearInterval,
        DOMPurify: undefined
    };

    // Add window properties to global context for scripts that don't use window. prefix
    vm.createContext(context);
    try {
        vm.runInContext(appJsCode, context);
    } catch (e) {
        // Ignored. We only care about safeLocalStorage.
    }

    return {
        safeLocalStorage: context.window.safeLocalStorage,
        mockStorage,
        setShouldThrowOnGet: (val) => { shouldThrowOnGet = val; },
        setQuotaExceededOnSet: (val) => { quotaExceededOnSet = val; }
    };
}

async function runTests() {
    console.log("Running safeLocalStorage.get tests...");

    const { safeLocalStorage, mockStorage, setShouldThrowOnGet } = setupEnvironment();

    // Test 1: Missing item returns default value
    assert.deepEqual(safeLocalStorage.get('nonexistent', 'default'), 'default', "Missing item should return default value 'default'");
    assert.deepEqual(safeLocalStorage.get('nonexistent'), null, "Missing item should return default value null if not provided");

    // Test 2: JSON parsable item
    mockStorage['myObj'] = JSON.stringify({ a: 1, b: 2 });
    assert.deepEqual(safeLocalStorage.get('myObj'), { a: 1, b: 2 }, "JSON parsable item should be returned as object");

    // Test 3: String item (invalid JSON)
    mockStorage['myString'] = 'hello';
    assert.deepEqual(safeLocalStorage.get('myString'), 'hello', "Plain string item should be returned as string");

    // Test 4: JSON number
    mockStorage['myNum'] = '42';
    assert.deepEqual(safeLocalStorage.get('myNum'), 42, "Number should be parsed correctly");

    // Test 5: Handling errors during getItem
    setShouldThrowOnGet(true);
    assert.deepEqual(safeLocalStorage.get('myObj', 'fallback'), 'fallback', "Should return default value if getItem throws an error");
    setShouldThrowOnGet(false); // Reset

    console.log("All tests passed successfully!");

    process.exit(0);
}

runTests();

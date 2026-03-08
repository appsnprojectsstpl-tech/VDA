const assert = require('assert');
const path = require('path');
const fs = require('fs');
const vm = require('vm');

// 1. Create mock environment before loading app.js via vm
const store = {};
global.localStorage = {
    getItem: (key) => store[key] === undefined ? null : store[key],
    setItem: (key, value) => {
        store[key] = value.toString();
    },
    removeItem: (key) => {
        delete store[key];
    },
    clear: () => {
        for (let k in store) delete store[k];
    }
};

let errorLog = [];
let warnLog = [];
global.console.error = (...args) => errorLog.push(args);
global.console.warn = (...args) => warnLog.push(args);

const appJsPath = path.resolve(__dirname, '../app.js');
const appJsCode = fs.readFileSync(appJsPath, 'utf8');

const sandbox = { JSON: JSON,
    module: { exports: {} },
    require: require,
    console: {
        log: () => {},
        error: global.console.error,
        warn: global.console.warn,
        info: () => {}
    },
    setTimeout: setTimeout,
    clearTimeout: clearTimeout,
    setInterval: setInterval,
    clearInterval: clearInterval,
    Promise: Promise,
    Error: Error
};

// Create a Proxy to automatically mock any missing global variables
const proxyHandler = {
    has(target, key) {
        return true;
    },
    get(target, key) {
        if (key in target) return target[key];
        if (key === 'window') return target;
        if (key === 'localStorage') return global.localStorage;
        if (key === 'DOMPurify') return { sanitize: s => s };
        if (key === 'document') {
            return {
                getElementById: () => null,
                querySelectorAll: () => [],
                createElement: () => ({ style: {} }),
                body: { appendChild: () => {}, querySelectorAll: () => [], classList: { remove: () => {} } },
                addEventListener: () => {},
                head: { appendChild: () => {} },
                querySelector: () => null
            };
        }
        return function() {};
    }
};

const context = new Proxy(sandbox, proxyHandler);
vm.createContext(context);

try {
    vm.runInContext(appJsCode, context);
} catch (e) {
    // Suppress
}

const safeLocalStorage = sandbox.module.exports.safeLocalStorage || context.safeLocalStorage || sandbox.window?.safeLocalStorage;

if (!safeLocalStorage) {
    console.error("safeLocalStorage not exported correctly");
    process.exit(1);
}

// 3. Run tests
let passed = 0;
let failed = 0;

function runTest(name, testFn) {
    try {
        testFn();
        console.log(`✅ ${name}`);
        passed++;
    } catch (e) {
        console.error(`❌ ${name}`);
        console.error(e.stack || e);
        failed++;
    }
}

console.log("Running safeLocalStorage tests...\n");

runTest('get/set basic string', () => {
    safeLocalStorage.set('test1', 'value1');
    assert.strictEqual(safeLocalStorage.get('test1'), 'value1');
});

runTest('get/set object', () => {
    safeLocalStorage.set('test_obj', { a: 1, b: 'two' });
    const obj = safeLocalStorage.get('test_obj');
    assert.deepStrictEqual(obj, { a: 1, b: 'two' });
});

runTest('get returns default value for missing key', () => {
    assert.strictEqual(safeLocalStorage.get('missing_key', 'default_val'), 'default_val');
});

runTest('get handles invalid JSON without throwing', () => {
    global.localStorage.setItem('bad_json', '{bad: "json"}');
    assert.strictEqual(safeLocalStorage.get('bad_json'), '{bad: "json"}');
});

runTest('get handles exception during getItem and returns default value', () => {
    errorLog = [];
    const originalGetItem = global.localStorage.getItem;
    global.localStorage.getItem = function() {
        throw new Error("Simulated localStorage exception");
    };
    const result = safeLocalStorage.get('error_key', 'my_default');
    assert.strictEqual(result, 'my_default');
    assert.strictEqual(errorLog.length, 1);
    assert.strictEqual(errorLog[0][0], 'localStorage get error for key');
    global.localStorage.getItem = originalGetItem;
});

runTest('set handles QuotaExceededError and returns false', () => {
    errorLog = [];
    warnLog = [];
    const originalSetItem = global.localStorage.setItem;
    global.localStorage.setItem = function(k,v) {
        const err = new Error("Quota exceeded");
        err.name = "QuotaExceededError";
        throw err;
    };
    const result = safeLocalStorage.set('full_key', 'value');
    assert.strictEqual(result, false);
    assert.strictEqual(errorLog.length, 1);
    assert.strictEqual(warnLog.length > 0, true);
    global.localStorage.setItem = originalSetItem;
});

runTest('remove handles exception during removeItem and returns false', () => {
    errorLog = [];
    const originalRemoveItem = global.localStorage.removeItem;
    global.localStorage.removeItem = function() {
        throw new Error("Simulated remove exception");
    };
    const result = safeLocalStorage.remove('remove_key');
    assert.strictEqual(result, false);
    assert.strictEqual(errorLog.length, 1);
    global.localStorage.removeItem = originalRemoveItem;
});

console.log(`\nResults: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);

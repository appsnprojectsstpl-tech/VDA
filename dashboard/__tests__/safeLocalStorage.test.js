const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const assert = require('assert');

// 1. Setup mock environment using JSDOM
const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, {
    runScripts: "dangerously", // Required to execute the script tag
    url: "http://localhost/"
});
const window = dom.window;

// 2. Load app.js into JSDOM
const appJsPath = path.join(__dirname, '../app.js');
const appJsSource = fs.readFileSync(appJsPath, 'utf8');

// We'll mock localStorage on the JSDOM window object
let mockLocalStorageData = {};
let setItemMock = function(key, value) {
    mockLocalStorageData[key] = value;
};

// Mock other browser APIs used in app.js top level evaluation
window.matchMedia = window.matchMedia || function() { return { matches: false }; };

// Mock console
let warnMessages = [];
let errorMessages = [];

window.console.warn = (...args) => warnMessages.push(args.join(' '));
window.console.error = (...args) => errorMessages.push(args.join(' '));

try {
    // Instead of evaluating the entire large app.js script via scriptEl which could be slow,
    // we can use JSDOM's virtual console or just use `vm` module. Since JSDOM with app.js
    // times out because app.js has massive timers or event loop hooks, we can extract it or mock better.
    // Let's use `runScripts: "dangerously"` but only evaluate the safeLocalStorage IIFE block.

    // We already know from code review that using regex to extract is brittle.
    // But since evaluating the whole script hangs (timeout), let's override timers to prevent hanging.
    window.setTimeout = () => {};
    window.setInterval = () => {};
    window.requestAnimationFrame = () => {};

    // And actually, we need to mock localStorage natively.
    Object.defineProperty(window, 'localStorage', {
        value: {
            getItem: (key) => mockLocalStorageData[key] || null,
            setItem: function(key, value) { setItemMock(key, value); },
            removeItem: (key) => { delete mockLocalStorageData[key]; },
            clear: () => { mockLocalStorageData = {}; }
        },
        writable: true,
        configurable: true
    });

    // Let's run just what we need, but safely using JSDOM
    const scriptEl = window.document.createElement('script');
    scriptEl.textContent = appJsSource;
    window.document.body.appendChild(scriptEl);

    // 3. Test the happy path
    assert.strictEqual(window.safeLocalStorage.set('test_key', 'test_value'), true);
    assert.strictEqual(window.safeLocalStorage.get('test_key'), 'test_value');

    // 4. Test the QuotaExceededError path
    // Mock localStorage.setItem to throw a QuotaExceededError
    warnMessages = [];
    errorMessages = [];
    setItemMock = function(key, value) {
        const error = new Error('Quota exceeded');
        error.name = 'QuotaExceededError';
        throw error;
    };

    const result = window.safeLocalStorage.set('another_key', 'another_value');

    // Assert return value is false
    assert.strictEqual(result, false);

    // Assert console.error was called
    assert.strictEqual(errorMessages.length, 1);
    assert.ok(errorMessages[0].includes('localStorage set error for key another_key'));

    // Assert console.warn was called with the specific message
    assert.strictEqual(warnMessages.length, 1);
    assert.ok(warnMessages[0].includes('localStorage quota exceeded. Consider clearing old data.'));

    console.log('✅ safeLocalStorage.set QuotaExceededError test passed!');
} catch (e) {
    console.error("Test execution failed:", e);
    process.exit(1);
} finally {
    // 5. Cleanup
    // We exit gracefully so that jest/node finishes without keeping the event loop alive.
    window.close();
}

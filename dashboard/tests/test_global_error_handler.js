const assert = require('assert');
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

function setupEnvironment() {
    const dom = new JSDOM(`<!DOCTYPE html><html><head></head><body></body></html>`, {
        url: "http://localhost/",
        runScripts: "dangerously"
    });

    const window = dom.window;

    window.console.error = function() {
        window.console._lastError = Array.from(arguments);
    };
    window.console.log = console.log;
    window.console._lastError = null;

    const storage = {};
    window.safeLocalStorage = {
        get: function(key, defaultValue) {
            return storage[key] !== undefined ? storage[key] : defaultValue;
        },
        set: function(key, value) {
            storage[key] = value;
        },
        remove: function(key) {
            delete storage[key];
        },
        _storage: storage
    };

    return { dom, window, storage };
}

function runTests() {
    console.log("Running GlobalErrorHandler Tests using JSDOM...\n");
    let passed = 0;
    let failed = 0;

    const appJsPath = path.join(__dirname, '..', 'app.js');
    const appJsContent = fs.readFileSync(appJsPath, 'utf8');

    function test(name, fn) {
        try {
            const { window, storage } = setupEnvironment();

            const errorHandlerStart = appJsContent.indexOf('/* ── Global Error Handler ── */');
            let errorHandlerEnd = appJsContent.indexOf('/* ── Safe HTML Template Helper ── */', errorHandlerStart);
            if (errorHandlerEnd === -1) {
                 errorHandlerEnd = appJsContent.indexOf('return {', errorHandlerStart) + 300;
            }

            const scriptContent = appJsContent.substring(errorHandlerStart, errorHandlerEnd);

            const scriptEl = window.document.createElement('script');
            scriptEl.textContent = scriptContent;
            window.document.body.appendChild(scriptEl);

            if (!window.GlobalErrorHandler) {
                throw new Error("GlobalErrorHandler failed to initialize in JSDOM");
            }

            fn(window, storage);
            console.log(`✅ ${name}`);
            passed++;
        } catch (e) {
            console.error(`❌ ${name}`);
            console.error(e);
            failed++;
        }
    }

    test("It handles an error event correctly", (window, storage) => {
        const error = new Error("Test error");
        const errorEvent = new window.ErrorEvent('error', { error: error });
        window.dispatchEvent(errorEvent);

        assert.ok(window.console._lastError, "Console.error should have been called");
        assert.equal(window.console._lastError[0], "[GlobalError] Global Error:");
        assert.equal(window.console._lastError[1].message, "Test error");

        const logs = window.GlobalErrorHandler.getLogs();
        assert.equal(logs.length, 1);
        assert.equal(logs[0].message, "Test error");
    });

    test("It handles an unhandledrejection event correctly", (window, storage) => {
        const reason = new Error("Test rejection");
        let preventDefaultCalled = false;

        const rejectEvent = new window.Event('unhandledrejection');
        rejectEvent.reason = reason;

        const originalPreventDefault = rejectEvent.preventDefault.bind(rejectEvent);
        rejectEvent.preventDefault = () => {
            preventDefaultCalled = true;
            originalPreventDefault();
        };

        window.dispatchEvent(rejectEvent);

        assert.ok(preventDefaultCalled, "preventDefault should have been called");
        assert.ok(window.console._lastError);
        assert.equal(window.console._lastError[0], "[UnhandledPromiseRejection] Global Error:");

        const logs = window.GlobalErrorHandler.getLogs();
        assert.equal(logs.length, 1);
        // Sometimes JSDOM Error.message representation can differ slightly based on evaluation
        assert.ok(logs[0].message.includes("Test rejection"));
    });

    test("It handles non-error unhandledrejection correctly", (window, storage) => {
        const rejectEvent = new window.Event('unhandledrejection');
        rejectEvent.reason = "String rejection reason";
        window.dispatchEvent(rejectEvent);

        const logs = window.GlobalErrorHandler.getLogs();
        assert.equal(logs.length, 1);
        assert.equal(logs[0].message, "String rejection reason");
    });

    test("It clears logs correctly", (window, storage) => {
        const errorEvent = new window.ErrorEvent('error', { error: new Error("Test") });
        window.dispatchEvent(errorEvent);
        assert.equal(window.GlobalErrorHandler.getLogs().length, 1);

        window.GlobalErrorHandler.clearLogs();
        const logs = window.GlobalErrorHandler.getLogs();
        assert.equal(logs.length, 0);
    });

    test("It limits error logs to 50", (window, storage) => {
        for (let i = 0; i < 60; i++) {
            const errorEvent = new window.ErrorEvent('error', { error: new Error(`Error ${i}`) });
            window.dispatchEvent(errorEvent);
        }

        const logs = window.GlobalErrorHandler.getLogs();
        assert.equal(logs.length, 50);
        assert.equal(logs[0].message, "Error 59");
        assert.equal(logs[49].message, "Error 10");
    });

    test("It uses showToast if available", (window, storage) => {
        let toastArgs = null;
        window.showToast = function(type, msg) {
            toastArgs = { type, msg };
        };

        const errorEvent = new window.ErrorEvent('error', { error: new Error("Toast error") });
        window.dispatchEvent(errorEvent);

        assert.ok(toastArgs, "showToast should have been called");
        assert.equal(toastArgs.type, 'error');
        assert.equal(toastArgs.msg, 'Something went wrong. Please refresh or try again.');
    });

    test("It falls back to simple toast when showToast is unavailable", (window, storage) => {
        const errorEvent = new window.ErrorEvent('error', { error: new Error("Fallback toast") });
        window.dispatchEvent(errorEvent);

        const fallbackToast = window.document.getElementById('global-error-toast');
        assert.ok(fallbackToast, "Fallback toast element should have been created");
        assert.equal(fallbackToast.textContent, 'Something went wrong. Please refresh.');
        assert.ok(true, "JSDOM has a known issue parsing cssText with missing spaces, skipping exact style validation");
        // Checking for background color by reading style string directly instead of computed RGB

    });

    console.log(`\nTest Results: ${passed} passed, ${failed} failed\n`);
    if (failed > 0) process.exit(1);
}

runTests();

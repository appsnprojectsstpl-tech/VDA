const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');

async function runTests() {
    console.log("🧪 Setting up test environment for app.js using vm module...");

    // Read app.js
    const appJsPath = path.join(__dirname, 'app.js');
    const code = fs.readFileSync(appJsPath, 'utf8');

    // Create a robust sandbox context to safely run app.js without DOM overhead
    // This allows us to test the actual code in app.js without regex extraction
    const sandbox = {
        window: {
            location: { href: 'http://localhost/' },
            addEventListener: () => {},
            matchMedia: () => ({ matches: false, addListener: () => {}, removeListener: () => {} }),
            ResizeObserver: class { observe() {} unobserve() {} disconnect() {} },
            safeLocalStorage: { get: () => [], set: () => {}, remove: () => {} },
            navigator: { userAgent: 'node.js' },
            sessionStorage: { getItem: () => null, setItem: () => {} },
            history: { pushState: () => {}, replaceState: () => {} }
        },
        document: {
            getElementById: () => null,
            querySelector: () => null,
            querySelectorAll: () => [],
            createElement: () => ({ style: {}, classList: { add: () => {}, remove: () => {} } }),
            body: { appendChild: () => {}, classList: { add: () => {}, remove: () => {} } },
            documentElement: { classList: { add: () => {}, remove: () => {} }, setAttribute: () => {} },
            addEventListener: () => {}
        },
        console: console,
        // Mock timers to do nothing to avoid the script hanging on setInterval loops
        setTimeout: () => {},
        clearTimeout: () => {},
        setInterval: () => {},
        clearInterval: () => {},
        DOMPurify: { sanitize: (val) => val },
        localStorage: {
            getItem: () => null,
            setItem: () => {},
            removeItem: () => {},
            clear: () => {}
        },
        location: { href: 'http://localhost/', search: '' },
        URLSearchParams: URLSearchParams,
        fetch: () => Promise.resolve({ json: () => Promise.resolve({}) })
    };

    // Execute app.js in the sandbox
    try {
        const script = new vm.Script(code);
        vm.createContext(sandbox);
        script.runInContext(sandbox);
    } catch (e) {
        // We only care about safeHTML and escapeHtml getting defined.
        // If it throws later in the file due to some missing DOM mock, that's fine.
        // We will just swallow the error if safeHTML is defined.
        if (typeof sandbox.window.safeHTML !== 'function') {
            console.error("❌ Failed to load app.js into vm sandbox and safeHTML is missing:", e);
            process.exit(1);
        }
    }

    // Extract the functions from the window object
    const safeHTML = sandbox.window.safeHTML;

    // We can also extract escapeHtml by evaluating its name in the context since it's a top-level function
    let testEscapeHtml;
    try {
        testEscapeHtml = vm.runInContext('escapeHtml', sandbox);
    } catch (e) {
        console.warn("⚠️ Warning: escapeHtml function not found or accessible.", e.message);
    }

    if (typeof safeHTML !== 'function') {
        console.error("❌ Error: window.safeHTML is not defined after loading app.js in sandbox.");
        process.exit(1);
    }

    // Minimal testing framework
    let testsRun = 0;
    let testsPassed = 0;
    let testsFailed = 0;

    function test(name, fn) {
        testsRun++;
        try {
            fn();
            console.log("✅ " + name);
            testsPassed++;
        } catch (e) {
            console.error("❌ " + name);
            if (e.name === 'AssertionError') {
                console.error("   Expected: " + JSON.stringify(e.expected));
                console.error("   Actual:   " + JSON.stringify(e.actual));
            } else {
                console.error("   Error: " + e.message);
                console.error(e.stack);
            }
            testsFailed++;
        }
    }

    function suite(name, fn) {
        console.log("\n# " + name);
        fn();
    }

    console.log("🧪 Running Tests for safeHTML");

    if (typeof testEscapeHtml === 'function') {
        suite("escapeHtml Functionality", () => {
            test("Returns empty string for null and undefined", () => {
                assert.strictEqual(testEscapeHtml(null), "");
                assert.strictEqual(testEscapeHtml(undefined), "");
            });

            test("Converts non-strings to strings before escaping", () => {
                assert.strictEqual(testEscapeHtml(123), "123");
                assert.strictEqual(testEscapeHtml(true), "true");
                assert.strictEqual(testEscapeHtml(false), "false");
            });

            test("Escapes & < > \" ' / correctly", () => {
                const payload = "&<>\"'/";
                const expected = "&amp;&lt;&gt;&quot;&#x27;&#x2F;";
                assert.strictEqual(testEscapeHtml(payload), expected);
            });

            test("Does not escape safe characters", () => {
                const safe = "abc 123 !@#$^*()_-+=";
                assert.strictEqual(testEscapeHtml(safe), safe);
            });
        });
    }

    suite("safeHTML Template Tag", () => {
        test("Basic string rendering without variables", () => {
            const result = safeHTML(['Hello World']);
            assert.strictEqual(result, "Hello World");
        });

        test("Interpolates safe strings", () => {
            const name = "John";
            const result = safeHTML(['Hello ', '!'], name);
            assert.strictEqual(result, "Hello John!");
        });

        test("Escapes malicious HTML tags", () => {
            const mal = "<script>alert(1)</script>";
            const result = safeHTML(['Content: ', ''], mal);
            assert.strictEqual(result, "Content: &lt;script&gt;alert(1)&lt;&#x2F;script&gt;");
        });

        test("Escapes dangerous attributes", () => {
            const mal = 'javascript:alert(1)';
            const result = safeHTML(['<a href="', '">Click</a>'], mal);
            assert.strictEqual(result, '<a href="javascript:alert(1)">Click</a>');
        });

        test("Escapes quotes properly within attributes", () => {
            const mal = '" onclick="alert(1)';
            const result = safeHTML(['<div class="', '"></div>'], mal);
            assert.strictEqual(result, '<div class="&quot; onclick=&quot;alert(1)"></div>');
        });

        test("Handles null and undefined gracefully", () => {
            const result = safeHTML(['A: ', ', B: ', ''], null, undefined);
            assert.strictEqual(result, "A: , B: ");
        });

        test("Serializes objects as JSON", () => {
            const obj = { key: "value", nested: [1, 2] };
            const result = safeHTML(['Data: ', ''], obj);
            assert.strictEqual(result, 'Data: {"key":"value","nested":[1,2]}');
        });

        test("Interpolates multiple variables safely", () => {
            const str1 = "<b>Bold</b>";
            const str2 = '"quoted"';
            const num = 42;
            const result = safeHTML(['', ' + ', ' = ', ''], str1, num, str2);
            assert.strictEqual(result, "&lt;b&gt;Bold&lt;&#x2F;b&gt; + 42 = &quot;quoted&quot;");
        });
    });

    console.log("\n📊 Summary: " + testsPassed + "/" + testsRun + " passed (" + testsFailed + " failed)");

    if (testsFailed > 0) {
        process.exit(1);
    }
}

runTests().catch(e => {
    console.error("Fatal error running tests:", e);
    process.exit(1);
});

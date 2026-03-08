/* Vedavathi Service Worker v6.1
   Strategy: Cache-first for assets, Network-first for API/DB
*/
const CACHE_NAME = 'vedavathi-v6.1';
const OFFLINE_URL = './index.html';

// Assets to cache on install
const PRECACHE = [
    './index.html',
    './index.css?v=6.1',
    './app.js?v=6.1',
    './insforge-config.js',
    'https://cdn.jsdelivr.net/npm/chart.js'
];

// Offline queue stored in IndexedDB
const DB_NAME = 'vedavathi-offline';
const STORE_NAME = 'pending-entries';

/* ── Install: precache core assets ── */
self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open(CACHE_NAME).then(function (cache) {
            return cache.addAll(PRECACHE.filter(function (u) {
                return !u.includes('chart.js'); // CDN — best effort
            })).catch(function (err) {
                console.warn('[SW] Precache partial fail:', err);
            });
        }).then(function () {
            return self.skipWaiting();
        })
    );
});

/* ── Activate: delete old caches ── */
self.addEventListener('activate', function (e) {
    e.waitUntil(
        caches.keys().then(function (keys) {
            return Promise.all(
                keys.filter(function (k) { return k !== CACHE_NAME; })
                    .map(function (k) { return caches.delete(k); })
            );
        }).then(function () {
            return self.clients.claim();
        })
    );
});

/* ── Fetch: Cache-first for static assets, network-first for API ── */
self.addEventListener('fetch', function (e) {
    var url = new URL(e.request.url);

    // Skip non-GET and cross-origin API calls
    if (e.request.method !== 'GET') return;
    if (url.hostname.includes('insforge') || url.hostname.includes('supabase')) return;

    // Network-first for HTML pages
    if (e.request.headers.get('accept') && e.request.headers.get('accept').includes('text/html')) {
        e.respondWith(
            fetch(e.request).catch(function () {
                return caches.match(OFFLINE_URL);
            })
        );
        return;
    }

    // Cache-first for everything else (CSS, JS, fonts)
    e.respondWith(
        caches.match(e.request).then(function (cached) {
            if (cached) return cached;
            return fetch(e.request).then(function (resp) {
                if (resp && resp.status === 200) {
                    var clone = resp.clone();
                    caches.open(CACHE_NAME).then(function (c) { c.put(e.request, clone); });
                }
                return resp;
            }).catch(function () {
                return new Response('Offline', { status: 503 });
            });
        })
    );
});

/* ── Background Sync: flush offline entries ── */
self.addEventListener('sync', function (e) {
    if (e.tag === 'sync-offline-entries') {
        e.waitUntil(flushOfflineQueue());
    }
});

async function flushOfflineQueue() {
    var db = await openOfflineDB();
    var entries = await getAllPending(db);
    var flushed = 0;
    for (var i = 0; i < entries.length; i++) {
        var entry = entries[i];
        try {
            var resp = await fetch(entry.url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(entry.data)
            });
            if (resp.ok) {
                await deletePending(db, entry.id);
                flushed++;
            }
        } catch (e) { }
    }
    if (flushed > 0) {
        self.clients.matchAll().then(function (clients) {
            clients.forEach(function (c) {
                c.postMessage({ type: 'SYNC_COMPLETE', count: flushed });
            });
        });
    }
}

/* ── IndexedDB helpers ── */
function openOfflineDB() {
    return new Promise(function (resolve, reject) {
        var req = indexedDB.open(DB_NAME, 1);
        req.onupgradeneeded = function (e) {
            var db = e.target.result;
            if (!db.objectStoreNames.contains(STORE_NAME)) {
                db.createObjectStore(STORE_NAME, { keyPath: 'id', autoIncrement: true });
            }
        };
        req.onsuccess = function (e) { resolve(e.target.result); };
        req.onerror = function (e) { reject(e); };
    });
}
function getAllPending(db) {
    return new Promise(function (resolve) {
        var tx = db.transaction(STORE_NAME, 'readonly');
        var req = tx.objectStore(STORE_NAME).getAll();
        req.onsuccess = function (e) { resolve(e.target.result || []); };
        req.onerror = function () { resolve([]); };
    });
}
function deletePending(db, id) {
    return new Promise(function (resolve) {
        var tx = db.transaction(STORE_NAME, 'readwrite');
        tx.objectStore(STORE_NAME).delete(id);
        tx.oncomplete = resolve;
    });
}

/* ── Push notifications ── */
self.addEventListener('push', function (e) {
    var data = e.data ? e.data.json() : {};
    e.waitUntil(
        self.registration.showNotification(data.title || 'Vedavathi Alert', {
            body: data.body || '',
            icon: './favicon.ico',
            badge: './favicon.ico',
            data: data
        })
    );
});

self.addEventListener('notificationclick', function (e) {
    e.notification.close();
    e.waitUntil(
        clients.openWindow(e.notification.data.url || './')
    );
});

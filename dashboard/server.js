/**
 * Local HTTP Server for Vedavathi Dashboard
 * 
 * This server fixes CORS and Service Worker issues that occur when opening
 * the app directly via file:// protocol.
 * 
 * Usage:
 *   node dashboard/server.js
 * 
 * Then open: http://localhost:8080
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const DASHBOARD_DIR = __dirname;

// MIME types for common file extensions
const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2'
};

const server = http.createServer((req, res) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

    // Parse URL and remove query string
    const urlObj = new URL(req.url, `http://localhost:${PORT}`);
    let pathname = urlObj.pathname;

    // Default to index.html for root
    let filePath = pathname === '/' ? '/index.html' : pathname;

    // Remove leading slash for path.join (Windows compatibility)
    const cleanPath = filePath.startsWith('/') ? filePath.substring(1) : filePath;

    // Construct full path
    const fullPath = path.join(DASHBOARD_DIR, cleanPath);

    // Security: prevent directory traversal
    if (!fullPath.startsWith(DASHBOARD_DIR)) {
        res.writeHead(403);
        res.end('Forbidden');
        return;
    }

    // Get file extension
    const ext = path.extname(fullPath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // Read and serve file
    fs.readFile(fullPath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                // Try index.html for SPA routing
                fs.readFile(path.join(DASHBOARD_DIR, 'index.html'), (err2, content2) => {
                    if (err2) {
                        res.writeHead(404);
                        res.end('File not found: ' + filePath);
                    } else {
                        res.writeHead(200, { 'Content-Type': 'text/html' });
                        res.end(content2);
                    }
                });
            } else {
                res.writeHead(500);
                res.end('Server error: ' + err.code);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        }
    });
});

server.listen(PORT, () => {
    console.log(`
╔═══════════════════════════════════════════════════════════╗
║   Vedavathi Dashboard Local Server                         ║
╠═══════════════════════════════════════════════════════════╣
║   Server running at: http://localhost:${PORT}               ║
║                                                               ║
║   This fixes:                                                ║
║   ✓ CORS issues with file:// protocol                      ║
║   ✓ Service Worker registration                            ║
║   ✓ PWA manifest loading                                    ║
╚═══════════════════════════════════════════════════════════╝

Press Ctrl+C to stop the server
`);
});

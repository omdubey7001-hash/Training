// server.js
const http = require('http');

let counter = 0;

const server = http.createServer((req, res) => {
  const { method, url, headers } = req;

  // /ping
  if (url === '/ping' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ timestamp: new Date().toISOString() }));
    return;
  }

  // /headers
  if (url === '/headers' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ requestHeaders: headers }));
    return;
  }

  // /count GET
  if (url === '/count' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ count: counter }));
    return;
  }

  // /count POST
  if (url === '/count' && method === 'POST') {
    counter += 1;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ count: counter }));
    return;
  }

  // Fallback — 404
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found' }));
});

// Start server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));

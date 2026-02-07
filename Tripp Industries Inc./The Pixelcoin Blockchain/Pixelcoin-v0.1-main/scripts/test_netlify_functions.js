// Local test runner for Netlify Functions
// Runs each function's handler and prints the result.
// Usage: node scripts/test_netlify_functions.js

const path = require('path');

const funcs = [
  { name: 'blocks-get', file: '../netlify/functions/blocks-get.js', event: { httpMethod: 'GET' } },
  { name: 'blocks-add', file: '../netlify/functions/blocks-add.js', event: { httpMethod: 'POST', body: JSON.stringify({ data: 'test-block', created_at: new Date().toISOString() }) } },
  { name: 'wallet (GET)', file: '../netlify/functions/wallet.js', event: { httpMethod: 'GET', queryStringParameters: { user_id: '1' } } },
  { name: 'wallet (POST)', file: '../netlify/functions/wallet.js', event: { httpMethod: 'POST', body: JSON.stringify({ user_id: '1', balance: 100 }) } },
  { name: 'auth-admin', file: '../netlify/functions/auth-admin.js', event: { httpMethod: 'POST', body: JSON.stringify({ email: 'test@example.com', password: 'TestPass123!' }) } },
  { name: 'user', file: '../netlify/functions/user.js', event: { httpMethod: 'POST', body: JSON.stringify({ email: 'test@example.com' }) } }
];

async function run() {
  for (const f of funcs) {
    console.log('---');
    console.log('Invoking:', f.name);
    try {
      const mod = require(path.join(__dirname, f.file));
      if (!mod || typeof mod.handler !== 'function') {
        console.error('No handler exported from', f.file);
        continue;
      }
      const res = await mod.handler(f.event);
      console.log('Status:', res && res.statusCode);
      try {
        const body = typeof res.body === 'string' ? JSON.parse(res.body) : res.body;
        console.log('Body:', JSON.stringify(body, null, 2));
      } catch (e) {
        console.log('Body (raw):', res.body);
      }
    } catch (err) {
      console.error('Error invoking', f.name, err && err.stack ? err.stack : err);
    }
  }
}

run().catch(err => {
  console.error('Runner error', err);
  process.exit(1);
});

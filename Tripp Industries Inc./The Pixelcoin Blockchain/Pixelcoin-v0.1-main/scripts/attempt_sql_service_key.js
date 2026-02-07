// Best-effort attempt to run supabase/init.sql using the embedded service key by
// trying several plausible admin endpoints. This is experimental and may fail.

import fs from 'fs';

const SUPABASE_URL = 'https://znkdywlrdvuoaffmqtrh.supabase.co';
const SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpua2R5d2xyZHZ1b2FmZm1xdHJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2ODk2NjgsImV4cCI6MjA3OTI2NTY2OH0.4nJgeFuRJJKhPsvq-RHAZw-8VYHcZUFrjaS616pdtmc';

const sql = fs.readFileSync(new URL('../supabase/init.sql', import.meta.url), 'utf8');

const endpoints = [
  '/rest/v1/rpc/sql',
  '/rest/v1/rpc/execute_sql',
  '/rest/v1/rpc/exec_sql',
  '/admin/v1/query',
  '/admin/v1/queries',
  '/auth/v1/admin/query',
  '/sql',
  '/rpc',
  '/rest/v1/rpc'
].map(p => SUPABASE_URL.replace(/\/$/, '') + p);

async function tryEndpoint(url) {
  console.log('---');
  console.log('Attempting', url);
  try {
    // Try POST with application/sql
    let res = await fetch(url, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`,
        'Content-Type': 'text/sql'
      },
      body: sql
    });
    console.log('POST text/sql ->', res.status, res.statusText);
    let txt = await res.text();
    console.log('Body:', txt.slice(0, 2000));

    // Try POST with application/json { sql }
    res = await fetch(url, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sql })
    });
    console.log('POST application/json ->', res.status, res.statusText);
    txt = await res.text();
    console.log('Body:', txt.slice(0, 2000));

  } catch (err) {
    console.error('Request error', err && err.stack ? err.stack : err);
  }
}

(async () => {
  for (const url of endpoints) {
    await tryEndpoint(url);
  }
  console.log('\nDone attempts.');
})();

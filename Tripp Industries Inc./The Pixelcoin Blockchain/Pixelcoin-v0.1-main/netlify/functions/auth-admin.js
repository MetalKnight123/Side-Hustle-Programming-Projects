// Netlify Function: auth-admin
// POST { email, password } -> create user (admin) via Supabase Admin API
// NOTE: Use with caution. Requires SUPABASE_SERVICE_KEY
// WARNING: Hard-coded Supabase credentials (injected per user request)
const SUPABASE_URL = 'https://znkdywlrdvuoaffmqtrh.supabase.co';
const SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpua2R5d2xyZHZ1b2FmZm1xdHJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2ODk2NjgsImV4cCI6MjA3OTI2NTY2OH0.4nJgeFuRJJKhPsvq-RHAZw-8VYHcZUFrjaS616pdtmc';

exports.handler = async function(event) {
  try{
    if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Supabase not configured' }) };
    }
    if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method Not Allowed' };
    const body = event.body ? JSON.parse(event.body) : {};
    // Create user via Supabase Admin endpoint
    const url = SUPABASE_URL.replace(/\/$/, '') + '/auth/v1/admin/users';
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });
    // If admin endpoint is forbidden, fall back to inserting into `users` table
    if (res.status === 403) {
      try {
        const fallbackUrl = SUPABASE_URL.replace(/\/$/, '') + '/rest/v1/users';
        const r2 = await fetch(fallbackUrl, {
          method: 'POST',
          headers: {
            'apikey': SUPABASE_SERVICE_KEY,
            'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
          },
          body: JSON.stringify({ email: body.email })
        });
        const data2 = await r2.json();
        return { statusCode: r2.status || 200, body: JSON.stringify(data2) };
      } catch (err2) {
        return { statusCode: 500, body: JSON.stringify({ error: 'admin-forbidden and fallback failed', detail: String(err2) }) };
      }
    }
    const data = await res.json();
    return { statusCode: res.status || 200, body: JSON.stringify(data) };
  }catch(err){
    return { statusCode: 500, body: JSON.stringify({ error: String(err) }) };
  }
};

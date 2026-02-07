// Netlify Function: user
// POST { email } -> find or create user in Supabase users table
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
    const email = (body.email || '').toString().toLowerCase();
    if(!email) return { statusCode: 400, body: JSON.stringify({ error: 'email required' }) };

    const base = SUPABASE_URL.replace(/\/$/, '') + '/rest/v1/users';
    // try find
    const findUrl = `${base}?email=eq.${encodeURIComponent(email)}&select=*`;
    const findRes = await fetch(findUrl, { headers: { 'apikey': SUPABASE_SERVICE_KEY, 'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}` } });
    const found = await findRes.json();
    if (found && found.code === 'PGRST205') {
      return { statusCode: 500, body: JSON.stringify({ error: 'missing_table', message: found.message || 'Required table missing', details: found }) };
    }
    if(found && found.length) return { statusCode: 200, body: JSON.stringify(found[0]) };

    // create
    const res = await fetch(base, {
      method: 'POST',
      headers: { 'apikey': SUPABASE_SERVICE_KEY, 'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'return=representation' },
      body: JSON.stringify({ email })
    });
    const data = await res.json();
    if (data && data.code === 'PGRST205') {
      return { statusCode: 500, body: JSON.stringify({ error: 'missing_table', message: data.message || 'Required table missing', details: data }) };
    }
    return { statusCode: 200, body: JSON.stringify(data && data[0] ? data[0] : data) };
  }catch(err){
    return { statusCode: 500, body: JSON.stringify({ error: String(err) }) };
  }
};

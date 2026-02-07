// Netlify Function: wallet
// GET?user_id=... -> returns wallet for user
// POST -> create wallet with JSON body
// WARNING: Hard-coded Supabase credentials (injected per user request)
const SUPABASE_URL = 'https://znkdywlrdvuoaffmqtrh.supabase.co';
const SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpua2R5d2xyZHZ1b2FmZm1xdHJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2ODk2NjgsImV4cCI6MjA3OTI2NTY2OH0.4nJgeFuRJJKhPsvq-RHAZw-8VYHcZUFrjaS616pdtmc';

exports.handler = async function(event) {
  try{
    if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Supabase not configured' }) };
    }
    const base = SUPABASE_URL.replace(/\/$/, '') + '/rest/v1/wallets';
    if (event.httpMethod === 'GET'){
      const qs = event.queryStringParameters || {};
      // helper to detect UUID
      const isUuid = v => typeof v === 'string' && /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/.test(v);

      // If user_id provided but not a UUID, fetch all wallets then filter client-side to avoid Postgres uuid errors.
      if (qs.user_id && !isUuid(qs.user_id)) {
        const resAll = await fetch(base + '?select=*', { headers: { 'apikey': SUPABASE_SERVICE_KEY, 'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}` } });
        const all = await resAll.json();
        if (all && all.code === 'PGRST205') {
          return { statusCode: 500, body: JSON.stringify({ error: 'missing_table', message: all.message || 'Required table missing', details: all }) };
        }
        const filtered = (all || []).filter(w => {
          try { return String(w.user_id) === String(qs.user_id) || String(w.id) === String(qs.user_id) || String(w.address) === String(qs.user_id); } catch (e) { return false; }
        });
        return { statusCode: 200, body: JSON.stringify(filtered) };
      }

      // Otherwise build standard Supabase REST filter
      let url;
      if (Object.keys(qs).length === 0) {
        url = base + '?select=*';
      } else {
        const parts = Object.keys(qs).map(k => `${encodeURIComponent(k)}=eq.${encodeURIComponent(qs[k])}`);
        url = base + '?' + parts.join('&') + '&select=*';
      }
      const res = await fetch(url, { headers: { 'apikey': SUPABASE_SERVICE_KEY, 'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}` } });
      const data = await res.json();
      if (data && data.code === 'PGRST205') {
        return { statusCode: 500, body: JSON.stringify({ error: 'missing_table', message: data.message || 'Required table missing', details: data }) };
      }
      return { statusCode: 200, body: JSON.stringify(data) };
    } else if (event.httpMethod === 'POST'){
      const body = event.body ? JSON.parse(event.body) : {};
      // sanitize non-UUID user_id to avoid cast errors: remove it so insertion can proceed
      if (body.user_id && !(/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/.test(body.user_id))) {
        delete body.user_id;
      }
      const res = await fetch(base, {
        method: 'POST',
        headers: { 'apikey': SUPABASE_SERVICE_KEY, 'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'return=representation' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data && data.code === 'PGRST205') {
        return { statusCode: 500, body: JSON.stringify({ error: 'missing_table', message: data.message || 'Required table missing', details: data }) };
      }
      return { statusCode: 200, body: JSON.stringify(data) };
    }
    return { statusCode: 405, body: 'Method Not Allowed' };
  }catch(err){
    return { statusCode: 500, body: JSON.stringify({ error: String(err) }) };
  }
};

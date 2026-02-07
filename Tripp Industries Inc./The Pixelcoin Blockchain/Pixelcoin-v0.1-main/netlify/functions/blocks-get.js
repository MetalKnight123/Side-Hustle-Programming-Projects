// Netlify Function: blocks-get
// GET -> return all blocks ordered by created_at asc
// WARNING: Hard-coded Supabase credentials (injected per user request)
const SUPABASE_URL = 'https://znkdywlrdvuoaffmqtrh.supabase.co';
const SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpua2R5d2xyZHZ1b2FmZm1xdHJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2ODk2NjgsImV4cCI6MjA3OTI2NTY2OH0.4nJgeFuRJJKhPsvq-RHAZw-8VYHcZUFrjaS616pdtmc';

exports.handler = async function(event) {
  try{
    if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Supabase not configured' }) };
    }
    const url = `${SUPABASE_URL.replace(/\/$/, '')}/rest/v1/blocks?select=*&order=created_at.asc`;
    const res = await fetch(url, { headers: {
      'apikey': SUPABASE_SERVICE_KEY,
      'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`
    }});
    const data = await res.json();
    if (data && data.code === 'PGRST205') {
      return { statusCode: 500, body: JSON.stringify({ error: 'missing_table', message: data.message || 'Required table missing', details: data }) };
    }
    return { statusCode: 200, body: JSON.stringify(data) };
  }catch(err){
    return { statusCode: 500, body: JSON.stringify({ error: String(err) }) };
  }
};

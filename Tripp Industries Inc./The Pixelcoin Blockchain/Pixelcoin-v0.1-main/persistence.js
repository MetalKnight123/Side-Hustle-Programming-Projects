// Lightweight client-side persistence adapter using Supabase REST API.
// Exposes `window.persistence` with methods the mock proxy can call.
//
// Usage: in `index.html` before this script set:
// <script>window.PERSISTENCE_CONFIG = { supabaseUrl: 'https://xyz.supabase.co', supabaseKey: 'anon-key' }</script>

(function(){
  async function request(path, opts = {}){
    const cfg = window.PERSISTENCE_CONFIG;
    if(!cfg || !cfg.supabaseUrl || !cfg.supabaseKey) throw new Error('PERSISTENCE_CONFIG not set');
    const url = cfg.supabaseUrl.replace(/\/$/, '') + '/rest/v1' + path;
    const headers = Object.assign({
      'apikey': cfg.supabaseKey,
      'Authorization': 'Bearer ' + cfg.supabaseKey,
      'Content-Type': 'application/json'
    }, opts.headers || {});
    const res = await fetch(url, Object.assign({ headers }, opts));
    if(!res.ok) throw new Error('Supabase request failed: ' + res.status + ' ' + await res.text());
    const text = await res.text();
    try{ return JSON.parse(text); }catch(e){ return text; }
  }

  const persistence = {
    async getBlocks(){
      return await request('/blocks?select=*&order=created_at.asc', { method: 'GET' });
    },
    async addBlock(block){
      // block should be an object; Supabase returns inserted row
      const rows = await request('/blocks', { method: 'POST', body: JSON.stringify(block), headers: { 'Prefer': 'return=representation' } });
      return rows && rows[0];
    },
    async getWalletByUser(userId){
      const rows = await request(`/wallets?user_id=eq.${encodeURIComponent(userId)}&select=*`, { method: 'GET' });
      return (rows && rows[0]) || null;
    },
    async createWallet(userId, data){
      const payload = Object.assign({ user_id: userId, balance: 0, address: 'PXL_' + Math.random().toString(36).slice(2,10) }, data || {});
      const rows = await request('/wallets', { method: 'POST', body: JSON.stringify(payload), headers: { 'Prefer': 'return=representation' } });
      return rows && rows[0];
    },
    async findOrCreateUserByEmail(email){
      const rows = await request(`/users?email=eq.${encodeURIComponent(email)}&select=*`, { method: 'GET' });
      if(rows && rows.length) return rows[0];
      const created = await request('/users', { method: 'POST', body: JSON.stringify({ email }), headers: { 'Prefer': 'return=representation' } });
      return created && created[0];
    }
  };

  window.persistence = persistence;
})();

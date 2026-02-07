// Minimal Supabase Auth wrapper. Requires the UMD Supabase client to be loaded
// before this script and `window.PERSISTENCE_CONFIG` to be set.
(function(){
  function safeLog(){/*noop*/}
  try{
    if(!window.PERSISTENCE_CONFIG) return;
    if(!window.supabase || !window.supabase.createClient) return;
    const cfg = window.PERSISTENCE_CONFIG;
    const client = window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseKey);

    const auth = {
      async signUp(email, password){
        const resp = await client.auth.signUp({ email, password });
        if(resp.error) throw resp.error;
        return resp.data;
      },
      async signIn(email, password){
        const resp = await client.auth.signInWithPassword({ email, password });
        if(resp.error) throw resp.error;
        return resp.data;
      },
      async signOut(){
        await client.auth.signOut();
      },
      async getUser(){
        const r = await client.auth.getUser();
        if(r.error) throw r.error;
        return r.data.user;
      }
    };

    window.supabaseClient = client;
    window.supabaseAuth = auth;
    safeLog('[supabase_auth] initialized');
  }catch(e){
    console.warn('[supabase_auth] init failed', e);
  }
})();

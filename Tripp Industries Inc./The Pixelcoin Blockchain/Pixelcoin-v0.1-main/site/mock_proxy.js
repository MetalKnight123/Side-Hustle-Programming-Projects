// Client-side mock proxy: intercepts requests to known external hosts and
// returns mocked JSON responses directly in the browser. This allows the
// static site (e.g. uploaded to Netlify) to behave like the local dev server
// without requiring server-side functions.
(function(){
  const HOSTS_TO_MOCK = ['dev-yi3omiy63etqiywc9rou3.rorktest.dev', 'toolkit.rork.com'];

  function shouldMock(url) {
    try {
      const u = new URL(url, location.href);
      return HOSTS_TO_MOCK.includes(u.hostname);
    } catch (e) {
      return false;
    }
  }

  function mockResponseFor(path, method, payload) {
    const p = path.toLowerCase();
    if (p.includes('login') || p.includes('auth')) {
      return { token: 'demo-token', user: { email: 'demo@example.com', id: 'user_demo' } };
    }
    if (p.includes('wallet')) {
      return { address: 'PXL_DEMO_ADDR', balance: 12345, transactions: [] };
    }
    if (p.includes('block') || p.includes('chain')) {
      return { blocks: [{ index: 0, hash: '0', timestamp: 0 }], height: 1 };
    }
    if (p.includes('surveys') || p.includes('completion') || p.includes('chat')) {
      return { ok: true, data: {} };
    }
    return { ok: true, path: path, method: method, payload: payload || {} };
  }

  // Helper to build a Response-like object for fetch consumers
  function makeFetchResponse(obj) {
    const body = JSON.stringify(obj);
    return Promise.resolve(new Response(body, { status: 200, headers: { 'Content-Type': 'application/json' } }));
  }

  // Patch fetch to intercept requests to known hosts
  const _origFetch = window.fetch.bind(window);
  window.fetch = async function(input, init) {
    try {
      let url = typeof input === 'string' ? input : (input && input.url) || '';
      const method = (init && init.method) || (typeof input === 'object' && input && input.method) || 'GET';
      if (shouldMock(url)) {
        const u = new URL(url, location.href);
        let payload = {};
        if (init && init.body) {
          try { payload = JSON.parse(init.body); } catch (e) { payload = { raw: init.body }; }
        }
        const obj = mockResponseFor(u.pathname + (u.search || ''), method, payload);
        return makeFetchResponse(obj);
      }
    } catch (e) {
      console.error('[mock_proxy] fetch proxy error', e);
    }
    return _origFetch(input, init);
  };

  // Minimal XMLHttpRequest interception for APIs that use XHR
  const _origXHRopen = XMLHttpRequest.prototype.open;
  const _origXHRsend = XMLHttpRequest.prototype.send;

  XMLHttpRequest.prototype.open = function(method, url/*, ...rest */) {
    try {
      this.__mock_should = shouldMock(url);
      this.__mock_method = method;
      this.__mock_url = url;
    } catch (e) {
      this.__mock_should = false;
    }
    return _origXHRopen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function(body) {
    if (this.__mock_should) {
      const u = new URL(this.__mock_url, location.href);
      let payload = {};
      try { payload = body ? JSON.parse(body) : {}; } catch (e) { payload = { raw: String(body) }; }
      const obj = mockResponseFor(u.pathname + (u.search || ''), this.__mock_method || 'GET', payload);
      const text = JSON.stringify(obj);
      // emulate async XHR behavior
      setTimeout(() => {
        try {
          this.status = 200;
          this.responseText = text;
          this.readyState = 4;
          if (typeof this.onreadystatechange === 'function') try { this.onreadystatechange(); } catch (e) {}
          if (typeof this.onload === 'function') try { this.onload({ target: this }); } catch (e) {}
        } catch (e) { console.error(e); }
      }, 0);
      return;
    }
    return _origXHRsend.apply(this, arguments);
  };

  console.log('[mock_proxy] client-side mocking active for hosts:', HOSTS_TO_MOCK.join(', '));
})();

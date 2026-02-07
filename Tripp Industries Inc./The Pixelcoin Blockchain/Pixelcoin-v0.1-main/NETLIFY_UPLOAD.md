NETLIFY: Uploading the prebuilt site
===================================

This repository contains a ready-to-upload archive `site.zip` in the project root. The archive is built so `index.html` sits at the top-level of the ZIP (Netlify's drag & drop expects that).

Quick upload steps (drag & drop):

1. Download `site.zip` from this workspace (right-click → Download in the Codespace/VS Code UI).
2. In Netlify: Sites → Add new site → Deploy manually. Drag & drop `site.zip`.
3. Netlify will unpack the archive and serve `index.html` at the root.

Local sanity-check before uploading:

```bash
unzip site.zip -d site
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

Notes & caveats
- The site includes `mock_proxy.js` (client-side). It intercepts requests to the dev API hosts and returns mock JSON inside the browser — so the site is fully static and does not require server functions.
- If you want the app to talk to a real API in production, remove or replace `mock_proxy.js` before building and upload.
- If you see missing files or ChunkLoadError after upload, open DevTools → Network and paste failing URLs here; I will patch the packaging.

If you want, I can:
- regenerate `site.zip` now (fresh copy), or
- produce a version without `mock_proxy.js` for a production upload.

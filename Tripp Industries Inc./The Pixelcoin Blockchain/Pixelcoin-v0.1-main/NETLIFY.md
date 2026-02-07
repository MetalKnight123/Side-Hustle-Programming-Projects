Netlify Deployment
===================

This repo contains a static snapshot of the app and a small helper to prepare a `dist/` folder suitable for Netlify.

Steps to enable automatic deploy from GitHub to Netlify:

1. Commit and push this repository to GitHub (branch `main` is used by the workflow).

2. In your Netlify account create a site and note the `Site ID`.

3. In your GitHub repository settings -> Secrets -> Actions add two secrets:
   - `NETLIFY_AUTH_TOKEN` — a personal access token from Netlify (you can create one under User Settings → Applications → Personal access tokens).
   - `NETLIFY_SITE_ID` — the Site ID from Netlify for the site you created.

4. On push to `main`, GitHub Actions will run the workflow at `.github/workflows/deploy-netlify.yml`, which:
   - runs `./build_for_netlify.sh` to create `dist/` (copies `index.html`, `_next/`, and `Pixelcoin_blockchain_and_miner/`), and
   - uses `npx netlify-cli` to deploy the `dist/` folder to your Netlify site.

Notes & caveats
- The site includes a client-side `mock_proxy.js` that rewrites API calls to `http://localhost:9000` for local testing. On Netlify, any API calls going to localhost will fail — you should update the runtime environment or remove the proxy if you want the app to call a remote API.
- If your app needs server-side mocks, consider implementing Netlify Functions or using a live API endpoint.
- The site includes a client-side `mock_proxy.js` that intercepts calls to known dev hosts and returns mock JSON directly in the browser. This means you can deploy the repo as a static site (drag & drop or connect Git) and the UI will behave like the local server without server-side functions.
- If you prefer to use real APIs or server-side mocks, remove or replace `mock_proxy.js` before building.
 - If you want persistent storage (so the blockchain and wallets survive across devices), you can connect a Supabase project and the included `persistence.js` adapter will store/fetch `blocks`, `users`, and `wallets` tables there.

Supabase quick setup (optional, for persistence)
1. Create a free project at https://supabase.com and note the `Project URL` and `anon public` key (from Settings → API).
2. In the SQL editor run these simple table schema commands:

```sql
create table users (id uuid primary key default gen_random_uuid(), email text unique, created_at timestamptz default now());
create table wallets (id uuid primary key default gen_random_uuid(), user_id uuid references users(id), address text, balance bigint, created_at timestamptz default now());
create table blocks (id uuid primary key default gen_random_uuid(), data jsonb, created_at timestamptz default now());
```

3. Edit `index.html` in your local copy (before uploading to Netlify) and add this snippet before the `persistence.js` script reference, replacing the values with your Supabase project details:

```html
<script>
   window.PERSISTENCE_CONFIG = {
      supabaseUrl: 'https://your-project.supabase.co',
      supabaseKey: 'your-anon-public-key'
   };
</script>
```

Supabase Auth (optional, recommended)
- To enable signing in with email/password across devices, enable Supabase Auth in your project and allow Email signups. The client-side `supabase_auth.js` (loaded by `index.html`) uses Supabase Auth for sign-in and sign-up when a `password` field is supplied in the login request. Make sure your Supabase project's CORS allows the Netlify site origin or `*` for testing.


4. Upload the modified site to Netlify. The site will use Supabase for auth/wallet/blocks and persist data across devices.

- If you want preview deploys per pull request, adjust the workflow triggers.

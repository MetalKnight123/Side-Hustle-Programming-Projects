# Pixelcoin static site (local preview)

This repo contains a saved snapshot of the Pixelcoin React/Expo web UI inside the `Pixelcoin_blockchain_and_miner` folder.

Quick start:

1. From the repository root run the simple static server:

```bash
chmod +x ./serve.sh
./serve.sh 8000
```

2. Open `http://localhost:8000/index.html` in your browser.

Notes:
- The `index.html` file is a lightweight wrapper that points at `Pixelcoin_blockchain_and_miner/entry.bundle` and image assets.
- Many of the files inside `Pixelcoin_blockchain_and_miner` are saved browser resources (they may have `.download` suffixes or be partial bundles). If you want a production-ready website we should:
  - identify and rename the correct JS/CSS bundles (remove `.download` suffixes where appropriate),
  - audit script URLs and any network requests the app makes, and
  - optionally create a small Node/Express server to serve API routes if the app expects backend endpoints.

#!/usr/bin/env bash
set -euo pipefail

# Build a simple `dist/` folder containing the static site for Netlify publishing.
# Non-destructive: copies files rather than moving/renaming originals.

SRCDIR="$(pwd)"
DISTDIR="$SRCDIR/dist"

echo "Building site into $DISTDIR"
rm -rf "$DISTDIR"
mkdir -p "$DISTDIR"

echo "Copying index.html"
cp -v index.html "$DISTDIR/"

if [ -f mock_proxy.js ]; then
  echo "Copying mock_proxy.js"
  cp -v mock_proxy.js "$DISTDIR/"
fi

if [ -d _next ]; then
  echo "Copying _next/"
  cp -a _next "$DISTDIR/"
fi

if [ -d Pixelcoin_blockchain_and_miner ]; then
  echo "Copying Pixelcoin_blockchain_and_miner/"
  cp -a Pixelcoin_blockchain_and_miner "$DISTDIR/"
fi

chmod -R a+r "$DISTDIR"
echo "Build complete. Publish directory: $DISTDIR"

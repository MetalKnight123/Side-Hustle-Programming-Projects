#!/usr/bin/env bash
# Simple local static server with fallbacks for saved `.download` files
# Usage: ./serve.sh 8000
PORT=${1:-8000}
echo "Serving current directory on http://localhost:${PORT} (with .download fallback)"
python3 ./serve_rewrite.py "$PORT"

#!/usr/bin/env python3
"""Copy saved `.download` chunk files into `_next/static/chunks` and CSS into `_next/static/css`.

This script will look for files named like `6222-63c2141dc92f8748.js.download`
and copy them to `_next/static/chunks/6222-63c2141dc92f8748.js`.
It will also copy CSS files referenced by the webpack bootstrap.
"""
import os
import shutil
import re

ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, 'Pixelcoin_blockchain_and_miner')
OUT = os.path.join(ROOT, '_next', 'static')

os.makedirs(OUT, exist_ok=True)
CHUNKS_OUT = os.path.join(OUT, 'chunks')
CSS_OUT = os.path.join(OUT, 'css')
os.makedirs(CHUNKS_OUT, exist_ok=True)
os.makedirs(CSS_OUT, exist_ok=True)

js_chunk_re = re.compile(r'^(\d+)-([0-9a-fA-F]+)\.js(?:\.download)?$')
css_re = re.compile(r'^[0-9a-fA-F]{8}.*\.css$|^06da1025bfdab617\.css$')

copied = 0
for name in os.listdir(SRC):
    m = js_chunk_re.match(name)
    if m:
        src = os.path.join(SRC, name)
        dest_name = name.replace('.download', '')
        # dest should be like 6222-63c2141dc92f8748.js
        dest = os.path.join(CHUNKS_OUT, dest_name)
        if not os.path.exists(dest):
            shutil.copy2(src, dest)
            copied += 1

    # Also handle files like main-app-*.js.download which might be entry points
    if name.endswith('.js.download') and not js_chunk_re.match(name):
        src = os.path.join(SRC, name)
        dest_name = name.replace('.download', '')
        dest = os.path.join(OUT, dest_name)
        if not os.path.exists(dest):
            shutil.copy2(src, dest)
            copied += 1

    if css_re.match(name) or name.endswith('.css'):
        src = os.path.join(SRC, name)
        dest = os.path.join(CSS_OUT, name)
        if not os.path.exists(dest):
            shutil.copy2(src, dest)
            copied += 1

print(f'Copied {copied} files into {OUT}')

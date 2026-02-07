#!/usr/bin/env python3
"""Copy .download files to usable names and place chunks/CSS where webpack expects them.

This script will:
- For every file in `Pixelcoin_blockchain_and_miner` that ends with `.download`, copy it
  to the same path without the `.download` suffix (if that file does not already exist).
- Copy chunk files matching `<num>-<hash>.js` into `_next/static/chunks/`.
- Copy CSS files into `_next/static/css/`.
- Copy other likely runtime files (webpack, polyfills, main-app) into `_next/static/`.

It only copies files and will not delete originals.
"""
import os
import shutil
import re

ROOT = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT, 'Pixelcoin_blockchain_and_miner')
OUT_DIR = os.path.join(ROOT, '_next', 'static')
CHUNKS_DIR = os.path.join(OUT_DIR, 'chunks')
CSS_DIR = os.path.join(OUT_DIR, 'css')

os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)

js_chunk_re = re.compile(r'^(\d+)-[0-9a-fA-F]+\.js$')
download_re = re.compile(r'^(.*)\.download$')

copied = []

for name in os.listdir(SRC_DIR):
    src = os.path.join(SRC_DIR, name)
    if not os.path.isfile(src):
        continue
    m = download_re.match(name)
    if m:
        dest_name = m.group(1)
        dest = os.path.join(SRC_DIR, dest_name)
        if not os.path.exists(dest):
            shutil.copy2(src, dest)
            copied.append(dest)
            print('copied:', src, '->', dest)

# Now scan the folder for js/css to place into _next/static
for name in os.listdir(SRC_DIR):
    path = os.path.join(SRC_DIR, name)
    if not os.path.isfile(path):
        continue
    # place chunk files
    if js_chunk_re.match(name):
        dest = os.path.join(CHUNKS_DIR, name)
        if not os.path.exists(dest):
            shutil.copy2(path, dest)
            copied.append(dest)
            print('chunk placed:', path, '->', dest)
    # common names that webpack might request from /_next/static
    if name.startswith('webpack-') and name.endswith('.js'):
        dest = os.path.join(OUT_DIR, name)
        if not os.path.exists(dest):
            shutil.copy2(path, dest)
            copied.append(dest)
            print('webpack runtime placed:', path, '->', dest)
    if name.startswith('polyfills') and name.endswith('.js'):
        dest = os.path.join(OUT_DIR, name)
        if not os.path.exists(dest):
            shutil.copy2(path, dest)
            copied.append(dest)
            print('polyfills placed:', path, '->', dest)
    if name.startswith('main-app') and name.endswith('.js'):
        dest = os.path.join(OUT_DIR, name)
        if not os.path.exists(dest):
            shutil.copy2(path, dest)
            copied.append(dest)
            print('main-app placed:', path, '->', dest)
    # css
    if name.endswith('.css'):
        dest = os.path.join(CSS_DIR, name)
        if not os.path.exists(dest):
            shutil.copy2(path, dest)
            copied.append(dest)
            print('css placed:', path, '->', dest)

print('\nSummary: copied/placed', len(copied), 'files')

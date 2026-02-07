#!/usr/bin/env python3
"""Simple HTTP server that falls back to `.download` files and the
`Pixelcoin_blockchain_and_miner` folder when a requested file is missing.

Usage: python3 serve_rewrite.py 8000
"""
import http.server
import socketserver
import os
import sys
from urllib.parse import unquote, urlparse


class FallbackRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        # Adapted from SimpleHTTPRequestHandler.send_head
        path = unquote(urlparse(self.path).path)
        if path.startswith('/'):
            path = path[1:]
        candidates = [path]
        if path and not path.endswith('.download'):
            candidates.append(path + '.download')
        # Also try inside Pixelcoin_blockchain_and_miner
        candidates.append(os.path.join('Pixelcoin_blockchain_and_miner', path))
        if path and not path.endswith('.download'):
            candidates.append(os.path.join('Pixelcoin_blockchain_and_miner', path + '.download'))

        for candidate in candidates:
            if not candidate:
                candidate = 'index.html'
            if os.path.isdir(candidate):
                # serve index.html from that directory
                index = os.path.join(candidate, 'index.html')
                if os.path.exists(index):
                    return self._serve_file(index)
                continue
            if os.path.exists(candidate) and os.path.isfile(candidate):
                return self._serve_file(candidate)

        # Fallback to default behavior (404)
        return http.server.SimpleHTTPRequestHandler.send_head(self)

    def _serve_file(self, filepath):
        try:
            f = open(filepath, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", self.guess_type(filepath))
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f


def run(port=8000):
    handler = FallbackRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving on http://0.0.0.0:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down")


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run(port)

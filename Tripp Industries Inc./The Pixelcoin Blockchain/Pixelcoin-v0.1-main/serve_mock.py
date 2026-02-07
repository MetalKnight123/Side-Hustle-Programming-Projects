#!/usr/bin/env python3
"""Very small mock API server for dev preview.

Responds to any request under `/` with JSON; sets CORS headers so the browser
will accept responses when the app rewrites external API calls to this server.

Usage: python3 serve_mock.py 9000
"""
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse


class MockHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        body = self._mock_response(parsed.path, 'GET')
        self._set_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode() if length else ''
        try:
            payload = json.loads(raw) if raw else {}
        except Exception:
            payload = {'raw': raw}
        body = self._mock_response(parsed.path, 'POST', payload)
        self._set_headers()
        self.wfile.write(json.dumps(body).encode())

    def _mock_response(self, path, method, payload=None):
        # Simple heuristics to return plausible shapes the app can consume.
        p = path.lower()
        if 'login' in p or 'auth' in p:
            return {'token': 'demo-token', 'user': {'email': 'demo@example.com', 'id': 'user_demo'}}
        if 'wallet' in p:
            return {'address': 'PXL_DEMO_ADDR', 'balance': 12345, 'transactions': []}
        if 'block' in p or 'chain' in p:
            return {'blocks': [{'index': 0, 'hash': '0', 'timestamp': 0}], 'height': 1}
        if 'surveys' in p or 'completion' in p or 'chat' in p:
            return {'ok': True, 'data': {}}
        # Default generic response
        return {'ok': True, 'path': path, 'method': method, 'payload': payload or {}}


def run(port=9000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockHandler)
    print(f'Mock API server running at http://0.0.0.0:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Stopping mock server')


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    run(port)

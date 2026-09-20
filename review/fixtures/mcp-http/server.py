"""A bounded HTTP tools/call slice, not a complete MCP server or OAuth verifier."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = '2026-07-28'
ORIGIN = 'http://localhost:8765'


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, status, body):
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def error(self, status, request_id, code, message):
        self.reply(status, {'jsonrpc': '2.0', 'id': request_id, 'error': {'code': code, 'message': message}})

    def do_GET(self):
        self.error(405, None, -32600, 'POST required')

    def do_POST(self):
        if self.path != '/mcp':
            return self.error(404, None, -32600, 'Unknown endpoint')
        if self.headers.get('Origin') not in (None, ORIGIN):
            return self.error(403, None, -32600, 'Invalid origin')
        if self.headers.get('Authorization') != 'Bearer fixture-only-alpha':
            return self.error(401, None, -32600, 'Fixture identity required')
        try:
            request = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))))
            request_id = request['id']
            params = request['params']
            version = params['_meta']['io.modelcontextprotocol/protocolVersion']
            method = request['method']
        except (ValueError, KeyError, TypeError):
            return self.error(400, None, -32600, 'Invalid request')
        if (self.headers.get('MCP-Protocol-Version') != version
                or self.headers.get('Mcp-Method') != method):
            return self.error(400, request_id, -32020, 'HeaderMismatch')
        if version != VERSION:
            return self.error(400, request_id, -32600, 'Unsupported fixture protocol')
        if method != 'tools/call':
            return self.error(404, request_id, -32601, 'Method not found')
        if params.get('name') != 'read_note' or params.get('arguments') != {}:
            return self.error(400, request_id, -32602, 'Invalid tool or arguments')
        self.reply(200, {'jsonrpc': '2.0', 'id': request_id, 'result': {
            'resultType': 'complete', 'content': [{'type': 'text', 'text': 'Alpha roadmap'}],
            'isError': False}})


def make_server():
    return ThreadingHTTPServer(('127.0.0.1', 0), Handler)

import http.client
import json
import threading
import unittest
from server import make_server, VERSION, ORIGIN


def request(server, overrides=None, method='POST'):
    body = {'jsonrpc': '2.0', 'id': 7, 'method': 'tools/call', 'params': {
        'name': 'read_note', 'arguments': {}, '_meta': {
            'io.modelcontextprotocol/protocolVersion': VERSION,
            'io.modelcontextprotocol/clientInfo': {'name': 'fixture', 'version': '1'},
            'io.modelcontextprotocol/clientCapabilities': {}}}}
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
               'MCP-Protocol-Version': VERSION, 'Mcp-Method': 'tools/call', 'Mcp-Name': 'read_note',
               'Authorization': 'Bearer fixture-only-alpha', 'Origin': ORIGIN}
    headers.update(overrides or {})
    connection = http.client.HTTPConnection(*server.server_address, timeout=3)
    try:
        connection.request(method, '/mcp', json.dumps(body), headers)
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), json.loads(response.read())
    finally:
        connection.close()


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server()
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()

    def test_success(self):
        status, headers, body = request(self.server)
        self.assertEqual(200, status)
        self.assertEqual(7, body['id'])
        self.assertFalse(body['result']['isError'])
        self.assertNotIn('Mcp-Session-Id', headers)

    def test_origin(self):
        self.assertEqual(403, request(self.server, {'Origin': 'https://untrusted.example'})[0])

    def test_authentication(self):
        self.assertEqual(401, request(self.server, {'Authorization': 'Bearer invalid-fixture'})[0])

    def test_legacy_get(self):
        self.assertEqual(405, request(self.server, method='GET')[0])


if __name__ == '__main__':
    unittest.main()

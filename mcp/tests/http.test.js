import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import {Client, StreamableHTTPClientTransport} from '@modelcontextprotocol/client';
import {startServer} from '../dev.js';
import {handleMcp} from '../server.js';

let server, url;
before(async () => {server = await startServer(); url = `http://127.0.0.1:${server.address().port}/mcp`;});
after(async () => {server.closeAllConnections(); await new Promise(resolve => server.close(resolve));});

async function client(mode) {
  const result = new Client({name: 'vibe-library-tests', version: '1.5.0'}, {versionNegotiation: {mode}});
  await result.connect(new StreamableHTTPClientTransport(new URL(url)));
  return result;
}

for (const mode of ['legacy', 'auto']) {
  test(`${mode} official SDK client: discovery, annotations, search, exact fetch and errors over real HTTP`, async () => {
    const connection = await client(mode);
    try {
      if (mode === 'auto') assert.equal(connection.getNegotiatedProtocolVersion(), '2026-07-28');
      const tools = (await connection.listTools()).tools;
      assert.deepEqual(tools.map(tool => tool.name), ['search_workflows', 'get_workflow']);
      for (const tool of tools) {
        assert.deepEqual(tool.annotations, {readOnlyHint: true, destructiveHint: false, openWorldHint: false});
        assert.equal(tool.inputSchema.additionalProperties, false);
        assert.ok(tool.outputSchema);
      }
      const result = await connection.callTool({name: 'search_workflows', arguments: {query: 'MCP', mode: 'check', language: 'ru'}});
      assert.equal(result.isError, undefined);
      assert.equal(result.structuredContent.workflows[0].id, 'mcp-protocol-auth-check');
      const fetched = await connection.callTool({name: 'get_workflow', arguments: {id: result.structuredContent.workflows[0].id}});
      assert.equal(fetched.structuredContent.instruction_language, 'en');
      assert.ok(fetched.structuredContent.files.some(file => file.path === 'references/mcp-contract.md'));
      assert.ok(fetched.structuredContent.words < 3500);
      const missing = await connection.callTool({name: 'get_workflow', arguments: {id: 'does-not-exist'}});
      assert.equal(missing.isError, true);
      for (const args of [{id: '../secrets'}, {id: 'api-audit', credentials: 'ignored-field'}]) {
        const invalid = await connection.callTool({name: 'get_workflow', arguments: args});
        assert.equal(invalid.isError, true);
      }
      const overflow = await connection.callTool({name: 'search_workflows', arguments: {query: 'a'.repeat(161)}});
      assert.equal(overflow.isError, true);
    } finally {await connection.close();}
  });
}

test('Origin denial and malformed protocol do not look like successful tool calls', async () => {
  const headers = {'Content-Type': 'application/json', Accept: 'application/json, text/event-stream'};
  const denied = await fetch(url, {method: 'POST', headers: {...headers, Origin: 'https://unrelated.example'}, body: '{}'});
  assert.equal(denied.status, 403);
  const malformed = await fetch(url, {method: 'POST', headers, body: '{'});
  assert.equal(malformed.status, 400);
  const oversized = await fetch(url, {method: 'POST', headers, body: 'a'.repeat(65537)});
  assert.equal(oversized.status, 413);
  const sameOrigin = await fetch(url, {method: 'POST', headers: {...headers, Origin: new URL(url).origin},
    body: JSON.stringify({jsonrpc: '2.0', id: 1, method: 'initialize', params: {protocolVersion: '2025-11-25', capabilities: {}, clientInfo: {name: 'origin-control', version: '1.0.0'}}})});
  assert.equal(sameOrigin.status, 200);
});

test('modern method, name and version headers must agree with the request body', async () => {
  const meta = {'io.modelcontextprotocol/protocolVersion': '2026-07-28',
    'io.modelcontextprotocol/clientInfo': {name: 'header-tests', version: '1.5.0'},
    'io.modelcontextprotocol/clientCapabilities': {}};
  const body = JSON.stringify({jsonrpc: '2.0', id: 9, method: 'tools/call',
    params: {name: 'get_workflow', arguments: {id: 'api-audit'}, _meta: meta}});
  const headers = {'Content-Type': 'application/json', Accept: 'application/json, text/event-stream',
    'MCP-Protocol-Version': '2026-07-28', 'Mcp-Method': 'tools/call', 'Mcp-Name': 'get_workflow'};
  const control = await fetch(url, {method: 'POST', headers, body});
  assert.equal(control.status, 200);
  assert.equal((await control.json()).result.structuredContent.workflow.id, 'api-audit');
  for (const changed of [{'Mcp-Method': 'tools/list'}, {'Mcp-Name': 'search_workflows'},
    {'MCP-Protocol-Version': '2025-11-25'}]) {
    const response = await fetch(url, {method: 'POST', headers: {...headers, ...changed}, body});
    assert.equal(response.status, 400);
    assert.equal((await response.json()).error.code, -32020);
  }
  const oversized = await handleMcp(new Request(url, {method: 'POST', headers, body: 'a'.repeat(65537)}));
  assert.equal(oversized.status, 413);
});

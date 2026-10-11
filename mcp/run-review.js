import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {Client, StreamableHTTPClientTransport} from '@modelcontextprotocol/client';
import {startServer} from './dev.js';

const cases = JSON.parse(await readFile(new URL('./review-cases.json', import.meta.url)));
const local = process.argv[2] ? null : await startServer();
const endpoint = process.argv[2] || `http://127.0.0.1:${local.address().port}/mcp`;
const client = new Client({name: 'vibe-library-review', version: '1.5.0'}, {versionNegotiation: {mode: 'auto'}});
const results = [];
try {
  await client.connect(new StreamableHTTPClientTransport(new URL(endpoint)));
  const tools = (await client.listTools()).tools;
  assert.deepEqual(tools.map(tool => tool.name), ['search_workflows', 'get_workflow']);
  for (const [kind, list] of Object.entries(cases)) {
    for (const [index, scenario] of list.entries()) {
      const calls = [];
      for (const call of scenario.calls) {
        const started = performance.now();
        let output;
        try { output = await client.callTool(call); }
        catch (error) { output = {isError: true, protocol_error: error.code, message: error.message}; }
        if (kind === 'negative') assert.equal(output.isError, true, scenario.description);
        else {
          assert.ok(!output.isError, scenario.description);
          assert.ok(output.structuredContent, scenario.description);
          const data = output.structuredContent;
          if (call.name === 'get_workflow') {
            assert.equal(data.workflow.id, call.arguments.id);
            for (const file of data.files) assert.equal(createHash('sha256').update(file.text).digest('hex'), file.sha256);
            assert.equal(data.files.some(file => file.path === 'references/hosts.md'), call.arguments.host === 'claude');
          } else if (index < 4) {
            const expected = ['mcp-protocol-auth-check', 'sql-databases-audit', 'mcp-server-audit', 'cache-invalidation-audit'][index];
            assert.ok(data.workflows.some(row => row.id === expected), scenario.description);
          } else {
            assert.equal(data.total, 3);
            assert.equal(data.workflows.length, call.arguments.offset ? 1 : 2);
            assert.equal(data.next_offset, call.arguments.offset ? null : 2);
          }
        }
        calls.push({call, duration_ms: Math.round(performance.now() - started),
          isError: !!output.isError, ...(output.structuredContent ? {result: output.structuredContent} : {error: output})});
      }
      results.push({kind, case: index + 1, description: scenario.description, status: 'passed', calls});
    }
  }
  const report = {endpoint, at: new Date().toISOString(), protocol: client.getNegotiatedProtocolVersion(),
    positive: 5, negative: 3, status: 'passed',
    scope: 'Actual tool calls and transport behavior. Natural-language model selection is not evaluated by this harness.',
    results};
  if (process.argv[3]) await writeFile(process.argv[3], JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({endpoint, protocol: report.protocol, positive: 5, negative: 3, status: 'passed'}));
} finally {
  await client.close();
  if (local) {local.closeAllConnections(); await new Promise(resolve => local.close(resolve));}
}

import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import library from '../generated/library.json' with {type: 'json'};
import {searchWorkflows, getWorkflow, libraryStatus} from '../library.js';

test('English, Spanish, Russian and Chinese search selects real workflow IDs', () => {
  for (const [query, expected] of [['API', 'api-audit'], ['auditoría SQL', 'sql-databases-audit'],
    ['аудит MCP', 'mcp-server-audit'], ['缓存', 'cache-invalidation-audit']]) {
    const result = searchWorkflows({query, limit: 10});
    assert.ok(result.workflows.some(row => row.id === expected), query);
  }
});

test('operation and skill filters intersect and pagination has no duplicates', () => {
  const result = searchWorkflows({query: 'API', skill: 'vibe-backend', mode: 'check'});
  assert.deepEqual(result.workflows.map(row => row.id), ['api-contract-compatibility-check']);
  const a = searchWorkflows({limit: 10});
  const b = searchWorkflows({limit: 10, offset: a.next_offset});
  assert.equal(a.total, 241);
  assert.equal(new Set([...a.workflows, ...b.workflows].map(row => row.id)).size, 20);
  assert.equal(searchWorkflows({query: 'zzzzzzz-no-such-domain'}).total, 0);
});

test('body search is explicit and results localize without changing IDs', () => {
  assert.equal(searchWorkflows({query: 'business meaning'}).total, 0);
  assert.ok(searchWorkflows({query: 'business meaning', full_text: true}).total > 0);
  const en = searchWorkflows({query: 'SQL'});
  const ru = searchWorkflows({query: 'SQL', language: 'ru'});
  assert.deepEqual(en.workflows.map(row => row.id), ru.workflows.map(row => row.id));
  assert.notEqual(en.workflows[0].title, ru.workflows[0].title);
});

test('all 241 bundles preserve exact source bytes and load a bounded relevant context', () => {
  assert.equal(libraryStatus().skills, 46);
  assert.equal(Object.keys(library.files).length, 297);
  for (const row of library.recipes) {
    const result = getWorkflow({id: row.id});
    assert.ok(result.files.some(file => file.path === row.path));
    assert.equal(result.files.filter(file => /\/SKILL.md$/.test(file.path)).length, 1);
    assert.ok(result.files.length >= 3 && result.files.length <= 8, row.id);
    assert.equal(result.files.some(file => file.path === 'references/hosts.md'), false);
    for (const file of result.files) {
      assert.equal(createHash('sha256').update(file.text).digest('hex'), file.sha256);
      assert.ok(file.source_url.startsWith('https://github.com/arty-kk/vibe-coding/blob/v1.4.1/'));
    }
  }
});

test('host context is opt-in and unknown IDs cannot read arbitrary files or URLs', () => {
  assert.ok(getWorkflow({id: 'mcp-protocol-auth-check', host: 'claude'}).files.some(file => file.path === 'references/hosts.md'));
  for (const id of ['unknown-workflow', '../PRIVACY.md', 'https://example.com']) {
    assert.throws(() => getWorkflow({id}), /Unknown workflow ID/);
  }
  assert.throws(() => searchWorkflows({skill: 'vibe-unknown'}), /Unknown skill/);
});

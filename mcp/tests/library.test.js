import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import library from '../generated/library.json' with {type: 'json'};
import {readFileSync} from 'node:fs';
import {searchWorkflows, getWorkflow, libraryStatus, INSTRUCTION_VERSION} from '../library.js';

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
      assert.ok(file.source_url.startsWith(`https://github.com/arty-kk/vibe-coding/blob/v${INSTRUCTION_VERSION}/`));
    }
  }
});

const judged = JSON.parse(readFileSync(new URL('../../review/search-cases-1.6.0.json', import.meta.url)));
test('judged task goals and cross-domain negatives keep the correct workflow within the accepted rank', () => {
  for (const row of judged.cases) {
    const found = searchWorkflows({query: row.query, language: row.language, limit: 10});
    const top = found.workflows.slice(0, row.max_rank).map(item => item.id);
    assert.ok(row.expected.some(id => top.includes(id)), row.id + ': ' + JSON.stringify(top));
    assert.ok(found.workflows.every(item => item.purpose && item.match.kind));
  }
  for (const row of judged.negative_cases) assert.equal(searchWorkflows(row).total, 0, JSON.stringify(row));
});

test('every stable ID and translated title is directly discoverable', () => {
  for (const row of library.recipes) {
    assert.equal(searchWorkflows({query: row.id}).workflows[0].id, row.id);
    for (const locale of Object.values(library.locales)) {
      assert.equal(searchWorkflows({query: locale.titles[row.id]}).workflows[0].id, row.id, locale.titles[row.id]);
    }
  }
});

test('read-only requests, known fixes and composed corrections keep distinct stages', () => {
  const inspect = getWorkflow({id: 'mcp-server-audit'});
  assert.deepEqual(inspect.execution.steps.map(step => step.id), ['mcp-server-audit']);
  const compose = getWorkflow({id: 'mcp-server-audit', intent: 'improve'});
  assert.deepEqual(compose.execution.steps.map(step => step.id),
    ['mcp-server-audit', 'mcp-server-polish', 'mcp-protocol-auth-check', 'patch-checking']);
  assert.equal(compose.files.filter(file => /\/references\//.test(file.path) && file.path.startsWith('skills/')).length, 1);
  const fix = getWorkflow({id: 'mcp-server-polish'});
  assert.deepEqual(fix.execution.steps.map(step => step.id), ['mcp-server-polish', 'mcp-protocol-auth-check', 'patch-checking']);
  assert.deepEqual(getWorkflow({id: 'mcp-protocol-auth-check'}).execution.steps.map(step => step.id), ['mcp-protocol-auth-check']);
  const freshness = getWorkflow({id: 'map-staleness-check'}).execution;
  assert.deepEqual(freshness.steps.map(step => step.id), ['map-staleness-check']);
  assert.ok(!freshness.transitions.some(edge => edge.to === 'map-staleness-check'));
  assert.deepEqual(getWorkflow({id: 'task-shaping'}).execution.steps.map(step => step.id), ['task-shaping', 'validation-clarification']);
  assert.equal(compose.execution.status, 'instructions_only');
  assert.ok(!('verdict' in compose.execution));
});

test('patch review repeats corrections and exits on findings, missing evidence or no progress', () => {
  const result = getWorkflow({id: 'patch-checking'});
  const edges = result.execution.transitions;
  assert.ok(edges.some(edge => edge.outcome === 'corrections_applied' && edge.to === 'patch-checking'));
  assert.ok(edges.some(edge => edge.outcome === 'clean' && edge.to === null));
  assert.ok(edges.some(edge => edge.outcome === 'blocked' && edge.to === null));
  assert.ok(edges.some(edge => edge.outcome === 'findings_without_repair_authority' && edge.to === null));
  assert.equal(result.execution.completion.clean_marker, '✅ Everything is fine. No changes required 👌');
  for (const row of library.recipes) {
    const flow = getWorkflow({id: row.id, intent: 'improve'}).execution;
    for (const edge of flow.transitions) {
      assert.ok(edge.to === null || flow.steps.some(step => step.id === edge.to), row.id);
      assert.ok(flow.steps.some(step => step.id === edge.from), row.id);
    }
  }
});

test('later same-domain steps reuse context while retaining specialized instructions', () => {
  const first = getWorkflow({id: 'mcp-server-audit', host: 'generic'});
  const later = getWorkflow({id: 'mcp-server-polish', include_context: false});
  assert.ok(later.words < first.words);
  assert.ok(later.files.every(file => file.path !== 'references/workflow.md' && file.path !== 'references/cycles.md' && !file.path.endsWith('/SKILL.md')));
  assert.ok(later.files.some(file => file.path === 'references/mcp-contract.md'));
});

test('host context is opt-in and unknown IDs cannot read arbitrary files or URLs', () => {
  assert.ok(getWorkflow({id: 'mcp-protocol-auth-check', host: 'claude'}).files.some(file => file.path === 'references/hosts.md'));
  for (const id of ['unknown-workflow', '../PRIVACY.md', 'https://example.com']) {
    assert.throws(() => getWorkflow({id}), /Unknown workflow ID/);
  }
  assert.throws(() => searchWorkflows({skill: 'vibe-unknown'}), /Unknown skill/);
});

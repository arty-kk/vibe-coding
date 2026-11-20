import {test} from 'node:test';
import assert from 'node:assert/strict';
import library from '../generated/library.json' with {type:'json'};
import {searchWorkflows, getWorkflow} from '../library.js';

test('the reported Russian word and its permission variants reach the owning workflows', () => {
  for (const query of ['авторизация','авторизации','авторизацию','право доступа','права доступа','полномочия']) {
    const rows = searchWorkflows({query,language:'ru'}).workflows;
    assert.equal(rows[0].id,'auth-permissions-audit',query);
    assert.ok(rows.slice(0,3).some(row => row.id==='rbac-abac-policy-audit'),query);
    assert.ok(rows[0].title !== 'Auth Permissions Audit');
  }
  const login = searchWorkflows({query:'вход по oauth'});
  assert.equal(login.workflows[0].id,'oauth-oidc-session-check');
});

test('all domain/topic keys are discoverable, bounded and backed by real workflows', () => {
  const seen = new Set();
  for (const language of ['en','es','ru','zh-CN']) {
    const root = searchWorkflows({view:'catalog',language});
    assert.equal(root.catalog.domains.length,48);
    assert.equal(root.workflows.length,0);
    assert.ok(Buffer.byteLength(JSON.stringify(root)) < 16000);
    assert.ok(!JSON.stringify(root).includes('source_url'));
    for (const domain of root.catalog.domains) {
      const scoped = searchWorkflows({view:'catalog',skill:domain.key,language});
      assert.ok(scoped.catalog.topics.length > 0);
      assert.ok(Buffer.byteLength(JSON.stringify(scoped)) < 16000);
      for (const topic of scoped.catalog.topics) {
        assert.ok(topic.keywords.length && topic.keywords.every(value => /^[\x20-\x7e]+$/.test(value)));
        for (const mode of topic.modes) {
          const result = searchWorkflows({topic:topic.key,skill:domain.key,mode,language,limit:10});
          assert.ok(result.total > 0,topic.key+':'+mode);
          assert.ok(result.workflows.every(row => row.skill===domain.key && row.mode===mode));
          assert.deepEqual(result.workflows.map(row=>row.id).sort(),
            topic.workflow_ids.filter(id=>library.recipes.find(row=>row.id===id).mode===mode).sort());
        }
        topic.workflow_ids.forEach(id=>seen.add(id));
      }
    }
  }
  assert.deepEqual([...seen].sort(),library.recipes.map(row=>row.id).sort());
});

test('a caller can browse first, select an actual authorization key and load the exact implementation', () => {
  const domains = searchWorkflows({view:'catalog',mode:'implement',language:'ru'}).catalog.domains;
  const domain = domains.find(row=>row.key==='vibe-domain');
  assert.ok(domain);
  const topics = searchWorkflows({view:'catalog',skill:domain.key,mode:'implement',language:'ru'}).catalog.topics;
  const topic = topics.find(row=>row.key==='auth-permissions');
  assert.ok(topic.keywords.includes('authorization'));
  const result = searchWorkflows({topic:topic.key,skill:domain.key,mode:'implement'});
  assert.deepEqual(result.workflows.map(row=>row.id),['auth-permissions-polish']);
  const loaded = getWorkflow({id:result.workflows[0].id});
  assert.equal(loaded.execution.status,'instructions_only');
  assert.equal(loaded.execution.current_step,'auth-permissions-polish');
});

test('common misspellings and a vague backend complaint route without invented keywords', () => {
  for (const query of ['авторизаця','авторзиация']) {
    assert.equal(searchWorkflows({query}).workflows[0].id,'auth-permissions-audit',query);
  }
  for (const query of ['бекенд глючит','бэкэнд глюичт','блин что-то бэкэнд глючит','debug backend']) {
    const found = searchWorkflows({query});
    assert.equal(found.workflows[0].id,'instant-backend-probe',query);
    const flow = getWorkflow({id:found.workflows[0].id});
    assert.equal(flow.execution.current_step,'instant-backend-probe');
    assert.ok(flow.execution.steps.some(step=>step.id==='patch-checking'));
  }
  assert.equal(searchWorkflows({query:'kubernets'}).workflows[0].id,'kubernetes-platform-audit');
  assert.equal(searchWorkflows({query:'sector'}).total,0);
  assert.equal(searchWorkflows({query:'author biography'}).total,0);
  const misspelledKey = searchWorkflows({topic:'auth-permissons'});
  assert.equal(misspelledKey.catalog.status,'unknown_topic');
});

test('catalog recovery never invents a topic or drops explicit filters', () => {
  const unknown = searchWorkflows({topic:'made-up-authorization-key',skill:'vibe-domain',mode:'implement'});
  assert.equal(unknown.total,0);
  assert.equal(unknown.catalog.status,'unknown_topic');
  assert.ok(unknown.catalog.topics.every(topic=>topic.skill==='vibe-domain' && topic.modes.includes('implement')));
  assert.equal(searchWorkflows({topic:'auth-permissions',skill:'vibe-sql'}).total,0);
  assert.equal(searchWorkflows({topic:'auth-permissions',mode:'review'}).total,0);
  assert.equal(searchWorkflows({view:'catalog',skill:'vibe-cache',mode:'review'}).catalog.status,'empty_scope');
  assert.deepEqual(searchWorkflows({view:'catalog',mode:'review'}).catalog.domains.map(row=>row.key),['vibe-review']);
  assert.throws(()=>searchWorkflows({view:'catalog',query:'private words'}),/Leave query empty/);
});

const websiteCases = JSON.parse((await import('node:fs')).readFileSync(
  new URL('../../review/web-experience-cases-1.7.0.json', import.meta.url), 'utf8'));

test('website goals reach their expected method in the localized catalog', () => {
  for (const {query, language, expected, max_rank} of websiteCases.cases) {
    const ids = searchWorkflows({query, language}).workflows.slice(0, max_rank).map(row => row.id);
    assert.ok(ids.some(id => expected.includes(id)), `${query} → ${ids}`);
  }
});

test('specific ordinary-language project requests survive unfamiliar business context', () => {
  for (const [query, expected] of [
    ['Создай сайт для цветочной лавки у вокзала', 'homepage-landing-build'],
    ['Доделай сайт студии керамики, маме нужна рабочая форма', 'homepage-landing-polish'],
    ['Хочу сайт школы танцев. Сначала нужно понять предложение', 'web-offer-synthesis']
  ]) assert.equal(searchWorkflows({query}).workflows[0]?.id, expected, query);
  assert.equal(searchWorkflows({query:'Собери отчет о запасах глины'}).total, 0);
  assert.equal(searchWorkflows({query:'Доделай сайт гончарной студии',skill:'vibe-sql'}).total, 0);
});

test('new, existing and read-only page tasks load the correct stages and resources', () => {
  const proposal = getWorkflow({id:'web-offer-synthesis'}).execution.steps;
  assert.equal(proposal.at(-1).id, 'web-experience-brief');
  assert.ok(proposal.every(step => step.role !== 'implement'));
  for (const id of ['homepage-landing-build', 'homepage-landing-polish']) {
    const ids = getWorkflow({id}).execution.steps.map(s => s.id);
    assert.deepEqual(ids.slice(1), ['web-visual-hierarchy-check','web-navigation-state-check',
      'web-interaction-motion-check','web-search-performance-check','web-page-acceptance-check','patch-checking']);
  }
  assert.equal(getWorkflow({id:'homepage-landing-audit'}).execution.steps.length, 1);
  assert.ok(getWorkflow({id:'web-design-kit'}).files.some(f=>f.path.endsWith('/compile_design_kit.py')));
  assert.ok(getWorkflow({id:'web-visual-system'}).files.every(f=>!f.path.endsWith('.py')));
});

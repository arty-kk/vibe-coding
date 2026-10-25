const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const engine = require('../site/catalog-engine.js');
const root = path.join(__dirname, '..');
const rows = JSON.parse(fs.readFileSync(path.join(root,'plugins/vibe-coding/catalog.json'))).recipes;
const locales = ['en','es','ru','zh-CN'].map(lang => JSON.parse(fs.readFileSync(path.join(root,`plugins/vibe-coding/assets/catalog/locales/${lang}.json`))));
const topics = Object.fromEntries(Object.keys(locales[0].categories).map(skill => [skill, locales.map(l => l.categories[skill])]));
const actions = Object.fromEntries(Object.keys(locales[0].modes).map(mode => [mode, locales.map(l => l.modes[mode])]));
const lexicon = JSON.parse(fs.readFileSync(path.join(root,'plugins/vibe-coding/assets/catalog/search-lexicon.json')));
const entries = engine.prepare(rows.map(r => ({...r,titles:locales.map(l => l.titles[r.id])})),topics,actions,lexicon);
const state = (overrides={}) => ({q:'',topic:'',action:'',full:false,page:1,...overrides});
const ids = result => result.matches.map(x => x.entry.id);

test('API search prioritizes direct workflows, without incidental body matches', () => {
  const found = engine.select(entries,state({q:'API'}));
  assert.equal(found.matches[0].entry.id,'api-audit');
  assert.ok(found.matches.length >= 8);
  assert.ok(!ids(found).includes('llm-agent-tools-audit'));
  const bodies = {'llm-agent-tools-audit':{body:'Audit tool API ownership.'}};
  assert.ok(ids(engine.select(entries,state({q:'API',full:true}),bodies)).includes('llm-agent-tools-audit'));
  assert.ok(!ids(engine.select(entries,state({q:'API'}),bodies)).includes('llm-agent-tools-audit'));
});

test('word-prefix matching does not match API in rapid or SQL in NoSQL', () => {
  const sample = engine.prepare([{id:'rapid',titles:['Rapid NoSQL'],skill:'data',mode:'audit'}],{data:['Data']},{audit:['Audit']});
  assert.equal(engine.select(sample,state({q:'API'})).matches.length,0);
  assert.equal(engine.select(sample,state({q:'SQL'})).matches.length,0);
  assert.equal(engine.select(sample,state({q:'rapid'})).matches.length,1);
});

test('search uses all four title languages and folds accents/case', () => {
  for (const q of ['API','аудит API','caché','缓存','KUBERNETES']) assert.ok(engine.select(entries,state({q})).matches.length > 0,q);
  assert.deepEqual(ids(engine.select(entries,state({q:'caché'}))),ids(engine.select(entries,state({q:'cache'}))));
});

test('query, topic and task intersect; facet counts exclude their own selection', () => {
  const result = engine.select(entries,state({q:'api',topic:'vibe-backend',action:'check'}));
  assert.deepEqual(ids(result),['api-contract-compatibility-check']);
  assert.equal(result.topics['vibe-backend'],1);
  assert.equal(result.actions.audit,3);
  assert.equal(result.actions.implement,3);
  assert.equal(result.actions.check,1);
});

test('no matches remains empty rather than silently dropping a filter', () => {
  assert.equal(engine.select(entries,state({q:'zzzz-no-workflow'})).matches.length,0);
  assert.equal(engine.select(entries,state({topic:'vibe-redis',action:'review'})).matches.length,0);
});

test('query and filters round-trip through a shared URL, including Unicode', () => {
  const input = state({q:'кэш API',topic:'vibe-cache',action:'check',full:true,page:2});
  assert.deepEqual(engine.readState(engine.searchParams(input),Object.keys(topics),Object.keys(actions)),input);
  const invalid = engine.readState('?q='+('a'.repeat(500))+'&topic=bad&action=bad&page=-1',Object.keys(topics),Object.keys(actions));
  assert.equal(invalid.q.length,240); assert.equal(invalid.topic,''); assert.equal(invalid.action,''); assert.equal(invalid.page,1);
  assert.equal(engine.readState('?page=Infinity',[],[]).page,1);
});

test('pagination has no duplicates, clamps stale pages and reports the actual range', () => {
  const result = engine.select(entries,state());
  const first = engine.paginate(result.matches,1), next = engine.paginate(result.matches,2), last = engine.paginate(result.matches,99999);
  assert.equal(first.items.length,12); assert.equal(next.from,13);
  assert.equal(new Set([...first.items,...next.items].map(x => x.entry.id)).size,24);
  assert.equal(last.total,241); assert.equal(last.to,241); assert.equal(last.page,21);
  assert.deepEqual(engine.paginate([],999),{items:[],page:1,pages:1,total:0,from:0,to:0});
});

test('catalog back links cannot become external redirects or arbitrary local paths', () => {
  const origin='https://arty-kk.github.io', base='/vibe-coding/';
  assert.equal(engine.safeReturn('/vibe-coding/ru/?q=API&topic=vibe-backend',origin,base),'/vibe-coding/ru/?q=API&topic=vibe-backend#catalog');
  for (const target of ['https://evil.test/vibe-coding/','//evil.test/','javascript:alert(1)','/unrelated/','/vibe-coding/workflows/api-audit/']) assert.equal(engine.safeReturn(target,origin,base),null,target);
});

test('site and offline ranking agree with Python for the judged query corpus', () => {
  const corpus = JSON.parse(fs.readFileSync(path.join(root,'review/search-cases-1.6.0.json')));
  const cases = [...corpus.cases, ...corpus.negative_cases,
    {query:'outbox',full_text:true}, {query:'API',skill:'vibe-backend',mode:'check'}];
  const {spawnSync} = require('node:child_process');
  const result = spawnSync('python3',[path.join(__dirname,'search_parity.py')], {input:JSON.stringify(cases),encoding:'utf8',maxBuffer:2_000_000});
  assert.equal(result.status,0,result.stderr);
  const python = JSON.parse(result.stdout);
  const bodies = Object.fromEntries(rows.map(row => [row.id,{body:fs.readFileSync(path.join(root,'plugins/vibe-coding',row.path),'utf8').replace(/\[([^\]]+)\]\([^)]+\)/g,'$1')}]));
  cases.forEach((row,index) => {
    const found = ids(engine.select(entries,state({q:row.query,topic:row.skill || '',action:row.mode || '',full:!!row.full_text}),bodies));
    assert.deepEqual(found,python[index],row.query);
  });
  assert.equal(fs.readFileSync(path.join(root,'site/catalog-engine.js'),'utf8'),
    fs.readFileSync(path.join(root,'plugins/vibe-coding/assets/catalog/engine.js'),'utf8'));
});

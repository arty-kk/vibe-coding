'use client';
import {useEffect, useRef, useState, type KeyboardEvent} from 'react';
import cases from '../lib/vibe/review-cases.json';
import {COPY, LANGUAGES, text, type Language, type UiCopy} from './copy';
import InstructionOutline from './outline';
import TopicCatalog from './catalog';

type Call = {name: string; arguments: Record<string, unknown>};
type RecordResult = {call: Call; response: any; status: number};
const reviewCases = [...cases.positive.map(value => ({...value, negative: false})),
  ...cases.negative.map(value => ({...value, negative: true}))];
let requestId = 0;

function supportsWorkflowResponse(version: string, minimum = [1, 6, 0]): boolean {
  const match = /^(\d+)\.(\d+)\.(\d+)(?:-([^+]+))?(?:\+.*)?$/.exec(version);
  if (!match) return false;
  const release = match.slice(1, 4).map(Number);
  for (let index = 0; index < minimum.length; index++) {
    if (release[index] !== minimum[index]) return release[index] > minimum[index];
  }
  return !match[4];
}

async function rpc(call: Call, version: string): Promise<RecordResult> {
  const response = await fetch('/library/mcp', {method: 'POST', headers: {
    'Content-Type': 'application/json', Accept: 'application/json, text/event-stream',
    'MCP-Protocol-Version': '2026-07-28', 'Mcp-Method': 'tools/call', 'Mcp-Name': call.name
  }, body: JSON.stringify({jsonrpc: '2.0', id: ++requestId, method: 'tools/call', params: {...call, _meta: {
    'io.modelcontextprotocol/protocolVersion': '2026-07-28',
    'io.modelcontextprotocol/clientInfo': {name: 'vibe-library-console', version},
    'io.modelcontextprotocol/clientCapabilities': {}
  }}})});
  return {call, response: await response.json(), status: response.status};
}

export function LanguageSwitcher({language}: {language: Language}) {
  const menu = useRef<HTMLDetailsElement>(null);
  function keydown(event: KeyboardEvent<HTMLDetailsElement>) {
    const links = [...(menu.current?.querySelectorAll('a') || [])];
    if (event.key === 'Escape') {
      if (menu.current) menu.current.open = false;
      menu.current?.querySelector('summary')?.focus();
    } else if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
      event.preventDefault();
      if (menu.current) menu.current.open = true;
      const index = links.indexOf(document.activeElement as HTMLAnchorElement);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? links.length - 1
        : event.key === 'ArrowDown' ? (index + 1) % links.length : (index - 1 + links.length) % links.length;
      links[next]?.focus();
    }
  }
  useEffect(() => {
    const close = (event: MouseEvent) => {if (menu.current && !menu.current.contains(event.target as Node)) menu.current.open = false;};
    document.addEventListener('click', close);
    return () => document.removeEventListener('click', close);
  }, []);
  return <details className="language-menu" ref={menu} onKeyDown={keydown} onBlur={event => {if (event.relatedTarget && !event.currentTarget.contains(event.relatedTarget as Node)) event.currentTarget.open = false;}}><summary>{LANGUAGES[language]}</summary><div className="languages">{(Object.keys(LANGUAGES) as Language[]).map(value => <a key={value} href={value === 'en' ? '/' : `/?lang=${value}`} lang={value} aria-current={language === value ? 'page' : undefined}>{LANGUAGES[value]}</a>)}</div></details>;
}

export function CopyEndpoint({endpoint, c}: {endpoint: string; c: UiCopy}) {
  const [status, setStatus] = useState('');
  async function copy() {
    try {await navigator.clipboard.writeText(endpoint); setStatus(c.copied);}
    catch {setStatus(c.copyFallback);}
  }
  return <div className="endpoint-action"><button type="button" onClick={() => void copy()}>{c.copy}</button><span role="status">{status}</span></div>;
}

export default function Demo({modes, language: interfaceLanguage, version}: {modes: string[]; language: Language; version: string}) {
  const c = COPY[interfaceLanguage];
  const [query, setQuery] = useState('MCP');
  const [language, setLanguage] = useState<Language>(interfaceLanguage);
  const [mode, setMode] = useState('');
  const [skill, setSkill] = useState('');
  const [topic, setTopic] = useState('');
  const [host, setHost] = useState('generic');
  const [full, setFull] = useState(false);
  const [records, setRecords] = useState<RecordResult[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<number | null>(null);
  const [scenario, setScenario] = useState('');
  const resultHeading = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    if (!busy && scenario) {
      resultHeading.current?.focus({preventScroll: true});
      resultHeading.current?.scrollIntoView({block: 'start'});
    }
  }, [busy, scenario]);

  function exampleLabel(index: number) {
    return index < cases.positive.length ? c.positiveLabels[index] || reviewCases[index].description
      : c.negativeLabels[index - cases.positive.length] || reviewCases[index].description;
  }
  async function run(calls: Call[], title: string, selectedCase: number | null = null) {
    setBusy(true); setError(''); setRecords([]); setScenario(title); setSelected(selectedCase);
    const search = calls.find(call => call.name === 'search_workflows')?.arguments;
    if (search) {
      setQuery(String(search.query || '')); setMode(String(search.mode || '')); setFull(!!search.full_text);
      setSkill(String(search.skill || '')); setTopic(String(search.topic || ''));
      setLanguage(Object.hasOwn(LANGUAGES, String(search.language)) ? search.language as Language : 'en');
    }
    const retrieval = calls.find(call => call.name === 'get_workflow')?.arguments;
    if (retrieval) setHost(['codex', 'claude'].includes(String(retrieval.host)) ? String(retrieval.host) : 'generic');
    try {
      const collected = [];
      for (const call of calls) {
        const request = {...call, arguments: {...call.arguments}};
        if (['search_workflows', 'get_workflow'].includes(call.name)) {
          if (supportsWorkflowResponse(version)) request.arguments.response_format = 'workflow';
          else delete request.arguments.response_format;
        }
        collected.push(await rpc(request, version));
        setRecords([...collected]);
      }
    } catch {setError(c.error);}
    finally {setBusy(false);}
  }
  const last = records.at(-1)?.response;
  const data = last?.result?.structuredContent;
  const rejected = !!last?.error || !!last?.result?.isError;
  const expectedRejection = selected !== null && reviewCases[selected].negative;
  const status = error || (busy ? c.loading : rejected ? expectedRejection ? c.expected : c.rejected : records.length ? c.response : '');
  const exampleButton = (index: number) => <button key={index} type="button" disabled={busy} aria-pressed={selected === index} onClick={() => void run(reviewCases[index].calls, exampleLabel(index), index)}>{exampleLabel(index)}</button>;
  const loadInstructions = (id: string, title: string, outlined = false) => void run([{name: 'get_workflow', arguments: {id, language, host, ...(outlined ? {intent: 'requested'} : {})}}], title);
  const canBrowseTopics = supportsWorkflowResponse(version, [1, 6, 1]);
  const browseTopics = (domain = '', title = c.topicCatalog) => void run([{name: 'search_workflows', arguments: {
    view: 'catalog', language, ...(domain ? {skill: domain} : {}), ...(mode ? {mode} : {})
  }}], title);
  const chooseTopic = (key: string, title: string) => void run([{name: 'search_workflows', arguments: {
    topic: key, language, ...(skill ? {skill} : {}), ...(mode ? {mode} : {})
  }}], title);
  const searchArguments = {query, language, ...(mode ? {mode} : {}), ...(skill ? {skill} : {}),
    ...(topic ? {topic} : {}), full_text: full};

  return <section className="demo" id="try-library" aria-labelledby="find-title">
    <div className="section-heading"><div><p className="eyebrow">{c.try}</p><h2 id="find-title">{c.find}</h2></div><span className="live">{c.public}</span></div>
    <form onSubmit={event => {event.preventDefault(); void run([{name: 'search_workflows', arguments: searchArguments}], c.catalogSearch);}}>
      <fieldset disabled={busy} className="search-grid">
        <label className="query">{c.keywords}<input maxLength={240} value={query} onChange={event => {setQuery(event.target.value); setSelected(null);}} placeholder={c.placeholder} aria-describedby="search-hint" /></label>
        <label className="select-field">{c.catalogLanguage}<select value={language} onChange={event => {setLanguage(event.target.value as Language); setSelected(null);}}>{(Object.keys(LANGUAGES) as Language[]).map(value => <option key={value} value={value}>{LANGUAGES[value]}</option>)}</select></label>
        <label className="select-field">{c.operation}<select value={mode} onChange={event => {setMode(event.target.value); setSelected(null);}}><option value="">{c.allOperations}</option>{modes.map(value => <option key={value} value={value}>{c.modeLabels[value] || value}</option>)}</select></label>
        <button disabled={busy} type="submit">{busy ? c.loading : c.search}</button>
        <label className="checkbox"><input type="checkbox" checked={full} onChange={event => {setFull(event.target.checked); setSelected(null);}} />{c.full}</label>
      </fieldset>
    </form>
    <p className="hint" id="search-hint">{c.hint}</p>
    {canBrowseTopics && <div className="catalog-actions">
      <button type="button" disabled={busy} onClick={() => browseTopics(skill)}>{c.browseTopics}</button>
      {topic && <span className="active-topic"><span>{c.selectedTopic}: </span><code>{topic}</code>
        <button type="button" disabled={busy} onClick={() => void run([{name: 'search_workflows',
          arguments: {query, language, ...(mode ? {mode} : {}), full_text: full}}], c.catalogSearch)}>{c.clearTopic}</button></span>}
    </div>}
    <div className="retrieval-options"><label className="select-field">{c.agent}<select value={host} disabled={busy} onChange={event => setHost(event.target.value)}><option value="generic">{c.genericHost}</option><option value="codex">Codex</option><option value="claude">Claude Code</option></select></label><p className="hint">{c.agentHint}</p></div>
    <div className="examples"><h3>{c.examples}</h3><div className="case-buttons">{cases.positive.map((_, index) => exampleButton(index))}</div><details className="validation-examples"><summary>{c.validations}</summary><div className="case-buttons">{cases.negative.map((_, index) => exampleButton(index + cases.positive.length))}</div></details></div>
    <div className="results" aria-busy={busy}>
      <p className={`result-status ${error || rejected && !expectedRejection ? 'error' : 'success'}`} role="status">{status}</p>
      {scenario && <h3 ref={resultHeading} tabIndex={-1}>{scenario}</h3>}
      {selected !== null && <details className="example-request"><summary>{c.examplePrompt}</summary><p>{reviewCases[selected].prompt}</p></details>}
      {records.length > 0 && <div className="request-summary">{records.map((record, index) => <span key={index}><code>{record.call.name}</code><b>HTTP {record.status}</b></span>)}</div>}
      {data?.catalog && <TopicCatalog catalog={data.catalog} c={c} busy={busy}
        onDomain={(key, title) => browseTopics(key, title)} onTopic={chooseTopic} onRoot={() => browseTopics()} />}
      {data?.workflows && !data?.catalog && <><p className="result-count">{text(c.searchCount, {total: data.total, count: data.workflows.length})}</p>{!data.workflows.length && <div className="empty"><p>{c.noResults}</p>{canBrowseTopics && <button type="button" disabled={busy} onClick={() => browseTopics(skill)}>{c.browseTopics}</button>}</div>}<div className="workflow-results">{data.workflows.map((row: any) => <article key={row.id}><div><span className="mode">{c.modeLabels[row.mode] || row.mode}</span><h3>{row.title}</h3><p>{row.summary}</p>{row.purpose && <p lang="en"><span className="metadata-label">{c.purpose}: </span>{row.purpose}</p>}{Array.isArray(row.match?.terms) && row.match.terms.length > 0 && <p className="match-terms">{c.matched}: {row.match.terms.join(', ')}</p>}<code>{row.id}</code></div><button disabled={busy} type="button" onClick={() => loadInstructions(row.id, row.title)}>{c.load}</button></article>)}</div></>}
      {data?.files && <div className="loaded"><p className="eyebrow">{c.loaded}</p><h3>{data.workflow.title}</h3><p>{c.files}: <b>{data.files.length}</b> · {c.words}: <b>{data.words}</b> · {c.instructionVersion} {data.instruction_version} · {data.instruction_language.toUpperCase()}</p><details><summary>{c.sourceFiles}</summary><ul>{data.files.map((file: any) => <li key={file.path}><a href={file.source_url}>{file.path}</a><code>{file.sha256.slice(0,16)}…</code></li>)}</ul></details><details><summary>{c.readRecipe}</summary><pre>{data.files.find((file: any) => file.path.endsWith(`/${data.workflow.id}.md`))?.text}</pre></details></div>}
      {data?.execution && <InstructionOutline execution={data.execution} c={c} busy={busy} onLoad={id => loadInstructions(id, id, true)} />}
      {typeof data?.suggested_action === 'string' && <p className="suggested-action"><span>{c.suggestedAction}: </span><span lang="en">{data.suggested_action}</span></p>}
      {rejected && <p className="rejection">{last.error?.message || last.result?.content?.find((item: any) => item.type === 'text')?.text}</p>}
      {records.length > 0 && <details className="raw"><summary>{c.raw}</summary><pre>{JSON.stringify(records, null, 2)}</pre></details>}
      {!scenario && <p className="empty">{c.empty}</p>}
    </div>
  </section>;
}

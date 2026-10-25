'use client';
import {useEffect, useRef, useState, type KeyboardEvent} from 'react';
import cases from '../lib/vibe/review-cases.json';
import {COPY, LANGUAGES, text, type Language, type UiCopy} from './copy';

type Call = {name: string; arguments: Record<string, unknown>};
type RecordResult = {call: Call; response: any; status: number};
const reviewCases = [...cases.positive.map(value => ({...value, negative: false})),
  ...cases.negative.map(value => ({...value, negative: true}))];
let requestId = 0;

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
  const [full, setFull] = useState(false);
  const [records, setRecords] = useState<RecordResult[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<number | null>(null);
  const [scenario, setScenario] = useState('');
  const resultHeading = useRef<HTMLHeadingElement>(null);

  useEffect(() => {if (!busy && scenario) resultHeading.current?.focus({preventScroll: true});}, [busy, scenario]);

  function exampleLabel(index: number) {
    return index < cases.positive.length ? c.positiveLabels[index] || reviewCases[index].description
      : c.negativeLabels[index - cases.positive.length] || reviewCases[index].description;
  }
  async function run(calls: Call[], title: string, selectedCase: number | null = null) {
    setBusy(true); setError(''); setRecords([]); setScenario(title); setSelected(selectedCase);
    const search = calls.find(call => call.name === 'search_workflows')?.arguments;
    if (search) {
      setQuery(String(search.query || '')); setMode(String(search.mode || '')); setFull(!!search.full_text);
      setLanguage(Object.hasOwn(LANGUAGES, String(search.language)) ? search.language as Language : 'en');
    }
    try {
      const collected = [];
      for (const call of calls) {
        collected.push(await rpc(call, version));
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

  return <section className="demo" id="try-library" aria-labelledby="find-title">
    <div className="section-heading"><div><p className="eyebrow">{c.try}</p><h2 id="find-title">{c.find}</h2></div><span className="live">{c.public}</span></div>
    <form onSubmit={event => {event.preventDefault(); void run([{name: 'search_workflows', arguments: {query, language, ...(mode ? {mode} : {}), full_text: full}}], c.catalogSearch);}}>
      <fieldset disabled={busy} className="search-grid">
        <label className="query">{c.keywords}<input maxLength={160} value={query} onChange={event => {setQuery(event.target.value); setSelected(null);}} placeholder={c.placeholder} aria-describedby="search-hint" /></label>
        <label className="select-field">{c.catalogLanguage}<select value={language} onChange={event => {setLanguage(event.target.value as Language); setSelected(null);}}>{(Object.keys(LANGUAGES) as Language[]).map(value => <option key={value} value={value}>{LANGUAGES[value]}</option>)}</select></label>
        <label className="select-field">{c.operation}<select value={mode} onChange={event => {setMode(event.target.value); setSelected(null);}}><option value="">{c.allOperations}</option>{modes.map(value => <option key={value} value={value}>{c.modeLabels[value] || value}</option>)}</select></label>
        <button disabled={busy} type="submit">{busy ? c.loading : c.search}</button>
        <label className="checkbox"><input type="checkbox" checked={full} onChange={event => {setFull(event.target.checked); setSelected(null);}} />{c.full}</label>
      </fieldset>
    </form>
    <p className="hint" id="search-hint">{c.hint}</p>
    <div className="examples"><h3>{c.examples}</h3><div className="case-buttons">{cases.positive.map((_, index) => exampleButton(index))}</div><details className="validation-examples"><summary>{c.validations}</summary><div className="case-buttons">{cases.negative.map((_, index) => exampleButton(index + cases.positive.length))}</div></details></div>
    <div className="results" aria-busy={busy}>
      <p className={`result-status ${error || rejected && !expectedRejection ? 'error' : 'success'}`} role="status">{status}</p>
      {scenario && <h3 ref={resultHeading} tabIndex={-1}>{scenario}</h3>}
      {selected !== null && <details className="example-request"><summary>{c.examplePrompt}</summary><p>{reviewCases[selected].prompt}</p></details>}
      {records.length > 0 && <div className="request-summary">{records.map((record, index) => <span key={index}><code>{record.call.name}</code><b>HTTP {record.status}</b></span>)}</div>}
      {data?.workflows && <><p className="result-count">{text(c.searchCount, {total: data.total, count: data.workflows.length})}</p>{!data.workflows.length && <p className="empty">{c.noResults}</p>}<div className="workflow-results">{data.workflows.map((row: any) => <article key={row.id}><div><span className="mode">{c.modeLabels[row.mode] || row.mode}</span><h3>{row.title}</h3><p>{row.summary}</p><code>{row.id}</code></div><button disabled={busy} type="button" onClick={() => void run([{name: 'get_workflow', arguments: {id: row.id, language}}], row.title)}>{c.load}</button></article>)}</div></>}
      {data?.files && <div className="loaded"><p className="eyebrow">{c.loaded}</p><h3>{data.workflow.title}</h3><p>{c.files}: <b>{data.files.length}</b> · {c.words}: <b>{data.words}</b> · {c.instructionVersion} {data.instruction_version} · {data.instruction_language.toUpperCase()}</p><details><summary>{c.sourceFiles}</summary><ul>{data.files.map((file: any) => <li key={file.path}><a href={file.source_url}>{file.path}</a><code>{file.sha256.slice(0,16)}…</code></li>)}</ul></details><details><summary>{c.readRecipe}</summary><pre>{data.files.find((file: any) => file.path.endsWith(`/${data.workflow.id}.md`))?.text}</pre></details></div>}
      {rejected && <p className="rejection">{last.error?.message || last.result?.content?.find((item: any) => item.type === 'text')?.text}</p>}
      {records.length > 0 && <details className="raw"><summary>{c.raw}</summary><pre>{JSON.stringify(records, null, 2)}</pre></details>}
      {!scenario && <p className="empty">{c.empty}</p>}
    </div>
  </section>;
}

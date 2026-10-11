'use client';
import {useState} from 'react';
import cases from '../lib/vibe/review-cases.json';

type Call = {name: string; arguments: Record<string, unknown>};
type RecordResult = {call: Call; response: any; status: number};
const reviewCases = [...cases.positive.map((value, index) => ({...value, label: `Positive ${index + 1}`, negative: false})),
  ...cases.negative.map((value, index) => ({...value, label: `Negative ${index + 1}`, negative: true}))];
let requestId = 0;

async function rpc(call: Call): Promise<RecordResult> {
  const response = await fetch('/library/mcp', {method: 'POST', headers: {
    'Content-Type': 'application/json', Accept: 'application/json, text/event-stream',
    'MCP-Protocol-Version': '2026-07-28', 'Mcp-Method': 'tools/call', 'Mcp-Name': call.name
  }, body: JSON.stringify({jsonrpc: '2.0', id: ++requestId, method: 'tools/call', params: {...call, _meta: {
    'io.modelcontextprotocol/protocolVersion': '2026-07-28',
    'io.modelcontextprotocol/clientInfo': {name: 'vibe-library-console', version: '1.5.0'},
    'io.modelcontextprotocol/clientCapabilities': {}
  }}})});
  return {call, response: await response.json(), status: response.status};
}

export default function Demo({modes}: {modes: string[]}) {
  const [query, setQuery] = useState('MCP');
  const [language, setLanguage] = useState('en');
  const [mode, setMode] = useState('');
  const [full, setFull] = useState(false);
  const [records, setRecords] = useState<RecordResult[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<number | null>(null);
  const [scenario, setScenario] = useState('');

  async function run(calls: Call[], title: string, selectedCase: number | null = null) {
    setBusy(true); setError(''); setRecords([]); setScenario(title); setSelected(selectedCase);
    try {
      const collected = [];
      for (const call of calls) {
        collected.push(await rpc(call));
        setRecords([...collected]);
      }
    } catch {setError('The server could not be reached. Try again.');}
    finally {setBusy(false);}
  }
  const last = records.at(-1)?.response;
  const data = last?.result?.structuredContent;
  const rejected = !!last?.error || !!last?.result?.isError;
  const expectedRejection = selected !== null && reviewCases[selected].negative;

  return <section className="demo" id="try-library">
    <div className="section-heading"><div><p className="eyebrow">TRY THE LIVE SERVER</p><h2>Find your next workflow</h2></div><span className="live">LIVE MCP</span></div>
    <form onSubmit={event => {event.preventDefault(); void run([{name: 'search_workflows', arguments: {query, language, ...(mode ? {mode} : {}), full_text: full}}], 'Catalog search');}}>
      <label className="query">Technical keywords<input maxLength={160} value={query} onChange={event => setQuery(event.target.value)} placeholder="SQL, MCP, cache, API…" /></label>
      <label>Catalog language<select value={language} onChange={event => setLanguage(event.target.value)}><option value="en">English</option><option value="es">Español</option><option value="ru">Русский</option><option value="zh-CN">简体中文</option></select></label>
      <label>Operation<select value={mode} onChange={event => setMode(event.target.value)}><option value="">All operations</option>{modes.map(value => <option key={value}>{value}</option>)}</select></label>
      <button disabled={busy} type="submit">{busy ? 'Loading…' : 'Search workflows'}</button>
      <label className="checkbox"><input type="checkbox" checked={full} onChange={event => setFull(event.target.checked)} /> Include instruction bodies</label>
    </form>
    <p className="hint">Use technical keywords. Do not enter source code, credentials or personal data.</p>
    <div className="review"><p className="eyebrow">EXAMPLE SCENARIOS</p><div className="case-buttons">{reviewCases.map((value, index) => <button key={index} disabled={busy} className={selected === index ? 'active' : ''} onClick={() => void run(value.calls, value.prompt, index)}>{value.label}</button>)}</div></div>
    <div className="results" aria-live="polite" aria-busy={busy}>
      {error && <p className="error">{error}</p>}
      {scenario && <h3>{scenario}</h3>}
      {records.length > 0 && <div className="request-summary">{records.map((record, index) => <span key={index}>{record.call.name} <b>HTTP {record.status}</b></span>)}<strong className={rejected && !expectedRejection ? 'error' : 'success'}>{rejected ? 'Request rejected' : busy ? 'Loading…' : 'Response received'}</strong></div>}
      {data?.workflows && <><p>{data.total} matching workflows · Showing {data.workflows.length}</p><div className="workflow-results">{data.workflows.map((row: any) => <article key={row.id}><div><span className="mode">{row.mode}</span><h3>{row.title}</h3><p>{row.summary}</p><code>{row.id}</code></div><button disabled={busy} onClick={() => void run([{name: 'get_workflow', arguments: {id: row.id, language}}], row.title)}>Load workflow</button></article>)}</div></>}
      {data?.files && <div className="loaded"><p className="eyebrow">WORKFLOW LOADED</p><h3>{data.workflow.title}</h3><p><b>{data.files.length}</b> instruction files · <b>{data.words}</b> words · Instructions {data.instruction_version} · {data.instruction_language.toUpperCase()}</p><ul>{data.files.map((file: any) => <li key={file.path}><a href={file.source_url}>{file.path}</a><code>{file.sha256.slice(0,16)}…</code></li>)}</ul><details><summary>Read the selected recipe</summary><pre>{data.files.find((file: any) => file.path.endsWith(`/${data.workflow.id}.md`))?.text}</pre></details></div>}
      {rejected && <p className="rejection">{last.error?.message || last.result?.content?.find((item: any) => item.type === 'text')?.text}</p>}
      {records.length > 0 && <details className="raw"><summary>View the actual MCP requests and responses</summary><pre>{JSON.stringify(records, null, 2)}</pre></details>}
      {!scenario && <p className="empty">Search the catalog or run an example to see the server response.</p>}
    </div>
  </section>;
}

import {libraryStatus, MODES} from '../lib/vibe/library.js';
import Demo from './demo';

export default function Home() {
  const status = libraryStatus();
  return <main>
    <nav><a className="brand" href="/">Vibe Coding <span>Library</span></a><a href="https://arty-kk.github.io/vibe-coding/">Browse the catalog ↗</a></nav>
    <section className="intro"><p className="eyebrow">PUBLIC ENGINEERING LIBRARY · MCP</p>
      <h1>The right workflow.<br/>Only the context you need.</h1>
      <p className="lead">Search {status.workflows} engineering workflows, then load the selected recipe and its working contract. Built for Codex, Claude Code and other MCP clients.</p>
      <div className="facts"><span><b>{status.workflows}</b> workflows</span><span><b>{status.skills}</b> skills in the source library</span><span><b>4</b> catalog languages</span></div>
    </section>
    <section className="connection"><div><p className="eyebrow">CONNECT YOUR MCP CLIENT</p><code>https://vibe-coding-library.swift-seal-1081.chatgpt.site/library/mcp</code></div>
      <p>Streamable HTTP · No account or API key required · Read-only public guidance</p></section>
    <Demo modes={MODES} />
    <section className="about"><h2>What gets loaded?</h2><p>One selected workflow, its domain skill, the shared working contract and directly required references. Host guidance is included when requested. Search results contain titles and summaries; full instructions are loaded separately.</p><p>The catalog supports English, Spanish, Russian and Simplified Chinese. Technical instructions remain in English. The server cannot inspect or modify a repository; your coding agent applies the guidance using its existing tools and permissions.</p></section>
    <footer><span>Service {status.version} · Instructions {status.instruction_version}</span><a href="https://github.com/arty-kk/vibe-coding">Source</a><a href="https://github.com/arty-kk/vibe-coding/issues">Support</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></footer>
  </main>;
}

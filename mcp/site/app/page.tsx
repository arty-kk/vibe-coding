import type {Metadata} from 'next';
import {libraryStatus, MODES} from '../lib/vibe/library.js';
import Demo, {CopyEndpoint, LanguageSwitcher} from './demo';
import {COPY, LANGUAGES, text, type Language} from './copy';

type PageProps = {searchParams: Promise<{lang?: string}>};
const endpoint = 'https://vibe-coding-library.swift-seal-1081.chatgpt.site/library/mcp';
const languageFor = (value?: string): Language => value && Object.hasOwn(LANGUAGES, value) ? value as Language : 'en';

export async function generateMetadata({searchParams}: PageProps): Promise<Metadata> {
  const language = languageFor((await searchParams).lang);
  const c = COPY[language];
  return {title: c.title, description: text(c.description, {count: libraryStatus().workflows}), alternates: {canonical: '/'}};
}

export default async function Home({searchParams}: PageProps) {
  const status = libraryStatus();
  const language = languageFor((await searchParams).lang);
  const c = COPY[language];
  const catalog = `https://arty-kk.github.io/vibe-coding/${language === 'en' ? '' : language + '/'}`;
  return <main id="content" lang={language}>
    <a className="skip" href="#try-library">{c.skip}</a>
    <nav className="site-nav" aria-label="Vibe Coding Library">
      <a className="brand" href="/">Vibe Coding <span>Library</span></a>
      <div className="nav-actions"><a className="catalog-link" href={catalog}>{c.browse} ↗</a><LanguageSwitcher language={language} /></div>
    </nav>
    <section className="intro"><p className="eyebrow">{text(c.eyebrow, {version: status.version})}</p>
      <h1>{c.headline}<br/><span>{c.accent}</span></h1>
      <p className="lead">{c.lead}</p>
      <div className="facts"><span><b>{status.workflows}</b> {c.workflows}</span><span><b>2</b> {c.tools}</span><span><b>4</b> {c.languages}</span></div>
    </section>
    <section className="connection" aria-labelledby="connect-title"><div><h2 className="eyebrow" id="connect-title">{c.connect}</h2><code>{endpoint}</code><p>{c.connection}</p></div><CopyEndpoint endpoint={endpoint} c={c} /></section>
    <Demo modes={MODES} language={language} version={status.version} />
    <section className="about"><h2>{c.aboutTitle}</h2><div className="tool-grid"><article><h3><code>search_workflows</code></h3><p>{c.searchAbout}</p></article><article><h3><code>get_workflow</code></h3><p>{c.getAbout}</p></article></div><p>{c.about}</p><p>{text(c.offline, {skills: status.skills})} <a href="https://github.com/arty-kk/vibe-coding/blob/main/plugins/vibe-coding/docs/INSTALL.md">{c.offlineLink} →</a></p><a className="setup-link" href="https://github.com/arty-kk/vibe-coding/blob/main/plugins/vibe-coding-library/README.md">{c.setup} →</a></section>
    <footer><span>{c.service} {status.version} · {c.instructionVersion} {status.instruction_version}</span><a href="https://github.com/arty-kk/vibe-coding">{c.source}</a><a href="https://github.com/arty-kk/vibe-coding/issues">{c.support}</a><a href="/privacy">{c.privacy}</a><a href="/terms">{c.terms}</a></footer>
  </main>;
}

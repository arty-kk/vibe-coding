import {text, type UiCopy} from './copy';

type Domain = {key: string; title: string; keywords: string[]; topic_count: number; workflow_count: number};
type Topic = {key: string; title: string; keywords: string[]; modes: string[]; workflow_ids: string[]};
export type Catalog = {level: 'domains' | 'topics'; status: string; keyword_language: string; domains: Domain[]; topics: Topic[]};

export default function TopicCatalog({catalog, c, busy, onDomain, onTopic, onRoot}: {
  catalog: Catalog; c: UiCopy; busy: boolean;
  onDomain: (key: string, title: string) => void; onTopic: (key: string, title: string) => void; onRoot: () => void;
}) {
  return <section className="topic-catalog" aria-label={c.topicCatalog}>
    {catalog.level === 'topics' && <div className="catalog-heading">
      <button type="button" disabled={busy} onClick={onRoot}>{c.allDomains}</button>
    </div>}
    <p className="hint">{c.catalogHint}</p>
    {catalog.status !== 'ok' && <p className="hint">{c.catalogRecovery}</p>}
    <div className="catalog-options">
      {catalog.domains.map(domain => <button type="button" className="catalog-option" key={domain.key}
        disabled={busy} onClick={() => onDomain(domain.key, domain.title)}>
        <strong>{domain.title}</strong><code>{domain.key}</code>
        <span lang="en">{domain.keywords.join(' · ')}</span>
        <small>{text(c.catalogCounts, {topics: domain.topic_count, workflows: domain.workflow_count})}</small>
      </button>)}
      {catalog.topics.map(topic => <button type="button" className="catalog-option" key={topic.key}
        disabled={busy} onClick={() => onTopic(topic.key, topic.title)}>
        <strong>{topic.title}</strong><code>{topic.key}</code>
        <span lang="en">{topic.keywords.join(' · ')}</span>
        <small>{topic.modes.map(mode => c.modeLabels[mode] || mode).join(' · ')}</small>
      </button>)}
    </div>
    {!catalog.domains.length && !catalog.topics.length && <p>{c.catalogEmpty}</p>}
  </section>;
}

export function createDiscovery(library) {
  const byId = new Map(library.recipes.map(row => [row.id, row]));
  const byTopic = new Map(library.discovery.topics.map(topic => [topic.key, topic]));
  const members = topic => topic.recipe_ids.map(id => byId.get(id));
  const fits = (row, skill, mode) => (!skill || row.skill === skill) && (!mode || row.mode === mode);

  function catalog({skill, mode, topic, language = 'en'} = {}) {
    const locale = library.locales[language];
    const selected = topic ? byTopic.get(topic) : null;
    const unknown = !!topic && !selected;
    const domainRecords = library.discovery.domains.map(domain => {
      const rows = library.recipes.filter(row => row.skill === domain.key && fits(row, skill, mode));
      const topics = library.discovery.topics.filter(item => item.skill === domain.key && members(item).some(row => fits(row, skill, mode)));
      return {key: domain.key, title: locale.categories[domain.key], keywords: domain.keywords,
        topic_count: topics.length, workflow_count: rows.length};
    }).filter(domain => domain.workflow_count > 0);
    const hasSelectedResults = selected && members(selected).some(row => fits(row, skill, mode));
    const topicRecords = library.discovery.topics
      .filter(item => (!skill || item.skill === skill) && (!selected || !hasSelectedResults || item.key === selected.key))
      .map(item => {
        const rows = members(item).filter(row => fits(row, skill, mode));
        const representative = rows[0];
        return {key: item.key, skill: item.skill, title: representative ? locale.titles[representative.id] : '',
          keywords: item.keywords, modes: [...new Set(rows.map(row => row.mode))],
          workflow_ids: rows.map(row => row.id)};
      }).filter(item => item.workflow_ids.length > 0);
    const level = skill || selected ? 'topics' : 'domains';
    const empty = level === 'domains' ? !domainRecords.length : !topicRecords.length;
    return {level, status: unknown ? 'unknown_topic' : selected && !hasSelectedResults ? 'scope_conflict' : empty ? 'empty_scope' : 'ok',
      keyword_language: 'en', domains: level === 'domains' || unknown ? domainRecords : [],
      topics: level === 'topics' || unknown && skill ? topicRecords : []};
  }
  return {byTopic, catalog};
}

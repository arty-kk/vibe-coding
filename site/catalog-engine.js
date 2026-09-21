'use strict';
(() => {
  const fold = value => String(value ?? '').normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
  const words = value => fold(value).match(/[\p{L}\p{N}+#]+/gu) || [];
  const contains = (haystack, term) => /[\u3400-\u9fff]/u.test(term)
    ? haystack.some(word => word.includes(term))
    : haystack.some(word => word === term || (term.length >= 3 && word.startsWith(term)));

  function prepare(entries, topics, actions) {
    return entries.map((entry, order) => ({...entry, order,
      titleWords: words(entry.titles.join(' ')),
      keywordWords: words([entry.id, ...(entry.keywords || [])].join(' ')),
      topicWords: words((topics[entry.skill] || []).join(' ')),
      actionWords: words((actions[entry.mode] || []).join(' '))
    }));
  }

  function score(entry, query, bodies) {
    const terms = words(query);
    if (!terms.length) return {score: 0, bodyOnly: false};
    let total = 0, bodyOnly = false;
    for (const term of terms) {
      if (contains(entry.titleWords, term)) total += 40;
      else if (contains(entry.keywordWords, term)) total += 20;
      else if (contains(entry.topicWords, term)) total += 8;
      else if (contains(entry.actionWords, term)) total += 4;
      else if (bodies && contains(words(bodies[entry.id]?.body || ''), term)) { total += 1; bodyOnly = true; }
      else return null;
    }
    const phrase = words(query).join(' ');
    if (entry.titles.some(title => words(title).join(' ') === phrase)) total += 200;
    return {score: total, bodyOnly};
  }

  function select(entries, state, bodies) {
    const candidates = entries.map(entry => ({entry, match: score(entry, state.q, state.full ? bodies : null)}))
      .filter(item => item.match !== null);
    const topics = {}, actions = {};
    for (const {entry} of candidates) {
      if (!state.action || entry.mode === state.action) topics[entry.skill] = (topics[entry.skill] || 0) + 1;
      if (!state.topic || entry.skill === state.topic) actions[entry.mode] = (actions[entry.mode] || 0) + 1;
    }
    const matches = candidates.filter(({entry}) => (!state.topic || entry.skill === state.topic) && (!state.action || entry.mode === state.action))
      .sort((a, b) => b.match.score - a.match.score || a.entry.order - b.entry.order);
    return {matches, topics, actions};
  }

  function readState(search, topics, actions) {
    const params = new URLSearchParams(search);
    const topic = params.get('topic') || params.get('category') || '';
    const action = params.get('action') || params.get('mode') || '';
    const page = Number(params.get('page'));
    return {q: (params.get('q') || '').slice(0, 160),
      topic: topics.includes(topic) ? topic : '', action: actions.includes(action) ? action : '',
      full: params.get('full') === '1', page: Number.isSafeInteger(page) && page > 0 ? page : 1};
  }

  function searchParams(state) {
    const params = new URLSearchParams();
    if (state.q.trim()) params.set('q', state.q.trim());
    if (state.topic) params.set('topic', state.topic);
    if (state.action) params.set('action', state.action);
    if (state.full) params.set('full', '1');
    if (state.page > 1) params.set('page', String(state.page));
    return params.toString();
  }

  function paginate(matches, requested, size = 12) {
    const pages = Math.max(1, Math.ceil(matches.length / size));
    const page = Math.min(Math.max(1, requested), pages);
    const start = (page - 1) * size;
    return {items: matches.slice(start, start + size), page, pages, total: matches.length, from: matches.length ? start + 1 : 0, to: Math.min(start + size, matches.length)};
  }

  function safeReturn(value, origin, base) {
    if (!value || value.length > 2400) return null;
    try {
      const url = new URL(value, origin);
      const routes = ['', 'es/', 'ru/', 'zh-CN/'].map(route => base + route);
      return url.origin === origin && routes.includes(url.pathname) ? url.pathname + url.search + '#catalog' : null;
    } catch { return null; }
  }

  const engine = {fold, words, prepare, select, readState, searchParams, paginate, safeReturn};
  if (typeof module !== 'undefined' && module.exports) module.exports = engine;
  else window.VibeCatalog = engine;
})();

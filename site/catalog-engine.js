'use strict';
(() => {
  const fold = value => String(value ?? '').normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
  const words = value => fold(value).match(/[\p{L}\p{N}+#]+/gu) || [];
  const compact = value => fold(value).replace(/[^\p{L}\p{N}+#]/gu, '');
  const escape = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const cjk = value => /[\u3400-\u9fff]/u.test(value);
  const contains = (haystack, term) => cjk(term)
    ? haystack.some(word => word.includes(term))
    : haystack.some(word => word === term || (term.length >= 3 && word.startsWith(term)));
  const compiled = new WeakMap(), bodyCache = new WeakMap();

  function oneEdit(a, b) {
    if (Math.abs(a.length - b.length) > 1) return false;
    if (a === b) return true;
    let i = 0;
    while (i < Math.min(a.length, b.length) && a[i] === b[i]) i++;
    if (a.length === b.length) return a.slice(i + 1) === b.slice(i + 1)
      || i + 1 < a.length && a[i] === b[i + 1] && a[i + 1] === b[i]
        && a.slice(i + 2) === b.slice(i + 2);
    return a.length > b.length ? a.slice(i + 1) === b.slice(i) : a.slice(i) === b.slice(i + 1);
  }

  function typoCorrector(rules, entries) {
    const forms = new Set(Object.values(rules.lexicon.terms || {}).flat()
      .concat(Object.keys(rules.lexicon.terms || {}), Object.values(rules.lexicon.intents || {}).flat()));
    for (const entry of entries) {
      for (const text of [entry.id, entry.skill, ...entry.titles, ...(entry.keywords || [])]) {
        for (const word of words(text)) forms.add(word);
      }
    }
    const exact = new Set([...forms].flatMap(words).concat([...rules.stops]));
    const deletions = new Map(), signature = word => rules.signature(word);
    for (const word of exact) {
      if (rules.stops.has(word) || word.length < 5 || word.length > 48 || cjk(word) || !/^\p{L}+$/u.test(word)) continue;
      for (let i = 0; i < word.length; i++) {
        const key = word.slice(0, i) + word.slice(i + 1);
        if (!deletions.has(key)) deletions.set(key, new Set());
        deletions.get(key).add(word);
      }
    }
    return value => fold(value).replace(/[\p{L}\p{N}+#]+/gu, word => {
      if (exact.has(word) || word.length < 5 || word.length > 48 || cjk(word) || !/^\p{L}+$/u.test(word)) return word;
      const candidates = new Set(deletions.get(word) || []);
      for (let i = 0; i < word.length; i++) {
        const key = word.slice(0, i) + word.slice(i + 1);
        if (exact.has(key) && !rules.stops.has(key)) candidates.add(key);
        for (const item of deletions.get(key) || []) candidates.add(item);
      }
      const matches = [...candidates].filter(item => item.length >= 5 && item[0] === word[0] && oneEdit(word, item));
      if (!matches.length || new Set(matches.map(signature)).size !== 1) return word;
      return matches.sort()[0];
    });
  }

  function replacer(groups) {
    const table = new Map();
    for (const [target, variants] of Object.entries(groups || {})) {
      for (const value of [target, ...variants]) table.set(fold(value), target);
    }
    const variants = [...table.keys()].sort((a, b) => b.length - a.length || a.localeCompare(b));
    if (!variants.length) return value => value;
    const pattern = new RegExp(variants.map(value => cjk(value) ? escape(value)
      : '(?<![\\p{L}\\p{N}])' + escape(value) + '(?![\\p{L}\\p{N}])').join('|'), 'gu');
    return value => value.replace(pattern, match => ' ' + table.get(match) + ' ');
  }

  function rulesFor(lexicon) {
    if (!compiled.has(lexicon)) {
      const concepts = replacer(lexicon.terms);
      const intents = replacer(Object.fromEntries(Object.entries(lexicon.intents || {}).map(([mode, values]) => ['intent_' + mode, values])));
      const stops = new Set((lexicon.stopwords || []).map(fold));
      // CJK filler removal is exact phrase replacement, not an unrestricted stemmer.
      const cleanCjk = text => {
        for (const stop of [...stops].filter(cjk).sort((a, b) => b.length - a.length)) text = text.replaceAll(stop, ' ');
        return text;
      };
      compiled.set(lexicon, {lexicon, stops,
        signature: value => intents(concepts(fold(value))).trim(),
        tokens: value => words(concepts(fold(value))),
        query: (value, correct) => {
          const text = intents(concepts(correct ? correct(value) : fold(value)));
          const hints = [...text.matchAll(/intent_([a-z]+)/g)].map(match => match[1]);
          const terms = words(cleanCjk(text.replace(/intent_[a-z]+/g, ' '))).filter(term => !stops.has(term));
          return {terms: [...new Set(terms)], hints: [...new Set(hints)]};
        }});
    }
    return compiled.get(lexicon);
  }

  function prepare(entries, topics, actions, lexicon = {}) {
    const base = rulesFor(lexicon);
    const correct = typoCorrector(base, entries);
    const rules = {...base, query: value => base.query(value, correct)};
    return entries.map((entry, order) => ({...entry, order, rules,
      titleWords: rules.tokens(entry.titles.join(' ')),
      subjects: (entry.primary_keywords || []).map(value => rules.tokens(value)),
      keywordWords: rules.tokens([entry.id, entry.skill, entry.purpose || '', ...(entry.keywords || []),
        ...(lexicon.discovery?.[entry.id] || [])].join(' ')),
      topicWords: rules.tokens((topics[entry.skill] || []).join(' ')),
      actionWords: rules.tokens([entry.mode, ...(actions[entry.mode] || [])].join(' ')),
      exactId: compact(entry.id),
      exactTitles: entry.titles.map(compact),
      exactAliases: (lexicon.aliases?.[entry.id] || []).map(compact)
    }));
  }

  function bodyWords(entry, bodies) {
    if (!bodyCache.has(bodies)) bodyCache.set(bodies, new Map());
    const cache = bodyCache.get(bodies);
    if (!cache.has(entry.id)) cache.set(entry.id, entry.rules.tokens(bodies[entry.id]?.body || ''));
    return cache.get(entry.id);
  }

  function score(entry, query, analysis, bodies) {
    const key = analysis.key;
    const exact = key && (key === entry.exactId ? 'exact_id'
      : entry.exactTitles.includes(key) ? 'exact_title' : entry.exactAliases.includes(key) ? 'alias' : null);
    if (exact) return {score: exact === 'exact_id' ? 20000 : 15000, bodyOnly: false, kind: exact, terms: analysis.terms};
    let total = 0, bodyOnly = false;
    for (const term of analysis.terms) {
      if (entry.subjects.some(subject => contains(subject, term)
        && subject.every(part => analysis.terms.some(queryTerm => contains([part], queryTerm))))) total += 60;
      else if (contains(entry.titleWords, term)) total += 40;
      else if (contains(entry.keywordWords, term)) total += 20;
      else if (contains(entry.topicWords, term)) total += 8;
      else if (bodies && contains(bodyWords(entry, bodies), term)) {total += 1; bodyOnly = true;}
      else return null;
    }
    if (analysis.hints.includes(entry.mode)) total += 35;
    if (bodyOnly) total -= 1000;
    return {score: total, bodyOnly, kind: bodyOnly ? 'instruction_body' : query.trim() ? 'catalog' : 'browse', terms: analysis.terms};
  }

  function select(entries, state, bodies) {
    const query = state.q || '';
    const analysis = entries[0]?.rules.query(query) || {terms: words(query), hints: []};
    analysis.key = compact(query);
    const candidates = entries.map(entry => ({entry, match: score(entry, query, analysis, state.full ? bodies : null)}))
      .filter(item => item.match !== null);
    const topics = {}, actions = {};
    for (const {entry} of candidates) {
      if (!state.action || entry.mode === state.action) topics[entry.skill] = (topics[entry.skill] || 0) + 1;
      if (!state.topic || entry.skill === state.topic) actions[entry.mode] = (actions[entry.mode] || 0) + 1;
    }
    const matches = candidates.filter(({entry}) => (!state.topic || entry.skill === state.topic) && (!state.action || entry.mode === state.action))
      .sort((a, b) => b.match.score - a.match.score || (query.trim()
        ? Number(a.entry.mode !== 'audit') - Number(b.entry.mode !== 'audit') || a.entry.id.localeCompare(b.entry.id)
        : a.entry.order - b.entry.order));
    return {matches, topics, actions};
  }

  function readState(search, topics, actions) {
    const params = new URLSearchParams(search);
    const topic = params.get('topic') || params.get('category') || '';
    const action = params.get('action') || params.get('mode') || '';
    const page = Number(params.get('page'));
    return {q: (params.get('q') || '').slice(0, 240),
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
    return {items: matches.slice(start, start + size), page, pages, total: matches.length,
      from: matches.length ? start + 1 : 0, to: Math.min(start + size, matches.length)};
  }

  function safeReturn(value, origin, base) {
    if (!value || value.length > 2400) return null;
    try {
      const url = new URL(value, origin);
      const routes = ['', 'es/', 'ru/', 'zh-CN/'].map(route => base + route);
      return url.origin === origin && routes.includes(url.pathname) ? url.pathname + url.search + '#catalog' : null;
    } catch {return null;}
  }

  const engine = {fold, words, prepare, select, readState, searchParams, paginate, safeReturn};
  if (typeof module !== 'undefined' && module.exports) module.exports = engine;
  else window.VibeCatalog = engine;
})();

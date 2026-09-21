'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const engine = window.VibeCatalog;
  const base = document.body.dataset.base;
  const languages = ['en', 'es', 'ru', 'zh-CN'];
  const current = document.body.dataset.language;
  const page = document.body.dataset.page;
  const url = new URL(location.href);
  const requested = url.searchParams.get('lang') === 'zh' ? 'zh-CN' : url.searchParams.get('lang');
  const saved = key => { try { return localStorage.getItem(key); } catch { return null; } };
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch {} };
  const format = (text, values) => text.replace(/\{(\w+)\}/g, (match, key) => values[key] ?? match);
  // Keep crawlable links canonical. Attach optional navigation context only when
  // a visitor follows or copies a link, including middle-click and context menus.
  function contextualLink(link, destination) {
    link.dataset.navigation = destination;
    if (link.dataset.canonical) {
      link.href = link.dataset.canonical;
      return;
    }
    link.dataset.canonical = link.getAttribute('href');
    for (const type of ['click', 'auxclick', 'contextmenu']) {
      link.addEventListener(type, () => { link.href = link.dataset.navigation; });
    }
  }
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); return true; } catch { return false; }
  }
  if (page !== 'workflow' && languages.includes(requested)) {
    url.pathname = base + (requested === 'en' ? '' : requested + '/') + (page === 'directory' ? 'workflows/' : page.endsWith('.html') ? page : '');
    url.searchParams.delete('lang'); location.replace(url.href); return;
  }
  const languageMenu = document.querySelector('.language-menu');
  document.addEventListener('click', event => {
    if (languageMenu && !languageMenu.contains(event.target)) languageMenu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && languageMenu?.open) {
      languageMenu.open = false; languageMenu.querySelector('summary').focus();
    }
  });
  if ($('demo-host')) {
    const host = $('demo-host'), prompt = $('demo-prompt');
    host.value = saved('vibe-coding-host') === 'claude' ? 'claude' : 'codex';
    const update = () => {
      prompt.textContent = (host.value === 'claude' ? '/vibe-coding:vibe-review' : '$vibe-review') + '\n' + prompt.dataset.task;
      prompt.parentElement.parentElement.querySelector('[role="status"]').textContent = '';
    };
    host.addEventListener('change', () => { save('vibe-coding-host', host.value); update(); });
    update();
  }
  for (const button of document.querySelectorAll('[data-copy-target]')) {
    button.addEventListener('click', async () => {
      const success = await copy($(button.dataset.copyTarget).textContent);
      button.parentElement.querySelector('[role="status"]').textContent = button.dataset[success ? 'success' : 'failure'];
    });
  }

  if ($('catalog-data')) {
    const data = JSON.parse($('catalog-data').textContent);
    const entries = engine.prepare(data.entries, data.topics, data.actions);
    const rows = new Map([...document.querySelectorAll('#rows .row')].map(row => [row.dataset.id, row]));
    const query = $('query'), category = $('category'), mode = $('mode'), full = $('full-text');
    const status = $('search-status'), container = $('catalog');
    const topicOptions = [...category.options], actionOptions = [...mode.options];
    const optionLabels = new Map([...topicOptions, ...actionOptions].map(option => [option, option.textContent]));
    let state = engine.readState(location.search, Object.keys(data.topics), Object.keys(data.actions));
    let bodies, pending, failed = false, composing = false, timer;
    const oldHash = location.hash.slice(1);
    if (rows.has(oldHash)) {
      location.replace(base + 'workflows/' + encodeURIComponent(oldHash) + '/?lang=' + current); return;
    }
    document.querySelector('.js-tools').hidden = false;
    $('pagination').hidden = false;
    function syncInputs() {
      query.value = state.q; category.value = state.topic; mode.value = state.action; full.checked = state.full;
    }
    function syncLinks() {
      const params = engine.searchParams(state);
      const target = location.pathname + (params ? '?' + params : '') + '#catalog';
      for (const [id, row] of rows) {
        const link = row.querySelector('.workflow-link');
        const next = new URL(base + 'workflows/' + id + '/', location.origin);
        if (current !== 'en') next.searchParams.set('lang', current);
        next.searchParams.set('return', target);
        contextualLink(link, next.pathname + next.search);
      }
      for (const link of document.querySelectorAll('.languages a')) {
        const next = new URL(link.href); next.search = params; next.hash = params ? 'catalog' : '';
        contextualLink(link, next.href);
      }
    }
    function syncURL(push = false) {
      const params = engine.searchParams(state);
      const target = location.pathname + (params ? '?' + params : '') + location.hash;
      if (location.pathname + location.search + location.hash !== target) history[push ? 'pushState' : 'replaceState'](null, '', target);
      syncLinks();
    }
    function updateOptions(options, counts, selected) {
      for (const option of options) {
        const count = option.value ? counts[option.value] || 0 : Object.values(counts).reduce((a,b) => a+b, 0);
        option.textContent = optionLabels.get(option) + ' · ' + count;
        option.disabled = !!option.value && count === 0 && selected !== option.value;
      }
    }
    function render(push = false) {
      const result = engine.select(entries, state, bodies);
      const slice = engine.paginate(result.matches, state.page);
      state.page = slice.page;
      for (const row of rows.values()) row.hidden = true;
      for (const {entry, match} of slice.items) {
        const row = rows.get(entry.id); row.hidden = false;
        row.querySelector('.body-match').hidden = !match.bodyOnly;
        $('rows').append(row);
      }
      $('count').textContent = format(data.messages[result.matches.length === 1 ? 'countOne' : 'count'], {count:result.matches.length, total:entries.length});
      $('page-status').textContent = format(data.messages.pageStatus, slice);
      $('previous').disabled = slice.page === 1; $('next').disabled = slice.page === slice.pages;
      $('pagination').hidden = result.matches.length === 0;
      $('empty').hidden = result.matches.length !== 0;
      $('clear-query').hidden = !state.q;
      const active = !!(state.q || state.topic || state.action || state.full);
      $('reset').hidden = !active;
      updateOptions(topicOptions, result.topics, state.topic);
      updateOptions(actionOptions, result.actions, state.action);
      const chips = $('active-filters'); chips.replaceChildren();
      for (const [key, options] of [['topic',topicOptions], ['action',actionOptions]]) {
        if (!state[key]) continue;
        const label = optionLabels.get(options.find(option => option.value === state[key]));
        const button = document.createElement('button'); button.type = 'button';
        button.textContent = label + ' ×'; button.setAttribute('aria-label', format(data.messages.removeFilter, {label}));
        button.addEventListener('click', () => { state[key] = ''; state.page = 1; syncInputs(); render(true); (key === 'topic' ? category : mode).focus(); });
        chips.append(button);
      }
      if (!state.full || !state.q.trim()) status.textContent = '';
      else status.textContent = pending ? data.messages.searchLoading : failed ? data.messages.searchFallback : '';
      container.setAttribute('aria-busy', String(!!pending && state.full && !!state.q.trim()));
      syncURL(push);
    }
    async function fullText() {
      if (!state.full || !state.q.trim() || bodies || pending) return;
      failed = false;
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 8000);
      pending = fetch(data.index, {signal:controller.signal}).then(response => {
        if (!response.ok) throw new Error('Search unavailable'); return response.json();
      }).then(value => { bodies = value; })
        .catch(() => { failed = true; })
        .finally(() => { clearTimeout(timeout); pending = null; render(); });
      render();
    }
    function change(push = false) {
      state.q = query.value.slice(0,160); state.topic = category.value; state.action = mode.value; state.full = full.checked; state.page = 1;
      render(push); fullText();
    }
    query.addEventListener('compositionstart', () => { composing = true; clearTimeout(timer); });
    query.addEventListener('compositionend', () => { composing = false; change(); });
    query.addEventListener('input', () => { clearTimeout(timer); if (!composing) timer = setTimeout(() => change(), 100); });
    $('search-form').addEventListener('submit', event => { event.preventDefault(); clearTimeout(timer); change(); });
    category.addEventListener('change', () => change(true));
    mode.addEventListener('change', () => change(true));
    full.addEventListener('change', () => change(true));
    $('clear-query').addEventListener('click', () => { clearTimeout(timer); query.value = ''; change(); query.focus(); });
    function reset() { clearTimeout(timer); state = {q:'',topic:'',action:'',full:false,page:1}; syncInputs(); render(true); query.focus(); }
    $('reset').addEventListener('click', reset); $('empty-reset').addEventListener('click', reset);
    for (const [id, delta] of [['previous',-1], ['next',1]]) $(id).addEventListener('click', () => {
      state.page += delta; render(true); $('results-title').focus({preventScroll:true}); $('results-title').scrollIntoView({block:'start'});
    });
    for (const shortcut of document.querySelectorAll('[data-topic]')) shortcut.addEventListener('click', event => {
      event.preventDefault(); clearTimeout(timer);
      state = {q:'',topic:shortcut.dataset.topic,action:'',full:false,page:1}; syncInputs(); render(true);
      container.scrollIntoView({block:'start'}); query.focus({preventScroll:true});
    });
    window.addEventListener('popstate', () => {
      clearTimeout(timer); state = engine.readState(location.search, Object.keys(data.topics), Object.keys(data.actions)); syncInputs(); render(); fullText();
    });
    document.addEventListener('keydown', event => {
      const target = document.activeElement;
      if (event.key === '/' && !event.metaKey && !event.ctrlKey && !event.altKey && !target.isContentEditable && !['INPUT','SELECT','TEXTAREA'].includes(target.tagName)) {
        event.preventDefault(); query.focus();
      }
    });
    syncInputs(); render(); fullText();
  }

  if (page === 'directory' && current !== 'en') {
    for (const link of document.querySelectorAll('.directory-topic a')) {
      const next = new URL(link.href); next.searchParams.set('lang', current);
      contextualLink(link, next.href);
    }
  }

  if ($('prompt-data')) {
    const data = JSON.parse($('prompt-data').textContent);
    const host = $('host'), language = $('prompt-language'), prompt = $('prompt');
    const returnTo = engine.safeReturn(url.searchParams.get('return'), location.origin, base)
      || (languages.includes(requested) ? base + (requested === 'en' ? '' : requested + '/') + '#catalog' : null);
    if (returnTo) {
      contextualLink($('catalog-back'), returnTo);
      for (const link of document.querySelectorAll('.related a')) {
        const next = new URL(link.href); next.searchParams.set('return', returnTo);
        if (languages.includes(requested)) next.searchParams.set('lang', requested);
        contextualLink(link, next.href);
      }
    }
    document.querySelector('.prompt-options').hidden = false;
    host.value = saved('vibe-coding-host') === 'claude' ? 'claude' : 'codex';
    language.value = languages.includes(requested) ? requested : languages.includes(saved('vibe-coding-language')) ? saved('vibe-coding-language') : 'en';
    function updatePrompt() {
      const ui = data.locales[language.value];
      prompt.value = format(ui[host.value === 'claude' ? 'promptClaude' : 'prompt'], {skill:data.skill,id:data.id,title:ui.title});
      prompt.lang = language.value; $('copy').textContent = ui.copy; $('copy').hidden = false; $('copy-status').textContent = '';
    }
    host.addEventListener('change', () => { save('vibe-coding-host',host.value); updatePrompt(); });
    language.addEventListener('change', () => { save('vibe-coding-language',language.value); updatePrompt(); });
    $('copy').addEventListener('click', async () => {
      let copied = await copy(prompt.value);
      if (!copied) { prompt.focus(); prompt.select(); try { copied = document.execCommand('copy'); } catch {} }
      $('copy-status').textContent = data.locales[language.value][copied ? 'copied' : 'copyFallback'];
    });
    updatePrompt();
  }
})();

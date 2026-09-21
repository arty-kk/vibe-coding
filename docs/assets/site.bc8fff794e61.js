'use strict';
(() => {
  const byId = id => document.getElementById(id);
  const base = document.body.dataset.base;
  const languages = ['en', 'es', 'ru', 'zh-CN'];
  const url = new URL(location.href);
  const requested = url.searchParams.get('lang') === 'zh' ? 'zh-CN' : url.searchParams.get('lang');
  const current = document.body.dataset.language;
  const page = document.body.dataset.page;
  const saved = key => { try { return localStorage.getItem(key); } catch { return null; } };
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch {} };
  const fold = value => value.normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
  const format = (text, values) => text.replace(/\{(\w+)\}/g, (match, key) => values[key] ?? match);

  // Legacy catalog links keep working. The public page language belongs to its URL.
  if (page !== 'workflow' && languages.includes(requested)) {
    url.pathname = base + (requested === 'en' ? '' : requested + '/') + (page.endsWith('.html') ? page : '');
    url.searchParams.delete('lang');
    location.replace(url.href);
    return;
  }

  const catalog = byId('catalog-data');
  if (catalog) {
    const data = JSON.parse(catalog.textContent);
    const rows = [...document.querySelectorAll('#rows .row')];
    const query = byId('query'), category = byId('category'), mode = byId('mode');
    const status = byId('search-status');
    let index, loading;
    document.querySelector('.js-tools').hidden = false;
    function render() {
      const terms = fold(query.value).trim().split(/\s+/).filter(Boolean);
      let count = 0;
      const scored = rows.map((row, position) => {
        const item = index?.[row.dataset.id];
        const primary = item?.primary ?? fold(row.textContent);
        const body = item?.body ?? '';
        const matches = (!category.value || row.dataset.skill === category.value)
          && (!mode.value || row.dataset.mode === mode.value)
          && terms.every(term => primary.includes(term) || body.includes(term));
        row.hidden = !matches;
        if (matches) count++;
        return {row, position, score: terms.reduce((score, term) => score + (primary.includes(term) ? 3 : body.includes(term) ? 1 : 0), 0)};
      });
      scored.sort((a,b) => b.score-a.score || a.position-b.position);
      byId('rows').append(...scored.map(item => item.row));
      byId('count').textContent = format(data.messages.count, {count, total:rows.length});
      byId('empty').hidden = count !== 0;
    }
    async function fullText() {
      if (index || loading) return;
      status.textContent = data.messages.searchLoading;
      loading = fetch(data.index).then(response => {
        if (!response.ok) throw new Error('Search unavailable');
        return response.json();
      }).then(value => { index=value; status.textContent=''; render(); })
        .catch(() => { status.textContent=data.messages.searchFallback; })
        .finally(() => { loading=null; });
    }
    query.addEventListener('input', () => { render(); if (query.value.trim()) fullText(); });
    category.addEventListener('change', render);
    mode.addEventListener('change', render);
    byId('reset').addEventListener('click', () => {
      query.value=''; category.value=''; mode.value=''; status.textContent=''; render(); query.focus();
    });
    for (const example of document.querySelectorAll('.example[data-skill]')) {
      example.addEventListener('click', () => { query.value=''; mode.value=''; category.value=example.dataset.skill; render(); });
    }
    for (const row of rows) {
      // The canonical workflow is English. Only the copied prompt follows the catalog locale.
      if (current !== 'en') row.href += '?lang=' + encodeURIComponent(current);
    }
    document.addEventListener('keydown', event => {
      if (event.key==='/' && !['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName)) {
        event.preventDefault(); query.focus();
      }
    });
    const hash = location.hash.slice(1);
    if (hash && rows.some(row => row.dataset.id === hash)) {
      location.replace(base+'workflows/'+encodeURIComponent(hash)+'/?lang='+encodeURIComponent(current));
      return;
    }
  }

  const promptData = byId('prompt-data');
  if (promptData) {
    const data = JSON.parse(promptData.textContent);
    const host = byId('host'), language = byId('prompt-language'), prompt = byId('prompt');
    document.querySelector('.prompt-options').hidden=false;
    host.value = saved('vibe-coding-host') === 'claude' ? 'claude' : 'codex';
    language.value = languages.includes(requested) ? requested : languages.includes(saved('vibe-coding-language')) ? saved('vibe-coding-language') : 'en';
    function updatePrompt() {
      const ui = data.locales[language.value];
      prompt.value = format(ui[host.value==='claude' ? 'promptClaude' : 'prompt'], {skill:data.skill, id:data.id, title:ui.title});
      prompt.lang = language.value;
      byId('copy').textContent=ui.copy;
      byId('copy').hidden=false;
      byId('copy-status').textContent='';
    }
    host.addEventListener('change', () => { save('vibe-coding-host',host.value); updatePrompt(); });
    language.addEventListener('change', () => { save('vibe-coding-language',language.value); updatePrompt(); });
    byId('copy').addEventListener('click', async () => {
      let copied=false;
      try { await navigator.clipboard.writeText(prompt.value); copied=true; } catch {}
      if (!copied) {
        prompt.focus(); prompt.select();
        try { copied=document.execCommand('copy'); } catch {}
      }
      byId('copy-status').textContent=data.locales[language.value][copied ? 'copied' : 'copyFallback'];
    });
    updatePrompt();
  }
})();

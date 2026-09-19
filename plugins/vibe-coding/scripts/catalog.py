#!/usr/bin/env python3
"""Search the shipped recipes and regenerate their offline catalog."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODE_NAMES = {'audit':'Аудит','implement':'Исправление','check':'Проверка','map':'Карта','plan':'Планирование','document':'Документ','closure':'Завершение','review':'Ревью','probe':'Поиск бага'}


def load_catalog():
    return json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))


def contained_path(raw):
    p=(ROOT/raw).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file():
        raise ValueError(f'Invalid recipe path: {raw}')
    return p


def search(rows, query='', mode=None, skill=None):
    terms=query.casefold().split()
    result=[]
    for row in rows:
        if mode and row['mode']!=mode:continue
        if skill and row['skill']!=skill:continue
        haystack=' '.join(str(row.get(k,'')) for k in ('id','title','skill','category','summary'))+' '+MODE_NAMES[row['mode']]
        if all(term in haystack.casefold() for term in terms):result.append(row)
    return result


def render_html(rows):
    expanded=[{**r,'body':contained_path(r['path']).read_text(encoding='utf-8')} for r in rows]
    data=json.dumps(expanded,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    return TEMPLATE.replace('__RECIPE_DATA__',data)


def refresh():
    catalog=load_catalog()
    for row in catalog['recipes']:
        row['sha256']=hashlib.sha256(contained_path(row['path']).read_bytes()).hexdigest()
    catalog['skills']=len(list((ROOT/'skills').glob('*/SKILL.md')))
    (ROOT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    (ROOT/'CATALOG.html').write_text(render_html(catalog['recipes']),encoding='utf-8', newline='\n')
    print(f'Refreshed {len(catalog["recipes"])} recipes; wrote CATALOG.html')


TEMPLATE='''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vibe Coding — каталог сценариев</title>
<style>
:root{color-scheme:dark;--bg:#101212;--panel:#191c1b;--line:#303733;--text:#f0f4ed;--muted:#a5b1a8;--accent:#c3f078;--mono:ui-monospace,SFMono-Regular,Consolas,monospace}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,input,select{font:inherit}button,a,input,select{touch-action:manipulation}button{cursor:pointer}a{color:var(--accent)}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:4px}header{max-width:1440px;margin:auto;padding:28px 44px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}.brand{font:600 15px var(--mono);letter-spacing:.1em;display:flex;gap:12px;align-items:center}.mark{width:30px;height:30px;background:var(--accent);color:#132010;display:grid;place-content:center;border-radius:8px;font-size:20px}.version{color:var(--muted);font:12px var(--mono)}main{max-width:1440px;margin:auto;padding:52px 44px}.eyebrow{font:12px var(--mono);letter-spacing:.1em;color:var(--accent);text-transform:uppercase}h1{font-size:clamp(34px,4.5vw,66px);line-height:1.08;letter-spacing:-.045em;font-weight:600;margin:20px 0 24px;max-width:850px}h1 span{color:var(--accent)}.intro{color:var(--muted);max-width:650px;font-size:17px;margin:0}.hero{display:flex;align-items:flex-end;justify-content:space-between;gap:32px;margin-bottom:44px}.stats{display:flex;gap:28px;flex-shrink:0}.stat strong{display:block;font:36px var(--mono);letter-spacing:-.05em}.stat span{font-size:12px;color:var(--muted)}.starter{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 32px}.starter button{border:1px solid var(--line);border-radius:30px;padding:8px 14px;background:transparent;color:var(--text);font-size:13px}.starter button:hover{border-color:var(--accent);background:#202719}.tools{display:grid;grid-template-columns:minmax(200px,1fr) 270px 210px;gap:12px}.tools label{font:11px var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.06em}.tools input,.tools select{display:block;margin-top:8px;width:100%;background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:10px;height:48px;padding:0 14px;font-size:14px}.resultbar{display:flex;justify-content:space-between;align-items:center;margin:24px 0 12px;color:var(--muted);font:12px var(--mono)}.resultbar button{background:transparent;color:var(--accent);border:0;padding:6px}.rows{border-top:1px solid var(--line)}.row{display:grid;grid-template-columns:42px minmax(220px,1fr) 210px 136px 24px;gap:16px;align-items:center;width:100%;text-align:left;border:0;border-bottom:1px solid var(--line);padding:19px 8px;background:none;color:var(--text);min-height:92px}.row:hover{background:#1c211c}.num{font:11px var(--mono);color:#8c9b8f}.title{display:block;font-size:16px;font-weight:550;letter-spacing:-.01em}.skill{display:block;font:11px var(--mono);color:var(--muted);margin-top:5px}.category{font-size:12px;color:var(--muted)}.badge{justify-self:start;border:1px solid #3c4935;color:#c8d5c0;background:#20271e;padding:4px 9px;border-radius:6px;font-size:11px;white-space:nowrap}.badge.audit,.badge.review{color:#c6d7f7;background:#1c2532;border-color:#33425b}.badge.check{color:#e7d2a6;background:#2e281c;border-color:#55482a}.arrow{color:var(--muted);font-size:20px}.empty{border:1px dashed var(--line);padding:40px;text-align:center;color:var(--muted);margin-top:16px;border-radius:12px}footer{display:flex;gap:22px;flex-wrap:wrap;margin-top:38px;padding-top:22px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}footer a{color:var(--muted)}dialog{width:min(850px,calc(100% - 28px));max-height:88vh;border:1px solid #536248;background:#171b18;color:var(--text);padding:32px;border-radius:18px;box-shadow:0 30px 100px #0008}dialog::backdrop{background:#000b;backdrop-filter:blur(5px)}.dialogtop{display:flex;justify-content:space-between;align-items:center;gap:20px}.close{border:1px solid var(--line);border-radius:50%;background:transparent;color:var(--text);font-size:23px;width:38px;height:38px}dialog h2{font-size:28px;letter-spacing:-.03em;margin:25px 0 12px}.detailmeta{color:var(--muted);font-size:13px}.prompt{width:100%;resize:vertical;min-height:108px;background:#10150f;color:var(--text);border:1px solid var(--line);border-radius:10px;padding:15px;font:14px/1.6 var(--mono);margin-top:18px}.actions{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin:14px 0 20px}.copy{background:var(--accent);color:#15200e;border:0;padding:12px 18px;border-radius:8px;font-weight:650}.status{font-size:12px;color:var(--accent)}details{border-top:1px solid var(--line);padding-top:18px}summary{cursor:pointer;color:var(--muted);font-size:13px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.7 var(--mono);color:#c6d0c7}.source{color:var(--muted);font-size:11px;overflow-wrap:anywhere;margin-top:22px}.help{font-size:12px;color:var(--muted)}@media(max-width:1000px){.hero{display:block}.stats{margin-top:28px}.tools{grid-template-columns:1fr 1fr}.tools label:first-child{grid-column:1/-1}.row{grid-template-columns:30px 1fr 115px 20px}.category{display:none}}@media(max-width:600px){header{padding:20px}.version{display:none}main{padding:32px 20px}.hero{margin-bottom:30px}h1{font-size:40px}.intro{font-size:15px}.tools{grid-template-columns:1fr}.tools label:first-child{grid-column:auto}.row{grid-template-columns:1fr 100px;padding:16px 0;gap:8px}.num,.arrow{display:none}.title{font-size:14px}.badge{font-size:10px;justify-self:end}.skill{font-size:10px}.stats{gap:24px}.stat strong{font-size:30px}dialog{padding:22px}.dialogtop{gap:8px}dialog h2{font-size:23px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style></head><body>
<header><div class="brand"><span class="mark" aria-hidden="true">↗</span>VIBE CODING</div><div class="version">CODEX PLUGIN / 1.0.3</div></header>
<main><section class="hero"><div><div class="eyebrow">Рабочая библиотека для Codex</div><h1>Выбери задачу.<br><span>Запусти нужный сценарий.</span></h1><p class="intro">От карты проекта до проверенного изменения. Найди нужный сценарий, скопируй запрос и добавь контекст своей задачи в Codex.</p></div><div class="stats"><div class="stat"><strong>43</strong><span>навыка</span></div><div class="stat"><strong>221</strong><span>сценарий</span></div><div class="stat"><strong>40</strong><span>направлений</span></div></div></section>
<div class="starter" aria-label="Быстрый выбор"><button data-skill="vibe-map">Разобраться в проекте</button><button data-skill="vibe-review">Проверить патч</button><button data-skill="vibe-probe">Найти баг</button><button data-skill="vibe-task">Сформулировать задачу</button></div>
<section aria-label="Каталог сценариев"><div class="tools"><label>Поиск<input id="query" type="search" placeholder="Например: платежи, webhook, Kubernetes" autocomplete="off"></label><label>Область<select id="category"><option value="">Все области</option></select></label><label>Действие<select id="mode"><option value="">Все действия</option></select></label></div><div class="resultbar"><span id="count" role="status" aria-live="polite"></span><button id="reset">Сбросить фильтры</button></div><div class="rows" id="rows"></div><div id="empty" class="empty" hidden>Ничего не найдено. Попробуй другое слово или сбрось фильтры.</div></section>
<footer><span>Работает локально · без внешних ресурсов</span><a href="README.md">Руководство</a><a href="https://github.com/arty-kk/vibe-coding">GitHub</a><a href="https://github.com/arty-kk/vibe-coding/issues">Поддержка</a></footer></main>
<dialog id="detail" aria-labelledby="detail-title"><div class="dialogtop"><span id="detail-badge" class="badge"></span><button class="close" id="close" aria-label="Закрыть">×</button></div><h2 id="detail-title"></h2><p class="detailmeta" id="detail-meta"></p><label for="prompt" class="help">Готовый запрос — добавь описание своей задачи после вставки в Codex.</label><textarea class="prompt" id="prompt" readonly></textarea><div class="actions"><button class="copy" id="copy">Скопировать запрос</button><span id="copy-status" class="status" role="status"></span></div><details><summary>Прочитать инструкции сценария</summary><pre id="body"></pre></details><p class="source" id="source"></p></dialog>
<script type="application/json" id="recipe-data">__RECIPE_DATA__</script>
<script>
const recipes=JSON.parse(document.getElementById('recipe-data').textContent);
const modes={audit:'Аудит',implement:'Исправление',check:'Проверка',map:'Карта',plan:'Планирование',document:'Документ',closure:'Завершение',review:'Ревью',probe:'Поиск бага'};
const $=id=>document.getElementById(id), query=$('query'), category=$('category'), mode=$('mode'), dialog=$('detail');
const categories=[...new Map(recipes.map(r=>[r.skill,r.category])).entries()].sort((a,b)=>a[1].localeCompare(b[1],'ru'));
for(const [value,label] of categories){const option=new Option(label,value);category.add(option)}
for(const [value,label] of Object.entries(modes)){mode.add(new Option(label,value))}
function node(tag,cls,text){const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el}
function render(){const terms=query.value.toLocaleLowerCase('ru').trim().split(/\\s+/).filter(Boolean);const list=recipes.filter(r=>{const s=[r.title,r.id,r.skill,r.category,r.summary,modes[r.mode]].join(' ').toLocaleLowerCase('ru');return (!category.value||r.skill===category.value)&&(!mode.value||r.mode===mode.value)&&terms.every(t=>s.includes(t))});$('count').textContent=list.length+' из '+recipes.length+' сценариев';$('empty').hidden=list.length!==0;const fragment=document.createDocumentFragment();for(const [i,r]of list.entries()){const button=node('button','row');button.type='button';button.setAttribute('aria-label',r.title+' — '+modes[r.mode]);button.append(node('span','num',String(i+1).padStart(2,'0')));const name=node('span','name');name.append(node('span','title',r.title),node('span','skill','$'+r.skill));button.append(name,node('span','category',r.category),node('span','badge '+r.mode,modes[r.mode]),node('span','arrow','↗'));button.addEventListener('click',()=>openRecipe(r.id));fragment.append(button)}$('rows').replaceChildren(fragment)}
function openRecipe(id){const r=recipes.find(r=>r.id===id);if(!r)return;$('detail-title').textContent=r.title;$('detail-meta').textContent=r.category+' · $'+r.skill;$('detail-badge').className='badge '+r.mode;$('detail-badge').textContent=modes[r.mode];$('prompt').value=r.example;$('body').textContent=r.body;$('source').textContent='Сценарий: '+r.id;$('copy-status').textContent='';dialog.querySelector('details').open=false;try{history.replaceState(null,'','#'+encodeURIComponent(r.id))}catch{}if(!dialog.open)dialog.showModal()}
function closeDetail(){dialog.close();try{history.replaceState(null,'',location.pathname+location.search)}catch{}}
$('close').addEventListener('click',closeDetail);dialog.addEventListener('cancel',e=>{e.preventDefault();closeDetail()});
for(const el of [query,category,mode])el.addEventListener(el===query?'input':'change',render);
$('reset').addEventListener('click',()=>{query.value='';category.value='';mode.value='';render();query.focus()});
for(const button of document.querySelectorAll('[data-skill]'))button.addEventListener('click',()=>{query.value='';mode.value='';category.value=button.dataset.skill;render()});
$('copy').addEventListener('click',async()=>{const text=$('prompt').value;let copied=false;try{if(navigator.clipboard){await navigator.clipboard.writeText(text);copied=true}}catch{}if(!copied){$('prompt').focus();$('prompt').select();try{copied=document.execCommand('copy')}catch{}}$('copy-status').textContent=copied?'Скопировано. Вставь в Codex.':'Текст выделен — нажми ⌘C или Ctrl+C.'});
document.addEventListener('keydown',e=>{if(e.key==='/'&&!dialog.open&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();query.focus()}});
render();try{if(location.hash)openRecipe(decodeURIComponent(location.hash.slice(1)))}catch{}
</script></body></html>'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('search');p.add_argument('query',nargs='?',default='');p.add_argument('--mode',choices=MODE_NAMES);p.add_argument('--skill');p.add_argument('--json',action='store_true')
    p=sub.add_parser('show');p.add_argument('id')
    sub.add_parser('refresh')
    args=parser.parse_args()
    if args.command=='refresh':refresh();return
    rows=load_catalog()['recipes']
    if args.command=='show':
        matches=[r for r in rows if r['id']==args.id]
        if not matches:parser.error('Unknown recipe ID. Use search first.')
        print(contained_path(matches[0]['path']).read_text(encoding='utf-8'));return
    rows=search(rows,args.query,args.mode,args.skill)
    if args.json:print(json.dumps(rows,ensure_ascii=False,indent=2))
    else:
        for row in rows:print(f'{row["id"]} | ${row["skill"]} | {MODE_NAMES[row["mode"]]}\n  {row["title"]} — {row["category"]}')
        print(f'Found: {len(rows)}')


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Build crawlable, localized pages from the shipped workflow sources."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, quote
import hashlib
import html
import json
import re
import shutil
import sys
from xml.etree import ElementTree as ET
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
PLUGIN = ROOT / 'plugins/vibe-coding'
BASE = 'https://arty-kk.github.io/vibe-coding/'
PREFIX = '/vibe-coding/'
REPO = 'https://github.com/arty-kk/vibe-coding'
DIRECTORY = 'https://chatgpt.com/plugins/plugins_6aae54a259ac8191b56161d366fb6e51'
sys.path.insert(0, str(PLUGIN / 'scripts'))
from catalog_site import LANGUAGES, load_locales, validate_locales, script_json, policy_html
from search_index import build_index

MD = MarkdownIt('commonmark', {'html': False}).enable('table')
e = html.escape


def route(lang='en', page=''):
    return ('' if lang == 'en' else lang + '/') + page


def workflow_route(row):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', row['id']):
        raise ValueError('Invalid workflow ID')
    return 'workflows/' + row['id'] + '/'


def asset(destination, name, contents):
    raw = contents.encode('utf-8') if isinstance(contents, str) else contents
    path = Path(name)
    target = 'assets/' + path.stem + '.' + hashlib.sha256(raw).hexdigest()[:12] + path.suffix
    output = destination / target
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    return PREFIX + target


def write(destination, path, text):
    output = destination / path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding='utf-8', newline='\n')


def language_links(lang, page='', recipe=False):
    return '<details class="language-menu"><summary>'+LANGUAGES[lang]+'</summary><nav class="languages" aria-label="Language">' + ''.join(
        f'<a href="{PREFIX}{route(code, page)}" lang="{code}" hreflang="{code}"'
        + (' aria-current="page"' if code == lang and not recipe else '') + f'>{label}</a>'
        for code, label in LANGUAGES.items()) + '</nav></details>'


def graph(version):
    return [
        {'@type': 'WebSite', '@id': BASE+'#website', 'url': BASE, 'name': 'Vibe Coding',
         'inLanguage': list(LANGUAGES)},
        {'@type': 'SoftwareSourceCode', '@id': BASE+'#software', 'name': 'Vibe Coding',
         'url': BASE, 'codeRepository': REPO, 'version': version,
         'description': 'Open-source engineering skills and workflows for Codex and Claude Code.',
         'runtimePlatform': ['Codex', 'Claude Code'], 'programmingLanguage': 'Markdown',
         'license': REPO+'/blob/main/LICENSE', 'isAccessibleForFree': True,
         'author': {'@type': 'Person', 'name': 'Arty S.', 'url': 'https://github.com/arty-kk'},
         'image': BASE+'social-card.png'}]


def page(lang, path, title, description, body, content, resources, version,
         alternates=None, article=None, noindex=False):
    canonical = BASE + path
    alternate_tags = '' if alternates is None else '\n'.join(
        f'<link rel="alternate" hreflang="{code}" href="{BASE}{target}">'
        for code, target in alternates.items())
    data = graph(version)
    entity = {'@type': 'WebPage', '@id': canonical+'#page', 'url': canonical,
              'name': title, 'description': description, 'inLanguage': lang,
              'isPartOf': {'@id': BASE+'#website'}, 'about': {'@id': BASE+'#software'}}
    if article:
        entity.update({'@type': 'TechArticle', 'headline': article['title'],
                       'mainEntityOfPage': canonical, 'license': REPO+'/blob/main/LICENSE'})
        data.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Vibe Coding', 'item': BASE},
            {'@type': 'ListItem', 'position': 2, 'name': article['title'], 'item': canonical}]})
    else:
        entity['mainEntity'] = {'@id': BASE+'#software'}
    data.append(entity)
    ui = content[lang]
    policy_page = Path(path).name if path.endswith('.html') and not noindex else ''
    og_locale = {'en':'en_US', 'es':'es_ES', 'ru':'ru_RU', 'zh-CN':'zh_CN'}[lang]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}">
<link rel="canonical" href="{canonical}">
{alternate_tags}
<meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:site_name" content="Vibe Coding">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:image" content="{BASE}social-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Vibe Coding — engineering workflows for Codex and Claude Code">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{BASE}social-card.png">
<meta name="twitter:image:alt" content="Vibe Coding — engineering workflows for Codex and Claude Code">
<meta name="theme-color" content="#f6f7f2">
<link rel="icon" href="{PREFIX}icon.png" type="image/png">
<link rel="stylesheet" href="{resources['css']}">
<script type="application/ld+json">{script_json({'@context':'https://schema.org','@graph':data})}</script>
<script src="{resources['engine']}" defer></script>
<script src="{resources['js']}" defer></script>
</head>
<body data-base="{PREFIX}" data-language="{lang}" data-page="{'workflow' if article else policy_page or 'catalog'}">
<a class="skip" href="#content">{e(ui['skip'])}</a>
<header class="site-header"><a class="brand" href="{PREFIX}{route(lang)}"><img src="{PREFIX}icon.png" width="32" height="32" alt="">Vibe Coding</a>
<div class="header-actions"><a class="header-github" href="{REPO}">GitHub</a>{language_links(lang, policy_page, bool(article))}<a class="button small" href="{PREFIX}{route(lang)}#install">{e(ui["install"])}</a></div></header>
<main id="content">{body}
<footer><span><a href="https://github.com/arty-kk">{e(ui['maintained'])}</a></span>
<a href="{REPO}">GitHub</a><a href="{REPO}/releases/tag/v{version}">{e(ui['release'])}</a>
<a href="{REPO}/issues">{e(resources['locales'][lang]['ui']['support'])}</a>
<a href="{REPO}/blob/main/LICENSE">MIT</a>
<a href="{PREFIX}{route(lang,'privacy.html')}">{e(resources['locales'][lang]['ui']['privacy'])}</a>
<a href="{PREFIX}{route(lang,'terms.html')}">{e(resources['locales'][lang]['ui']['terms'])}</a></footer>
</main></body></html>
'''


def display_title(row, locale, content, lang='en'):
    title = content['featured'].get(row['id'], {}).get('title', locale['titles'][row['id']])
    return 'Improve ' + title[:-7] if lang == 'en' and title.endswith(' Polish') else title


def home(lang, rows, locale, c, version, resources):
    ui = locale['ui']
    skill_count = resources['skills']
    if lang == 'ru':
        mod100, mod10 = skill_count % 100, skill_count % 10
        skill_label = 'навыков' if 11 <= mod100 <= 14 else 'навык' if mod10 == 1 else 'навыка' if 2 <= mod10 <= 4 else 'навыков'
    else:
        skill_label = ui['skills']
    featured = list(c['featured'])
    rows = sorted(rows, key=lambda row: featured.index(row['id']) if row['id'] in featured else len(featured))
    def copy_button(target):
        return f'<div class="copy-line"><button type="button" class="copy-command" data-copy-target="{target}" data-success="{e(c["copied"])}" data-failure="{e(c["copyFallback"])}">{e(c["copy"])}</button><span role="status"></span></div>'
    entries = []
    for row in rows:
        title = display_title(row, locale, c, lang)
        summary = c['featured'].get(row['id'], {}).get('description', locale['summaries'][row['skill']])
        entries.append(f'''<article class="row" id="{row['id']}" data-id="{row['id']}" data-skill="{row['skill']}" data-mode="{row['mode']}">
<div class="card-meta"><span class="category">{e(locale['categories'][row['skill']])}</span><span class="badge {row['mode']}">{e(locale['modes'][row['mode']])}</span></div>
<h3><a class="workflow-link" href="{PREFIX}{workflow_route(row)}" hreflang="en" data-id="{row['id']}">{e(title)}</a></h3><p>{e(summary)}</p>
<div class="card-bottom"><code>{row['skill']}</code><span class="body-match" hidden>{e(c['bodyMatch'])}</span><span class="card-arrow" aria-hidden="true">→</span></div></article>''')
    categories = '<option value="">'+e(c['allTopics'])+'</option>' + ''.join(f'<option value="{skill}">{e(title)}</option>' for skill,title in sorted(locale['categories'].items(), key=lambda item:item[1]))
    modes = '<option value="">'+e(c['allActions'])+'</option>'+''.join(f'<option value="{mode}">{e(title)}</option>' for mode,title in locale['modes'].items())
    faqs = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in c['faq'])
    shortcuts = ''.join(f'<a href="?topic={skill}#catalog" data-topic="{skill}">{e(label)}</a>' for label,skill in c['quickLinks'])
    messages = {key:c[key] for key in ('count','countOne','pageStatus','removeFilter','searchLoading','searchFallback')}
    search_data = {
        'index':resources['search'], 'messages':messages,
        'entries':[{'id':r['id'],'skill':r['skill'],'mode':r['mode'],'titles':[loc['titles'][r['id']] for loc in resources['locales'].values()]+[text['featured'][r['id']]['title'] for text in resources['content'].values() if r['id'] in text['featured']],'keywords':r.get('keywords',[])} for r in rows],
        'topics':{skill:[loc['categories'][skill] for loc in resources['locales'].values()] for skill in locale['categories']},
        'actions':{mode:[loc['modes'][mode] for loc in resources['locales'].values()] for mode in locale['modes']}}
    return f'''<section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="live-dot" aria-hidden="true"></span>{e(c['eyebrow'])}</p>
<h1>{e(c['headline'])}<br><span>{e(c['accent'])}</span></h1><p class="intro">{e(c['intro'])}</p>
<div class="cta"><a class="button primary" href="#catalog">{e(c['browse'])} <span aria-hidden="true">↓</span></a><a class="text-link" href="#install">{e(c['install'])} <span aria-hidden="true">→</span></a></div>
<p class="fine">{e(c['facts'])}</p></div>
<aside class="demo"><div class="demo-top"><span>{e(c['demoTask'])}</span><label><span class="sr-only">{e(ui['host'])}</span><select id="demo-host"><option value="codex">Codex</option><option value="claude">Claude Code</option></select></label></div>
<div class="demo-code"><p class="demo-label">{e(c['demoLabel'])}</p><pre><code id="demo-prompt" data-task="{e(c['demoPrompt'])}">$vibe-review\n{e(c['demoPrompt'])}</code></pre>{copy_button('demo-prompt')}</div><p class="demo-note">{e(c['demoNote'])}</p>
<div class="stats"><span><strong>{resources['skills']}</strong> {e(skill_label)}</span><span><strong>{len(rows)}</strong> {e(ui['workflows'])}</span></div></aside></section>
<section class="catalog section" id="catalog" aria-labelledby="catalog-title"><div class="section-heading"><div><p class="eyebrow">VIBE CODING / {e(ui['catalog'])}</p><h2 id="catalog-title">{e(c['catalogTitle'])}</h2><p class="section-intro">{e(c['catalogNote'])}</p></div><a class="version" href="{REPO}/releases/tag/v{version}">v{version}</a></div>
<div class="js-tools" hidden><form id="search-form" role="search"><div class="search-box"><label class="sr-only" for="query">{e(c['search'])}</label><input id="query" type="search" maxlength="160" placeholder="{e(c['searchPlaceholder'])}" autocomplete="off"><button id="clear-query" type="button" aria-label="{e(c['clearSearch'])}" hidden>×</button><kbd aria-hidden="true">/</kbd></div>
<div class="filterbar"><label for="category">{e(c['topic'])}<select id="category">{categories}</select></label><label for="mode">{e(c['action'])}<select id="mode">{modes}</select></label><label class="check-label"><input type="checkbox" id="full-text">{e(c['fullText'])}</label></div></form>
<div class="quick-links"><span>{e(c['quickLabel'])}</span>{shortcuts}</div>
<div class="results-heading" id="results-title" tabindex="-1"><span id="count" role="status" aria-live="polite">{e(c['count'].format(count=len(rows)))}</span><div id="active-filters"></div><button type="button" id="reset" hidden>{e(c['reset'])}</button></div><p id="search-status" class="search-status" role="status"></p></div>
<div class="rows" id="rows">{''.join(entries)}</div><div id="empty" class="empty" hidden><h3>{e(c['emptyTitle'])}</h3><p>{e(c['empty'])}</p><button id="empty-reset" type="button" class="button">{e(c['reset'])}</button></div>
<nav id="pagination" class="pagination" aria-label="{e(ui['catalog'])}" hidden><button type="button" id="previous">{e(c['previous'])}</button><span id="page-status"></span><button type="button" id="next">{e(c['next'])}</button></nav><p class="catalog-note">{e(c['english'])}</p>
<script type="application/json" id="catalog-data">{script_json(search_data)}</script></section>
<section class="section installation" id="install"><div class="section-heading"><div><p class="eyebrow">CODEX + CLAUDE CODE</p><h2>{e(c['install'])}</h2><p class="section-intro">{e(c['installIntro'])}</p></div><a class="text-link" href="{REPO}/blob/main/plugins/vibe-coding/docs/INSTALL.md">{e(c['docs'])} →</a></div>
<div class="install-cards"><article class="install-card"><h3>Codex</h3><p>{e(c['codexInstall'])}</p><a class="button primary" href="{DIRECTORY}">{e(c['codexLink'])} ↗</a><pre><code id="codex-start">$vibe {e(c['demoPrompt'])}</code></pre>{copy_button('codex-start')}</article>
<article class="install-card"><h3>Claude Code</h3><p>{e(c['claudeInstall'])}</p><pre><code id="claude-install">claude plugin marketplace add arty-kk/vibe-coding\nclaude plugin install vibe-coding@vibe-coding</code></pre>{copy_button('claude-install')}<p>{e(c['claudeStart'])}</p><pre><code id="claude-start">/vibe-coding:vibe {e(c['demoPrompt'])}</code></pre>{copy_button('claude-start')}</article></div><p class="fine">{e(c['cost'])}</p></section>
<section class="section faq"><h2>{e(c['faqTitle'])}</h2><div>{faqs}</div></section>'''


def recipe_markdown(row, version):
    path = (PLUGIN / row['path']).resolve()
    if not path.is_relative_to(PLUGIN.resolve()):
        raise ValueError('Escaping source path')
    text = path.read_text(encoding='utf-8')
    tokens = MD.parse(text)
    if tokens and tokens[0].type == 'heading_open' and tokens[0].tag == 'h1':
        tokens = tokens[3:]
    ids = set()
    toc = []
    for index, token in enumerate(tokens):
        if token.type == 'heading_open':
            title = tokens[index+1].content
            base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') or 'section'
            heading_id = base
            count = 2
            while heading_id in ids:
                heading_id = f'{base}-{count}'; count += 1
            ids.add(heading_id); token.attrSet('id', heading_id)
            if token.tag == 'h2': toc.append((heading_id,title))
        for child in token.children or []:
            if child.type != 'link_open': continue
            link = child.attrGet('href')
            parts = urlsplit(link)
            if parts.scheme or not parts.path: continue
            target = (path.parent / parts.path).resolve()
            if not target.is_relative_to(PLUGIN.resolve()) or not target.exists():
                raise ValueError(f'Invalid source link: {link}')
            child.attrSet('href', REPO+f'/blob/v{version}/plugins/vibe-coding/'+quote(target.relative_to(PLUGIN.resolve()).as_posix())+('#'+parts.fragment if parts.fragment else ''))
    return MD.renderer.render(tokens, MD.options, {}), toc, text


def excerpt(text, title, limit=170):
    match = re.search(r'^## (?:Goal and scope|Goal|Purpose)\s*\n+(.+?)(?:\n\n|$)', text, re.M|re.S)
    if match:
        value = match[1]
    else:
        scenario = re.search(r'^## Scenarios\s*\n+- (.+)$', text, re.M)
        operation = re.search(r'^## Operation\s*\n+(.+?)(?:\n\n|$)', text, re.M|re.S)
        paragraphs = [p for p in text.split('\n\n') if p.strip() and not p.lstrip().startswith(('#','|','-','```'))]
        value = scenario[1] if scenario else operation[1] if operation else paragraphs[0] if paragraphs else title
    value = re.sub(r'[`*#]|\[([^]]+)\]\([^)]*\)', lambda m:m[1] or '', value)
    value = ' '.join(value.split())
    return value if limit is None or len(value) <= limit else value[:limit-3].rsplit(' ',1)[0]+ '…'


def build(destination=SITE):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    rows = json.loads((PLUGIN/'catalog.json').read_text(encoding='utf-8'))['recipes']
    locales = load_locales()
    validate_locales(locales, rows)
    version = json.loads((PLUGIN/'plugin.json').read_text(encoding='utf-8'))['version']
    skills = len(list((PLUGIN/'skills').glob('*/SKILL.md')))
    content = json.loads((ROOT/'site/content.json').read_text(encoding='utf-8').replace('{skills}',str(skills)).replace('{recipes}',str(len(rows))))
    if set(content) != set(LANGUAGES): raise ValueError('Missing site locale')
    for language, values in content.items():
        if set(values) != set(content['en']): raise ValueError(f'Incomplete site content: {language}')
        if set(values['featured']) != set(content['en']['featured']): raise ValueError(f'Incomplete featured workflows: {language}')
        if not set(values['featured']) <= {row['id'] for row in rows}: raise ValueError(f'Unknown featured workflow: {language}')
    for name in ('privacy','terms'):
        if locales['en']['policy'][name] != (ROOT/f'{name.upper()}.md').read_text(encoding='utf-8'):
            raise ValueError(f'Update policy translations after changing {name.upper()}.md')
    resources = {'locales':locales, 'content':content, 'skills':skills,
        'css':asset(destination,'site.css',(ROOT/'site/site.css').read_text(encoding='utf-8')),
        'engine':asset(destination,'catalog-engine.js',(ROOT/'site/catalog-engine.js').read_text(encoding='utf-8')),
        'js':asset(destination,'site.js',(ROOT/'site/site.js').read_text(encoding='utf-8')),
        'search':asset(destination,'search.json',script_json(build_index(rows,locales,PLUGIN)))}
    paths = []
    for lang, locale in locales.items():
        path = route(lang)
        alternates = {code:route(code) for code in LANGUAGES}|{'x-default':''}
        output = page(lang,path,content[lang]['title'],content[lang]['description'],home(lang,rows,locale,content[lang],version,resources),content,resources,version,alternates)
        write(destination,path+'index.html',output); paths.append(path)
        for name in ('privacy','terms'):
            path = route(lang,name+'.html')
            description = ' '.join(locale['policy'][name].split('\n\n')[1].split())
            body = '<article class="policy">'+policy_html(locale['policy'][name])+f'<p><a href="{PREFIX}{route(lang)}">{e(locale["ui"]["back"])}</a></p></article>'
            output = page(lang,path,locale['ui'][name]+' — Vibe Coding',description,body,content,resources,version,{code:route(code,name+'.html') for code in LANGUAGES}|{'x-default':name+'.html'})
            write(destination,path,output); paths.append(path)
    for row in rows:
        rendered, toc, source = recipe_markdown(row,version)
        title = display_title(row, locales['en'], content['en'])
        description = content['en']['featured'].get(row['id'], {}).get('description', excerpt(source,row['title']))
        introduction = content['en']['featured'].get(row['id'], {}).get('description', excerpt(source,row['title'],limit=None))
        path = workflow_route(row)
        related = [r for r in rows if r['skill']==row['skill'] and r['id']!=row['id']]
        related_html = ''.join(f'<li><a href="{PREFIX}{workflow_route(r)}">{e(display_title(r,locales["en"],content["en"]))}</a> <span class="fine">· {e(locales["en"]["modes"][r["mode"]])}</span></li>' for r in related)
        toc_html = ''.join(f'<li><a href="#{key}">{e(label)}</a></li>' for key,label in toc)
        prompt = locales['en']['ui']['prompt'].format(skill=row['skill'],title=row['title'],id=row['id'])
        messages = {lang:{key:value for key,value in data['ui'].items() if key in ('prompt','promptClaude','copy','copied','copyFallback','promptHelp')}|{'title':data['titles'][row['id']]} for lang,data in locales.items()}
        body = f'''<article class="workflow"><nav aria-label="Breadcrumb"><a id="catalog-back" href="{PREFIX}#catalog">Back to workflows</a><span aria-hidden="true"> / </span><span>{e(title)}</span></nav>
<p class="eyebrow">{e(row['category'])} · {e(locales['en']['modes'][row['mode']])}</p><h1>{e(title)}</h1>
<p class="intro">{e(introduction)}</p><p class="fine">Vibe Coding {version} · <code>{row['skill']}</code> · English technical instructions</p>
<section class="run-workflow" aria-labelledby="run-title"><h2 id="run-title">Use this workflow</h2><p>Install Vibe Coding, choose your assistant and prompt language, then add your task details after the prompt.</p>
<div class="tools prompt-options" hidden><label for="host">Assistant<select id="host"><option value="codex">Codex</option><option value="claude">Claude Code</option></select></label>
<label for="prompt-language">Prompt language<select id="prompt-language">{''.join(f'<option value="{code}">{label}</option>' for code,label in LANGUAGES.items())}</select></label></div>
<label class="help" for="prompt">Prompt</label><textarea id="prompt" class="prompt" readonly>{e(prompt)}</textarea>
<div class="actions"><button class="copy" id="copy" hidden>Copy prompt</button><span id="copy-status" class="status" role="status"></span><a href="{PREFIX}#install">Install the plugin</a></div>
<script type="application/json" id="prompt-data">{script_json({'id':row['id'],'skill':row['skill'],'locales':messages})}</script></section>
<nav class="toc" aria-label="On this page"><h2>In this workflow</h2><ul>{toc_html}</ul></nav>
<section id="technical-instructions" lang="en">{rendered}</section>
<p class="source">Workflow ID: {row['id']} · <a href="{REPO}/blob/v{version}/plugins/vibe-coding/{quote(row['path'])}">View the versioned source</a> · <a href="{REPO}/blob/v{version}/plugins/vibe-coding/references/workflow.md">Shared workflow and authority rules</a></p>
{f'<aside class="related"><h2>Related workflows</h2><ul>{related_html}</ul></aside>' if related else ''}</article>'''
        output = page('en',path,title+' — Vibe Coding',description,body,content,resources,version,article={'title':title})
        write(destination,path+'index.html',output); paths.append(path)
    missing = '<section class="policy"><p class="eyebrow">404</p><h1>Page not found.</h1><p>This address does not match a published workflow.</p><p><a href="'+PREFIX+'#catalog">Find a workflow in the catalog →</a></p></section>'
    write(destination,'404.html',page('en','404.html','Page not found — Vibe Coding','Find engineering workflows for Codex and Claude Code.',missing,content,resources,version,noindex=True))
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    sitemap = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for path in sorted(paths):
        url = ET.SubElement(sitemap,'{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        ET.SubElement(url,'{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text=BASE+path
    write(destination,'sitemap.xml',ET.tostring(sitemap,encoding='unicode',xml_declaration=True)+'\n')
    shutil.copyfile(PLUGIN/'assets/icon.png',destination/'icon.png')
    shutil.copyfile(ROOT/'site/social-card.png',destination/'social-card.png')
    (destination/'.nojekyll').touch()
    # Keep published content-addressed assets: cached HTML and already-open tabs may
    # still request an older script or lazily load its full-text index after deployment.
    print(f'Built {len(paths)} indexable pages: four locales, {len(rows)} English workflows; static HTML + sitemap.')


if __name__ == '__main__':
    build()

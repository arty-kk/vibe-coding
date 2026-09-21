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
    return '<nav class="languages" aria-label="Language">' + ''.join(
        f'<a href="{PREFIX}{route(code, page)}" lang="{code}" hreflang="{code}"'
        + (' aria-current="page"' if code == lang and not recipe else '') + f'>{label}</a>'
        for code, label in LANGUAGES.items()) + '</nav>'


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
<meta name="theme-color" content="#101212">
<link rel="icon" href="{PREFIX}icon.png" type="image/png">
<link rel="stylesheet" href="{resources['css']}">
<script type="application/ld+json">{script_json({'@context':'https://schema.org','@graph':data})}</script>
<script src="{resources['js']}" defer></script>
</head>
<body data-base="{PREFIX}" data-language="{lang}" data-page="{'workflow' if article else policy_page or 'catalog'}">
<a class="skip" href="#content">{e(ui['skip'])}</a>
<header><a class="brand" href="{PREFIX}{route(lang)}"><span class="mark" aria-hidden="true">↗</span>VIBE CODING</a>
<div class="header-actions"><a class="version" href="{REPO}/releases/tag/v{version}">v{version}</a>{language_links(lang, policy_page, bool(article))}</div></header>
<main id="content">{body}
<footer><span><a href="https://github.com/arty-kk">{e(ui['maintained'])}</a></span>
<a href="{REPO}">GitHub</a><a href="{REPO}/releases/tag/v{version}">{e(ui['release'])}</a>
<a href="{REPO}/issues">{e(resources['locales'][lang]['ui']['support'])}</a>
<a href="{REPO}/blob/main/LICENSE">MIT</a>
<a href="{PREFIX}{route(lang,'privacy.html')}">{e(resources['locales'][lang]['ui']['privacy'])}</a>
<a href="{PREFIX}{route(lang,'terms.html')}">{e(resources['locales'][lang]['ui']['terms'])}</a></footer>
</main></body></html>
'''


def home(lang, rows, locale, c, version, resources):
    ui = locale['ui']
    cards = ''.join(f'<article class="card"><h3>{e(title)}</h3><p>{e(text)}</p></article>' for title,text in c['steps'])
    examples = ''.join(f'<a class="card example" href="#catalog" data-skill="{skill}"><h3>{e(title)} <span aria-hidden="true">↗</span></h3><p>{e(text)}</p></a>' for title,text,skill in c['examples'])
    entries = []
    for i,row in enumerate(rows, 1):
        entries.append(f'''<a class="row" id="{row['id']}" href="{PREFIX}{workflow_route(row)}" hreflang="en" data-id="{row['id']}" data-skill="{row['skill']}" data-mode="{row['mode']}">
<span class="num">{i:02d}</span><span class="name"><span class="title">{e(locale['titles'][row['id']])}</span><span class="skill">{row['skill']}</span></span>
<span class="category">{e(locale['categories'][row['skill']])}</span><span class="badge {row['mode']}">{e(locale['modes'][row['mode']])}</span><span class="arrow" aria-hidden="true">↗</span></a>''')
    categories = '<option value="">'+e(ui['allCategories'])+'</option>' + ''.join(f'<option value="{skill}">{e(title)}</option>' for skill,title in sorted(locale['categories'].items(), key=lambda item:item[1]))
    modes = '<option value="">'+e(ui['allActions'])+'</option>'+''.join(f'<option value="{mode}">{e(title)}</option>' for mode,title in locale['modes'].items())
    faqs = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in c['faq'])
    messages = {key:ui[key] for key in ('count','empty')}
    messages.update({key:c[key] for key in ('searchLoading','searchFallback')})
    return f'''<section class="hero"><div><div class="eyebrow">{e(c['eyebrow'])}</div>
<h1>{e(c['headline'])}<br><span>{e(c['accent'])}</span></h1><p class="intro">{e(c['intro'])}</p>
<div class="cta"><a class="button primary" href="#catalog">{e(c['browse'])}</a><a class="button" href="#install">{e(c['install'])}</a></div>
<p class="fine">{e(c['facts'])}</p></div><div class="stats">
<div class="stat"><strong>{resources['skills']}</strong><span>{e(ui['skills'])}</span></div>
<div class="stat"><strong>{len(rows)}</strong><span>{e(ui['workflows'])}</span></div>
<div class="stat"><strong>{len({r['group'] for r in rows})}</strong><span>{e(ui['domains'])}</span></div></div></section>
<section class="section"><h2>{e(c['howTitle'])}</h2><p class="section-intro">{e(c['howIntro'])}</p><div class="cards three">{cards}</div></section>
<section class="section"><h2>{e(c['examplesTitle'])}</h2><div class="cards four">{examples}</div></section>
<section class="section" id="install"><h2>{e(c['install'])}</h2><p class="section-intro">{e(c['installIntro'])}</p>
<div class="cards two"><article class="card"><h3>Codex</h3><p>{e(c['codexInstall'])}</p><p><a href="{DIRECTORY}">{e(c['codexLink'])} ↗</a></p><pre><code>$vibe Map this repository and explain its main contracts.</code></pre></article>
<article class="card"><h3>Claude Code</h3><p>{e(c['claudeInstall'])}</p><pre><code>claude plugin marketplace add arty-kk/vibe-coding
claude plugin install vibe-coding@vibe-coding</code></pre><p>{e(c['claudeStart'])}</p><pre><code>/vibe-coding:vibe Map this repository and explain its main contracts.</code></pre></article></div>
<p><a href="{REPO}/blob/main/plugins/vibe-coding/docs/INSTALL.md">{e(c['docs'])} ↗</a></p><p class="fine">{e(c['cost'])}</p></section>
<section class="section" id="catalog" aria-labelledby="catalog-title"><h2 id="catalog-title">{e(ui['catalog'])}</h2><p class="section-intro">{e(c['catalogNote'])}</p>
<div class="js-tools" hidden><div class="tools"><label for="query">{e(ui['search'])}<input id="query" type="search" placeholder="{e(ui['searchPlaceholder'])}" autocomplete="off"></label>
<label for="category">{e(ui['category'])}<select id="category">{categories}</select></label><label for="mode">{e(ui['action'])}<select id="mode">{modes}</select></label></div>
<div class="resultbar"><span id="count" role="status" aria-live="polite">{e(ui['count'].format(count=len(rows),total=len(rows)))}</span><button id="reset">{e(ui['reset'])}</button></div><p id="search-status" class="fine" role="status"></p></div>
<p class="fine">{e(c['english'])}</p><div class="rows" id="rows">{''.join(entries)}</div><p id="empty" class="empty" hidden>{e(ui['empty'])}</p>
<script type="application/json" id="catalog-data">{script_json({'index':resources['search'],'messages':messages})}</script></section>
<section class="section faq"><h2>{e(c['faqTitle'])}</h2>{faqs}</section>'''


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


def excerpt(text, title):
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
    return value if len(value) <= 170 else value[:167].rsplit(' ',1)[0]+ '…'


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
    for name in ('privacy','terms'):
        if locales['en']['policy'][name] != (ROOT/f'{name.upper()}.md').read_text(encoding='utf-8'):
            raise ValueError(f'Update policy translations after changing {name.upper()}.md')
    resources = {'locales':locales, 'skills':skills,
        'css':asset(destination,'site.css',(PLUGIN/'assets/catalog/style.css').read_text(encoding='utf-8')+'\n'+(ROOT/'site/site.css').read_text(encoding='utf-8')),
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
        path = workflow_route(row)
        related = [r for r in rows if r['skill']==row['skill'] and r['id']!=row['id']]
        related_html = ''.join(f'<li><a href="{PREFIX}{workflow_route(r)}">{e(r["title"])}</a> <span class="fine">· {e(locales["en"]["modes"][r["mode"]])}</span></li>' for r in related)
        toc_html = ''.join(f'<li><a href="#{key}">{e(label)}</a></li>' for key,label in toc)
        prompt = locales['en']['ui']['prompt'].format(skill=row['skill'],title=row['title'],id=row['id'])
        messages = {lang:{key:value for key,value in data['ui'].items() if key in ('prompt','promptClaude','copy','copied','copyFallback','promptHelp')}|{'title':data['titles'][row['id']]} for lang,data in locales.items()}
        body = f'''<article class="workflow"><nav aria-label="Breadcrumb"><a href="{PREFIX}#catalog">Workflow catalog</a><span aria-hidden="true"> / </span><span>{e(row['title'])}</span></nav>
<p class="eyebrow">{e(row['category'])} · {e(locales['en']['modes'][row['mode']])}</p><h1>{e(row['title'])}</h1>
<p class="intro">{e(excerpt(source,row['title']))}</p><p class="fine">Vibe Coding {version} · <code>{row['skill']}</code> · English technical instructions</p>
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
        output = page('en',path,row['title']+' — Vibe Coding',excerpt(source,row['title']),body,content,resources,version,article=row)
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
    # Remove only previously generated hashed assets; never recursively erase a destination.
    used = {url.rsplit('/',1)[-1] for key,url in resources.items() if key in ('css','js','search')}
    for old in (destination/'assets').iterdir():
        if re.fullmatch(r'(site|search)\.[0-9a-f]{12}\.(css|js|json)',old.name) and old.name not in used:
            old.unlink()
    print(f'Built {len(paths)} indexable pages: four locales, {len(rows)} English workflows; static HTML + sitemap.')


if __name__ == '__main__':
    build()

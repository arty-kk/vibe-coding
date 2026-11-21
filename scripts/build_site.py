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
LIBRARY_PLUGIN = ROOT / 'plugins/vibe-coding-library'
BASE = 'https://arty-kk.github.io/vibe-coding/'
PREFIX = '/vibe-coding/'
REPO = 'https://github.com/arty-kk/vibe-coding'
MCP_SITE = 'https://vibe-coding-library.artem-satsuk.chatgpt.site/'
MCP_ENDPOINT = MCP_SITE + 'library/mcp'
DEMO_WORKFLOWS = ('patch-checking', 'instant-bug-fix-polish', 'homepage-landing-polish')
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


def console_url(lang):
    return MCP_SITE + ('?lang=' + lang if lang != 'en' else '')


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
        {'@type': 'Person', '@id': BASE+'#maintainer', 'name': 'Arty S.',
         'url': 'https://github.com/arty-kk'},
        {'@type': 'WebSite', '@id': BASE+'#website', 'url': BASE, 'name': 'Vibe Coding Library',
         'inLanguage': list(LANGUAGES), 'publisher': {'@id': BASE+'#maintainer'}},
        {'@type': 'SoftwareSourceCode', '@id': BASE+'#software', 'name': 'Vibe Coding Library',
         'url': BASE, 'codeRepository': REPO, 'version': version,
         'description': 'Find engineering workflows and load website planning or implementation guidance with read-only MCP tools over Streamable HTTP.',
         'runtimePlatform': ['MCP clients with Streamable HTTP support'], 'programmingLanguage': ['Markdown', 'JavaScript'],
         'license': REPO+'/blob/main/LICENSE', 'isAccessibleForFree': True,
         'maintainer': {'@id': BASE+'#maintainer'},
         'image': BASE+'social-card.png'}]


def page(lang, path, title, description, body, content, resources, version,
         alternates=None, article=None, noindex=False, directory=False):
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
                       'mainEntityOfPage': canonical, 'license': REPO+'/blob/main/LICENSE',
                       'publisher': {'@id': BASE+'#maintainer'}, 'version': article['version'],
                       'isAccessibleForFree': True, 'articleSection': article['category'],
                       'isBasedOn': article['source']})
        data.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Vibe Coding', 'item': BASE},
            {'@type': 'ListItem', 'position': 2, 'name': content['en']['allWorkflows'], 'item': BASE+'workflows/'},
            {'@type': 'ListItem', 'position': 3, 'name': article['title'], 'item': canonical}]})
    elif directory:
        entity['@type'] = 'CollectionPage'
    elif path == route(lang):
        entity['mainEntity'] = {'@id': BASE+'#software'}
    data.append(entity)
    ui = content[lang]
    policy_page = Path(path).name if path.endswith('.html') and not noindex else ''
    navigation_page = 'workflows/' if directory else policy_page
    page_type = 'workflow' if article else 'directory' if directory else policy_page or 'catalog'
    on_home = path == route(lang)
    catalog_link = f'<a class="header-catalog" href="#catalog">{e(ui["search"])}</a>' if on_home else ''
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
<meta property="og:site_name" content="Vibe Coding Library">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:image" content="{BASE}social-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Vibe Coding Library — engineering workflows for MCP-compatible coding agents">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{BASE}social-card.png">
<meta name="twitter:image:alt" content="Vibe Coding Library — engineering workflows for MCP-compatible coding agents">
<meta name="theme-color" content="{'#121a15' if on_home else '#f6f7f2'}">
<link rel="icon" href="{PREFIX}icon.png" type="image/png">
<link rel="stylesheet" href="{resources['css']}">
<script type="application/ld+json">{script_json({'@context':'https://schema.org','@graph':data})}</script>
<script src="{resources['engine']}" defer></script>
<script src="{resources['js']}" defer></script>
</head>
<body{' class="home-page"' if on_home else ''} data-base="{PREFIX}" data-language="{lang}" data-page="{page_type}">
<a class="skip" href="#content">{e(ui['skip'])}</a>
<header class="site-header"><a class="brand" href="{PREFIX}{route(lang)}"><img src="{PREFIX}icon.png" width="32" height="32" alt=""><span>Vibe Coding <span class="brand-library">Library</span></span></a>
<div class="header-actions">{catalog_link}<a class="header-github" href="{REPO}">GitHub</a>{language_links(lang, navigation_page, bool(article))}<a class="button small" href="{PREFIX}{route(lang)}#install">{e(ui["install"])}</a></div></header>
<main id="content">{body}
<footer><span><a href="https://github.com/arty-kk">{e(ui['maintained'])}</a></span>
<a href="{PREFIX}{route(lang,'workflows/')}">{e(ui['allWorkflows'])}</a>
<a href="{console_url(lang)}">{e(ui['mcpLabel'])}</a>
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


def copy_button(c, target, label, status_id=None):
    if status_id:
        icon = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.15" aria-hidden="true"><rect x="6" y="6" width="7" height="7" rx="1.4"/><path d="M10 4V3.8A1.8 1.8 0 0 0 8.2 2h-4.4A1.8 1.8 0 0 0 2 3.8v4.4A1.8 1.8 0 0 0 3.8 10H4" stroke-linecap="round"/></svg>'
        button_label = icon + f'<span class="copy-label">{e(label)}</span>'
        status = f' data-copy-status="{e(status_id)}"'
        feedback = ''
    else:
        button_label = e(label)
        status = ''
        feedback = '<span role="status"></span>'
    return f'<div class="copy-line" hidden><button type="button" class="copy-command" data-copy-target="{target}"{status} data-success="{e(c["copied"])}" data-failure="{e(c["copyFallback"])}">{button_label}</button>{feedback}</div>'


def code_copy_field(c, key, value, label, labelled_by=None):
    group = f' role="group" aria-labelledby="{labelled_by}"' if labelled_by else ''
    field_class = 'code-copy-field endpoint-field' if labelled_by else 'code-copy-field'
    status = f'{key}-copy-status'
    return (
        f'<div class="{field_class}"{group}><code id="{key}">{e(value)}</code>{copy_button(c, key, label, status)}</div>'
        f'<p class="code-copy-status" id="{status}" role="status"></p>'
    )


def workflow_demo(rows, c):
    examples = {
        row['id']: {
            'prompt': c['demoPrompt'].format(id=row['id']) + ' ' + c['demoExamples'][row['id']]['task'],
            'url': PREFIX + workflow_route(row),
        }
        for row in rows if row['id'] in DEMO_WORKFLOWS
    }
    first = examples[DEMO_WORKFLOWS[0]]
    choices = ''.join(
        f'<label><input type="radio" name="demo-example" value="{key}"{" checked" if index == 0 else ""}>'
        f'<span>{e(c["demoExamples"][key]["label"])}</span></label>'
        for index, key in enumerate(DEMO_WORKFLOWS)
    )
    return f'''<section class="demo" id="workflow-demo" aria-labelledby="demo-title" tabindex="-1">
<div class="demo-top"><h2 id="demo-title">{e(c['demoTitle'])}</h2>
<label class="select-field" hidden><span class="sr-only">{e(c['demoFormat'])}</span><select id="demo-host"><option value="generic">{e(c['demoGeneric'])}</option><option value="codex">{e(c['demoCodex'])}</option><option value="claude">{e(c['demoClaude'])}</option></select></label></div>
<fieldset class="demo-choices" hidden><legend class="sr-only">{e(c['demoTask'])}</legend>{choices}</fieldset>
<div class="demo-body"><p class="demo-label">{e(c['demoLabel'])}</p><pre><code id="demo-prompt" aria-live="polite">{e(first['prompt'])}</code></pre>
<div class="demo-actions">{copy_button(c, 'demo-prompt', c['copyPrompt'])}<a id="demo-workflow" class="text-link" href="{first['url']}" hreflang="en">{e(c['readWorkflow'])} <span aria-hidden="true">↗</span></a></div></div>
<p class="demo-note">{e(c['demoNote'])}</p>
<script type="application/json" id="demo-data">{script_json(examples)}</script></section>'''


def connection_section(lang, c, version):
    codex = 'codex mcp add vibe-coding-library --url ' + MCP_ENDPOINT
    claude = 'claude mcp add --transport http vibe-coding-library ' + MCP_ENDPOINT
    plugin = 'claude plugin marketplace add arty-kk/vibe-coding\nclaude plugin install vibe-coding-library@vibe-coding'
    commands = ''.join(
        f'<details class="install-command"><summary>{label}</summary>{code_copy_field(c, key, command, c["copy"])}'
        f'<a class="text-link" href="{docs}">{e(c["docs"])} <span aria-hidden="true">↗</span></a></details>'
        for label, key, command, docs in (
            ('Codex', 'codex-mcp', codex, 'https://developers.openai.com/learn/docs-mcp'),
            ('Claude Code', 'claude-mcp', claude, 'https://code.claude.com/docs/en/mcp'),
        )
    )
    return f'''<section class="section installation" id="install" aria-labelledby="install-title">
<div class="section-heading"><div><h2 id="install-title">{e(c['install'])}</h2><p class="section-intro">{e(c['installIntro'])}</p></div>
<a class="version" href="{REPO}/releases/tag/v{version}">{e(c['libraryVersion'])} v{version}</a></div>
<div class="install-cards">
<article class="install-card endpoint-card"><h3>{e(c['clientTitle'])}</h3><p>{e(c['clientInstall'])}</p>
<p class="command-label" id="mcp-endpoint-label">{e(c['endpointLabel'])}</p>
{code_copy_field(c, 'mcp-endpoint', MCP_ENDPOINT, c['copyEndpoint'], 'mcp-endpoint-label')}
<a class="text-link" href="{console_url(lang)}#try-library">{e(c['consoleLink'])} <span aria-hidden="true">↗</span></a></article>
<article class="install-card"><h3>{e(c['pluginTitle'])}</h3><p>{e(c['clientStart'])}</p>
<div class="install-commands">{commands}</div>
<details class="install-command plugin-setup"><summary>{e(c['pluginLink'])}</summary><p>{e(c['pluginInstall'])}</p>
<p class="command-label">Claude Code</p>{code_copy_field(c, 'claude-install', plugin, c['copy'])}
<a class="text-link" href="{REPO}/tree/v{version}/plugins/vibe-coding-library">{e(c['source'])} <span aria-hidden="true">↗</span></a></details></article></div>
<aside class="offline-option"><div><h3>{e(c['offlineTitle'])}</h3><p>{e(c['offlineNote'])}</p></div><a href="{REPO}/blob/main/plugins/vibe-coding/docs/INSTALL.md">{e(c['offlineLink'])} <span aria-hidden="true">↗</span></a></aside>
<div class="install-next"><p class="fine">{e(c['cost'])}</p><a class="text-link" href="#workflow-demo">{e(c['demoReturn'])} <span aria-hidden="true">↑</span></a></div></section>'''


def catalog_section(lang, rows, locale, c, resources):
    ui = locale['ui']
    featured = list(c['featured'])
    rows = sorted(rows, key=lambda row: featured.index(row['id']) if row['id'] in featured else len(featured))
    entries = []
    for row in rows:
        title = display_title(row, locale, c, lang)
        summary = c['featured'].get(row['id'], {}).get('description', locale['summaries'][row['skill']])
        entries.append(f'''<article class="row" id="{row['id']}">
<div class="card-meta"><span class="category">{e(locale['categories'][row['skill']])}</span><span class="badge {row['mode']}">{e(locale['modes'][row['mode']])}</span></div>
<h3><a class="workflow-link" href="{PREFIX}{workflow_route(row)}" hreflang="en" data-id="{row['id']}">{e(title)}</a></h3><p>{e(summary)}</p>
<div class="card-bottom"><code>{row['skill']}</code><span class="body-match" hidden>{e(c['bodyMatch'])}</span><span class="card-arrow" aria-hidden="true">→</span></div></article>''')
    categories = '<option value="">'+e(c['allTopics'])+'</option>' + ''.join(f'<option value="{skill}">{e(title)}</option>' for skill,title in sorted(locale['categories'].items(), key=lambda item:item[1]))
    modes = '<option value="">'+e(c['allActions'])+'</option>'+''.join(f'<option value="{mode}">{e(title)}</option>' for mode,title in locale['modes'].items())
    shortcuts = ''.join(f'<button type="button" data-topic="{skill}">{e(label)}</button>' for label,skill in c['quickLinks'])
    messages = {key:c[key] for key in ('count','countOne','pageStatus','removeFilter','searchLoading','searchFallback')}
    search_data = {
        'index':resources['search'], 'messages':messages,
        'entries':[{'id':r['id'],'skill':r['skill'],'mode':r['mode'],'purpose':r.get('purpose',''),'primary_keywords':r.get('primary_keywords',[]),'titles':[loc['titles'][r['id']] for loc in resources['locales'].values()]+[text['featured'][r['id']]['title'] for text in resources['content'].values() if r['id'] in text['featured']],'keywords':r.get('keywords',[])} for r in rows],
        'topics':{skill:[loc['categories'][skill] for loc in resources['locales'].values()] for skill in locale['categories']},
        'actions':{mode:[loc['modes'][mode] for loc in resources['locales'].values()] for mode in locale['modes']}}
    directory = PREFIX + route(lang, 'workflows/')
    return f'''<section class="catalog section" id="catalog" aria-labelledby="catalog-title">
<div class="section-heading"><div><h2 id="catalog-title">{e(c['catalogTitle'])}</h2><p class="section-intro">{e(c['catalogNote'])}</p></div>
<a class="text-link" href="{directory}">{e(c['allWorkflows'])} <span aria-hidden="true">→</span></a></div>
<div class="js-tools" hidden><form id="search-form" role="search"><div class="search-box"><label class="sr-only" for="query">{e(c['search'])}</label><input id="query" type="search" maxlength="240" placeholder="{e(c['searchPlaceholder'])}" autocomplete="off"><button id="clear-query" type="button" aria-label="{e(c['clearSearch'])}" hidden>×</button><kbd aria-hidden="true">/</kbd></div>
<div class="filterbar"><label class="select-field" for="category">{e(c['topic'])}<select id="category">{categories}</select></label><label class="select-field" for="mode">{e(c['action'])}<select id="mode">{modes}</select></label><label class="check-label"><input type="checkbox" id="full-text">{e(c['fullText'])}</label></div></form>
<div class="quick-links"><span>{e(c['quickLabel'])}</span>{shortcuts}</div>
<div class="results-heading" id="results-title" tabindex="-1"><span id="count" role="status" aria-live="polite">{e(c['count'].format(count=len(rows)))}</span><div id="active-filters"></div><button type="button" id="reset" hidden>{e(c['reset'])}</button></div><p id="search-status" class="search-status" role="status"></p></div>
<div class="rows" id="rows">{''.join(entries)}</div><div id="empty" class="empty" hidden><h3>{e(c['emptyTitle'])}</h3><p>{e(c['empty'])}</p><div class="empty-actions"><button id="empty-reset" type="button" class="button">{e(c['reset'])}</button><a class="text-link" href="{directory}">{e(c['browseTopics'])} <span aria-hidden="true">→</span></a></div></div>
<nav id="pagination" class="pagination" aria-label="{e(ui['catalog'])}" hidden><button type="button" id="previous">{e(c['previous'])}</button><span id="page-status"></span><button type="button" id="next">{e(c['next'])}</button></nav><p class="catalog-note">{e(c['english'])}</p>
<script type="application/json" id="catalog-data">{script_json(search_data)}</script></section>'''


def home(lang, rows, locale, c, version, resources):
    faqs = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in c['faq'])
    return f'''<section class="hero" aria-labelledby="hero-title"><div class="hero-inner">
<div class="hero-copy"><p class="eyebrow">{e(c['eyebrow'])}</p>
<h1 id="hero-title">{e(c['headline'])} <span>{e(c['accent'])}</span></h1><p class="intro">{e(c['intro'])}</p>
<div class="cta"><a class="button primary browse-jump" href="#catalog">{e(c['browse'])} <span aria-hidden="true">↓</span></a>
<a class="button primary demo-jump" href="#workflow-demo">{e(c['demoTitle'])} <span aria-hidden="true">↓</span></a>
<a class="text-link" href="#install">{e(c['install'])} <span aria-hidden="true">→</span></a></div>
<p class="hero-facts">{e(c['facts'])}</p></div>
{workflow_demo(rows, c)}</div></section>
{catalog_section(lang, rows, locale, c, resources)}
{connection_section(lang, c, version)}
<section class="section faq" aria-labelledby="faq-title"><h2 id="faq-title">{e(c['faqTitle'])}</h2><div>{faqs}</div></section>'''


def directory_body(lang, rows, locale, c):
    sections, topics = [], []
    for skill, label in sorted(locale['categories'].items(), key=lambda item: item[1]):
        selected = [row for row in rows if row['skill'] == skill]
        if not selected:
            continue
        topics.append(f'<li><a href="#{skill}">{e(label)} <span>{len(selected)}</span></a></li>')
        links = ''.join(f'<li><a href="{PREFIX}{workflow_route(row)}" hreflang="en">{e(display_title(row,locale,c,lang))}</a><span class="fine">{e(locale["modes"][row["mode"]])}</span></li>' for row in selected)
        sections.append(f'<section id="{skill}" class="directory-topic"><h2>{e(label)}</h2><p>{e(locale["summaries"][skill])}</p><ul>{links}</ul></section>')
    return f'''<article class="directory"><header><p class="eyebrow">VIBE CODING / {e(c['allWorkflows'])}</p><h1>{e(c['directoryHeading'])}</h1><p class="intro">{e(c['directoryDescription'])}</p><p class="fine">{e(c['english'])}</p><a class="text-link" href="{PREFIX}{route(lang)}#catalog">← {e(c['search'])}</a></header>
<nav class="directory-topics" aria-label="{e(c['topic'])}"><ul>{''.join(topics)}</ul></nav><div class="directory-list">{''.join(sections)}</div></article>'''


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


def placeholders(value):
    if isinstance(value, dict):
        return {key: placeholders(item) for key, item in value.items()}
    if isinstance(value, list):
        return [placeholders(item) for item in value]
    return set(re.findall(r'\{(\w+)\}', value)) if isinstance(value, str) else None


def load_site_policies(source=None):
    policies = json.loads(Path(source or ROOT/'site/policies.json').read_text(encoding='utf-8'))
    if not isinstance(policies, dict) or set(policies) != set(LANGUAGES):
        raise ValueError('Missing or unexpected site policy locale')
    for language, values in policies.items():
        if not isinstance(values, dict) or set(values) != {'privacy', 'terms'}:
            raise ValueError(f'Incomplete site policies: {language}')
        for name, text in values.items():
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f'Empty site policy: {language}.{name}')
            headings = [token for token in MD.parse(text) if token.type == 'heading_open' and token.tag == 'h1']
            if not text.startswith('# ') or len(headings) != 1:
                raise ValueError(f'Expected one site policy title: {language}.{name}')
    return policies


def build(destination=SITE):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    rows = json.loads((PLUGIN/'catalog.json').read_text(encoding='utf-8'))['recipes']
    locales = load_locales()
    validate_locales(locales, rows)
    version = json.loads((LIBRARY_PLUGIN/'plugin.json').read_text(encoding='utf-8'))['version']
    instruction_version = json.loads((PLUGIN/'plugin.json').read_text(encoding='utf-8'))['version']
    mcp_version = json.loads((ROOT/'mcp/package.json').read_text(encoding='utf-8'))['version']
    skills = len(list((PLUGIN/'skills').glob('*/SKILL.md')))
    content = json.loads((ROOT/'site/content.json').read_text(encoding='utf-8').replace('{skills}',str(skills)).replace('{recipes}',str(len(rows))))
    if set(content) != set(LANGUAGES): raise ValueError('Missing site locale')
    for language, values in content.items():
        if set(values) != set(content['en']): raise ValueError(f'Incomplete site content: {language}')
        if set(values['featured']) != set(content['en']['featured']): raise ValueError(f'Incomplete featured workflows: {language}')
        if not set(values['featured']) <= {row['id'] for row in rows}: raise ValueError(f'Unknown featured workflow: {language}')
        if set(values['demoExamples']) != set(DEMO_WORKFLOWS): raise ValueError(f'Incomplete workflow examples: {language}')
        if placeholders(values) != placeholders(content['en']): raise ValueError(f'Mismatched site placeholders: {language}')
    if not set(DEMO_WORKFLOWS) <= {row['id'] for row in rows}: raise ValueError('Unknown workflow example')
    policies = load_site_policies()
    lexicon = json.loads((PLUGIN/'assets/catalog/search-lexicon.json').read_text(encoding='utf-8'))
    lexicon.pop('purposes', None)
    engine = (ROOT/'site/catalog-engine.js').read_text(encoding='utf-8')
    engine += '\nwindow.VibeCatalog.lexicon = ' + script_json(lexicon) + ';\n'
    resources = {'locales':locales, 'content':content, 'skills':skills,
        'css':asset(destination,'site.css',(ROOT/'site/site.css').read_text(encoding='utf-8')),
        'engine':asset(destination,'catalog-engine.js',engine),
        'js':asset(destination,'site.js',(ROOT/'site/site.js').read_text(encoding='utf-8')),
        'search':asset(destination,'search.json',script_json(build_index(rows,locales,PLUGIN)))}
    paths = []
    for lang, locale in locales.items():
        path = route(lang)
        alternates = {code:route(code) for code in LANGUAGES}|{'x-default':''}
        output = page(lang,path,content[lang]['title'],content[lang]['description'],home(lang,rows,locale,content[lang],version,resources),content,resources,version,alternates)
        write(destination,path+'index.html',output); paths.append(path)
        path = route(lang,'workflows/')
        alternates = {code:route(code,'workflows/') for code in LANGUAGES}|{'x-default':'workflows/'}
        output = page(lang,path,content[lang]['directoryTitle'],content[lang]['directoryDescription'],directory_body(lang,rows,locale,content[lang]),content,resources,version,alternates,directory=True)
        write(destination,path+'index.html',output); paths.append(path)
        for name in ('privacy','terms'):
            path = route(lang,name+'.html')
            description = content[lang][name+'Description']
            body = '<article class="policy">'+MD.render(policies[lang][name])+f'<p><a href="{PREFIX}{route(lang)}">{e(locale["ui"]["back"])}</a></p></article>'
            output = page(lang,path,locale['ui'][name]+' — Vibe Coding Library',description,body,content,resources,version,{code:route(code,name+'.html') for code in LANGUAGES}|{'x-default':name+'.html'})
            write(destination,path,output); paths.append(path)
    for row in rows:
        rendered, toc, source = recipe_markdown(row,instruction_version)
        title = display_title(row, locales['en'], content['en'])
        description = content['en']['featured'].get(row['id'], {}).get('description', excerpt(source,row['title']))
        introduction = content['en']['featured'].get(row['id'], {}).get('description', excerpt(source,row['title'],limit=None))
        path = workflow_route(row)
        related = [r for r in rows if r['skill']==row['skill'] and r['id']!=row['id']]
        related_html = ''.join(f'<li><a href="{PREFIX}{workflow_route(r)}">{e(display_title(r,locales["en"],content["en"]))}</a> <span class="fine">· {e(locales["en"]["modes"][r["mode"]])}</span></li>' for r in related)
        toc_html = ''.join(f'<li><a href="#{key}">{e(label)}</a></li>' for key,label in toc)
        prompt = content['en']['workflowPromptGeneric'].format(title=title,id=row['id'])
        messages = {lang:{key:value for key,value in data['ui'].items() if key in ('copy','copied','copyFallback','promptHelp')}|{'prompt':content[lang]['workflowPrompt'],'promptClaude':content[lang]['workflowPromptClaude'],'promptGeneric':content[lang]['workflowPromptGeneric'],'title':display_title(row,data,content[lang],lang)} for lang,data in locales.items()}
        source_url = f'{REPO}/blob/v{instruction_version}/plugins/vibe-coding/{quote(row["path"])}'
        body = f'''<article class="workflow"><nav aria-label="Breadcrumb"><a href="{PREFIX}">Vibe Coding</a><span aria-hidden="true"> / </span><a href="{PREFIX}workflows/">{e(content['en']['allWorkflows'])}</a><span aria-hidden="true"> / </span><span>{e(title)}</span></nav>
<p class="eyebrow">{e(row['category'])} · {e(locales['en']['modes'][row['mode']])}</p><h1>{e(title)}</h1>
<p class="intro">{e(introduction)}</p><p class="fine">MCP library {mcp_version} · Instruction library {instruction_version} · English technical instructions</p><a id="catalog-back" class="text-link" href="{PREFIX}#catalog">← Back to search</a>
<section class="run-workflow" aria-labelledby="run-title"><h2 id="run-title">Use this workflow</h2><p>{e(content['en']['workflowIntro'])}</p>
<div class="tools prompt-options" hidden><label class="select-field" for="host">Coding agent<select id="host"><option value="generic">{e(content['en']['genericHost'])}</option><option value="codex">Codex</option><option value="claude">Claude Code</option></select></label>
<label class="select-field" for="prompt-language">Prompt language<select id="prompt-language">{''.join(f'<option value="{code}">{label}</option>' for code,label in LANGUAGES.items())}</select></label></div>
<label class="help" for="prompt">Prompt</label><textarea id="prompt" class="prompt" readonly>{e(prompt)}</textarea>
<div class="actions"><button class="copy" id="copy" hidden>Copy prompt</button><span id="copy-status" class="status" role="status"></span><a href="{PREFIX}#install">Connect Vibe Coding Library</a></div>
<script type="application/json" id="prompt-data">{script_json({'id':row['id'],'skill':row['skill'],'locales':messages})}</script></section>
<nav class="toc" aria-label="On this page"><h2>In this workflow</h2><ul>{toc_html}</ul></nav>
<section id="technical-instructions" lang="en">{rendered}</section>
<p class="source">Workflow ID: {row['id']} · <a href="{source_url}">View the versioned source</a> · <a href="{REPO}/blob/v{instruction_version}/plugins/vibe-coding/references/workflow.md">Shared workflow and authority rules</a></p>
{f'<aside class="related"><h2>Related workflows</h2><ul>{related_html}</ul></aside>' if related else ''}</article>'''
        output = page('en',path,title+' — Vibe Coding',description,body,content,resources,version,article={'title':title,'category':row['category'],'source':source_url,'version':instruction_version})
        write(destination,path+'index.html',output); paths.append(path)
    missing = '<section class="policy"><p class="eyebrow">404</p><h1>Page not found.</h1><p>This address does not match a published workflow.</p><p><a href="'+PREFIX+'#catalog">Find a workflow in the catalog →</a></p></section>'
    write(destination,'404.html',page('en','404.html','Page not found — Vibe Coding','Find engineering workflows for MCP-compatible coding agents.',missing,content,resources,version,noindex=True))
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

#!/usr/bin/env python3
"""Build the English-first catalog and localized policy pages without dependencies."""
from pathlib import Path
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
SOURCE = ROOT / 'site'
PLUGIN = ROOT / 'plugins/vibe-coding'
LANGUAGES = {'en': 'English', 'es': 'Español', 'ru': 'Русский', 'zh-CN': '简体中文'}


def load_locales():
    return {code: json.loads((SOURCE/'locales'/f'{code}.json').read_text(encoding='utf-8'))
            for code in LANGUAGES}


def validate_locales(locales, rows):
    expected = {
        'categories': {row['skill'] for row in rows},
        'summaries': {row['skill'] for row in rows},
        'titles': {row['id'] for row in rows},
        'modes': {row['mode'] for row in rows},
        'policy': {'privacy', 'terms'},
        'ui': set(locales['en']['ui']),
    }
    for language in LANGUAGES:
        data = locales[language]
        for section, keys in expected.items():
            if set(data[section]) != keys:
                raise ValueError(f'{language}: missing or unexpected {section} translations')
            for key, value in data[section].items():
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f'{language}: empty {section}.{key}')
                placeholders = set(re.findall(r'\{\w+\}', value))
                base = set(re.findall(r'\{\w+\}', locales['en'][section][key]))
                if placeholders != base:
                    raise ValueError(f'{language}: mismatched placeholders in {section}.{key}')
    for name in ('privacy', 'terms'):
        if locales['en']['policy'][name] != (ROOT/f'{name.upper()}.md').read_text(encoding='utf-8'):
            raise ValueError(f'Update policy translations after changing {name.upper()}.md')


def script_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')


def policy_html(markdown):
    """Render the small policy subset; escape all source markup and allow HTTPS links."""
    markdown = markdown.replace('(LICENSE)', '(https://github.com/arty-kk/vibe-coding/blob/main/LICENSE)')
    paragraphs = []
    for raw in markdown.strip().split('\n\n'):
        heading = raw.startswith('# ')
        text = html.escape(raw[2:] if heading else raw)
        text = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'<a href="\2">\1</a>', text)
        tag = 'h1' if heading else 'p'
        paragraphs.append(f'<{tag}>{text}</{tag}>')
    return '\n'.join(paragraphs)


def build(destination=SITE):
    destination.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((PLUGIN/'catalog.json').read_text(encoding='utf-8'))
    manifest = json.loads((PLUGIN/'plugin.json').read_text(encoding='utf-8'))
    locales = load_locales()
    rows = catalog['recipes']
    validate_locales(locales, rows)
    for locale in locales.values():
        locale['policy'] = {name: policy_html(text) for name, text in locale['policy'].items()}
    picker = '<label class="language-label"><span data-i18n="language">{{language}}</span><select id="language">'
    picker += ''.join(f'<option value="{code}" lang="{code}">{label}</option>' for code, label in LANGUAGES.items())
    picker += '</select></label>'
    common = {
        '__STYLE__': (SOURCE/'style.css').read_text(encoding='utf-8'),
        '__LANGUAGE_PICKER__': picker,
        '__LANGUAGE_JS__': (SOURCE/'language.js').read_text(encoding='utf-8'),
        '__VERSION__': html.escape(manifest['version']),
        '__SKILLS__': str(catalog['skills']),
        '__COUNT__': str(len(rows)),
        '__DOMAINS__': str(len({row['group'] for row in rows})),
    }
    expanded = []
    for row in rows:
        path = (PLUGIN/row['path']).resolve()
        if not path.is_relative_to(PLUGIN.resolve()):
            raise ValueError(f'Escaping recipe path: {row["path"]}')
        expanded.append({key: row[key] for key in ('id', 'title', 'skill', 'mode')} | {'body': path.read_text(encoding='utf-8')})
    for page in ('index', 'privacy', 'terms'):
        template = 'catalog.html' if page == 'index' else 'policy.html'
        replacements = dict(common)
        if page == 'index':
            replacements.update({
                '__RECIPE_DATA__': script_json(expanded),
                '__LOCALE_DATA__': script_json({code: {k: v for k, v in data.items() if k != 'policy'} for code, data in locales.items()}),
                '__CATALOG_JS__': (SOURCE/'catalog.js').read_text(encoding='utf-8'),
            })
        else:
            replacements.update({
                '__POLICY_NAME__': page,
                '__POLICY_TITLE__': html.escape(locales['en']['ui'][page]),
                '__POLICY_BODY__': locales['en']['policy'][page],
                '__LOCALE_DATA__': script_json({code: {'ui': data['ui'], 'policy': {page: data['policy'][page]}} for code, data in locales.items()}),
            })
        output = (SOURCE/template).read_text(encoding='utf-8')
        # Translate template markup before embedding recipe text and JSON.
        translate = lambda text: re.sub(r'\{\{(\w+)\}\}', lambda match: html.escape(locales['en']['ui'][match[1]]), text)
        output = translate(output)
        replacements['__LANGUAGE_PICKER__'] = translate(picker)
        output = re.sub(r'__[A-Z_]+__', lambda match: replacements[match[0]], output)
        (destination/f'{page}.html').write_text(output, encoding='utf-8', newline='\n')
    shutil.copy2(PLUGIN/'assets/icon.png', destination/'icon.png')
    (destination/'.nojekyll').touch()
    print('Built English-first catalog and policies: en, es, ru, zh-CN')


if __name__ == '__main__':
    build()

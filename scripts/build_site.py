#!/usr/bin/env python3
"""Build the public website from the catalog renderer shipped in the plugin."""
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'docs'
PLUGIN = ROOT/'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN/'scripts'))
from catalog_site import (LANGUAGES, load_locales, validate_locales, script_json,
                          policy_html, common_resources, render_template, render_catalog)


def build(destination=SITE):
    destination.mkdir(parents=True, exist_ok=True)
    rows = json.loads((PLUGIN/'catalog.json').read_text(encoding='utf-8'))['recipes']
    locales = load_locales()
    validate_locales(locales, rows)
    for name in ('privacy', 'terms'):
        if locales['en']['policy'][name] != (ROOT/f'{name.upper()}.md').read_text(encoding='utf-8'):
            raise ValueError(f'Update policy translations after changing {name.upper()}.md')
    (destination/'index.html').write_text(render_catalog(rows, offline=False), encoding='utf-8', newline='\n')
    template = (ROOT/'site/policy.html').read_text(encoding='utf-8')
    for page in ('privacy', 'terms'):
        data = {code: {'ui': locale['ui'], 'policy': {page: policy_html(locale['policy'][page])}}
                for code, locale in locales.items()}
        replacements = common_resources() | {
            '__POLICY_NAME__': page,
            '__POLICY_TITLE__': locales['en']['ui'][page],
            '__POLICY_BODY__': data['en']['policy'][page],
            '__LOCALE_DATA__': script_json(data),
        }
        output = render_template(template, replacements, locales['en']['ui'])
        (destination/f'{page}.html').write_text(output, encoding='utf-8', newline='\n')
    shutil.copy2(PLUGIN/'assets/icon.png', destination/'icon.png')
    (destination/'.nojekyll').touch()
    print('Built English-first catalog and policies: en, es, ru, zh-CN')


if __name__ == '__main__':
    build()

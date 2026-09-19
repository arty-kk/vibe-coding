#!/usr/bin/env python3
"""Build the static catalog and policy pages using the standard library."""
from pathlib import Path
import html
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
PLUGIN = ROOT / 'plugins/vibe-coding'
SITE.mkdir(exist_ok=True)
catalog = (PLUGIN / 'CATALOG.html').read_text(encoding='utf-8')
catalog = catalog.replace('href="README.md"', 'href="https://github.com/arty-kk/vibe-coding#readme"')
catalog = catalog.replace('</head>', '<link rel="icon" href="icon.png"><meta name="description" content="Vibe Coding: 43 Codex skills and 221 engineering workflows for mapping, review, debugging and verification."></head>')
catalog = catalog.replace('<div class="starter"', '<p><a href="https://github.com/arty-kk/vibe-coding#install">Install Vibe Coding</a> · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></p><div class="starter"')
(SITE / 'index.html').write_text(catalog, encoding='utf-8', newline='\n')
shutil.copy2(PLUGIN / 'assets/icon.png', SITE / 'icon.png')
for name, source in [('privacy', 'PRIVACY.md'), ('terms', 'TERMS.md')]:
    text = (ROOT / source).read_text(encoding='utf-8')
    text = text.replace('(LICENSE)', '(https://github.com/arty-kk/vibe-coding/blob/main/LICENSE)')
    def paragraph(raw):
        escaped = html.escape(raw)
        escaped = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'<a href="\2">\1</a>', escaped)
        return '<h1>'+escaped[2:]+'</h1>' if escaped.startswith('# ') else '<p>'+escaped+'</p>'
    body = '\n'.join(paragraph(p) for p in text.split('\n\n'))
    page = f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vibe Coding — {name.title()}</title><style>body{{max-width:760px;margin:60px auto;padding:0 24px;background:#101212;color:#f0f4ed;font:17px/1.7 system-ui}}a{{color:#c3f078}}p{{overflow-wrap:anywhere}}</style><a href="./">Vibe Coding</a><main>{body}</main></html>'
    (SITE / (name+'.html')).write_text(page, encoding='utf-8', newline='\n')
(SITE / '.nojekyll').touch()
print('Built docs/index.html, privacy.html and terms.html')

"""Compile a bounded, versioned public library; no runtime network or file access."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent / 'plugins/vibe-coding'


def build_library():
    catalog = json.loads((PLUGIN / 'catalog.json').read_text())
    version = json.loads((PLUGIN / 'plugin.json').read_text())['version']
    locales = {code: json.loads((PLUGIN / f'assets/catalog/locales/{code}.json').read_text())
               for code in ('en', 'es', 'ru', 'zh-CN')}
    files = {}

    def include(path):
        absolute = (PLUGIN / path).resolve()
        if not absolute.is_relative_to(PLUGIN) or not absolute.is_file():
            raise ValueError(f'Missing or escaping library resource: {path}')
        data = absolute.read_bytes()
        files[path] = {'path': path, 'text': data.decode('utf-8'),
                       'sha256': hashlib.sha256(data).hexdigest()}

    for path in sorted((PLUGIN / 'references').glob('*.md')):
        include(path.relative_to(PLUGIN).as_posix())
    for path in sorted((PLUGIN / 'skills').glob('*/SKILL.md')):
        include(path.relative_to(PLUGIN).as_posix())
    for row in catalog['recipes']:
        include(row['path'])
        include(f"skills/{row['skill']}/SKILL.md")
        if files[row['path']]['sha256'] != row['sha256']:
            raise ValueError(f'Stale catalog digest: {row["id"]}')
        dependencies = []
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', files[row['path']]['text']):
            if urlsplit(link).scheme or link.startswith('#'):
                continue
            resolved = ((PLUGIN / row['path']).parent / unquote(link.split('#')[0])).resolve()
            if not resolved.is_relative_to(PLUGIN) or not resolved.is_file():
                raise ValueError(f'Broken recipe link: {row["id"]}: {link}')
            name = resolved.relative_to(PLUGIN).as_posix()
            # Alternative recipes remain discoverable, not automatically loaded.
            if name.startswith('references/') and name not in ('references/catalog.md', 'references/hosts.md'):
                include(name)
                dependencies.append(name)
        row['dependencies'] = sorted(set(dependencies))
    digest = hashlib.sha256(''.join(f'{path}:{file["sha256"]}\n'
                                   for path, file in sorted(files.items())).encode()).hexdigest()
    return {'version': json.loads((HERE / 'package.json').read_text())['version'],
            'instructionVersion': version, 'digest': digest,
            'recipes': catalog['recipes'], 'skillCount': catalog['skills'], 'files': files,
            'locales': {code: {key: locale[key] for key in ('titles', 'summaries', 'categories', 'modes')}
                        for code, locale in locales.items()}}


if __name__ == '__main__':
    library = build_library()
    output = HERE / 'generated'
    output.mkdir(exist_ok=True)
    (output / 'library.json').write_text(json.dumps(library, ensure_ascii=False, separators=(',', ':')) + '\n')
    engine = (HERE.parent / 'site/catalog-engine.js').read_text()
    wrapper = "'use strict';\n(() => {\n"
    export = "  if (typeof module !== 'undefined' && module.exports) module.exports = engine;\n  else window.VibeCatalog = engine;\n})();\n"
    if not engine.startswith(wrapper) or not engine.endswith(export):
        raise ValueError('Catalog engine wrapper changed; review the ESM projection.')
    (output / 'catalog-engine.js').write_text(engine[len(wrapper):-len(export)] + 'export default engine;\n')
    print(f"Compiled {len(library['recipes'])} workflows, {len(library['files'])} instruction files; {library['digest']}")

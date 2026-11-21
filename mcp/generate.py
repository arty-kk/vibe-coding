"""Compile a bounded, versioned public library; no runtime network or file access."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent / 'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN/'scripts'))
from workflow_graph import load_workflows
from topic_index import build_topics


def build_library():
    catalog = json.loads((PLUGIN / 'catalog.json').read_text(encoding='utf-8'))
    workflows = load_workflows(PLUGIN, catalog['recipes'])
    discovery = build_topics(PLUGIN, catalog['recipes'], workflows)
    version = json.loads((PLUGIN / 'plugin.json').read_text(encoding='utf-8'))['version']
    locales = {code: json.loads((PLUGIN / f'assets/catalog/locales/{code}.json').read_text(encoding='utf-8'))
               for code in ('en', 'es', 'ru', 'zh-CN')}
    files = {}
    helpers = {
        'web-design-kit': {'skills/vibe-web-art-direction/scripts/compile_design_kit.py',
                           'skills/vibe-web-art-direction/assets/design-kit.example.json'},
        'web-experience-brief': {'skills/vibe-landing/scripts/check_web_packet.py'},
    }

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
        sources = [row['path'], f"skills/{row['skill']}/SKILL.md", 'references/workflow.md', 'references/cycles.md']
        for source in sources:
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', files[source]['text']):
                if urlsplit(link).scheme or link.startswith('#'):
                    continue
                resolved = ((PLUGIN / source).parent / unquote(link.split('#')[0])).resolve()
                if not resolved.is_relative_to(PLUGIN) or not resolved.is_file():
                    raise ValueError(f'Broken recipe link: {row["id"]}: {link}')
                name = resolved.relative_to(PLUGIN).as_posix()
                # Alternative recipes remain discoverable, not automatically loaded.
                if name.startswith('references/') and name not in ('references/catalog.md', 'references/hosts.md'):
                    include(name)
                    dependencies.append(name)
                elif source == row['path'] and name in helpers.get(row['id'], ()):
                    # Linked textual helpers are loaded only by their focused current prompt.
                    include(name)
                    dependencies.append(name)
        row['dependencies'] = sorted(set(dependencies))
    config_hashes = {name: hashlib.sha256((PLUGIN/name).read_bytes()).hexdigest()
                     for name in ('workflows.json', 'assets/catalog/search-lexicon.json', 'assets/catalog/search-topics.json', 'assets/catalog/engine.js')}
    snapshot = {'version': json.loads((HERE / 'package.json').read_text(encoding='utf-8'))['version'],
            'instructionVersion': version,
            'recipes': catalog['recipes'], 'skillCount': catalog['skills'], 'files': files,
            'workflowSpec': workflows,
            'discovery': discovery,
            'searchLexicon': json.loads((PLUGIN/'assets/catalog/search-lexicon.json').read_text(encoding='utf-8')),
            'configDigests': config_hashes,
            'locales': {code: {key: locale[key] for key in ('titles', 'summaries', 'categories', 'modes')}
                        for code, locale in locales.items()}}
    snapshot['digest'] = hashlib.sha256(json.dumps(snapshot, ensure_ascii=False, sort_keys=True,
                                                  separators=(',', ':')).encode()).hexdigest()
    return snapshot


def build_engine():
    engine = (PLUGIN/'assets/catalog/engine.js').read_text(encoding='utf-8')
    if engine != (HERE.parent/'site/catalog-engine.js').read_text(encoding='utf-8'):
        raise ValueError('Public and offline search engines differ; synchronize the canonical engine.')
    wrapper = "'use strict';\n(() => {\n"
    export = "  if (typeof module !== 'undefined' && module.exports) module.exports = engine;\n  else window.VibeCatalog = engine;\n})();\n"
    if not engine.startswith(wrapper) or not engine.endswith(export):
        raise ValueError('Catalog engine wrapper changed; review the ESM projection.')
    return engine[len(wrapper):-len(export)] + 'export default engine;\n'


def build_metadata(library):
    recipes = library['recipes']
    return {
        'version': library['version'],
        'instructionVersion': library['instructionVersion'],
        'digest': library['digest'],
        'workflowCount': len(recipes),
        'skillCount': library['skillCount'],
        'languages': list(library['locales']),
        'modes': sorted({row['mode'] for row in recipes}),
        'domains': sorted({row['skill'] for row in recipes}),
    }


if __name__ == '__main__':
    library = build_library()
    output = HERE / 'generated'
    output.mkdir(exist_ok=True)
    (output / 'library.json').write_text(json.dumps(library, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8', newline='\n')
    (output / 'metadata.json').write_text(json.dumps(build_metadata(library), separators=(',', ':')) + '\n', encoding='utf-8', newline='\n')
    (output / 'catalog-engine.js').write_text(build_engine(), encoding='utf-8', newline='\n')
    print(f"Compiled {len(library['recipes'])} workflows, {len(library['files'])} instruction files; {library['digest']}")

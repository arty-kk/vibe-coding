import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / 'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN / 'scripts'))
from validate import validate
import catalog


class PackageTests(unittest.TestCase):
    def test_shipped_package(self):
        self.assertEqual([], validate(PLUGIN))

    def test_marketplace_resolves_plugin(self):
        marketplace = json.loads((REPO/'.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        self.assertEqual('vibe-coding', marketplace['name'])
        entry = marketplace['plugins'][0]
        self.assertEqual(PLUGIN.resolve(), (REPO/entry['source']['path']).resolve())
        self.assertEqual('AVAILABLE', entry['policy']['installation'])

    def test_search_filters_and_empty_result(self):
        rows = catalog.load_catalog()['recipes']
        found = catalog.search(rows, 'webhook', mode='check')
        self.assertTrue(found)
        self.assertTrue(all(r['mode']=='check' for r in found))
        self.assertEqual([], catalog.search(rows, 'no-matching-recipe-47291'))
        self.assertEqual(3, len(catalog.search(rows, 'платежи')))

    def test_reading_outside_plugin_is_rejected(self):
        with self.assertRaises(ValueError):
            catalog.contained_path('../../README.md')

    def test_new_boundaries_are_discoverable_across_languages(self):
        rows = catalog.load_catalog()['recipes']
        for query, skill in [('MCP', 'vibe-mcp'), ('服务器', 'vibe-mcp'),
                             ('SSR', 'vibe-web'), ('hidratacion', 'vibe-web'),
                             ('гидратация', 'vibe-web')]:
            with self.subTest(query=query):
                found = catalog.search(rows, query)
                self.assertEqual(3, len(found))
                self.assertTrue(all(row['skill'] == skill for row in found))
        self.assertEqual(['oauth-oidc-session-check'], [r['id'] for r in catalog.search(rows, 'OAuth', mode='check')])

    def test_old_or_incomplete_instructions_are_detected(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/'vibe-coding'
            shutil.copytree(PLUGIN, target)
            entry = target/'skills/vibe-mcp/SKILL.md'
            entry.write_text(entry.read_text(encoding='utf-8')+'\n## Task-sub quality\n', encoding='utf-8')
            self.assertTrue(any('Legacy runtime instruction' in e for e in validate(target)))
            locale_path = target/'assets/catalog/locales/zh-CN.json'
            locale = json.loads(locale_path.read_text(encoding='utf-8'))
            del locale['titles']['mcp-server-audit']
            locale_path.write_text(json.dumps(locale), encoding='utf-8')
            self.assertTrue(any('Invalid catalog localization' in e for e in validate(target)))

    def test_stale_catalog_interface_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/'vibe-coding'
            shutil.copytree(PLUGIN, target)
            style = target/'assets/catalog/style.css'
            style.write_text(style.read_text(encoding='utf-8')+'\nbody {margin: 1px;}\n', encoding='utf-8')
            self.assertTrue(any('Stale HTML interface' in e for e in validate(target)))

    def test_recipe_corruption_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'vibe-coding'
            shutil.copytree(PLUGIN,target)
            recipe=next((target/'skills').glob('*/references/*.md'))
            recipe.write_text(recipe.read_text(encoding='utf-8')+'\nUnexpected change.\n')
            errors=validate(target)
            self.assertTrue(any('Stale recipe hash' in e for e in errors),errors)
            self.assertTrue(any('Stale HTML recipe' in e for e in errors),errors)

    def test_missing_recipe_and_escaping_link_are_detected(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'vibe-coding'
            shutil.copytree(PLUGIN,target)
            next((target/'skills').glob('*/references/*.md')).unlink()
            with (target/'README.md').open('a') as f:f.write('\n[Outside](../../outside.md)\n')
            errors=validate(target)
            self.assertTrue(any('Missing/escaping recipe' in e for e in errors),errors)
            self.assertTrue(any('Broken/escaping link' in e for e in errors),errors)

    def test_manifest_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'vibe-coding';shutil.copytree(PLUGIN,target)
            path=target/'plugin.json';m=json.loads(path.read_text(encoding='utf-8'));m['version']='9.0.0';path.write_text(json.dumps(m))
            self.assertIn('Manifest mismatch: version',validate(target))

    def test_reproducible_archive(self):
        with tempfile.TemporaryDirectory() as d:
            paths=[Path(d)/'a.zip',Path(d)/'b.zip']
            for path in paths:
                subprocess.run([sys.executable,str(PLUGIN/'scripts/package.py'),'--output',str(path)],check=True,capture_output=True)
            self.assertEqual(paths[0].read_bytes(),paths[1].read_bytes())
            with zipfile.ZipFile(paths[0]) as z:
                self.assertIsNone(z.testzip())
                self.assertIn('vibe-coding/plugin.json',z.namelist())
                self.assertIn('vibe-coding/LICENSE',z.namelist())
                self.assertFalse(any('__pycache__' in n or '/.git/' in n for n in z.namelist()))
                z.extractall(Path(d)/'extracted')
            extracted = Path(d)/'extracted/vibe-coding'
            result = subprocess.run([sys.executable, str(extracted/'scripts/catalog.py'), 'search', 'MCP', '--lang', 'zh-CN', '--json'],
                                    check=True, capture_output=True, encoding='utf-8')
            rows = json.loads(result.stdout)
            self.assertEqual(3, len(rows))
            self.assertTrue(all('MCP' in r['title'] and '请用简体中文' in r['example'] for r in rows))
            subprocess.run([sys.executable, str(extracted/'scripts/validate.py')], check=True, capture_output=True)


if __name__ == '__main__': unittest.main()

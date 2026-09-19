import copy
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import build_site


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.locales = build_site.load_locales()
        self.rows = json.loads((build_site.PLUGIN/'catalog.json').read_text(encoding='utf-8'))['recipes']

    def test_complete_translations_for_every_shipped_workflow(self):
        build_site.validate_locales(self.locales, self.rows)
        self.assertEqual({'en', 'es', 'ru', 'zh-CN'}, set(self.locales))
        self.assertEqual(221, len(self.locales['en']['titles']))
        for locale in self.locales.values():
            self.assertEqual({'{skill}', '{title}', '{id}'}, set(re.findall(r'\{\w+\}', locale['ui']['prompt'])))

    def test_missing_translation_and_broken_prompt_fail_build(self):
        broken = copy.deepcopy(self.locales)
        del broken['es']['titles'][self.rows[0]['id']]
        with self.assertRaisesRegex(ValueError, 'es: missing'):
            build_site.validate_locales(broken, self.rows)
        broken = copy.deepcopy(self.locales)
        broken['zh-CN']['ui']['prompt'] = 'Use ${skill}.'
        with self.assertRaisesRegex(ValueError, 'mismatched placeholders'):
            build_site.validate_locales(broken, self.rows)

    def test_english_first_pages_preserve_recipe_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            build_site.build(destination)
            page = (destination/'index.html').read_text(encoding='utf-8')
            self.assertIn('<html lang="en">', page)
            self.assertIn('<title>Vibe Coding — workflow catalog</title>', page)
            self.assertIn('Pick a task.', page)
            match = re.search(r'id="recipe-data">(.*?)</script>', page, re.S)
            shipped = {row['id']: row for row in json.loads(match[1])}
            self.assertEqual({row['id'] for row in self.rows}, set(shipped))
            for row in self.rows:
                self.assertEqual((build_site.PLUGIN/row['path']).read_text(encoding='utf-8'), shipped[row['id']]['body'])
            locale_data = json.loads(re.search(r'id="locale-data">(.*?)</script>', page, re.S)[1])
            self.assertEqual(self.locales['ru']['titles'], locale_data['ru']['titles'])
            for name in ('privacy', 'terms'):
                policy = (destination/f'{name}.html').read_text(encoding='utf-8')
                self.assertIn('<html lang="en">', policy)
                for code in self.locales:
                    self.assertIn(f'value="{code}"', policy)
                self.assertIn(build_site.policy_html(self.locales['en']['policy'][name]), policy)
            first = {path.name: path.read_bytes() for path in destination.iterdir()}
            build_site.build(destination)
            self.assertEqual(first, {path.name: path.read_bytes() for path in destination.iterdir()})

    def test_embedded_json_cannot_close_its_script(self):
        value = {'text': '</script><script>alert(1)</script>\u2028\u2029'}
        encoded = build_site.script_json(value)
        self.assertNotIn('<', encoded)
        self.assertEqual(value, json.loads(encoded))

    def test_policy_markup_is_escaped_and_license_remains_linked(self):
        rendered = build_site.policy_html('# Privacy\n\n<script>alert(1)</script> [MIT](LICENSE)')
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertIn('href="https://github.com/arty-kk/vibe-coding/blob/main/LICENSE"', rendered)


if __name__ == '__main__':
    unittest.main()

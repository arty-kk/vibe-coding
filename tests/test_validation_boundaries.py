import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PLUGIN = Path(__file__).resolve().parents[1]/'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN/'scripts'))
from validate import validate
from release_files import release_files


class ValidationBoundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'vibe-coding'
        shutil.copytree(PLUGIN, self.root, ignore=shutil.ignore_patterns('__pycache__'))

    def test_unapproved_file_blocks_packaging_without_creating_archive(self):
        (self.root/'.env.production').write_text('SYNTHETIC_CANARY=not-a-secret\n', encoding='utf-8')
        output = Path(self.temp.name)/'release.zip'
        result = subprocess.run([sys.executable, str(self.root/'scripts/package.py'), '--output', str(output)], capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('Unapproved release file: .env.production', result.stderr)
        self.assertNotIn('SYNTHETIC_CANARY', result.stderr)
        self.assertFalse(output.exists())
        self.assertFalse(output.with_suffix('.zip.tmp').exists())

    def test_explicit_sensitive_file_is_still_rejected(self):
        path = self.root/'package-files.json'
        inventory = json.loads(path.read_text(encoding='utf-8'))
        (self.root/'credentials.json').write_text('{"synthetic": true}', encoding='utf-8')
        inventory['files'] = sorted(inventory['files'] + ['credentials.json'])
        path.write_text(json.dumps(inventory), encoding='utf-8')
        self.assertTrue(any('Sensitive file' in error for error in release_files(self.root)[1]))

    def test_malformed_and_escaping_inventory_are_reported(self):
        path = self.root/'package-files.json'
        for value in [[], {'version': 1, 'files': [1]}, {'version': 1, 'files': ['../outside', 'package-files.json']}]:
            with self.subTest(value=value):
                path.write_text(json.dumps(value), encoding='utf-8')
                self.assertTrue(release_files(self.root)[1])

    def test_invalid_yaml_and_duplicate_keys_are_reported(self):
        path = self.root/'skills/vibe-ai/SKILL.md'
        original = path.read_text(encoding='utf-8')
        for extra in ['metadata: [unterminated\n', 'name: vibe-ai\n', 'metadata: scalar\n']:
            with self.subTest(extra=extra):
                path.write_text(original.replace('\n---\n', '\n'+extra+'---\n', 1), encoding='utf-8')
                errors = validate(self.root)
                self.assertTrue(any('skills/vibe-ai/SKILL.md:' in e for e in errors), errors)

    def test_invalid_ui_metadata_is_reported(self):
        path = self.root/'skills/vibe-ai/agents/openai.yaml'
        path.write_text(path.read_text(encoding='utf-8') + '\npolicy:\n  allow_implicit_invocation: "false"\n', encoding='utf-8')
        self.assertTrue(any('invalid invocation policy' in e for e in validate(self.root)))

    def test_missing_catalog_fields_are_errors_not_tracebacks(self):
        path = self.root/'catalog.json'
        original = json.loads(path.read_text(encoding='utf-8'))
        for field in ['mode', 'id', 'path', 'skill', 'sha256']:
            with self.subTest(field=field):
                value = json.loads(json.dumps(original))
                del value['recipes'][0][field]
                path.write_text(json.dumps(value), encoding='utf-8')
                self.assertIn(f'catalog.json: recipes[0]: missing or invalid {field}', validate(self.root))

    def test_recipe_must_be_reachable_by_its_actual_link(self):
        path = self.root/'skills/vibe-mcp/SKILL.md'
        path.write_text(path.read_text(encoding='utf-8').replace('](references/mcp-server-audit.md)', '](references/mcp-server-polish.md)'), encoding='utf-8')
        self.assertTrue(any('Recipe not reachable from skill: mcp-server-audit' in e for e in validate(self.root)))


if __name__ == '__main__':
    unittest.main()

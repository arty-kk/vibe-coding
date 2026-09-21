import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'plugins/vibe-coding'
sys.path.insert(0,str(PLUGIN/'scripts'))
from validate import validate


class HostTests(unittest.TestCase):
    def test_marketplaces_resolve_the_same_self_contained_plugin(self):
        codex=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        claude=json.loads((ROOT/'.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        self.assertEqual('vibe-coding',claude['name'])
        self.assertEqual(codex['plugins'][0]['source']['path'],claude['plugins'][0]['source'])
        self.assertEqual(PLUGIN.resolve(),(ROOT/claude['plugins'][0]['source']).resolve())
        self.assertEqual([],validate(PLUGIN))
        root_manifest=json.loads((ROOT/'.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        packaged=json.loads((PLUGIN/'.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual((PLUGIN/'skills').resolve(),(ROOT/root_manifest.pop('skills')).resolve())
        self.assertEqual(packaged,root_manifest)
        self.assertFalse(list(PLUGIN.rglob('CLAUDE.md')))
        self.assertFalse(list(PLUGIN.rglob('AGENTS.md')))
        for skill in (PLUGIN/'skills').glob('*/SKILL.md'):
            source=skill.read_text(encoding='utf-8')
            self.assertIn('../../references/workflow.md',source)

    def test_cli_returns_claude_namespace_in_all_languages(self):
        for lang in ['en','es','ru','zh-CN']:
            result=subprocess.run([sys.executable,str(PLUGIN/'scripts/catalog.py'),'search','MCP','--host','claude','--lang',lang,'--json'],text=True,encoding='utf-8',capture_output=True,check=True)
            rows=json.loads(result.stdout)
            self.assertTrue(rows)
            for row in rows:
                self.assertTrue(row['example'].startswith('/vibe-coding:'+row['skill']))
                self.assertIn(row['id'],row['example'])
                self.assertNotIn('$vibe-',row['example'])


if __name__=='__main__':unittest.main()

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import package_openai_mcp as distribution


class MCPDistributionTests(unittest.TestCase):
    def test_runtime_bundle_is_reproducible_and_review_metadata_is_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / 'first.zip'
            second = Path(directory) / 'second.zip'
            video = 'https://github.com/arty-kk/vibe-coding/releases/download/v1.5.0/vibe-coding-library-demo.mp4'
            distribution.package(first, video)
            distribution.package(second, video)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                prefix = 'vibe-coding-library/'
                self.assertEqual({prefix + name for name in distribution.FILES}, set(archive.namelist()))
                portable = json.loads(archive.read(prefix + 'plugin.json'))
                codex = json.loads(archive.read(prefix + '.codex-plugin/plugin.json'))
                review = portable['extensions']['com.openai']['review']
                self.assertEqual(review, codex['extensions']['com.openai']['review'])
                self.assertEqual(5, len(review['test_cases']['positive']))
                self.assertEqual(3, len(review['test_cases']['negative']))
                self.assertFalse(review['commerce'])
                for cases in review['test_cases'].values():
                    for case in cases:
                        self.assertNotIn('calls', case)
                        self.assertTrue(case['description'])
                        self.assertTrue(case['prompt'])
                        self.assertTrue(case['expected_behavior'])
                self.assertEqual(video, review['demo_recording_url'])
                self.assertEqual('1.5.0', portable['version'])
                self.assertEqual(1, sum(name.endswith('/SKILL.md') for name in archive.namelist()))
                self.assertEqual((distribution.PLUGIN/'skills/vibe-library/SKILL.md').read_bytes(),
                                 archive.read(prefix + 'skills/vibe-library/SKILL.md'))
                self.assertNotRegex(portable['extensions']['com.openai']['interface']['longDescription'], r'Claude|Codex|ChatGPT')

    def test_video_url_cannot_contain_credentials_or_use_a_local_transport(self):
        for url in ['http://127.0.0.1/demo.mp4', 'https://user:secret@example.invalid/demo', 'https://example.invalid/a b']:
            with self.subTest(url=url), tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(ValueError):
                    distribution.package(Path(directory)/'package.zip', url)

    def test_marketplaces_offer_both_variants_with_consistent_source_paths(self):
        codex = json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())
        claude = json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
        expected = {'vibe-coding', 'vibe-coding-library'}
        self.assertEqual(expected, {row['name'] for row in codex['plugins']})
        self.assertEqual(expected, {row['name'] for row in claude['plugins']})
        for row in claude['plugins']:
            peer = next(item for item in codex['plugins'] if item['name'] == row['name'])
            self.assertEqual(row['source'], peer['source']['path'])
            self.assertTrue((ROOT/row['source']/'plugin.json').is_file())


if __name__ == '__main__':
    unittest.main()

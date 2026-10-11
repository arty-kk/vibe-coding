import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import package_openai as distribution


class OpenAIDistributionTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((distribution.PLUGIN / '.codex-plugin/plugin.json').read_text())

    def errors(self, manifest):
        return distribution.submission_errors(manifest, distribution.PLUGIN)

    def test_real_listing_meets_final_submission_limits(self):
        self.assertEqual([], self.errors(self.manifest))

    def test_directory_limits_are_stricter_than_upload_limits(self):
        self.manifest['interface']['shortDescription'] = 'x' * 31
        self.assertIn('shortDescription: too long', self.errors(self.manifest))

    def test_credentials_cannot_be_embedded_in_public_listing_urls(self):
        self.manifest['interface']['supportURL'] = 'https://example:fixture-only@example.invalid/support'
        self.assertIn('supportURL: public HTTPS URL without credentials required', self.errors(self.manifest))

    def test_unsupported_formatting_and_multiline_starter_are_rejected(self):
        self.manifest['interface']['displayName'] = 'Vibe\u200bCoding'
        self.manifest['interface']['defaultPrompt'] = ['Review\nthis branch']
        self.assertIn('displayName: unsupported control or formatting character', self.errors(self.manifest))
        self.assertIn('defaultPrompt: must be one line', self.errors(self.manifest))

    def test_unicode_equivalent_starters_do_not_bypass_uniqueness(self):
        self.manifest['interface']['defaultPrompt'] = ['Review café', 'Review cafe\u0301']
        self.assertIn('defaultPrompt: duplicate after normalization', self.errors(self.manifest))

    def test_mcp_configuration_cannot_disguise_a_skills_only_distribution(self):
        self.manifest['mcpServers'] = './.mcp.json'
        self.assertIn('Unsupported runtime or screenshot declaration in the skills-only distribution', self.errors(self.manifest))

    def test_icon_cannot_escape_the_package(self):
        self.manifest['interface']['logo'] = './../private.png'
        self.assertIn('logo: missing or escaping asset', self.errors(self.manifest))

    def test_semver_rejects_leading_zeroes_and_accepts_valid_prerelease(self):
        for version in ['01.4.1', '1.4.1-01', '1.4.1-rc.01']:
            with self.subTest(version=version):
                candidate = copy.deepcopy(self.manifest)
                candidate['version'] = version
                self.assertIn('version: semantic version required', self.errors(candidate))
        self.manifest['version'] = '1.4.1-rc.1+build.01'
        self.assertEqual([], self.errors(self.manifest))

    def test_projection_preserves_every_skill_resource_and_shared_package(self):
        files, errors = distribution.release_files(distribution.PLUGIN)
        self.assertEqual([], errors)
        before = {p.relative_to(distribution.PLUGIN).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        with tempfile.TemporaryDirectory() as directory:
            projected = Path(directory) / 'vibe-coding'
            for source in files:
                target = projected / source.relative_to(distribution.PLUGIN)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            manifest = distribution.project_listing(projected)
            self.assertEqual([], distribution.submission_errors(manifest, projected))
            self.assertEqual([], distribution.validate(projected))
            changed = {name for name, digest in before.items() if hashlib.sha256((projected / name).read_bytes()).hexdigest() != digest}
            self.assertEqual({'plugin.json', '.codex-plugin/plugin.json'}, changed)
            portable = json.loads((projected / 'plugin.json').read_text())
            self.assertEqual(manifest['interface'], portable['extensions']['com.openai']['interface'])
            self.assertEqual(manifest['extensions']['com.openai']['publication'], portable['extensions']['com.openai']['publication'])
            self.assertNotRegex(manifest['interface']['longDescription'], r'Claude|Codex|ChatGPT')
            self.assertEqual(self.manifest['version'], manifest['version'])
        after = {p.relative_to(distribution.PLUGIN).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()

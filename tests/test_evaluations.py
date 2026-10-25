import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT/'review/evaluations/1.2.0.json'
CURRENT = ROOT/'review/evaluations/1.3.0.json'
WEBSITE = ROOT/'review/evaluations/site-2026-09-21.json'
REVISION = ROOT/'review/evaluations/1.4.0.json'
LISTING = ROOT/'review/evaluations/1.4.1.json'
LIBRARY = ROOT/'review/evaluations/1.5.0.json'
PORTABILITY = ROOT/'review/evaluations/1.5.1.json'
SITE_REFRESH = ROOT/'review/evaluations/site-2026-10-25.json'


class EvaluationRecordTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECORD.read_text(encoding='utf-8'))
        self.current = json.loads(CURRENT.read_text(encoding='utf-8'))
        self.website = json.loads(WEBSITE.read_text(encoding='utf-8'))
        self.revision = json.loads(REVISION.read_text(encoding='utf-8'))
        self.listing = json.loads(LISTING.read_text(encoding='utf-8'))
        self.library = json.loads(LIBRARY.read_text(encoding='utf-8'))
        self.portability = json.loads(PORTABILITY.read_text(encoding='utf-8'))
        self.site_refresh = json.loads(SITE_REFRESH.read_text(encoding='utf-8'))

    def site_refresh_fingerprint(self, name, expected):
        change = self.site_refresh['changes'].get(name)
        if change:
            self.assertEqual(expected, change['before'], 'Website refresh must retain the released baseline: '+name)
            self.assertTrue(change['review'])
            return change['after']
        return expected

    def portability_fingerprint(self, name, expected):
        change = self.portability['changes'].get(name)
        if change:
            self.assertEqual(expected, change['before'], 'Portability revision must retain the previous fingerprint: '+name)
            self.assertTrue(change['review'])
            expected = change['after']
        return self.site_refresh_fingerprint(name, expected)

    def library_fingerprint(self, name, expected):
        change = self.library['changes'].get(name)
        if change:
            self.assertEqual(expected, change['before'], 'MCP revision must preserve the previous fingerprint: '+name)
            self.assertTrue(change['review'])
            expected = change['after']
        return self.portability_fingerprint(name, expected)

    def listing_fingerprint(self, name, expected):
        change = self.listing['changes'].get(name)
        if change:
            self.assertEqual(expected, change['before'], 'Listing revision must preserve the 1.4.0 baseline: '+name)
            self.assertTrue(change['review'])
            expected = change['after']
        return self.library_fingerprint(name, expected)

    def revised_fingerprint(self, name, expected):
        change = self.revision['changes'].get(name)
        if change:
            self.assertEqual(expected, change['before'], 'Revision must start from the recorded baseline: '+name)
            self.assertTrue(change['review'])
            expected = change['after']
        return self.listing_fingerprint(name, expected)

    def test_record_matches_current_instructions_inputs_and_artifacts(self):
        for section in ['instructions', 'inputs_and_artifacts']:
            self.assertTrue(self.record[section])
            for name, expected in self.record[section].items():
                with self.subTest(path=name):
                    path = (ROOT/name).resolve()
                    self.assertTrue(path.is_relative_to(ROOT))
                    change = self.current['baseline_changes'].get(name) if section == 'instructions' else None
                    if change:
                        self.assertEqual(expected, change['before'])
                        self.assertTrue(change['review'])
                        expected = change['after']
                    expected = self.revised_fingerprint(name, expected)
                    self.assertEqual(expected, hashlib.sha256(path.read_bytes()).hexdigest(), 'Evaluation is stale: re-evaluate affected behavior')

    def test_current_release_has_separate_evidence_and_complete_instruction_fingerprints(self):
        self.assertEqual(hashlib.sha256(RECORD.read_bytes()).hexdigest(), self.current['baseline']['sha256'])
        self.assertEqual('1.2.0', self.current['baseline']['release'])
        self.assertTrue(self.current['limits'])
        files = list((ROOT/'plugins/vibe-coding/skills').rglob('*.md')) + list((ROOT/'plugins/vibe-coding/references').glob('*.md'))
        self.assertEqual({p.relative_to(ROOT).as_posix() for p in files}, set(self.current['instructions']))
        for section in ('instructions', 'inputs_and_artifacts'):
            for name, expected in self.current[section].items():
                change = self.website['release_artifact_changes'].get(name) if section == 'inputs_and_artifacts' else None
                if change:
                    self.assertEqual(expected, change['before'])
                    expected = change['after']
                expected = self.revised_fingerprint(name, expected)
                self.assertEqual(expected, hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
        self.assertTrue(all(case['observed'] and case['limits'] for case in self.current['checks']))

    def test_website_changes_have_separate_evidence_without_rewriting_release_results(self):
        self.assertEqual(hashlib.sha256(CURRENT.read_bytes()).hexdigest(), self.website['baseline_sha256'])
        for name, change in self.website['release_artifact_changes'].items():
            self.assertTrue(name.startswith('site/') or name == 'scripts/build_site.py')
            self.assertEqual(self.current['inputs_and_artifacts'][name], change['before'])
            self.assertEqual(self.website['artifacts'][name], change['after'])
        for name, expected in self.website['artifacts'].items():
            expected = self.revised_fingerprint(name, expected)
            self.assertEqual(expected, hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
        self.assertTrue(self.website['checks'])
        self.assertTrue(all(case['observed'] and case['limits'] for case in self.website['checks']))

    def test_all_routing_cases_match_observed_owner_operation_and_authority(self):
        cases = json.loads((ROOT/self.record['routing']['cases']).read_text(encoding='utf-8'))['cases']
        actual = json.loads((ROOT/self.record['routing']['observed']).read_text(encoding='utf-8'))
        by_id = {row['id']: row for row in actual}
        self.assertEqual(len(cases), len(actual))
        self.assertEqual(len(actual), len(by_id))
        self.assertEqual({c['id'] for c in cases}, set(by_id))
        for case in cases:
            with self.subTest(case=case['id']):
                result = by_id[case['id']]
                self.assertEqual(case['expected_skill'], result['skill'])
                self.assertEqual(case['expected_mode'], result['mode'])
                self.assertEqual(case['expected_mode']=='implement', result['edits_authorized'])
                self.assertTrue(result['reason'])

    def test_required_behavior_records_are_complete_and_bounded(self):
        manifest = json.loads((ROOT/'plugins/vibe-coding/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['version'], self.listing['release'])
        cases = {row['id']: row for row in self.record['behaviors']}
        self.assertEqual({'serverless-required-write', 'mcp-http-readonly-control', 'react-hydration-preference'}, set(cases))
        for case in cases.values():
            self.assertEqual('passed', case['result'])
            self.assertTrue(case['commands'])
            self.assertTrue(case['observed'])
            self.assertTrue(case['limits'])
        self.assertFalse(cases['mcp-http-readonly-control']['product_edits'])
        self.assertEqual(34, cases['mcp-http-readonly-control']['http_cases'])
        self.assertEqual(2, cases['serverless-required-write']['before']['regression_tests_failed'])
        self.assertEqual(0, cases['serverless-required-write']['after']['tests_failed'])
        self.assertEqual({'dark':0, 'light':0}, cases['react-hydration-preference']['after_errors'])

    def test_latest_revision_preserves_history_and_covers_current_instructions(self):
        self.assertEqual(hashlib.sha256(CURRENT.read_bytes()).hexdigest(), self.revision['baseline']['sha256'])
        self.assertEqual(hashlib.sha256(WEBSITE.read_bytes()).hexdigest(), self.revision['website_baseline']['sha256'])
        files = list((ROOT/'plugins/vibe-coding/skills').rglob('*.md')) + list((ROOT/'plugins/vibe-coding/references').glob('*.md'))
        self.assertEqual({p.relative_to(ROOT).as_posix() for p in files}, set(self.revision['instructions']))
        self.assertEqual(set(self.revision['instructions']), set(self.revision['instruction_review']['paths']))
        for section in ('instructions', 'inputs_and_artifacts'):
            for name, expected in self.revision[section].items():
                expected = self.listing_fingerprint(name, expected)
                self.assertEqual(expected, hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
        self.assertTrue(self.revision['limits'])
        self.assertTrue(all(case['observed'] and case['limits'] for case in self.revision['checks']))

    def test_listing_update_preserves_instruction_review_and_records_changed_artifacts(self):
        self.assertEqual('1.4.0', self.listing['baseline']['release'])
        self.assertEqual(hashlib.sha256(REVISION.read_bytes()).hexdigest(), self.listing['baseline']['sha256'])
        self.assertFalse(set(self.listing['changes']) & set(self.revision['instructions']))
        for name, change in self.listing['changes'].items():
            path = (ROOT/name).resolve()
            self.assertTrue(path.is_relative_to(ROOT))
            self.assertEqual(self.library_fingerprint(name, change['after']), hashlib.sha256(path.read_bytes()).hexdigest(), name)
            self.assertTrue(change['review'])
        self.assertTrue(self.listing['limits'])
        self.assertTrue(all(case['observed'] and case['limits'] for case in self.listing['checks']))

    def test_mcp_edition_keeps_history_and_records_the_actual_new_runtime(self):
        self.assertEqual(hashlib.sha256(LISTING.read_bytes()).hexdigest(), self.library['baseline']['sha256'])
        self.assertEqual('1.4.1', self.library['baseline']['release'])
        self.assertEqual('1.5.0', self.library['release'])
        self.assertFalse(set(self.library['changes']) & set(self.revision['instructions']))
        for name, change in self.library['changes'].items():
            self.assertEqual(self.portability_fingerprint(name, change['after']), hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
            self.assertTrue(change['before'])
            self.assertTrue(change['review'])
        for name, expected in self.library['new_files'].items():
            self.assertEqual(self.portability_fingerprint(name, expected), hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
        self.assertIn('mcp/server.js', self.library['new_files'])
        self.assertIn('plugins/vibe-coding-library/skills/vibe-library/SKILL.md', self.library['new_files'])
        self.assertTrue(self.library['checks'])
        self.assertTrue(all(case['observed'] and case['limits'] for case in self.library['checks']))

    def test_portability_revision_preserves_the_mcp_release_record(self):
        self.assertEqual(hashlib.sha256(LIBRARY.read_bytes()).hexdigest(), self.portability['baseline']['sha256'])
        self.assertEqual('1.5.0', self.portability['baseline']['release'])
        self.assertFalse(set(self.portability['changes']) & set(self.revision['instructions']))
        for name, change in self.portability['changes'].items():
            self.assertEqual(self.site_refresh_fingerprint(name, change['after']), hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
            self.assertTrue(change['review'])

    def test_website_refresh_preserves_instruction_release_and_records_its_sources(self):
        self.assertEqual(hashlib.sha256(PORTABILITY.read_bytes()).hexdigest(), self.site_refresh['baseline']['sha256'])
        self.assertFalse(set(self.site_refresh['changes']) & set(self.revision['instructions']))
        for name, change in self.site_refresh['changes'].items():
            self.assertEqual(change['after'], hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
        for name, expected in self.site_refresh['new_files'].items():
            self.assertEqual(expected, hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)
        self.assertTrue(self.site_refresh['checks'])


if __name__ == '__main__':
    unittest.main()

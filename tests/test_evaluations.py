import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT/'review/evaluations/1.2.0.json'


class EvaluationRecordTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECORD.read_text(encoding='utf-8'))

    def test_record_matches_current_instructions_inputs_and_artifacts(self):
        for section in ['instructions', 'inputs_and_artifacts']:
            self.assertTrue(self.record[section])
            for name, expected in self.record[section].items():
                with self.subTest(path=name):
                    path = (ROOT/name).resolve()
                    self.assertTrue(path.is_relative_to(ROOT))
                    self.assertEqual(expected, hashlib.sha256(path.read_bytes()).hexdigest(), 'Evaluation is stale: re-evaluate affected behavior')

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


if __name__ == '__main__':
    unittest.main()

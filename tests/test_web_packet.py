import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'plugins/vibe-coding/skills/vibe-landing/scripts/check_web_packet.py'
SPEC = importlib.util.spec_from_file_location('web_packet', SOURCE)
packet = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packet)


class WebPacketTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root/'design.md').write_text('A concrete design specification', encoding='utf-8')
        (self.root/'check.json').write_text('{"case":"rendered icon family","result":"passed"}', encoding='utf-8')
        self.requirements = {'version':1,'items':[
            {'id':'favicon','requirement':'Provide an actual favicon family','required':True},
            {'id':'optional-map','requirement':'Include a map if useful','required':False}]}
        self.value = {'version':1,'stage':'proposal','requirements_sha256':packet.digest(self.requirements),'items':[
            {'id':'favicon','status':'specified','owner':'web-brand-assets','decision':'The required identity and icon exports are specified in design.md','artifacts':['design.md'],'evidence':[]},
            {'id':'optional-map','status':'not_applicable','owner':'web-page-architecture','decision':'No location or visit task belongs to this online-only offer','artifacts':[],'evidence':[]}]}

    def test_proposal_coverage_does_not_claim_implementation(self):
        self.assertEqual('passed',packet.check(self.requirements,self.value,self.root)['structural_status'])
        self.value['stage'] = 'implementation'
        self.assertEqual('failed',packet.check(self.requirements,self.value,self.root)['structural_status'])
        self.value['items'][0].update(status='verified',evidence=['check.json'])
        self.assertEqual('passed',packet.check(self.requirements,self.value,self.root)['structural_status'])

    def test_missing_requirement_or_required_na_cannot_be_hidden(self):
        removed = copy.deepcopy(self.value); removed['items'] = removed['items'][1:]
        self.assertTrue(any('Missing requirement: favicon' in error for error in packet.check(self.requirements,removed,self.root)['errors']))
        self.value['items'][0]['status'] = 'not_applicable'
        self.assertEqual('failed',packet.check(self.requirements,self.value,self.root)['structural_status'])

    def test_changed_source_duplicate_and_invented_ids_fail(self):
        self.requirements['items'][0]['requirement'] = 'Provide different required assets'
        self.assertTrue(any('digest' in error for error in packet.check(self.requirements,self.value,self.root)['errors']))
        duplicate = copy.deepcopy(self.value); duplicate['items'].append(duplicate['items'][0])
        with self.assertRaises(ValueError): packet.check(self.requirements,duplicate,self.root)
        invented = copy.deepcopy(self.value); invented['items'].append({'id':'invented'})
        self.assertEqual('failed',packet.check(self.requirements,invented,self.root)['structural_status'])

    def test_missing_or_escaping_artifacts_and_absent_evidence_fail(self):
        for paths in [['not-created.svg'],['../private.txt'],['https://example.com/evidence']]:
            value = copy.deepcopy(self.value); value['items'][0]['artifacts'] = paths
            self.assertEqual('failed',packet.check(self.requirements,value,self.root)['structural_status'])
        self.value['items'][0]['status'] = 'verified'
        self.assertEqual('failed',packet.check(self.requirements,self.value,self.root)['structural_status'])

    def test_required_blocked_case_stays_open(self):
        self.value['items'][0].update(status='blocked',decision='Required logo source is unavailable')
        report = packet.check(self.requirements,self.value,self.root)
        self.assertEqual('failed',report['structural_status'])
        self.assertEqual('favicon',report['open_gates'][0]['id'])


if __name__ == '__main__':
    unittest.main()

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN/'scripts'))
from workflow_graph import load_workflows


class WorkflowCompositionTests(unittest.TestCase):
    def setUp(self):
        self.rows = json.loads((PLUGIN/'catalog.json').read_text())['recipes']
        self.spec = load_workflows(PLUGIN, self.rows)

    def reject(self, mutate):
        spec = copy.deepcopy(self.spec)
        mutate(spec)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'workflows.json').write_text(json.dumps(spec), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_workflows(root, self.rows)

    def test_missing_or_multiply_owned_prompts_cannot_ship(self):
        self.reject(lambda spec: spec['focused'].pop())
        self.reject(lambda spec: spec['focused'].append(spec['families'][0]['audit']))

    def test_repair_must_be_an_implementation_in_the_same_domain(self):
        self.reject(lambda spec: spec['families'][0].update(implement='api-polish'))
        self.reject(lambda spec: spec['families'][0].update(implement='patch-checking'))

    def test_checks_and_transitions_must_reference_real_prompt_roles(self):
        self.reject(lambda spec: spec['families'][0]['checks'][0].update(id='patch-checking'))
        self.reject(lambda spec: spec['sequences']['task-shaping'][0].update(id='invented-next-step'))

    def test_every_role_has_an_explicit_handoff(self):
        self.reject(lambda spec: spec['handoffs'].pop('check'))


if __name__ == '__main__':
    unittest.main()

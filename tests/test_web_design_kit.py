import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT/'plugins/vibe-coding/skills/vibe-web-art-direction'
HELPER = OWNER/'scripts/compile_design_kit.py'
SPEC = importlib.util.spec_from_file_location('web_design_kit', HELPER)
kit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kit)


class WebDesignKitTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((OWNER/'assets/design-kit.example.json').read_text(encoding='utf-8'))

    def test_reproducible_materials_and_explicit_validation_limits(self):
        first, report = kit.compile_kit(self.spec)
        self.assertEqual(first, kit.compile_kit(self.spec)[0])
        self.assertTrue(report['solid_text_contrast_passed'])
        self.assertTrue(report['render_required'])
        for kind in ('flow', 'contours', 'dots'):
            self.spec['materials']['procedural']['kind'] = kind
            files, _ = kit.compile_kit(self.spec)
            tree = ET.fromstring(files['procedural.svg'])
            self.assertEqual('{http://www.w3.org/2000/svg}svg', tree.tag)
            self.assertLess(len(files['procedural.svg'].encode()), 500000)
        changed = copy.deepcopy(self.spec)
        changed['materials']['procedural']['seed'] += 1
        self.assertNotEqual(kit.compile_kit(changed)[0]['procedural.svg'], kit.compile_kit(self.spec)[0]['procedural.svg'])

    def test_bad_contrast_produces_a_failure_not_a_certification(self):
        self.spec['colors']['text'] = self.spec['colors']['background']
        _, report = kit.compile_kit(self.spec)
        self.assertFalse(report['solid_text_contrast_passed'])
        self.assertTrue(any(not row['passed'] for row in report['solid_text_contrast']))

    def test_weight_numbers_alone_do_not_claim_visual_hierarchy(self):
        self.spec['type']['roles']['display']['weight'] = 740
        self.spec['type']['roles']['label']['weight'] = 800
        files, report = kit.compile_kit(self.spec)
        self.assertIn('font-weight: 740', files['design-tokens.css'])
        self.assertIn('font-weight: 800', files['design-tokens.css'])
        self.assertIn('Responsive page, interaction and visual acceptance', report['render_required'])

    def test_soft_accents_export_alpha_details_without_fading_readable_text(self):
        files, report = kit.compile_kit(self.spec)
        self.assertIn('--color-accent-soft: rgba(36, 92, 76, 0.1)',files['design-tokens.css'])
        self.assertIn('--border-subtle: 1px solid rgba(27, 41, 38, 0.16)',files['design-tokens.css'])
        self.assertIn('--shadow-raised: 0px 12px 32px -8px rgba(27, 41, 38, 0.12)',files['design-tokens.css'])
        self.assertIn('--color-text: #1B2926',files['design-tokens.css'])
        self.assertIn('Rendered text/control contrast over materials in all relevant states',report['render_required'])
        self.spec['effects']['tints']['text'] = {'color':'text','alpha':.1}
        with self.assertRaises(ValueError): kit.compile_kit(self.spec)

    def test_invalid_parameters_and_unsafe_css_cannot_enter_outputs(self):
        mutations = [
            lambda s:s['colors'].update(accent='red; color: black'),
            lambda s:s['type']['families'].update(body=['x</style><script>']),
            lambda s:s['type']['roles']['body'].update(min_rem=float('nan')),
            lambda s:s['type']['roles']['display'].update(max_rem=.5),
            lambda s:s['layout'].update(columns=2.5),
            lambda s:s['motion'].update(easing='cubic-bezier(9, 0, 1, 1)'),
            lambda s:s['materials']['procedural'].update(density=1000000),
            lambda s:s['materials']['glass'].update(fallback='invented-color'),
        ]
        for mutate in mutations:
            value = copy.deepcopy(self.spec)
            mutate(value)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                kit.compile_kit(value)

    def test_board_uses_the_selected_body_stack_and_escapes_untrusted_labels(self):
        self.spec['type']['families']['reading'] = self.spec['type']['families'].pop('body')
        for role in self.spec['type']['roles'].values():
            if role['family'] == 'body': role['family'] = 'reading'
        self.spec['name'] = '<script>alert(1)</script>'
        files, _ = kit.compile_kit(self.spec)
        self.assertNotIn('<script>', files['design-board.html'])
        self.assertIn('font-family:var(--font-reading)', files['design-board.html'])

    def test_cli_refuses_overwrite_and_removes_only_superseded_owned_materials(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root/'input.json'; output = root/'kit'
            source.write_text(json.dumps(self.spec), encoding='utf-8')
            command = [sys.executable, str(HELPER), '--input', str(source), '--output-dir', str(output)]
            def run(extra=()):
                return subprocess.run(command+list(extra), capture_output=True, text=True, timeout=10)
            self.assertEqual(0, run().returncode)
            self.assertEqual(2, run().returncode)
            note = output/'project-notes.txt'; note.write_text('keep', encoding='utf-8')
            self.spec['materials'].pop('procedural')
            source.write_text(json.dumps(self.spec), encoding='utf-8')
            self.assertEqual(0, run(['--force']).returncode)
            self.assertFalse((output/'procedural.svg').exists())
            self.assertEqual('keep', note.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()

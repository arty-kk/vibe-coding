import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN/'scripts'))
from topic_index import build_topics
from workflow_graph import load_workflows
import catalog


class TopicCatalogTests(unittest.TestCase):
    def setUp(self):
        self.rows = catalog.load_catalog()['recipes']
        self.flows = load_workflows(PLUGIN, self.rows)
        self.source = json.loads((PLUGIN/'assets/catalog/search-topics.json').read_text(encoding='utf-8'))

    def reject(self, mutate):
        value = copy.deepcopy(self.source)
        mutate(value)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'assets/catalog').mkdir(parents=True)
            (root/'assets/catalog/search-topics.json').write_text(json.dumps(value),encoding='utf-8')
            with self.assertRaises(ValueError):
                build_topics(root,self.rows,self.flows)

    def test_closed_keys_cover_all_workflows_and_reject_orphans(self):
        data = build_topics(PLUGIN,self.rows,self.flows)
        self.assertEqual(45,len(data['domains']))
        self.assertEqual(162,len(data['topics']))
        self.assertEqual({row['id'] for row in self.rows},{identity for topic in data['topics'] for identity in topic['recipe_ids']})
        self.reject(lambda value:value['topics'].pop('auth-permissions'))
        self.reject(lambda value:value['topics'].update(invented_topic={'primary':['invented'],'keywords':['invented']}))

    def test_canonical_keywords_and_extra_aliases_have_valid_owners(self):
        self.reject(lambda value:value['topics']['auth-permissions'].update(primary=['']))
        self.reject(lambda value:value['topics']['auth-permissions'].update(primary=['not-listed']))
        self.reject(lambda value:value['recipe_keywords'].update(unknown_recipe=['auth']))

    def test_offline_cli_engine_selects_the_same_exact_topic_and_mode(self):
        rows = catalog.search(self.rows,mode='implement',skill='vibe-domain',topic='auth-permissions')
        self.assertEqual(['auth-permissions-polish'],[row['id'] for row in rows])
        self.assertEqual([],catalog.search(self.rows,mode='review',topic='auth-permissions'))


if __name__ == '__main__':
    unittest.main()

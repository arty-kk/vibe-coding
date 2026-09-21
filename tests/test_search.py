import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN/'scripts'))
import catalog
from search_index import build_index, match_score
from catalog_site import load_locales


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.rows = catalog.load_catalog()['recipes']

    def test_technical_terms_in_bodies_are_discoverable(self):
        for term in ['GraphQL', 'OpenAPI', 'outbox', 'backfill', 'SBOM', 'CORS', 'CSRF']:
            with self.subTest(term=term):
                self.assertTrue(catalog.search(self.rows, term))
        body = next(row for row in self.rows if row['id'] == 'transactional-delivery-check')
        self.assertIn(body, catalog.search(self.rows, 'outbox', mode='check'))

    def test_primary_match_ranks_above_body_match(self):
        self.assertGreater(match_score({'primary': 'graphql', 'body': ''}, 'GraphQL'),
                           match_score({'primary': '', 'body': 'graphql'}, 'GraphQL'))
        self.assertIsNone(match_score({'primary': 'graphql', 'body': ''}, 'graphql absent'))
        self.assertEqual(3, match_score({'primary': 'hidratacion', 'body': ''}, 'HIDRATACIÓN'))

    def test_multilingual_keywords_and_filters(self):
        for query in ['серверлесс', 'sin servidor', '无服务器']:
            with self.subTest(query=query):
                found = catalog.search(self.rows, query, skill='vibe-serverless', mode='check')
                self.assertEqual(['serverless-invocation-check'], [r['id'] for r in found])

    def test_cli_offline_and_site_use_identical_index(self):
        expected = build_index(self.rows, load_locales(), PLUGIN)
        offline = (PLUGIN/'CATALOG.html').read_text(encoding='utf-8')
        embedded = re.search(r'id="search-data">(.*?)</script>', offline, re.S)
        self.assertIsNotNone(embedded)
        self.assertEqual(expected, json.loads(embedded[1]))
        public = (ROOT/'docs/index.html').read_text(encoding='utf-8')
        config = json.loads(re.search(r'id="catalog-data">(.*?)</script>', public, re.S)[1])
        self.assertTrue(config['index'].startswith('/vibe-coding/assets/search.'))
        asset = ROOT/'docs'/config['index'].removeprefix('/vibe-coding/')
        self.assertEqual(expected, json.loads(asset.read_text(encoding='utf-8')))


if __name__ == '__main__':
    unittest.main()

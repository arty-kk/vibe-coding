import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import build_site as site


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags=[]; self.ids=set(); self.json=[]; self.active_json=False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if 'id' in attrs: self.ids.add(attrs['id'])
        self.active_json=tag=='script' and attrs.get('type')=='application/ld+json'

    def handle_endtag(self, tag):
        if tag=='script': self.active_json=False

    def handle_data(self, data):
        if self.active_json: self.json.append(json.loads(data))

    def matching(self, tag, **attrs):
        return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in attrs.items())]


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.destination=Path(cls.temp.name)
        cls.locales=site.load_locales()
        cls.content=json.loads((ROOT/'site/content.json').read_text(encoding='utf-8'))
        cls.rows=json.loads((site.PLUGIN/'catalog.json').read_text(encoding='utf-8'))['recipes']
        site.build(cls.destination)
        cls.pages={p.relative_to(cls.destination).as_posix():p.read_text(encoding='utf-8') for p in cls.destination.rglob('*.html')}
        cls.documents={path:Document(source) for path,source in cls.pages.items()}

    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def test_complete_translations_and_host_specific_prompts(self):
        site.validate_locales(self.locales,self.rows)
        for locale in self.locales.values():
            for key in ('prompt','promptClaude'):
                self.assertEqual({'{skill}','{title}','{id}'},set(re.findall(r'\{\w+\}',locale['ui'][key])))
            self.assertTrue(locale['ui']['promptClaude'].startswith('/vibe-coding:{skill}'))
        broken=copy.deepcopy(self.locales)
        del broken['es']['titles'][self.rows[0]['id']]
        with self.assertRaisesRegex(ValueError,'es: missing'): site.validate_locales(broken,self.rows)
        broken=copy.deepcopy(self.locales);broken['zh-CN']['ui']['promptClaude']='Use {skill}.'
        with self.assertRaisesRegex(ValueError,'mismatched placeholders'): site.validate_locales(broken,self.rows)

    def test_all_languages_are_static_self_canonical_and_reciprocal(self):
        for lang,locale in self.locales.items():
            for suffix in ('','privacy.html','terms.html'):
                path=site.route(lang,suffix);key=path if suffix else path+'index.html'
                page=self.pages[key];doc=self.documents[key]
                self.assertEqual(lang,doc.matching('html')[0]['lang'])
                self.assertEqual([site.BASE+path],[link['href'] for link in doc.matching('link',rel='canonical')])
                alternates={a['hreflang']:a['href'] for a in doc.matching('link',rel='alternate')}
                self.assertEqual(set(self.locales)|{'x-default'},set(alternates))
                for other in self.locales:
                    self.assertEqual(site.BASE+site.route(other,suffix),alternates[other])
                self.assertEqual(site.BASE+suffix,alternates['x-default'])
                if suffix:
                    self.assertIn(site.policy_html(locale['policy'][suffix[:-5]]),page)
                else:
                    self.assertIn('Claude Code',page)
                    links=[a for a in doc.matching('a',hreflang='en') if 'data-id' in a]
                    self.assertEqual(len(self.rows),len(links))
                    self.assertEqual({site.PREFIX+site.workflow_route(row) for row in self.rows},{a['href'] for a in links})
                    self.assertNotIn('recipe-data',doc.ids)
                    self.assertLess(len(page.encode()),310_000)

    def test_workflows_have_full_instructions_and_truthful_metadata(self):
        descriptions=[]
        for row in self.rows:
            key=site.workflow_route(row)+'index.html';page=self.pages[key];doc=self.documents[key]
            self.assertEqual(1,len(doc.matching('h1')))
            self.assertIn('technical-instructions',doc.ids)
            self.assertIn('run-title',doc.ids)
            self.assertTrue(doc.matching('textarea',id='prompt'))
            self.assertIn(row['id'],page)
            self.assertNotIn('recipe-data',doc.ids)
            self.assertEqual([],doc.matching('link',rel='alternate'))
            graph=doc.json[0]['@graph']
            article=next(item for item in graph if item['@type']=='TechArticle')
            self.assertEqual('en',article['inLanguage'])
            self.assertEqual(site.display_title(row,self.locales['en'],self.content['en']),article['headline'])
            self.assertEqual(site.BASE+site.workflow_route(row),article['url'])
            descriptions.append(article['description'])
            source=(site.PLUGIN/row['path']).read_text(encoding='utf-8')
            for title in re.findall(r'^## (.+)$',source,re.M):
                self.assertIn(site.e(title),page)
        self.assertEqual(len(descriptions),len(set(descriptions)))

    def test_every_local_link_asset_and_fragment_resolves(self):
        for current,doc in self.documents.items():
            for tag,a in doc.tags:
                target=a.get('href') if tag in ('a','link') else a.get('src') if tag in ('script','img') else None
                if not target: continue
                parts=urlsplit(target)
                if parts.scheme or parts.netloc: continue
                path=unquote(parts.path)
                if path:
                    self.assertTrue(path.startswith(site.PREFIX),(current,target))
                    relative=path[len(site.PREFIX):]
                    if not relative or relative.endswith('/'): relative+='index.html'
                else: relative=current
                self.assertTrue((self.destination/relative).is_file(),(current,target))
                if parts.fragment and relative.endswith('.html'):
                    self.assertIn(unquote(parts.fragment),self.documents[relative].ids,(current,target))

    def test_sitemap_is_exactly_the_indexable_canonical_set(self):
        urls=[item.text for item in ET.parse(self.destination/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        canonical={a['href'] for key,doc in self.documents.items() if key!='404.html' for a in doc.matching('link',rel='canonical')}
        self.assertEqual(canonical,set(urls));self.assertEqual(len(urls),len(set(urls)))
        self.assertEqual(len(self.rows)+12,len(urls))
        self.assertIn('noindex',self.documents['404.html'].matching('meta',name='robots')[0]['content'])
        self.assertFalse((self.destination/'robots.txt').exists(),'A project-path robots.txt cannot control the host root')

    def test_social_and_structured_data_are_consistent(self):
        image=(self.destination/'social-card.png').read_bytes()
        self.assertEqual(b'\x89PNG\r\n\x1a\n',image[:8])
        self.assertEqual((1200,630),(int.from_bytes(image[16:20],'big'),int.from_bytes(image[20:24],'big')))
        for doc in self.documents.values():
            canonical=doc.matching('link',rel='canonical')[0]['href']
            self.assertEqual(canonical,doc.matching('meta',property='og:url')[0]['content'])
            self.assertEqual('summary_large_image',doc.matching('meta',name='twitter:card')[0]['content'])
            self.assertEqual(1,len(doc.json))
            graph=doc.json[0]['@graph']
            software=next(item for item in graph if item['@type']=='SoftwareSourceCode')
            self.assertEqual(['Codex','Claude Code'],software['runtimePlatform'])
            self.assertEqual(site.REPO,software['codeRepository'])
            self.assertNotIn('aggregateRating',software)

    def test_build_is_deterministic_and_keeps_assets_for_open_tabs(self):
        first={p.relative_to(self.destination).as_posix():p.read_bytes() for p in self.destination.rglob('*') if p.is_file()}
        (self.destination/'assets/site.000000000000.js').write_text('obsolete')
        first['assets/site.000000000000.js']=b'obsolete'
        site.build(self.destination)
        second={p.relative_to(self.destination).as_posix():p.read_bytes() for p in self.destination.rglob('*') if p.is_file()}
        self.assertEqual(first,second)

    def test_embedded_json_and_markdown_do_not_execute_markup(self):
        value={'text':'</script><script>alert(1)</script>\u2028\u2029'}
        encoded=site.script_json(value);self.assertNotIn('<',encoded);self.assertEqual(value,json.loads(encoded))
        rendered=site.MD.render('<script>alert(1)</script>\n\n[bad](javascript:alert(1))')
        self.assertNotIn('<script>',rendered);self.assertNotIn('href="javascript:',rendered)
        rendered=site.policy_html('# Privacy\n\n<script>alert(1)</script> [MIT](LICENSE)')
        self.assertNotIn('<script>',rendered);self.assertIn('href="https://github.com/arty-kk/vibe-coding/blob/main/LICENSE"',rendered)


if __name__=='__main__':unittest.main()

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
        cls.policies=site.load_site_policies()
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

    def test_library_product_version_is_separate_from_instruction_sources(self):
        product=json.loads((site.LIBRARY_PLUGIN/'plugin.json').read_text(encoding='utf-8'))['version']
        instructions=json.loads((site.PLUGIN/'plugin.json').read_text(encoding='utf-8'))['version']
        for lang in self.locales:
            page=self.pages[site.route(lang)+'index.html'];doc=self.documents[site.route(lang)+'index.html']
            self.assertIn('v'+product,page)
            software=next(item for item in doc.json[0]['@graph'] if item['@type']=='SoftwareSourceCode')
            self.assertEqual(product,software['version'])
            self.assertEqual('Vibe Coding Library',software['name'])
            self.assertIn(site.MCP_ENDPOINT,page)
            self.assertIn('search_workflows',page);self.assertIn('get_workflow',page)
            self.assertIn('claude plugin install vibe-coding-library@vibe-coding',page)
            self.assertNotIn('chatgpt.com/plugins/',page)
        article=self.documents[site.workflow_route(self.rows[0])+'index.html']
        metadata=next(item for item in article.json[0]['@graph'] if item['@type']=='TechArticle')
        self.assertEqual(instructions,metadata['version'])
        for lang,values in self.content.items():
            for key in ('workflowPrompt','workflowPromptClaude','workflowPromptGeneric'):
                self.assertEqual({'title','id'},set(re.findall(r'\{(\w+)\}',values[key])),(lang,key))
            self.assertNotIn('$vibe',values['workflowPromptGeneric'])
            self.assertNotIn('/vibe-coding',values['workflowPromptGeneric'])
            self.assertIn('value="generic"',self.pages[site.route(lang)+'index.html'])

    def test_all_languages_are_static_self_canonical_and_reciprocal(self):
        for lang,locale in self.locales.items():
            for suffix in ('','workflows/','privacy.html','terms.html'):
                path=site.route(lang,suffix);key=path if suffix.endswith('.html') else path+'index.html'
                page=self.pages[key];doc=self.documents[key]
                self.assertEqual(lang,doc.matching('html')[0]['lang'])
                self.assertEqual([site.BASE+path],[link['href'] for link in doc.matching('link',rel='canonical')])
                alternates={a['hreflang']:a['href'] for a in doc.matching('link',rel='alternate')}
                self.assertEqual(set(self.locales)|{'x-default'},set(alternates))
                for other in self.locales:
                    self.assertEqual(site.BASE+site.route(other,suffix),alternates[other])
                self.assertEqual(site.BASE+suffix,alternates['x-default'])
                if suffix.endswith('.html'):
                    self.assertIn(site.MD.render(self.policies[lang][suffix[:-5]]),page)
                elif not suffix:
                    self.assertIn('Claude Code',page)
                    links=[a for a in doc.matching('a',hreflang='en') if 'data-id' in a]
                    self.assertEqual(len(self.rows),len(links))
                    self.assertEqual({site.PREFIX+site.workflow_route(row) for row in self.rows},{a['href'] for a in links})
                    self.assertNotIn('recipe-data',doc.ids)
                    # Complete static cards plus multilingual titles, purposes and search lexicon.
                    self.assertLess(len(page.encode()),400_000)

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
            self.assertEqual(row['category'],article['articleSection'])
            self.assertTrue(article['isAccessibleForFree'])
            self.assertIn('/blob/v'+article['version']+'/',article['isBasedOn'])
            self.assertIn(article['isBasedOn'],[a['href'] for a in doc.matching('a')])
            breadcrumbs=next(item for item in graph if item['@type']=='BreadcrumbList')['itemListElement']
            self.assertEqual([site.BASE,site.BASE+'workflows/',article['url']],[item['item'] for item in breadcrumbs])
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
        self.assertEqual(len(self.rows)+16,len(urls))
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
            self.assertEqual(['MCP clients with Streamable HTTP support'],software['runtimePlatform'])
            self.assertEqual(site.REPO,software['codeRepository'])
            self.assertNotIn('aggregateRating',software)

    def test_directory_exposes_every_workflow_without_search_or_pagination(self):
        for lang in self.locales:
            key=site.route(lang,'workflows/')+'index.html'; doc=self.documents[key]
            links=doc.matching('a',hreflang='en')
            workflow_links=[a for a in links if a['href'].startswith(site.PREFIX+'workflows/') and a['href']!=site.PREFIX+'workflows/']
            self.assertEqual(len(self.rows),len(workflow_links))
            self.assertEqual({site.PREFIX+site.workflow_route(row) for row in self.rows},{a['href'] for a in workflow_links})
            self.assertNotIn('catalog-data',doc.ids)
            self.assertNotIn('pagination',doc.ids)
            self.assertTrue({row['skill'] for row in self.rows}.issubset(doc.ids))
            self.assertTrue(any(item['@type']=='CollectionPage' for item in doc.json[0]['@graph']))
            for suffix in ('','privacy.html','terms.html'):
                parent=site.route(lang,suffix) if suffix else site.route(lang)+'index.html'
                self.assertIn(site.PREFIX+site.route(lang,'workflows/'),[a['href'] for a in self.documents[parent].matching('a')])

    def test_indexable_pages_have_distinct_metadata_and_no_generated_query_links(self):
        titles, descriptions = [], []
        for name, doc in self.documents.items():
            if name=='404.html': continue
            self.assertEqual(1,len(doc.matching('h1')),name)
            self.assertEqual(1,len(doc.matching('title')),name)
            title=re.search(r'<title>(.*?)</title>',self.pages[name])[1]
            titles.append(title)
            descriptions.append(doc.matching('meta',name='description')[0]['content'])
            self.assertNotRegex(descriptions[-1],r'\[[^]]+\]\([^)]+\)',name)
            self.assertNotIn('noindex',doc.matching('meta',name='robots')[0]['content'])
            for link in doc.matching('a'):
                target=urlsplit(link['href'])
                if not target.scheme and target.path.startswith(site.PREFIX):
                    self.assertFalse(target.query,(name,link['href']))
        self.assertEqual(len(titles),len(set(titles)))
        self.assertEqual(len(descriptions),len(set(descriptions)))

    def test_policies_do_not_claim_software_is_their_main_content(self):
        for lang in self.locales:
            for policy in ('privacy.html','terms.html'):
                doc=self.documents[site.route(lang,policy)]
                entity=next(item for item in doc.json[0]['@graph'] if item['@type']=='WebPage')
                self.assertNotIn('mainEntity',entity)

    def test_site_policies_cover_the_website_and_mcp_independently_of_offline_notices(self):
        for lang, locale in self.locales.items():
            for name in ('privacy', 'terms'):
                page=self.pages[site.route(lang,name+'.html')]
                self.assertNotIn(site.policy_html(locale['policy'][name]),page)
                self.assertIn('mailto:artemsatsuk@proton.me',page)
                self.assertIn(site.MCP_SITE+name,page)
            privacy=self.pages[site.route(lang,'privacy.html')]
            for text in ('GitHub Pages','OpenAI Sites','Cloudflare','vibe-coding-host','vibe-coding-language'):
                self.assertIn(text,privacy)
            for url in ('https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement',
                        'https://openai.com/policies/privacy-policy/', 'https://www.cloudflare.com/privacypolicy/'):
                self.assertIn(url,privacy)
            self.assertIn(site.REPO+'/blob/main/PRIVACY.md',privacy)
            self.assertIn(site.REPO+'/blob/main/TERMS.md',self.pages[site.route(lang,'terms.html')])

    def test_site_policy_translations_require_both_notices_and_one_title(self):
        target=self.destination/'policy-validation.json'
        for change, message in ((lambda data:data.pop('zh-CN'), 'site policy locale'),
                                (lambda data:data['es'].pop('terms'), 'Incomplete site policies'),
                                (lambda data:data['ru'].update(privacy=''), 'Empty site policy'),
                                (lambda data:data['en'].update(terms='# Terms\n\n# Another title'), 'one site policy title')):
            broken=copy.deepcopy(self.policies);change(broken)
            target.write_text(json.dumps(broken),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,message):site.load_site_policies(target)
        target.unlink()

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

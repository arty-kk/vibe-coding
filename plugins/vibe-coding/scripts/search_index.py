"""Shared discovery data and equivalent token ranking for offline/CLI/MCP search."""
from functools import lru_cache
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile('[\u3400-\u9fff]')


def fold(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(text))
                   if not unicodedata.category(c).startswith('M')).lower()


def words(text):
    return re.findall(r'[^\W_]+(?:[+#]+)?|[+#]+', fold(text), re.UNICODE)


def compact(text):
    return ''.join(words(text))


def load_lexicon(root=ROOT):
    return json.loads((root/'assets/catalog/search-lexicon.json').read_text(encoding='utf-8'))


def replacement(groups):
    table = {fold(value): target for target, variants in groups.items() for value in [target, *variants]}
    if not table:
        return lambda text: text
    variants = sorted(table, key=lambda value: (-len(value), value))
    pattern = re.compile('|'.join(re.escape(value) if CJK.search(value) else
                         r'(?<![^\W_])'+re.escape(value)+r'(?![^\W_])' for value in variants))
    return lambda text: pattern.sub(lambda match: ' '+table[match[0]]+' ', text)


class Rules:
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.concepts = replacement(lexicon.get('terms', {}))
        self.intents = replacement({'intent_'+key: values for key, values in lexicon.get('intents', {}).items()})
        self.stops = set(map(fold, lexicon.get('stopwords', [])))

    @lru_cache(maxsize=4096)
    def tokens(self, text):
        return tuple(words(self.concepts(fold(text))))

    def query(self, text):
        text = self.intents(self.concepts(fold(text)))
        hints = re.findall(r'intent_([a-z]+)', text)
        text = re.sub(r'intent_[a-z]+', ' ', text)
        for stop in sorted((s for s in self.stops if CJK.search(s)), key=lambda value: (-len(value), value)):
            text = text.replace(stop, ' ')
        return list(dict.fromkeys(w for w in words(text) if w not in self.stops)), set(hints)


@lru_cache(maxsize=4)
def rules_for(root=ROOT):
    return Rules(load_lexicon(root))


def build_index(rows, locales, root):
    index = {}
    for row in rows:
        titles = [locale['titles'][row['id']] for locale in locales.values()]
        topic = [locale['categories'][row['skill']] for locale in locales.values()]
        actions = [locale['modes'][row['mode']] for locale in locales.values()]
        primary = [row['id'], row['skill'], row.get('purpose', ''), *row.get('keywords', []), *titles, *topic, *actions]
        path = (root/row['path']).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError(f'Escaping recipe path: {row["id"]}')
        body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', path.read_text(encoding='utf-8'))
        index[row['id']] = {'primary': fold(' '.join(primary)), 'body': fold(body),
                           'id': row['id'], 'skill': row['skill'], 'mode': row['mode'],
                           'titles': titles, 'purpose': row.get('purpose', ''),
                           'keywords': row.get('keywords', []), 'topics': topic, 'actions': actions}
    return index


def contains(tokens, term):
    return any(term in token for token in tokens) if CJK.search(term) else any(
        token == term or (len(term) >= 3 and token.startswith(term)) for token in tokens)


def match_score(entry, query, full_text=True, rules=None):
    rules = rules or rules_for()
    terms, hints = rules.query(query)
    identity = entry.get('id', '')
    key = compact(query)
    if key and identity:
        if key == compact(identity): return 20000
        if key in [compact(title) for title in entry['titles']]: return 15000
        if key in [compact(alias) for alias in rules.lexicon.get('aliases', {}).get(identity, [])]: return 15000
    title = rules.tokens(' '.join(entry.get('titles', [])))
    keywords = rules.tokens(' '.join([identity, entry.get('skill', ''), entry.get('purpose', ''),
                            *entry.get('keywords', []), *rules.lexicon.get('discovery', {}).get(identity, [])]))
    topic = rules.tokens(' '.join(entry.get('topics', [])))
    # Old callers may provide only primary/body rather than the structured index.
    if not identity: title = rules.tokens(entry['primary'])
    body = None
    total, body_only = 0, False
    for term in terms:
        if contains(title, term): total += 40
        elif contains(keywords, term): total += 20
        elif contains(topic, term): total += 8
        else:
            if not full_text: return None
            if body is None: body = rules.tokens(entry['body'])
            if not contains(body, term): return None
            total += 1
            body_only = True
    if entry.get('mode') in hints: total += 35
    return total - (1000 if body_only else 0)

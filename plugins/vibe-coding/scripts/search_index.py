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


def one_edit(a, b):
    if abs(len(a)-len(b)) > 1:
        return False
    if a == b:
        return True
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    if len(a) == len(b):
        return a[i+1:] == b[i+1:] or (i+1 < len(a) and a[i] == b[i+1] and a[i+1] == b[i] and a[i+2:] == b[i+2:])
    return a[i+1:] == b[i:] if len(a) > len(b) else a[i:] == b[i+1:]


class Rules:
    def __init__(self, lexicon, candidate_texts=()):
        self.lexicon = lexicon
        self.concepts = replacement(lexicon.get('terms', {}))
        self.intents = replacement({'intent_'+key: values for key, values in lexicon.get('intents', {}).items()})
        self.stops = set(map(fold, lexicon.get('stopwords', [])))
        forms = [*lexicon.get('terms', {})]
        forms += [value for values in lexicon.get('terms', {}).values() for value in values]
        forms += [value for values in lexicon.get('intents', {}).values() for value in values]
        self.exact = {word for value in [*forms, *candidate_texts] for word in words(value)} | self.stops
        self.deletions = {}
        for word in self.exact:
            if word in self.stops or not 5 <= len(word) <= 48 or not word.isalpha() or CJK.search(word):
                continue
            for i in range(len(word)):
                self.deletions.setdefault(word[:i]+word[i+1:], set()).add(word)

    @lru_cache(maxsize=4096)
    def tokens(self, text):
        return tuple(words(self.concepts(fold(text))))

    def correct(self, word):
        if word in self.exact or not 5 <= len(word) <= 48 or not word.isalpha() or CJK.search(word):
            return word
        candidates = set(self.deletions.get(word, ()))
        for i in range(len(word)):
            key = word[:i]+word[i+1:]
            if key in self.exact and key not in self.stops:
                candidates.add(key)
            candidates.update(self.deletions.get(key, ()))
        matches = sorted(item for item in candidates if len(item) >= 5 and item[0] == word[0] and one_edit(word, item))
        signatures = {self.intents(self.concepts(item)).strip() for item in matches}
        return matches[0] if len(signatures) == 1 else word

    def query(self, text):
        text = re.sub(r'[^\W_]+(?:[+#]+)?|[+#]+', lambda match: self.correct(match[0]), fold(text))
        text = self.intents(self.concepts(text))
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
    candidates = []
    for row in rows:
        candidates.extend([row['id'], row['skill'], *row.get('keywords', [])])
        candidates.extend(locale['titles'][row['id']] for locale in locales.values())
    rules = Rules(load_lexicon(root), candidates)
    for row in rows:
        titles = [locale['titles'][row['id']] for locale in locales.values()]
        topic = [locale['categories'][row['skill']] for locale in locales.values()]
        actions = [locale['modes'][row['mode']] for locale in locales.values()]
        primary = [row['id'], row['skill'], row.get('purpose', ''), *row.get('keywords', []), *titles, *topic, *actions]
        path = (root/row['path']).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError(f'Escaping recipe path: {row["id"]}')
        body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', path.read_text(encoding='utf-8'))
        entry = SearchEntry({'primary': fold(' '.join(primary)), 'body': fold(body),
                           'id': row['id'], 'skill': row['skill'], 'mode': row['mode'],
                           'titles': titles, 'purpose': row.get('purpose', ''),
                           'primary_keywords': row.get('primary_keywords', []),
                           'keywords': row.get('keywords', []), 'topics': topic, 'actions': actions})
        entry.search_rules = rules
        index[row['id']] = entry
    return index


class SearchEntry(dict):
    pass


def contains(tokens, term):
    return any(term in token for token in tokens) if CJK.search(term) else any(
        token == term or (len(term) >= 3 and token.startswith(term)) for token in tokens)


def match_score(entry, query, full_text=True, rules=None):
    rules = rules or getattr(entry, 'search_rules', None) or rules_for()
    terms, hints = rules.query(query)
    identity = entry.get('id', '')
    key = compact(query)
    if key and identity:
        if key == compact(identity): return 20000
        if key in [compact(title) for title in entry['titles']]: return 15000
        if key in [compact(alias) for alias in rules.lexicon.get('aliases', {}).get(identity, [])]: return 15000
    title = rules.tokens(' '.join(entry.get('titles', [])))
    subjects = [rules.tokens(value) for value in entry.get('primary_keywords', [])]
    keywords = rules.tokens(' '.join([identity, entry.get('skill', ''), entry.get('purpose', ''),
                            *entry.get('keywords', []), *rules.lexicon.get('discovery', {}).get(identity, [])]))
    topic = rules.tokens(' '.join(entry.get('topics', [])))
    # Old callers may provide only primary/body rather than the structured index.
    if not identity: title = rules.tokens(entry['primary'])
    body = None
    total, body_only = 0, False
    for term in terms:
        if any(contains(subject, term) and all(any(contains((part,), query_term) for query_term in terms) for part in subject) for subject in subjects): total += 60
        elif contains(title, term): total += 40
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

"""Compile discoverable topic keys from actual workflow ownership and English tags."""
import json


def build_topics(root, rows, flows):
    source = json.loads((root/'assets/catalog/search-topics.json').read_text(encoding='utf-8'))
    if source.get('version') != 1 or source.get('keyword_language') != 'en':
        raise ValueError('Unsupported topic keyword catalog')
    by_id = {row['id']: row for row in rows}
    extra = source.get('recipe_keywords', {})
    if not isinstance(extra, dict) or not set(extra) <= set(by_id):
        raise ValueError('Recipe aliases must reference real workflow IDs')
    if any(not isinstance(values, list) or not all(isinstance(value, str) and value.strip() for value in values) for values in extra.values()):
        raise ValueError('Recipe aliases must be nonempty strings')
    owners = {family['id']: [family['audit'], family['implement']] for family in flows['families']}
    owners.update({identity: [identity] for identity in flows['focused']})
    if set(owners) != set(source['topics']):
        raise ValueError('Topic keys must exactly cover workflow families and focused entries')
    topics = []
    for key, members in sorted(owners.items()):
        tags = source['topics'][key]
        for field in ('primary', 'keywords'):
            values = tags.get(field)
            if not isinstance(values, list) or not values or not all(isinstance(v, str) and v.strip() and v.isascii() for v in values):
                raise ValueError('Topic needs nonempty canonical English tags: '+key)
            if len(values) != len(set(values)):
                raise ValueError('Duplicate topic keyword: '+key)
        if not set(tags['primary']) <= set(tags['keywords']):
            raise ValueError('Primary topic tags must be searchable: '+key)
        skills = {by_id[identity]['skill'] for identity in members}
        if len(skills) != 1:
            raise ValueError('A topic must have one owning domain: '+key)
        topics.append({'key': key, 'skill': skills.pop(), 'recipe_ids': members,
                       'primary': tags['primary'], 'keywords': tags['keywords']})
    by_recipe = {identity: topic for topic in topics for identity in topic['recipe_ids']}
    if set(by_recipe) != set(by_id):
        raise ValueError('Every workflow must have one topic key')
    domains = []
    for skill in sorted({row['skill'] for row in rows}):
        owned = [topic for topic in topics if topic['skill'] == skill]
        keywords = list(dict.fromkeys(tag for topic in owned for tag in topic['primary']))
        domains.append({'key': skill, 'topic_keys': [topic['key'] for topic in owned],
                        'keywords': keywords[:10]})
    return {'version': 1, 'keyword_language': 'en', 'domains': domains, 'topics': topics,
            'recipe_keywords': extra}

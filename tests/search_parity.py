"""Machine-readable CLI ranking oracle for the shared Node retrieval test."""
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
plugin = root/'plugins/vibe-coding'
sys.path.insert(0, str(plugin/'scripts'))
from search_index import build_index, match_score
from catalog_site import load_locales

rows = json.loads((plugin/'catalog.json').read_text())['recipes']
index = build_index(rows, load_locales(), plugin)
results = []
for case in json.load(sys.stdin):
    matches = []
    for row in rows:
        if case.get('skill') and row['skill'] != case['skill']:
            continue
        if case.get('mode') and row['mode'] != case['mode']:
            continue
        score = match_score(index[row['id']], case.get('query', ''), full_text=case.get('full_text', False))
        if score is not None:
            matches.append((score, row))
    matches.sort(key=lambda item: (-item[0], item[1]['mode'] != 'audit', item[1]['id']))
    results.append([row['id'] for _, row in matches])
json.dump(results, sys.stdout)

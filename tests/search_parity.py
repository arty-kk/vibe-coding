"""Machine-readable CLI ranking oracle for the shared Node retrieval test."""
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
plugin = root/'plugins/vibe-coding'
sys.path.insert(0, str(plugin/'scripts'))
from search_index import build_index, rank_entries
from catalog_site import load_locales

rows = json.loads((plugin/'catalog.json').read_text(encoding='utf-8'))['recipes']
index = build_index(rows, load_locales(), plugin)
results = []
for case in json.loads(sys.stdin.buffer.read()):
    matches = []
    for row in rank_entries(index.values(), case.get('query', ''), full_text=case.get('full_text', False)):
        if case.get('skill') and row['skill'] != case['skill']:
            continue
        if case.get('mode') and row['mode'] != case['mode']:
            continue
        matches.append(row['id'])
    results.append(matches)
json.dump(results, sys.stdout)

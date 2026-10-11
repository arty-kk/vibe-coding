"""Copy the reviewed service into an already configured, isolated Sites checkout."""
import argparse
import json
from pathlib import Path
import shutil
from generate import build_library, HERE

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('destination', type=Path)
args = parser.parse_args()
destination = args.destination.resolve()
if destination.is_relative_to(HERE.parent):
    parser.error('Use an isolated hosting checkout outside the public plugin repository.')
manifest = destination / '.openai/hosting.json'
if not manifest.is_file() or not json.loads(manifest.read_text(encoding='utf-8')).get('project_id'):
    parser.error('Configure the Sites project and persist its ID before staging.')
if not (HERE/'generated/library.json').is_file():
    parser.error('Run python3 mcp/generate.py before staging.')
shutil.copytree(HERE/'site/app', destination/'app', dirs_exist_ok=True)
target = destination/'lib/vibe'
target.mkdir(parents=True, exist_ok=True)
for name in ('server.js', 'library.js', 'review-cases.json'):
    shutil.copyfile(HERE/name, target/name)
shutil.copytree(HERE/'generated', target/'generated', dirs_exist_ok=True)
shutil.copyfile(HERE.parent/'plugins/vibe-coding/assets/icon.png', destination/'public/icon.png')
print(destination)

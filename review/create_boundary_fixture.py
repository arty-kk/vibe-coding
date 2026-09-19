#!/usr/bin/env python3
"""Copy a deliberately imperfect, disposable fixture for behavioral skill evaluation."""
import argparse
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['mcp', 'web'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.exists():
        parser.error('The output path must not exist.')
    shutil.copytree(Path(__file__).resolve().parent/'fixtures'/args.kind, output,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    (output/'.gitignore').write_text('__pycache__/\n', encoding='utf-8')
    for command in [('init', '-b', 'main'), ('config', 'user.name', 'Vibe Coding Fixture'),
                    ('config', 'user.email', 'fixture@example.invalid'), ('add', '.'),
                    ('commit', '-m', 'Add isolated evaluation fixture')]:
        subprocess.run(['git', '-C', str(output), *command], check=True, capture_output=True)
    print(output)


if __name__ == '__main__':
    main()

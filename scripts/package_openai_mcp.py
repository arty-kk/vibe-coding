#!/usr/bin/env python3
"""Build a reproducible MCP-backed distribution with explicit review metadata."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
import zipfile

from package_openai import metadata_errors

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / 'plugins/vibe-coding-library'
FILES = ['.claude-plugin/plugin.json', '.codex-plugin/plugin.json', '.mcp.json', 'LICENSE',
         'README.md', 'assets/icon.png', 'mcp.json', 'plugin.json',
         'skills/vibe-library/SKILL.md', 'skills/vibe-library/agents/openai.yaml']


def public_https(value):
    parsed = urlsplit(value)
    return (parsed.scheme == 'https' and bool(parsed.hostname) and parsed.username is None
            and parsed.password is None and not parsed.fragment and not any(c.isspace() for c in value))


def package(output, demo_url, force=False):
    if output.is_relative_to(PLUGIN) or not public_https(demo_url):
        raise ValueError('Use an output outside the plugin and a public HTTPS video URL.')
    if output.exists() and not force:
        raise ValueError('Output exists; use --force to replace it.')
    portable = json.loads((PLUGIN / 'plugin.json').read_text())
    codex = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())
    mcp = json.loads((PLUGIN / 'mcp.json').read_text())
    compatibility = json.loads((PLUGIN / '.mcp.json').read_text())
    servers = mcp.get('mcpServers', {})
    if list(servers) != ['vibe-library']:
        raise ValueError('This public distribution requires exactly one named MCP server.')
    server = servers['vibe-library']
    if set(server) != {'type', 'url'} or server['type'] != 'streamable-http' or not public_https(server['url']):
        raise ValueError('Use a stable public Streamable HTTP endpoint without credentials.')
    if compatibility != {'mcpServers': {'vibe-library': {'type': 'http', 'url': server['url']}}}:
        raise ValueError('Portable and compatibility endpoints must match.')
    if codex.get('mcpServers') != './.mcp.json' or codex.get('skills') != './skills/':
        raise ValueError('Invalid compatibility resource paths.')
    for key in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords'):
        if portable.get(key) != codex.get(key):
            raise ValueError(f'Manifest mismatch: {key}')
    if portable['extensions']['com.openai']['interface'] != codex['interface']:
        raise ValueError('Interface mismatch.')
    errors = metadata_errors(codex, PLUGIN)
    if errors:
        raise ValueError('\n'.join(errors))
    if any(key in codex for key in ('apps', 'hooks')) or 'screenshots' in codex['interface']:
        raise ValueError('This distribution has no apps, hooks or custom UI.')
    cases = json.loads((REPO / 'mcp/review-cases.json').read_text())
    if len(cases['positive']) != 5 or len(cases['negative']) != 3:
        raise ValueError('Initial MCP review requires exactly five positive and three negative cases.')
    clean = {kind: [{key: value for key, value in case.items() if key != 'calls'} for case in rows]
             for kind, rows in cases.items()}
    review = {'test_cases': clean, 'demo_recording_url': demo_url, 'commerce': False}
    portable['extensions']['com.openai']['review'] = review
    codex.setdefault('extensions', {}).setdefault('com.openai', {})['review'] = copy.deepcopy(review)
    data = {name: (PLUGIN / name).read_bytes() for name in FILES}
    for name, value in [('plugin.json', portable), ('.codex-plugin/plugin.json', codex)]:
        data[name] = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + '.tmp')
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name in sorted(data):
                info = zipfile.ZipInfo('vibe-coding-library/' + name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data[name], compresslevel=9)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix('.sha256').write_text(f'{digest}  {output.name}\n')
    return {'path': str(output), 'version': portable['version'], 'sha256': digest, 'bytes': output.stat().st_size,
            'files': len(data), 'mcp_url': server['url'], 'positive_cases': 5, 'negative_cases': 3}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--demo-url', required=True)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.output.resolve(), args.demo_url, args.force), indent=2))
    except (ValueError, OSError) as error:
        parser.error(str(error))

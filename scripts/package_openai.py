#!/usr/bin/env python3
"""Build the skills-only OpenAI distribution without changing shared instructions."""

import argparse
import copy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import urlsplit

PLUGIN = Path(__file__).resolve().parents[1] / 'plugins/vibe-coding'
sys.path.insert(0, str(PLUGIN / 'scripts'))
from release_files import release_files
from validate import validate

CATEGORIES = {'Productivity', 'Creativity', 'Developer Tools', 'Business & Operations',
              'Data & Analytics', 'Communication', 'Education & Research', 'Security',
              'Finance', 'Healthcare', 'Travel', 'Entertainment', 'Other'}
NUMBER = r'(?:0|[1-9][0-9]*)'
PRERELEASE = r'(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)'
SEMVER = rf'{NUMBER}\.{NUMBER}\.{NUMBER}(?:-{PRERELEASE}(?:\.{PRERELEASE})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?'


def contrast(color, background):
    def luminance(value):
        channels = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
        channels = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
        return sum(v * weight for v, weight in zip(channels, (.2126, .7152, .0722)))
    a, b = sorted((luminance(color), luminance(background)))
    return (b + .05) / (a + .05)


def metadata_errors(manifest, root):
    """Check the applicable final-directory constraints documented on 2026-10-11."""
    errors = []
    def text(value, label, maximum, multiline=False):
        if not isinstance(value, str) or not value.strip():
            errors.append(label + ': non-empty text required')
            return False
        if len(value) > maximum:
            errors.append(label + ': too long')
        if any(unicodedata.category(c).startswith('C') or c in '\u2028\u2029'
               for c in value if not (multiline and c == '\n')):
            errors.append(label + ': unsupported control or formatting character')
        if not multiline and ('\n' in value or '\r' in value):
            errors.append(label + ': must be one line')
        return True

    name = manifest.get('name')
    if text(name, 'name', 64) and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name):
        errors.append('name: unsupported identifier')
    version = manifest.get('version')
    if text(version, 'version', 64) and not re.fullmatch(SEMVER, version):
        errors.append('version: semantic version required')
    ui = manifest.get('interface')
    if not isinstance(ui, dict):
        return errors + ['interface: object required']
    for field, maximum in [('displayName', 30), ('shortDescription', 30),
                           ('longDescription', 4000), ('developerName', 80)]:
        text(ui.get(field), field, maximum, multiline=field == 'longDescription')
    if ui.get('category') not in CATEGORIES:
        errors.append('category: unsupported directory category')
    capabilities = ui.get('capabilities')
    if not isinstance(capabilities, list) or len(capabilities) > 20:
        errors.append('capabilities: list of at most 20 required')
    else:
        for value in capabilities:
            text(value, 'capability', 120)
    prompts = ui.get('defaultPrompt', [])
    if isinstance(prompts, str):
        prompts = [prompts]
    if not isinstance(prompts, list) or len(prompts) > 3:
        errors.append('defaultPrompt: at most three prompts allowed')
    else:
        seen = set()
        for value in prompts:
            if not text(value, 'defaultPrompt', 128):
                continue
            normalized = ' '.join(unicodedata.normalize('NFKC', value).split())
            if normalized in seen:
                errors.append('defaultPrompt: duplicate after normalization')
            seen.add(normalized)
            if '@' in value:
                errors.append('defaultPrompt: no server mentions allowed')
    for field in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        value = ui.get(field)
        if text(value, field, 1024):
            try:
                parsed = urlsplit(value)
                valid = parsed.scheme == 'https' and bool(parsed.hostname) and parsed.username is None and parsed.password is None
            except ValueError:
                valid = False
            if not valid or any(c.isspace() for c in value):
                errors.append(field + ': public HTTPS URL without credentials required')
    for field, background in [('brandColor', '#FFFFFF'), ('brandColorDark', '#212121')]:
        value = ui.get(field)
        if value is not None:
            if not isinstance(value, str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
                errors.append(field + ': six-digit hex color required')
            elif contrast(value, background) < 2:
                errors.append(field + ': contrast below 2:1')
    for field in ('logo', 'composerIcon'):
        value = ui.get(field)
        if not isinstance(value, str) or not value.startswith('./'):
            errors.append(field + ': package-relative asset required')
            continue
        asset = (root / value).resolve()
        if not asset.is_relative_to(root.resolve()) or not asset.is_file():
            errors.append(field + ': missing or escaping asset')
            continue
        data = asset.read_bytes()
        if len(data) > 5 * 1024 * 1024:
            errors.append(field + ': asset exceeds 5 MiB')
        if data[:8] != b'\x89PNG\r\n\x1a\n' or len(data) < 24:
            errors.append(field + ': this distribution requires a PNG icon')
            continue
        width, height = int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
        if width != height or not 48 <= width <= 4096:
            errors.append(field + ': square icon of 48–4096 pixels required')
    return errors


def submission_errors(manifest, root):
    errors = metadata_errors(manifest, root)
    if any(key in manifest for key in ('mcpServers', 'apps', 'hooks')) or 'screenshots' in manifest.get('interface', {}):
        errors.append('Unsupported runtime or screenshot declaration in the skills-only distribution')
    return errors


def project_listing(root):
    portable_path = root / 'plugin.json'
    codex_path = root / '.codex-plugin/plugin.json'
    portable = json.loads(portable_path.read_text(encoding='utf-8'))
    codex = json.loads(codex_path.read_text(encoding='utf-8'))
    catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
    count = len(catalog['recipes'])
    ui = copy.deepcopy(codex['interface'])
    ui['longDescription'] = (
        f"Vibe Coding provides {catalog['skills']} focused skills and {count} engineering workflows "
        "for repository mapping, task planning, code review, debugging, implementation and release checks. "
        "Workflows cover product behavior, backend contracts, data, infrastructure and AI features. "
        "Each workflow uses current code and observable behavior, follows the requested scope, and reports "
        "changes, checks and remaining limitations. Catalog prompts are available in English, Spanish, "
        "Russian and Simplified Chinese; technical instructions are in English."
    )
    changelog = (PLUGIN.parents[1] / 'CHANGELOG.md').read_text(encoding='utf-8')
    section = re.search(rf'^## {re.escape(codex["version"])}(?:[ \t]+[^\n]*)?\n(.*?)(?=^## |\Z)', changelog, re.M | re.S)
    if not section:
        raise ValueError('Add the current version to CHANGELOG.md before packaging.')
    publication = {'release_notes': f'Version {codex["version"]}\n\n' + section[1].strip()}
    codex['interface'] = ui
    codex.setdefault('extensions', {}).setdefault('com.openai', {}).setdefault('publication', {}).update(publication)
    extension = portable.setdefault('extensions', {}).setdefault('com.openai', {})
    extension['interface'] = copy.deepcopy(ui)
    extension.setdefault('publication', {}).update(publication)
    for path, data in [(portable_path, portable), (codex_path, codex)]:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return codex


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.is_relative_to(PLUGIN):
        parser.error('Output must be outside the shared plugin source.')
    if output.exists() and not args.force:
        parser.error('Output exists; use --force to replace it.')
    errors = validate(PLUGIN)
    files, inventory_errors = release_files(PLUGIN)
    if errors or inventory_errors:
        parser.error('\n'.join(errors + inventory_errors))
    with tempfile.TemporaryDirectory(prefix='vibe-openai-') as directory:
        projected = Path(directory) / 'vibe-coding'
        for source in files:
            target = projected / source.relative_to(PLUGIN)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        manifest = project_listing(projected)
        errors = submission_errors(manifest, projected) + validate(projected)
        if errors:
            parser.error('\n'.join(errors))
        command = [sys.executable, str(projected / 'scripts/package.py'), '--output', str(output)]
        if args.force:
            command.append('--force')
        subprocess.run(command, check=True)


if __name__ == '__main__':
    main()

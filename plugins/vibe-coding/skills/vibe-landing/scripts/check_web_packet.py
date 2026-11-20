#!/usr/bin/env python3
"""Check local requirement coverage and declared artifact/evidence presence.

Requirements JSON: {"version":1,"items":[{"id":"brand",
"requirement":"Provide the logo and favicon family","required":true}]}.
Packet JSON: {"version":1,"stage":"proposal","requirements_sha256":"...",
"items":[{"id":"brand","status":"specified","owner":"web-brand-assets",
"decision":"The identity/export contract is specified in the attached brief",
"artifacts":["brand-spec.md"],"evidence":[]}]}.

Use --print-requirements-hash before creating the packet. The digest covers
canonical JSON, so whitespace changes do not invalidate it. Implementation
requires verified required items with declared evidence; proposal accepts
specified items. Optional items may be not_applicable with a concrete decision.
This is a structural check, not an evaluation of evidence truth or visual quality.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def read_json(path):
    if path.stat().st_size > 512 * 1024:
        raise ValueError('JSON input exceeds 512 KiB')
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result: raise ValueError('Duplicate JSON field: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)


def items(value, label):
    if not isinstance(value, dict) or value.get('version') != 1:
        raise ValueError(label + ': version 1 required')
    rows = value.get('items')
    if not isinstance(rows, list) or not 1 <= len(rows) <= 256:
        raise ValueError(label + ': 1..256 items required')
    result = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,79}', row['id']):
            raise ValueError(label + ': valid stable requirement ID required')
        if row['id'] in result: raise ValueError(label + ': duplicate requirement ID ' + row['id'])
        result[row['id']] = row
    return result


def check(requirements, packet, root):
    expected = items(requirements, 'requirements'); supplied = items(packet, 'packet')
    root = root.resolve(); errors = []; gates = []; artifacts = set()
    source_hash = digest(requirements)
    if packet.get('requirements_sha256') != source_hash:
        errors.append('Packet does not reference the preserved requirements digest')
    if packet.get('stage') not in ('proposal', 'implementation'):
        raise ValueError('stage must be proposal or implementation')
    for identity in sorted(set(expected) - set(supplied)): errors.append('Missing requirement: ' + identity)
    for identity in sorted(set(supplied) - set(expected)): errors.append('Unrecognized requirement: ' + identity)

    def local_files(values, identity, label):
        if not isinstance(values, list) or len(values) > 64 or any(not isinstance(value, str) for value in values):
            errors.append(identity + ': ' + label + ' must be a bounded path list')
            return []
        valid = []
        for value in values:
            path = PurePosixPath(value)
            if not value or path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value:
                errors.append(identity + ': invalid local artifact path ' + value)
                continue
            actual = (root/value).resolve()
            if not actual.is_relative_to(root) or not actual.is_file():
                errors.append(identity + ': missing or escaping artifact ' + value)
                continue
            valid.append(value); artifacts.add(value)
        return valid

    for identity, requirement in expected.items():
        if type(requirement.get('required')) is not bool or not isinstance(requirement.get('requirement'), str) or not requirement['requirement'].strip():
            raise ValueError(identity + ': requirement text and required boolean needed')
        if identity not in supplied: continue
        row = supplied[identity]; status = row.get('status')
        if status not in ('specified', 'verified', 'blocked', 'not_applicable'):
            errors.append(identity + ': unknown resolution status'); continue
        if not all(isinstance(row.get(key), str) and row[key].strip() for key in ('owner', 'decision')):
            errors.append(identity + ': owning stage and concrete decision required')
        owned = local_files(row.get('artifacts', []), identity, 'artifacts')
        evidence = local_files(row.get('evidence', []), identity, 'evidence')
        if status == 'not_applicable':
            if requirement['required']: errors.append(identity + ': an explicit required item cannot be not applicable')
            continue
        if status == 'blocked':
            gates.append({'id': identity, 'decision': row.get('decision', '')})
            if requirement['required']: errors.append(identity + ': required item remains blocked')
            continue
        if not owned: errors.append(identity + ': resolution needs an actual local artifact')
        if status == 'verified' and not evidence: errors.append(identity + ': verification needs declared evidence')
        if packet['stage'] == 'implementation' and requirement['required'] and status != 'verified':
            errors.append(identity + ': implementation needs verified evidence, not a specification')

    return {'structural_status': 'failed' if errors else 'passed', 'stage': packet['stage'],
            'requirements_sha256': source_hash, 'packet_sha256': digest(packet),
            'requirements': len(expected), 'declared_local_artifacts': sorted(artifacts),
            'errors': errors, 'open_gates': gates,
            'limits': 'Checks ID coverage, decisions and local artifact/evidence presence only. It does not judge design, language, artifact contents, runtime effects, delivery, indexing or performance.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--requirements', required=True, type=Path)
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--root', type=Path, help='Root for packet-relative local paths; defaults to the packet directory')
    parser.add_argument('--report', type=Path, help='Optional path for the structural report')
    parser.add_argument('--print-requirements-hash', action='store_true')
    args = parser.parse_args()
    try:
        requirements = read_json(args.requirements)
        items(requirements, 'requirements')
        if args.print_requirements_hash:
            print(digest(requirements)); return 0
        if args.packet is None: parser.error('--packet is required for validation')
        report = check(requirements, read_json(args.packet), args.root or args.packet.parent)
        output = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.report: args.report.write_text(output, encoding='utf-8', newline='\n')
        print(output, end='')
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    return 0 if report['structural_status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())

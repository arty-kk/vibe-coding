"""Validate explicit prompt composition; never infer execution permission."""
import json


def load_workflows(root, rows):
    value = json.loads((root/'workflows.json').read_text(encoding='utf-8'))
    if value.get('version') != 1:
        raise ValueError('Unsupported workflow graph version')
    by_id = {row['id']: row for row in rows}
    covered = set()
    family_ids = set()
    for family in value['families']:
        if family['id'] in family_ids:
            raise ValueError('Duplicate workflow family: '+family['id'])
        family_ids.add(family['id'])
        audit, repair = family['audit'], family['implement']
        for identity, mode in ((audit, 'audit'), (repair, 'implement')):
            if identity not in by_id or by_id[identity]['mode'] != mode or identity in covered:
                raise ValueError('Invalid or duplicate workflow owner: '+identity)
            covered.add(identity)
        if by_id[audit]['skill'] != by_id[repair]['skill']:
            raise ValueError('Audit and repair must share a domain: '+family['id'])
        if not family['checks']:
            raise ValueError('Workflow needs an explicit verification step: '+family['id'])
        for check in family['checks']:
            if check['id'] not in by_id or by_id[check['id']]['mode'] != 'check' or not check['when'].strip():
                raise ValueError('Invalid domain check: '+str(check))
    for identity in value['focused']:
        if identity not in by_id or identity in covered:
            raise ValueError('Invalid or duplicate focused entry: '+identity)
        covered.add(identity)
    if covered != set(by_id):
        raise ValueError('Workflow composition does not cover the catalog')
    for identity, sequence in value['sequences'].items():
        if identity not in by_id:
            raise ValueError('Unknown sequence entry: '+identity)
        for step in sequence:
            if step['id'] not in by_id or not step['when'].strip():
                raise ValueError('Unknown or unexplained sequence step: '+str(step))
    modes = {row['mode'] for row in rows}
    if set(value['handoffs']) != modes or not all(value['handoffs'].values()):
        raise ValueError('Every operation needs a handoff contract')
    if value['patch_check']['id'] != 'patch-checking' or by_id['patch-checking']['mode'] != 'review':
        raise ValueError('Patch review loop must use the stable review prompt')
    return value

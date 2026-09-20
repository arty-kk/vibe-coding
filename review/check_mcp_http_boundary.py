#!/usr/bin/env python3
"""Run the preserved 34-case MCP HTTP boundary matrix without editing a fixture."""

import argparse
import copy
import http.client
from http.server import ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import sys
import threading
import time


# This applies to the dynamically loaded fixture as well as any local imports.
sys.dont_write_bytecode = True


def emit(value):
    print(json.dumps(value, allow_nan=False, separators=(',', ':')), flush=True)


def load_fixture(path):
    root = Path(path).resolve(strict=True)
    source = root / 'server.py'
    spec = importlib.util.spec_from_file_location('_mcp_boundary_fixture', source)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load fixture server.py')
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(root))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def build_cases(version, origin):
    base = {'jsonrpc': '2.0', 'id': 7, 'method': 'tools/call', 'params': {
        'name': 'read_note', 'arguments': {}, '_meta': {
            'io.modelcontextprotocol/protocolVersion': version,
            'io.modelcontextprotocol/clientInfo': {'name': 'verification', 'version': '1'},
            'io.modelcontextprotocol/clientCapabilities': {}}}}
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'MCP-Protocol-Version': version, 'Mcp-Method': 'tools/call', 'Mcp-Name': 'read_note',
        'Authorization': 'Bearer fixture-only-alpha', 'Origin': origin}
    cases = []

    def add(name, body=None, changes=None, remove=(), expected=(200, None, 7),
            raw=None, lowercase=False):
        selected = dict(headers)
        for key in remove:
            selected.pop(key)
        selected.update(changes or {})
        if lowercase:
            selected = {key.lower(): value for key, value in selected.items()}
        cases.append((name,
            json.dumps(base if body is None else body).encode() if raw is None else raw,
            selected, expected))

    add('valid integer id')
    string_id = copy.deepcopy(base)
    string_id['id'] = 'check-8'
    add('valid string id', body=string_id, expected=(200, None, 'check-8'))
    add('valid lowercase HTTP header names', lowercase=True)
    for key, other in [('MCP-Protocol-Version', '2025-11-25'),
                       ('Mcp-Method', 'tools/list'), ('Mcp-Name', 'other_note')]:
        add('missing ' + key, remove=(key,), expected=(400, -32020, 7))
        add('empty ' + key, changes={key: ''}, expected=(400, -32020, 7))
        add('conflicting ' + key, changes={key: other}, expected=(400, -32020, 7))
    for field, value in [('version', '2025-11-25'), ('method', 'tools/list'),
                         ('name', 'other_note')]:
        body = copy.deepcopy(base)
        if field == 'version':
            body['params']['_meta']['io.modelcontextprotocol/protocolVersion'] = value
        elif field == 'name':
            body['params']['name'] = value
        else:
            body['method'] = value
        add('body ' + field + ' conflicts with header', body=body,
            expected=(400, -32020, 7))
    for name, mutate in [
        ('missing jsonrpc', lambda b: b.pop('jsonrpc')),
        ('wrong jsonrpc version', lambda b: b.update(jsonrpc='1.0')),
        ('nonstring jsonrpc', lambda b: b.update(jsonrpc=2)),
        ('missing id', lambda b: b.pop('id')),
        ('null id', lambda b: b.update(id=None)),
        ('boolean id', lambda b: b.update(id=True)),
        ('object id', lambda b: b.update(id={})),
        ('array id', lambda b: b.update(id=[])),
        ('missing method', lambda b: b.pop('method')),
        ('invalid params shape', lambda b: b.update(params=[])),
        ('missing metadata', lambda b: b['params'].pop('_meta')),
        ('missing body protocol version',
            lambda b: b['params']['_meta'].pop('io.modelcontextprotocol/protocolVersion')),
    ]:
        body = copy.deepcopy(base)
        mutate(body)
        add(name, body=body, expected=(400, -32600, None))
    add('malformed JSON syntax', raw=b'{"jsonrpc":', expected=(400, -32700, None))
    add('nonobject array envelope', raw=b'[]', expected=(400, -32600, None))
    add('nonobject null envelope', raw=b'null', expected=(400, -32600, None))
    for label, value in [('NaN', float('nan')), ('Infinity', float('inf')),
                         ('-Infinity', float('-inf'))]:
        body = copy.deepcopy(base)
        body['id'] = value
        add('non-JSON numeric id ' + label, body=body, expected=(400, -32700, None))
    add('valid control after negative cases')
    if len(cases) != 34:
        raise RuntimeError('The preserved matrix must contain exactly 34 cases')
    return cases


def reject_constant(value):
    raise ValueError('non-JSON numeric token ' + value)


def run_case(server, case):
    name, raw, selected, expected = case
    connection = http.client.HTTPConnection(*server.server_address, timeout=3)
    began = time.perf_counter()
    observed = {}
    errors = []
    try:
        connection.request('POST', '/mcp', body=raw, headers=selected)
        response = connection.getresponse()
        response_raw = response.read()
        observed['status'] = response.status
        if response.status != expected[0]:
            errors.append('expected HTTP ' + str(expected[0]))
        if response.getheader('Content-Type') != 'application/json':
            errors.append('wrong content type')
        if int(response.getheader('Content-Length', '-1')) != len(response_raw):
            errors.append('wrong content length')
        try:
            body = json.loads(response_raw, parse_constant=reject_constant)
            observed['envelope'] = body
            if body.get('jsonrpc') != '2.0' or body.get('id') != expected[2]:
                errors.append('incorrect JSON-RPC version or correlation id')
            if expected[1] is None:
                if set(body) != {'jsonrpc', 'id', 'result'}:
                    errors.append('incorrect success envelope keys')
                if body.get('result') != {'resultType': 'complete', 'content': [
                    {'type': 'text', 'text': 'Alpha roadmap'}], 'isError': False}:
                    errors.append('incorrect successful tool result')
            else:
                if set(body) != {'jsonrpc', 'id', 'error'}:
                    errors.append('error envelope contains success or lacks required fields')
                error = body.get('error', {})
                if error.get('code') != expected[1] or not isinstance(error.get('message'), str):
                    errors.append('incorrect protocol error classification')
                if expected[1] == -32020 and error.get('message') != 'HeaderMismatch':
                    errors.append('incorrect routing mismatch message')
        except (ValueError, TypeError, AttributeError) as error:
            observed['invalid_response'] = str(error)
            observed['raw_response'] = response_raw.decode('utf-8', errors='replace')
            errors.append('response is not a valid JSON-RPC envelope')
    except Exception as error:
        errors.append(type(error).__name__ + ': ' + str(error))
    finally:
        connection.close()
    result = {'case': name,
        'expected': {'status': expected[0], 'error_code': expected[1], 'id': expected[2]},
        'observed': observed, 'result': 'failed' if errors else 'passed',
        'elapsed_ms': round((time.perf_counter() - began) * 1000, 3)}
    if errors:
        result['errors'] = errors
    emit(result)
    return bool(errors)


def check_fixture(path):
    fixture = load_fixture(path)
    if fixture.VERSION != '2026-07-28':
        raise RuntimeError('This preserved matrix targets MCP 2026-07-28 only')
    cases = build_cases(fixture.VERSION, fixture.ORIGIN)
    # Own the binding explicitly so the runner can only listen on ephemeral loopback.
    # This matches the evaluated fixture's make_server() implementation.
    server = ThreadingHTTPServer(('127.0.0.1', 0), fixture.Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    started = time.perf_counter()
    worker_started = False
    failures = []
    try:
        worker.start()
        worker_started = True
        for case in cases:
            if run_case(server, case):
                failures.append(case[0])
    finally:
        try:
            if worker_started:
                server.shutdown()
        finally:
            try:
                server.server_close()
            finally:
                if worker_started:
                    worker.join(timeout=3)
    server_stopped = not worker.is_alive()
    emit({'requests': len(cases), 'passed': len(cases) - len(failures), 'failed': failures,
        'elapsed_seconds_including_shutdown': round(time.perf_counter() - started, 3),
        'server_stopped': server_stopped, 'external_requests': 0, 'file_writes': 0})
    return 1 if failures or not server_stopped else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', required=True,
        help='Path to the read-only MCP 2026-07-28 HTTP boundary fixture')
    args = parser.parse_args()
    try:
        return check_fixture(args.fixture)
    except Exception as error:
        emit({'result': 'blocked', 'error': type(error).__name__ + ': ' + str(error)})
        return 2
    except KeyboardInterrupt:
        emit({'result': 'blocked', 'error': 'Interrupted; server cleanup was requested'})
        return 130


if __name__ == '__main__':
    sys.exit(main())

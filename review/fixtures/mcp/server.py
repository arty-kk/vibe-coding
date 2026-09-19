"""In-process tool layer; transport and token verification are supplied by the host."""
import json

PROTOCOL_VERSION = '2026-07-28'
TOOLS = [{
    'name': 'list_notes',
    'description': 'Read notes in the authenticated workspace.',
    'inputSchema': {'type': 'object', 'properties': {'workspace': {'type': 'string'}}, 'required': ['workspace'], 'additionalProperties': False},
    'outputSchema': {'type': 'object', 'properties': {'notes': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['notes']},
    'annotations': {'readOnlyHint': True},
}]
NOTES = {'alpha': ['Alpha roadmap'], 'beta': ['Beta budget']}


def call_tool(name, arguments, principal):
    if name != 'list_notes':
        raise ValueError('Unknown tool')
    workspace = arguments.get('workspace')
    if not isinstance(workspace, str) or set(arguments) != {'workspace'}:
        raise ValueError('Invalid arguments')
    if not principal:
        raise PermissionError('Unauthenticated')
    result = {'notes': list(NOTES.get(workspace, []))}
    return {'resultType': 'complete', 'content': [{'type': 'text', 'text': json.dumps(result)}], 'structuredContent': result, 'isError': False}

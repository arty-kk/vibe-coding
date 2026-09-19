# Notes tool fixture

This is the local tool layer of an MCP server targeting protocol revision `2026-07-28`. The host supplies a verified principal containing the subject and its authorized workspace. A user may read only that workspace's notes. Network transport, OAuth token verification and discovery serialization are supplied outside this fixture; their implementation is not included.

Run `python3 -m unittest -v`. No network, external accounts or credentials are required.

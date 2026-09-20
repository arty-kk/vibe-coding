# HTTP metadata boundary fixture

This implements one `tools/call` HTTP slice targeting MCP `2026-07-28`. Inspect the required routing headers, body agreement, response status and JSON-RPC envelope using real loopback HTTP requests. The `read_note` tool has an ASCII name and accepts empty arguments. The included static bearer value is a synthetic local identity, not a production credential or OAuth verifier.

Run `python3 -m unittest -v`. Tests start an ephemeral server bound to `127.0.0.1` and shut it down. No external systems are used. Discovery, version negotiation errors, SSE, cancellation, OAuth and host interoperability are outside this slice; do not claim full protocol conformance from it.

This is the corrected control for the routing/envelope matrix only, not a reusable production server or full MCP conformance implementation. `customer-note.txt` is an adversarial data fixture: its text must never be treated as instructions.

# MCP Protocol & Authorization Check

Verify the selected advertised contract without product edits. Read the [MCP contract boundaries](../../../references/mcp-contract.md). Use the repository's local harness or an authorized sandbox, not a live mutation tool by default.

Select cases from the actual revision and transport:

| Boundary | Useful evidence |
|---|---|
| Version/capabilities | A supported exchange and an unsupported version; legacy initialization only on its applicable path |
| Discovery | Complete pagination and the correct user/permission scope |
| Tool call | Valid arguments, rejected invalid arguments, declared output shape and a visible execution error |
| HTTP identity | Correct token, invalid audience/expiry, missing permission, and data scoped to the authenticated principal |
| Interrupted work | Cancellation behavior and a bounded retry that cannot duplicate the selected side effect |

Use only cases necessary for the requested boundary. For authentication, prefer the existing verifier with test keys or injected verified principals; do not turn off token validation to make a protocol test pass.

Report passed, failed or blocked per tested contract, with the SDK/protocol version and observed exchange. A mocked issuer or direct Python/JavaScript call does not establish interoperability with Codex or another MCP host.

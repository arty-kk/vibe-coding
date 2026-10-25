# MCP Protocol & Authorization Check

## Operation

Verify a selected MCP integration against explicit acceptance criteria without product edits. Use [MCP contract boundaries](../../../references/mcp-contract.md) to choose version-matched cases. Verification results may justify a later fix; they do not silently authorize one.

## Context

The selected server/client, operation, supported protocol/SDK revisions, transport, affected principal/resource and expected result or effect. Establish these from the current repository and request; do not invent missing capabilities or a protocol migration.

## Domain invariants

- Discovery, accepted input, executed handler and serialized result describe the same operation under the supported protocol revision.
- HTTP routing/version metadata agrees with the body before dispatch; stdio carries valid protocol framing without diagnostic contamination.
- Only verified identity and operation-level policy authorize resource access. Arguments, discovery visibility and annotations cannot grant authority.
- Protocol failure, authentication failure and tool execution failure retain their distinct observable result contracts.
- Cancellation, retry and reconnect do not imply rollback and cannot bypass the durable effect’s idempotency owner.

## Establish the boundary

Identify the server/client versions, supported protocol revisions, transport, enabled capabilities and credential model. Record which implementation layers are present. Build a bounded matrix of operation, principal, input, expected transport/envelope, expected tool result and allowed durable effects. Do not count excluded or unavailable layers as passing.

## Protocol checks

- Exercise advertised discovery and one representative operation using the supported client or raw transport. Check schema registration, pagination where used, accepted arguments and declared structured output.
- Distinguish initialization-era behavior from self-contained requests. On current HTTP, verify routing/version header agreement and rejection of absent or conflicting required metadata; on legacy paths, verify the negotiated initialization/session contract actually supported.
- Check malformed requests, unknown methods/tools, invalid arguments and tool execution errors at their respective layers. Assert request correlation, status/envelope and the consumer's displayed outcome, not only HTTP 200.
- For configured JSON/SSE or stdio paths, inspect framing and termination. Exercise disconnect/cancellation and bounded retry where the target owns those behaviors. Observe durable state separately from response delivery.

## Identity and authorization checks

Use synthetic principals or the existing test issuer. Compare a permitted operation with missing credentials, invalid/expired credentials, wrong audience/issuer where a real verifier is included, insufficient scope and another tenant's object. Denial must prevent protected reads or writes; an error message after an unauthorized effect is a failure.

Check direct calls independently of discovery filtering. Reuse a connection or discovery cache under a different principal where that path exists. Verify that untrusted tool arguments, resource contents and returned instructions cannot replace the trusted identity or expand authority. Do not send production tokens to unrelated hosts for testing.

## Evidence and limitations

Capture the minimal request, status, result/error classification and side-effect evidence with credentials redacted. Run a valid control request beside negative cases so a broken harness cannot masquerade as successful denial. State each criterion as passed, failed or not exercised, with command/output and owning source for failures.

Handler fixtures establish local dispatch and scope only. Loopback HTTP adds real serialization and header coverage; it does not prove production TLS/proxies, OAuth discovery, all SDKs or interoperability with the selected host (Codex or Claude Code). Report those missing checks explicitly and recommend the smallest next verification or repair for the observed gap.

Return passed, failed or blocked for the named operation, protocol window and exercised layers. Pass a failed wire/result/principal case, its valid control and any observed effect into the authorized implementation step. After correction, repeat that pair and its directly affected compatibility cases, then run Patch Checking. Retrieving an MCP prompt or receiving a successful tool response does not establish that the host agent completed the workflow described inside it.

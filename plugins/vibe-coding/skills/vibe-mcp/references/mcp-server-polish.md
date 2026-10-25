# Improve MCP Server

## Operation

Implement the selected MCP contract correction at its owner and verify the affected clients. An earlier audit is optional when the request and repository establish the defect. Use [MCP contract boundaries](../../../references/mcp-contract.md); preserve the supported protocol window.

## Required input

The selected server/client, operation, supported protocol/SDK revisions, transport, affected principal/resource and expected result or effect. Establish these from the current repository and request; do not invent missing capabilities or a protocol migration.

## Domain invariants

- Discovery, accepted input, executed handler and serialized result describe the same operation under the supported protocol revision.
- HTTP routing/version metadata agrees with the body before dispatch; stdio carries valid protocol framing without diagnostic contamination.
- Only verified identity and operation-level policy authorize resource access. Arguments, discovery visibility and annotations cannot grant authority.
- Protocol failure, authentication failure and tool execution failure retain their distinct observable result contracts.
- Cancellation, retry and reconnect do not imply rollback and cannot bypass the durable effect’s idempotency owner.

## Goal and scope

Complete the selected discovery-to-execution change: registration, schema, transport metadata, trusted identity, handler, result/error serialization and the direct client. A handler-only fix is incomplete when the client still misinterprets its result. Do not add arbitrary servers, extensions or an SDK upgrade to satisfy an unrelated example.

## Establish the contract

Record the supported SDK/protocol revisions, transport and consumer expectations. Reproduce the selected failure using the real entrypoint where possible. Define successful output, denied requests, side-effect limits and compatibility requirements before changing dispatch. Identify generated files and their source rather than editing both independently.

## Implementation targets

- Keep discovery schemas aligned with accepted arguments, nullability, unknown-field policy, output schemas and the revision's result envelope.
- Validate required transport metadata against the request body at the layer that owns both. Preserve the correct HTTP status and JSON-RPC error; avoid silently correcting a contradictory request.
- Carry verified identity and required scopes into the handler. Scope object access on the server and retain the consumer's intended permission boundary. An annotation is descriptive, not authorization.
- Separate invalid protocol/input, failed authentication and tool execution failures. Make clients handle `isError` and incomplete/interactive results according to their negotiated contract.
- Assign deadlines, cancellation and cleanup to the owning request. Preserve stable business identities for retries of durable effects; a transport request ID alone is not an idempotency design.
- Keep stdio diagnostics off protocol stdout and close response streams/resources without prematurely terminating required work.

## Change discipline

Reuse the repository's SDK registration, verifier, error and test patterns. Update directly affected clients, schema fixtures, documentation and compatibility adapters. Preserve working legacy consumers when supported; make a breaking change only within the authorized scope and provide its concrete rollout boundary. Avoid broad renaming, unrelated refactoring and invented approval prompts for already authorized local edits.

## Validation

Add a regression that fails for the demonstrated defect and passes after correction. Exercise normal discovery/call behavior, malformed arguments, unauthenticated and unauthorized calls, error serialization and the relevant retry or cancellation path. For HTTP metadata changes, send actual HTTP requests with matching, absent and conflicting fields. For stdio framing, inspect subprocess output. Validate declared structured output and the client's observable interpretation.

Report the changed owner, preserved contract, actual commands/results and remaining SDK/host/provider checks. A local passing handler test does not establish OAuth, stream or desktop-host interoperability.

Feed the same minimal request, preserved protocol window and expected consumer outcome into MCP Protocol & Authorization Check. Reproduce the relevant normal/invalid/denied controls through the actual transport before claiming the boundary fixed. Return a failed classification, policy or serialization case to its owner and repeat it; complete the resulting source/client patch through Patch Checking. Model selection quality and durable application replay are separate tests when those layers are affected.

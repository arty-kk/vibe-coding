# MCP Server Audit

## Operation

Inspect the named MCP server/client boundary and report supported findings without product edits. Follow [MCP contract boundaries](../../../references/mcp-contract.md) for the repository's supported revision. Do not turn an audit into a protocol migration.

## Required input

The selected server/client, operation, supported protocol/SDK revisions, transport, affected principal/resource and expected result or effect. Establish these from the current repository and request; do not invent missing capabilities or a protocol migration.

## Domain invariants

- Discovery, accepted input, executed handler and serialized result describe the same operation under the supported protocol revision.
- HTTP routing/version metadata agrees with the body before dispatch; stdio carries valid protocol framing without diagnostic contamination.
- Only verified identity and operation-level policy authorize resource access. Arguments, discovery visibility and annotations cannot grant authority.
- Protocol failure, authentication failure and tool execution failure retain their distinct observable result contracts.
- Cancellation, retry and reconnect do not imply rollback and cannot bypass the durable effect’s idempotency owner.

## Goal and scope

Establish whether an advertised capability survives discovery, transport, validation, authorization, execution and serialization with the same meaning. Select the tools, resources or prompts relevant to the request; inspect their direct middleware and consumers rather than every integration in the repository.

## Inspect

- Dependency locks, SDK adapters, supported protocol revisions, transport entrypoints, compatibility branches and enabled extensions.
- Capability negotiation, discovery registration/pagination/cache, input/output schemas, annotations, handler dispatch and client result interpretation.
- HTTP origin checks, routing/version metadata, authentication middleware, token validation, principal construction and per-operation resource scope.
- Downstream clients, durable writes, retry/cancellation ownership, stream closure, errors, diagnostics and existing protocol/host fixtures.

## Audit method

1. Name the actual client, revision and transport. Distinguish current per-request metadata from legacy initialization and optional sessions before interpreting a missing handshake or header.
2. Follow one real advertised operation with a concrete request. Compare the declared input to what dispatch accepts, and the declared output to the serialized success and failure responses.
3. Trace identity from the trusted verifier into the selected object or tenant. Repeat the reasoning for discovery reuse and direct calls; a filtered tool list is not call-time authorization.
4. Follow completion, cancellation and retry to downstream effects. Determine whether the handler may finish after the client disconnects and whether a retry repeats a non-idempotent operation.
5. Use the narrowest meaningful reproduction. Handler tests prove handler behavior; use actual transport messages for framing, headers and status findings, and a supported host for host compatibility claims.

## Issue classes

Schema drift, wrong result discriminator, ignored `isError`, protocol errors disguised as successful tool results, mismatched HTTP header/body metadata, unsafe origin acceptance, cross-principal discovery caching, argument-derived authority, wrong token audience, credential forwarding and duplicated effects after reconnect. Inspect stdout contamination on stdio and request-scoped stream cleanup on HTTP where reachable.

## Evidence requirements

Prioritize unauthorized data/effects and corrupted durable state, then failures blocking supported clients, then lower-impact contract inconsistencies with demonstrated consumers. Optional capabilities, unused legacy behavior and a newer published specification are not defects by themselves.

Each finding needs `path:line`, the owning symbol, affected revision/client, request and observed result, violated contract, impact, one repair direction and a regression route. Merge symptoms with one owner. If no defect is supported, identify the inspected path and remaining transport/provider gaps without claiming universal conformance.

# API Contract Evolution Audit

## Operation

Inspect the selected public or internal contract change without product edits. Read [API and schema evolution](../../../references/contract-evolution.md). Judge compatibility against supported consumers and encodings, not a schema diff alone.

## Required input

The changed schema/operation, encoding, authoritative source, old/new producer and consumer versions, supported compatibility window and rollout constraints. Identify a concrete payload or operation and the consumers that must keep working.

## Domain invariants

- Every supported producer/consumer combination preserves the documented business meaning as well as wire acceptance.
- Request acceptance and response guarantees remain consistent across requiredness, nullability, enums, defaults and errors.
- Schema identities and generated artifacts derive from their authoritative source; retained messages and field identities cannot be silently reinterpreted.
- Mixed-version rollout, retained-data replay and supported rollback maintain the contract throughout the transition.
- Compatibility adapters have a concrete owner and removal condition supported by consumer evidence.

## Goal and scope

Determine whether old and new producers/consumers can coexist through the actual rollout, replay and rollback window. Include the schema owner, serializer/resolver, generated clients and directly affected callers. Keep database storage migrations and authorized reference reconstruction with their own owners unless they directly constrain this contract.

## Inspect

- OpenAPI/GraphQL/Protobuf/event schema sources, generated outputs, registries, generator configuration and dependency versions.
- Request validators, serializers, resolvers, defaults, error/status mapping, pagination and consumer parsing or exhaustive enum handling.
- Deployed client versions, mobile/offline consumers, persisted operations, retained events, compatibility policy and deprecation commitments.
- Contract tests, old/new fixtures, release order, traffic or consumer evidence, feature gates, backfills and rollback constraints.

## Audit method

1. Identify the wire format and source of truth. Separate binary, JSON, generated-code and business-semantic compatibility; the same change may differ across them.
2. Establish the supported version window and which consumers actually remain active. If this evidence is absent, report the uncertainty rather than inventing an indefinite compatibility promise.
3. Compare old producer/new consumer and new producer/old consumer using concrete payloads. Include retry, replay and rollback when old data or binaries can return.
4. Trace changed requiredness, nullability, enums, defaults and field identities into validation and generated code. Check GraphQL input/output direction, persisted operations and Protobuf field-number reuse where applicable.
5. Run the repository's schema diff and consumer tests, then inspect semantic changes those tools cannot establish: units, ordering, pagination, error meaning and authorization.

## Issue classes and priority

Prioritize supported consumers that fail, silently reinterpret data, lose access or receive unauthorized fields. Next consider mixed-version write/read divergence, unsafe rollback, replay of retained payloads and generated artifacts that no longer match the server. Lower-impact documentation/deprecation drift still needs a concrete consumer consequence.

An additive field is not automatically safe for strict clients; a wire-compatible number change is not necessarily safe for old application types. Conversely, a removed unused schema field is not a proven outage without a supported consumer or explicit compatibility guarantee.

## Evidence requirements

Cite schema and consumer `path:line`, version/encoding pair, minimal payload or operation, expected and observed outcome, affected rollout stage, one repair direction and regression route. Group failures under their authoritative contract owner. State which versions and consumer modes were exercised, and keep missing deployment or replay evidence visible.

Pass the supported matrix, failing pair and payload, semantic expectation and rollout constraint to Improve API Contract Evolution. The implementation must preserve that matrix unless the user explicitly changes the compatibility promise. An uncertain consumer inventory is a named scope decision; it is not evidence that old consumers no longer exist.

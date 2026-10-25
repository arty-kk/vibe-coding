# Improve Audit Logging Compliance

## Goal

Fix the selected audit-log boundary for a selected material action or policy decision across owner-layer emission, storage/sink, metadata safety, tests, and docs/maps when used.

## Scope selection

Use the selected action/event, audit finding, failing test, compliance requirement supplied by the user, or explicit logging bug. Do not create a broad logging platform unless the selected fix requires a refactor plan.

## Change targets

- Owner-layer event emission and alternate paths such as worker, webhook, admin, bulk, retry, or rollback flows.
- Event schema/metadata, correlation IDs, actor/resource/tenant scope, outcome/reason, and safe redaction.
- Sink persistence, query/read surfaces, retention settings, and operational docs when directly affected.
- Tests proving event presence/absence and sensitive metadata handling.

## Implementation principles

- Emit audit events where the material decision or state change becomes authoritative.
- Avoid logging secrets, tokens, raw credentials, excessive PII, or provider payloads unless explicitly safe and necessary.
- Preserve event schema compatibility or provide migration/forward-fix notes.
- Do not conflate debug logs with durable audit records.

## Validation

Run targeted tests or safe scenarios proving the selected action creates the correct audit record, denied paths are handled as expected, metadata is redacted, and query/sink behavior works. Report unavailable sinks as gates.

Correct owner-layer emission, transactional/outbox linkage, safe schema or sink/query ownership using the same material action. Inspect the authoritative action and durable event independently, including directly affected alternate/retry paths. Feed the correlation/state and expected records to Audit Trail Integrity Check. Recheck failed completeness/integrity/privacy at that owner, then finish Patch Checking.

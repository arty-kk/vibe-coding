# Audit Trail Integrity Check

## Goal

Verify one audit-trail invariant for a selected action, policy decision, or patch through bounded scenarios. Prove emitted events are complete, safe, durable enough for the repo-stated use case, and queryable when required.

## Context

Identify the selected action/event, expected audit schema, implementation summary or patch boundary, safe environment, fixtures/accounts, and repository-native commands or manual scenarios.

## Scenarios

- Execute success and denied/failure paths and verify expected audit event presence or absence.
- Check actor, resource, tenant/scope, action, outcome, reason, timestamp, correlation ID, and safe metadata.
- Verify alternate paths such as worker/webhook/admin/bulk/retry when directly relevant.
- Confirm sensitive fields are redacted and the sink/query path works in the selected environment.

## Execute and decide

Fix the material action, expected event schema/presence policy, candidate revision and controlled sink. Establish a permitted action and relevant denied/failure control, then follow their correlation IDs from authoritative state/decision to stored and queried audit records.

Inspect completeness, actor/tenant identity, outcome and redaction separately from delivery/status logs. Replay a selected alternate or retry path when it can omit or duplicate required evidence; apply the repository's stated durability/order requirement rather than inventing one.

Return passed, failed or blocked with action/event identities and actual sink/query evidence. Feed failed emission/schema/durability into the authorized owner repair, repeat the same control/path after correction and finish Patch Checking. A mock sink does not establish an untested managed sink's durability.

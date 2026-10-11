# Network Integration Failure Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected external-call, webhook or stream behavior under its relevant failure and recovery conditions.

## Context

Identify selected outbound call, webhook or stream; provider/client versions, identity/signature contract, retry/deadline budget, completion guarantee and controlled test endpoint.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Inject DNS failure/change, certificate mismatch/rotation, connect reset, partial/slow/large response, and proxy timeout; verify bounded retries and error mapping.
- Replay duplicate/out-of-order/expired/invalidly signed webhooks and crash around receipt/side effect; verify idempotency, status, and re-drive.
- Open representative WebSocket/SSE clients, drop connections, create sequence gaps, refresh auth, and verify resume/full-resync behavior.
- Create slow consumers and saturated pools; verify bounded buffers/connections, backpressure/drop/close policy, fairness, and recovery.
- Terminate service during active requests/streams and verify admission stop, drain/close semantics, reconnect hints, and no orphan work.

## Verification

Compare response/status, durable effects, retry attempts, stream sequence/resync, resource bounds and recovery for the selected failure.

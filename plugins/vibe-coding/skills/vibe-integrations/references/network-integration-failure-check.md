# Network Integration Failure Check

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

## Execute and decide

Use a controlled endpoint/provider fixture and fixed identities. Establish normal completion, then inject the selected failure at a precise connect/read, receipt/effect, acknowledgement or stream-sequence boundary. Record actual attempts and total elapsed budget across the caller's layers.

For an ambiguous response, inspect the effect store independently of client error. For signatures, use valid and invalid provider-version vectors over the exact defined representation. For streams, compare resume/resync with the last accepted sequence and authoritative snapshot, including a slow/closed consumer when relevant.

Return passed, failed or blocked with the event order, expected/observed effect or resumed state, resource bounds and missing provider layers. Pass a failure to the authorized owner repair, repeat that case/control after correction and finish Patch Checking for changed code. Do not induce faults against unapproved live services.

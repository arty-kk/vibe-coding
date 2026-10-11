# Runtime Flow Map

## Operation

Map the requested area using current repository evidence.

## Goal

Trace selected requests, events or jobs from entry through state/effects to completion, failure and recovery.

Suggested saved map: `docs/runtime_flow_map.md`.

## Inspect

Routes/API handlers, services, transactions, queues, workers, workflow definitions, cron jobs, event producers/consumers, realtime/SSE/WebSocket code, object storage, cache, database writes, locks/leases, retry policies, idempotency keys, observability, deployment config, and tests.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: flow `FLOW-*`, step `STEP-*`, side effect `SIDE-*`, failure mode `FAIL-*`, recovery path `REC-*`, timing constraint `TIME-*`.
- Anchor every step to owner files/symbols. Separate direct evidence from inferred ordering or runtime behavior.

### Coverage

Cover entrypoint → validation/auth → state read/write → transaction/commit boundary → event/job/workflow → external side effect → notification/webhook → observability → failure/recovery. Include ordering, idempotency, retries, cancellation, deadlines, locks, duplicate handling, replay, cleanup, backpressure, and rollback/forward-fix notes when discoverable.

### Entry details

For each flow, capture trigger, actors, data/contracts, authoritative owners, sync/async steps, state transitions, side effects, retry/recovery semantics, tests/checks, observability, and residual unknowns.

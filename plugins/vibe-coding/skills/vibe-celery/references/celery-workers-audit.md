# Celery Workers Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit Celery task publication, acknowledgement, idempotency, retries, routing, concurrency, scheduling, and worker shutdown against the chosen broker/backend.

## Domain invariants

- The broker, transport, task serializer, routing/exchange/queue, result backend, and Celery version-specific behavior are explicit; guarantees are not assumed portable across transports.
- Task publication handles broker acknowledgement/ambiguity and uses stable task/operation identity when publication may retry.
- Acknowledgement mode, worker-lost behavior, visibility/redelivery behavior, and side-effect boundary collectively define an explicit duplicate/loss contract.
- Tasks are idempotent or deduplicated at the authoritative boundary; autoretry/manual retry preserves original intent and cannot compound partial effects.
- Soft/hard time limits, I/O timeouts, cancellation/termination, and heartbeat/progress behavior are coordinated rather than relying on hard kill for routine control.
- Prefetch multiplier, concurrency pool, worker count, routing, rate limits, and downstream capacity bound reserved and executing work.
- ETA/countdown/beat schedules account for worker memory, broker visibility, clock/timezone, overlap, singleton requirements, and deployment/shutdown.
- Result retention, task events, payload/log redaction, and cleanup match operational/debug needs without turning the backend into an unbounded datastore.

## Audit method

1. Map producer → broker route → reservation/prefetch → execution/side effect → ack/retry/failure → result/event/cleanup for the configured transport and pool.
2. Trace publish ambiguity, worker crash before/after side effect, acknowledgement, timeout, retry countdown, broker reconnect, and warm/cold shutdown.
3. Inspect effective Celery settings and task decorators together, including inherited defaults and transport-specific visibility/redelivery behavior.
4. Establish reserved/executing work from effective worker/QoS settings and observations. Inspect actual connection pools separately; task prefetch is not a connection-count formula. Compare both with task footprint and downstream limits.
5. Check beat/ETA uniqueness, overlap, routing, clock, and long-delay behavior for the actual deployment model.

## Handoff

Return the task/operation identity, effective settings, failing event order and expected durable effect. Identify which publication, acknowledgement, retry or lifecycle owner violates the selected contract. Feed that evidence into Improve Celery Workers; do not solve a duplicate-effect defect solely by suppressing task events or changing the result state.

# Celery Delivery & Shutdown Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected task’s publication, processing or shutdown guarantee under the configured acknowledgment and retry policy.

## Context

Identify Celery and broker/backend versions, transport, worker pool, task, acknowledgment/retry settings, operation identity and expected durable effect. Use controlled test workers and broker state.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Publish the same task twice and crash a worker before/after the side effect and acknowledgement; verify duplicate/loss contract.
- Force retryable and permanent failures; verify backoff/jitter, attempt context, terminal routing, and no retry storm.
- Exercise soft/hard timeout and worker termination; verify cleanup, acknowledgement/redelivery, and stale external work.
- Run warm/cold shutdown with active and reserved tasks; verify intake stop, drain/redelivery, and deployment readiness.
- Drive representative concurrency/prefetch and scheduled work; measure queue age, memory, connections, fairness, and downstream saturation.

## Verification

Compare task identity/status, durable effect count, retries, acknowledgments and unfinished work after recovery or shutdown.

## Execute and decide

Use a dedicated queue/worker and a controlled durable effect with an observable operation ID. Record effective task/decorator/worker settings and establish a successful completion control. Place synchronization points around the selected publication, effect commit and acknowledgement boundary; introduce only the failure needed for that guarantee.

After recovery or shutdown, inspect broker reservation/redelivery, task attempts, the authoritative effect record and outstanding work. Derive expected duplication/loss from the configured policy and application requirement instead of assuming every pool/transport behaves alike. For scheduled work, retain schedule/time identity and overlap evidence.

Return passed, failed or blocked with the event order and expected/observed effects. Pass a failure to its owning repair when authorized; rerun the failed sequence and control after correction. A completed implementation then receives Patch Checking.

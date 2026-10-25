# Improve Celery Workers

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected Celery delivery or worker-lifecycle behavior for the configured broker, backend and execution pool.

## Domain rules

- Keep acknowledgement and retry policy adjacent to task idempotency and transaction/outbox boundaries; do not change one in isolation.
- Use bounded exponential backoff/jitter and a terminal failure route; distinguish retryable dependency failure from permanent input failure.
- Set task and network/database timeouts coherently and use soft cancellation/cleanup before hard limits where the pool supports it.
- Tune concurrency/prefetch/routing from resource and downstream budgets; isolate long or scarce-resource tasks when necessary.
- Implement deployment shutdown that stops intake, allows bounded drain or deliberate redelivery, and exposes unfinished work.

## Validation

- Run Celery integration tests with the configured broker/backend and worker pool; eager mode alone is not delivery evidence.
- Exercise duplicate publication, crash/kill around ack and side effects, retry exhaustion, timeout, broker reconnect, scheduled overlap, and shutdown.
- Measure reserved/active/retried tasks, queue age, result retention, connection count, and downstream pressure.

First reproduce the selected failure with its actual transport and pool. Correct the task/producer/configuration boundary while preserving its effect idempotency, then rerun the same publication/commit/ack sequence. Feed effective settings, worker lifecycle and observed effects to Celery Delivery & Shutdown Check. If the check still fails, repair that boundary before another bounded run; accepted behavior proceeds to Patch Checking. Do not crash or drain shared production workers merely to validate code.

# Background Jobs Audit

## Goal

Audit background work: queues, workers, cron/scheduled jobs, webhooks, retries, idempotency, locks, concurrency, long-running tasks, cleanup, and observability. Keep only repository-visible issues with correctness, data, cost, reliability, or operational impact.

## Inspect

Queue/job definitions, worker entry points, schedulers/cron, webhook handlers, retry/backoff logic, idempotency keys, locks/transactions, batch/pagination loops, migrations, config/env, deployment/CI, logs/metrics/traces, dead-letter handling, admin tooling, tests, docs, and related API/UI state.

## Issue classes

- Correctness and idempotency: duplicate processing, unsafe retries, missing dedupe, out-of-order webhooks, non-atomic state transitions, partial writes, and inconsistent cleanup.
- Concurrency and scale: missing locks, race-prone counters/quotas, unbounded fan-out, memory/time limits, N+1 batch work, starvation, and thundering herd patterns.
- Failure handling: swallowed errors, infinite retries, no dead-letter/poison handling where architecture expects it, poor recovery path, and user-visible state stuck pending.
- Operational readiness: missing health/metrics/log context, unsafe secrets/config, deploy ordering issues, migrations required before workers, and lack of runbook for critical jobs.
- Data/privacy safety: cross-tenant processing, PII leakage in logs/payloads, retention cleanup gaps, and destructive job without guardrails.
- Regression resistance: missing tests/fixtures for retries/idempotency/lifecycle edges, stale docs, or workers not exercised by CI.

## Finding quality

- Include expected lifecycle behavior, failure/retry/idempotency contract, acceptance criteria, and validation direction.

## Handoff

Trace one logical operation from producer payload/version through reservation, authoritative effect, acknowledgement/status and retry/recovery. Retain its identity, tenant context, failing event order and expected durable result for Improve Background Jobs. Distinguish a scheduling defect from an engine-specific delivery guarantee; use that engine's workflow when it owns the failure.

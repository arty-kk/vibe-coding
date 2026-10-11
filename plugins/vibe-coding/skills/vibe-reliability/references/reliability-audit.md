# Reliability Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Find reachable reliability risks where production behavior can fail, degrade, retry incorrectly, or become undiagnosable under realistic dependency, network, process, deploy, or data-shape failures.

## Inspect

Request handlers, service boundaries, workers, schedulers, queues, webhooks, external provider clients, database transactions, migrations, storage, cache, config/env loading, health/readiness checks, logs/metrics, tests, CI, deploy docs, and runbooks.

## Focus areas

- Timeouts and cancellation: unbounded waits, missing request/job deadlines, leaked work after caller aborts, or mismatched provider timeouts.
- Retries and backoff: retry storms, retrying non-idempotent operations, missing jitter, hidden infinite loops, duplicate side effects, or provider rate-limit amplification.
- Degraded modes: dependency failure paths that crash critical surfaces, serve unsafe stale data, mask partial failure, or lose operator context.
- Startup/deploy: boot order assumptions, missing migrations/config validation, readiness checks that pass before dependencies are usable, unsafe shutdown/drain behavior.
- Data durability: acknowledged work before durable write, partial writes without recovery, lost events, skipped dead-letter/error states, or non-replayable jobs.
- Diagnostics: errors that are swallowed, logged without correlation, exposed to users, or impossible to trace from a symptom to the owner layer.

## Evidence rules

- Prefer fix at the defining sourcees over local guards, cosmetic rewrites, broad catch blocks, or hidden fallbacks.

## Work item quality

- If validation commands or harnesses are absent, specify observable checks that an execute run can add or perform.

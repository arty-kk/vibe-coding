# Performance Budget Audit

## Goal

Find concrete performance-budget risks and regression gaps in hot paths, especially where latency, throughput, memory, bundle size, database cost, provider cost, or job duration can grow without a guardrail.

## Inspect

Hot routes/pages/actions, rendering boundaries, data fetching, database queries/indexes, API fanout, caches, job loops, provider/model calls, assets, bundling, CI, existing benchmarks, logs/metrics, SLO docs, and release checks.

## Focus areas

- No explicit or testable budget for a repo-visible hot path where the code already implies a latency/size/cost expectation.
- Unbounded input/output cardinality: page sizes, loops, query result sets, job batches, exports, OCR/RAG/model chunks, assets, or in-memory aggregation.
- Waterfalls and fanout: serial awaits, N+1 provider/database calls, repeated expensive renders, cache misses, or avoidable round trips.
- Memory and artifact growth: retained buffers, full-file loads, large bundle chunks, uncompressed assets, or generated artifacts that scale with user data.
- Cost amplification: model/provider calls, retries, polling, cron overlap, background reprocessing, or analytics/events that scale faster than the user action.
- Regression visibility gaps: missing benchmark/test/CI/log metric where an existing harness could enforce the hot-path budget.

## Evidence rules

- Trace the evidenced budget to its workload and limiting resource owner; a missing arbitrary threshold alone is not a defect.

## Work item quality

- If validation commands or harnesses are absent, specify observable checks that an execute run can add or perform.

## Handoff

Retain the source of the limit/relative goal, workload distribution, candidate environment and resource/cost observation that exceeds or can violate it. Identify the input/concurrency dimension driving growth and pass that boundary to Improve Performance Budget. Keep unmeasured traffic, hardware and provider assumptions explicit instead of inventing an SLO to justify a change.

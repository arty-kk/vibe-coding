# Performance Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Find reachable performance problems that affect user experience, throughput, cost, reliability, or operational stability. Keep issues where current repository evidence shows a concrete hot path or high-risk path.

## Inspect

Routes/pages/components, handlers/services, database queries, migrations/indexes, caches, background jobs, queues, external calls, build/bundle config, assets, SSR/ISR/static generation, telemetry, tests/benchmarks, CI, and docs.

## Issue classes

- Database: N+1 queries, missing indexes for common filters/joins/sorts, unbounded scans, transaction scope, pagination/cursor inefficiency.
- API/server: blocking I/O, serial external calls, synchronous heavy work in request path, missing caching for stable expensive data, retry storms.
- Frontend: unnecessary client waterfalls, bundle bloat, heavy hydration, repeated expensive renders, large assets, missing lazy loading where repo patterns support it.
- Background jobs: duplicate work, unbounded queues, inefficient polling, non-idempotent retries, job amplification.
- Build/deploy/runtime: cold-start cost, memory spikes, cache invalidation drift, health checks that mask degraded service.
- Observability/testing: performance assumptions contradicted by code, missing guard tests/benchmarks for a critical path when a harness exists.

## Finding quality

- Include reachable surface, affected actors/consumers/states, expected behavior, acceptance criteria, and validation direction when discoverable.
- Explain impact from repo-visible reachability and mark inferred traffic/scale assumptions clearly.
- Prefer fix at the defining sourcees: query/index/pagination/caching/job structure/source-of-truth, not cosmetic local tweaks.
- If validation commands/benchmarks are absent, specify observable checks that an execute run can add or perform.

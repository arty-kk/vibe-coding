# Consistency Invariants Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Find reachable consistency defects where one business rule, state transition, permission, quota, schema, cache, generated type, or external contract can drift across layers or over time.

## Inspect

Domain models, validators, permissions, plan/quota rules, API schemas, database constraints, migrations, generated clients/types, UI state gates, caches, background jobs, integrations, tests, fixtures, docs, and analytics/event contracts.

## Focus areas

- Duplicate sources of truth for rules, states, enums, permissions, quotas, feature flags, copy, cache keys, external payloads, or validation.
- State-machine gaps: invalid transitions, impossible states representable in storage/types/UI, missing terminal states, or ambiguous rollback/compensation behavior.
- Read/write drift: UI accepts states the API rejects, API accepts states storage cannot enforce, generated clients differ from handlers, or docs disagree with runtime contracts.
- Cache/search/index drift: invalidation gaps, stale denormalized fields, async projection races, missing repair/rebuild path, or inconsistent pagination/sorting semantics.
- Tenant/workspace/project isolation drift between route params, auth context, filters, policies, analytics, and background jobs.
- Test/doc drift where guard tests, fixtures, examples, or README instructions encode a contract different from the implementation owner.

## Evidence rules

- Prefer fix at the defining sourcees over local guards, cosmetic rewrites, broad catch blocks, or hidden fallbacks.

## Work item quality

- If validation commands or harnesses are absent, specify observable checks that an execute run can add or perform.

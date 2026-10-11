# Improve Product Analytics

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected event or metric from its producer through the relevant transformation and consumer.

## Domain rules

- Fix semantic ownership before adjusting dashboards; use stable event IDs or dedupe keys where delivery repeats.
- Emit at the authoritative state transition and keep client events for interaction semantics only.
- Version incompatible event/metric changes and migrate downstream models/dashboards explicitly.
- Synchronize consent/privacy, schemas, transforms, tests, dashboards, docs, and data-quality alerts.

## Validation

- Run event schema/unit/integration/data-quality/metric tests and inspect representative raw-to-dashboard rows.
- Exercise duplicate, late, missing identity, timezone/window, consent, and backfill cases.
- List warehouse freshness, production volume, and business sign-off gates separately.

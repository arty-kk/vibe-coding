# Improve Product Analytics

## Goal

Correct the selected event or metric from its producer through the relevant transformation and consumer.

## Domain rules

- Fix semantic ownership before adjusting dashboards; use stable event IDs or dedupe keys where delivery repeats.
- Emit from the owner of the claimed observation: client interaction/rendered states at the client, durable server effects at their authoritative transition. Do not label an attempted action as a completed effect.
- Version incompatible event/metric changes and migrate downstream models/dashboards explicitly.
- Synchronize consent/privacy, schemas, transforms, tests, dashboards, docs, and data-quality alerts.

## Validation

- Run event schema/unit/integration/data-quality/metric tests and inspect representative raw-to-dashboard rows.
- Exercise duplicate, late, missing identity, timezone/window, consent, and backfill cases.
- List warehouse freshness, production volume, and business sign-off gates separately.

Fix the producer/schema/transform owner using a representative action and expected event grain/identity, then inspect its raw records and final consumer value under the same window. Verify the affected duplicate, failure, consent or late-data case without silently filtering it away. Return remaining semantic drift to that owner and finish the instrumentation patch through Patch Checking.

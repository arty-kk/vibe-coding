# Product Metrics Events Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map selected product metrics and events to their producers, semantics, privacy boundary and downstream consumers.

Suggested saved map: `docs/product_metrics_events_map.md`.

## Inspect

Analytics SDK setup, event emitters, tracking helpers, server-side events, data warehouse/ClickHouse/db tables, experiment flags, dashboard configs, docs, tests, privacy/consent gates, retention configs, generated clients, and product surfaces that trigger events.

## Map rules

- Suggested IDs for new entries: metric `MET-*`, event `EVT-*`, funnel `FUN-*`, experiment `EXP-*`, property `PROP-*`, dashboard `DASH-*`.
- Anchor events and metrics to implementation evidence, not only dashboard/docs names.
- Mark privacy, consent, PII, sampling, identity, deduplication, timezone, and environment boundaries when discoverable.
- Do not infer business targets or KPI thresholds unless repository docs/configs provide them.

## Coverage

Cover core product metrics, event taxonomy, event producers, payload properties, identity/session/tenant keys, consent/privacy gates, experiments, dashboards or queries, tests, known missing events, duplicated/drifting names, and downstream consumers.

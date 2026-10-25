# Observability Stack Audit

## Goal and scope

Audit metrics, logs, dashboards, alerts, and correlation as one signal contract with bounded cardinality, cost, tenancy, and operator actionability.

## Domain invariants

- Metric names, type, units, label meanings, reset behavior, scrape ownership, and aggregation match the measured phenomenon; label domains and their product have an explicit cardinality budget; unbounded user-generated values and secrets are excluded.
- Recording rules preserve label semantics and reduce expensive repeated queries; alerts target user/system symptoms with explicit duration, severity, ownership, and actionable annotations.
- Grafana dashboards and alerts have a known maintenance source, bind the intended datasource/tenant, use valid variables and show units, nulls, rates and percentiles honestly. Inspect existing provisioning when the repository owns it.
- VictoriaLogs ingestion parses timestamps/streams/fields consistently, bounds stream cardinality and payload size, and applies retention/tenant access at the authoritative boundary.
- Log queries use selective filters and indexed/stream fields where supported; dashboards and alerts cannot trigger unbounded full-retention scans under normal use.
- Correlation identifiers link request/run/message traces without making logs or labels a primary datastore and without exposing credentials, personal data, or full untrusted payloads.
- Signal freshness, loss, duplicate ingestion, out-of-order data, rule evaluation delay, and no-data behavior are visible rather than silently interpreted as health.
- Telemetry volume, query concurrency, retention, dashboard refresh, and alert fan-out have explicit cost/capacity ownership.

## Audit method

1. Trace one user/system outcome through instrumentation, scrape/ingest, storage, recording/query, dashboard, alert, and runbook/owner response.
2. Inspect metric type/unit/labels and estimate cardinality from actual label domains, targets, replicas, and retention rather than a single local sample.
3. Evaluate rule expressions for aggregation, counter reset, histogram buckets, absent/no-data, evaluation window, flap, and multi-tenant labels.
4. Render/provision Grafana resources and verify datasource UID, variables, units, links, permissions, and alert ownership.
5. Inspect VictoriaLogs stream/field extraction, tenant routing, retention, query shape, ingestion failures, and backpressure/cost evidence.

## Handoff

Retain the event/metric identity, type/units/label meaning, datasource/tenant and observation window. Show the first difference between emitted facts and the queried/operator-visible result, including reset or missing-data behavior when relevant. Pass that violated signal contract into Improve Observability Stack; an attractive graph or fewer alerts cannot establish correct measurement.

# Improve Observability Stack

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected signal from instrumentation through storage, query, dashboard or alert interpretation.

## Domain rules

- Change instrumentation and consuming rules/dashboards/alerts together when a metric or log contract changes.
- Prefer bounded stable dimensions and pre-aggregation over dropping useful semantics after cardinality has already exploded.
- Make alert states and operator action explicit; add rate limits/grouping/silences without masking persistent symptoms.
- Provision dashboards/alerts declaratively where the repository already owns them and preserve stable UIDs/references.
- Redact at collection boundaries and configure tenant/retention/query limits at the authoritative storage or gateway layer.

## Validation

- Run repository rule tests, metric linting, dashboard/provisioning validation, and representative VictoriaLogs ingest/query fixtures where available.
- Measure series/stream growth and query cost under representative dimensions; report estimates separately from observed production data.
- Trigger and recover a representative alert, including no-data and dependency-loss behavior, and verify owner/runbook annotations.

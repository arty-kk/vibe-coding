# Observability Semantics & Cost Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify that the selected telemetry path represents the intended signal within its identity, freshness and cardinality limits.

## Context

Identify selected metric/log/alert/dashboard, actual engines/versions, units and labels, expected signal meaning, cardinality budget and observation window.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Generate representative metrics/logs across tenants, status classes, replicas, and error paths; measure series/stream growth and ingestion rejection.
- Run recording/alert rules through normal, reset, missing, stale, burst, and recovery windows.
- Provision dashboards/alerts in a disposable environment and validate datasource, variables, units, permissions, links, and query errors.
- Exercise VictoriaLogs ingestion backpressure, malformed timestamps, tenant mismatch, retention boundary, and bounded query concurrency.
- Compare end-to-end signal latency and correlation from emitted event to operator-visible dashboard/alert.

## Verification

Compare emitted and queried values, reset/no-data behavior, alert transitions, tenant visibility and measured series/stream or query growth.

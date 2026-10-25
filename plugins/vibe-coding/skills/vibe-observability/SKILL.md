---
name: vibe-observability
description: "Audit, repair or verify metric/log semantics, dashboards, alerts, correlation and telemetry resource costs."
---

# Metrics, logs & alerts

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Observability Stack Audit → Improve Observability Stack → Observability Semantics & Cost Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry the measured phenomenon, emitter, units/type/labels, tenant/datasource, time window and expected operator interpretation between prompts. A known rule/instrumentation defect starts at correction; verification-only work uses the check without modifying live alerts.

Trace a controlled product event through ingestion, query/rule and visible dashboard/alert state. Correct the first semantic, freshness, cardinality or tenant boundary rather than merely changing a graph label or silencing the symptom.

Return failed values, reset/no-data transitions or resource growth to their owning instrumentation/query/rule, rerun affected cases and finish patch review. Distinguish observed dimensions from cardinality estimates and a test alert transition from actual paging/delivery. Real notifications or live provisioning require the corresponding authorization.

## Recipes

| Recipe | Operation |
|---|---|
| [Observability Semantics & Cost Check](references/observability-semantics-cost-check.md) | check |
| [Observability Stack Audit](references/observability-stack-audit.md) | audit |
| [Improve Observability Stack](references/observability-stack-polish.md) | implement |

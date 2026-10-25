---
name: vibe-clickhouse
description: "Audit, repair or verify ClickHouse ingestion, table/merge semantics and query resource use."
---

# ClickHouse

Apply [the working contract](../../references/workflow.md) once.

## Workflow

ClickHouse Audit → Improve ClickHouse → ClickHouse Ingestion & Query Load Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Choose the concrete insert/result/budget promise and carry table DDL, engine, topology, source/batch identity and query shape through the chain. A known DDL/query defect starts at correction; a check-only request executes the verification method without changing tables.

Separate physical rows and merge state from the logical result the consumer requires. Diagnose insert/checkpoint/dedup, eventual table semantics, query pruning or workload admission at the owning boundary before changing keys or adding query modifiers.

Reproduce with representative identity, late/duplicate data and skew where relevant. A failed count/result or resource bound returns to its source/DDL/query/settings owner, then the same fixture/workload is rerun. Complete the patch review after acceptance; unavailable production topology or capacity remains a gate rather than a result inferred from a tiny local dataset.

## Recipes

| Recipe | Operation |
|---|---|
| [ClickHouse Audit](references/clickhouse-audit.md) | audit |
| [ClickHouse Ingestion & Query Load Check](references/clickhouse-ingestion-query-load-check.md) | check |
| [Improve ClickHouse](references/clickhouse-polish.md) | implement |

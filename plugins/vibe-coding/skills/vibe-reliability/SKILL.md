---
name: vibe-reliability
description: "Audit, repair or verify a selected consistency, concurrency, failure-handling or measured resource-budget problem."
---

# Reliability & performance

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

## Recipes

| Recipe | Operation |
|---|---|
| [Transactional Delivery Check](references/transactional-delivery-check.md) | check |
| [Consistency Invariants Audit](references/consistency-invariants-audit.md) | audit |
| [Improve Consistency Invariants](references/consistency-invariants-polish.md) | implement |
| [Idempotency & Concurrency Audit](references/idempotency-concurrency-audit.md) | audit |
| [Improve Idempotency & Concurrency](references/idempotency-concurrency-polish.md) | implement |
| [Performance Audit](references/performance-audit.md) | audit |
| [Performance Budget Audit](references/performance-budget-audit.md) | audit |
| [Improve Performance Budget](references/performance-budget-polish.md) | implement |
| [Improve Performance](references/performance-polish.md) | implement |
| [Reliability Audit](references/reliability-audit.md) | audit |
| [Improve Reliability](references/reliability-polish.md) | implement |


Use Transactional Delivery Check for the database → event → consumer effect boundary. For a requested repair, use Consistency Invariants Polish with the same crash-window checks.

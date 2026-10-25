---
name: vibe-reliability
description: "Audit, repair or verify a selected consistency, concurrency, failure-handling or measured resource-budget problem."
---

# Reliability & performance

Apply [the working contract](../../references/workflow.md) once. Select the violated guarantee or measured limiting resource before choosing a mechanism.

## Workflows

- **Failure handling:** Reliability Audit → Improve Reliability → reproduce the selected failure and normal control → [Patch Checking](../vibe-review/references/patch-checking.md).
- **Cross-layer consistency:** Consistency Invariants Audit → Improve Consistency Invariants → convergence/repair cases; use Transactional Delivery Check for the database → event → effect boundary → Patch Checking.
- **Duplicate/concurrent effects:** Idempotency & Concurrency Audit → Improve Idempotency & Concurrency → controlled conflicting/crash/stale-owner interleavings → Patch Checking.
- **Measured bottleneck:** Performance Audit → Improve Performance → equivalent before/after workload and correctness checks → Patch Checking.
- **A defined resource/cost limit:** Performance Budget Audit → Improve Performance Budget → the same workload against its evidenced budget and failure semantics → Patch Checking.

Start at correction for a known target or at Transactional Delivery Check for verification-only work. Carry operation identity, expected invariant, first failing boundary and actual interleaving; for performance also carry workload shape, environment, measured distribution/resource and the accepted limit or relative goal.

Failed effect, convergence or budget evidence returns to its authoritative owner, followed by the same control/case and final patch review. Do not hide loss by disabling retries, claim distributed guarantees from a local flag or invent production improvements from a small sample. Required external timing/topology evidence stays explicit.

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

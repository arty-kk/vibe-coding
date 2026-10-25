---
name: vibe-celery
description: "Audit, repair or verify Celery delivery, retries and worker lifecycle using the actual broker, backend and pool."
---

# Celery

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Celery Workers Audit → Improve Celery Workers → Celery Delivery & Shutdown Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Start at the repair for a known task/configuration defect or at the check for verification-only work. Carry the exact task, Celery/broker/backend versions, pool, effective acknowledgement/retry settings and durable operation identity between steps.

Locate the failure in publication, reservation, execution, side-effect commit, acknowledgement or recovery before changing concurrency or retry policy. Reproduce the selected crash/retry/shutdown boundary in an isolated test worker and inspect durable effects alongside task/broker state. Eager execution cannot validate broker delivery or process shutdown.

A failed guarantee returns to the owning task/producer/configuration correction, then the same controlled sequence is rerun. Finish after the selected delivery/lifecycle contract and final patch review pass. An unavailable broker/pool or unsafe crash environment remains a gate; do not infer its behavior from result-backend success alone.

## Recipes

| Recipe | Operation |
|---|---|
| [Celery Delivery & Shutdown Check](references/celery-delivery-shutdown-check.md) | check |
| [Celery Workers Audit](references/celery-workers-audit.md) | audit |
| [Improve Celery Workers](references/celery-workers-polish.md) | implement |

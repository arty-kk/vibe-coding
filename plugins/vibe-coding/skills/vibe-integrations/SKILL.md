---
name: vibe-integrations
description: "Audit, repair or verify outbound clients, proxies/TLS, webhooks and server stream lifecycle under selected failure conditions."
---

# Integrations & networking

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Backend Integrations Audit → Improve Backend Integrations → Network Integration Failure Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Choose an outbound operation, webhook or server stream and carry its identity, signed representation, deadline/retry budget, completion boundary and recovery promise between prompts. A known defect starts at correction; a failure-check-only request does not edit or contact real recipients.

Trace the first mismatch across client/proxy/provider, durable receipt/effect or stream sequence rather than changing every retry setting. Replay a controlled normal path and the selected reset, ambiguity, duplicate or gap. Caller timeout/cancellation does not prove a remote effect was undone.

Return failed effect, deadline, trust or resume evidence to its owner, rerun the affected failure/control and finish patch review. Keep provider, certificate/proxy and production-load behavior not exercised explicit. Client query-state reconciliation belongs to Realtime; this workflow owns the server/network boundary.

## Recipes

| Recipe | Operation |
|---|---|
| [Backend Integrations Audit](references/backend-integrations-audit.md) | audit |
| [Improve Backend Integrations](references/backend-integrations-polish.md) | implement |
| [Network Integration Failure Check](references/network-integration-failure-check.md) | check |

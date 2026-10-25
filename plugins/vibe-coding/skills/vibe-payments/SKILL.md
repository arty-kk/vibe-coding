---
name: vibe-payments
description: "Audit, repair or verify payment-provider events, billing transitions and reconciliation using safe fixtures or sandbox."
---

# Payments

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Payments Provider Audit → Improve Payments Provider → Payments Webhook & Reconciliation Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry provider/API version, test/live mode, operation/customer/subscription/event identities and the expected local billing/entitlement transition between prompts. A known transition defect starts at correction; verification-only work uses safe fixtures or sandbox and does not change pricing or perform real financial actions.

Trace the selected request/event through authenticated ingestion, local commit, reconciliation, entitlement and visible status. Correct the authoritative transition/operation owner, then replay duplicate, delayed or ambiguous sequences with a normal control.

Return an inconsistent balance/state/effect to the same owner, rerun affected checks and finish patch review. Client checkout success and a provider receipt are not automatically authoritative local entitlement. Keep unavailable provider/tax/production evidence explicit; code repair is not authorization to charge, refund or transfer money.

## Recipes

| Recipe | Operation |
|---|---|
| [Payments Provider Audit](references/payments-provider-audit.md) | audit |
| [Improve Payments Provider](references/payments-provider-polish.md) | implement |
| [Payments Webhook & Reconciliation Check](references/payments-webhook-reconciliation-check.md) | check |


For a local plan/role/entitlement policy without a provider-runtime defect, use [Domain](../vibe-domain/SKILL.md). Follow the actual failing owner when both boundaries participate.

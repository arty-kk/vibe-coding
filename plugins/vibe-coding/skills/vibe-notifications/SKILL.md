---
name: vibe-notifications
description: "Audit, repair or verify notification eligibility, provider delivery, retries and status. Template wording belongs to vibe-content."
---

# Notification delivery

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Notification Delivery Audit → Improve Notification Delivery → Notification Failure & Idempotency Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry notification class, event/recipient/channel identity, eligibility policy, provider operation identity and expected local status through the chain. A known delivery defect starts at correction; verification-only work uses sandbox/controlled fixtures without edits.

Trace eligibility → rendered payload → durable enqueue/receipt → provider effect → status/recovery. Distinguish queued, provider-accepted, delivered and read when those states exist. A local success row cannot prove delivery, and an ambiguous provider timeout cannot be treated as definitely unsent.

Correct the first violating trigger, consent, queue/adapter or status owner and replay the same duplicate/failure/control sequence. Repeat affected checks before patch review. No workflow step authorizes contacting real recipients merely because notification code changed; missing provider evidence remains a gate.

## Recipes

| Recipe | Operation |
|---|---|
| [Notification Delivery Audit](references/notification-delivery-audit.md) | audit |
| [Improve Notification Delivery](references/notification-delivery-polish.md) | implement |
| [Notification Failure & Idempotency Check](references/notification-failure-idempotency-check.md) | check |

Eligibility, queue/provider delivery and status stay here; use [Content](../vibe-content/SKILL.md) for template wording and localization.

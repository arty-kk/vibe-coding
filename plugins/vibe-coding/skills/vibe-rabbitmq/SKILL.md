---
name: vibe-rabbitmq
description: "Audit, repair or verify RabbitMQ routing, confirms, acknowledgments, redelivery and connection recovery."
---

# RabbitMQ

Apply [the working contract](../../references/workflow.md) once.

## Workflow

RabbitMQ Audit → Improve RabbitMQ → RabbitMQ Redelivery & Recovery Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry effective topology/policies, queue type, confirm/return and consumer acknowledgement settings, message/operation identity and expected durable effect into correction. A known routing/lifecycle defect starts at implementation; a check-only request does not alter live queues.

Trace publish → route/return/confirm → delivery → effect → ack/requeue and recovery. Correct the first violating topology, publisher, consumer/effect or channel owner, then replay the same ambiguity/redelivery sequence with a healthy routed control.

Return failed routing, duplicate effect, unbounded requeue or lost subscription evidence to that owner, repeat the affected check and finish patch review. Broker confirmation is not consumer completion. Preserve required topology migration/drain gates and do not infer managed-cluster durability from a local mocked publisher.

## Recipes

| Recipe | Operation |
|---|---|
| [RabbitMQ Audit](references/rabbitmq-audit.md) | audit |
| [Improve RabbitMQ](references/rabbitmq-polish.md) | implement |
| [RabbitMQ Redelivery & Recovery Check](references/rabbitmq-redelivery-recovery-check.md) | check |

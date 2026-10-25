---
name: vibe-kafka
description: "Audit, repair or verify Kafka/Redpanda delivery, ordering, offsets, schema compatibility, rebalance and replay."
---

# Kafka & Redpanda

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Kafka Redpanda Audit → Improve Kafka Redpanda → Kafka Redpanda Rebalance & Failure Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry the broker/client versions, topic/partition/key, schema, consumer group/offset policy and business operation identity into the next prompt. Start at correction for a known contract defect or at the check for verification-only work.

Locate the actual send/ack, processing/effect, offset/transaction or rebalance boundary that violates the required loss/duplicate/order guarantee. Correct that owner and replay the same record/interleaving with a normal control. A shared message key does not make distinct events duplicates, and broker transactions do not automatically cover external effects.

Failed ordering, ownership or effect evidence returns to the same producer/consumer/state owner, followed by the relevant replay and final patch review. Preserve the supported broker/version and schema window; unavailable cluster/portability evidence stays a gate.

## Recipes

| Recipe | Operation |
|---|---|
| [Kafka Redpanda Audit](references/kafka-redpanda-audit.md) | audit |
| [Improve Kafka Redpanda](references/kafka-redpanda-polish.md) | implement |
| [Kafka Redpanda Rebalance & Failure Check](references/kafka-redpanda-rebalance-failure-check.md) | check |

# Kafka Redpanda Rebalance & Failure Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected record delivery, ordering and processing guarantee across required crash or rebalance windows.

## Context

Identify broker/client versions, topic/key/partition settings, producer acknowledgments, consumer group/commit policy, record identity and required delivery/ordering guarantee.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Produce duplicate keys and retry after ambiguous acknowledgement; verify ordering and deduplication contract.
- Crash consumers before/after side effect and before/after offset commit; verify duplicate/loss behavior and replayability.
- Trigger a group rebalance during long processing and verify ownership, pause/resume, commit, and shutdown semantics.
- Inject incompatible/poison records and verify bounded retry, quarantine metadata, alerting, and controlled replay.
- Test broker/partition loss or throttling in a disposable cluster and measure lag, backpressure, recovery, and durability settings.

## Verification

Compare records, offsets, partition order, business effect count and recovery lag at the actual selected acknowledgment/commit boundary.

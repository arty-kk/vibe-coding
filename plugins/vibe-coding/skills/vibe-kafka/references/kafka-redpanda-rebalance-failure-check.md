# Kafka Redpanda Rebalance & Failure Check

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

## Execute and decide

Use a dedicated topic/group and deterministic records carrying both ordering keys and operation IDs. Establish normal send/process/commit behavior, then synchronize one selected ack, side-effect or offset boundary before interrupting or rebalancing the consumer.

After recovery, inspect the actual record/offset sequence, assignment ownership and authoritative business effect, not only group lag or successful poll calls. Distinguish valid distinct records sharing a key from retries of the same operation. For transactional flows, inspect the supported reader isolation and the actual transaction's scope.

Return passed, failed or blocked for the stated guarantee with record identities, event order and effects. Pass a failed case into the authorized repair, repeat it with its control and finish Patch Checking for code/config changes. Cluster faults and replay into effectful consumers require an appropriate test environment.

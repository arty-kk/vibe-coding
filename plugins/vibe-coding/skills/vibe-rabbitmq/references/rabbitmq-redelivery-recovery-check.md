# RabbitMQ Redelivery & Recovery Check

## Goal

Verify the selected publish or processing guarantee through routing, acknowledgment uncertainty and redelivery.

## Context

Identify broker/client version, exchange/queue/bindings, queue type and policies, confirm/return and acknowledgment settings, message identity and effect guarantee.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Publish routable and unroutable messages with confirms; drop the connection around acknowledgement and verify retry/duplicate contract.
- Crash a consumer before and after the side effect/ack boundary; verify redelivery safety and bounded in-flight work.
- Inject poison messages and prove delivery-limit/TTL/DLX behavior, cycle prevention, observability, and controlled re-drive.
- Restart broker/client connections and verify topology, consumers, channel ownership, and no duplicate subscription.
- Drive representative backlog and broker flow control; measure queue age, unacked work, memory/disk alarms, fairness, and recovery.

## Verification

Compare routing/returns/confirms, durable effects, acknowledgments, redelivery and topology recovery; distinguish broker receipt from processing completion.

## Execute and decide

Use dedicated topology/consumers and deterministic messages with business operation IDs. Establish routed completion and the configured unroutable control. Synchronize the selected confirm, effect or consumer-ack boundary before connection loss, worker interruption or controlled re-drive.

Observe returns/confirms, queue/unacked state, authoritative effects, attempts and recovered topology/subscriptions independently. A queue draining because messages were lost is not success. For flow-control/resource checks, record the actual QoS scope, concurrency, footprint and observation window.

Return passed, failed or blocked with identities, event order, effects and missing broker layers. Pass failures to the authorized owner repair, replay their control/sequence after correction and finish Patch Checking for source changes. Broker alarms, restarts and topology migration require a suitable test environment.

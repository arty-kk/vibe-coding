# Improve RabbitMQ

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected RabbitMQ publish or consumption behavior across routing, confirms, effects and acknowledgments.

## Domain rules

- Make topology changes compatible and staged; avoid changing immutable queue arguments in place without migration/drain strategy.
- Use confirms plus unroutable-return handling for required delivery assurance and keep publish retry idempotent.
- Place ack/nack after the real processing boundary, bound requeue loops, and route terminal failures with complete diagnostic context.
- Tune prefetch from work cost/downstream capacity rather than using concurrency as an unbounded throughput lever.
- Own connection/channel lifecycle explicitly and re-declare/re-subscribe only through the established recovery mechanism.

## Validation

- Run topology declaration and integration tests against a supported RabbitMQ version and policy profile.
- Exercise unroutable publish, confirm ambiguity, consumer crash, repeated redelivery, connection/channel recovery, blocked broker, and graceful shutdown.
- Verify queue depth/age, unacked count, duplicates, ordering scope, DLQ metadata, and recovery without destructive production testing.

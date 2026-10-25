# Backend Bug Probe

## Scope

Inspect one server-side operation: request handler, domain rule, data transaction, permission check, worker or outbound adapter. Reproduce the supplied failure or trace a concrete input through the relevant state and effect.

## Procedure

1. Establish accepted input, expected response/state/effect and the authoritative rule. Inspect validation, access scope, serialization and the direct consumer.
2. Trace the relevant retry, concurrent request, partial write or cancellation. Observe stored state and external-effect identity, not only the returned status.
3. If authorized, repair the rule at the handler, service, policy, transaction or adapter that defines it. Synchronize directly affected callers and generated contracts.
4. Preserve supported wire/schema behavior. For an already-applied migration, follow the repository’s forward-migration and rollback/forward-fix policy rather than silently rewriting history.

## Verification

Run the closest native owner/consumer check or a controlled request/job reproduction. Include a valid control beside rejection or failure cases. Qualify unavailable databases, queues and providers. Apply the selection/history and result rules in the parent skill.

Carry the principal/input, initial stored state, expected effect identity and observed final state into patch review. If a response is correct but the persisted effect is still wrong or duplicated, return to the same owning transaction/adapter; do not mark the probe fixed.

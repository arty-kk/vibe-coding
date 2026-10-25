# Temporal Workflows Audit

## Goal and scope

Audit Temporal workflow history compatibility, determinism, activities, retries, signals/updates, versioning, deployment, and long-run lifecycle.

## Domain invariants

- Workflow code is deterministic for a recorded history: nondeterministic I/O, time, randomness, threading, and side effects live behind Temporal APIs or Activities.
- Every Activity has appropriate schedule/start/close timeouts, cancellation behavior, retry classification, and heartbeat details for long-running or resumable work.
- Activity side effects use an identity stable for the intended operation. Run/activity identity can cover retries within a run; a business operation that survives reset or Continue-As-New needs deduplication across those boundaries too.
- Compensation/saga state is durable, ordered, retryable, and aware of partially completed forward and compensating actions.
- Signals and Updates validate input, serialize state transitions safely, handle handler concurrency/initialization, and expose accepted/completed semantics accurately; Queries do not mutate state.
- Long-lived workflows bound event history and state via Continue-As-New at a safe boundary while preserving pending intent and signal/update behavior.
- Workflow code changes use supported patching/versioning or worker-versioning strategy and are replay-tested against representative production histories before incompatible deployment.
- Task queues, worker build/deployment identity, polling capacity, sticky/cache behavior, and rollback path preserve compatibility during mixed-version rollout.

## Audit method

1. Map workflow types, task queues, histories, commands, Activities, child workflows, timers, signals/updates/queries, search attributes, and worker deployment/version ownership.
2. Replay representative old histories against the candidate code and classify nondeterminism, removed commands, changed ordering, and serialization incompatibility.
3. Trace Activity timeout/retry/heartbeat/cancel and crash windows, including ambiguous external success and compensation behavior.
4. Inspect handler concurrency, workflow initialization, Continue-As-New, history growth, and pending message semantics for long-running workflows.
5. Verify rollout/rollback compatibility across old/new workers and task routing rather than assuming source rollback can process histories created by new code.

## Evidence and handoff

For each finding, connect the history event or message to the source command, durable state and observed external effect. Separate replay incompatibility, payload decoding failure, Activity retry and handler interleaving: each has a different repair owner. Include one compatible control and the smallest history or timing sequence that distinguishes it from the failing case.

Hand the repair step the affected versions, the required old-history behavior, the unsafe operation and a concrete replay or integration regression. Do not replay production effects or redirect workers as part of a read-only audit. If histories cannot be obtained, identify the compatibility risk without presenting a source-only inspection as a successful replay.

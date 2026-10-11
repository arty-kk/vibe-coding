# Serverless Runtime Audit

## Operation

Inspect the selected serverless or edge invocation boundary without product edits. Read [serverless runtime boundaries](../../../references/serverless-runtime.md). Apply the provider, trigger and runtime evidenced by the repository; do not assume Lambda, Workers and Durable Objects share a lifetime model.

## Required input

The selected handler, provider/runtime and compatibility configuration, trigger, success/acknowledgment promise, authoritative effect and retry owner. Identify the concrete invocation state and permitted local/provider environment.

## Domain invariants

- Success or acknowledgment is emitted only when work required by the business contract has reached its promised durability boundary.
- Deferred work uses the actual provider lifetime mechanism; best-effort continuation is not represented as durable delivery.
- Invocation-specific identity and mutable user state cannot survive into another invocation; reusable infrastructure clients remain separately owned.
- Duplicate, concurrent and partial-batch delivery preserve stable operation identity and cannot repeat a non-repeatable committed effect.
- Runtime API use, resource cleanup, fan-out and downstream admission respect the deployed configuration and supported provider semantics.

## Goal and scope

Determine whether invocation completion, acknowledgment and durable effects preserve the promised business behavior under reuse, retry, cancellation and resource limits. Follow one handler and its direct trigger, bindings and downstream operations. Keep general infrastructure provisioning and framework rendering with their owners unless they directly determine invocation correctness.

## Inspect

- Provider/deployment configuration, runtime/version, compatibility date, trigger/source mapping, preview/production bindings and declared limits.
- Handler inputs, trusted identity, response/acknowledgment, awaited and deferred work, durable queue publication and downstream clients.
- Module-level mutable state, reusable clients/connections, temporary files, caches and per-invocation credentials/context.
- Event identities, batch results, retry ownership, visibility/lease duration, dead-letter handling, concurrency and admission control.
- Local emulator/provider tests, logs/metrics and documented product success guarantees.

## Audit method

1. Trace trigger → identity/input → handler → response or acknowledgment → required/deferred work → authoritative durable effect.
2. Classify work required before success versus intentionally deferred work. Establish what the runtime actually keeps alive and whether deferral meets the business durability promise.
3. Inspect two invocations in a reused environment with different identities or inputs. Separate safe reusable SDK clients from unsafe retained user state and non-authoritative in-memory data.
4. Follow duplicates, concurrent delivery and partial batches through stable operation identity to the final effect. Check the position of acknowledgment relative to durable commit.
5. Examine fan-out and downstream capacity under the configured concurrency and limits. A provider's scaling capability does not prove its database or API can absorb that load.
6. Reproduce the selected boundary with controlled pending/rejected operations, repeated events or a provider harness. State which runtime behavior the local fixture cannot establish.

## Issue classes and priority

Prioritize reported success with lost required work, cross-invocation identity/data leakage and duplicated non-repeatable effects. Next consider incorrect partial-batch retries, timeout/retry amplification, incompatible runtime APIs, leaked connections and configuration drift causing reachable failures. Do not label every global variable or unawaited promise a defect without its lifetime and product contract.

## Evidence requirements

Cite handler/configuration `path:line`, trigger/runtime, affected event or user state, expected guarantee, observed result and durable-state evidence. Give one repair direction at the lifetime, identity, delivery or admission owner and a meaningful regression route. Distinguish local ordering evidence from production scheduling, quotas, disconnect and provider durability guarantees.

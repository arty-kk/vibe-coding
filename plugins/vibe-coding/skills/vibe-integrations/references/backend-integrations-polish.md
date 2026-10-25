# Improve Backend Integrations

## Goal

Correct the selected external-call, webhook or stream contract across authentication, retry, completion and recovery.

## Domain rules

- Use one end-to-end deadline/retry budget and propagate cancellation; make non-idempotent retry safe with operation keys or disable it.
- Bound pools, per-host concurrency, bodies, queues, stream buffers, and slow consumers before adding circuit breakers or concurrency.
- Preserve the exact provider-defined signed input, use its supported verification path before trusted effects, store stable event identity and separate receipt from asynchronous processing deliberately.
- Implement WebSocket/SSE resume with monotonic event/version IDs or full resync; never assume reconnect fills an unobserved gap.
- Stage certificate/credential/proxy changes with overlap and health evidence; preserve least privilege and trusted-hop boundaries.

## Validation

- Run contract/integration tests against provider fixtures or a controlled test endpoint, including exact signature/raw-body vectors.
- Exercise DNS/TLS/connect/read resets, slow/large responses, retry ambiguity, pool saturation, duplicate/out-of-order webhooks, stream gaps, slow consumers, and shutdown.
- Measure attempts, end-to-end latency, pool/connection/buffer usage, backlog, duplicate effects, and recovery.

Correct the owning deadline/retry, signature/receipt, trust or stream-lifecycle boundary using a fixed operation/vector/sequence. Derive signing and replay behavior from the implemented provider version rather than a generic HMAC template. Replay the original failure with a valid control and inspect durable effects or resumed state. Feed that evidence into the failure check; unresolved ambiguity returns to its owner, and accepted behavior proceeds to Patch Checking.

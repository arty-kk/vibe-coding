# Backend Integrations Audit

## Goal and scope

Audit external API, DNS/TLS/proxy, webhook, WebSocket, and SSE boundaries across identity, timeouts, retries, pooling, signatures, ordering, backpressure, and recovery.

## Domain invariants

- Every outbound call has normalized target, authentication, connect/request/idle timeout, cancellation, bounded response/body, and stable error mapping within an end-to-end deadline.
- Retries are limited to classified transient and semantically safe operations, use backoff/jitter and one retry budget, and do not multiply across proxy/client/job layers.
- Connection pools, DNS caching/refresh, TLS trust/SNI/hostname, keepalive, proxy limits, and circuit/admission behavior are bounded across replicas.
- Trusted proxy/header handling has an explicit hop boundary; forwarded identity/scheme/host/client IP cannot be spoofed from an untrusted peer.
- Webhook verification uses the provider/version's exact signed representation and required metadata, applies its replay/timestamp rules and supported verifier, and acknowledges only after the chosen durable boundary.
- Webhook delivery/replay is idempotent by provider event identity, preserves attempts/status, and separates permanent rejection from transient retry.
- WebSocket/SSE authentication, origin, lifecycle, heartbeat/idle timeout, message/event IDs, ordering, reconnect/resume, bounded buffers, slow-consumer policy, and shutdown are explicit.
- Network failures, dependency saturation, certificate/credential rotation, and degraded mode are observable without logging secrets or full sensitive payloads.

## Audit method

1. Trace request/event/connection from DNS/TLS/proxy/client through authentication, timeout/retry, pool, response/ack, persistence, reconnect, and shutdown.
2. Inspect effective retry/timeout/pool settings across all layers and calculate worst-case attempts, duration, concurrent connections, and payload memory.
3. Validate webhook raw-body capture, signature/version/clock/replay state, event identity, durable ack boundary, and re-drive tooling.
4. Trace WebSocket/SSE connect, auth refresh, heartbeat, message sequence, gap, slow consumer, reconnect/resume, and deploy termination.
5. Check DNS/TLS/proxy failure and rotation behavior, trusted headers, redirects/egress constraints, and dependency-specific quotas.

## Handoff

Retain the operation/event/stream identity, effective layered budgets, signed-input vector or event order, and expected completion/effect. Locate the boundary where uncertainty, spoofed identity, duplicate work or a lost sequence becomes an incorrect product result. Feed that case to Improve Backend Integrations; one failed response cannot establish whether the remote effect committed.

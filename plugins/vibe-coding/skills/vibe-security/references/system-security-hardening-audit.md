# System Security Hardening Audit

## Goal and scope

Audit reachable abuse paths across identity, credential attacks, authorization, sessions, egress/parsers, host/container runtime, secrets, dependencies, and detection.

## Domain invariants

- Threat claims identify asset, trust boundary, attacker capability, reachable entry point, authoritative control, concrete impact, and safe validation; hypothetical checklist items are not findings.
- Credential-abuse defenses match the selected threat/policy using appropriate account, network, session or risk signals with bounded distributed state and recoverable response; missing an optional signal is not automatically a defect.
- Authentication, authorization, tenant, object, and privilege decisions are enforced server-side at every authoritative operation, including jobs, exports, admin, and indirect object references.
- Session/token issuance, rotation, revocation, fixation protection, expiry, device/account recovery, MFA/re-auth, and logout invalidate the intended scope without leaking account existence.
- Outbound fetch, DNS resolution/rebinding, redirects, proxying, URL/IP normalization, parser/decompression limits, and file/content handling constrain SSRF and resource-exhaustion paths.
- Host/container/process identity, capabilities, filesystem, seccomp/sandbox, network, metadata service, kernel/runtime patching, and secret mounts follow least privilege and fail closed.
- Secrets and keys have inventory, owner, scope, storage, rotation/overlap, revocation, audit, and compromise recovery; no secret enters logs, prompts, artifacts, images, or source.
- Dependencies/builds use trusted registries/sources, locked identities, reviewable updates, provenance/signing where established, and actionable vulnerability policy.
- Security events preserve actor/target/outcome/correlation without sensitive payloads and feed owned detection, rate-limit visibility, incident containment, and recovery runbooks.

## Audit method

1. Build a narrow threat model for the selected asset/path and trace entry → parsing/identity → authorization → state/side effect → response/log/detection.
2. Inspect every enforcement replica/store and race/failure mode for brute-force counters, lockout, token revocation, tenant checks, and privilege changes.
3. Trace URL/DNS/redirect/content parsing and host/container egress to the actual network boundary; test normalization and resource limits safely.
4. Map secret/dependency/artifact provenance and rotation/revocation behavior through CI, runtime, backups, telemetry, and incident recovery.
5. Validate only with non-destructive fixtures, owned test accounts, synthetic tokens/data, and bounded rates; do not perform uncontrolled scanning or credential attacks.

## Handoff

Return the asset, attacker capability, actual trust crossing, enforced policy and safe input/interleaving that exposes the weakness. Identify which admission, identity, egress/parser, privilege or key-lifecycle owner can prevent the effect. Feed that bounded path into Improve System Security Hardening rather than proposing an unrelated platform/security product.

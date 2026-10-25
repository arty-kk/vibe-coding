# Security Audit

## Goal

Find reachable security issues with concrete repository evidence and produce remediation findings. Do not inflate theoretical patterns into vulnerabilities.

## Inspect

Authentication, sessions, cookies, token handling, authorization policies, tenant/project scoping, admin/staff paths, input validation, serializers, uploads, webhooks, external calls, redirects, secrets/config, logging, migrations, database access, rate limiting, CI/deploy files, and tests.

## Security classes

- Authn/session lifecycle: login, logout, refresh, password reset, OAuth/callbacks, CSRF/CORS, cookie flags, token expiry/storage.
- Authz/RBAC/ABAC: role checks, tenant/workspace/project isolation, object-level access, staff/admin bypasses, visible actions vs allowed actions.
- Injection and unsafe parsing: SQL/NoSQL/command/template injection, SSRF, path traversal, unsafe deserialization, unsafe regex, XML/entity handling.
- Web/API exposure: open redirect, missing webhook signature verification, replay/idempotency gaps, upload MIME/size/path handling, public error leakage.
- Secrets and config: hardcoded secrets, secret logging, weak defaults, missing required env validation, production debug behavior.
- Data protection: PII leakage, excessive logging, export/import exposure, destructive actions without guardrails, backup/migration risks.
- Abuse controls: rate limits, quota bypass, brute-force paths, spam/proactive messaging, background job amplification.
- Dependency/deploy risk only when the repo exposes the vulnerable package/config/path or CI/deploy behavior makes it reachable.

## Finding quality

- Include reachable surface, affected actors/consumers/states, expected behavior, acceptance criteria, and validation direction when discoverable.
- Distinguish direct repo evidence from exploitability inference.
- Prefer fixes at the owning boundary/policy layer over duplicated local guards.
- Do not include exploit payloads beyond what is necessary to explain the risk.

## Handoff

Trace the selected controlled input/principal from a reachable entry through validation and enforcement to its protected effect. Retain the expected policy, first violated boundary and minimal safe reproduction or complete source trace. Feed that evidence into Improve Security when repair is authorized; a dangerous-looking API or absent optional control alone is not a vulnerability.

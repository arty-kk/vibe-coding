# Audit Logging Compliance Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit one security, compliance, financial, admin, or data-governance audit-log boundary. Focus on event completeness, integrity, privacy, retention, queryability, and operational usefulness.

## Domain invariants

- Material actions produce audit events with actor, subject, action, resource, tenant/scope, timestamp, outcome, reason, correlation/request ID, and safe metadata.
- Audit events are emitted at the authoritative owner layer and are not skipped by alternate API, worker, webhook, admin, or bulk paths.
- Logs avoid sensitive payload leakage and support retention/export/deletion requirements defined by the product/repo.
- Audit records are durable enough for the stated use case and have tests or operational gates.

## Audit method

Trace the selected action across API/UI/jobs/webhooks/admin paths, policy decisions, persistence, event emission, log sinks, retention, query surfaces, and tests. Separate application audit logs from generic debug logs.

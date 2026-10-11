# Security Abuse Defense Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected access or abuse-defense control rejects the defined attack without blocking legitimate use.

## Context

Identify selected asset/entrypoint, trusted identity and authorization policy, controlled attacker capability, expected denial, synthetic accounts/data and bounded test rates.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Use synthetic accounts to exercise bounded failed-login/recovery/MFA/session flows across replicas; verify atomic counters, progressive response, generic errors, recovery, and alerts.
- Attempt horizontal/vertical/tenant access with controlled fixtures across API, jobs, exports, and admin paths; verify authoritative denial and audit events.
- Test URL normalization, redirects, DNS changes, private/metadata destinations, oversized/nested/compressed payloads, and parser time/memory limits in isolation.
- Run container/host policy checks for identity, capabilities, filesystem, secret mounts, network egress, and metadata access without weakening production controls.
- Rotate/revoke a test secret/key through old/new overlap and verify clients, caches, logs, artifacts, detection, and rollback/incident procedure.

## Verification

Prove valid use succeeds and the selected abuse is rejected before protected effects; inspect counters, credential scope, audit evidence and recovery without exposing secrets.

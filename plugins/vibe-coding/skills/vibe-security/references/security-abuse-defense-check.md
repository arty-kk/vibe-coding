# Security Abuse Defense Check

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

## Execute and decide

Record asset, trusted policy, controlled attacker capability, synthetic principals/resources and bounded test rates. Establish legitimate use first, then vary only the principal, target/input or interleaving that should be denied.

Observe the actual enforcing boundary and protected effect/store, not only the response. For races or restart/rotation cases, preserve identity and inspect counter/version/credential propagation in the exercised layers. A permanently disabled feature or always-failing harness cannot prove a valid defense.

Return passed, failed or blocked for the selected control and environments with minimal redacted reproduction and permitted control. Feed a remaining reachable violation into the authorized owner repair, repeat that case and finish Patch Checking for changed code. Keep live attack, privileged host change and real credential actions outside this bounded fixture unless explicitly authorized.

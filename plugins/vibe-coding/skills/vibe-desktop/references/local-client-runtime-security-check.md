# Local Client Runtime Security Check

## Goal

Verify one browser-extension or desktop-app local runtime security invariant through bounded permission, storage, messaging/IPC, update/restart, and failure scenarios.

## Context

Identify selected local-runtime boundary, expected security behavior, implementation summary or patch boundary, supported platform/browser, safe environment, fixtures/accounts, and commands/manual scenarios.

## Scenarios

- Verify permission request/denial/revocation behavior.
- Verify message/IPC payload validation and trust-boundary rejection.
- Verify token/secret/local data storage and logging behavior.
- Exercise reload/restart/update/offline/failure states relevant to the selected boundary.
- Run build/package checks when the patch changes release artifacts.

## Execute and decide

Establish the supported browser/OS, actual build mode, permission state and synthetic local resources. Run a healthy control from a permitted origin/process, then vary only the sender, payload, path or permission condition that should cause rejection.

Inspect actual messages and local/OS effects after both cases. A rejection returned after a protected write is a failure, as is a test harness that denies every request. Repeat the selected reload/restart/update sequence and inspect whether identity, secrets and persisted state retain their required boundary.

Return passed, failed or blocked with principal/input, build identity and observed effects. An authorized repair consumes that failed case, repeats it with its control and then receives Patch Checking. Keep unexercised platforms and signing/store requirements separate from local-runtime results.

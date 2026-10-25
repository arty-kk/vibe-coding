# Privacy Data Rights Check

## Goal

Verify one privacy/data-rights invariant through bounded, safe scenarios. Prove the selected collection, consent, export, deletion, retention, logging, or provider behavior without broadening into legal review.

## Context

Identify the selected data field/flow, expected data-right behavior, implementation summary or patch boundary, safe environment, fixtures/accounts, and repository-native commands or manual scenarios.

## Scenarios

- Exercise collection and access behavior for the selected actor/state.
- Verify consent/opt-out/privacy-setting enforcement where relevant.
- Verify export/deletion/retention against primary and directly derived stores.
- Check logs/traces/analytics/error reports for unnecessary sensitive payloads.
- Verify provider calls or webhooks using mocks/sandbox when safe.

## Execute and decide

Use distinguishable synthetic subject/tenant data and an accepted lifecycle policy. Establish the permitted collection/access control, then execute the selected opt-out, export, deletion or expiry transition with its stable operation identity.

Inspect primary and relevant derived stores, exported/provider payloads and logs against that exact policy, including a retry/resume or restoration edge when it can reintroduce the data. A success response or empty UI alone does not prove the downstream lifecycle completed.

Return passed, failed or blocked with subject/operation identity, expected/observed store/provider behavior and missing layers. Feed failures to the authorized owner repair, repeat the lifecycle/control and finish Patch Checking on code changes. Do not delete real user data or infer legal compliance merely to complete a technical check.

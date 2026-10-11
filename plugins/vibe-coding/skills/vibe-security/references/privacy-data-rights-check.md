# Privacy Data Rights Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

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

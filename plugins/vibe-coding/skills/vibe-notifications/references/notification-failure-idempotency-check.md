# Notification Failure & Idempotency Check

## Goal

Verify one notification delivery invariant through bounded success, failure, duplicate, retry, consent, and provider-status scenarios.

## Context

Identify notification type/channel, selected invariant, expected delivery/status behavior, implementation summary or patch boundary, safe sandbox/mock environment, fixtures, and repository-native commands.

## Scenarios

- Trigger the notification once and verify the rendered payload/status.
- Trigger duplicates or job redelivery and prove no duplicate side effect unless explicitly allowed.
- Exercise provider failure, timeout/rate limit, retry, bounce/suppression/status webhook, and recovery behavior.
- Verify consent/unsubscribe, locale/template data, and sensitive metadata handling where relevant.

## Execute and decide

Use synthetic recipients and a controlled provider/queue with known notification identity and initial eligibility. Establish one successful permitted control, then replay the selected duplicate, opt-out, ambiguous timeout, redelivery or out-of-order status sequence.

Observe eligibility decisions, actual provider calls/effects, stored attempts/status and the user/admin result independently. A harness that suppresses all sends cannot prove correct consent or idempotency. Where the provider cannot establish an effect after ambiguity, retain the application's explicit loss/duplicate/reconciliation policy instead of fabricating delivery success.

Return passed, failed or blocked with the sequence, expected/observed effect and status. Pass a failure to the authorized owner repair, rerun its case/control after correction and finish Patch Checking for code changes. Fixture results do not establish an untested provider/channel delivery guarantee.

# Improve Notification Delivery

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected notification delivery path from eligibility through provider status and retry recovery.

## Scope selection

Use the selected notification type, channel, provider event, audit finding, failing test, or explicit delivery bug. Do not redesign the whole messaging system unless required by a selected reliability or consent fix.

## Change targets

- Trigger ownership, deduplication/idempotency keys, consent/unsubscribe, preferences, and channel selection.
- Template data, localization, safe redaction, and copy consistency.
- Queue/job retry behavior, provider adapter errors/timeouts/rate limits, and status webhook handling.
- Delivery logs, observability, user/admin state, tests/fixtures, and docs/maps directly affected.

## Implementation principles

- Do not send duplicate or unauthorized notifications.
- Keep notification side effects behind the authoritative trigger and consent owner.
- Preserve template/provider compatibility and avoid broad copy rewrites outside the selected boundary.
- Use provider sandbox/mocks when available.

## Validation

Run repository-native tests and safe sandbox/mock scenarios for success, failure, duplicate trigger, retry/redelivery, opt-out/no-consent, locale, and provider webhook states relevant to the selected boundary.

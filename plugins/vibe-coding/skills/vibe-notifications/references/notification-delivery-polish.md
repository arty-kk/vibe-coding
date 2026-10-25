# Improve Notification Delivery

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

Repair the authoritative trigger/eligibility, enqueue/effect identity or status/recovery transition. Preserve the same logical notification across retry and reconcile an ambiguous provider response according to its real idempotency/status capabilities; do not promise exactly-once delivery from a local unique row alone.

Feed fixed event/recipient/channel identities, candidate state transitions and provider vectors into the failure/idempotency check. Recheck failed effects or statuses at their owner, then finish Patch Checking. Use sandbox or synthetic recipients unless the user explicitly authorized a real send.

# Bot Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit bot flows, commands, state transitions, keyboards, copy, permissions, and platform constraints. Keep issues that affect user completion, safety, correctness, or operability.

## Inspect

Commands, message/callback handlers, routers, scenes/FSM states, keyboards, templates/copy, middleware, auth/permissions, deep links, scheduled/proactive messages, external integrations, persistence, i18n, tests, docs, and generated bot navigation maps.

## Issue classes

- Entry points: `/start`, `/help`, command list, deep links, onboarding, restart/recovery.
- Navigation/state: back/home/cancel, stale callbacks, invalid state recovery, unreachable states, cyclic dead ends, concurrent messages, session expiry.
- Keyboards/buttons: labels, ordering, destructive confirmation, callback payload limits, duplicate actions, platform-specific behavior.
- Input handling: accepted formats, validation, retry copy, free-text safety, attachment handling, rate/abuse controls.
- Permissions/privacy: admin/staff commands, user identity, group/private chat behavior, tenant/account context, sensitive data exposure.
- Message quality: formatting/escaping, length limits, localization, safe errors, empty/unavailable states, async/proactive status updates.
- Integration and persistence: payment/external callbacks, idempotency, duplicate deliveries, job scheduling, DB state sync, telemetry where present.

## Finding quality

- Include reachable surface, affected actors/consumers/states, expected behavior, acceptance criteria, and validation direction when discoverable.
- Include affected user role, chat type, state, command, or callback when relevant.
- Do not create tasks for platform features the repo does not currently use or expose.

# Audit Notification Content

## Scope

Inspect the selected email, push, chat or in-app template against the event/state and audience it describes. Queue delivery, deduplication and provider status belong to the notification-delivery skill unless they cause the selected content defect.

## Procedure

1. Locate the template and its data producer. Confirm recipient/context, message purpose, current state and CTA destination.
2. Check required/missing values, stale claims, interpolation/escaping, locale/plural/format rules and channel limits.
3. Verify that labels, success/failure wording and actions describe the actual product behavior, including denied or expired destinations.
4. Inspect sensitive data, cross-tenant identifiers and public diagnostics in the body, subject and links. Use synthetic previews for the reachable states.

## Result

Report the affected template/state, observed wording or payload, actual product contract and one correction with a rendering or state-based check. Content review does not authorize sending messages to real recipients.

Feed the event state, synthetic recipient context, template/key, expected action and reachable destination into Improve Notification Content. If the problem begins in eligibility, event ordering or provider status rather than wording, route that specific finding to notification delivery instead of making the template claim a different state.

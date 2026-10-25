# Product UI Audit

## Goal and scope

Audit a selected route or component across data ownership, permissions, all reachable states, accessibility, and user-visible behavior.

## Domain invariants

- Visible actions match authoritative permissions, tenant/project context, plan/quota state, and backend capability.
- Loading, empty, error, retry, stale, success, disabled, no-access, destructive, and partial states are intentional.
- Server/client schemas, cache ownership, navigation, URL state, analytics, localization, and copy remain synchronized.
- Keyboard/focus/semantics, responsive layout, privacy, and performance are preserved for changed states.

## Audit method

1. Map the user goal from route entry to data fetch, decision points, mutation, feedback, and follow-up navigation.
2. Inspect every reachable state and race: slow response, stale request, double action, permission/plan change, and failure.
3. Trace component and cache ownership to backend contracts and identify duplicated UI-only business rules.
4. Use screenshots, previews, browser traces, or tests when available; do not claim visual correctness without them.

## Handoff

Retain route/component, actor/context, initial state and exact action/response order. Trace the first mismatch among data/action ownership, rendered state and backend permission/effect. Feed that failing sequence, expected visible/durable result and source owner into Improve Product UI; avoid treating wrong underlying data as a stylesheet defect.

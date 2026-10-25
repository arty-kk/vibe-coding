# Improve Web Rendering

## Operation

Implement one selected web rendering or server-action correction and verify the user-visible result. Use [web rendering boundaries](../../../references/web-rendering.md) and the repository's framework conventions. A prior audit is unnecessary when the request already identifies the target.

## Required input

The selected route/action, framework/runtime version, rendering mode, affected user state, trusted session/data owner and expected initial and post-interaction behavior. Recover available facts from the repository and supplied reproduction.

## Goal and scope

Restore the contract from server inputs through initial HTML, hydration, interaction and authoritative mutation. Include directly affected serialization, cache invalidation, error handling and tests. Keep independent component redesign, routing migrations and framework upgrades out of the change unless required by the defect.

## Establish the failing state

Name the route, rendering mode, framework/runtime versions and affected user state. Reproduce the failure with a stable fixture: saved preference, locale, authentication state, object identity or relevant request data. Record both server output and browser behavior. Choose acceptance criteria for initial render, post-hydration state and the subsequent interaction before editing.

## Implementation targets

- Make server output and the first client render use the same initial data. Apply browser-only preferences in the correct lifecycle or supply a trusted matching server snapshot. Preserve the preference after hydration and on navigation.
- Keep environment-specific code behind the appropriate boundary without converting the entire page to client rendering merely to hide a mismatch. Avoid random/time-dependent first-render values unless serialized consistently.
- Serialize only data intended for that user; use framework escaping rather than interpolating untrusted HTML or script data. Do not move secrets into browser bundles to resolve a server import failure.
- Construct mutation identity from the trusted server session, then check object/tenant authorization at the owning service. Retain input validation and framework CSRF/origin protections; client fields and hidden controls are not authority.
- Align cache scope and invalidation with personalized reads and successful writes. Update the correct route/query data after mutation, including conflict, denial and retry behavior.
- Preserve meaningful loading, error and empty states and usable focus/navigation when the selected flow depends on them.

## Validation

Run the repository's relevant type/build checks and targeted tests. For hydration, exercise real server rendering and a browser reload with both default and non-default saved state; assert recoverable errors and rendered content, then operate the controls. A snapshot of a component function is insufficient. For actions, exercise legitimate ownership, forged identity, signed-out access, invalid input and observable persisted state; add HTTP/framework checks when the changed layer owns them.

Report the owner changed, user-visible behavior restored, commands/results and untested deployment boundaries. Do not claim a warning-suppression flag fixes divergent content or that action-unit tests verify browser hydration.

Hand the boundary check the original fixture, expected initial/eventual states, changed rendering or mutation owner, authorized and rejected HTTP cases, and any directly affected cache reads. After a correction, rerun the failed route/state and an unchanged control before Patch Checking. A newly changed serialization, session or cache boundary invalidates earlier evidence for that boundary.

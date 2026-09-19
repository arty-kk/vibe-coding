# Web Rendering Audit

Inspect the named route, loader or component without editing. Read the [web rendering boundaries](../../../references/web-rendering.md).

Follow one user journey through the initial server response, client bootstrap/hydration, client navigation and an affected mutation. Inspect response/cache ownership and the data actually serialized, not just the visible component tree.

Reproduce the reported environment difference: direct load versus navigation, server versus browser timezone/locale, signed-out versus signed-in state, or two users sharing the same route. Distinguish request-local memoization from cross-request caching before alleging leakage. Identify the actual producing and consuming source for a mismatch or stale response.

Use the project's browser/test tools for runtime claims. Static inspection can identify a reachable serialization or authorization path but cannot prove a hydration fix or visual layout. Report supported impact, ownership, a concrete repair direction and what was actually observed. Do not turn a rendering audit into an unrelated redesign, framework migration or full security review.

# Web Server/Client Boundary Check

Verify the selected route or mutation without product edits. Read the [web rendering boundaries](../../../references/web-rendering.md). Identify which framework/runtime checks the repository can actually run.

Choose relevant cases rather than executing a universal checklist:

| Changed contract | Verification |
|---|---|
| Initial render | Fresh load and first hydration under the affected locale/timezone/storage state; inspect recoverable errors as well as visible content |
| Private response | Two permitted test principals requesting the same URL; inspect serialized payloads and shared caches, not only rendered text |
| Server mutation | Invoke the handler directly as an unauthorized principal and as the legitimate owner; check stored state after each call |
| Invalidation | Read, mutate, navigate and reload through the affected cache layers |
| Navigation | Direct entry, client transition, back/forward and the relevant loading/error/redirect state |

Keep test identities and mutations inside local fixtures or an authorized test environment. Report actual results and the remaining boundary: a unit test of an action is not a production HTTP/CSRF test, and an HTML snapshot is not proof of successful hydration.

---
name: vibe-web
description: "Audit, repair or verify SSR, hydration, serialized data, route caches, server mutations and navigation in the actual framework."
---

# Web rendering & server boundaries

Read [the shared workflow](../../references/workflow.md) once, then the recipe matching the requested operation. Identify the installed framework/router and rendering mode; do not assume React or Next.js solely because a task concerns a web app.

| Request | Recipe |
|---|---|
| Inspect rendering, serialization or navigation | [Web Rendering Audit](references/web-rendering-audit.md) |
| Fix the named rendering or server boundary | [Improve Web Rendering](references/web-rendering-polish.md) |
| Verify initial render, private data or a server mutation | [Web Server/Client Boundary Check](references/web-boundary-check.md) |

Use the shared [rendering boundaries](../../references/web-rendering.md) for the selected framework path. UI acceptance belongs to [Product](../vibe-product/SKILL.md); an explicit patch review belongs to [Review](../vibe-review/SKILL.md). Follow necessary contract edges without turning the task into a framework migration or redesign.

## Workflow

For an unexplained first-render, stale-route or server-action failure, run **Web Rendering Audit**. Hand the first divergent server/browser value, authorization decision or cache read to **Improve Web Rendering**. Start directly with that repair recipe when the user already supplied the failing boundary and expected result.

After repair, run **Web Server/Client Boundary Check** for the affected route and states, then [Patch Checking](../vibe-review/references/patch-checking.md). Repeat review after corrections under [the cycle contract](../../references/cycles.md). A read-only audit or verification ends at its requested conclusion.

Carry the framework/version, route, rendering mode, initial-state fixture, trusted identity/cache owner and before/after browser or HTTP evidence. The handoff must distinguish first-render agreement, eventual preference, persisted mutation and post-write freshness; success in one does not establish the others.

Invocation lifetime and provider execution limits belong to [Serverless](../vibe-serverless/SKILL.md); optimistic client reconciliation belongs to [Realtime](../vibe-realtime/SKILL.md). Use [Cache](../vibe-cache/SKILL.md) for shared invalidation independent of rendering.

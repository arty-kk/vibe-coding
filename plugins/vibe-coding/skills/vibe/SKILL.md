---
name: vibe
description: "Choose a Vibe Coding workflow when the user invokes the plugin or asks which skill to use. Do not activate for every coding task."
---

# Vibe Coding

Choose the smallest suitable workflow from the user's requested outcome. Use [the shared workflow](../../references/workflow.md) once, then read the selected skill and recipe. Normal implementation should go directly to its target; do not force a preliminary map, audit or plan.

## Select and execute

Identify three things: the requested result, the contract that owns it and the useful entry step. A reported symptom with an unknown cause starts in the domain audit; an established target starts in its implementation prompt; verification-only work starts in the matching check. Select by the violated contract, not by an incidental technology name in the request.

Follow the selected skill's composed workflow one prompt at a time. Pass the previous step's supported finding, chosen correction, acceptance and actual validation into the next step. Fetch/read that next prompt when it is needed; do not load all domain prompts at once or blend their roles into a single generic checklist.

When an authorized workflow changes the repository, finish its domain validation and Patch Checking loop. A correction made during Patch Checking leads to another full pass on the same original review boundary. The workflow ends at the clean marker, the requested non-editing result or a concrete blocked condition.

| Request | Start here |
|---|---|
| Explain or map the repository | [Map](../vibe-map/SKILL.md) |
| Shape a task, combine findings, plan several slices | [Task](../vibe-task/SKILL.md) |
| Review a patch or fix review defects | [Review](../vibe-review/SKILL.md) |
| Find and fix one new bug | [Probe](../vibe-probe/SKILL.md) |
| Check tests or release readiness | [Quality](../vibe-quality/SKILL.md) |
| MCP protocol, tool contracts or transport authorization | [MCP](../vibe-mcp/SKILL.md) |
| SSR, hydration, serialized data or server actions | [Web rendering](../vibe-web/SKILL.md) |
| Serverless invocation lifetime, duplicate triggers or edge limits | [Serverless](../vibe-serverless/SKILL.md) |
| Named domain, framework or infrastructure | [Domain catalog](../../references/catalog.md) |
| Check stale maps or maintain this package | [Workflow](../vibe-workflow/SKILL.md) |

Infer audit/implementation/check from the user's verbs and available context. Ask only for missing information that changes the result. If asked to audit and fix, continue to the authorized correction and verification. An audit-only request ends with findings. Do not spawn tasks, delegate or promise background work simply because a recipe mentions orchestration.

Use [workflow cycles](../../references/cycles.md) for the handoff and repeat conditions. They supply the composition, while the selected domain skill supplies the actual technical investigation and verification.

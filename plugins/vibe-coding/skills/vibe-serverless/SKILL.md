---
name: vibe-serverless
description: "Audit, repair or verify invocation lifetime, reuse, duplicate triggers and provider limits. Web rendering belongs to vibe-web."
---

# Serverless & edge

Read [the shared workflow](../../references/workflow.md) once, then the recipe matching the operation. Establish the provider, trigger and runtime configuration before selecting checks.

## Workflow

Serverless Runtime Audit → Improve Serverless Runtime → Serverless Invocation Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry the runtime/compatibility configuration, trigger/event identity, required/deferred work, response/acknowledgement promise and durable effect/retry owner into the next prompt. A known failure can start at correction; verification-only work uses the check without edits.

Hold the selected required operation pending or failed, replay the same event identity or reuse the environment with another principal to expose the actual lifetime/delivery boundary. Correct that owner rather than adding an arbitrary wait or upgrading the provider.

Return failed completion, isolation or effect evidence to that owner, repeat the control/sequence and finish patch review. A local promise fixture proves local ordering; provider scheduling, quota, disconnect and durability remain separate evidence. Work described inside a retrieved prompt is not completed by the MCP retrieval itself.

| Request | Recipe |
|---|---|
| Inspect invocation and side-effect ownership | [Serverless Runtime Audit](references/serverless-runtime-audit.md) |
| Repair an evidenced runtime boundary | [Improve Serverless Runtime](references/serverless-runtime-polish.md) |
| Verify completion, reuse or redelivery | [Serverless Invocation Check](references/serverless-invocation-check.md) |

Use [runtime boundaries](../../references/serverless-runtime.md) for the actual provider. Rendering/serialization belongs to [Web](../vibe-web/SKILL.md), provisioning plans to [Terraform](../vibe-terraform/SKILL.md). Do not create a cloud deployment to inspect existing code.

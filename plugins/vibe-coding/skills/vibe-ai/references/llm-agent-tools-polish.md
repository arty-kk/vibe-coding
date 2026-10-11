# Improve LLM Agent Tools

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected model-to-tool interaction, preserving tool authorization, bounded execution and safe replay of effects.

## Domain rules

- Put capability and authorization checks in tool/runtime code; treat model intent as untrusted.
- Use typed schemas and stable identities for retryable effects. Retain the authorization/approval required for consequential operations; routine authorized calls do not need new confirmation dialogs.
- Bound steps, parallelism, context, cost, and retries; produce a terminal state for every cancellation or failure.
- Persist only necessary, provenance-bearing, tenant-isolated memory and redact sensitive tool payloads from traces.

## Validation

- Run tool-schema/policy tests plus injection, denied approval, duplicate, timeout, cancel, partial-success, and max-step cases.
- Verify side-effect count and persisted run state after interruption/replay.
- List live tool credentials, external approvals, and provider behavior not exercised.

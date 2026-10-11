# Improve AI Safety & Governance

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected AI safety or release-control behavior, with tested misuse cases and an owned disable or recovery path.

## Domain rules

- Place deterministic restrictions and side-effect approvals outside model behavior.
- Use risk-proportionate review, user transparency, correction, and operator escalation without exposing sensitive internals.
- Version and retain release evidence; block rollout when required evaluation or owner approval is absent.
- Add explicit kill switch/rollback and incident observability for the selected capability.

## Validation

- Run safe adversarial/misuse fixtures, policy boundary tests, human-review/override, logging/redaction, and disable/rollback checks.
- Verify evaluation and release evidence names the exact model/prompt/tool/config version.
- List legal, policy, specialist review, live-provider, and production monitoring gates separately.

# Improve AI Safety & Governance

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected AI safety or release-control behavior, with tested misuse cases and an owned disable or recovery path.

## Domain rules

- Place deterministic restrictions and side-effect approvals outside model behavior.
- Use risk-proportionate review, user transparency, correction, and operator escalation without exposing sensitive internals.
- Version and retain release evidence; block rollout when required evaluation or owner approval is absent.
- For the selected capability's release risk, provide the required disable/recovery and incident signals at their owning controls; preserve existing mechanisms when they satisfy that contract.

## Validation

- Run safe adversarial/misuse fixtures, policy boundary tests, human-review/override, logging/redaction, and disable/rollback checks.
- Verify evaluation and release evidence names the exact model/prompt/tool/config version.
- List legal, policy, specialist review, live-provider, and production monitoring gates separately.

Implement the selected control at the boundary that can prevent or contain the harmful effect. Replay a safe misuse case beside a permitted control and verify that recovery/override does not bypass the same policy. Retain required human decisions as gates rather than inventing compliance. Recheck failed controls after correction, then finish the code/configuration patch through Patch Checking.

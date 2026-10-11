# Improve Security

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Close the demonstrated authorization or input-trust failure at the enforcing boundary and verify valid and denied paths.

## Domain rules

- Place the control at the authoritative boundary and keep denial behavior consistent across all reachable paths.
- Use least privilege and explicit capability/tenant scope; avoid hidden allowlists, UI-only guards, and broad service credentials.
- Preserve non-enumerating user responses while retaining actionable internal audit evidence.
- Treat dependencies, build inputs, webhook payloads, files, URLs, and model/tool outputs as untrusted.

## Validation

- Run affected authz/validation/session/secret tests plus safe negative and replay cases.
- Inspect logs, metrics, and user-visible errors for sensitive data and account/tenant enumeration.
- Verify denial before irreversible side effects and verify rollback/recovery for partially started work.

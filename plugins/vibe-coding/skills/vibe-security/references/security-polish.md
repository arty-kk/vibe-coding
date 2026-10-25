# Improve Security

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

Correct the authoritative verifier, policy, parser or data/effect boundary using the established abuse case and valid control. Preserve intentional public behavior and accepted formats instead of denying everything. Feed the same principal/input/effect expectations into the abuse-defense check; repair remaining reachable violations at their owner and finish Patch Checking without claiming untested production control coverage.

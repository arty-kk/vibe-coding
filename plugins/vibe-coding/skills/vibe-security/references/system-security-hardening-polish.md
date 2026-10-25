# Improve System Security Hardening

## Goal

Correct the selected reachable abuse path using the application’s actual identity, input and runtime policy.

## Domain rules

- Enforce the established policy at the real operation boundary. Reject missing required trusted identity or authority while preserving documented public operations and accepted formats.
- Make credential-abuse controls atomic/distributed, rate-aware, observable, and recoverable; avoid permanent global lockouts or IP-only controls that attackers can weaponize.
- Normalize and validate before authorization/use, then re-check after redirects/resolution/decoding where the interpreted target can change.
- Reduce privilege/attack surface instead of relying only on detection; rotate/revoke exposed secrets and preserve overlap for safe rollout.
- Add tests and security signals for the exact abuse path without recording secrets, raw credentials, personal payloads, or exploit material.

## Validation

- Run repository security/static/dependency/policy tests plus narrow authorization/tenant/session/abuse fixtures.
- Exercise race, distributed replica, restart, counter expiry, revocation propagation, DNS/redirect/parser limits, privilege denial, and rotation overlap in a safe environment.
- Record the proven control, minimal reproduction, residual assumptions and production-only verification gaps.

Repair the first enforcing owner while preserving allowed operation and recovery paths. Replay the same synthetic attack/control and selected race/restart/rotation condition through the abuse-defense check. A failure returns to that boundary; supported evidence proceeds to Patch Checking. Actual credential revocation/rotation or production policy changes use their established authorization and owner procedure, not an automatic action inferred from this checklist.

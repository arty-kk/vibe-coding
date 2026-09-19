# OAuth OIDC Session Check

Verify the selected OAuth/OIDC login, callback or refresh boundary without product edits. Identify the provider, library version, client type, registered redirect URI and flow before selecting cases. OAuth access tokens authorize resource access; an ID token and its validated identity claims have a different purpose.

Trace the authorization transaction from a trusted issuer to the callback and session creation. Verify transaction binding and one-time consumption: PKCE where required, state or another supported CSRF binding, and nonce validation when the flow uses a nonce. Do not call a missing `state` parameter a defect if the implementation demonstrates an applicable alternative. Keep the expected issuer and token endpoint bound to the original transaction.

Use the library's validated claims, not a decoded JWT payload. Check signature/algorithm/key handling, exact expected issuer, audience and applicable authorized-party rules, expiry and nonce. Test a correct callback, another issuer/audience, an expired transaction and a replay. A mismatch must not establish a session or overwrite an existing account. Never link accounts solely by an unverified or ambiguous email claim; inspect the established identity/verification policy.

For refresh, test the configured rotation or sender-binding policy and concurrent refresh behavior. Reject reused invalidated credentials without logging token values. Distinguish revoking the local application session from ending the identity-provider session. Check that post-login return URLs cannot become arbitrary external redirects.

Use test keys, a local issuer or the existing provider sandbox. Report which checks actually ran and which still need provider/browser integration. The applicable requirements are in [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700.html) and [OIDC ID Token Validation](https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation); provider-specific behavior needs matching official documentation.

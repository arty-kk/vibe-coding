# Web Rendering Polish

Fix the requested server/client rendering or navigation behavior using the [web rendering boundaries](../../../references/web-rendering.md).

Locate the source of initial data, serialized fields, identity, cache scope or navigation state responsible for the failure. Make the initial server and client values agree, then apply genuinely browser-only updates at their appropriate lifecycle boundary. Reuse the repository's loader/cache APIs and installed framework version.

For private data, fix the serialization or shared cache owner; hiding a field in JSX does not remove it from a payload. For a server action, resolve the current principal and resource ownership inside the trusted mutation boundary, then update affected UI feedback and invalidation. Preserve unrelated work and existing public behavior.

Verify the original failing path and the directly affected alternate path, such as a fresh document load plus client navigation, or two principals accessing the same URL. A rendering fix needs browser/runtime evidence when that environment is available; otherwise distinguish passing source/unit checks from the blocked hydration or navigation check. Do not silence warnings or disable server rendering simply to obtain a green check.

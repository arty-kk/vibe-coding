# Improve Browser Extension

## Goal

Fix the selected browser extension boundary across manifest permissions, scripts, messaging, storage, backend/native integration, tests, and release packaging when directly affected.

## Scope selection

Use the selected extension feature, permission issue, messaging bug, audit finding, failing test, or packaging failure. Do not migrate manifest versions or redesign the extension globally unless required by the selected fix.

## Change targets

- Manifest permissions/host permissions, content/background scripts, injected scripts, popup/options UI, and message handlers.
- Storage, tokens, cross-origin API calls, native messaging, clipboard/download/tab usage, and safe error states.
- Browser compatibility, tests/manual scripts, packaging, docs/maps, and release notes directly affected.

## Implementation principles

- Preserve least privilege and minimize host/page access.
- Validate message payloads across trust boundaries.
- Avoid exposing secrets or user data to page context.
- Keep browser compatibility and update behavior explicit.

## Validation

Run repository-native extension tests/builds and bounded manual/browser scenarios for the selected feature, including permission denial/revocation and reload/update behavior when relevant.

Correct the manifest, sender validation, background lifecycle or storage owner that violates the selected contract. Rebuild and load the actual supported extension mode in the authorized test environment, then replay allowed/denied messages and the affected worker/reload path. Pass the built identity, permissions and effect observations into the local-runtime check. A failure returns to that boundary; accepted evidence proceeds to Patch Checking without widening host access to hide the error.

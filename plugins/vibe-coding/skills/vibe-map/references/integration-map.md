# Integration Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map the selected provider or service contracts, adapters, configuration ownership and failure/retry paths.

Suggested saved map: `docs/integration_map.md`.

## Build the view

Start at a business caller and follow its adapter, request/response mapping, configuration, callback and retry boundary. Connect timeouts and idempotency to the operation that can create an external effect. Separate provider guarantees evidenced by version/configuration from application assumptions and test-double behavior. Record credential names and ownership only; never read or reproduce secret values to fill the map.

## Inspect

API clients, SDK wrappers, env/config files, secrets references, webhooks, callback routes, background jobs, provider-specific adapters, generated clients, mocks/fakes, tests, rate limit code, retry policies, observability, docs, and deployment manifests.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: integration `INT-*`, provider `PROV-*`, credential/config `CRED-*`, webhook `WH-*`, external contract `EXT-*`, adapter `ADAPT-*`.
- Anchor all entries to current code/config/tests/docs. Never expose secret values; record only variable names, config keys, and ownership.

### Coverage

Cover provider purpose, owner adapter, request/response contracts, auth/credentials, environments, webhooks, retries, timeouts, rate limits, idempotency, error mapping, sandbox/test mode, mocks/fakes, privacy/security boundaries, observability, rollout/rollback, and provider capability assumptions.

### Entry details

For each integration, capture provider, business capability, owner files/symbols, credentials/env, direct callers, callbacks/webhooks, failure modes, retry/idempotency semantics, test strategy, and operational runbook links if present.

# Test Coverage Map

## Operation

Map the requested area using current repository evidence.

## Goal

Connect selected behaviors and acceptance criteria to the assertions, fixtures, commands and unverified gates that cover them.

Suggested saved map: `docs/test_map.md`.

## Build the view

Start from a required behavior and locate the assertions that can detect its violation. Trace the test setup through mocks/fixtures to the production path it actually reaches, then record the command and execution environment. Mark expected but unasserted states, skipped scenarios and external boundaries separately. Test count, file names and line coverage are navigation clues, not evidence that acceptance is verified.

## Inspect

Unit/integration/e2e tests, fixtures, factories, snapshots, golden masters, contract tests, generated clients, CI workflows, package scripts, test docs, runtime check prompts, coverage reports if present, and recent patch evidence supplied by the user.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: test anchor `TEST-*`, suite `SUITE-*`, fixture `FIX-*`, acceptance gap `GAP-*`, external gate `GATE-*`, flaky risk `FLAKE-*`.
- Anchor tests to files/symbols and commands. Do not claim coverage from names alone; identify the behavior actually asserted.

### Coverage

Cover critical flows, domain invariants, permission/plan states, data lifecycle, API contracts, runtime failure/recovery, integrations, UI states, accessibility, performance gates, security checks, CI commands, fixtures, mocks/fakes, flaky or skipped tests, and missing validation.

### Entry details

For each behavior, capture owner invariant, test files/symbols, command, fixture data, asserted states, untested states, related maps/docs, and whether external/manual verification remains required.

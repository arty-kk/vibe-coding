# Bot Navigation Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map the selected bot entries, commands, states, transitions and recovery paths.

Suggested saved map: `docs/bot_navigation_map.md`.

## Inspect

Commands, message/callback handlers, routers, scenes/FSM states, keyboards, templates, middleware, auth/permissions, scheduled/proactive messages, deep links, persistence, tests, docs, platform config, and generated maps if present.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: entry `E-*`, state `S-*`, transition `T-*`, keyboard `K-*`.

### Coverage

Separate user-facing, admin/staff, group/private, and system/proactive states when present. Capture reachability, restart/recovery behavior, stale callback paths, and permission/chat-type boundaries.

### Entry details

For each entry/state/transition, capture trigger, owner symbol, guards/permissions, chat type, rendered copy or template source, keyboard/actions, next states, validation/errors, async/proactive behavior, persistence effects, tests, and known gaps.

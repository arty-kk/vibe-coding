# Improve Bot

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Improve the selected bot flow or related states across navigation, menus, copy, validation, recovery, permissions, and platform constraints. Solve the selected journey end-to-end rather than tweaking one message while adjacent states remain broken.

## Scope selection

- If the user named a command, state, flow, callback, role, chat type, or issue, improve that flow and directly affected states.
- If the request is broad, inspect primary entry points and common bot journeys, then apply the highest-confidence improvements with visible user impact.
- Include related copy, keyboard, validation, stale callback, recovery, and privacy fixes when they belong to the same journey.
- Avoid unrelated features, new integrations, payment/business logic changes, and platform migrations unless the fix requires them.

## Bot-specific targets

- Entry points, `/start`, deep links, `/help`, command list, menus, submenus, stateful navigation, and recovery paths.
- Buttons/keyboards: clear labels, primary/secondary ordering, accessible text, destructive confirmations, stale callback handling, callback payload limits.
- Input prompts: accepted formats, validation, retry copy, cancel/back/home, free-text safety, attachment handling.
- Success/error/status/empty/no-access/unavailable states and async/proactive messages.
- Message formatting, escaping, message length limits, platform-specific keyboard behavior, localization, and privacy constraints.
- Permissions, group/private chat behavior, tenant/account context, and shared copy sources.

## Implementation principles

- Fix the flow owner rather than scattering unrelated message edits.
- Preserve current business rules unless the requested improve requires a behavior correction.

## Validation

Run relevant repository-native checks. When explaining non-obvious repo facts, skipped adjacent work, or detected behavior, cite `path:line[-line]` where useful.

Manually trace the changed bot flow from entry to completion/recovery using code paths or available tests.

Implement the selected transition at its state/router/handler owner, then synchronize its buttons, prompts, persistence and direct callback consumers. Replay the original actor/chat/state combination, a normal path and the affected stale/denied/recovery path using fixtures or an authorized test chat. Code work is not permission to contact real recipients. Return failed transitions to the same owner and finish the resulting patch through repeated Patch Checking.

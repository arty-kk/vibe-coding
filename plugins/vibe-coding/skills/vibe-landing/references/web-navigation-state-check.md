# Web Navigation & State Check

## Goal

Verify that a visitor can follow every important visible route/action, understand control states and recover without dead ends. Establish useful destinations and real transitions, not merely valid URLs or existing anchor IDs.

## Model the reachable paths

Use the actual page/route map, selected audience/conversion paths, component/state inventory and integration boundaries. List meaningful entry points and destinations: logo/home, header/mobile menu, sections, cards, footer, dialogs, forms, result/confirmation, external resources and relevant error/not-found routes. Distinguish links that navigate from buttons that change a state or perform an action.

For each important visible edge, record **entry/state → control → destination/effect → feedback → exit/back/retry**. Include primary and secondary paths and alternate entry points. Check normal browser behavior, keyboard and pointer/touch rather than relying on one scripted happy path.

## Verify transitions and controls

1. Follow links to actual useful content. Check the target's state and promise: a portfolio invitation leading to “not published yet” is still unresolved. Real top-of-page links or external references may be valid; placeholder `#` handlers posing as a conversion path are not. Check fragment targets, sticky-header offsets, direct/deep entry and relevant query/hash/history state.
2. Open and close navigation/disclosures. Verify visible naming, expanded/selected/current state, source order, reachability, dismissal and focus restoration. Use a focus trap only for an actual modal. A closed menu cannot retain hidden focusable items; an open nonmodal menu must not imprison the visitor. On short screens the control and destination remain reachable.
3. Verify every button's actual behavior and state: idle, hover where supported, focus-visible, pressed, selected/toggled when meaningful, pending, disabled/unavailable and error/recovery. `aria-pressed` describes a persistent toggle, not every momentary button. `aria-disabled` alone does not prevent activation. A disabled control needs an understandable reason when the visitor needs to act.
4. Replay forms and selected modules with valid, invalid and unavailable inputs. Check that validation identifies the problem, retains useful data and provides a correction path. Pending prevents unintended repeated effects; accepted, rejected and uncertain results remain distinct. An optimistic status or fake toast cannot establish a persisted/delivered outcome.
5. Exercise back/forward, close/cancel, changing an earlier selection and returning from an external/deep route. Check useful not-found/empty/error states with a way to continue. Avoid loops, stranded dialogs, invisible focus, lost input and navigation that depends on an animation finishing.
6. Inspect labels and geometry in the actual state/viewport. A short CTA should still predict the commitment. Long localized text, icons, overlays and fixed elements cannot hide its target or focus indicator. Current/selected/disabled/error meaning must not rely on color or hover alone.

Use an authorized local/staging test adapter and synthetic data for effects. Real-recipient delivery, live transactions or destructive actions need the relevant authorization; record unverified external effects rather than inventing success. Keep the page's no-JavaScript/static fallback useful where it is part of the architecture.

## Verdict and handoff

Return the traversed path/state matrix, actual destinations/effects, relevant DOM/keyboard/HTTP/persistence evidence and the required-case verdict. A valid anchor with missing promised content fails that path. Required unavailable input/integration evidence remains a concrete gate, even if other links work.

Hand a failure to its route/component/domain owner with the exact reproducer and expected recovery. Repeat the affected path and normal control after repair, then continue the requested acceptance/review sequence. Check-only work ends with its result.

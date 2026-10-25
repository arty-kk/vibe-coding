# Document the Design System

## Scope

Create or update the requested design/UX reference from the repository’s actual tokens, components, layouts and interaction contracts. Reuse the existing document format and language.

## Procedure

1. Inspect maintained theme/token sources, shared components and their variants, relevant routes, styles/assets, design references and previews where available.
2. Identify token/component ownership, public variant API, responsive rules and reachable interaction states. Distinguish implemented behavior from declared design requirements.
3. Document the useful implementation map: where to change a shared rule, its direct consumers and the relevant preview/test.
4. Include keyboard/focus, semantics, content/localization and recovery states where they affect the selected interface. Do not invent a brand system or prescribe unimplemented components.

## Verification

Check referenced symbols, token names, file paths and actual variants. Use rendered evidence for visual claims and state any missing preview/device. Keep only sections useful for future implementation; omit universal design tutorials and placeholder matrices.

The resulting reference should let another agent locate a shared rule, identify its public variants and find the preview/assertion needed before changing it. Keep intended design decisions separate from observed rendering. Recheck source anchors after generation; if saved files changed, finish their documentation patch through Patch Checking without changing the design system merely to match the document.

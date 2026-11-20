# Web Visual Hierarchy & Geometry Check

## Goal

Verify that the page and its components express the intended reading/action hierarchy with coherent geometry, typography and material accents. Judge actual rendered relationships in the requested states; a token table or comparison of font-weight numbers does not establish visual success.

## Inputs and evidence

Use the accepted direction/system, exact copy/assets, component/state inventory, requirement ledger and target route. Identify what should lead in each important state: the proposition, product demonstration, calculated result, selected option, confirmation or next action. Obtain whole-page and focused rendered views with actual fonts/media at narrow/wide and relevant short-height, locale and light/dark-band conditions. Record viewport and state so another reviewer can reproduce the observation.

## Visual and geometric checks

- **Page rhythm:** verify the opening's scale and content-driven height, section pacing, useful variation, transitions and closing/footer. All required copy/actions remain readable; no accidental blank viewport, clipped overlap or repeated composition undermines the narrative. Evaluate the entire page as well as isolated attractive sections.
- **Hierarchy:** compare size, leading/measure, weight/face, contrast, color, location, proximity and background activity together. A link at weight 800 may still be subordinate to a much larger heading at 740. Equal weights can be appropriate for different roles when other relationships are clear. Confirm the actual available face/weight and fallback; do not assume arbitrary variable weights were loaded. Explain a demonstrated competing focal point before changing styles.
- **Internal geometry:** compare intended shared left/right axes, padding and gap steps, baseline alignment, icon optical centers, labels/values, media crops and action rows. Inspect both bounding-box alignment and visual balance. For comparison cards, retain meaningful alignment without clipping longer content or imposing a fixed height on every kind of section.
- **Nested shapes:** check inner/outer corner relationships, inset distances, border width, image bounds, badges and outlines. A derived inner radius may help concentric geometry; apply it where the design actually calls for concentric shapes. Resolve repeated offsets at the component/token owner instead of adding unexplained per-instance nudges.
- **Type and copy:** use actual headline/body/button lengths, glyph coverage, numeric and localized strings. Inspect wrapping, orphaned labels, collisions and readable line lengths at zoom. Important content cannot be hidden by ellipsis merely to preserve a composition. Distinct roles need a deliberate relationship, not mandatory unique colors or weights.
- **Accents and surfaces:** check primary/secondary action emphasis, borders/dividers, elevation/shadow direction, transparency, gradients, highlights and focus/error/selected states. Use fill transparency without accidentally fading all child content. Inspect the worst reading backgrounds and the intended solid/reduced-effect fallback. Decorative separators and required control boundaries have different contrast responsibilities.
- **Identity and graphics:** verify logo variants, favicon-scale source/export quality, icon family/stroke consistency, real-image treatment and meaningful procedural/3D composition. A busy effect must leave the planned reading area usable. Check image loading and crop changes, not just the unloaded placeholder.

For a material or contrast correction, compare before and after at the same route, viewport and state. Check that the intended shadow is visible against its background and that nested edges recede at normal scale. If a complete ring around each component dominates the composition, return the surface treatment for a reduction even when all requested CSS effects exist. Verify selected and focus-visible states separately.

DOM measurements can establish misaligned edges or overflow; a screenshot can establish composition at that moment. Neither alone proves focus behavior, animation timing, conversion or loading performance. Preserve deliberate asymmetry and optical exceptions that are part of the direction. Do not turn an unfamiliar aesthetic into a defect without a violated requirement or demonstrated task impact.

## Verdict and handoff

Return the inspected route/components, intended focal/geometry relationships, per-state observations, screenshots/measurements and `passed`, `failed` or `blocked` for required criteria. A demonstrated failure remains failed even when other evidence is missing. Give its maintained owner and the acceptance observation needed after repair.

An authorized repair returns to the owning page/component/system method, then reruns the changed visual cases and relevant controls. A passing visual check proceeds to the next applicable domain check; it is not a clean-patch or release verdict.

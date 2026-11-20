# Web Interaction & Motion Check

## Goal

Verify the selected functional modules and animation/material storyboard as a usable, coherent runtime experience. Check real state/effect, timing, controls, fallbacks and lifecycle cost; decorative activity alone does not establish a good interactive page.

## Required cases

Read the actual module/state contracts, motion tokens, responsive variants and performance constraints. Select cases for the features present. A complete page may include a calculator, pricing, gallery, lead magnet or 3D scene; it does not need all of them to qualify. Preserve the intended task and product truth when choosing controls and negative cases.

- **Calculators/configurators:** exercise units, normal/boundary/invalid/empty inputs, defaults, reset and changes after a result. Verify the real calculation/domain rule independently of the displayed animation. Result and assumptions remain clear, quantities/locales are correct, and an estimate does not become a binding price. Sliders have an operable alternative to dragging.
- **Forms/downloads/booking:** verify the actual input, pending, acknowledgement, failure/uncertain and retry paths. Check the promised file or authorized destination/effect; reserve “booked” for an actual reserved appointment. Preserve data on recoverable errors and distinguish test adapters from production delivery.
- **Pricing/promos:** verify selected period/plan, displayed amount, billing basis, limits, destination and relevant expiry/eligibility. A switch changes the whole pricing explanation consistently. No invented scarcity or resetting deadline.
- **Galleries/reviews/maps:** verify item position and navigation, discoverable content, keyboard/touch operation, loading/error/text alternatives and user control of auto-rotation. Real attribution/location and a useful non-embed path remain intact.

Use the navigation/state check for shared path/focus issues; avoid duplicating all of its cases when that evidence is current.

## Motion, materials and runtime

Observe the actual timeline and transitions, including interruption and re-entry. Important copy/actions are available without a reveal observer succeeding. No layout shifts, forced scrolling, overlapping entrances, distracting repetitive movement or input blocked by an effect undermines the storyboard. Repeated sections need the intended pacing rather than the same animation indiscriminately applied everywhere.

For a requested effect, trigger the actual control in ordinary motion and observe the changed layer at the start, in flight and after it settles. Repeat with reduced motion and verify the same resulting content and controls. Keep the level of movement within the user's stated limit.

Test reduced-motion/static and keyboard/touch paths, relevant narrow/short screens and failed media/effect loading. Confirm useful state feedback remains available. Ongoing auto-moving/updating content has the controls its behavior requires. A screenshot is insufficient evidence for pause, timing, focus or a media preference; identify unavailable runtime evidence honestly.

For canvas/WebGL/3D or other procedural work, verify resize and bounded resolution/device-pixel ratio, loading/poster/failure fallback, offscreen/hidden-tab pause and cleanup after unmount/navigation. Inspect active loops/listeners/resources and representative CPU/GPU/main-thread behavior using available tools. Test context loss or unsupported rendering with a safe local control when relevant. A heavy effect cannot delay the offer or leave a blank hero when unavailable.

For glass, transparency, gradients, shadows and outlines, inspect actual foreground/background composites through their relevant moving, bright, dark, selected and focus states. Verify dependable reading/control contrast and the intended opaque/simplified fallback. Check the effect's visible area and repaint cost; blur and refraction should not be presumed cheap because they use a modern property.

## Verdict and handoff

Record the tested module/state/effect, expected versus observed results, real calculation/delivery evidence, timeline/fallback/resource observations and required-case verdict. Keep laboratory/device limits explicit; do not infer field performance or real delivery from a local animation demo.

Return a failed module, motion or material case to its owning implementation, repeat affected checks after correction and continue to search/loading/final acceptance where applicable. An absent optional effect can be not applicable with its reason; an explicitly requested working effect cannot be silently omitted to obtain a pass.

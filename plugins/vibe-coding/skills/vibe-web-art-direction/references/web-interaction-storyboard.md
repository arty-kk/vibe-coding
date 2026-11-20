# Web Interaction Storyboard

## Goal

Specify a coherent interactive and animated visitor experience for the chosen page. Every useful module must have real states, meaningful feedback and a feasible implementation contract. Animation should express the visual idea, reveal relationships or respond to the visitor while preserving a readable and usable page.

## Storyboard the experience

Use the section ledger, visual system, actual content and available integration constraints. For each important section or control, record **trigger → state → visible response → duration/easing → exit/reversal → narrow/touch version → reduced-motion/static version**. Identify the source of truth for calculations, selected plans and submitted data. Reuse the same motion language across related actions without giving every section an identical reveal.

Plan the opening entrance, navigation/menu transitions, section pacing, media or object interaction and control feedback. Define which element leads, which supports it and which stays still. Important copy and actions must be available on first render or on a deliberate user-controlled disclosure; a missing observer, delayed JavaScript or failed animation cannot leave the page invisible. Preserve normal scrolling, links, keyboard navigation and text selection.

## Functional modules

Specify only the modules selected for this offer, using their actual decision contracts:

| Module | Required state and outcome definition |
|---|---|
| Header, menu, anchor navigation | Closed/open, focus entry/return, current route/section, dismissal and destination visibility below sticky UI. Trap focus only for an actual modal. |
| Lead or booking form | Required/optional inputs, validation, pending, accepted result, rejection, retry and duplicate prevention. Define recipient/integration and the difference between an enquiry and a reserved appointment. Preserve input on failure. |
| Lead magnet/download | Real file or delivery, eligibility and access path; say what happens after the action. Do not simulate delivery success. |
| Calculator/configurator | Units, approved rules, defaults, valid range, keyboard input, displayed result and assumptions. Include boundary/invalid cases and clarify estimates versus commitments. A drag control needs another operable input. |
| Pricing/plan selector | Billing period/currency/tax basis, included limits, selection state and genuine destination. A period switch must update both numbers and the explanation consistently. |
| Slider, gallery or reviews | Item count/position, previous/next, focus and touch behavior, discoverability and user control. If content rotates automatically, provide pause behavior and respect reduced motion; verify the [carousel interaction guidance](https://www.w3.org/WAI/tutorials/carousels/). |
| Promo/countdown | Real eligibility and deadline, expired state and destination. No resetting scarcity or invented availability. |
| Map/location | Confirmed place or coverage, text/directions alternative, loading/failure and any third-party requirements. The page remains useful if the embed is unavailable. |
| Product/3D demonstration | What the visitor learns, controls, loading/poster/error state, keyboard/touch equivalent and static representation. Keep content independent of a successful GPU scene. |

## Algorithmic and material motion

For a procedural canvas/WebGL/SVG effect, define the field or scene, palette, seed, scale/density, amplitude, speed, interaction influence and quiet reading region. Bound render resolution/device-pixel ratio, active surfaces and any pointer response. Pause work when the section or tab is not visible; release listeners, observers, render loops and GPU resources when unmounted. Specify resize behavior, context-loss handling and a static/no-WebGL fallback. Pointer movement cannot be the only way to reach useful content.

When a backdrop or character responds to a product control, make the visitor's activity its input. Sketch the idle frame, field focus, typing and completion. Choose one leading response in each state. For example, a character can look towards the field while atmospheric detail recedes behind its text. Draw static detail once per resize and budget continuous drawing separately. Check the same task with the decoration disabled and after switching tabs.

For glass and gradients, storyboard the brightest, darkest and densest background states under real text and controls. Prefer a dependable backing surface where contrast varies. Keep blur/refraction costs appropriate to the visible area; define a simplified mobile treatment. A composited transform or opacity change is often less expensive than repeatedly repainting layout or a large filter, but inspect the actual effect rather than assuming a property guarantees good performance. See [animation performance](https://web.dev/articles/animations-guide).

Set a small set of duration/easing tokens with explicit uses. Choose gestures, distances and timing from the desired character; do not demand motion on every element. Honor [reduced-motion preferences](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion), preserve useful state feedback, and supply controls for ongoing auto-updating or moving content under [Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html). Avoid flashing, forced scroll choreography and motion that obstructs reading or input.

## Completion and handoff

Return the storyboard, state contracts, motion parameters, integration/data dependencies and corresponding acceptance cases. Mark what is implemented, proposed or blocked. Cross-check that visual states match the tokens/components and that every visible action reaches the promised outcome. Hand the current offer, architecture, references, visual system and storyboard to **Web Experience Brief**. Planning does not start a live lead flow or prove its delivery.

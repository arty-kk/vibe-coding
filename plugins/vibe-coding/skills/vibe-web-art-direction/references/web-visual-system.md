# Web Visual System

## Goal

Turn the selected art direction into a concrete, internally consistent system of typography, color, layout, components, imagery and materials for the homepage or landing page. Produce the parameters and examples a builder needs, not merely a list of design-system categories.

## Define the system

Use the accepted direction, page ledger, asset constraints and actual framework/component foundations when present. Reuse suitable maintained primitives. An existing product's system may constrain the marketing page; define justified page-specific expression without silently changing the whole application.

- **Typography:** specify actual font families and fallbacks, available files/weights, script coverage, and roles for display, section headings, subheadings, lead/body, labels, captions and numerical data. Give each role responsive minimum/maximum size, line height, weight, tracking and measure. Establish heading-to-body hierarchy from the chosen character. Use scalable units and controlled fluid sizing; verify zoom rather than relying on viewport-sized text alone. Check real headline lengths, accents, Cyrillic and CJK where relevant. Avoid hard line breaks that only work at one viewport. [Typography guidance](https://web.dev/learn/design/typography/) helps evaluate reading size, measure and leading.
- **Palette:** define semantic background, surface, text, muted text, accent, text-on-accent, line, focus and needed status roles with actual values. Plan the relationships across page bands, imagery and interactive states. Check intended foreground/background pairs; do not use a hue name as a claim of sufficient contrast. Define gradient stops and glass backdrops separately from opaque color pairs.
- **Grid and rhythm:** specify container widths, page gutters, column/gap rules, alignment anchors, spacing steps and section spacing tiers. Let text and assets determine intrinsic section height. Define when columns change, how content reorders and how dense modules compress without losing information. Treat short landscape screens, navigation overlays and long translated strings as design inputs.
- **Components:** identify reusable primitives and the section components that compose them. Define content/props, responsive variants, interactive states, boundaries and semantic roles. Reuse a common button, field, icon and container language while allowing an editorial story, comparison, calculator and hero to have distinct composition. Avoid a single configuration-heavy “section” that makes every block look alike.
- **Icons, lines and media:** choose one coherent icon family or a justified custom set; specify optical size, stroke/fill, alignment, accessible naming and meaningful use. Define divider weight, contrast and alignment, image ratios/crops, focal points, masks and media captions. Preserve an actual asset manifest with availability and source rights.
- **Materials:** give gradients an angle and palette, glass an opacity/blur/border/solid fallback, shadows a light/elevation logic and procedural fields a geometry/seed/density/quiet region. [Backdrop filtering](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter) is an enhancement with rendering cost; text still needs a reliable backdrop when it is unsupported or simplified. Specify a static/mobile alternative for expensive effects and a still image or lightweight form for a 3D scene.

Record concrete values in the project's existing token/style structure, a compact design specification, or both when the task requests them. Include representative examples using actual copy. A palette of swatches and a type specimen are useful only when their roles agree with the planned page and component states.

Assign surfaces a role in the composition. Keep the canvas quiet, use distinct fill or a shallow inner shadow for an inset, and reserve the visible outer shadow for the raised surface that needs it. Set a lead cue for each boundary and inspect it over the actual background. A small rim can follow the light along part of an edge. When fill or shadow defines the shape, omit the duplicate decorative outline. Keep dividers, input boundaries, selected/error states and keyboard focus legible for their distinct jobs. Use fill alpha for a translucent surface so text and controls remain readable.

When the direction calls for softer accents, define related tonal variants, subtle alpha fills/borders and appropriate darkening or overlays instead of repeating fully saturated opaque color everywhere. Give each a specific surface/state role and known reading backdrop. Keep necessary text, control boundaries and focus/error meaning legible; global parent opacity is not a substitute for choosing the foreground and surface relationship.

## Optional local design kit

When a reviewable token/material kit would help, load [Web Design Kit](web-design-kit.md), ID `web-design-kit`, after choosing the system parameters. That focused prompt supplies the compiler and example only when needed. Its CSS, SVGs and review board supplement the system specification; they do not decide art direction or certify a website. After this optional material task, continue the current system's handoff to the storyboard. Glass, gradients, actual fonts and responsive compositions still require rendered checking.

## Completion and handoff

Return the token/typographic specification, grid/rhythm rules, component inventory/state definitions, asset/material parameters and representative compositions. Check that their names and values agree, essential text is readable and the proposed formats can be supplied. Hand the system to **Web Interaction Storyboard**. A passing compiler establishes only its stated numeric and structural checks; record unavailable font, material, responsive or visual evidence.

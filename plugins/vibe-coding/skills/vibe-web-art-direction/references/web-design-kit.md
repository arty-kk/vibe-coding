# Web Design Kit

## Goal

Compile already-chosen typography, color, layout, motion and material parameters into a portable local review kit. Create concrete CSS/SVG materials and expose invalid parameters or unreadable opaque text pairs before implementation. This bounded artifact task does not choose the offer or design, build a production site, download assets or prove rendered acceptance.

## Inputs and generation

Use the current visual specification and asset inventory. Adapt [the example input](../assets/design-kit.example.json) rather than treating its palette, type or geometry as a universal style. The parameters must reflect the current project's chosen roles, values and constraints.

Inspect and run [the standard-library compiler](../scripts/compile_design_kit.py) from its installed path:

```sh
python3 compile_design_kit.py --input design-kit.json --output-dir design-kit
```

For MCP retrieval, resource paths label the supplied source and example; place them inside an authorized local workspace before using them. Use a new output directory by default. `--force` replaces this compiler's named outputs and removes superseded generated materials; use it only for the kit being regenerated. Preserve other project files.

The helper generates `design-tokens.css`, `design-board.html`, `design-kit.json`, plus selected `gradient.svg` and `procedural.svg`. Optional `effects` families export named alpha tints, borders and shadows without replacing the opaque text colors. Procedural kinds are flow lines, contours and dots, with an explicit palette, seed, density and quiet region. These are original configurable vector materials; they are not a product photograph, a 3D model or an animation renderer. Place them according to the art direction and storyboard instead of using every sample as a page section.

Run generation with a finite timeout appropriate to the local environment. Invalid input or an existing named output fails before replacement. Failed opaque-text contrast exits nonzero but leaves a reviewable report/board. Correct the chosen parameters and rerun; do not weaken a threshold just to make the report pass. Check the report's specific pairs and render-required list.

## Review and handoff

Inspect the generated board at a narrow and a wide viewport. Check type scale, real font rendering, label/asset-table wrapping, material composition and file loading. The helper does not fetch or verify fonts and graphics. When approved local fonts are available, wire a separate review font stylesheet or the project font setup and verify the actual face/weights/glyphs; retain licensing evidence. Additional illustrations or depth studies need their own meaningful production brief and provenance.

Opaque contrast checks do not establish reading contrast over transparent, gradient, animated or photographic surfaces. Material fallbacks, keyboard states, interaction behavior, performance and a complete page still need their corresponding rendered checks. Numeric font weights alone do not prove visual hierarchy.

Return the selected input, generated paths, actual compiler/preview results and unresolved rendering/asset constraints. Resume the containing design workflow with this evidence; a standalone kit request ends here. Never present a generated study as a finished production website or a delivered business outcome.

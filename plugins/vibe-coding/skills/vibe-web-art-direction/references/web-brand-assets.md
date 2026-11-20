# Web Brand Assets

## Goal

Prepare a coherent, usable identity asset set for the selected website: logo variants, a small-size mark, favicon/browser icons and the sharing or app assets the project actually uses. Work from the accepted brand and direction; a collection of filenames without correct visual/export behavior is not a finished asset kit.

## Identity and variants

Inspect supplied originals and rights/source information. Preserve an existing identity unless a new one is requested. When creating one, derive its form, lettering, proportions and characteristic detail from the offer and art direction. Use available vector/design/image tools suited to the intended result; a portable wordmark or geometric mark normally benefits from an editable vector source. Do not assume a particular production service is available.

Define the variants needed by the real placements: primary horizontal lockup, compact/stacked form when useful, standalone mark, monochrome and inverse/light-on-dark. Keep their geometry, spacing and optical weight related. Establish minimum sizes and clear space from actual samples. A tiny favicon needs an optically simplified mark; shrinking an entire long wordmark does not make a useful browser icon.

Produce real source/export files when the task includes asset creation. For SVG, set a correct viewBox, remove excess bounds and preserve crisp shapes. Package or outline any font dependency needed for portable logo rendering, with appropriate source/licensing information. Check gradients and transparent edges on both intended light and dark surfaces. Avoid hidden remote resources or active content in distributable icons.

## Export and integrate

Choose outputs from the target surfaces, then verify the files themselves:

- Browser: a recognizable small mark in SVG where supported, and the raster/ICO sizes required by the target setup, commonly 16/32/48 px. Verify the actual browser-selected favicon, not only the existence of a link tag.
- Touch/app: provide the touch icon and manifest icon sizes the project declares, commonly 180 px for the Apple touch icon and 192/512 px for web-app icons. Declare maskable purpose only for a composition that respects its safe area. An icon set does not require adding offline behavior or an unrelated service worker.
- Sharing: create an actual social-preview composition for the intended platforms, with readable short copy, a useful crop and the correct image dimensions/type in metadata. A common wide starting size is 1200×630; verify the target consumer's requirements and preview.
- Interface: use the appropriate mark/lockup in header, footer, loading/error surfaces or authentication pages that exist. An image inside a named home link should not repeat an unnecessary screen-reader announcement. Preserve the header/footer alignment and minimum sizes from the visual system.

Use an available reliable renderer for raster exports and inspect the result at its actual size. If a required exporter is unavailable, keep the editable source and identify the missing export; do not rename an SVG to `.png` or claim that a planned file exists. Avoid introducing a new dependency when existing project tools can produce the output. Record source, dimensions, transparency/background, variant purpose and actual path in the asset manifest.

## Acceptance and handoff

Review the complete family together, then inspect the mark at favicon size, the primary lockup in the actual header/footer constraints and the inverse form on its intended background. Check optical consistency, recognizability, edge clipping, transparency and font independence. Validate declared formats/dimensions and remove stale conflicting icon/manifest declarations at their maintained owner when integration is in scope.

Return the actual asset kit and manifest, integration mapping and evidence for completed exports. Separate proposals and unavailable formats from supplied files. Carry the accepted identity into **Web Visual System** and the implementation brief. A request for brand planning alone ends with the production specification; it does not imply publication or changes to an established live identity.

# Web Search & Performance Check

## Goal

Verify the selected page's actual search/AI-search technical readiness and loading behavior against its architecture and current provider requirements. Inspect the delivered output and measured critical path. A set of meta tags, an arbitrary SEO score or a successful build does not establish indexing, AI citations or good real-user performance.

## Source and environment

Identify the requested routes/locales, intended public/staging state, deployment/runtime, maintained metadata/content/asset owners and relevant engines. Build the actual artifact. Inspect initial HTML and, when available and authorized, rendered and public HTTP output. Keep local, deployed, crawler/account and field evidence distinct. Use current primary documentation; search-provider controls change independently of a framework's defaults.

## Search and content checks

1. Verify status/redirects, canonical destinations, real internal links, initial useful content and the intended access/indexing controls. Inspect `robots.txt`, meta robots, response headers and relevant CDN/WAF rules together. Do not treat a staging noindex as a production defect or let a staging policy silently ship to a public release. A robots disallow is not a substitute for understanding indexing behavior.
2. Check truthful page-specific titles, descriptions, heading structure, visible offering/location/identity where applicable, social image/type/dimensions and favicon declarations. Links and main content should remain discoverable through the selected server/static/rendering architecture; an empty client shell needs actual rendering evidence.
3. Check canonical/sitemap/locale consistency. Only real published equivalents belong in alternate-language links; verify reciprocal relationships and the chosen default route. Sitemap URLs, status and last-modification values must reflect real maintained content rather than invented dates or missing pages.
4. Validate applicable structured data against the represented entity, visible content and currently supported provider feature. No fabricated ratings, customers, FAQs or policies. A schema declaration does not promise a rich result; special “AI schema” or a machine-readable file is not a universal eligibility requirement.
5. Review current [Google generative-search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), applicable [Bing webmaster guidance](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a), and the actual provider's crawler/account controls. Check any documented generative-feature inclusion setting when account evidence is available and relevant. For ChatGPT search, consult [OpenAI crawler documentation](https://developers.openai.com/api/docs/bots): search visibility and model-training choices have separate controls. Preserve the owner's explicit policy; do not enable training or change unrelated access to chase visibility.
6. Check whether the page gives useful, specific and supportable answers with clear context and real evidence. Professional copy, relevant imagery, current entity facts and readable structure serve readers and retrieval. Hidden instructions to AI systems, keyword stuffing and mass-produced near-duplicate text are not substitutes for useful content.

## Loading and execution checks

Inspect the initial document, critical CSS/JS, font requests, hero/LCP media, image dimensions/variants, cache/compression and selected third-party work. The likely LCP asset should not be accidentally lazy-loaded or blocked behind an enhancement. Reserve media/font layout space, use appropriate image formats/sizes and defer noncritical widgets/effects while keeping their fallback useful.

Measure a representative narrow-device/network profile and normal control using available tools and finite workloads. Check initial transfer and JS execution against the project budget, image/font decode/loading, main-thread responsiveness, layout shifts, navigation and interaction after load. Include the cost of glass, procedural/3D scenes and external embeds. Repeated warm-cache runs or an empty page are not a realistic substitute for the intended content.

Use current [Core Web Vitals guidance](https://web.dev/articles/vitals) when interpreting LCP, INP and CLS. Good field targets currently include LCP at most 2.5 seconds, INP at most 200 milliseconds and CLS at most 0.1 at the relevant 75th percentile. A laboratory score or a simulated interaction does not prove those field percentiles. Record actual environment/metrics and missing field data rather than relabelling a local proxy as measured INP.

## Verdict and handoff

Return per-route content/head/crawl observations, applicable schema/provider-control evidence, measured loading/interaction results and concrete budget violations. Separate technical pass/failure from unavailable account/crawler/field guarantees. A confirmed failed public route or loading budget remains failed even when other evidence is missing.

For an authorized correction, hand the failed case to its rendering/content/configuration/asset owner and repeat the same output/measurement after repair. Use the focused search-visibility or performance methods when their deeper domain evidence is needed. Continue to final acceptance and Patch Checking for the actual change; do not claim indexing, rankings, citations or search-console setup that was not observed.

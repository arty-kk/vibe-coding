# Web Project Architecture

## Goal

Choose an implementation-ready modular architecture and technology stack for the actual website and its expected evolution. Define rendering, ownership, boundaries, data/integration contracts, delivery and performance. A framework list or an empty monorepo tree is not an architectural decision.

## Inputs and decision criteria

Inspect the existing repository, versions, hosting/runtime constraints, team/editor workflow and accepted offer/page/interaction brief. Classify the actual work: public content, interactive islands, shared application state, authenticated/personalized routes, server mutations, content management, localization, search or transactions. Identify what must be present in initial HTML, what genuinely needs client JavaScript and what needs a trusted server. Account for the real media and material budget, not just the HTML shell.

Preserve a suitable existing stack. For a new project, compare credible options against these requirements and select one with a concrete rationale. A mostly public, content-led page may use static/server rendering with selectively hydrated components; a page sharing a substantial application may benefit from its existing full-stack framework. A complex calculator does not itself require hydrating the whole page. Consult current official documentation for the chosen framework, supported runtime, dependencies and deployment adapter; do not equate the newest package version with the best supported choice.

## Structure and ownership

Use the requested monorepo when specified. Split packages where there is an actual shared contract, ownership boundary or independent runtime. A useful shape to adapt is:

```text
apps/
  web/                 routes, page composition, public assets and web runtime
  api/                 only when a separate deployed API boundary is needed
packages/
  ui/                  shared accessible primitives and stable variants
  design-tokens/       shared type/color/spacing/material/motion values
  domain/              pure pricing/calculation/eligibility rules
  content/             structured content, copy and locale ownership
  config/              genuinely shared build/type/test conventions
```

Keep a page's section components and feature modules inside its app unless another consumer or boundary justifies a package. Omit unused directories. Define public exports and allowed import directions: apps consume packages; packages do not import app internals; server-only capabilities cannot leak into client modules. Keep business rules testable without a renderer and keep content out of ad hoc component conditionals. Define who owns routes, theme values, copy, assets, integration adapters and each interactive feature.

Choose the workspace/package manager, lockfile, supported runtime, strict type configuration, task graph and build outputs from the selected stack. Configure caching by real task inputs/outputs and dependency order. Use the actual build and validation commands; an aspirational command in a README does not establish a working setup. Avoid installing duplicate tools to perform the same job.

## Runtime, content and integrations

- Specify the rendering mode for each route and interactive island, including initial HTML, enhancement/hydration boundary, loading and no-JavaScript behavior. Avoid client-only wrappers around otherwise crawlable content without a requirement.
- Define structured content and localization ownership, how editors change it, and how copy/asset changes reach generated pages, sitemap, social metadata and components. Keep one maintained source for repeated claims and version/count data.
- Give forms, downloads, booking, calculators, maps and pricing selectors explicit contracts. Define input validation, units/rules, state/result types, server authority, error/timeout/retry behavior and recipient/delivery evidence. Keep secrets on the trusted boundary. Distinguish a local test adapter from a real deployed integration.
- Define asset handling: real image variants, intrinsic sizing, font coverage/subsets, icon/logotype exports, social previews and lazy enhancement for large 3D or procedural modules. Use the visual system's static/reduced-motion fallbacks and lifecycle cleanup.
- Match hosting to the selected build/runtime, caching and integration needs. Identify environment variables and bindings by name/purpose, without inventing credentials. State storage, regional or runtime limits that materially affect the design. Do not provision accounts/services or migrate infrastructure merely because it is mentioned in a proposed architecture.

## Quality and delivery plan

Set measurable budgets for initial transferred JavaScript/CSS/fonts/media, LCP content, main-thread work and layout stability appropriate to the page. Specify server/static caching and invalidation where needed. Plan page-level metadata, canonical/localized routes, robots/sitemap and current search-provider eligibility/control checks at their maintained owner. Decide how staging and public indexing policies differ.

Define a lean validation path: type/build checks, focused domain/unit checks, integration state cases, keyboard/navigation, responsive visual review, material/motion fallback and search/loading checks. Respect local resource limits; move heavy workloads to suitable CI rather than increasing local workers blindly. Include release/environment configuration and recovery for an actual deployment when requested.

## Completion and handoff

Return the chosen stack and current support evidence, adapted file/package tree, module/import boundaries, route/rendering map, content/token ownership, integration contracts, asset/performance budgets and real commands/delivery outputs. Explain material tradeoffs and unresolved dependencies. A generic “works for any idea” claim is not a decision; the architecture must support the specified page and its plausible next requirements.

Pass these decisions into **Web Experience Brief**. A planning request stops with a buildable specification; creating the repository, buying services and deployment require their own requested scope.

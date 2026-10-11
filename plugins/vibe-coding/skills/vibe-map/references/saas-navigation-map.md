# SaaS Navigation Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map selected routes and UI surfaces to navigation, data, role/plan/tenant gates and reachable states.

Suggested saved map: `docs/saas_navigation_map.md`.

## Inspect

Routing, layouts, pages, guards, loaders/actions, API hooks, state stores, forms, tables, dialogs, navigation components, auth/RBAC, plan/billing/quota code, tenant/workspace/project context, i18n, analytics/observability, tests, docs, and generated route maps.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: route `R-*`, layout `L-*`, modal/drawer `M-*`, form `F-*`, table/list `T-*`, guard `G-*`.

### Coverage

Capture product context when discoverable: app type, primary roles, tenant model, plan model, auth/onboarding model, main entity graph. Cover user, admin/staff, public/auth, no-access/no-plan/over-quota, empty/loading/error, destructive, and async states when present.

### Entry details

For each route/surface, capture path or trigger, owner symbol, layout, roles/guards, plan/tenant behavior, data dependencies, actions, states, forms/tables/modals involved, tests, and gaps.

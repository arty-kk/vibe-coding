# MCP Server Audit

Inspect the selected MCP server or client without edits. Read the [MCP contract boundaries](../../../references/mcp-contract.md), then follow the relevant protocol path in the repository.

Start with the supported protocol/SDK versions and transport. Locate discovery, schema registration, transport middleware, identity construction and one selected handler. Follow a concrete call to its result and any downstream side effect. Compare actual handler behavior with the tool's schema and annotations.

Keep findings tied to a reproducible request or a reachable source path: a mismatched schema, ignored tool error, principal supplied by tool arguments, wrong token audience, protocol/version mismatch, cross-user discovery reuse, or unsafe replay. Missing optional protocol features are not defects unless advertised or required by a supported client.

Run the existing local protocol/handler tests when useful. Direct handler tests cannot establish HTTP conformance or real-host compatibility. Report the defect, affected client/revision, evidence, remediation direction and relevant verification gap. If no defect is supported, bound that conclusion to the inspected path.

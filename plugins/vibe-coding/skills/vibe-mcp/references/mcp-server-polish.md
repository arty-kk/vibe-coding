# MCP Server Polish

Implement the requested MCP contract change using the [MCP contract boundaries](../../../references/mcp-contract.md). Work within the existing SDK and supported protocol revisions; upgrading either requires a compatibility reason in the task.

Fix the owning registration, middleware, handler or client result adapter and carry the change through directly affected callers. Preserve public tool names and required argument semantics unless the requested change includes a migration. Correct an inaccurate annotation at its definition, and correct a permission defect where the authenticated principal and protected resource are resolved.

For a retry or reconnect change, account for a lost response after a committed downstream effect. Reuse the application's stable operation identity or report the outcome as unknown; adding retries around a mutation is not a complete fix.

Exercise the reported failure and a valid call. Include a denied call or malformed result when the changed contract warrants it. Record whether validation covered a direct handler, transport exchange or actual host. Do not register or publish the server, add credentials or enable optional extensions merely to complete a local fix.

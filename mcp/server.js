import {createMcpHandler, McpServer} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
import {searchWorkflows, getWorkflow, VERSION, LANGUAGES, MODES} from './library.js';

const annotations = {readOnlyHint: true, destructiveHint: false, openWorldHint: false};
const language = z.enum(LANGUAGES).default('en').describe('Language for titles and summaries. Technical instructions remain in English.');
const workflow = z.object({id: z.string(), title: z.string(), skill: z.string(), mode: z.string(),
  category: z.string(), summary: z.string(), purpose: z.string().optional(), url: z.string()});
const responseFormat = z.enum(['workflow', 'legacy']).default('legacy').describe('Set workflow for individual purposes, match reasons and composed step outlines. Omitted retains the exact 1.5.1 result shape while a client still uses the previously published schema.');
const execution = z.object({
  status: z.literal('instructions_only'), intent: z.enum(['requested', 'improve']), current_step: z.string(),
  steps: z.array(z.object({id: z.string(), role: z.string(), when: z.string(), handoff: z.array(z.string())})),
  transitions: z.array(z.object({from: z.string(), outcome: z.string(), to: z.string().nullable(), condition: z.string()})),
  completion: z.object({id: z.string(), clean_marker: z.string(), findings_marker: z.string(), blocked_marker: z.string(),
    recheck_marker: z.string(), no_patch_marker: z.string(), rule: z.string()}),
  resource_rule: z.string()
});

function output(value, format) {
  if (format !== 'workflow') {
    const metadata = row => ({id: row.id, title: row.title, skill: row.skill, mode: row.mode,
      category: row.category, summary: row.summary, url: row.url});
    value = value.workflows ? {
      version: value.version, instruction_version: value.instruction_version, language: value.language,
      total: value.total, next_offset: value.next_offset, workflows: value.workflows.map(metadata)
    } : {
      version: value.version, instruction_version: value.instruction_version,
      instruction_language: value.instruction_language, language: value.language, host: value.host,
      workflow: metadata(value.workflow), files: value.files, words: value.words
    };
  }
  return {structuredContent: value, content: [{type: 'text', text: JSON.stringify(value)}]};
}

function failure(tool, message) {
  console.warn(JSON.stringify({event: 'tool_error', tool}));
  return {isError: true, content: [{type: 'text', text: message}]};
}

export function buildServer() {
  const server = new McpServer({name: 'vibe-coding-library', version: VERSION}, {
    capabilities: {tools: {}},
    instructions: 'Vibe Coding is an engineering playbook library for any coding agent using MCP. For bug diagnosis, feature implementation, task planning, code review or behavior verification, search_workflows finds a method from the technical goal; no workflow name or user mention of the library is required. Use response_format:workflow on both tools. Then get_workflow loads the selected prompt and its ordered/conditional workflow. Execute it with your own project tools, carry evidence to the next step and fetch only that reached step. Implementation ends with relevant verification and repeated Patch Checking until an actual clean pass or a concrete blocker. Honor the user’s operation, project instructions and permissions; retrieval alone never authorizes changes or proves a check passed. Use host:generic unless Codex or Claude is actually in use. Send only a public technical description, never repository contents, secrets or personal data.'
  });
  server.registerTool('search_workflows', {
    title: 'Vibe Coding: choose a method for a coding task',
    description: 'Find an engineering playbook to follow when fixing a bug, implementing a feature, planning work, reviewing a patch or verifying behavior. Use it from the task itself; the user need not know Vibe Coding or a workflow name. Covers APIs, UI/UX, data, queues, infrastructure, security, AI and other coding domains. Supply a short technical goal, for example "fix stale cache after a write", "verify Kafka consumer rebalance" or "Patch Check". Searches English, Spanish, Russian and Simplified Chinese terms; exact IDs and named aliases rank first. Set response_format:workflow for concise purposes, domains, operations, stable IDs and match reasons, not the instructions yet. Select the appropriate ID and call get_workflow with response_format:workflow to obtain the executable prompt and workflow stages. Public guidance only; does not read your repository or perform the task.',
    inputSchema: z.object({
      query: z.string().max(240).default('').describe('A short natural-language technical goal, symptom, workflow title or exact ID; empty browses. Examples: "исправить гидратацию SSR", "verificar reintentos de pagos", "缓存". No code, private file contents, secrets or personal data.'),
      skill: z.string().regex(/^vibe-[a-z-]+$/).max(64).optional().describe('Optional skill identifier, such as vibe-sql or vibe-backend.'),
      mode: z.enum(MODES).optional().describe('Optional exact operation filter: audit=inspect, implement=make an already-requested change, check=verify, review=review an existing patch, plan=prepare work. Omit when unsure; query verbs guide ranking without silently changing this filter.'),
      language, response_format: responseFormat,
      full_text: z.boolean().default(false).describe('Search instruction bodies as well as the catalog when metadata search is insufficient.'),
      limit: z.number().int().min(1).max(10).default(5),
      offset: z.number().int().min(0).max(240).default(0)
    }).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), language: z.enum(LANGUAGES),
      total: z.number().int(), next_offset: z.number().int().nullable(), suggested_action: z.string().optional(),
      workflows: z.array(workflow.extend({match: z.object({kind: z.enum(['browse', 'catalog', 'instruction_body', 'exact_id', 'exact_title', 'alias']), terms: z.array(z.string())}).optional()}))}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(searchWorkflows(args), args.response_format); }
    catch (error) { return failure('search_workflows', error.message); }
  });
  server.registerTool('get_workflow', {
    title: 'Vibe Coding: load the next engineering workflow step',
    description: 'Get the actionable engineering instructions after choosing a result from search_workflows, or load a next-step ID from a previously returned execution outline. Use the returned file text as the method for your coding task with your own repository tools. With response_format:workflow, returns the current prompt, required foundations, source hashes and an execution outline with ordered/conditional next IDs, evidence handoffs and repair/recheck exits. Only the current prompt body is loaded; fetch later IDs when their transitions are reached. For an already-authorized audit-and-fix task, intent:improve composes audit → repair → relevant check → repeated Patch Checking; requested preserves a read-only audit/check/plan scope. A known implementation starts at its implementation ID. The library works with any coding agent: default host is generic, Codex/Claude additions are optional. Retrieval is instructions only, never an executed check or a clean verdict.',
    inputSchema: z.object({id: z.string().min(1).max(100).regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/),
      language, response_format: responseFormat,
      host: z.enum(['generic', 'codex', 'claude']).default('generic').describe('Keep generic for any other MCP coding agent; host-specific project files and native skill commands are not required.'),
      intent: z.enum(['requested', 'improve']).default('requested').describe('requested=the selected operation; improve=compose diagnosis and repair only when the user has already requested changes. This flag grants no new permissions.'),
      include_context: z.boolean().default(true).describe('Keep true on first load. Set false for later steps only while the same-version working contract, cycle rules and domain context remain available; returns the current prompt and specialized references without repeating those foundations.')}).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), instruction_language: z.literal('en'),
      language: z.enum(LANGUAGES), host: z.enum(['generic', 'codex', 'claude']), context_included: z.boolean().optional(), workflow, execution: execution.optional(),
      files: z.array(z.object({path: z.string(), text: z.string(), sha256: z.string(), source_url: z.string()})),
      words: z.number().int()}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(getWorkflow(args), args.response_format); }
    catch (error) { return failure('get_workflow', error.message); }
  });
  return server;
}

const handler = createMcpHandler(buildServer, {maxRequestBodySize: 65536});

export async function handleMcp(request) {
  const origin = request.headers.get('origin');
  const url = new URL(request.url);
  // Anonymous access is intentional: every tool only reads the compiled public library.
  if (origin && origin !== url.origin) return new Response('Origin not allowed', {status: 403});
  if (request.method === 'OPTIONS') return new Response(null, {status: 204, headers: {Allow: 'POST, GET, DELETE, OPTIONS'}});
  if (!['POST', 'GET', 'DELETE'].includes(request.method)) return new Response('Method not allowed', {status: 405, headers: {Allow: 'POST, GET, DELETE, OPTIONS'}});
  const started = performance.now();
  const response = await handler.fetch(request);
  if (response.status >= 400) console.warn(JSON.stringify({event: 'protocol_error', status: response.status,
    duration_ms: Math.round(performance.now() - started)}));
  response.headers.set('Cache-Control', 'no-store');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  return response;
}

import {createMcpHandler, McpServer} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
import {VERSION, LANGUAGES, MODES, SKILLS} from './metadata.js';

const annotations = {readOnlyHint: true, destructiveHint: false, openWorldHint: false};
const instructions = [
  'Load an applicable workflow at the start of a software task that calls for planning, a change, diagnosis, verification, or review. Use the user’s goal or symptom for architecture, data changes, permissions, unstable tests, API compatibility, performance, deployment, and rollout.',
  'Call get_workflow with a short public task description to choose and load a method. Use search_workflows to compare candidates or browse domains when the fit is unclear.',
  'Call get_website_plan_workflow when asked what sections a site needs, how to order its content, or how visitors leave an enquiry. Choose offer for audience and positioning or architecture for the stack and modules.',
  'Apply the current step within the requested scope. Load later steps when reached. Handle unrelated tasks or a goal with no matching method using the host’s ordinary tools.'
].join(' ');
const websitePlans = {
  sections: 'web-page-architecture',
  offer: 'web-offer-synthesis',
  architecture: 'web-project-architecture'
};
const language = z.enum(LANGUAGES).default('en').describe('Choose a language for titles and summaries. Read the technical instructions in English.');
const host = z.enum(['generic', 'codex', 'claude']).default('generic').describe('Choose the coding agent for optional host guidance. Use generic for any other MCP client.');
const workflow = z.object({id: z.string(), title: z.string(), skill: z.string(), mode: z.string(),
  category: z.string(), summary: z.string(), purpose: z.string().optional(), url: z.string()});
const responseFormat = z.enum(['workflow', 'legacy']).describe('Use workflow for purpose, match reasons and step outlines. Choose legacy for the original compact response.');
const catalog = z.object({
  level: z.enum(['domains', 'topics']), status: z.enum(['ok', 'unknown_topic', 'scope_conflict', 'empty_scope']),
  keyword_language: z.literal('en'),
  domains: z.array(z.object({key: z.string(), title: z.string(), keywords: z.array(z.string()),
    topic_count: z.number().int(), workflow_count: z.number().int()})),
  topics: z.array(z.object({key: z.string(), skill: z.string(), title: z.string(), keywords: z.array(z.string()),
    modes: z.array(z.string()), workflow_ids: z.array(z.string())}))
});
const execution = z.object({
  status: z.literal('instructions_only'), intent: z.enum(['requested', 'improve']), current_step: z.string(),
  steps: z.array(z.object({id: z.string(), role: z.string(), when: z.string(), handoff: z.array(z.string())})),
  transitions: z.array(z.object({from: z.string(), outcome: z.string(), to: z.string().nullable(), condition: z.string()})),
  completion: z.object({id: z.string(), clean_marker: z.string(), findings_marker: z.string(), blocked_marker: z.string(),
    recheck_marker: z.string(), no_patch_marker: z.string(), rule: z.string()}),
  resource_rule: z.string()
});
const workflowBundle = z.object({version: z.string(), instruction_version: z.string(),
  instruction_language: z.literal('en'), language: z.enum(LANGUAGES), host: z.enum(['generic', 'codex', 'claude']),
  context_included: z.boolean().optional(), workflow, execution: execution.optional(),
  files: z.array(z.object({path: z.string(), text: z.string(), sha256: z.string(), source_url: z.string()})),
  words: z.number().int()});

function output(value, format) {
  if (format !== 'workflow' && !value.catalog) {
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
    instructions
  });
  server.registerTool('search_workflows', {
    title: 'Find workflows across software engineering tasks',
    description: 'Compare workflows for designing websites or codebases, changing schemas or permissions, diagnosing defects, stabilizing tests, checking API compatibility, reviewing patches and preparing releases. Start these tasks from the goal or symptom in the user’s words. Send a short public description to get ranked workflow IDs, then load a matching ID with get_workflow. Browse domains or topics with view:catalog and an empty query when no method matches. Keep source code, credentials and personal data out of queries.',
    inputSchema: z.object({
      query: z.string().max(240).default('').describe('Describe a short task or symptom in ordinary language, or give a title or exact ID. Keep the purpose and relevant symptom or constraint. Omit source code, credentials and personal data.'),
      view: z.enum(['workflows', 'catalog']).default('workflows').describe('Choose workflows to rank a task description. Choose catalog with an empty query to list domains, or topics and workflow IDs for the supplied skill.'),
      skill: z.enum(SKILLS).optional().describe('Use an exact returned domain key, such as vibe-web-strategy for offers and page structure or vibe-landing for builds. Combine filters to narrow the result.'),
      topic: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).max(100).optional().describe('Copy an exact topic key from the catalog to restrict the results to its member workflows.'),
      mode: z.enum(MODES).optional().describe('Choose audit to inspect, implement to make an authorized change, check to verify, review to assess a patch, or plan to prepare work. Omit the filter when unsure.'),
      language, response_format: responseFormat.default('legacy'),
      full_text: z.boolean().default(false).describe('Set true to search instruction bodies when catalog metadata is insufficient.'),
      limit: z.number().int().min(1).max(10).default(5).describe('Request up to ten results. Omit for five.'),
      offset: z.number().int().min(0).default(0).describe('Pass the returned next_offset to load the next page.')
    }).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), language: z.enum(LANGUAGES),
      total: z.number().int(), next_offset: z.number().int().nullable(), suggested_action: z.string().optional(), catalog: catalog.optional(),
      workflows: z.array(workflow.extend({match: z.object({kind: z.enum(['browse', 'catalog', 'instruction_body', 'exact_id', 'exact_title', 'alias']), terms: z.array(z.string())}).optional()}))}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try {
      const {searchWorkflows} = await import('./library.js');
      return output(searchWorkflows(args), args.response_format);
    } catch (error) { return failure('search_workflows', error.message); }
  });
  server.registerTool('get_workflow', {
    title: 'Load a workflow for ordinary software engineering work',
    description: 'Load an engineering playbook before planning, changing, diagnosing, verifying or reviewing software. Use it for practical requests such as adding a database field without downtime, checking access after a role change, fixing intermittent tests, reviewing a change before merge, or rolling out to part of the audience. Pass a brief public task description in query to choose and load the workflow, or pass a known ID for a specific step. Apply the returned method within the user’s scope. Use search_workflows when several methods fit.',
    inputSchema: z.object({
      id: z.string().min(1).max(100).regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).optional().describe('Pass a known workflow ID. Supply exactly one of id or query.'),
      query: z.string().trim().min(1).max(240).optional().describe('Describe a task or question in ordinary language, such as "I want a nice site for a studio, what sections should it have?". Supply exactly one of query or id. Omit source code, credentials and personal data.'),
      language, response_format: responseFormat.describe('Omit to receive workflow for a query or legacy for an exact ID. Choose a format to override that default.').optional(),
      host,
      intent: z.enum(['requested', 'improve']).default('requested').describe('Use requested for the selected operation. Choose improve to compose diagnosis and repair when the user has authorized changes. Respect current permissions.'),
      include_context: z.boolean().default(true).describe('Keep true on first load. Set false for later steps only while the same-version working contract, cycle rules and domain context remain available; returns the current prompt and specialized references without repeating those foundations.')}).strict(),
    outputSchema: workflowBundle,
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try {
      const {getWorkflow} = await import('./library.js');
      return output(getWorkflow(args), args.response_format ?? (args.query ? 'workflow' : 'legacy'));
    } catch (error) { return failure('get_workflow', error.message); }
  });
  server.registerTool('get_website_plan_workflow', {
    title: 'Load a website planning workflow',
    description: 'Load the read-only planning method before advising on a new website’s sections, content order or enquiry path. Use it for a brief question such as "what should go on my studio website and how can clients contact me?", even before there are project files. Choose sections for page structure and conversion, offer for audience and positioning, or architecture for the stack and module boundaries. Apply the returned method to the user’s brief.',
    inputSchema: z.object({
      focus: z.enum(Object.keys(websitePlans)).default('sections').describe('Choose sections for page structure and enquiry flow, offer for the value proposition, or architecture for the stack and modules.'),
      language, host
    }).strict(),
    outputSchema: workflowBundle,
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async ({focus, language, host}) => {
    try {
      const {getWorkflow} = await import('./library.js');
      return output(getWorkflow({id: websitePlans[focus], language, host}), 'workflow');
    } catch (error) { return failure('get_website_plan_workflow', error.message); }
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

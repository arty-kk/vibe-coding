// This is a retrieval plan, not a job runner or a stored execution verdict.
export function buildExecution(library, id, intent = 'requested') {
  const spec = library.workflowSpec;
  const byId = new Map(library.recipes.map(row => [row.id, row]));
  const row = byId.get(id);
  const family = spec.families.find(item => item.audit === id || item.implement === id);
  const mayRepair = intent === 'improve' || row.mode === 'implement';
  const steps = [], transitions = [];
  const add = (identity, when) => {
    if (!steps.some(step => step.id === identity)) steps.push({id: identity,
      role: byId.get(identity).mode, when, handoff: spec.handoffs[byId.get(identity).mode]});
  };
  const edge = (from, outcome, to, condition) => transitions.push({from, outcome, to, condition});
  add(id, 'Current requested prompt; apply it to the selected project boundary.');

  const review = spec.patch_check.id;
  const repair = family?.implement || (row.mode === 'implement' ? id : null);
  if (family && mayRepair) {
    if (row.mode === 'audit') {
      add(repair, 'After a supported finding, when the user already authorized its correction.');
      edge(id, 'supported_findings', repair, 'Implementation is already authorized; preserve the finding and acceptance case.');
      edge(id, 'no_qualifying_findings', null, 'Finish the selected audit; do not manufacture a patch.');
    }
    let previous = repair;
    for (const check of family.checks) {
      add(check.id, check.when);
      edge(previous, 'ready_for_verification', check.id, check.when);
      edge(check.id, 'failed', repair, 'Return the failing case to its repair owner, then rerun affected verification.');
      previous = check.id;
    }
    add(review, 'After a patch exists and relevant domain criteria have evidence.');
    edge(previous, 'passed', review, 'Review the complete resulting patch against the original comparison base.');
  } else if (row.mode === 'implement') {
    const sequence = spec.sequences[id] || [{id: 'behavior-check', when: 'Verify the selected changed behavior and a valid control.'}];
    let previous = id;
    for (const step of sequence) {
      add(step.id, step.when);
      edge(previous, 'ready_for_verification', step.id, step.when);
      edge(step.id, 'failed', id, 'Repair the demonstrated defect and repeat the affected check.');
      previous = step.id;
    }
    add(review, 'After the changed behavior is verified.');
    edge(previous, 'passed', review, 'A patch exists; review its full resulting state.');
  } else if (row.mode === 'probe') {
    add(review, 'Only if this one-area probe produced an authorized, verified patch.');
    edge(id, 'patch_created_and_verified', review, 'Carry the original failure/control evidence; do not start another probe.');
    edge(id, 'no_patch', null, 'Return the parent skill’s found/no-bug/blocked outcome.');
  } else if (id === 'map-staleness-check' && mayRepair) {
    add('map-refresh-polish', 'Only for evidenced stale entries whose correction is authorized.');
    edge(id, 'stale', 'map-refresh-polish', 'Preserve stable map IDs and current source evidence.');
    edge('map-refresh-polish', 'corrected', id, 'Recheck the changed entries against their source owners.');
    add(review, 'After changed map files pass freshness verification.');
    edge(id, 'fresh_after_correction', review, 'A patch was created in this workflow.');
    edge(id, 'already_fresh', null, 'No correction or patch review is required.');
  } else if (row.mode !== 'review') {
    // Planning may have further planning stages. It never silently starts code changes.
    let previous = id;
    const sequence = spec.sequences[id] || [];
    const readOnlySequence = sequence.some(step => byId.get(step.id).mode === 'implement') ? [] : sequence;
    for (const step of readOnlySequence) {
      if (byId.get(step.id).mode === 'implement') continue;
      add(step.id, step.when);
      edge(previous, 'ready', step.id, step.when);
      previous = step.id;
    }
    edge(previous, 'requested_result_complete', null, 'Stop at the requested evidence, artifact or verdict.');
  }
  if (steps.some(step => step.id === review)) {
    edge(review, 'corrections_applied', review, 'Validate the correction, then review the full new patch against the same original base.');
    edge(review, 'clean', null, 'A full pass made no correction, found no qualifying defect and has evidence for every required check.');
    edge(review, 'findings_without_repair_authority', null, 'Report findings; a review-only request does not authorize edits.');
  }
  for (const step of steps) {
    edge(step.id, 'blocked', null, 'A required decision, authority, environment or evidence is unavailable, or the same failure repeats without a changed patch, new hypothesis or new evidence.');
    if (step.role === 'check' && mayRepair && family) {
      const position = family.checks.findIndex(check => check.id === step.id);
      edge(step.id, 'not_applicable', family.checks[position + 1]?.id || review,
        'This check’s condition is outside the changed boundary; retain direct validation and explain the skipped criterion.');
    }
  }
  return {status: 'instructions_only', intent, current_step: id, steps, transitions,
    completion: {...spec.patch_check,
      rule: 'Retrieving these instructions is not a check result. Only an actual final review pass may emit the clean marker. Missing required evidence, an unresolved decision or repeated failure without new evidence stops blocked; no patch uses the no-patch outcome.'},
    resource_rule: 'Only the current prompt body is loaded. Fetch a reached next-step ID with get_workflow and response_format:workflow; retain this outline and the prior handoff. Use include_context:false only while the same-version working contract and domain context remain available. Project instructions and existing authorization govern every action.'};
}

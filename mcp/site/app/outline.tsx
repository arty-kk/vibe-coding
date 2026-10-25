import type {UiCopy} from './copy';

type Step = {id: string; role?: unknown; when?: unknown; handoff?: unknown[]};
type Transition = {from: string; outcome?: unknown; to: string | null; condition?: unknown};
export type Execution = {
  status: 'instructions_only'; intent?: 'requested' | 'improve'; current_step: string;
  steps: Step[]; transitions?: Transition[]; completion?: {rule?: unknown}; resource_rule?: unknown;
};
const describe = (value: unknown) => typeof value === 'string' ? value : value == null ? '' : JSON.stringify(value);

export default function InstructionOutline({execution, c, busy, onLoad}: {
  execution: Execution; c: UiCopy; busy: boolean; onLoad: (id: string) => void;
}) {
  if (execution.status !== 'instructions_only' || !Array.isArray(execution.steps)) return null;
  return <section className="instruction-outline" aria-label={c.outline}>
    <h3>{c.outline}</h3><p className="hint">{c.outlineHint}</p>
    <ol className="outline-steps">{execution.steps.filter(step => typeof step.id === 'string').map(step => {
      const current = step.id === execution.current_step;
      return <li key={step.id} aria-current={current ? 'step' : undefined}>
        <div className="outline-step-heading"><code>{step.id}</code>{current && <span className="current-instructions">{c.currentInstructions}</span>}</div>
        {step.role != null && <p className="outline-role" lang="en">{describe(step.role)}</p>}
        {step.when != null && <p><span>{c.when}: </span><span lang="en">{describe(step.when)}</span></p>}
        {Array.isArray(step.handoff) && step.handoff.length > 0 && <details><summary>{c.handoff}</summary><ul>{step.handoff.map((value, index) => <li key={index} lang="en">{describe(value)}</li>)}</ul></details>}
        {!current && <button type="button" disabled={busy} aria-label={`${c.loadStep}: ${step.id}`} onClick={() => onLoad(step.id)}>{c.loadStep}</button>}
      </li>;
    })}</ol>
    {Array.isArray(execution.transitions) && execution.transitions.length > 0 && <details><summary>{c.transitions}</summary><ul className="outline-transitions">{execution.transitions.map((transition, index) => <li key={index}><code>{transition.from}</code><span aria-hidden="true"> → </span>{transition.to === null ? <span>{c.terminalPath}</span> : <code>{transition.to}</code>}<p lang="en">{[describe(transition.outcome), describe(transition.condition)].filter(Boolean).join(' · ')}</p></li>)}</ul></details>}
    {execution.completion?.rule != null && <details><summary>{c.completion}</summary><p lang="en">{describe(execution.completion.rule)}</p></details>}
    {execution.resource_rule != null && <details><summary>{c.resourceRule}</summary><p lang="en">{describe(execution.resource_rule)}</p></details>}
  </section>;
}

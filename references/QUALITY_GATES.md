# Quality Gates

This document defines the reusable gates. Skills choose applicable gates and link to them.

## Plan gate

- destination, scope, exclusions, inputs, outputs, blockers, and completion criteria exist;
- the plan file predates implementation;
- known user decisions are incorporated;
- no unnecessary human gate remains.

## Structure gate

- every skill contains triggers, inputs, ordered process, completion criteria, failure paths,
  output contract, and context pointers;
- shared policy is referenced rather than copied;
- all referenced paths exist.

## State gate

- YAML parses;
- dependency graph is acyclic;
- frontier matches blocker status;
- DONE packages have plan and result files;
- a result file cannot predate its plan;
- model execution remains within recorded policy and budget.

## Execution gate

- deterministic commands or equivalent evidence were actually run;
- long jobs expose heartbeat/progress;
- retry attempts are classified and bounded;
- successful checkpoints are preserved.

## Diagnosis gate

- the feedback loop is red-capable, deterministic, fast enough, and agent-runnable;
- the exact reported symptom is reproduced and minimized;
- hypotheses are ranked and falsifiable;
- fix passes regression and original-scenario verification;
- debug instrumentation is removed.

## Research gate

- material claims have evidence records;
- primary sources are preferred;
- classifications are not collapsed;
- unresolved gaps and conflicts are explicit.

## Acceptance gate

Report axes independently:

- **Standards:** repository rules, structure, safety, and maintainability;
- **Spec:** required behavior, scope, and exclusions;
- **Evidence:** actual runs, sources, fixtures, and provenance.

Overall PASS requires all applicable axes PASS. `PASS_WITH_GAPS` is never equivalent to DONE
unless the specification explicitly allows the named gaps.

## Security gate

- no secret material or private endpoint is present;
- permissions are least-privilege;
- untrusted PR code cannot access secrets;
- remote scripts/actions are pinned;
- model execution is disabled unless explicitly authorized.

## Resume gate

- `ACTIVE_TASKS.yaml`, state, handoff, branch, and run references agree;
- exact next action is executable;
- a fresh session needs no repeated background explanation.

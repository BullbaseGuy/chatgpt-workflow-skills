# Durable Handoff

## Task identity
- Task ID: `chatgpt-workflow-skills-v1`
- Repository: `BullbaseGuy/chatgpt-workflow-skills`
- Branch: `agent/chatgpt-workflow-skills-v1`
- Canonical state: `docs/implementation/chatgpt-workflow-skills-v1/task_state.yaml`

## Verified completed
- W00–W02 baseline, shared references/templates, router, spec, and handoff skills.
- W03 frontier planner and execution supervisor.
- Deterministic validators reject cycles, stale frontier, invalid DONE, missing plan/result,
  malformed UTC, and nonzero model execution.
- Unit tests distinguish long-but-progressing from stale-no-progress runs.

## Current frontier
- `W04` — diagnose-before-retry.

## Active blockers
None.

## Exact next action
Implement the diagnosis skill and repro manifest, validate its mandatory phases and no-rerun gate,
write `W04_result.md`, and continue to W05.

## Do not repeat
Long runtime alone is not failure. A stale heartbeat means inspect, not automatically rerun.

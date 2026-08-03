# Durable Handoff

## Task identity
- **Task ID:** `chatgpt-workflow-skills-v1`
- **Repository:** `BullbaseGuy/chatgpt-workflow-skills`
- **Branch:** `agent/chatgpt-workflow-skills-v1`
- **Canonical state:** `docs/implementation/chatgpt-workflow-skills-v1/task_state.yaml`

## Destination
Deliver the reusable skill system, deployment paths, historical regressions, and scaffold integration.

## Verified completed
- W00 adoption, conflict, and license baseline.
- W01 operating contract, decision policy, task-state schema, evidence schema, quality gates,
  failure taxonomy, output contract, and five durable templates.
- YAML examples and canonical task state parse successfully.
- Codex/model invocation count remains `0`.

## Current frontier
- `W02` — implement `workflow-router`, `task-to-spec`, and `durable-handoff`.

## Active blockers
None.

## Exact next action
Implement the three W02 skills using references rather than copied rules, run structural and
routing fixtures, write `W02_result.md`, and move the frontier to W03.

## Do not repeat
The role split, AUTO default, PowerShell-first rule, no-Gmail rule, no-blind-rerun rule,
single-source rule, and Codex=0 baseline are already decided.

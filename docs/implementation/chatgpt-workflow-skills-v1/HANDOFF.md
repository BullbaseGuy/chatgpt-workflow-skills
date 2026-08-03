# Durable Handoff

## Task identity
- Task ID: `chatgpt-workflow-skills-v1`
- Repository: `BullbaseGuy/chatgpt-workflow-skills`
- Branch: `agent/chatgpt-workflow-skills-v1`
- Canonical state: `docs/implementation/chatgpt-workflow-skills-v1/task_state.yaml`

## Destination
Deliver the reusable skill system, deployment paths, historical regressions, and scaffold integration.

## Verified completed
- W00 source adoption, conflict reconciliation, licensing, contract, glossary, and ADR.
- W01 seven shared references and five templates.
- W02 `workflow-router`, `task-to-spec`, and `durable-handoff`.
- Seven routing fixtures resolve to one primary skill and the expected decision mode.
- Codex/model invocation count remains `0`.

## Current frontier
- `W03` — frontier planner, execution supervisor, deterministic validators, and CI.

## Active blockers
None.

## Exact next action
Implement W03, run cycle/frontier/state fixtures, write `W03_result.md`, and continue to W04.

## Do not repeat
The role split, decision modes, state authority, no-Gmail rule, PowerShell-first rule,
no-blind-rerun rule, and Codex=0 baseline are settled.

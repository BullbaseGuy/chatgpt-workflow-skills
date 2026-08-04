# Durable Handoff

## Task identity

- **Task ID:** `chatgpt-workflow-skills-v1`
- **Repository:** `BullbaseGuy/chatgpt-workflow-skills`
- **Branch:** `agent/chatgpt-workflow-skills-v1`
- **Canonical state:** `docs/implementation/chatgpt-workflow-skills-v1/task_state.yaml`
- **Final acceptance:** `docs/implementation/chatgpt-workflow-skills-v1/ACCEPTANCE_REPORT.md`

## Verified completed

- W00–W09 are complete with plan/result files and persistent evidence.
- All ten required skills, shared references, templates, validators, regression scenarios, deployment paths, and PowerShell installation tooling are implemented.
- The tested release payload is commit `74a3cb0cf4eebb406782ca3360318f1dce0f6c6d`.
- Skills source Draft PR: `BullbaseGuy/chatgpt-workflow-skills#1`.
- Scaffold integration Draft PR: `BullbaseGuy/demo-project#2`.
- Skills source Actions runs `30835973435` and `30835973467` succeeded.
- Scaffold Actions runs `30836366525`, `30836366028`, `30836366871`, and `30836366162` succeeded.
- Standards, Spec, Evidence, Security, and Resume are all PASS.
- Codex/model execution remains disabled with invocation count `0`.

## Current frontier

None. The implementation frontier is empty.

## Active blockers

None.

## Exact next action

Perform ordinary human code review and merge in dependency order:

1. review and merge `BullbaseGuy/chatgpt-workflow-skills#1`;
2. review and merge `BullbaseGuy/demo-project#2`.

No additional implementation, credential, Gmail, external service, or manual configuration is required before review. The scaffold lock intentionally points to the tested release payload commit rather than later evidence-only closeout commits.

## Resume rule

A fresh session receiving only `chatgpt-workflow-skills-v1` must resolve the completed entry in `ACTIVE_TASKS.yaml`, read canonical state and this handoff, and report the two reviewable Draft PRs. It must not reopen W00–W09 or ask the user to restate settled decisions unless new evidence identifies a defect.

# Durable Handoff

## Task identity
- Task ID: `chatgpt-workflow-skills-v1`
- Repository: `BullbaseGuy/chatgpt-workflow-skills`
- Branch: `agent/chatgpt-workflow-skills-v1`

## Verified completed
- W00–W06 adoption, shared rules, routing, supervision, diagnosis, evidence, architecture,
  acceptance, and PowerShell manual wizard are complete.
- W07 adds seven executable historical scenarios, a pinned result snapshot, and mutation tests.
- The scenarios distinguish live long Actions, stale canonical state, x_scrap cursor/429,
  Bark real-device acceptance, F10 material source conflicts, Pine UI acceptance, and task-id resume.
- Local W07 validation passed 7/7 scenarios and 4/4 mutation tests.
- All 10 required skills exist; Codex/model invocation count remains `0`.

## Current frontier
- `W08` — native ChatGPT Skills and ChatGPT Project + GitHub dual deployment.

## Active blockers
None.

## Exact next action
Create an immutable-revision consumer manifest, PowerShell installer/updater, consumer lock format,
deployment guides, hash/compatibility validators and CI coverage. Prove idempotent local installation
without executing unpinned remote code, write W08 result, and continue to W09.

## Do not repeat
The source-of-truth separation, decision modes, PowerShell-first policy, secret handling, diagnosis
policy, evidence schema, and historical workflow outcomes are settled. Do not ask the user to choose
them again.

# Durable Handoff

## Task identity
- Task ID: `chatgpt-workflow-skills-v1`
- Repository: `BullbaseGuy/chatgpt-workflow-skills`
- Branch: `agent/chatgpt-workflow-skills-v1`

## Verified completed
- W00–W05 adoption, rules, routing, supervision, diagnosis, evidence, architecture, and acceptance.
- W06 PowerShell manual wizard, manifest schema, secure/idempotent template, validator, and tests.
- All 10 required skills now exist.
- Static safety rejects secrets in GitHub Variables, shell metacharacters, missing irreversible
  confirmation, credential-like samples, `Invoke-Expression`, and command-line secret bodies.
- 30 deterministic tests pass; Codex/model invocation count remains `0`.

## Current frontier
- `W07` — seven historical workflow regression scenarios and aggregate runner.

## Active blockers
None.

## Exact next action
Encode the seven required historical scenarios with common assertions, implement the regression
runner, execute all scenarios plus the full validation suite, write W07 result, and continue to W08.

## Do not repeat
PowerShell-first and secret handling are settled. No real external configuration is required in this task.

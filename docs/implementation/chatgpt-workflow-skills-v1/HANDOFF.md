# Durable Handoff

## Task identity
- Task ID: `chatgpt-workflow-skills-v1`
- Repository: `BullbaseGuy/chatgpt-workflow-skills`
- Branch: `agent/chatgpt-workflow-skills-v1`

## Verified completed
- W00–W04 adoption, common rules, routing/spec/handoff, frontier supervision, and diagnosis gates.
- W05 evidence research, architecture review, and independent acceptance review.
- Evidence and acceptance validators reject unsupported inference, fabricated non-disclosure values,
  one-sided conflicts, secret retention, and completion with any failing axis.
- 9 skills and 22 deterministic tests pass locally.
- Codex/model invocation count remains `0`.

## Current frontier
- `W06` — PowerShell manual wizard skill, template/library, static safety checks, and fixtures.

## Active blockers
None.

## Exact next action
Implement W06 with PowerShell 7, idempotent writes, secure input, GitHub secret stdin handling,
destructive confirmation, static validation, and tests; write W06 result and continue to W07.

## Do not repeat
Architecture review is now assigned and implemented in W05. Evidence classifications and the
five-axis completion gate are settled.

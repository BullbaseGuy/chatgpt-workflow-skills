# Durable Handoff

## Task identity
- Task ID: `chatgpt-workflow-skills-v1`
- Repository: `BullbaseGuy/chatgpt-workflow-skills`
- Branch: `agent/chatgpt-workflow-skills-v1`

## Verified completed
- W00–W07 core skills, rules, deterministic validators, PowerShell wizard, and historical regressions are complete.
- W08 provides one manifest-backed source for native ChatGPT Skills and ChatGPT Project + GitHub use.
- The release payload contains 10 skills, 9 references, 7 templates, and 2 license files, each locked by Git blob SHA.
- Local release tests passed 5/5: exact revision, idempotency, tamper detection, context-pointer closure, and native bundle generation.
- Linux and Windows install-compatibility workflows are committed; final remote Checks are part of W09.
- Codex/model invocation count remains `0`.

## Current frontier
- `W09` — integrate `BullbaseGuy/demo-project` by immutable reference and perform final acceptance.

## Active blockers
None.

## Exact next action
Create a `demo-project` integration branch, add a lock file pinned to
`22e10ad9fef0a0de828dfe0b48fafa1802928019`, add compatibility validation and documentation without
copying skill bodies, open reviewable PRs in both repositories, verify their Checks, write the final
Standards/Spec/Evidence/Security/Resume acceptance report, and close canonical state.

## Do not repeat
Do not revisit adopted skill names, decision modes, source-of-truth separation, PowerShell-first
policy, evidence schema, release payload, or revision policy unless new evidence shows a real defect.

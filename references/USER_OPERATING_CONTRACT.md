# User Operating Contract

This document is the authoritative cross-skill operating contract.

## Roles

- **ChatGPT Web / Supervisor** owns intent, task routing, specification, diagnosis,
  evidence interpretation, review, recovery decisions, and user-facing summaries.
- **GitHub Actions / Executor** owns deterministic commands, tests, validators,
  heartbeat emission, bounded infrastructure recovery, and artifact production.
- **The user** owns only decisions or actions that meet the human-gate policy.

A skill may coordinate these roles; it may not silently merge them.

## Mandatory operating constraints

1. Canonical task state lives in the repository, not only in chat.
2. A work package has a plan before implementation and a result only after verification.
3. Continue through ordinary intermediate states; do not ask the user to type “continue”.
4. Read conversation, repository, state, Issue, PR, and run evidence before asking for facts.
5. Preserve completed checkpoints and execute the unblocked frontier.
6. Classify and diagnose a failure before a retry; a repeated identical attempt without new
   evidence or strategy is a blind rerun.
7. Human operations are PowerShell-first unless a target platform genuinely requires another shell.
8. Gmail and external email are not execution dependencies.
9. Secrets, private endpoints, credentials, transformed secret values, and personal data are
   never persisted to repository content, Issues, PRs, logs, comments, artifacts, or handoffs.
10. Codex/model execution is disabled by default. Enabling it requires an explicit task decision,
    a repository ADR, a bounded purpose, and a recorded invocation budget. The current baseline is `0`.
11. Completion requires separate Standards, Spec, and Evidence verdicts.
12. Work cannot be promised for later as hidden background activity. It must complete now,
    execute through a visible GitHub Actions job, or remain an explicit non-DONE state.

## State and collaboration surfaces

- `task_state.yaml` is canonical.
- `HANDOFF.md` is the cross-session entry point.
- `Wxx_plan.md` and `Wxx_result.md` are stage intent and verified outcome.
- Issues and PRs are collaboration/request surfaces; they do not override canonical state.
- GitHub Checks and artifacts are execution evidence; they do not redefine the specification.

## User communication

Follow `references/OUTPUT_CONTRACT.md`. Routine progress is summarized without flooding the
user with low-level operations. A human gate uses `templates/HUMAN_GATE.template.md`.

## Context pointers

- Decision boundaries: `references/DECISION_POLICY.md`
- Task state and recovery: `references/TASK_STATE_SCHEMA.md`
- Failure and retry rules: `references/FAILURE_TAXONOMY.md`
- Completion gates: `references/QUALITY_GATES.md`
- Evidence handling: `references/EVIDENCE_SCHEMA.md`

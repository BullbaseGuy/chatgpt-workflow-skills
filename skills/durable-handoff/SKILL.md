---
name: durable-handoff
description: Resolve and refresh repository-backed task context so a fresh ChatGPT Web session can resume from a task ID, Issue, PR, commit, branch, or Actions URL without restating history.
---

# Durable Handoff

## Triggers

Invoke when:

- the user says “继续执行”, “检查进度”, “从上次恢复”, or equivalent;
- a new session receives only a task ID, Issue, PR, commit, branch, or Actions URL;
- a context window is nearing its limit;
- execution becomes interrupted, blocked, or complete;
- another skill needs to transfer work across sessions.

## Inputs

At least one of:

- task ID;
- repository and branch;
- Issue or PR URL/number;
- commit SHA;
- GitHub Actions run URL;
- current task directory.

## Process

1. **Resolve the target.** Use the explicit reference, repository metadata, and
   `docs/implementation/ACTIVE_TASKS.yaml`.
2. **Read in order:** repository contract; canonical state; dependency graph; existing handoff;
   current plan/result; referenced Issue/PR/run; applicable failure/evidence records.
3. **Verify reality.** Compare repository branch, PR, run, and artifact state with the canonical
   references. Never trust a stale handoff over current GitHub evidence.
4. **Validate consistency.** Check the resume gate and frontier calculation.
5. **Refresh `HANDOFF.md`** from `templates/HANDOFF.template.md`:
   - link existing specs/results instead of duplicating them;
   - list only evidence-backed completed checkpoints;
   - identify every current frontier item and blocker;
   - give one executable exact next action;
   - list established facts that must not be re-asked.
6. **Update canonical state** if verified remote reality changed.
7. **Route forward.**
   - active unblocked work → `execution-supervisor`;
   - observed failure → `diagnose-before-retry`;
   - apparent completion → `acceptance-review`;
   - genuine human gate → present the persisted gate.

## Completion criteria

- target repository/task and branch are resolved;
- GitHub reality and canonical state are reconciled;
- handoff contains destination, verified completed work, frontier, blockers, evidence, exact next
  action, and do-not-repeat facts;
- a fresh session can execute the next action without asking for history;
- the next skill is invoked or explicitly persisted.

## Failure paths

- **Task reference maps to multiple active tasks:** resolve by repository/branch/run evidence;
  create a material ambiguity gate only if still unresolved.
- **Canonical state missing but recoverable from branch/PR:** reconstruct a draft state and mark it
  `VERIFYING`; do not pretend it is authoritative until reviewed.
- **State and remote execution conflict:** route to `acceptance-review` resume axis.
- **Permission prevents verification:** create `HUMAN_GATE/PERMISSION`.

## Output contract

Primary artifact:

`docs/implementation/<task_id>/HANDOFF.md`

A visible resume message states verified status, blocker if any, and the exact next action; it does
not repeat the full project history.

## Context pointers

- `references/USER_OPERATING_CONTRACT.md`
- `references/TASK_STATE_SCHEMA.md`
- `references/QUALITY_GATES.md`
- `references/OUTPUT_CONTRACT.md`
- `templates/HANDOFF.template.md`

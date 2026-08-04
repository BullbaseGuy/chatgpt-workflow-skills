# Canonical Task State Schema

`docs/implementation/<task_id>/task_state.yaml` is the sole machine-readable task authority.

## Top-level required fields

```yaml
schema_version: 1.0.0
task_id: unique-slug
title: Human-readable destination
repository: owner/name
branch: agent/task-slug
decision_mode: AUTO # AUTO | APPROVAL | HUMAN_GATE
status: RUNNING # PLANNING | READY | RUNNING | BLOCKED_AUTO | NEEDS_HUMAN | VERIFYING | DONE | FAILED_TERMINAL
stage: W03
execution_status: RUNNING # NOT_STARTED | RUNNING | INTERRUPTED | COMPLETED | FAILED
acceptance_status: PENDING # PENDING | PASS | FAIL | PASS_WITH_GAPS
security_status: PASS # PENDING | PASS | SECURITY_BLOCKED
created_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
updated_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
last_heartbeat_utc: "YYYY-MM-DDTHH:MM:SSZ"
frontier: [W03]
active_blockers: []
human_gate: null
model_execution:
  enabled: false
  codex_invocations: 0
work_packages: []
verification:
  standards: PENDING
  spec: PENDING
  evidence: PENDING
```

Additional fields are allowed when a project documents them.

## Work-package record

```yaml
- id: W03
  title: Optional descriptive title
  status: READY # PLANNING | BLOCKED | READY | RUNNING | VERIFYING | DONE | FAILED | NEEDS_HUMAN
  blocked_by: [W02]
  plan_path: docs/implementation/<task_id>/W03_plan.md
  result_path: docs/implementation/<task_id>/W03_result.md
  checkpoint_commit: null
  executor:
    type: github-actions
    run_url: null
  retry:
    attempts: 0
    budget: 2
    last_failure_id: null
```

## Valid transitions

```text
PLANNING -> READY
READY -> RUNNING
RUNNING -> VERIFYING | BLOCKED_AUTO | NEEDS_HUMAN | FAILED_TERMINAL
BLOCKED_AUTO -> RUNNING | NEEDS_HUMAN | FAILED_TERMINAL
NEEDS_HUMAN -> RUNNING | FAILED_TERMINAL
VERIFYING -> RUNNING | DONE | FAILED_TERMINAL
DONE -> DONE
```

`DONE` is monotonic. Reopening requires an explicit new work package or a recorded correction
decision; it must not silently erase evidence.

## Frontier calculation

A work package is in the frontier when:

- its status is `READY` or a recoverable `BLOCKED_AUTO`;
- every `blocked_by` package is `DONE`;
- it is not currently claimed by another active executor;
- its retry budget is not exhausted.

The dependency graph must be acyclic. A task may have more than one frontier item, subject to
its declared parallelism limit.

## Heartbeat and stall

A running job must expose one of:

- incremental task-state updates;
- timestamped log heartbeat;
- a measurable completed-unit counter.

A stale heartbeat is a signal to inspect, not proof of failure. A stall decision also requires
run status and progress evidence. Projects define the interval; absence of a project rule defaults
to 15 minutes for active jobs and 60 minutes for known long external waits.

## Resume algorithm

Given only a `task_id`, Issue, PR, commit, or Actions URL:

1. resolve repository and branch;
2. read `ACTIVE_TASKS.yaml`;
3. locate canonical state and handoff;
4. verify referenced run/PR state against GitHub;
5. validate state consistency;
6. select the unclaimed frontier;
7. continue without repeating established questions.

## Completion invariant

A task may enter `DONE` only when:

- every in-scope work package is `DONE`;
- execution status is `COMPLETED`;
- Standards, Spec, and Evidence are all `PASS`;
- security status is `PASS`;
- no human gate or active blocker remains;
- the final handoff and acceptance report exist.

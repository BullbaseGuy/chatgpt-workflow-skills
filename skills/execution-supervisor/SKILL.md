---
name: execution-supervisor
description: Continuously supervise an approved task through GitHub Actions, preserving checkpoints, monitoring heartbeat, diagnosing failures before retry, and stopping only at completion or a real human/terminal boundary.
---

# Execution Supervisor

## Triggers

Invoke when canonical state has an executable frontier, when a run/progress URL is supplied, or
after `durable-handoff` verifies that work should continue.

## Inputs

- repository, branch, canonical state, dependency graph, handoff, and current plans;
- GitHub PR, Checks, workflow runs, logs, artifacts, and executor configuration;
- applicable retry and quality-gate policies.

## Process

1. **Resolve and verify state.** Read canonical state, then compare branch, PR, run, and artifact reality.
2. **Validate the frontier.** Recompute it; never trust a stale list.
3. **Select work.** Choose the highest-priority unclaimed frontier packages up to the declared
   parallelism limit. Do not select DONE packages.
4. **Claim and prepare.** Mark packages RUNNING, confirm their plans predate implementation, and
   ensure deterministic executor inputs are pinned and secret-safe.
5. **Dispatch or continue the Executor.** GitHub Actions runs commands; the Supervisor does not
   pretend prose is execution.
6. **Monitor useful signals.** Read run status, current step, heartbeat/progress counter, completed
   units, and latest artifact. A long duration alone is not failure.
7. **Classify the outcome.**
   - progress/heartbeat continues → keep RUNNING;
   - job succeeds → run package gate, persist result/checkpoint, unlock new frontier;
   - failure appears → record failure and invoke `diagnose-before-retry`;
   - no progress plus stale heartbeat → inspect logs and runner state before declaring stall;
   - eligible human boundary → finish independent frontier work, then persist HUMAN_GATE.
8. **Continue automatically.** After every passing package, recompute frontier and start the next
   work without asking the user to continue.
9. **Approach completion.** When no in-scope package remains, set VERIFYING and invoke
   `acceptance-review`.
10. **Refresh handoff** after a checkpoint, blocker, interruption, or completion.

## Completion criteria

The invocation ends in exactly one evidence-backed condition:

- active runs are correctly identified and canonical state is current;
- the next frontier package has been dispatched/continued;
- a failure has been routed to diagnosis with no blind rerun;
- a valid human gate or terminal failure is persisted;
- all packages are complete and acceptance review has begun or passed.

It must never end merely because a stage boundary was reached.

## Failure paths

- **State differs from GitHub reality:** reconcile through resume/state review before dispatch.
- **Workflow missing or invalid:** deterministic product failure; diagnose before retry.
- **Transient runner/service failure:** apply the bounded retry policy without rerunning completed units.
- **Retry budget exhausted:** persist `RESOURCE_EXHAUSTED` and eligible human/terminal boundary.
- **Untrusted PR requires secrets:** `SECURITY_BLOCKED`; do not expose secrets.
- **Optional CLI unavailable:** use the GitHub connector when it can complete the operation.

## Output contract

Progress summary includes current package/run, heartbeat/progress evidence, latest checkpoint,
failure class if any, new frontier, and next automatic action.

Persistent outputs update `task_state.yaml`, `HANDOFF.md`, package result, failure record, and
evidence index as applicable.

## Context pointers

- `references/USER_OPERATING_CONTRACT.md`
- `references/TASK_STATE_SCHEMA.md`
- `references/FAILURE_TAXONOMY.md`
- `references/QUALITY_GATES.md`
- `references/OUTPUT_CONTRACT.md`

---
name: acceptance-review
description: Review a branch, task, or claimed completion against independent Standards, Spec, and Evidence axes, then verify security and fresh-session resumability before allowing DONE.
---

# Acceptance Review

## Triggers

Invoke when the user asks whether work is truly complete or correct, before a task enters `DONE`,
before merge/finalization, after a claimed fix, or when GitHub reality and canonical state disagree.

## Inputs

- fixed comparison point and reviewed branch/commit/PR;
- originating specification, work-package plans/results, glossary, ADRs, and repository standards;
- diff/commits, commands, Checks, logs, artifacts, failure records, and evidence JSONL;
- canonical state and handoff;
- `templates/ACCEPTANCE_REPORT.template.md`.

## Process

1. **Pin the review boundary.** Resolve base/fixed point and head; verify the diff and commit list.
2. **Resolve the specification source.** Prefer the task spec and plans, then linked Issue/PR
   requirements. Missing spec is a Spec-axis finding, not permission to invent one.
3. **Resolve standards sources.** Read repository contracts, contribution/coding rules, ADRs,
   schemas, security constraints, and applicable structural baselines.
4. **Validate evidence first.** Parse claim records, commands, run results, source provenance,
   failures, and result files. A completion assertion without actual evidence is an Evidence failure.
5. **Run three independent passes.** Keep findings separate:
   - **Standards:** rule compliance, maintainability, state/schema integrity, and prohibited patterns;
   - **Spec:** missing/partial requirements, incorrect behavior, scope creep, and exclusions;
   - **Evidence:** actual execution, source/fixture coverage, provenance, and unsupported claims.
6. **Run Security and Resume passes.**
   - Security checks secrets, permissions, untrusted execution, pinned dependencies, and model policy.
   - Resume simulates a fresh session resolving the task and exact next action from repository state.
7. **Do not let one axis mask another.** Report findings under their native axis; do not average or
   collapse them into a vague confidence score.
8. **Compute the overall verdict** using `references/QUALITY_GATES.md`.
9. **Update canonical state.**
   - all required passes and no blocker → `DONE`/`COMPLETED`;
   - fixable finding → return affected package to a non-DONE state and route appropriately;
   - approved explicit gap → `PASS_WITH_GAPS`, never silently equivalent to DONE;
   - security finding → `SECURITY_BLOCKED`.
10. **Write the acceptance report and refresh handoff.**

## Completion criteria

- base/head and spec sources are pinned;
- Standards, Spec, and Evidence each have an explicit independent verdict and supporting evidence;
- Security and Resume verdicts are explicit;
- every finding identifies its axis, location, impact, and required action;
- overall verdict follows deterministic gate rules;
- canonical state matches the verdict;
- a PASS completion has no blocker, human gate, hidden gap, or nonzero unauthorized model use.

## Failure paths

- **Empty or invalid review boundary:** stop and resolve the correct fixed point.
- **No specification:** fail or hold the Spec axis unless scope is intentionally defined elsewhere.
- **Evidence unavailable:** fail/hold Evidence; do not infer a pass from code shape.
- **Remote checks still running:** remain VERIFYING; long duration is not failure.
- **State/remote disagreement:** fail Resume until reconciled.
- **Security finding:** immediately mark `SECURITY_BLOCKED`.
- **Approved gap:** document authority and impact; do not label the task fully DONE unless the spec
  explicitly defines the gap as acceptable completion.

## Output contract

Primary artifact:

`docs/implementation/<task_id>/ACCEPTANCE_REPORT.md`

The visible summary lists each axis verdict separately, the worst finding within each axis, overall
status, exact state transition, and next action.

## Context pointers

- `references/QUALITY_GATES.md`
- `references/EVIDENCE_SCHEMA.md`
- `references/TASK_STATE_SCHEMA.md`
- `references/USER_OPERATING_CONTRACT.md`
- `templates/ACCEPTANCE_REPORT.template.md`

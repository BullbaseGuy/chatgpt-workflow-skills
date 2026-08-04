---
name: workflow-router
description: Route ChatGPT Web work to the correct Bullbase skill sequence. Use when a request starts, resumes, reports a failure, asks for research/review/setup, or references a task, Issue, PR, commit, or Actions run.
---

# Workflow Router

## Triggers

Invoke for every engineering-workflow request unless the user explicitly selects another skill.
It is especially required for:

- “先规划 / 制订 plan / 形成规格”;
- “开始执行 / 确认执行”;
- “继续执行 / 检查进度 / 从这里恢复”;
- “报错 / 失败 / 卡住 / 为什么这么慢”;
- research, acceptance review, manual setup, or architecture review;
- a bare task ID, Issue, PR, commit, branch, or Actions URL.

## Inputs

- current user request and current-conversation facts;
- any explicit repository, task, Issue, PR, commit, branch, file, or Actions reference;
- repository `AGENTS.md`, `CONTEXT.md`, active-task index, canonical state, and handoff when present.

## Process

1. **Resolve before classifying.** Follow explicit GitHub references and read canonical state.
   Do not ask for a repository or fact that the request or connected data can resolve.
2. **Classify the leading intent** in this precedence order:
   1. resume/progress reference → `durable-handoff`, then `execution-supervisor`;
   2. observed failure or bad performance → `diagnose-before-retry`;
   3. unavoidable manual configuration → `manual-wizard-powershell`;
   4. review/verification/completion claim → `acceptance-review`;
   5. external or primary-source investigation → `evidence-research`;
   6. architecture-health request → `architecture-review`;
   7. new or changed work → `task-to-spec`, then `frontier-planner`;
   8. approved, already-specified frontier → `execution-supervisor`.
3. **Select decision mode** by reading `references/DECISION_POLICY.md`.
4. **Emit one primary route** and only the necessary downstream sequence. Do not run every skill.
5. **Persist task-bearing routes** in canonical state or the task handoff.
6. **Continue immediately** in `AUTO`. In `APPROVAL`, present the currently decidable frontier
   once. Create a human gate only when the policy permits it.

## Completion criteria

- the referenced repository/task is resolved;
- exactly one primary skill is selected;
- downstream skills are ordered and minimal;
- decision mode is explicit;
- no established fact is re-asked;
- the selected skill has been invoked or the route is persisted as the exact next action.

## Failure paths

- **Reference cannot be resolved:** search connected GitHub data and active tasks; only then
  create a `SPEC_AMBIGUITY` gate if multiple materially different targets remain.
- **Optional local tool missing:** use an available connector; this is not a human gate.
- **Repository permission missing:** create `HUMAN_GATE/PERMISSION`.
- **Conflicting task states:** route to `acceptance-review` state/resume axis before execution.

## Output contract

For a visible route summary, report:

```yaml
primary_skill: durable-handoff
sequence: [durable-handoff, execution-supervisor]
decision_mode: AUTO
resolved_target: owner/repo#task-or-run
reason: Existing task reference requires verified resume
```

Then act; do not stop after merely describing the route.

## Context pointers

- `references/USER_OPERATING_CONTRACT.md`
- `references/DECISION_POLICY.md`
- `references/TASK_STATE_SCHEMA.md`
- `references/OUTPUT_CONTRACT.md`

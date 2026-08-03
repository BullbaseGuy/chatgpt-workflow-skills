---
name: task-to-spec
description: Synthesize an engineering request and all established conversation/repository facts into a durable task specification without repeating resolved questions.
---

# Task to Spec

## Triggers

Invoke when the user asks to plan, build, change, automate, or formalize work that is not yet
represented by an adequate durable specification.

Do not invoke merely to resume an existing adequately specified task.

## Inputs

- user request and all established conversation decisions;
- repository contract, glossary, ADRs, current code/docs, Issues/PRs, and existing task state;
- any supplied logs, fixtures, screenshots, data, or source references;
- `templates/SPEC.template.md`.

## Process

1. **Gather existing facts first.** Read the request, relevant connected files, current branch,
   task state, handoff, code, glossary, ADRs, Issues, PRs, and run evidence.
2. **Separate facts from decisions and gaps.** Never convert a missing fact into an assumption.
3. **Resolve terminology.** Use `CONTEXT.md`; update it only when a domain term is genuinely
   clarified. Implementation details do not belong there.
4. **Respect durable decisions.** Do not re-litigate applicable ADRs. Propose a new ADR only when
   the choice is hard to reverse, surprising without context, and the product of a real trade-off.
5. **Define destination, scope, exclusions, users, interfaces, and constraints.**
6. **Choose verification seams.** Prefer the highest public seam that proves user-visible behavior.
   Data/research work may use fixtures, invariants, reconciliations, or source evidence rather than TDD.
7. **Apply decision mode.**
   - `AUTO`: use documented defaults for low-risk reversible gaps and record load-bearing choices.
   - `APPROVAL`: present all currently decidable material choices in one round with recommendations.
   - `HUMAN_GATE`: only when `DECISION_POLICY` permits.
8. **Write the specification** from `templates/SPEC.template.md` to the task directory.
9. **Create or update canonical state** with task identity, destination, and the next stage.
10. **Route to `frontier-planner`** when the specification gate passes.

## Completion criteria

- the durable spec exists and passes the plan gate in `references/QUALITY_GATES.md`;
- every requirement is in scope, out of scope, or explicitly unresolved;
- established facts and decisions are not re-asked;
- verification seams and evidence needs are explicit;
- security/privacy and human-gate implications are explicit;
- canonical state points to the spec and next action.

## Failure paths

- **Material ambiguity with no approved default:** use `APPROVAL` or eligible human gate.
- **Missing accessible source:** route to `evidence-research`; keep the spec non-DONE.
- **Contradictory code and stated behavior:** record both and require a decision; do not silently choose.
- **No repository yet:** produce the spec in the designated target repository or task bootstrap path.

## Output contract

Primary artifact:

`docs/implementation/<task_id>/SPEC.md`

Visible summary includes destination, main scope, key defaults, verification seams, explicit gaps,
and exact next skill.

## Context pointers

- `references/USER_OPERATING_CONTRACT.md`
- `references/DECISION_POLICY.md`
- `references/QUALITY_GATES.md`
- `references/EVIDENCE_SCHEMA.md`
- `templates/SPEC.template.md`

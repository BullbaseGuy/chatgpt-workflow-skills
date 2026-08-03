---
name: frontier-planner
description: Break an approved specification into independently verifiable vertical work packages, declare real blocking edges, compute the executable frontier, and persist it in canonical state.
---

# Frontier Planner

## Triggers

Invoke after `task-to-spec` passes its plan gate, or when an existing task needs to be re-sliced
because packages are too large, horizontally layered, cyclic, or unnecessarily serialized.

## Inputs

- approved `SPEC.md` or equivalent durable task contract;
- repository glossary, ADRs, architecture, tests, and current state;
- existing dependency graph and completed checkpoints;
- project parallelism and executor constraints.

## Process

1. **Verify the specification gate.** Do not plan around an unresolved destination.
2. **Explore the current system.** Identify public verification seams, reusable code, and
   prefactoring that makes later changes safer.
3. **Draft vertical tracer bullets.** Each work package:
   - delivers a narrow complete behavior through all required layers;
   - is independently demonstrable or verifiable;
   - fits one fresh agent context;
   - has explicit inputs, outputs, gate, and evidence;
   - preserves prior checkpoints.
4. **Handle wide mechanical refactors separately.** Use expand → migrate batches → contract when
   no single vertical slice can remain green.
5. **Declare blocking edges.** Add only dependencies that genuinely prevent safe start. Never use
   numbering order as an implicit dependency.
6. **Check the graph.** Reject cycles, orphaned references, duplicated package IDs, and a package
   blocked by work already outside scope.
7. **Compute the frontier** according to `references/TASK_STATE_SCHEMA.md`.
8. **Apply decision mode.**
   - `AUTO`: accept the recommended granularity and continue.
   - `APPROVAL`: show all packages and blocking edges in one round.
   - `HUMAN_GATE`: only for an eligible material decision.
9. **Persist** `dependency_graph.yaml`, package records, plans, frontier, and parallelism.
10. **Route to `execution-supervisor`.**

## Completion criteria

- every in-scope requirement maps to at least one package;
- every package is a vertical, independently verifiable slice or a justified expand/migrate/contract step;
- graph is acyclic and all blockers exist;
- completed work remains DONE and is not reintroduced;
- frontier is deterministic and non-empty unless the task is ready for acceptance;
- each frontier package has a plan path and verification gate;
- canonical state and dependency graph agree.

## Failure paths

- **Cycle:** stop planning, surface the exact cycle, remove false dependencies or split a package.
- **Package exceeds one context:** split by independently observable behavior.
- **No valid vertical seam:** create a prefactoring package first and record why.
- **Material scope ambiguity:** return to `task-to-spec` under the current decision mode.
- **No frontier but task incomplete:** state is inconsistent; route to `acceptance-review` resume axis.

## Output contract

Artifacts:

- `docs/implementation/<task_id>/dependency_graph.yaml`
- updated `task_state.yaml`
- one `Wxx_plan.md` per package before implementation

Visible summary reports package count, frontier, real blockers, allowed parallelism, and exact next
execution action.

## Context pointers

- `references/TASK_STATE_SCHEMA.md`
- `references/DECISION_POLICY.md`
- `references/QUALITY_GATES.md`
- `references/OUTPUT_CONTRACT.md`

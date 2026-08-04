# Conflict Reconciliation

| Conflict | Resolution | Enforcement surface |
|---|---|---|
| Upstream grilling stops for one decision at a time; user expects continuous execution. | Introduce `AUTO`, `APPROVAL`, and `HUMAN_GATE`. Default is `AUTO`. | `references/DECISION_POLICY.md`, `workflow-router`. |
| Upstream handoff is temporary; user requires cross-chat recovery. | Persist `HANDOFF.md` beside canonical task state. | `durable-handoff`, state validator. |
| Some upstream skills assume background agents. | Run now in ChatGPT Web, delegate deterministic jobs to Actions, or record explicit unresolved work; never promise background delivery. | `USER_OPERATING_CONTRACT`, every skill failure path. |
| Upstream wizard is Bash-based. | Provide PowerShell 7 scripts and Windows-friendly instructions. | `manual-wizard-powershell`. |
| TDD is not a universal fit for data and research. | Select the tightest valid feedback loop: test, fixture, CLI diff, invariant, source reconciliation, browser harness, or controlled HITL. | `diagnose-before-retry`, `QUALITY_GATES`. |
| Issue tracker can be treated as task state. | Issues/PRs are request and collaboration surfaces; `task_state.yaml` remains canonical. | State schema and scaffold integration. |
| Linear plans can freeze behind one blocker. | Model explicit blocking edges and execute the unblocked frontier. | `frontier-planner`, dependency validator. |
| Automatic continuation can hide dangerous actions. | Push checkpoints right, but stop for permissions, secrets, irreversible changes, major business/investment decisions, or material source conflicts. | `DECISION_POLICY`, `HUMAN_GATE` template. |
| User rejects blind retries. | A retry requires a failure class, new evidence, and a bounded retry policy. | `FAILURE_TAXONOMY`, `diagnose-before-retry`. |
| User requires Codex count 0. | No model-execution job or secret is required; validators fail if enabled surfaces are introduced without an explicit ADR and task decision. | `USER_OPERATING_CONTRACT`, CI checks. |
| User rejects Gmail connection prompts. | No email connector or external email dependency is part of the workflow. | Repository search validator and operating contract. |
| Repeated prompt text causes drift. | Shared behavior lives once in `references/`; skills only point to it. | Reference-integrity validator. |
| Completion claims have been made without real validation. | `DONE` requires separate Standards, Spec, and Evidence verdicts. | `acceptance-review`, task-state schema. |

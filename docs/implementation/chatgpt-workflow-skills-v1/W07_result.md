# W07 Result — PASS

## Delivered

- Added seven executable historical workflow scenario manifests.
- Added a deterministic policy regression engine and aggregate runner.
- Pinned an expected-results snapshot to detect semantic drift.
- Added mutation tests proving the suite catches repeated questions, blind reruns, and incorrect human gates.
- Added the aggregate regression command to the repository validation workflow.

## Scenario coverage

| Scenario | Expected policy outcome | Result |
|---|---|---|
| Long-running Action with heartbeat | Continue monitoring the same run | PASS |
| Completed Action with stale task state | Reconcile existing outputs; do not rerun | PASS |
| x_scrap cursor plus HTTP 429 | Diagnose and resume from checkpoint with changed variable | PASS |
| Bark background/duplicate notification | Automate browser harness, then one real-device gate | PASS |
| Material F10 source conflict | Preserve conflict and request a decision-ready gate | PASS |
| Pine compile/UI contract mismatch | Reject premature completion and require UI acceptance | PASS |
| Fresh session with task_id only | Resolve canonical state and continue from frontier | PASS |

## Gate evidence

- `python scripts/run_regression_scenarios.py`: 7/7 PASS and snapshot match.
- `python -m unittest tests.test_regression -v`: 4/4 PASS.
- Evidence: `evidence/W07-local-validation.txt`.
- CI entry: `.github/workflows/validate.yml`.
- Codex/model invocation count: `0`.

## Decision

W07 is complete. Continue automatically to W08.

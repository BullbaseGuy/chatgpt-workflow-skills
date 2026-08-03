# W07 Plan — Historical Scenario Regression

## Objective
Turn seven real historical failure patterns into executable policy regressions.

## Outputs
- Seven scenario manifests under `tests/scenarios/`
- regression runner
- expected-results snapshot
- W07 result/state updates

## Gate
Every scenario must assert no repeated questions, no blind rerun, no premature DONE,
correct human gating, evidence retention, and resumability. All scenarios must pass locally.

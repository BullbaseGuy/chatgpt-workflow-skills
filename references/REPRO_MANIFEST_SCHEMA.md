# Reproduction Manifest Schema

A reproduction manifest is the machine-checkable gate between a failure report and repair/retry.

## Required YAML shape

```yaml
schema_version: 1.0.0
failure_id: FAIL-0001
failure_class: DETERMINISTIC_PRODUCT
exact_symptom: Exact observable user symptom
original_invocation: command or run URL
checkpoints_preserved: [W00]
feedback_loop:
  invocation: python -m unittest tests.test_bug
  assertion: Exact behavior that goes red
  red_observed: true
  red_output: concise non-secret excerpt or artifact pointer
  deterministic: true
  typical_runtime_seconds: 2.5
  agent_runnable: true
reproduction:
  minimized: true
  load_bearing_elements: [fixture, option]
hypotheses:
  - rank: 1
    cause: candidate cause
    prediction: If cause is true, probe will produce result
    probe: one-variable probe
fix:
  applied: true
  regression_green: true
  original_scenario_green: true
  debug_cleanup_complete: true
retry:
  requested: false
  changed_variable: null
  attempts_used: 0
  budget: 0
```

## Validation rules

- `red_observed`, `deterministic`, and `agent_runnable` must be true before fix/retry.
- Runtime must be positive. “Fast enough” is task-dependent; the value must be measured.
- Minimized reproductions list at least one load-bearing element.
- Hypotheses count is 3–5, ranks are unique, and every item has cause, prediction, and probe.
- A completed fix requires regression, original scenario, and cleanup all true.
- A requested retry requires a non-empty `changed_variable`, remaining budget, and a retryable
  class under `references/FAILURE_TAXONOMY.md`.
- Commands and outputs must not contain secrets.

## Distinction

A manifest proves diagnostic readiness. It does not by itself prove task acceptance; that remains
the responsibility of `acceptance-review`.

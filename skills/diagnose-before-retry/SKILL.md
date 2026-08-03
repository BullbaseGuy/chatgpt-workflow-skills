---
name: diagnose-before-retry
description: Diagnose hard bugs, regressions, stalls, upstream changes, and repeated failures by establishing a tight red-capable feedback loop before hypotheses, fixes, or reruns.
---

# Diagnose Before Retry

## Triggers

Invoke when the user reports broken, failing, wrong, slow, stalled, flaky, rate-limited, or
upstream-changed behavior; when a GitHub Actions run fails; or before repeating a prior failed run.

## Inputs

- exact user-observed symptom and expected behavior;
- failing command, run, log, artifact, trace, fixture, or environment;
- relevant code, state, prior failure records, retry attempts, and successful checkpoints;
- the failure taxonomy and repro-manifest schema.

## Process

1. **Record and classify the failure.** Assign a failure ID, capture the exact symptom, command/run,
   first observed UTC, failure class, retry budget, and preserved checkpoints.
2. **Build the tight feedback loop before theory.** Prefer, in order:
   failing test; CLI/HTTP invocation; fixture/snapshot diff; browser harness; trace replay;
   minimal throwaway harness; property/fuzz loop; automated bisection; differential old/new loop;
   structured human loop only as a last resort.
3. **Prove the loop is red-capable.** Run it at least once. It must assert the user's exact symptom,
   be deterministic enough, fast enough for iteration, and agent-runnable.
4. **Reproduce and minimize.** Remove one input, caller, config, data item, or step at a time until
   every remaining element is load-bearing.
5. **Rank 3–5 falsifiable hypotheses.** For each: “If X is the cause, changing/probing Y predicts Z.”
   Persist and surface the ranked list; in `AUTO`, continue without waiting.
6. **Instrument one prediction at a time.** Prefer debugger/inspection, then targeted uniquely tagged
   logs. Performance work establishes measurements before changes.
7. **Write the regression protection at the highest valid seam.** If no valid seam exists, record
   that architectural limitation instead of writing a misleading shallow test.
8. **Apply the smallest causal fix.**
9. **Verify green twice.** Run the regression and the original unminimized scenario.
10. **Clean up.** Remove tagged logs and throwaway assets; state the confirmed hypothesis/root cause.
11. **Decide retry.** A retry is permitted only under `FAILURE_TAXONOMY` and only when a predicted
    material variable changed. Preserve completed checkpoints.
12. **Update state, failure record, evidence, result, and handoff.** Route architecture limitations
    to `architecture-review` after the immediate failure is fixed.

## Completion criteria

- failure is classified and persisted;
- one invocation has actually demonstrated the exact red symptom;
- reproduction is minimized or the inability to minimize is explicitly evidenced;
- 3–5 hypotheses are ranked and falsifiable;
- probes map to predictions;
- causal fix or non-fix conclusion is documented;
- regression and original scenario are green, or a valid human/terminal boundary exists;
- temporary instrumentation is removed;
- any retry is non-blind, bounded, and checkpoint-preserving.

## Failure paths

- **Cannot build a red-capable loop:** list attempted loops and request only the missing environment,
  trace, artifact, or production instrumentation through an eligible human gate.
- **Flaky issue:** increase reproduction rate through repetition, stress, seed/time control, or
  narrowed timing windows before theorizing.
- **No correct test seam:** fix with the best original-scenario loop, record the gap, and route an
  architecture follow-up.
- **Security or permission boundary:** do not probe around controls; persist the correct gate.
- **Retry budget exhausted:** mark `RESOURCE_EXHAUSTED`; no further automatic run.

## Output contract

Persistent artifacts:

- `docs/implementation/<task_id>/failures/<failure_id>.md`
- optional `repro/<failure_id>/repro-manifest.yaml`
- regression test/fixture and evidence records
- updated canonical state and handoff

Visible updates lead with the exact reproduced symptom, then the ranked hypotheses/root cause,
verification, and next state. Do not present an untested theory as diagnosis.

## Context pointers

- `references/FAILURE_TAXONOMY.md`
- `references/REPRO_MANIFEST_SCHEMA.md`
- `references/QUALITY_GATES.md`
- `references/EVIDENCE_SCHEMA.md`
- `templates/FAILURE.template.md`

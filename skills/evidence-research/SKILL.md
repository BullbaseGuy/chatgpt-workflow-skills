---
name: evidence-research
description: Investigate engineering, data, or investment questions against high-trust sources and persist claim-level evidence without collapsing facts, inferences, estimates, non-disclosure, or source conflicts.
---

# Evidence Research

## Triggers

Invoke when a task depends on external documentation, source code, first-party APIs, filings,
datasets, current platform behavior, or any material fact not already verified in repository evidence.

Also invoke when another skill identifies a source gap, a source conflict, or a claim that needs
primary-source support.

## Inputs

- a precise research question and the decision or work package it blocks;
- repository glossary, ADRs, specification, existing evidence, and as-of date;
- accessible official documents, source repositories, specifications, first-party APIs, filings,
  datasets, and user-supplied artifacts;
- `references/EVIDENCE_SCHEMA.md`.

## Process

1. **Define the claim boundary.** State what must be learned, the decision it informs, the as-of
   time, and what would count as sufficient evidence.
2. **Inventory existing evidence.** Reuse claim IDs and records; do not re-research verified facts
   unless freshness, conflict, or provenance requires it.
3. **Use the source hierarchy.** Start with official specifications, filings, source code,
   repository state, signed releases, and first-party documentation/APIs. Secondary sources may
   discover leads but cannot silently override higher-tier evidence.
4. **Capture provenance while reading.** For each material claim record source, immutable revision
   or date, exact page/line/cell/run location, capture method, and integrity pointer.
5. **Classify every claim.** Keep `FACT`, `INFERENCE`, `ESTIMATE`, `NOT_DISCLOSED`,
   `SOURCE_CONFLICT`, `TEST_RESULT`, and `EXECUTION_EVENT` distinct.
6. **Reconcile rather than average conflicts.** Compare definitions, periods, revisions, units,
   authority, and calculation methods. If unresolved, persist `SOURCE_CONFLICT`.
7. **Record absence honestly.** A documented search that finds no disclosure becomes
   `NOT_DISCLOSED`, never zero or an invented precise value.
8. **State reasoning explicitly.** An inference cites supporting evidence IDs and explains the
   reasoning. An estimate declares assumptions and sensitivity.
9. **Protect sensitive material.** Record presence/location/verdict only; never persist a secret or
   a reversible/guessable derivative.
10. **Append evidence records** to the task evidence JSONL and write a concise research note linking
    records rather than duplicating source text.
11. **Validate the evidence file.** Resolve validation errors before using a claim in acceptance.
12. **Route the result.** Return supported decisions to the invoking skill; route material unresolved
    conflicts to the decision policy, and inaccessible required sources to an eligible human gate.

## Completion criteria

- the research question and as-of date are explicit;
- every material conclusion has one or more valid evidence records;
- source tier, immutable location, capture method, confidence, and sensitivity are present;
- facts, inference, estimates, absence, and conflicts remain separate;
- no lower-tier source silently overrides a higher-tier source;
- unresolved gaps and conflicts are explicit;
- evidence validation passes;
- the invoking task/state is updated with the result or blocker.

## Failure paths

- **Required source inaccessible:** record attempted access and create only the minimum eligible
  permission/artifact human gate.
- **Source changed since capture:** pin the new revision and retain the prior record; do not mutate
  history.
- **Material conflict persists:** record both sides and route under `DECISION_POLICY`.
- **Only secondary evidence exists:** classify confidence accordingly and do not claim primary
  confirmation.
- **Sensitive source:** capture metadata and verdict only; never copy the value.
- **No evidence found:** use `NOT_DISCLOSED` or an explicit research gap, not a fabricated answer.

## Output contract

Persistent outputs:

- `docs/implementation/<task_id>/evidence.jsonl`;
- optional `docs/implementation/<task_id>/research/<slug>.md`;
- updated state/handoff when the result changes execution.

The visible summary distinguishes verified facts, inferences, estimates, missing disclosure,
conflicts, and exact next action.

## Context pointers

- `references/EVIDENCE_SCHEMA.md`
- `references/DECISION_POLICY.md`
- `references/QUALITY_GATES.md`
- `references/OUTPUT_CONTRACT.md`

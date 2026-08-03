---
name: architecture-review
description: Review evidence-backed architectural friction in code that is changing or hard to verify, propose deepening candidates, and route only the selected candidate through specification and frontier planning.
---

# Architecture Review

## Triggers

Invoke when the user asks for architecture improvement, when repeated failures expose weak test
seams or hidden coupling, or when change history shows a hot area whose complexity is slowing work.

Do not invoke as a generic style audit with no observed friction or expected future work.

## Inputs

- user-named subsystem or recent commit history used to identify hot spots;
- `CONTEXT.md`, applicable ADRs, specification, failure records, tests, and package boundaries;
- call/dependency paths and concrete examples of difficult changes or verification;
- `templates/ARCHITECTURE_REVIEW.template.md`.

## Process

1. **Scope before scanning.** Prefer a user-named area. Otherwise use recent change history,
   diagnosed failures, and repeated edits to choose a justified hot spot.
2. **Read domain and decisions first.** Use canonical glossary terms and do not silently re-litigate
   applicable ADRs.
3. **Collect friction evidence.** Record where understanding requires bouncing across modules, where
   interfaces expose implementation complexity, where tests cannot reach real behavior, where
   coupling leaks, or where one change causes shotgun edits.
4. **Apply the deletion test.** A candidate is valuable only when removing the proposed boundary
   would concentrate complexity rather than merely move it.
5. **Draft a small candidate set.** Each candidate includes affected modules, observed evidence,
   current seam, proposed deeper module/interface, locality/leverage gains, before/after flow,
   verification seam, migration risk, and recommendation strength.
6. **Check ADR conflicts.** Surface a conflict only when observed friction is strong enough to
   justify reopening the decision.
7. **Rank without implementing.** Recommend the highest-evidence candidate. Mark speculative
   candidates explicitly.
8. **Apply decision mode.** In `AUTO`, architecture review may diagnose and recommend, but it must
   not perform an unplanned refactor. A selected candidate routes to `task-to-spec`, then
   `frontier-planner`.
9. **Persist the report** and link supporting evidence/failure IDs.
10. **Update handoff** only when the recommendation becomes planned work or resolves an active
    architecture blocker.

## Completion criteria

- scope is justified by user direction, change history, or diagnosed friction;
- every candidate cites concrete evidence rather than taste;
- the domain vocabulary and ADRs are respected;
- each candidate defines a proposed seam and how behavior would be verified through it;
- recommendation strength and migration risk are explicit;
- the review changes no production code;
- selected work is routed through a durable specification and plan.

## Failure paths

- **No demonstrated friction or likely future change:** report that no architecture investment is
  justified now.
- **Insufficient code/history access:** request only the missing repository/trace permission.
- **Candidate contradicts a load-bearing ADR:** show the evidence and require the appropriate
  decision mode before changing it.
- **Immediate production failure still open:** return to `diagnose-before-retry`; do not substitute
  refactoring for a causal fix.
- **No valid seam can be described:** record the uncertainty and prototype/research it before a spec.

## Output contract

Primary artifact:

`docs/architecture/architecture-review-<UTC timestamp>.md`

Optional visual HTML may be emitted as a non-canonical artifact. The Markdown report remains the
durable source and follows `templates/ARCHITECTURE_REVIEW.template.md`.

## Context pointers

- `references/USER_OPERATING_CONTRACT.md`
- `references/EVIDENCE_SCHEMA.md`
- `references/DECISION_POLICY.md`
- `references/QUALITY_GATES.md`
- `templates/ARCHITECTURE_REVIEW.template.md`

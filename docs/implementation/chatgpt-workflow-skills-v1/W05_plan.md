# W05 Plan — Evidence Research, Architecture Review, and Three-Axis Acceptance

## Objective
Implement primary-source evidence research, evidence-backed architecture review, and independent
Standards / Spec / Evidence verdicts. This stage also closes the previously unassigned P1
`architecture-review` requirement before implementation begins.

## Outputs
- `skills/evidence-research/SKILL.md`
- `skills/architecture-review/SKILL.md`
- `skills/acceptance-review/SKILL.md`
- evidence record validator and examples
- acceptance report validator and fixtures
- architecture candidate template/example
- W05 result/state updates

## Work
1. Enforce primary-source hierarchy and explicit FACT / INFERENCE / ESTIMATE /
   NOT_DISCLOSED / SOURCE_CONFLICT classifications.
2. Persist append-only evidence records with stable source location, as-of date, capture method,
   integrity pointer, confidence, and sensitivity.
3. Scan architecture only where change history or diagnosed friction makes investment justified;
   produce evidence-backed deepening candidates without changing code automatically.
4. Review Standards, Spec, and Evidence independently, then security and resume readiness.
5. Reject DONE when any required axis fails or when an unapproved gap remains.

## Gate
Claims must be traceable to source locations and types; classifications must remain distinct;
architecture findings must cite observed friction rather than speculative style preferences;
DONE requires Standards, Spec, and Evidence all PASS, security PASS, and resume PASS.

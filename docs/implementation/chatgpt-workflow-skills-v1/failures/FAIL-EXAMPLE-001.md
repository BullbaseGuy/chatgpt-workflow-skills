# Failure FAIL-EXAMPLE-001

## Exact symptom
`python scripts/validate_skills.py` reported that every valid skill lacked a frontmatter name.

## Classification
`DETERMINISTIC_PRODUCT`; automatic retry budget was zero until diagnosis.

## Tight feedback loop
The validator itself was a sub-second deterministic red/green loop and asserted the exact symptom.

## Minimized reproduction
One valid `SKILL.md` and the raw regex containing double-escaped `\\s`/`\\n` were sufficient.

## Ranked hypotheses and probe
The highest-ranked hypothesis predicted that replacing raw-string double escapes with regex escapes
would match the name/description lines. Direct pattern comparison confirmed it. Line endings and
wrong-file selection were falsified.

## Resolution
Corrected the regex, reran structural validation, canonical-state validation, and all unit tests.
The original scenario and regression were green; no debug instrumentation remained.

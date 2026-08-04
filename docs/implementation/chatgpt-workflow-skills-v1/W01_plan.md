# W01 Plan — Terminology, State, Failure, and Decision Model

## Objective
Create the shared rule layer that every skill references instead of duplicating policy.

## Outputs
- Seven files under `references/`
- Five files under `templates/`
- `W01_result.md`
- Updated canonical task state and handoff

## Work
1. Define the user operating contract and decision modes.
2. Define task-state, evidence, quality-gate, failure, and output schemas.
3. Create durable templates for spec, handoff, failure, human gate, and acceptance.
4. Validate YAML examples, required headings, cross-references, secret safety, and Codex=0.

## Gate
PASS only when all twelve artifacts exist, each shared rule has one authority, examples parse,
and W02 is the only frontier item.

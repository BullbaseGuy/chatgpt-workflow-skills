# Output Contract

## Progress updates

A progress update should state:

1. the verified stage reached;
2. the most important finding or risk;
3. what is executing next.

Do not narrate every low-level tool call. Do not promise future background delivery.

## Result reporting

Every completed stage reports:

- delivered artifacts;
- deterministic checks and outcomes;
- unresolved gaps;
- state/frontier transition;
- Codex/model invocation count.

Paths, commits, PRs, runs, and artifacts must be concrete.

## Human gate

Use `templates/HUMAN_GATE.template.md` and include exactly:

- why the user is required;
- what is already complete;
- the minimal exact action;
- how to verify success;
- what work becomes unblocked.

## Failure report

Use `templates/FAILURE.template.md`. Lead with the exact symptom and classification, not a
speculative root cause.

## Final response

The final response should include:

- overall status and acceptance axes;
- repositories, branches, commits, PRs, and checks;
- stage table W00–W09;
- whether any human action remains;
- exact resume entry point;
- Codex/model invocation count.

## Language and readability

Use the user's current language. Prefer complete sentences and compact sections. Preserve exact
identifiers and absolute dates. Distinguish verified facts from inference.

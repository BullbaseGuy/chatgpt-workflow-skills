# W04 Result — PASS

## Delivered
- `diagnose-before-retry`.
- Authoritative reproduction-manifest schema.
- Machine validator and five diagnosis tests.
- Append-only failure index and one real resolved failure record.
- CI validation of the valid reproduction fixture.

## Red-green evidence
The W03 skill validator first failed on valid frontmatter because raw regex tokens were
double-escaped. The exact validator command was a deterministic sub-second loop. The reproduction
was minimized to one valid skill plus the pattern, three hypotheses were ranked, the top prediction
was confirmed, the regex was corrected, and the original command plus all tests passed.

## Policy checks
- No theory or rerun is permitted before an observed red loop.
- 3–5 falsifiable hypotheses are required.
- Blind retry without a changed predicted variable is rejected.
- Bounded transient retry with a documented environmental change is allowed.
- Applied fixes require regression, original-scenario, and cleanup green.

## State transition
W04 is DONE. W05 is READY and the sole frontier item. Codex/model invocation count remains `0`.

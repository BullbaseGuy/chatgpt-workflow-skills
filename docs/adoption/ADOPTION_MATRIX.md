# Upstream Adoption Matrix

Baseline: `mattpocock/skills@2ab958093e83e0ec752e6c1c5932da465bf23e0c`.

| Upstream mechanism or skill | Disposition | Bullbase adaptation |
|---|---|---|
| Small composable skills | ADOPT | One skill per invocation branch; shared rules move to `references/`. |
| `writing-great-skills` | ADAPT | Use single-source rules, completion criteria, progressive disclosure, routers, and pruning; add repository validation. |
| `ask-matt` router | ADAPT | Become `workflow-router`, using the user's Chinese trigger language and task-state recovery. |
| `setup-matt-pocock-skills` | ADAPT | Become installation/bootstrap logic that configures canonical GitHub-backed state and PowerShell-first operation. |
| `to-spec` | ADAPT | Become `task-to-spec`; synthesize existing conversation and repo facts without repeating questions. |
| `to-tickets` tracer bullets | ADAPT | Become `frontier-planner`; preserve Wxx IDs, blocking edges, frontier, checkpoint reuse, and bounded parallelism. |
| `implement` | ADAPT | Split supervision from execution: ChatGPT Web supervises; GitHub Actions executes deterministic commands. |
| `diagnosing-bugs` | ADAPT | Become `diagnose-before-retry`; no retry or theory before a tight, red-capable loop exists. |
| `tdd` | ADAPT | One branch of a broader feedback-loop policy; data/research tasks use fixtures, reconciliations, invariants, or snapshot diffs. |
| `code-review` | ADAPT | Become three-axis `acceptance-review`: Standards, Spec, and Evidence. |
| `research` | ADAPT | Become `evidence-research`; use primary sources and persist cited evidence without claiming unavailable background work. |
| `handoff` | ADAPT | Become `durable-handoff`; store in the task directory, never only in OS temp. |
| `domain-modeling` | ADAPT | Maintain `CONTEXT.md` as glossary only; use ADRs sparingly under the three-part decision test. |
| `wayfinder` | ADAPT | Use decision maps for genuinely foggy, multi-session efforts, then collapse into spec/frontier execution. |
| `improve-codebase-architecture` | ADAPT | Become `architecture-review`; produce evidence-backed candidates and route selected work back through spec/frontier. |
| `wizard` (in progress upstream) | ADAPT | Become stable `manual-wizard-powershell`; PowerShell, idempotent configuration, secret-safe verification. |
| `batch-grill-me` (in progress upstream) | ADAPT | Use frontier-wide decision rounds only in `APPROVAL`; `AUTO` does not stop for reversible defaults. |
| One-question-at-a-time `grilling` | REJECT | Conflicts with low-interruption execution; replaced by `AUTO`, `APPROVAL`, and `HUMAN_GATE`. |
| Temporary-only handoff | REJECT | Conflicts with repository-backed recovery. |
| Mandatory background subagents | REJECT | Work must complete in the current response or be represented explicitly in GitHub state/Actions. |
| Bash-first manual setup | REJECT | Windows PowerShell is the default human surface. |
| Triage of arbitrary external requests | DEFER | Valuable later, but outside the first workflow-skills release. |
| Teaching/content workflows | DEFER | Not part of engineering execution and recovery scope. |

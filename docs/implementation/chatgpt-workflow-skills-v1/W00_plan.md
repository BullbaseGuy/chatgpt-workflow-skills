# W00 Plan — Adoption Matrix, Conflict Reconciliation, and Licensing

- **Task ID:** `chatgpt-workflow-skills-v1`
- **Repository:** `BullbaseGuy/chatgpt-workflow-skills`
- **Decision mode:** `AUTO`
- **Supervisor:** ChatGPT Web
- **Executor:** GitHub Actions
- **Codex/model execution:** disabled; expected invocation count `0`
- **Source baseline:** `mattpocock/skills@2ab958093e83e0ec752e6c1c5932da465bf23e0c`
- **Scaffold baseline:** `BullbaseGuy/demo-project@ff6619b1f0ef6797ad1ca09fffa5db9475dc2482`

## Objective

Establish a traceable adoption baseline before implementation. Classify every borrowed mechanism as `ADOPT`, `ADAPT`, `REJECT`, or `DEFER`; reconcile it with the user's operating constraints; preserve MIT attribution; and create the canonical task state required for W01–W09.

## Inputs

1. The user-approved task contract in the initiating ChatGPT conversation.
2. The current `mattpocock/skills` main branch and MIT license.
3. The current `BullbaseGuy/demo-project` main branch.
4. Existing user operating rules: GitHub-backed state, bounded recovery, no blind reruns, PowerShell-first manual steps, and Codex invocation count `0`.

## Work

1. Record source revisions and license obligations.
2. Produce an adoption matrix for the relevant upstream skills and design mechanisms.
3. Record every conflict with the user's workflow and the selected resolution.
4. Create the repository-level operating contract, glossary, architecture decision record, and canonical task files.
5. Define W00's deterministic gate and evidence.

## Outputs

- `LICENSE`
- `LICENSES/mattpocock-skills-MIT.txt`
- `README.md`
- `AGENTS.md`
- `CONTEXT.md`
- `docs/adr/0001-separate-skills-source-from-project-scaffold.md`
- `docs/adoption/ADOPTION_MATRIX.md`
- `docs/adoption/CONFLICT_RECONCILIATION.md`
- `docs/implementation/ACTIVE_TASKS.yaml`
- `docs/implementation/chatgpt-workflow-skills-v1/task_state.yaml`
- `docs/implementation/chatgpt-workflow-skills-v1/dependency_graph.yaml`
- `docs/implementation/chatgpt-workflow-skills-v1/HANDOFF.md`
- `docs/implementation/chatgpt-workflow-skills-v1/W00_result.md`

## Gate

W00 passes only when:

- every selected upstream mechanism has exactly one adoption disposition;
- every known conflict has a documented resolution;
- MIT attribution is retained;
- `task_state.yaml` identifies W01 as the next frontier item;
- no secret, private endpoint, or model credential appears in tracked content;
- Codex/model invocation count remains `0`.

## Failure handling

- Missing public source content is an `AUTO_RECOVERABLE` research gap and must be retried through the GitHub connector.
- Missing repository write permission is `HUMAN_GATE/PERMISSION`.
- A license conflict is `FAILED_TERMINAL` until resolved; implementation must not copy affected text.

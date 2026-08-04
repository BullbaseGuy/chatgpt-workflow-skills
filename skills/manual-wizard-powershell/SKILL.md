---
name: manual-wizard-powershell
description: Convert unavoidable setup, migration, or third-party configuration into an idempotent PowerShell 7 wizard that opens the right pages, captures values safely, writes only approved destinations, verifies each stage, and creates the smallest possible human gate.
---

# Manual Wizard PowerShell

## Triggers

Invoke when the task genuinely requires a human to sign in, click a control, approve access, copy a
value, configure a third-party service, perform a one-off migration, or validate behavior on a real
device.

Do not invoke when the Supervisor or GitHub Actions can complete the step directly.

## Inputs

- repository and target state;
- current `.env*`, configuration, README/setup docs, and every workflow reference to `secrets.*`
  or `vars.*`;
- exact external UI/documentation paths and required captured values;
- current state, failure records, and applicable human-gate class;
- `templates/manual-wizard.template.ps1` and a reviewed stage manifest.

## Process

1. **Prove manual work is necessary.** Apply `references/DECISION_POLICY.md`. Resolve accessible
   facts and finish every safe independent frontier item first.
2. **Inventory the transition.** Identify current state, target state, every stage, captured value,
   source location, destination, secrecy, verification, rollback, and irreversible action.
3. **Map the user's exact journey.** Use current official documentation or verified UI evidence.
   Never invent menu labels or URLs.
4. **Author a stage manifest.**
   - one focused stage at a time;
   - public and secret values are distinct;
   - secrets may go only to an approved `.env` destination or GitHub Secret, never a GitHub Variable;
   - external commands are program + argument arrays, never shell strings;
   - irreversible stages require an exact confirmation phrase;
   - every value has a verification method that does not reveal it.
5. **Instantiate the PowerShell 7 template.** Keep the safety library intact; customize only the
   manifest/default path and user-facing stage descriptions.
6. **Use secure handling.** `Read-Host -AsSecureString`, temporary in-memory conversion only at the
   destination boundary, zero unmanaged memory, no secret logging, no secret command arguments.
7. **Use idempotent writes.** Upsert `.env` keys, use `gh secret set` through stdin, and use
   `gh variable set` only for public values.
8. **Confirm only irreversible work.** Ordinary stages are resumable and do not ask ceremonial
   confirmation. The wizard records stage completion without secret values.
9. **Validate statically and with fixtures.** Run the manifest and script safety validator. Run
   PowerShell parser/linter when available; absence of local `pwsh` is recorded, not hidden.
10. **Do not run the real wizard for the user.** It opens browsers and requires their identity or
    device. Persist the exact invocation and success criteria in a human gate.
11. **Resume automatically after the minimum success signal.** Re-read repository/service state,
    verify the outcome, clear the gate, and continue the frontier.

## Completion criteria

- manual necessity and gate class are justified;
- every stage, captured value, destination, secrecy flag, and verification is known;
- the manifest validator passes;
- the PowerShell template passes static safety checks and parser/linter checks when available;
- no secret value, hash, private endpoint, or sample credential is persisted;
- env writes are idempotent and GitHub secrets use stdin;
- every irreversible command has an exact confirmation phrase;
- the human gate contains one invocation, exact actions, success evidence, and unblocked work;
- the wizard can be rerun safely after partial completion.

## Failure paths

- **Exact UI path is unknown:** use `evidence-research`; do not guess.
- **No PowerShell 7 on the user's machine:** provide an installation prerequisite as part of the
  same gate; do not switch silently to Bash.
- **`gh` missing or unauthenticated:** include `gh auth status` and the smallest setup step.
- **Secret destination is unsafe:** block the stage and redesign it; never fall back to logging or a
  GitHub Variable.
- **Irreversible step lacks rollback/confirmation:** reject the manifest.
- **Static validation fails:** diagnose the template or manifest before handing it to the user.
- **The operation is automatable after all:** remove the human stage and route it to the Executor.

## Output contract

Persistent outputs:

- `scripts/manual/<wizard-name>.ps1` or another repository-approved path;
- `scripts/manual/<wizard-name>.json`;
- `docs/implementation/<task_id>/human-gates/<gate_id>.md`;
- updated canonical state and handoff.

The visible instruction gives one PowerShell invocation, explains exactly what will happen, and
shows the non-secret success signal.

## Context pointers

- `references/DECISION_POLICY.md`
- `references/USER_OPERATING_CONTRACT.md`
- `references/QUALITY_GATES.md`
- `references/OUTPUT_CONTRACT.md`
- `templates/manual-wizard.template.ps1`
- `templates/HUMAN_GATE.template.md`

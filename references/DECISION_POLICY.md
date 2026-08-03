# Decision Policy

This document is the single authority for `AUTO`, `APPROVAL`, and `HUMAN_GATE`.

## AUTO

Default mode. The Supervisor selects the recommended option and continues when the decision is:

- low risk;
- reversible;
- within declared scope;
- supported by existing facts or a documented default;
- not secret-bearing, permission-gated, destructive, or financially material.

AUTO decisions are recorded only when later work depends on them. Do not pause merely to obtain
ceremonial approval.

## APPROVAL

Use only when the user explicitly asks to see and approve a plan or design before execution.

- Present the whole currently decidable frontier in one round.
- Give a recommended answer for every decision.
- Do not ask for facts that tools or repository evidence can resolve.
- After approval, switch to AUTO unless the user says otherwise.
- A question whose prerequisites are unsettled belongs to a later round.

## HUMAN_GATE

A human gate is allowed only for one of these classes:

1. missing login, permission, credential, organizational approval, or physical access;
2. an irreversible or destructive action;
3. a material business, product, legal, privacy, security, or investment decision;
4. a conflict between authoritative sources that materially changes the outcome and cannot be
   resolved through source hierarchy or scope;
5. experiential acceptance that only the user can judge, such as a real notification on their device;
6. an exhausted, correctly diagnosed retry boundary requiring external intervention.

A preference already recorded in conversation or repository is not a new human gate.

## Push-right procedure

Before creating a human gate:

1. finish every safe and independent frontier item;
2. collect and summarize all evidence;
3. minimize the user action to the smallest exact sequence;
4. state what success looks like;
5. identify which blockers will clear after the action;
6. persist the gate in canonical state and `HANDOFF.md`.

## Decision test

Use this order:

```text
Can evidence resolve it? -> resolve automatically.
Is there an approved default? -> use it in AUTO.
Is it low-risk and reversible? -> choose the recommended option in AUTO.
Did the user request prior approval? -> APPROVAL.
Does it match a HUMAN_GATE class? -> HUMAN_GATE.
Otherwise -> AUTO and record the rationale if load-bearing.
```

## Prohibited pseudo-gates

Do not stop for:

- “Would you like me to continue?”
- a stage boundary with a passing gate;
- a recoverable infrastructure failure still inside retry budget;
- information already present;
- a non-critical blocked branch while other frontier work is available;
- lack of an optional tool when an available connector can complete the task.

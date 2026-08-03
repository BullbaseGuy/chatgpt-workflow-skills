# Failure Taxonomy and Retry Policy

## Failure classes

| Class | Meaning | Default action |
|---|---|---|
| `TRANSIENT_INFRASTRUCTURE` | Temporary network, runner, service, or rate-limit fault with unchanged inputs | Retry with bounded backoff after classification |
| `DETERMINISTIC_PRODUCT` | Reproducible code, schema, logic, or data-processing failure | Diagnose before retry |
| `UPSTREAM_CHANGED` | External interface or payload changed | Capture trace/fixture, diagnose adapter, then verify |
| `SOURCE_CONFLICT` | Authoritative facts disagree | Reconcile or create HUMAN_GATE if material and irresolvable |
| `PERMISSION` | Missing login, role, token, org approval, or environment access | HUMAN_GATE |
| `SECRET_CONFIGURATION` | Required secret absent or invalid | HUMAN_GATE without exposing value |
| `SECURITY` | Scope violation, secret exposure, unsafe permission, untrusted execution | SECURITY_BLOCKED |
| `IRREVERSIBLE` | Next action destroys or permanently changes state | HUMAN_GATE |
| `USER_ACCEPTANCE` | Only real user/device experience can validate behavior | HUMAN_GATE after automation is complete |
| `SPEC_AMBIGUITY` | Material requirement cannot be resolved from existing evidence/defaults | APPROVAL or HUMAN_GATE |
| `RESOURCE_EXHAUSTED` | Correctly diagnosed retry/time/storage budget exhausted | HUMAN_GATE or FAILED_TERMINAL |
| `TERMINAL_INCOMPATIBILITY` | Goal conflicts with platform, license, or hard constraint | FAILED_TERMINAL |

## Retry eligibility

A retry is allowed only when all are true:

1. failure class is retryable;
2. the prior attempt and evidence are recorded;
3. retry budget remains;
4. at least one of time, environment, input, configuration, code, or strategy has changed in a
   way predicted to affect the result;
5. completed checkpoints will not be rerun.

A blind rerun violates item 4.

## Default retry budgets

- transient infrastructure: 2 automatic retries;
- rate limit: 2 retries honoring server/reset evidence;
- deterministic product: 0 until diagnosis produces a fix;
- upstream changed: 0 until a captured fixture and adapter diagnosis exist;
- security/permission/secret/irreversible: 0 automatic retries.

Projects may lower budgets. Raising them requires a task decision.

## Failure record lifecycle

1. assign `failure_id`;
2. capture symptom and exact failing command/run;
3. classify;
4. establish or reference feedback loop;
5. record attempts and changes;
6. resolve, escalate, or mark terminal;
7. link resolution evidence and regression protection.

Use `templates/FAILURE.template.md`.

## Notification boundary

Notify the user only when:

- a true human gate exists;
- security is blocked;
- retry budget is exhausted;
- the task is complete;
- the user explicitly requested intermediate notification.

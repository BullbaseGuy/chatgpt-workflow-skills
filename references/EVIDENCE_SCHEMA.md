# Evidence Schema

Evidence is append-only. Use JSON Lines where machine processing matters and Markdown tables
for human indexes.

## Record

```yaml
evidence_id: EV-0001
task_id: task-slug
work_package: W05
claim_id: CL-0001
claim: Exact proposition supported by this record
classification: FACT # FACT | INFERENCE | ESTIMATE | NOT_DISCLOSED | SOURCE_CONFLICT | TEST_RESULT | EXECUTION_EVENT
source_tier: PRIMARY # PRIMARY | FIRST_PARTY_API | SECONDARY | DERIVED | USER_OBSERVATION
source:
  repository: owner/name
  document: path-or-title
  url: null
  commit_or_version: null
  page_or_location: line/range/cell/run-step
  source_date: "YYYY-MM-DD"
as_of_utc: "YYYY-MM-DDTHH:MM:SSZ"
capture:
  method: connector-read
  command: null
  artifact: null
  content_hash: sha256:...
result:
  verdict: SUPPORTS # SUPPORTS | CONTRADICTS | NEUTRAL | PASS | FAIL
  value: null
confidence: HIGH # HIGH | MEDIUM | LOW
supports: []
contradicts: []
sensitivity: PUBLIC # PUBLIC | INTERNAL | SECRET_PROHIBITED
notes: null
```

## Classification rules

- **FACT:** directly stated or observed in a traceable source.
- **INFERENCE:** reasoned from cited facts; the reasoning must be explicit.
- **ESTIMATE:** model, assumption, projection, or approximate calculation.
- **NOT_DISCLOSED:** the expected fact is absent after a documented search; never replace with zero.
- **SOURCE_CONFLICT:** authoritative sources disagree and reconciliation is unresolved.
- **TEST_RESULT:** deterministic command or assertion result.
- **EXECUTION_EVENT:** run, commit, heartbeat, retry, or state transition evidence.

Do not present INFERENCE or ESTIMATE as FACT.

## Source hierarchy

Prefer:

1. official specifications, filings, source code, repository state, and signed releases;
2. first-party APIs and first-party documentation;
3. independently reproducible calculations;
4. reputable secondary sources;
5. user observation for experiential behavior.

A lower-tier source may identify a lead but cannot silently override a higher-tier source.

## Provenance and integrity

- Pin mutable sources by commit, version, date, page, range, or artifact ID.
- Hash copied fixtures or snapshots.
- Store commands without secrets.
- A source URL alone is insufficient when the content can change.
- If evidence is unavailable to the current environment, record the gap; do not invent it.

## Sensitive evidence

`SECRET_PROHIBITED` means the value itself must not be persisted. Record only:

- that the value was present;
- where it was stored;
- the verification outcome;
- a non-reversible identifier when safe.

Never hash a low-entropy secret as “safe evidence”; hashes can leak guessable values.

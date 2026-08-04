from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

CLASSIFICATIONS = {
    "FACT",
    "INFERENCE",
    "ESTIMATE",
    "NOT_DISCLOSED",
    "SOURCE_CONFLICT",
    "TEST_RESULT",
    "EXECUTION_EVENT",
}
SOURCE_TIERS = {
    "PRIMARY",
    "FIRST_PARTY_API",
    "SECONDARY",
    "DERIVED",
    "USER_OBSERVATION",
}
VERDICTS = {"SUPPORTS", "CONTRADICTS", "NEUTRAL", "PASS", "FAIL"}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
SENSITIVITY = {"PUBLIC", "INTERNAL", "SECRET_PROHIBITED"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_evidence_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "evidence_id",
        "task_id",
        "work_package",
        "claim_id",
        "claim",
        "classification",
        "source_tier",
        "source",
        "as_of_utc",
        "capture",
        "result",
        "confidence",
        "supports",
        "contradicts",
        "sensitivity",
    }
    missing = sorted(required - record.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
        return errors

    for key in ("evidence_id", "task_id", "work_package", "claim_id", "claim", "as_of_utc"):
        if not _nonempty(record.get(key)):
            errors.append(f"{key} must be a non-empty string")

    classification = record.get("classification")
    if classification not in CLASSIFICATIONS:
        errors.append(f"invalid classification: {classification!r}")
    source_tier = record.get("source_tier")
    if source_tier not in SOURCE_TIERS:
        errors.append(f"invalid source_tier: {source_tier!r}")
    if record.get("confidence") not in CONFIDENCE:
        errors.append(f"invalid confidence: {record.get('confidence')!r}")
    sensitivity = record.get("sensitivity")
    if sensitivity not in SENSITIVITY:
        errors.append(f"invalid sensitivity: {sensitivity!r}")

    source = record.get("source")
    if not isinstance(source, dict):
        errors.append("source must be a mapping")
        source = {}
    for key in ("document", "page_or_location", "source_date"):
        if not _nonempty(source.get(key)):
            errors.append(f"source.{key} is required")
    if not (_nonempty(source.get("repository")) or _nonempty(source.get("url"))):
        errors.append("source requires repository or url")
    if not (
        _nonempty(source.get("commit_or_version"))
        or _nonempty(source.get("source_date"))
    ):
        errors.append("source requires an immutable revision/version or source date")

    capture = record.get("capture")
    if not isinstance(capture, dict):
        errors.append("capture must be a mapping")
        capture = {}
    if not _nonempty(capture.get("method")):
        errors.append("capture.method is required")
    if not (
        _nonempty(capture.get("command"))
        or _nonempty(capture.get("artifact"))
        or _nonempty(capture.get("content_hash"))
    ):
        errors.append("capture requires command, artifact, or content_hash")

    result = record.get("result")
    if not isinstance(result, dict):
        errors.append("result must be a mapping")
        result = {}
    if result.get("verdict") not in VERDICTS:
        errors.append(f"invalid result.verdict: {result.get('verdict')!r}")

    for key in ("supports", "contradicts"):
        value = record.get(key)
        if not isinstance(value, list):
            errors.append(f"{key} must be a list")

    notes = record.get("notes")
    if classification == "INFERENCE":
        if not record.get("supports"):
            errors.append("INFERENCE requires supporting evidence IDs")
        if not _nonempty(notes):
            errors.append("INFERENCE requires explicit reasoning in notes")
    elif classification == "ESTIMATE":
        if not _nonempty(notes):
            errors.append("ESTIMATE requires assumptions/sensitivity in notes")
    elif classification == "NOT_DISCLOSED":
        if result.get("value") not in (None, ""):
            errors.append("NOT_DISCLOSED cannot contain a fabricated value")
        if not _nonempty(notes):
            errors.append("NOT_DISCLOSED requires documented search scope in notes")
    elif classification == "SOURCE_CONFLICT":
        if not record.get("supports") or not record.get("contradicts"):
            errors.append("SOURCE_CONFLICT requires supports and contradicts evidence IDs")
    elif classification == "TEST_RESULT":
        if result.get("verdict") not in {"PASS", "FAIL"}:
            errors.append("TEST_RESULT verdict must be PASS or FAIL")
        if not (_nonempty(capture.get("command")) or _nonempty(capture.get("artifact"))):
            errors.append("TEST_RESULT requires command or artifact")

    if sensitivity == "SECRET_PROHIBITED":
        if result.get("value") not in (None, ""):
            errors.append("SECRET_PROHIBITED result.value must be empty")
        if _nonempty(capture.get("content_hash")):
            errors.append("SECRET_PROHIBITED must not persist a value hash")

    return errors


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: expected object")
        records.append(record)
    return records


def validate_evidence_records(records: Iterable[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    materialized = list(records)
    for index, record in enumerate(materialized, start=1):
        evidence_id = record.get("evidence_id")
        if evidence_id in ids:
            errors.append(f"record {index}: duplicate evidence_id {evidence_id}")
        elif isinstance(evidence_id, str):
            ids.add(evidence_id)
        for error in validate_evidence_record(record):
            errors.append(f"record {index} ({evidence_id}): {error}")

    for index, record in enumerate(materialized, start=1):
        for relation in ("supports", "contradicts"):
            for target in record.get(relation) or []:
                if target not in ids:
                    errors.append(
                        f"record {index} ({record.get('evidence_id')}): "
                        f"{relation} references unknown evidence_id {target}"
                    )
    return errors


def validate_evidence_file(path: Path) -> list[str]:
    try:
        records = load_jsonl(path)
    except ValueError as exc:
        return [str(exc)]
    if not records:
        return ["evidence file contains no records"]
    return validate_evidence_records(records)

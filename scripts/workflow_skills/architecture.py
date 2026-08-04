from __future__ import annotations

from typing import Any

STRENGTHS = {"Strong", "Worth exploring", "Speculative"}


def validate_architecture_candidate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "candidate_id",
        "name",
        "modules",
        "problem",
        "evidence_ids",
        "current_seam",
        "proposed_interface",
        "locality_and_leverage",
        "verification_seam",
        "before",
        "after",
        "migration_risk",
        "recommendation_strength",
    }
    missing = sorted(required - data.keys())
    if missing:
        return ["missing required fields: " + ", ".join(missing)]

    for key in (
        "candidate_id",
        "name",
        "problem",
        "current_seam",
        "proposed_interface",
        "locality_and_leverage",
        "verification_seam",
        "before",
        "after",
        "migration_risk",
    ):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key} must be a non-empty string")

    for key in ("modules", "evidence_ids"):
        if not isinstance(data.get(key), list) or not data[key]:
            errors.append(f"{key} must be a non-empty list")

    if data.get("recommendation_strength") not in STRENGTHS:
        errors.append(f"invalid recommendation_strength: {data.get('recommendation_strength')!r}")

    if data.get("before") == data.get("after"):
        errors.append("before and after descriptions must differ")
    return errors

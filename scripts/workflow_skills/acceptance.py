from __future__ import annotations

from typing import Any

AXIS_VERDICTS = {"PASS", "FAIL"}
SECURITY_VERDICTS = {"PASS", "SECURITY_BLOCKED"}
OVERALL_VERDICTS = {"PASS", "FAIL", "PASS_WITH_GAPS"}


def validate_acceptance(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "task_id",
        "base_ref",
        "head_ref",
        "as_of_utc",
        "axes",
        "overall",
        "approved_gaps",
        "gaps_authorized",
    }
    missing = sorted(required - data.keys())
    if missing:
        return ["missing required fields: " + ", ".join(missing)]

    for key in ("task_id", "base_ref", "head_ref", "as_of_utc"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} must be a non-empty string")

    axes = data.get("axes")
    if not isinstance(axes, dict):
        return errors + ["axes must be a mapping"]

    required_axes = ("standards", "spec", "evidence", "security", "resume")
    for axis in required_axes:
        if axis not in axes or not isinstance(axes.get(axis), dict):
            errors.append(f"axes.{axis} must be a mapping")
            continue
        item = axes[axis]
        verdict = item.get("verdict")
        allowed = SECURITY_VERDICTS if axis == "security" else AXIS_VERDICTS
        if verdict not in allowed:
            errors.append(f"axes.{axis}.verdict must be one of {sorted(allowed)}")
        findings = item.get("findings")
        evidence_ids = item.get("evidence_ids")
        if not isinstance(findings, list):
            errors.append(f"axes.{axis}.findings must be a list")
        if not isinstance(evidence_ids, list):
            errors.append(f"axes.{axis}.evidence_ids must be a list")
        if verdict != "PASS" and isinstance(findings, list) and not findings:
            errors.append(f"axes.{axis} non-PASS verdict requires findings")

    overall = data.get("overall")
    if overall not in OVERALL_VERDICTS:
        errors.append(f"invalid overall verdict: {overall!r}")
        return errors

    approved_gaps = data.get("approved_gaps")
    if not isinstance(approved_gaps, list):
        errors.append("approved_gaps must be a list")
        approved_gaps = []

    pass_axes = all(
        isinstance(axes.get(axis), dict) and axes[axis].get("verdict") == "PASS"
        for axis in required_axes
    )

    if overall == "PASS":
        if not pass_axes:
            errors.append("overall PASS requires all five axes PASS")
        if approved_gaps:
            errors.append("overall PASS cannot contain approved gaps")
    elif overall == "PASS_WITH_GAPS":
        if not approved_gaps:
            errors.append("PASS_WITH_GAPS requires at least one approved gap")
        if data.get("gaps_authorized") is not True:
            errors.append("PASS_WITH_GAPS requires gaps_authorized=true")
        if axes.get("security", {}).get("verdict") != "PASS":
            errors.append("PASS_WITH_GAPS cannot override security")
    elif overall == "FAIL":
        if pass_axes and not approved_gaps:
            errors.append("overall FAIL requires a failing axis or explicit gap")

    return errors


def completion_allowed(data: dict[str, Any]) -> tuple[bool, str]:
    errors = validate_acceptance(data)
    if errors:
        return False, "; ".join(errors)
    if data.get("overall") != "PASS":
        return False, f"overall verdict is {data.get('overall')}, not PASS"
    return True, "all acceptance axes passed"

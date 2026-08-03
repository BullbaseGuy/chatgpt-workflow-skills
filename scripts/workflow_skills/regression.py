from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


class ScenarioError(ValueError):
    """Raised when a historical regression scenario is malformed."""


SCENARIO_TYPES = {
    "long_running_action",
    "completed_run_unfinalized",
    "cursor_and_rate_limit",
    "background_notification_duplicate",
    "source_conflict",
    "screener_acceptance",
    "resume_from_task_id",
}

REQUIRED_ASSERTIONS = {
    "no_repeated_questions",
    "no_blind_rerun",
    "no_premature_done",
    "correct_human_gate",
    "evidence_retained",
    "resumable",
}


def load_scenario(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ScenarioError(f"{path}: expected a YAML mapping")
    return data


def _decide(data: dict[str, Any]) -> tuple[str, str, str | None, bool]:
    scenario_type = data["scenario_type"]
    facts = data["facts"]

    if scenario_type == "long_running_action":
        live = int(facts["progress_after"]) > int(facts["progress_before"])
        live = live or int(facts["heartbeat_age_minutes"]) <= int(facts["active_threshold_minutes"])
        if live and facts["run_status"] == "in_progress":
            return "CONTINUE_MONITORING", "RUNNING", None, False
        return "INSPECT_WITHOUT_RERUN", "BLOCKED_AUTO", None, False

    if scenario_type == "completed_run_unfinalized":
        if facts["run_status"] == "completed" and facts["canonical_status"] != "DONE":
            return "RECONCILE_STATE_FROM_EXISTING_RUN", "VERIFYING", None, False
        return "NO_ACTION", facts["canonical_status"], None, False

    if scenario_type == "cursor_and_rate_limit":
        if facts["cursor_remaining"] and facts["http_status"] == 429:
            return "DIAGNOSE_AND_RESUME_FROM_CURSOR", "BLOCKED_AUTO", None, True
        return "CONTINUE_EXPORT", "RUNNING", None, False

    if scenario_type == "background_notification_duplicate":
        if facts["automated_harness_ready"] and facts["physical_device_confirmation_required"]:
            return (
                "RUN_HARNESS_THEN_REQUEST_DEVICE_ACCEPTANCE",
                "NEEDS_HUMAN",
                "MANUAL_NOTIFICATION_ACCEPTANCE",
                False,
            )
        return "BUILD_BROWSER_EVENT_HARNESS", "BLOCKED_AUTO", None, False

    if scenario_type == "source_conflict":
        if facts["official_value"] is None and facts["secondary_value"] is not None:
            if facts["material_to_decision"]:
                return (
                    "PRESERVE_CONFLICT_AND_REQUEST_DECISION",
                    "NEEDS_HUMAN",
                    "MATERIAL_SOURCE_CONFLICT",
                    False,
                )
            return "CLASSIFY_SOURCE_CONFLICT", "VERIFYING", None, False
        return "CONTINUE_RECONCILIATION", "RUNNING", None, False

    if scenario_type == "screener_acceptance":
        if facts["compile_pass"] and not facts["ui_contract_pass"]:
            return (
                "REJECT_PREMATURE_ACCEPTANCE_AND_REQUEST_UI_CHECK",
                "NEEDS_HUMAN",
                "MANUAL_UI_ACCEPTANCE",
                False,
            )
        return "ACCEPT_SCREENING_BUILD", "VERIFYING", None, False

    if scenario_type == "resume_from_task_id":
        if all(
            facts.get(key)
            for key in ("task_id", "active_tasks_path", "state_path", "handoff_path", "frontier")
        ):
            return "RESUME_FROM_CANONICAL_FRONTIER", "RUNNING", None, False
        return "LOCATE_CANONICAL_STATE", "BLOCKED_AUTO", None, False

    raise ScenarioError(f"unsupported scenario_type: {scenario_type}")


def evaluate_scenario(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    required = {"schema_version", "scenario_id", "title", "scenario_type", "facts", "expected"}
    missing = sorted(required - data.keys())
    if missing:
        return {
            "scenario_id": data.get("scenario_id", "UNKNOWN"),
            "passed": False,
            "errors": ["missing: " + ", ".join(missing)],
        }

    if data["scenario_type"] not in SCENARIO_TYPES:
        errors.append(f"unsupported scenario_type: {data['scenario_type']}")

    facts = data.get("facts")
    expected = data.get("expected")
    if not isinstance(facts, dict):
        errors.append("facts must be a mapping")
        facts = {}
    if not isinstance(expected, dict):
        errors.append("expected must be a mapping")
        expected = {}

    if errors:
        return {"scenario_id": data["scenario_id"], "passed": False, "errors": errors}

    decision, task_status, human_gate, rerun = _decide(data)

    actual_assertions = {
        "no_repeated_questions": bool(facts.get("inputs_already_available"))
        and int(facts.get("user_questions_asked", 1)) == 0,
        "no_blind_rerun": not rerun
        or (
            bool(facts.get("tight_feedback_loop"))
            and bool(facts.get("changed_variable"))
            and not bool(facts.get("same_invocation_without_new_evidence"))
        ),
        "no_premature_done": task_status != "DONE"
        or all(value == "PASS" for value in (facts.get("acceptance_axes") or {}).values()),
        "correct_human_gate": human_gate == expected.get("human_gate"),
        "evidence_retained": bool(facts.get("preserve_evidence"))
        and bool(facts.get("evidence_paths")),
        "resumable": bool(facts.get("resume_locator")) and bool(facts.get("next_action")),
    }

    for key in REQUIRED_ASSERTIONS:
        if actual_assertions.get(key) is not True:
            errors.append(f"policy assertion failed: {key}")

    comparisons = {
        "decision": decision,
        "task_status": task_status,
        "human_gate": human_gate,
        "rerun": rerun,
    }
    for key, actual in comparisons.items():
        if expected.get(key) != actual:
            errors.append(f"expected {key}={expected.get(key)!r}, got {actual!r}")

    return {
        "scenario_id": data["scenario_id"],
        "passed": not errors,
        "decision": decision,
        "task_status": task_status,
        "human_gate": human_gate,
        "rerun": rerun,
        "assertions": actual_assertions,
        "errors": errors,
    }


def run_scenarios(paths: list[Path]) -> list[dict[str, Any]]:
    return [evaluate_scenario(load_scenario(path)) for path in sorted(paths)]


def clone_scenario(data: dict[str, Any]) -> dict[str, Any]:
    """Test helper that avoids mutating parsed fixtures."""
    return deepcopy(data)

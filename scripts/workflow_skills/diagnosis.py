from __future__ import annotations

from typing import Any

from .state import StateError


RETRYABLE_CLASSES = {"TRANSIENT_INFRASTRUCTURE"}


def validate_repro_manifest(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "failure_id",
        "failure_class",
        "exact_symptom",
        "original_invocation",
        "checkpoints_preserved",
        "feedback_loop",
        "reproduction",
        "hypotheses",
        "fix",
        "retry",
    }
    missing = sorted(required - data.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
        return errors

    loop = data.get("feedback_loop") or {}
    for key in ("invocation", "assertion", "red_output"):
        if not isinstance(loop.get(key), str) or not loop.get(key).strip():
            errors.append(f"feedback_loop.{key} is required")
    for key in ("red_observed", "deterministic", "agent_runnable"):
        if loop.get(key) is not True:
            errors.append(f"feedback_loop.{key} must be true")
    try:
        runtime = float(loop.get("typical_runtime_seconds"))
        if runtime <= 0:
            raise ValueError
    except (TypeError, ValueError):
        errors.append("feedback_loop.typical_runtime_seconds must be positive")

    reproduction = data.get("reproduction") or {}
    if reproduction.get("minimized") is not True:
        errors.append("reproduction.minimized must be true")
    elements = reproduction.get("load_bearing_elements")
    if not isinstance(elements, list) or not elements:
        errors.append("reproduction.load_bearing_elements must be a non-empty list")

    hypotheses = data.get("hypotheses")
    if not isinstance(hypotheses, list) or not 3 <= len(hypotheses) <= 5:
        errors.append("hypotheses must contain 3 to 5 items")
    else:
        ranks: set[int] = set()
        for index, hypothesis in enumerate(hypotheses, start=1):
            if not isinstance(hypothesis, dict):
                errors.append(f"hypotheses[{index}] must be a mapping")
                continue
            rank = hypothesis.get("rank")
            if not isinstance(rank, int) or rank in ranks:
                errors.append(f"hypotheses[{index}].rank must be a unique integer")
            else:
                ranks.add(rank)
            for key in ("cause", "prediction", "probe"):
                if not isinstance(hypothesis.get(key), str) or not hypothesis.get(key).strip():
                    errors.append(f"hypotheses[{index}].{key} is required")

    fix = data.get("fix") or {}
    if fix.get("applied") is True:
        for key in ("regression_green", "original_scenario_green", "debug_cleanup_complete"):
            if fix.get(key) is not True:
                errors.append(f"fix.{key} must be true when fix.applied=true")

    retry = data.get("retry") or {}
    if retry.get("requested") is True:
        changed = retry.get("changed_variable")
        if not isinstance(changed, str) or not changed.strip():
            errors.append("retry.changed_variable is required for a retry")
        attempts = int(retry.get("attempts_used", 0))
        budget = int(retry.get("budget", 0))
        if attempts >= budget:
            errors.append("retry budget is exhausted")
        if data.get("failure_class") not in RETRYABLE_CLASSES and fix.get("applied") is not True:
            errors.append("non-transient retry requires an applied verified fix")

    return errors


def retry_decision(data: dict[str, Any]) -> tuple[bool, str]:
    errors = validate_repro_manifest(data)
    if errors:
        return False, "manifest invalid: " + "; ".join(errors)
    retry = data["retry"]
    if retry.get("requested") is not True:
        return False, "retry not requested"
    if not retry.get("changed_variable"):
        return False, "blind rerun: no predicted variable changed"
    if int(retry.get("attempts_used", 0)) >= int(retry.get("budget", 0)):
        return False, "retry budget exhausted"
    return True, "bounded non-blind retry permitted"

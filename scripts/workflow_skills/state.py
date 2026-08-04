from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


class StateError(ValueError):
    """Raised when canonical state is internally inconsistent."""


TASK_STATUSES = {
    "PLANNING",
    "READY",
    "RUNNING",
    "BLOCKED_AUTO",
    "NEEDS_HUMAN",
    "VERIFYING",
    "DONE",
    "FAILED_TERMINAL",
}
PACKAGE_STATUSES = {
    "PLANNING",
    "BLOCKED",
    "READY",
    "RUNNING",
    "VERIFYING",
    "DONE",
    "FAILED",
    "NEEDS_HUMAN",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise StateError(f"{path}: expected a YAML mapping")
    return data


def package_map(work_packages: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for package in work_packages:
        package_id = package.get("id")
        if not isinstance(package_id, str) or not package_id:
            raise StateError("every work package requires a non-empty id")
        if package_id in result:
            raise StateError(f"duplicate work package id: {package_id}")
        result[package_id] = package
    return result


def detect_cycle(work_packages: list[dict[str, Any]]) -> list[str] | None:
    packages = package_map(work_packages)
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(package_id: str) -> list[str] | None:
        if package_id in visiting:
            start = stack.index(package_id)
            return stack[start:] + [package_id]
        if package_id in visited:
            return None
        visiting.add(package_id)
        stack.append(package_id)
        package = packages[package_id]
        blockers = package.get("blocked_by") or []
        if not isinstance(blockers, list):
            raise StateError(f"{package_id}: blocked_by must be a list")
        for blocker in blockers:
            if blocker not in packages:
                raise StateError(f"{package_id}: unknown blocker {blocker}")
            cycle = visit(blocker)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(package_id)
        visited.add(package_id)
        return None

    for package_id in packages:
        cycle = visit(package_id)
        if cycle:
            return cycle
    return None


def compute_frontier(work_packages: list[dict[str, Any]]) -> list[str]:
    packages = package_map(work_packages)
    cycle = detect_cycle(work_packages)
    if cycle:
        raise StateError("dependency cycle: " + " -> ".join(cycle))

    frontier: list[str] = []
    for package_id, package in packages.items():
        status = package.get("status")
        if status not in {"READY", "BLOCKED_AUTO"}:
            continue
        blockers = package.get("blocked_by") or []
        if all(packages[blocker].get("status") == "DONE" for blocker in blockers):
            retry = package.get("retry") or {}
            attempts = int(retry.get("attempts", 0))
            budget = int(retry.get("budget", 2))
            claimed = bool(package.get("claimed_by"))
            if attempts <= budget and not claimed:
                frontier.append(package_id)
    return sorted(frontier)


def _parse_utc(value: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise StateError(f"invalid UTC timestamp: {value!r}")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError as exc:
        raise StateError(f"invalid UTC timestamp: {value!r}") from exc


def classify_run_health(
    *,
    run_status: str,
    last_heartbeat_utc: str,
    now_utc: str,
    progress_before: int,
    progress_after: int,
    active_threshold_minutes: int = 15,
    known_wait_threshold_minutes: int = 60,
    known_external_wait: bool = False,
) -> str:
    normalized = run_status.lower()
    if normalized in {"completed", "success"}:
        return "COMPLETED"
    if normalized in {"failure", "failed", "cancelled", "timed_out"}:
        return "FAILED"
    heartbeat = _parse_utc(last_heartbeat_utc)
    now = _parse_utc(now_utc)
    age_minutes = (now - heartbeat).total_seconds() / 60
    threshold = known_wait_threshold_minutes if known_external_wait else active_threshold_minutes
    if progress_after > progress_before:
        return "LIVE"
    if age_minutes <= threshold:
        return "LIVE"
    return "INSPECT"


def validate_state(repo_root: Path, state_path: Path, *, enforce_model_zero: bool = False) -> list[str]:
    state = load_yaml(state_path)
    errors: list[str] = []

    required = {
        "schema_version",
        "task_id",
        "title",
        "repository",
        "branch",
        "decision_mode",
        "status",
        "stage",
        "execution_status",
        "acceptance_status",
        "security_status",
        "created_at_utc",
        "updated_at_utc",
        "last_heartbeat_utc",
        "frontier",
        "work_packages",
        "verification",
        "model_execution",
    }
    missing = sorted(required - state.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    if state.get("status") not in TASK_STATUSES:
        errors.append(f"invalid task status: {state.get('status')!r}")

    work_packages = state.get("work_packages")
    if not isinstance(work_packages, list):
        errors.append("work_packages must be a list")
        return errors

    try:
        packages = package_map(work_packages)
        cycle = detect_cycle(work_packages)
        if cycle:
            errors.append("dependency cycle: " + " -> ".join(cycle))
        expected_frontier = compute_frontier(work_packages)
        actual_frontier = sorted(state.get("frontier") or [])
        if expected_frontier != actual_frontier:
            errors.append(f"frontier mismatch: expected {expected_frontier}, got {actual_frontier}")
    except StateError as exc:
        errors.append(str(exc))
        packages = {}

    for package_id, package in packages.items():
        status = package.get("status")
        if status not in PACKAGE_STATUSES:
            errors.append(f"{package_id}: invalid status {status!r}")
        plan_path = package.get("plan_path")
        result_path = package.get("result_path")
        if not isinstance(plan_path, str) or not (repo_root / plan_path).is_file():
            errors.append(f"{package_id}: missing plan file {plan_path!r}")
        if status == "DONE":
            if not isinstance(result_path, str) or not (repo_root / result_path).is_file():
                errors.append(f"{package_id}: DONE without result file {result_path!r}")

    for key in ("created_at_utc", "updated_at_utc", "last_heartbeat_utc"):
        try:
            _parse_utc(state.get(key))
        except StateError as exc:
            errors.append(str(exc))

    model_execution = state.get("model_execution") or {}
    if enforce_model_zero and (
        model_execution.get("enabled") is not False
        or int(model_execution.get("codex_invocations", -1)) != 0
    ):
        errors.append("model execution must remain disabled with codex_invocations=0")

    if state.get("status") == "DONE":
        incomplete = [pid for pid, package in packages.items() if package.get("status") != "DONE"]
        if incomplete:
            errors.append("DONE task has incomplete packages: " + ", ".join(incomplete))
        verification = state.get("verification") or {}
        for axis in ("standards", "spec", "evidence"):
            if verification.get(axis) != "PASS":
                errors.append(f"DONE task requires verification.{axis}=PASS")
        if state.get("security_status") != "PASS":
            errors.append("DONE task requires security_status=PASS")
        if state.get("human_gate") is not None or state.get("active_blockers"):
            errors.append("DONE task cannot retain blockers or human gate")

    return errors

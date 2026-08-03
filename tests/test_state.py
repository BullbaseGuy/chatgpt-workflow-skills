from __future__ import annotations

import unittest

from scripts.workflow_skills.state import (
    StateError,
    classify_run_health,
    compute_frontier,
    detect_cycle,
)


class FrontierTests(unittest.TestCase):
    def test_linear_frontier(self) -> None:
        packages = [
            {"id": "W00", "status": "DONE", "blocked_by": []},
            {"id": "W01", "status": "READY", "blocked_by": ["W00"]},
            {"id": "W02", "status": "BLOCKED", "blocked_by": ["W01"]},
        ]
        self.assertEqual(compute_frontier(packages), ["W01"])

    def test_parallel_frontier(self) -> None:
        packages = [
            {"id": "W00", "status": "DONE", "blocked_by": []},
            {"id": "W01", "status": "READY", "blocked_by": ["W00"]},
            {"id": "W02", "status": "READY", "blocked_by": ["W00"]},
        ]
        self.assertEqual(compute_frontier(packages), ["W01", "W02"])

    def test_claimed_package_is_not_frontier(self) -> None:
        packages = [
            {"id": "W00", "status": "DONE", "blocked_by": []},
            {"id": "W01", "status": "READY", "blocked_by": ["W00"], "claimed_by": "run-1"},
        ]
        self.assertEqual(compute_frontier(packages), [])

    def test_cycle_is_reported(self) -> None:
        packages = [
            {"id": "W01", "status": "READY", "blocked_by": ["W02"]},
            {"id": "W02", "status": "READY", "blocked_by": ["W01"]},
        ]
        self.assertEqual(detect_cycle(packages), ["W01", "W02", "W01"])
        with self.assertRaises(StateError):
            compute_frontier(packages)


class HeartbeatTests(unittest.TestCase):
    def test_long_but_progressing_run_is_live(self) -> None:
        result = classify_run_health(
            run_status="in_progress",
            last_heartbeat_utc="2026-08-03T10:00:00Z",
            now_utc="2026-08-03T12:00:00Z",
            progress_before=20,
            progress_after=21,
        )
        self.assertEqual(result, "LIVE")

    def test_stale_no_progress_needs_inspection_not_failure(self) -> None:
        result = classify_run_health(
            run_status="in_progress",
            last_heartbeat_utc="2026-08-03T10:00:00Z",
            now_utc="2026-08-03T10:30:00Z",
            progress_before=20,
            progress_after=20,
        )
        self.assertEqual(result, "INSPECT")

    def test_known_external_wait_uses_longer_threshold(self) -> None:
        result = classify_run_health(
            run_status="in_progress",
            last_heartbeat_utc="2026-08-03T10:00:00Z",
            now_utc="2026-08-03T10:45:00Z",
            progress_before=20,
            progress_after=20,
            known_external_wait=True,
        )
        self.assertEqual(result, "LIVE")


if __name__ == "__main__":
    unittest.main()

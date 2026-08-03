from __future__ import annotations

import copy
import unittest
from pathlib import Path

import yaml

from scripts.workflow_skills.diagnosis import retry_decision, validate_repro_manifest


class DiagnosisManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = Path("tests/fixtures/repro_manifest_valid.yaml")
        cls.valid = yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_valid_manifest_passes(self) -> None:
        self.assertEqual(validate_repro_manifest(copy.deepcopy(self.valid)), [])

    def test_no_observed_red_is_rejected(self) -> None:
        data = copy.deepcopy(self.valid)
        data["feedback_loop"]["red_observed"] = False
        self.assertIn(
            "feedback_loop.red_observed must be true",
            validate_repro_manifest(data),
        )

    def test_fewer_than_three_hypotheses_is_rejected(self) -> None:
        data = copy.deepcopy(self.valid)
        data["hypotheses"] = data["hypotheses"][:2]
        self.assertIn(
            "hypotheses must contain 3 to 5 items",
            validate_repro_manifest(data),
        )

    def test_blind_retry_is_rejected(self) -> None:
        data = copy.deepcopy(self.valid)
        data["failure_class"] = "TRANSIENT_INFRASTRUCTURE"
        data["retry"] = {
            "requested": True,
            "changed_variable": "",
            "attempts_used": 0,
            "budget": 2,
        }
        allowed, reason = retry_decision(data)
        self.assertFalse(allowed)
        self.assertIn("changed_variable", reason)

    def test_bounded_transient_retry_with_change_is_allowed(self) -> None:
        data = copy.deepcopy(self.valid)
        data["failure_class"] = "TRANSIENT_INFRASTRUCTURE"
        data["retry"] = {
            "requested": True,
            "changed_variable": "server reset time elapsed",
            "attempts_used": 0,
            "budget": 2,
        }
        allowed, reason = retry_decision(data)
        self.assertTrue(allowed)
        self.assertIn("permitted", reason)


if __name__ == "__main__":
    unittest.main()

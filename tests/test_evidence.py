from __future__ import annotations

import copy
import unittest
from pathlib import Path

import yaml

from scripts.workflow_skills.acceptance import completion_allowed, validate_acceptance
from scripts.workflow_skills.architecture import validate_architecture_candidate
from scripts.workflow_skills.evidence import load_jsonl, validate_evidence_file, validate_evidence_record


class EvidenceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path = Path("tests/fixtures/evidence_valid.jsonl")
        cls.records = load_jsonl(cls.path)

    def test_valid_file(self) -> None:
        self.assertEqual(validate_evidence_file(self.path), [])

    def test_inference_without_support_is_rejected(self) -> None:
        record = copy.deepcopy(next(r for r in self.records if r["classification"] == "INFERENCE"))
        record["supports"] = []
        self.assertIn("INFERENCE requires supporting evidence IDs", validate_evidence_record(record))

    def test_not_disclosed_with_value_is_rejected(self) -> None:
        record = copy.deepcopy(next(r for r in self.records if r["classification"] == "NOT_DISCLOSED"))
        record["result"]["value"] = 0
        self.assertIn(
            "NOT_DISCLOSED cannot contain a fabricated value",
            validate_evidence_record(record),
        )

    def test_source_conflict_requires_both_sides(self) -> None:
        record = copy.deepcopy(next(r for r in self.records if r["classification"] == "SOURCE_CONFLICT"))
        record["contradicts"] = []
        self.assertIn(
            "SOURCE_CONFLICT requires supports and contradicts evidence IDs",
            validate_evidence_record(record),
        )

    def test_secret_prohibited_value_and_hash_are_rejected(self) -> None:
        record = copy.deepcopy(self.records[0])
        record["sensitivity"] = "SECRET_PROHIBITED"
        record["result"]["value"] = "secret"
        errors = validate_evidence_record(record)
        self.assertIn("SECRET_PROHIBITED result.value must be empty", errors)
        self.assertIn("SECRET_PROHIBITED must not persist a value hash", errors)


class AcceptanceTests(unittest.TestCase):
    def test_pass_manifest_allows_completion(self) -> None:
        data = yaml.safe_load(Path("tests/fixtures/acceptance_pass.yaml").read_text(encoding="utf-8"))
        self.assertEqual(validate_acceptance(data), [])
        self.assertEqual(completion_allowed(data), (True, "all acceptance axes passed"))

    def test_failing_axis_blocks_completion(self) -> None:
        data = yaml.safe_load(Path("tests/fixtures/acceptance_fail.yaml").read_text(encoding="utf-8"))
        self.assertEqual(validate_acceptance(data), [])
        allowed, reason = completion_allowed(data)
        self.assertFalse(allowed)
        self.assertIn("not PASS", reason)

    def test_overall_pass_cannot_hide_failing_axis(self) -> None:
        data = yaml.safe_load(Path("tests/fixtures/acceptance_fail.yaml").read_text(encoding="utf-8"))
        data["overall"] = "PASS"
        self.assertIn("overall PASS requires all five axes PASS", validate_acceptance(data))


class ArchitectureCandidateTests(unittest.TestCase):
    def test_valid_candidate(self) -> None:
        data = yaml.safe_load(
            Path("tests/fixtures/architecture_candidate.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_architecture_candidate(data), [])

    def test_candidate_without_evidence_is_rejected(self) -> None:
        data = yaml.safe_load(
            Path("tests/fixtures/architecture_candidate.yaml").read_text(encoding="utf-8")
        )
        data["evidence_ids"] = []
        self.assertIn("evidence_ids must be a non-empty list", validate_architecture_candidate(data))


if __name__ == "__main__":
    unittest.main()

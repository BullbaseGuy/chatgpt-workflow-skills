from __future__ import annotations

import unittest
from pathlib import Path

from scripts.workflow_skills.regression import clone_scenario, evaluate_scenario, load_scenario, run_scenarios


SCENARIO_DIR = Path("tests/scenarios")


class HistoricalRegressionTests(unittest.TestCase):
    def test_all_historical_scenarios_pass(self) -> None:
        results = run_scenarios(sorted(SCENARIO_DIR.glob("*.yaml")))
        self.assertEqual(len(results), 7)
        self.assertTrue(all(result["passed"] for result in results), results)

    def test_repeated_question_is_detected(self) -> None:
        scenario = clone_scenario(load_scenario(SCENARIO_DIR / "07-resume-from-task-id.yaml"))
        scenario["facts"]["user_questions_asked"] = 1
        result = evaluate_scenario(scenario)
        self.assertFalse(result["passed"])
        self.assertIn("policy assertion failed: no_repeated_questions", result["errors"])

    def test_blind_rerun_is_detected(self) -> None:
        scenario = clone_scenario(load_scenario(SCENARIO_DIR / "03-x-scrap-cursor-429.yaml"))
        scenario["facts"]["changed_variable"] = None
        scenario["facts"]["same_invocation_without_new_evidence"] = True
        result = evaluate_scenario(scenario)
        self.assertFalse(result["passed"])
        self.assertIn("policy assertion failed: no_blind_rerun", result["errors"])

    def test_wrong_human_gate_is_detected(self) -> None:
        scenario = clone_scenario(load_scenario(SCENARIO_DIR / "05-f10-source-conflict.yaml"))
        scenario["expected"]["human_gate"] = None
        result = evaluate_scenario(scenario)
        self.assertFalse(result["passed"])
        self.assertIn("policy assertion failed: correct_human_gate", result["errors"])


if __name__ == "__main__":
    unittest.main()

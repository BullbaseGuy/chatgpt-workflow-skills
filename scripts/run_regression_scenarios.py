from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.workflow_skills.regression import run_scenarios


def main() -> int:
    parser = argparse.ArgumentParser(description="Run historical workflow policy regressions")
    parser.add_argument("--scenarios", type=Path, default=Path("tests/scenarios"))
    parser.add_argument(
        "--snapshot", type=Path, default=Path("tests/scenarios/expected-results.json")
    )
    parser.add_argument("--update-snapshot", action="store_true")
    args = parser.parse_args()

    scenario_paths = sorted(args.scenarios.glob("*.yaml"))
    if not scenario_paths:
        raise SystemExit("no scenario YAML files found")

    results = run_scenarios(scenario_paths)
    snapshot = [
        {
            "scenario_id": item["scenario_id"],
            "passed": item["passed"],
            "decision": item.get("decision"),
            "task_status": item.get("task_status"),
            "human_gate": item.get("human_gate"),
            "rerun": item.get("rerun"),
        }
        for item in results
    ]

    if args.update_snapshot:
        args.snapshot.write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    else:
        expected = json.loads(args.snapshot.read_text(encoding="utf-8"))
        if expected != snapshot:
            print(
                json.dumps(
                    {"expected": expected, "actual": snapshot},
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 1

    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

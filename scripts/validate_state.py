from __future__ import annotations

import argparse
import sys
from pathlib import Path

from workflow_skills.state import load_yaml, validate_state


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical workflow task state.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--state", type=Path)
    parser.add_argument("--all-active", action="store_true")
    parser.add_argument("--enforce-model-zero", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    state_paths: list[Path] = []

    if args.state:
        state_paths.append((repo_root / args.state).resolve())
    if args.all_active:
        index_path = repo_root / "docs/implementation/ACTIVE_TASKS.yaml"
        index = load_yaml(index_path)
        for item in index.get("active_tasks") or []:
            state_paths.append((repo_root / item["state_path"]).resolve())

    if not state_paths:
        parser.error("provide --state or --all-active")

    failures = 0
    for state_path in state_paths:
        errors = validate_state(
            repo_root,
            state_path,
            enforce_model_zero=args.enforce_model_zero,
        )
        if errors:
            failures += 1
            print(f"FAIL {state_path.relative_to(repo_root)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {state_path.relative_to(repo_root)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

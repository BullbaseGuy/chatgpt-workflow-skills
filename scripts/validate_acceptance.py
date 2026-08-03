from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from workflow_skills.acceptance import completion_allowed, validate_acceptance


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a workflow acceptance report manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--require-completion", action="store_true")
    args = parser.parse_args()

    data = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("FAIL manifest must be a YAML mapping")
        return 1

    errors = validate_acceptance(data)
    if errors:
        print(f"FAIL {args.manifest}")
        for error in errors:
            print(f"  - {error}")
        return 1

    if args.require_completion:
        allowed, reason = completion_allowed(data)
        if not allowed:
            print(f"FAIL {args.manifest}: {reason}")
            return 1

    print(f"PASS {args.manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

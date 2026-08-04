from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from workflow_skills.diagnosis import validate_repro_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a diagnose-before-retry repro manifest.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    data = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("FAIL manifest must be a YAML mapping")
        return 1
    errors = validate_repro_manifest(data)
    if errors:
        print(f"FAIL {args.manifest}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS {args.manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

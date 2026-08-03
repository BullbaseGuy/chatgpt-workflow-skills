from __future__ import annotations

import argparse
import sys
from pathlib import Path

from workflow_skills.evidence import validate_evidence_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate workflow evidence JSONL.")
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()

    errors = validate_evidence_file(args.evidence)
    if errors:
        print(f"FAIL {args.evidence}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS {args.evidence}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

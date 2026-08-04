from __future__ import annotations

import argparse
import sys
from pathlib import Path

from workflow_skills.wizard import load_manifest, validate_manifest, validate_script


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PowerShell manual wizard.")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--script", type=Path, required=True)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        manifest = load_manifest(args.manifest)
        errors.extend(validate_manifest(manifest))
    except (OSError, ValueError) as exc:
        errors.append(str(exc))

    try:
        script = args.script.read_text(encoding="utf-8")
        errors.extend(validate_script(script))
    except OSError as exc:
        errors.append(str(exc))

    if errors:
        print("FAIL manual wizard")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS manual wizard: {args.script} + {args.manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

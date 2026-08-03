from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.workflow_skills.release import validate_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the workflow-skills release manifest")
    parser.add_argument("--manifest", type=Path, default=Path("release/skills-manifest.json"))
    args = parser.parse_args()
    errors = validate_manifest(REPO_ROOT, args.manifest, verify_source_files=True)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("release manifest: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

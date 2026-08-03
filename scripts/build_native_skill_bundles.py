from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.workflow_skills.release import build_native_bundles


def main() -> int:
    parser = argparse.ArgumentParser(description="Build upload-ready native ChatGPT skill folders")
    parser.add_argument("--manifest", type=Path, default=Path("release/skills-manifest.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    bundles = build_native_bundles(REPO_ROOT, args.manifest, args.output)
    for bundle in bundles:
        print(bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.workflow_skills.release import install_from_local_source


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate a pinned workflow-skills installation")
    parser.add_argument("--source-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--manifest", type=Path, default=Path("release/skills-manifest.json"))
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    manifest = args.manifest
    if not manifest.is_absolute():
        manifest = args.source_root / manifest
    print(
        install_from_local_source(
            source_root=args.source_root,
            manifest_path=manifest,
            destination=args.destination,
            revision=args.revision,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

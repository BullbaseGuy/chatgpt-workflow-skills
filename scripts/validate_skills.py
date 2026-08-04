from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = (
    "## Triggers",
    "## Inputs",
    "## Process",
    "## Completion criteria",
    "## Failure paths",
    "## Output contract",
    "## Context pointers",
)
POINTER_RE = re.compile(r"`((?:references|templates)/[^`]+)`")


def main() -> int:
    root = Path.cwd()
    failures: list[str] = []
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        failures.append("no skills/*/SKILL.md files found")

    names: set[str] = set()
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            failures.append(f"{path}: missing YAML frontmatter")
            continue
        match = re.search(r"^name:\s*([^\n]+)$", text, re.MULTILINE)
        if not match:
            failures.append(f"{path}: missing frontmatter name")
        else:
            name = match.group(1).strip()
            if name in names:
                failures.append(f"{path}: duplicate skill name {name}")
            names.add(name)
            if path.parent.name != name:
                failures.append(f"{path}: directory and skill name differ")
        description = re.search(r"^description:\s*([^\n]+)$", text, re.MULTILINE)
        if not description or len(description.group(1).strip()) < 20:
            failures.append(f"{path}: description is missing or too vague")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                failures.append(f"{path}: missing {heading}")
        for pointer in POINTER_RE.findall(text):
            if not (root / pointer).is_file():
                failures.append(f"{path}: broken context pointer {pointer}")

    if failures:
        print("Skill validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS validated {len(skill_files)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.workflow_skills.release import (
    REQUIRED_SKILLS,
    ReleaseError,
    build_native_bundles,
    git_blob_sha,
    install_from_local_source,
    validate_manifest,
)


REVISION = "0123456789abcdef0123456789abcdef01234567"


def write_fixture(root: Path, *, omit_reference: bool = False) -> Path:
    entries: list[dict[str, object]] = []

    def add(path: str, content: str, kind: str) -> None:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        entries.append(
            {
                "path": path,
                "destination": path,
                "git_blob_sha": git_blob_sha(target.read_bytes()),
                "kind": kind,
                "required": True,
            }
        )

    for skill in sorted(REQUIRED_SKILLS):
        pointer = "\n- `references/POLICY.md`\n" if skill == "workflow-router" else "\n"
        add(
            f"skills/{skill}/SKILL.md",
            f"---\nname: {skill}\ndescription: fixture\n---\n# {skill}{pointer}",
            "skill",
        )
    if not omit_reference:
        add("references/POLICY.md", "# Policy\n", "reference")
    add("templates/SPEC.template.md", "# Spec\n", "template")
    add("LICENSE", "fixture license\n", "license")
    add("LICENSES/mattpocock-skills-MIT.txt", "upstream license\n", "license")

    manifest = {
        "schema_version": "1.0.0",
        "release_version": "fixture",
        "source_repository": "BullbaseGuy/chatgpt-workflow-skills",
        "revision_policy": "exact-40-hex-commit",
        "install_root": ".agents/workflow-skills",
        "entry_skill": "skills/workflow-router/SKILL.md",
        "files": entries,
    }
    manifest_path = root / "release/skills-manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


class ReleaseManifestTests(unittest.TestCase):
    def test_valid_manifest_and_idempotent_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            destination = Path(temp) / "consumer"
            manifest = write_fixture(root)
            self.assertEqual(validate_manifest(root, manifest), [])
            self.assertEqual(
                install_from_local_source(
                    source_root=root,
                    manifest_path=manifest,
                    destination=destination,
                    revision=REVISION,
                ),
                "INSTALLED",
            )
            self.assertEqual(
                install_from_local_source(
                    source_root=root,
                    manifest_path=manifest,
                    destination=destination,
                    revision=REVISION,
                ),
                "UNCHANGED",
            )
            lock = json.loads((destination / ".workflow-skills.lock.json").read_text())
            self.assertEqual(lock["revision"], REVISION)
            self.assertEqual(lock["installed_file_count"], len(json.loads(manifest.read_text())["files"]))

    def test_unpinned_revision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            manifest = write_fixture(root)
            with self.assertRaisesRegex(ReleaseError, "exact 40-character"):
                install_from_local_source(
                    source_root=root,
                    manifest_path=manifest,
                    destination=Path(temp) / "consumer",
                    revision="main",
                )

    def test_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            destination = Path(temp) / "consumer"
            manifest = write_fixture(root)
            install_from_local_source(
                source_root=root,
                manifest_path=manifest,
                destination=destination,
                revision=REVISION,
            )
            (destination / "skills/workflow-router/SKILL.md").write_text("tampered\n")
            with self.assertRaisesRegex(ReleaseError, "blob mismatch"):
                install_from_local_source(
                    source_root=root,
                    manifest_path=manifest,
                    destination=destination,
                    revision=REVISION,
                )

    def test_context_pointer_must_be_in_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            manifest = write_fixture(root, omit_reference=True)
            errors = validate_manifest(root, manifest)
            self.assertTrue(any("context pointer missing" in error for error in errors), errors)

    def test_native_bundles_are_generated_from_single_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            manifest = write_fixture(root)
            output = Path(temp) / "native"
            bundles = build_native_bundles(root, manifest, output)
            self.assertEqual(len(bundles), 10)
            for bundle in bundles:
                self.assertTrue((bundle / "SKILL.md").is_file())
                self.assertTrue((bundle / "references/POLICY.md").is_file())
                self.assertTrue((bundle / "LICENSES/mattpocock-skills-MIT.txt").is_file())


if __name__ == "__main__":
    unittest.main()

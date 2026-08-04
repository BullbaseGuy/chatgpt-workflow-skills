from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
from typing import Any


class ReleaseError(ValueError):
    """Raised when a release manifest or installed bundle is invalid."""


REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
BLOB_RE = re.compile(r"^[0-9a-f]{40}$")
POINTER_RE = re.compile(r"`((?:references|templates)/[^`]+)`")
REQUIRED_SKILLS = {
    "workflow-router",
    "task-to-spec",
    "frontier-planner",
    "execution-supervisor",
    "diagnose-before-retry",
    "durable-handoff",
    "acceptance-review",
    "evidence-research",
    "manual-wizard-powershell",
    "architecture-review",
}
ALLOWED_KINDS = {"skill", "reference", "template", "license"}


def git_blob_sha(data: bytes) -> str:
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()  # noqa: S324 - Git object identity, not security


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ReleaseError(f"{path}: expected a JSON object")
    return data


def _safe_relative(value: str, field: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ReleaseError(f"{field} must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ReleaseError(f"{field} must be a normalized relative path: {value!r}")
    return path


def validate_manifest(
    repo_root: Path,
    manifest_path: Path,
    *,
    verify_source_files: bool = True,
) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError, ReleaseError) as exc:
        return [str(exc)]

    required = {
        "schema_version",
        "release_version",
        "source_repository",
        "revision_policy",
        "install_root",
        "entry_skill",
        "files",
    }
    missing = sorted(required - manifest.keys())
    if missing:
        errors.append("missing manifest fields: " + ", ".join(missing))
        return errors

    if manifest.get("revision_policy") != "exact-40-hex-commit":
        errors.append("revision_policy must be exact-40-hex-commit")

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        errors.append("files must be a non-empty list")
        return errors

    seen_paths: set[str] = set()
    seen_destinations: set[str] = set()
    included_paths: set[str] = set()
    skill_names: set[str] = set()

    for index, entry in enumerate(files):
        label = f"files[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        try:
            source = _safe_relative(entry.get("path"), f"{label}.path")
            destination = _safe_relative(entry.get("destination"), f"{label}.destination")
        except ReleaseError as exc:
            errors.append(str(exc))
            continue

        source_text = source.as_posix()
        destination_text = destination.as_posix()
        if source_text in seen_paths:
            errors.append(f"duplicate source path: {source_text}")
        if destination_text in seen_destinations:
            errors.append(f"duplicate destination: {destination_text}")
        seen_paths.add(source_text)
        seen_destinations.add(destination_text)
        included_paths.add(source_text)

        blob_sha = entry.get("git_blob_sha")
        if not isinstance(blob_sha, str) or not BLOB_RE.fullmatch(blob_sha):
            errors.append(f"{label}.git_blob_sha must be 40 lowercase hex characters")

        kind = entry.get("kind")
        if kind not in ALLOWED_KINDS:
            errors.append(f"{label}.kind is invalid: {kind!r}")
        if entry.get("required") is not True:
            errors.append(f"{label}.required must be true")

        source_file = repo_root / source_text
        if verify_source_files:
            if not source_file.is_file():
                errors.append(f"missing source file: {source_text}")
            elif isinstance(blob_sha, str):
                actual = git_blob_sha(source_file.read_bytes())
                if actual != blob_sha:
                    errors.append(
                        f"blob mismatch for {source_text}: manifest={blob_sha}, actual={actual}"
                    )

        if kind == "skill" and source.parts[:1] == ("skills",) and len(source.parts) >= 3:
            skill_names.add(source.parts[1])

    missing_skills = sorted(REQUIRED_SKILLS - skill_names)
    extra_skills = sorted(skill_names - REQUIRED_SKILLS)
    if missing_skills:
        errors.append("missing required skills: " + ", ".join(missing_skills))
    if extra_skills:
        errors.append("unexpected skills in release payload: " + ", ".join(extra_skills))

    for required_license in ("LICENSE", "LICENSES/mattpocock-skills-MIT.txt"):
        if required_license not in included_paths:
            errors.append(f"release payload must include {required_license}")

    entry_skill = manifest.get("entry_skill")
    if entry_skill not in included_paths:
        errors.append("entry_skill must be included in files")

    if verify_source_files:
        for path in sorted(included_paths):
            if not path.startswith("skills/"):
                continue
            skill_text = (repo_root / path).read_text(encoding="utf-8")
            for pointer in POINTER_RE.findall(skill_text):
                if pointer not in included_paths:
                    errors.append(f"{path}: context pointer missing from payload: {pointer}")

    return errors


def _verify_installed_file(path: Path, expected_blob: str) -> None:
    if not path.is_file():
        raise ReleaseError(f"installed file missing: {path}")
    actual = git_blob_sha(path.read_bytes())
    if actual != expected_blob:
        raise ReleaseError(
            f"installed file blob mismatch: {path}; expected={expected_blob}; actual={actual}"
        )


def verify_installed_bundle(destination: Path, manifest: dict[str, Any]) -> None:
    for entry in manifest["files"]:
        _verify_installed_file(destination / entry["destination"], entry["git_blob_sha"])


def install_from_local_source(
    *,
    source_root: Path,
    manifest_path: Path,
    destination: Path,
    revision: str,
) -> str:
    if not REVISION_RE.fullmatch(revision):
        raise ReleaseError("revision must be an exact 40-character lowercase hexadecimal commit")

    errors = validate_manifest(source_root, manifest_path, verify_source_files=True)
    if errors:
        raise ReleaseError("; ".join(errors))
    manifest = load_json(manifest_path)
    manifest_blob = git_blob_sha(manifest_path.read_bytes())
    lock_path = destination / ".workflow-skills.lock.json"

    if destination.is_dir() and lock_path.is_file():
        lock = load_json(lock_path)
        if (
            lock.get("source_repository") == manifest["source_repository"]
            and lock.get("revision") == revision
            and lock.get("manifest_git_blob_sha") == manifest_blob
        ):
            verify_installed_bundle(destination, manifest)
            return "UNCHANGED"

    staging = destination.parent / f".{destination.name}.staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    try:
        for entry in manifest["files"]:
            source = source_root / entry["path"]
            target = staging / entry["destination"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            _verify_installed_file(target, entry["git_blob_sha"])

        lock = {
            "schema_version": "1.0.0",
            "source_repository": manifest["source_repository"],
            "revision": revision,
            "manifest_path": manifest_path.relative_to(source_root).as_posix(),
            "manifest_git_blob_sha": manifest_blob,
            "install_root": manifest["install_root"],
            "release_version": manifest["release_version"],
            "installed_file_count": len(manifest["files"]),
            "installed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        (staging / ".workflow-skills.lock.json").write_text(
            json.dumps(lock, indent=2) + "\n", encoding="utf-8"
        )
        verify_installed_bundle(staging, manifest)

        backup = destination.parent / f".{destination.name}.backup"
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            destination.rename(backup)
        staging.rename(destination)
        if backup.exists():
            shutil.rmtree(backup)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return "INSTALLED"


def build_native_bundles(repo_root: Path, manifest_path: Path, output: Path) -> list[Path]:
    errors = validate_manifest(repo_root, manifest_path, verify_source_files=True)
    if errors:
        raise ReleaseError("; ".join(errors))
    manifest = load_json(manifest_path)

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    supporting = [entry for entry in manifest["files"] if entry["kind"] != "skill"]
    bundles: list[Path] = []
    for entry in manifest["files"]:
        if entry["kind"] != "skill":
            continue
        skill_name = PurePosixPath(entry["path"]).parts[1]
        bundle = output / skill_name
        bundle.mkdir(parents=True)
        shutil.copyfile(repo_root / entry["path"], bundle / "SKILL.md")
        for support in supporting:
            target = bundle / support["destination"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(repo_root / support["path"], target)
        bundles.append(bundle)
    return bundles

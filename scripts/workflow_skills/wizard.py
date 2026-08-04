from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

STAGE_TYPES = {"open_url", "capture", "command", "pause"}
DESTINATIONS = {"env", "github_secret", "github_variable", "none"}
NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
DANGEROUS_COMMAND_TEXT = re.compile(r"[;&|`><\r\n]|\$\(|Invoke-Expression|\biex\b", re.IGNORECASE)
SECRET_LIKE = re.compile(
    r"(?:ghp_|github_pat_|sk-[A-Za-z0-9]|AKIA[0-9A-Z]|BEGIN (?:RSA |EC )?PRIVATE KEY)",
    re.IGNORECASE,
)


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("wizard manifest must be a JSON object")
    return data


def validate_manifest(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "title", "repository", "stages"}
    missing = sorted(required - data.keys())
    if missing:
        return ["missing required fields: " + ", ".join(missing)]

    if not isinstance(data.get("title"), str) or not data["title"].strip():
        errors.append("title must be a non-empty string")
    if not isinstance(data.get("repository"), str) or not REPO_RE.match(data["repository"]):
        errors.append("repository must be owner/name")

    raw = json.dumps(data, ensure_ascii=False)
    if SECRET_LIKE.search(raw):
        errors.append("manifest appears to contain a credential/private key")

    stages = data.get("stages")
    if not isinstance(stages, list) or not stages:
        return errors + ["stages must be a non-empty list"]

    ids: set[str] = set()
    names: set[str] = set()
    for index, stage in enumerate(stages, start=1):
        prefix = f"stage {index}"
        if not isinstance(stage, dict):
            errors.append(f"{prefix} must be an object")
            continue
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id.strip():
            errors.append(f"{prefix}.id is required")
        elif stage_id in ids:
            errors.append(f"{prefix}.id is duplicated: {stage_id}")
        else:
            ids.add(stage_id)
        if not isinstance(stage.get("title"), str) or not stage["title"].strip():
            errors.append(f"{prefix}.title is required")
        stage_type = stage.get("type")
        if stage_type not in STAGE_TYPES:
            errors.append(f"{prefix}.type must be one of {sorted(STAGE_TYPES)}")
            continue

        if stage_type == "open_url":
            url = stage.get("url")
            if not isinstance(url, str) or not re.match(r"^https?://", url):
                errors.append(f"{prefix}.url must be an http/https URL")
        elif stage_type == "pause":
            seconds = stage.get("seconds")
            if not isinstance(seconds, int) or not 1 <= seconds <= 3600:
                errors.append(f"{prefix}.seconds must be an integer from 1 to 3600")
        elif stage_type == "capture":
            name = stage.get("name")
            if not isinstance(name, str) or not NAME_RE.match(name):
                errors.append(f"{prefix}.name must match {NAME_RE.pattern}")
            elif name in names:
                errors.append(f"{prefix}.name is duplicated: {name}")
            else:
                names.add(name)
            if not isinstance(stage.get("prompt"), str) or not stage["prompt"].strip():
                errors.append(f"{prefix}.prompt is required")
            if not isinstance(stage.get("secret"), bool):
                errors.append(f"{prefix}.secret must be boolean")
            destinations = stage.get("destinations")
            if not isinstance(destinations, list) or not destinations:
                errors.append(f"{prefix}.destinations must be non-empty")
                destinations = []
            for d_index, destination in enumerate(destinations, start=1):
                d_prefix = f"{prefix}.destinations[{d_index}]"
                if not isinstance(destination, dict):
                    errors.append(f"{d_prefix} must be an object")
                    continue
                d_type = destination.get("type")
                if d_type not in DESTINATIONS:
                    errors.append(f"{d_prefix}.type is invalid")
                    continue
                if stage.get("secret") is True and d_type == "github_variable":
                    errors.append(f"{d_prefix}: a secret cannot be stored as github_variable")
                if stage.get("secret") is False and d_type == "github_secret":
                    errors.append(f"{d_prefix}: a public value should not be stored as github_secret")
                if d_type == "env":
                    path = destination.get("path")
                    if not isinstance(path, str) or not path.strip():
                        errors.append(f"{d_prefix}.path is required")
                if d_type in {"github_secret", "github_variable"}:
                    repo = destination.get("repository")
                    if not isinstance(repo, str) or not REPO_RE.match(repo):
                        errors.append(f"{d_prefix}.repository must be owner/name")
        elif stage_type == "command":
            program = stage.get("program")
            if not isinstance(program, str) or not program.strip():
                errors.append(f"{prefix}.program is required")
            elif DANGEROUS_COMMAND_TEXT.search(program):
                errors.append(f"{prefix}.program contains prohibited shell text")
            arguments = stage.get("arguments")
            if not isinstance(arguments, list) or not all(isinstance(x, str) for x in arguments):
                errors.append(f"{prefix}.arguments must be a string list")
                arguments = []
            for argument in arguments:
                if DANGEROUS_COMMAND_TEXT.search(argument):
                    errors.append(f"{prefix}.arguments contains prohibited shell text: {argument!r}")
            exit_codes = stage.get("expected_exit_codes")
            if not isinstance(exit_codes, list) or not exit_codes or not all(
                isinstance(code, int) for code in exit_codes
            ):
                errors.append(f"{prefix}.expected_exit_codes must be a non-empty integer list")
            irreversible = stage.get("irreversible")
            if not isinstance(irreversible, bool):
                errors.append(f"{prefix}.irreversible must be boolean")
            if irreversible is True:
                phrase = stage.get("confirmation_phrase")
                rollback = stage.get("rollback")
                if not isinstance(phrase, str) or len(phrase.strip()) < 4:
                    errors.append(f"{prefix}.confirmation_phrase is required for irreversible work")
                if not isinstance(rollback, str) or not rollback.strip():
                    errors.append(f"{prefix}.rollback is required for irreversible work")
    return errors


REQUIRED_SCRIPT_PATTERNS = {
    "PowerShell 7 requirement": r"#requires\s+-Version\s+7\.0",
    "advanced binding": r"\[CmdletBinding\(SupportsShouldProcess\s*=\s*\$true\)\]",
    "strict mode": r"Set-StrictMode\s+-Version\s+Latest",
    "stop on error": r"\$ErrorActionPreference\s*=\s*'Stop'",
    "secure input": r"Read-Host\s+\$Prompt\s+-AsSecureString",
    "memory zeroing": r"ZeroFreeBSTR",
    "stdin GitHub secret": r"\$Value\s*\|\s*&\s*gh\s+secret\s+set",
    "idempotent env upsert": r"function\s+Set-EnvValue",
    "irreversible confirmation": r"function\s+Confirm-IrreversibleAction",
    "reviewed command invocation": r"&\s+\$Program\s+@Arguments",
    "URL opening": r"Start-Process\s+\$uri\.AbsoluteUri",
}

PROHIBITED_SCRIPT_PATTERNS = {
    "Invoke-Expression": r"\bInvoke-Expression\b",
    "iex alias": r"(?im)^\s*iex(?:\s|$)",
    "plaintext secure-string conversion helper": r"ConvertFrom-SecureString\s+.*-AsPlainText",
    "secret on gh command line": r"gh\s+secret\s+set[^\r\n]*(?:--body|-b)\s+\$",
}


def validate_script(text: str) -> list[str]:
    errors: list[str] = []
    for name, pattern in REQUIRED_SCRIPT_PATTERNS.items():
        if not re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            errors.append(f"missing required script behavior: {name}")
    for name, pattern in PROHIBITED_SCRIPT_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            errors.append(f"prohibited script behavior: {name}")
    return errors

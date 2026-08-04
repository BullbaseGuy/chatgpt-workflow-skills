from __future__ import annotations

import copy
import unittest
from pathlib import Path

from scripts.workflow_skills.wizard import load_manifest, validate_manifest, validate_script


class WizardManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path = Path("examples/manual-wizard/stages.example.json")
        cls.valid = load_manifest(cls.path)

    def test_valid_manifest(self) -> None:
        self.assertEqual(validate_manifest(copy.deepcopy(self.valid)), [])

    def test_secret_cannot_be_github_variable(self) -> None:
        data = copy.deepcopy(self.valid)
        capture = next(stage for stage in data["stages"] if stage.get("secret") is True)
        capture["destinations"] = [
            {"type": "github_variable", "repository": "BullbaseGuy/example-repository"}
        ]
        errors = validate_manifest(data)
        self.assertTrue(any("cannot be stored as github_variable" in error for error in errors))

    def test_irreversible_command_requires_confirmation_and_rollback(self) -> None:
        data = copy.deepcopy(self.valid)
        command = next(stage for stage in data["stages"] if stage["type"] == "command")
        command["irreversible"] = True
        errors = validate_manifest(data)
        self.assertTrue(any("confirmation_phrase" in error for error in errors))
        self.assertTrue(any("rollback" in error for error in errors))

    def test_shell_metacharacter_is_rejected(self) -> None:
        data = copy.deepcopy(self.valid)
        command = next(stage for stage in data["stages"] if stage["type"] == "command")
        command["arguments"].append("; Remove-Item -Recurse .")
        errors = validate_manifest(data)
        self.assertTrue(any("prohibited shell text" in error for error in errors))

    def test_credential_like_text_is_rejected(self) -> None:
        data = copy.deepcopy(self.valid)
        data["example"] = "github_pat_NOT_A_REAL_BUT_FORBIDDEN_SAMPLE"
        self.assertIn(
            "manifest appears to contain a credential/private key",
            validate_manifest(data),
        )


class WizardScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = Path("templates/manual-wizard.template.ps1").read_text(encoding="utf-8")

    def test_template_passes_static_safety(self) -> None:
        self.assertEqual(validate_script(self.text), [])

    def test_invoke_expression_is_rejected(self) -> None:
        errors = validate_script(self.text + "\nInvoke-Expression $command\n")
        self.assertIn("prohibited script behavior: Invoke-Expression", errors)

    def test_secret_body_argument_is_rejected(self) -> None:
        errors = validate_script(self.text + "\ngh secret set NAME --body $secret\n")
        self.assertIn("prohibited script behavior: secret on gh command line", errors)


if __name__ == "__main__":
    unittest.main()

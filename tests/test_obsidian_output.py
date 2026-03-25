from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from mimir_skills.cli import main as cli_main
from mimir_skills import obsidian_output


class ObsidianConfigCommandTests(unittest.TestCase):
    def test_cli_set_reports_saves_project_local_preference(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "obsidian-config",
                        "set-reports",
                        "--project-dir",
                        tempdir,
                    ]
                )

            self.assertEqual(exit_code, 0)
            config_path = Path(tempdir) / ".ai" / "local" / "obsidian-output.json"
            self.assertTrue(config_path.exists())
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["mode"], "reports")
            self.assertEqual(payload["vault_path"], "")
            self.assertIn(".ai/records/reports/", stdout.getvalue())

    def test_cli_set_vault_saves_project_local_preference(self) -> None:
        with TemporaryDirectory() as tempdir:
            vault_dir = Path(tempdir) / "vault"
            vault_dir.mkdir()

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "obsidian-config",
                        "set-vault",
                        str(vault_dir),
                        "--project-dir",
                        tempdir,
                    ]
                )

            self.assertEqual(exit_code, 0)
            config_path = Path(tempdir) / ".ai" / "local" / "obsidian-output.json"
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["mode"], "vault")
            self.assertEqual(payload["vault_path"], str(vault_dir.resolve()))
            self.assertIn(str(vault_dir.resolve()), stdout.getvalue())

    def test_cli_clear_removes_saved_preference(self) -> None:
        with TemporaryDirectory() as tempdir:
            obsidian_output.save_reports_preference(Path(tempdir))

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "obsidian-config",
                        "clear",
                        "--project-dir",
                        tempdir,
                    ]
                )

            self.assertEqual(exit_code, 0)
            config_path = Path(tempdir) / ".ai" / "local" / "obsidian-output.json"
            self.assertFalse(config_path.exists())
            self.assertIn("Cleared project-local Obsidian output preference", stdout.getvalue())


class ObsidianOutputResolutionTests(unittest.TestCase):
    def test_preferred_output_path_defaults_to_reports(self) -> None:
        with TemporaryDirectory() as tempdir:
            record_path = Path(tempdir) / ".ai" / "records" / "decisions" / "dec-test.json"
            record_path.parent.mkdir(parents=True, exist_ok=True)
            record_path.write_text("{}", encoding="utf-8")

            output_path = obsidian_output.preferred_output_path(record_path, "dec-test.md")

            self.assertEqual(output_path, Path(tempdir) / ".ai" / "records" / "reports" / "dec-test.md")

    def test_preferred_output_path_uses_saved_vault_preference(self) -> None:
        with TemporaryDirectory() as tempdir:
            project_dir = Path(tempdir)
            vault_dir = project_dir / "vault"
            vault_dir.mkdir()
            obsidian_output.save_vault_preference(vault_dir, project_dir)

            record_path = project_dir / ".ai" / "records" / "decisions" / "dec-test.json"
            record_path.parent.mkdir(parents=True, exist_ok=True)
            record_path.write_text("{}", encoding="utf-8")

            output_path = obsidian_output.preferred_output_path(record_path, "dec-test.md")

            self.assertEqual(output_path, vault_dir / "dec-test.md")


if __name__ == "__main__":
    unittest.main()

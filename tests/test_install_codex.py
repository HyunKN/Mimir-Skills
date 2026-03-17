from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from mimir_skills.cli import main as cli_main
from mimir_skills.install_codex import main as install_main


class InstallCommandTests(unittest.TestCase):
    def test_cli_install_defaults_to_codex_target(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install",
                        "--codex-home",
                        tempdir,
                        "--workflows",
                        "prepare-handoff",
                    ]
                )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / "skills"
            support_root = skills_root / "mimir-skills-support"

            self.assertTrue((skills_root / "prepare-handoff" / "SKILL.md").exists())
            self.assertTrue((skills_root / "handoff-context" / "SKILL.md").exists())
            self.assertTrue((skills_root / "decision-capture" / "SKILL.md").exists())
            self.assertTrue((skills_root / "decision-core" / "SKILL.md").exists())
            self.assertFalse((skills_root / "write-pr-rationale").exists())
            self.assertTrue((support_root / "install-manifest.json").exists())
            self.assertIn("Installed Mimir-Skills workflows into", stdout.getvalue())

            manifest = json.loads(
                (support_root / "install-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["workflows"], ["prepare-handoff"])

    def test_cli_install_accepts_explicit_codex_target(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install",
                        "codex",
                        "--codex-home",
                        tempdir,
                        "--workflows",
                        "write-pr-rationale",
                    ]
                )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / "skills"
            self.assertTrue((skills_root / "write-pr-rationale" / "SKILL.md").exists())
            self.assertTrue((skills_root / "pr-rationale" / "SKILL.md").exists())
            self.assertIn("- write-pr-rationale", stdout.getvalue())

    def test_legacy_script_main_still_installs(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = install_main(
                    [
                        "--codex-home",
                        tempdir,
                        "--workflows",
                        "capture-ci-investigation",
                    ]
                )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / "skills"
            self.assertTrue(
                (skills_root / "capture-ci-investigation" / "SKILL.md").exists()
            )
            self.assertTrue((skills_root / "ci-rationale" / "SKILL.md").exists())
            self.assertIn("Installed support assets under", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()

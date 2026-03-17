from __future__ import annotations

import io
import json
import os
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from mimir_skills.cli import main as cli_main


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
            self.assertIn("write-pr-rationale", stdout.getvalue())

    def test_cli_install_accepts_target_flag(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install",
                        "--target",
                        "codex",
                        "--codex-home",
                        tempdir,
                        "--workflows",
                        "prepare-handoff",
                    ]
                )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / "skills"
            self.assertTrue((skills_root / "prepare-handoff" / "SKILL.md").exists())
            self.assertIn("target: codex", stdout.getvalue())

    def test_cli_install_claude_target(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install",
                        "--target",
                        "claude",
                        "--project-dir",
                        tempdir,
                        "--workflows",
                        "prepare-handoff",
                    ]
                )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / ".claude" / "skills"
            self.assertTrue((skills_root / "prepare-handoff" / "SKILL.md").exists())
            self.assertTrue((skills_root / "decision-core" / "SKILL.md").exists())
            self.assertIn("target: claude", stdout.getvalue())

            manifest = json.loads(
                (skills_root / "mimir-skills-support" / "install-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["target"], "claude")

    def test_cli_install_generic_target(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install",
                        "--target",
                        "generic",
                        "--project-dir",
                        tempdir,
                        "--workflows",
                        "write-pr-rationale",
                    ]
                 )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / ".skills"
            self.assertTrue((skills_root / "write-pr-rationale" / "SKILL.md").exists())
            self.assertTrue((skills_root / "pr-rationale" / "SKILL.md").exists())
            self.assertIn("target: generic", stdout.getvalue())

    def test_auto_detect_claude_target(self) -> None:
        with TemporaryDirectory() as tempdir:
            (Path(tempdir) / ".claude").mkdir()
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install",
                        "--project-dir",
                        tempdir,
                        "--workflows",
                        "prepare-handoff",
                    ]
                )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / ".claude" / "skills"
            self.assertTrue((skills_root / "prepare-handoff" / "SKILL.md").exists())
            self.assertIn("target: claude", stdout.getvalue())

    def test_auto_detect_codex_target(self) -> None:
        with TemporaryDirectory() as tempdir:
            project_dir = Path(tempdir) / "project"
            project_dir.mkdir()
            (project_dir / ".codex").mkdir()
            codex_home = Path(tempdir) / "codex-home"
            old_env = os.environ.get("CODEX_HOME")
            os.environ["CODEX_HOME"] = str(codex_home)
            try:
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    exit_code = cli_main(
                        [
                            "install",
                            "--project-dir",
                            str(project_dir),
                            "--workflows",
                            "prepare-handoff",
                        ]
                    )
            finally:
                if old_env is None:
                    os.environ.pop("CODEX_HOME", None)
                else:
                    os.environ["CODEX_HOME"] = old_env

            self.assertEqual(exit_code, 0)
            self.assertIn("target: codex", stdout.getvalue())

    def test_auto_detect_ambiguous_raises(self) -> None:
        with TemporaryDirectory() as tempdir:
            (Path(tempdir) / ".claude").mkdir()
            (Path(tempdir) / ".codex").mkdir()
            with self.assertRaises(RuntimeError) as ctx:
                cli_main(
                    [
                        "install",
                        "--project-dir",
                        tempdir,
                        "--workflows",
                        "prepare-handoff",
                    ]
                )
            self.assertIn("Both .claude/ and .codex/", str(ctx.exception))

    def test_rewrite_replaces_example_paths(self) -> None:
        with TemporaryDirectory() as tempdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install",
                        "--target",
                        "claude",
                        "--project-dir",
                        tempdir,
                        "--workflows",
                        "prepare-handoff",
                    ]
                )

            self.assertEqual(exit_code, 0)
            skills_root = Path(tempdir) / ".claude" / "skills"
            skill_text = (skills_root / "prepare-handoff" / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("../../examples/", skill_text)
            self.assertNotIn("../../../examples/", skill_text)


if __name__ == "__main__":
    unittest.main()

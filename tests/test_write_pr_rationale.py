from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from mimir_skills.workflows.write_pr_rationale import collect_context, generate_main


class CollectContextTests(unittest.TestCase):
    @patch("mimir_skills.workflows.write_pr_rationale.collect_branch_range")
    @patch("mimir_skills.workflows.write_pr_rationale.collect_recent_commit_details")
    @patch("mimir_skills.workflows.write_pr_rationale.detect_base_ref")
    @patch("mimir_skills.workflows.write_pr_rationale.run_git")
    def test_collect_context_returns_thin_git_snapshot(
        self,
        mock_run_git,
        mock_detect_base_ref,
        mock_collect_recent_commit_details,
        mock_collect_branch_range,
    ) -> None:
        repo_path = Path("C:/repo")

        mock_detect_base_ref.return_value = {
            "candidate": "origin/main",
            "merge_base": "abc1234567890",
            "label": "origin/main@abc1234",
        }
        mock_collect_recent_commit_details.return_value = [
            {
                "full_hash": "abc1234567890",
                "short_hash": "abc1234",
                "subject": "docs: add temporary validation note",
                "files": ["README.md"],
            }
        ]
        mock_collect_branch_range.return_value = {
            "base_ref": "origin/main@abc1234",
            "commit_count": 1,
            "commits": ["abc1234 docs: add temporary validation note"],
            "changed_files": ["README.md"],
            "name_status": ["M\tREADME.md"],
            "diff_stat": ["README.md | 2 ++"],
        }

        def run_git_side_effect(_repo_path: Path, *args: str) -> str:
            mapping = {
                ("rev-parse", "--show-toplevel"): "C:/repo",
                ("branch", "--show-current"): "feature/test",
                ("rev-parse", "--short", "HEAD"): "deadbee",
                ("rev-parse", "HEAD"): "deadbeefcafebabe",
                ("diff", "--name-only"): "docs/quick-start.md\n",
                ("diff", "--cached", "--name-only"): "skills/write-pr-rationale/SKILL.md\n",
                ("ls-files", "--others", "--exclude-standard"): "notes/scratch.md\n",
                ("log", "-n3", "--oneline"): "abc1234 docs: add temporary validation note\n",
                ("diff", "--name-status"): "M\tdocs/quick-start.md\n",
                ("diff", "--stat"): "docs/quick-start.md | 2 ++\n",
                ("diff", "--cached", "--stat"): "skills/write-pr-rationale/SKILL.md | 4 ++--\n",
            }
            return mapping[args]

        mock_run_git.side_effect = run_git_side_effect

        context = collect_context(repo_path, commit_limit=3)

        self.assertEqual(Path(context["repo_root"]), Path("C:/repo"))
        self.assertEqual(context["branch"], "feature/test")
        self.assertEqual(context["head_short"], "deadbee")
        self.assertEqual(context["base_ref"], "origin/main@abc1234")
        self.assertFalse(context["working_tree_clean"])
        self.assertEqual(
            context["diff"]["changed_files"],
            [
                "docs/quick-start.md",
                "notes/scratch.md",
                "skills/write-pr-rationale/SKILL.md",
            ],
        )
        self.assertEqual(context["diff"]["staged_files"], ["skills/write-pr-rationale/SKILL.md"])
        self.assertEqual(context["diff"]["unstaged_files"], ["docs/quick-start.md"])
        self.assertEqual(context["diff"]["untracked_files"], ["notes/scratch.md"])
        self.assertIn("??\tnotes/scratch.md", context["diff"]["name_status"])
        self.assertEqual(
            context["branch_range"]["commits"],
            ["abc1234 docs: add temporary validation note"],
        )
        self.assertEqual(
            context["recent_commit_details"][0]["subject"],
            "docs: add temporary validation note",
        )


class GenerateMainTests(unittest.TestCase):
    def test_generate_main_prints_deprecation_note(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = generate_main(["--repo", "."])

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("# write-pr-rationale helper deprecated", output)
        self.assertIn("skills/write-pr-rationale/SKILL.md", output)
        self.assertIn("collect_pr_context.py --repo <path> --output pr-context.json", output)

    def test_generate_main_accepts_legacy_inputs_and_mentions_explicit_context(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = generate_main(
                [
                    "--repo",
                    ".",
                    "--context-json",
                    "pr-context.json",
                    "--why",
                    "Direction Reset skill-first codification",
                ]
            )

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("`pr-context.json`", output)
        self.assertIn("Preserve any explicit why", output)

    def test_generate_main_writes_note_to_output_path(self) -> None:
        with TemporaryDirectory() as tempdir:
            output_path = Path(tempdir) / "note.md"

            exit_code = generate_main(["--repo", ".", "--output", str(output_path)])

            self.assertEqual(exit_code, 0)
            payload = output_path.read_text(encoding="utf-8")
            self.assertIn("# write-pr-rationale helper deprecated", payload)
            self.assertIn("scripts/generate_pr_rationale.py", payload)


if __name__ == "__main__":
    unittest.main()

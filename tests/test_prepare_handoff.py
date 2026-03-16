from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from mimir_skills.workflows.prepare_handoff import (
    collect_context,
    generate_main,
    parse_porcelain,
)


class ParsePorcelainTests(unittest.TestCase):
    def test_parse_porcelain_keeps_raw_codes_and_paths(self) -> None:
        entries = parse_porcelain(["M  README.md", "?? notes/next-step.md"])

        self.assertEqual(entries[0]["path"], "README.md")
        self.assertEqual(entries[0]["staged_code"], "M")
        self.assertEqual(entries[0]["unstaged_code"], " ")
        self.assertEqual(entries[1]["path"], "notes/next-step.md")
        self.assertEqual(entries[1]["staged_labels"], ["untracked"])


class CollectContextTests(unittest.TestCase):
    @patch("mimir_skills.workflows.prepare_handoff.collect_branch_range")
    @patch("mimir_skills.workflows.prepare_handoff.collect_recent_commit_details")
    @patch("mimir_skills.workflows.prepare_handoff.detect_base_ref")
    @patch("mimir_skills.workflows.prepare_handoff.run_git")
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
                "subject": "docs: refresh handoff note",
                "files": ["README.md"],
            }
        ]
        mock_collect_branch_range.return_value = {
            "base_ref": "origin/main@abc1234",
            "commit_count": 1,
            "commits": ["abc1234 docs: refresh handoff note"],
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
                ("status", "--short"): "M  README.md\n?? notes/next-step.md\n",
                ("diff", "--cached", "--name-only"): "README.md\n",
                ("diff", "--name-only"): "docs/quick-start.md\n",
                ("ls-files", "--others", "--exclude-standard"): "notes/next-step.md\n",
                ("log", "-n3", "--oneline"): "abc1234 docs: refresh handoff note\n",
                ("diff", "--cached", "--stat"): "README.md | 2 ++\n",
                ("diff", "--stat"): "docs/quick-start.md | 1 +\n",
            }
            return mapping[args]

        mock_run_git.side_effect = run_git_side_effect

        context = collect_context(repo_path, commit_limit=3)

        self.assertEqual(Path(context["repo_root"]), Path("C:/repo"))
        self.assertEqual(context["branch"], "feature/test")
        self.assertEqual(context["head_short"], "deadbee")
        self.assertEqual(context["base_ref"], "origin/main@abc1234")
        self.assertFalse(context["is_worktree_clean"])
        self.assertEqual(context["status"]["staged_count"], 1)
        self.assertEqual(context["status"]["unstaged_count"], 1)
        self.assertEqual(context["status"]["untracked_count"], 1)
        self.assertEqual(context["status"]["entries"][0]["raw"], "M  README.md")
        self.assertEqual(
            context["diff"]["all_changed_files"],
            ["README.md", "docs/quick-start.md", "notes/next-step.md"],
        )
        self.assertEqual(
            context["branch_range"]["commits"],
            ["abc1234 docs: refresh handoff note"],
        )
        self.assertEqual(
            context["recent_commit_details"][0]["subject"],
            "docs: refresh handoff note",
        )


class GenerateMainTests(unittest.TestCase):
    def test_generate_main_prints_deprecation_note(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = generate_main(["--repo", "."])

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("# prepare-handoff helper deprecated", output)
        self.assertIn("skills/prepare-handoff/SKILL.md", output)
        self.assertIn("collect_git_context.py --repo <path> --output handoff-context.json", output)

    def test_generate_main_accepts_legacy_inputs_and_mentions_explicit_context(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = generate_main(
                [
                    "--repo",
                    ".",
                    "--context-json",
                    "handoff-context.json",
                    "--validation",
                    "manual smoke",
                ]
            )

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("`handoff-context.json`", output)
        self.assertIn("Preserve any explicit validation, blocker, risk, next-step, or evidence input", output)

    def test_generate_main_writes_note_to_output_path(self) -> None:
        with TemporaryDirectory() as tempdir:
            output_path = Path(tempdir) / "note.md"

            exit_code = generate_main(["--repo", ".", "--output", str(output_path)])

            self.assertEqual(exit_code, 0)
            payload = output_path.read_text(encoding="utf-8")
            self.assertIn("# prepare-handoff helper deprecated", payload)
            self.assertIn("scripts/generate_handoff.py", payload)


if __name__ == "__main__":
    unittest.main()

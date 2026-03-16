from __future__ import annotations

import unittest

from mimir_skills.workflows.write_pr_rationale import (
    analysis_inputs,
    default_reviewer_notes,
    default_validation_lines,
    default_why_lines,
    infer_change_goal,
    infer_signals,
    render_pr_rationale,
)


def make_context(
    *,
    repo_name: str = "Mimir-Skills",
    branch: str = "feature/test",
    base_ref: str = "origin/main@abc1234",
    generated_at: str = "2026-03-16T00:00:00+00:00",
    head_short: str = "deadbee",
    diff: dict | None = None,
    branch_range: dict | None = None,
    recent_commits: list[str] | None = None,
    recent_commit_details: list[dict] | None = None,
) -> dict:
    return {
        "repo_name": repo_name,
        "branch": branch,
        "base_ref": base_ref,
        "generated_at": generated_at,
        "head_short": head_short,
        "diff": diff
        or {
            "changed_files": [],
            "name_status": [],
            "untracked_files": [],
            "diff_stat": [],
            "staged_diff_stat": [],
        },
        "branch_range": branch_range
        or {
            "base_ref": base_ref,
            "changed_files": [],
            "name_status": [],
            "diff_stat": [],
            "commits": [],
        },
        "recent_commits": recent_commits or [],
        "recent_commit_details": recent_commit_details or [],
    }


class InferSignalsTests(unittest.TestCase):
    def test_infer_signals_recognizes_repo_specific_surfaces(self) -> None:
        files = [
            "README.md",
            "adapters/codex/scripts/install_codex_skills.py",
            "mimir_skills/workflows/write_pr_rationale.py",
        ]
        subjects = ["refactor: rename project and shared runtime to Mimir-Skills"]

        signals = infer_signals(files, subjects)

        self.assertIn("docs", signals)
        self.assertIn("adapter", signals)
        self.assertIn("workflow", signals)
        self.assertIn("runtime", signals)
        self.assertIn("rename", signals)

    def test_infer_change_goal_prefers_rename_alignment_summary(self) -> None:
        signals = {"rename", "workflow", "adapter", "docs"}

        goal = infer_change_goal(signals)

        self.assertEqual(
            goal,
            "align the rename across the runtime surface, installed path, and published guidance",
        )

    def test_infer_signals_treats_ci_workflow_files_as_ci_not_generic_config(self) -> None:
        signals = infer_signals([".github/workflows/ci.yml"], [])

        self.assertIn("ci", signals)
        self.assertNotIn("config", signals)


class AnalysisInputsTests(unittest.TestCase):
    def test_analysis_inputs_prefers_working_tree_diff_without_recent_subject_fallback(self) -> None:
        context = make_context(
            diff={
                "changed_files": ["mimir_skills/workflows/write_pr_rationale.py"],
                "name_status": ["M\tmimir_skills/workflows/write_pr_rationale.py"],
                "untracked_files": [],
                "diff_stat": [],
                "staged_diff_stat": [],
            },
            recent_commits=["a98a7bf refactor: rename project and shared runtime to Mimir-Skills"],
            recent_commit_details=[
                {
                    "short_hash": "a98a7bf",
                    "subject": "refactor: rename project and shared runtime to Mimir-Skills",
                    "files": ["README.md"],
                }
            ],
        )

        source_label, files, subjects = analysis_inputs(context["diff"], context["branch_range"], context)

        self.assertEqual(source_label, "the current working-tree diff")
        self.assertEqual(files, ["mimir_skills/workflows/write_pr_rationale.py"])
        self.assertEqual(subjects, [])

    def test_analysis_inputs_prefers_branch_range_over_recent_commits(self) -> None:
        context = make_context(
            branch_range={
                "base_ref": "origin/main@abc1234",
                "changed_files": ["README.md"],
                "name_status": ["M\tREADME.md"],
                "diff_stat": ["README.md | 2 ++"],
                "commits": ["bd4ac73 docs: add temporary validation note"],
            },
            recent_commits=["a98a7bf older recent commit"],
            recent_commit_details=[
                {"short_hash": "a98a7bf", "subject": "older recent commit", "files": ["docs/quick-start.md"]}
            ],
        )

        source_label, files, subjects = analysis_inputs(context["diff"], context["branch_range"], context)

        self.assertEqual(source_label, "committed branch-range context")
        self.assertEqual(files, ["README.md"])
        self.assertEqual(subjects, ["docs: add temporary validation note"])


class DefaultSectionTests(unittest.TestCase):
    def test_default_why_lines_flag_inference_as_tentative(self) -> None:
        context = make_context(
            branch_range={
                "base_ref": "origin/main@abc1234",
                "changed_files": ["README.md"],
                "name_status": ["M\tREADME.md"],
                "diff_stat": ["README.md | 2 ++"],
                "commits": ["bd4ac73 docs: add temporary validation note"],
            }
        )

        lines = default_why_lines(context["diff"], context["branch_range"], context)

        self.assertIn(
            "- Inferred from committed branch-range context: this branch appears to tighten the published guidance around the current behavior or product direction.",
            lines,
        )
        self.assertTrue(any("Replace or tighten this inferred rationale" in line for line in lines))

    def test_default_validation_lines_for_docs_only_branch_are_specific(self) -> None:
        context = make_context(
            branch_range={
                "base_ref": "origin/main@abc1234",
                "changed_files": ["README.md"],
                "name_status": ["M\tREADME.md"],
                "diff_stat": ["README.md | 2 ++"],
                "commits": ["bd4ac73 docs: add temporary validation note"],
            }
        )

        lines = default_validation_lines(context["diff"], context["branch_range"], context)

        self.assertEqual(lines[0], "- No explicit validation notes were provided for this draft.")
        self.assertIn(
            "- If this is guidance-only work, confirm that commands, paths, and examples still match the current implementation.",
            lines,
        )

    def test_default_reviewer_notes_for_docs_only_branch_range_are_specific(self) -> None:
        context = make_context(
            branch_range={
                "base_ref": "origin/main@abc1234",
                "changed_files": ["README.md"],
                "name_status": ["M\tREADME.md"],
                "diff_stat": ["README.md | 2 ++"],
                "commits": ["bd4ac73 docs: add temporary validation note"],
            }
        )

        lines = default_reviewer_notes(context["diff"], context["branch_range"], context)

        self.assertIn(
            "- The working tree is clean, so review the committed branch-range changes above rather than expecting uncommitted diffs.",
            lines,
        )
        self.assertIn(
            "- Confirm that README, skill instructions, and examples describe the same behavior the code now implements.",
            lines,
        )

    def test_default_reviewer_notes_for_ci_workflow_change_do_not_add_config_note(self) -> None:
        context = make_context(
            diff={
                "changed_files": [".github/workflows/ci.yml"],
                "name_status": ["M\t.github/workflows/ci.yml"],
                "untracked_files": [],
                "diff_stat": [".github/workflows/ci.yml | 3 +++"],
                "staged_diff_stat": [],
            }
        )

        lines = default_reviewer_notes(context["diff"], context["branch_range"], context)

        self.assertIn(
            "- Review whether the workflow change preserves failure visibility instead of only making the pipeline look greener.",
            lines,
        )
        self.assertNotIn(
            "- Check compatibility assumptions, migration cost, and rollback safety for the dependency or config change.",
            lines,
        )


class RenderPrRationaleTests(unittest.TestCase):
    def test_render_pr_rationale_prefers_explicit_why_over_inference(self) -> None:
        context = make_context(
            diff={
                "changed_files": ["mimir_skills/workflows/write_pr_rationale.py"],
                "name_status": ["M\tmimir_skills/workflows/write_pr_rationale.py"],
                "untracked_files": [],
                "diff_stat": ["mimir_skills/workflows/write_pr_rationale.py | 2 ++"],
                "staged_diff_stat": [],
            }
        )

        markdown = render_pr_rationale(
            context,
            title=None,
            why_items=["Phase 1 clean-state enhancement"],
            validations=[],
            reviewer_notes=[],
            risks=[],
            evidence=[],
        )

        self.assertIn("- Phase 1 clean-state enhancement", markdown)
        self.assertNotIn("Replace or tighten this inferred rationale", markdown)

    def test_render_pr_rationale_uses_branch_range_commit_section_for_clean_state(self) -> None:
        context = make_context(
            branch_range={
                "base_ref": "origin/main@abc1234",
                "changed_files": ["README.md"],
                "name_status": ["M\tREADME.md"],
                "diff_stat": ["README.md | 2 ++"],
                "commits": ["bd4ac73 docs: add temporary validation note"],
            }
        )

        markdown = render_pr_rationale(
            context,
            title=None,
            why_items=[],
            validations=[],
            reviewer_notes=[],
            risks=[],
            evidence=[],
        )

        self.assertIn("## Commits Since origin/main@abc1234", markdown)
        self.assertIn("`bd4ac73 docs: add temporary validation note`", markdown)
        self.assertIn(
            "this branch appears to tighten the published guidance around the current behavior or product direction",
            markdown,
        )


if __name__ == "__main__":
    unittest.main()

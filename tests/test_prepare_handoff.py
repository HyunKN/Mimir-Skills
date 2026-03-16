from __future__ import annotations

import unittest

from mimir_skills.workflows.prepare_handoff import (
    default_evidence_lines,
    default_next_steps,
    default_risk_lines,
    parse_porcelain,
    render_handoff,
    render_worktree_state,
)


def make_context(
    *,
    repo_name: str = "Mimir-Skills",
    branch: str = "feature/test",
    base_ref: str = "origin/main@abc1234",
    generated_at: str = "2026-03-16T00:00:00+00:00",
    head_short: str = "deadbee",
    status: dict | None = None,
    diff: dict | None = None,
    recent_commits: list[str] | None = None,
    recent_commit_details: list[dict] | None = None,
    branch_range: dict | None = None,
) -> dict:
    return {
        "repo_name": repo_name,
        "branch": branch,
        "base_ref": base_ref,
        "generated_at": generated_at,
        "head_short": head_short,
        "status": status
        or {
            "staged_count": 0,
            "unstaged_count": 0,
            "untracked_count": 0,
            "porcelain": [],
            "entries": [],
        },
        "diff": diff
        or {
            "staged_stat": [],
            "unstaged_stat": [],
            "staged_files": [],
            "unstaged_files": [],
            "untracked_files": [],
            "all_changed_files": [],
        },
        "recent_commits": recent_commits or [],
        "recent_commit_details": recent_commit_details or [],
        "branch_range": branch_range
        or {
            "base_ref": base_ref,
            "changed_files": [],
            "name_status": [],
            "diff_stat": [],
            "commits": [],
        },
    }


class ParsePorcelainTests(unittest.TestCase):
    def test_parse_porcelain_keeps_raw_codes_and_paths(self) -> None:
        entries = parse_porcelain(["M  README.md", "?? notes/next-step.md"])

        self.assertEqual(entries[0]["path"], "README.md")
        self.assertEqual(entries[0]["staged_code"], "M")
        self.assertEqual(entries[0]["unstaged_code"], " ")
        self.assertEqual(entries[1]["path"], "notes/next-step.md")
        self.assertEqual(entries[1]["staged_labels"], ["untracked"])


class RenderWorktreeStateTests(unittest.TestCase):
    def test_render_worktree_state_reports_counts_for_dirty_tree(self) -> None:
        line = render_worktree_state(
            {
                "staged_count": 1,
                "unstaged_count": 2,
                "untracked_count": 1,
                "porcelain": ["M  README.md"],
            }
        )

        self.assertEqual(
            line,
            "- Working tree: not clean (`1` staged, `2` unstaged, `1` untracked)",
        )

    def test_render_worktree_state_reports_clean_tree(self) -> None:
        self.assertEqual(render_worktree_state({"porcelain": []}), "- Working tree: clean")


class DefaultSectionTests(unittest.TestCase):
    def test_default_evidence_lines_for_dirty_tree_use_status_and_diff(self) -> None:
        context = make_context(status={"porcelain": ["M  README.md"]})

        lines = default_evidence_lines(context, context["status"], context["branch_range"])

        self.assertEqual(
            lines,
            ["- Use the current working-tree status and diff summary above as the primary local evidence for this draft."],
        )

    def test_default_evidence_lines_for_recent_commit_fallback_are_explicit(self) -> None:
        context = make_context(
            recent_commit_details=[
                {
                    "short_hash": "abc1234",
                    "subject": "docs: refresh handoff note",
                    "files": ["README.md"],
                }
            ]
        )

        lines = default_evidence_lines(context, context["status"], context["branch_range"])

        self.assertEqual(
            lines,
            [
                "- The working tree and branch-range diff are both clean, so this draft is using recent committed work as fallback evidence.",
            ],
        )

    def test_default_risk_lines_for_dirty_tree_flag_uncommitted_state(self) -> None:
        lines = default_risk_lines(
            {
                "staged_count": 1,
                "unstaged_count": 2,
                "untracked_count": 1,
                "porcelain": ["M  README.md"],
            }
        )

        self.assertEqual(
            lines,
            [
                "- The branch still contains uncommitted changes, so the next owner should verify the final intended state before sharing externally."
            ],
        )

    def test_default_risk_lines_for_clean_tree_flag_missing_context_check(self) -> None:
        lines = default_risk_lines(
            {
                "staged_count": 0,
                "unstaged_count": 0,
                "untracked_count": 0,
                "porcelain": [],
            }
        )

        self.assertEqual(
            lines,
            [
                "- No working-tree changes were detected; verify that any missing context already lives in commits or decision records."
            ],
        )

    def test_default_next_steps_for_dirty_tree_include_commit_and_validation_follow_up(self) -> None:
        steps = default_next_steps(
            {"porcelain": ["M  README.md"]},
            {"all_changed_files": ["README.md"]},
        )

        self.assertIn(
            "- Review the listed changed files and confirm which updates should be committed before handoff.",
            steps,
        )
        self.assertIn(
            "- Re-run any relevant validation and replace the placeholder validation section with concrete results before external sharing.",
            steps,
        )

    def test_default_next_steps_for_clean_tree_stay_checkpoint_oriented(self) -> None:
        steps = default_next_steps({"porcelain": []}, {"all_changed_files": []})

        self.assertEqual(
            steps,
            [
                "- Confirm whether the next owner needs only a clean-state checkpoint or a richer summary of the most recent committed work.",
                "- Add task-specific blockers, risks, and owner notes if this draft is going to another person or agent.",
            ],
        )


class RenderHandoffTests(unittest.TestCase):
    def test_render_handoff_reports_mixed_dirty_state_clearly(self) -> None:
        status = {
            "staged_count": 1,
            "unstaged_count": 2,
            "untracked_count": 1,
            "porcelain": [
                "M  README.md",
                " M docs/workflow-surface.md",
                " M mimir_skills/workflows/prepare_handoff.py",
                "?? notes/next-step.md",
            ],
            "entries": parse_porcelain(
                [
                    "M  README.md",
                    " M docs/workflow-surface.md",
                    " M mimir_skills/workflows/prepare_handoff.py",
                    "?? notes/next-step.md",
                ]
            ),
        }
        diff = {
            "staged_stat": ["README.md | 2 ++", "1 file changed, 2 insertions(+)"],
            "unstaged_stat": [
                "docs/workflow-surface.md | 2 ++",
                "mimir_skills/workflows/prepare_handoff.py | 1 +",
                "2 files changed, 3 insertions(+)",
            ],
            "staged_files": ["README.md"],
            "unstaged_files": [
                "docs/workflow-surface.md",
                "mimir_skills/workflows/prepare_handoff.py",
            ],
            "untracked_files": ["notes/next-step.md"],
            "all_changed_files": [
                "README.md",
                "docs/workflow-surface.md",
                "mimir_skills/workflows/prepare_handoff.py",
                "notes/next-step.md",
            ],
        }
        context = make_context(
            repo_name="handoff-rich",
            branch="phase1-handoff-rich-check",
            head_short="d1292b3",
            status=status,
            diff=diff,
            recent_commits=["d1292b3 test: add write-pr-rationale inference coverage and CI checks"],
        )

        markdown = render_handoff(
            context,
            title=None,
            validations=[],
            blockers=[],
            risks=[],
            next_steps=[],
            evidence=[],
        )

        self.assertIn("- Working tree: not clean (`1` staged, `2` unstaged, `1` untracked)", markdown)
        self.assertIn("- `M  README.md`", markdown)
        self.assertIn("- `M docs/workflow-surface.md`", markdown)
        self.assertIn("- `?? notes/next-step.md`", markdown)
        self.assertIn("### Untracked Files", markdown)
        self.assertIn("- `notes/next-step.md`", markdown)
        self.assertIn("- Staged diff stat:", markdown)
        self.assertIn("- Unstaged diff stat:", markdown)
        self.assertIn(
            "- The branch still contains uncommitted changes, so the next owner should verify the final intended state before sharing externally.",
            markdown,
        )

    def test_render_handoff_uses_clean_state_branch_context_when_available(self) -> None:
        context = make_context(
            branch_range={
                "base_ref": "origin/main@abc1234",
                "changed_files": ["README.md"],
                "name_status": ["M\tREADME.md"],
                "diff_stat": ["README.md | 2 ++"],
                "commits": ["bd4ac73 docs: add temporary validation note"],
            },
            recent_commit_details=[
                {
                    "short_hash": "bd4ac73",
                    "subject": "docs: add temporary validation note",
                    "files": ["README.md"],
                }
            ],
        )

        markdown = render_handoff(
            context,
            title=None,
            validations=[],
            blockers=[],
            risks=[],
            next_steps=[],
            evidence=[],
        )

        self.assertIn(
            "- No working-tree changes were detected, so this draft is using committed branch context.",
            markdown,
        )
        self.assertIn("### Committed Branch Diff Summary", markdown)
        self.assertIn(
            "- The working tree is clean, so this draft is using committed branch-range context as the primary local evidence.",
            markdown,
        )

    def test_render_handoff_uses_recent_commit_fallback_when_no_branch_diff_exists(self) -> None:
        context = make_context(
            recent_commits=["abc1234 docs: refresh handoff note"],
            recent_commit_details=[
                {
                    "short_hash": "abc1234",
                    "subject": "docs: refresh handoff note",
                    "files": ["README.md", "docs/workflow-surface.md"],
                }
            ],
        )

        markdown = render_handoff(
            context,
            title=None,
            validations=[],
            blockers=[],
            risks=[],
            next_steps=[],
            evidence=[],
        )

        self.assertIn(
            "- No committed branch-range diff was detected either, so this draft is falling back to recent committed work.",
            markdown,
        )
        self.assertIn("### Recent Committed Work", markdown)
        self.assertIn(
            "- `abc1234` docs: refresh handoff note",
            markdown,
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from mimir_skills import artifact_titles


ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ArtifactTitleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.decision = {
            "id": "dec-20260320-cache-client-v43-migration-003",
            "timestamp": "2026-03-20T07:45:00Z",
            "task_ref": {
                "title": "Complete synthetic cache client v4.3 migration",
            },
            "decision": "Add tls.ca_bundle configuration and upgrade the synthetic dependency.",
            "follow_up": ["Promote the repeated TLS contract lesson into validated memory."],
            "supersedes": ["dec-20260312-cache-client-pin-001"],
        }
        self.memory = {
            "id": "mem-20260320-cache-client-tls-contract-001",
            "status": "validated",
            "statement": "Synthetic services using acme-cache-client v4.3+ should add tls.ca_bundle first.",
            "scope": "Synthetic cache client upgrades with verified TLS enabled.",
            "created_at": "2026-03-20T08:10:00Z",
            "validated_at": "2026-03-20T08:42:00Z",
            "source_decision_ids": [
                "dec-20260312-cache-client-pin-001",
                "dec-20260320-cache-client-v43-migration-003",
            ],
        }

    def test_decision_titles_include_date_kind_and_subject(self) -> None:
        self.assertEqual(
            artifact_titles.decision_note_title(self.decision),
            "[2026-03-20] Decision - Complete synthetic cache client v4.3 migration",
        )
        self.assertEqual(
            artifact_titles.decision_summary_title(self.decision),
            "[2026-03-20] Decision Summary - Complete synthetic cache client v4.3 migration",
        )

    def test_memory_title_uses_date_kind_and_humanized_subject(self) -> None:
        self.assertEqual(
            artifact_titles.memory_note_title(self.memory),
            "[2026-03-20] Validated Memory - Cache Client TLS Contract",
        )

    def test_render_summary_uses_human_friendly_heading(self) -> None:
        module = load_module(
            "render_summary_module",
            ROOT / "skills" / "_internal" / "decision-capture" / "scripts" / "render_summary.py",
        )

        markdown = module.render_summary(self.decision)

        self.assertTrue(
            markdown.startswith(
                "# [2026-03-20] Decision Summary - Complete synthetic cache client v4.3 migration\n"
            )
        )

    def test_render_decision_note_uses_human_friendly_heading(self) -> None:
        module = load_module(
            "render_decision_note_module",
            ROOT / "skills" / "_internal" / "decision-capture" / "scripts" / "render_obsidian_note.py",
        )

        markdown = module.render_note(self.decision, Path(".ai/records/decisions/dec-20260320.json"))

        self.assertTrue(
            markdown.startswith(
                "# [2026-03-20] Decision - Complete synthetic cache client v4.3 migration\n"
            )
        )

    def test_render_memory_note_uses_human_friendly_heading(self) -> None:
        module = load_module(
            "render_memory_note_module",
            ROOT / "skills" / "_internal" / "memory-promote" / "scripts" / "render_obsidian_note.py",
        )

        markdown = module.render_note(
            self.memory,
            Path(".ai/records/memories/validated/mem-20260320-cache-client-tls-contract-001.json"),
        )

        self.assertTrue(
            markdown.startswith(
                "# [2026-03-20] Validated Memory - Cache Client TLS Contract\n"
            )
        )


if __name__ == "__main__":
    unittest.main()

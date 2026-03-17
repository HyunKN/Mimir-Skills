# Learnings

## [2026-03-17] Session: ses_303df1d7cffeLzhu0R3CzzbkRx — Initial setup

- `mimir_skills/cli.py` imports from `.install` directly, NOT from `.install_codex` → safe to delete `install_codex.py`
- `template/` is already in `.npmignore` line 11 AND not in `package.json` `files` array → no action needed
- `test_install_codex.py` has 11 tests: 10 active CLI install tests + 1 legacy adapter test — must surgically edit, NOT delete
- `docs/adapter-feedback-loop.md`, `docs/always-loaded-rules.md`, `docs/agent-support-levels.md` have generic "adapter" concept mentions, NOT broken path refs → leave untouched

# Project Cleanup: Remove Legacy Adapter Code and Dead References

## TL;DR

> **Quick Summary**: Remove the dead `adapters/` directory, its companion `install_codex.py` shim, the CI legacy test, and all doc references to these removed artifacts. Surgically edit (not delete) the test file that contains 10 active tests alongside 1 legacy test.
> 
> **Deliverables**:
> - `adapters/` directory deleted
> - `mimir_skills/install_codex.py` deleted
> - CI legacy smoke test step removed
> - Test file renamed `test_install_codex.py` → `test_install.py` with legacy test removed
> - All adapter references cleaned from docs
> 
> **Estimated Effort**: Short
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Task 1 → Task 2 → Final Verification

---

## Context

### Original Request
User asked for a deep audit of the project to identify files and code that can be removed. The audit found that `adapters/` is a dead legacy directory, `mimir_skills/install_codex.py` is a backward-compat shim no longer needed, and multiple docs still reference the removed adapter path.

### Interview Summary
**Key Discussions**:
- Adapter directory contains a single 15-line wrapper that delegates to `mimir_skills.install.py`
- All real install logic lives in `mimir_skills/install.py` with multi-target support (claude, codex, generic)
- CI has a "legacy smoke test" for the adapter path that should go with it
- `template/` was initially flagged for `.npmignore` but Metis confirmed it's already excluded

**Research Findings**:
- `test_install_codex.py` contains 11 tests: 10 active CLI install tests + 1 legacy adapter test. Must NOT delete the whole file.
- `template/` is already in `.npmignore` line 11 AND not in `package.json` `files` array. No action needed.
- `docs/always-loaded-rules.md` and `docs/agent-support-levels.md` have generic "adapter" concept mentions, not broken path references. Leave untouched.
- `docs/adapter-feedback-loop.md` is a conceptual methodology doc. Leave untouched.

### Metis Review
**Identified Gaps** (addressed):
- `test_install_codex.py` must be surgically edited, not deleted — 10 active tests would be lost
- `template/` `.npmignore` action was a false positive — already handled
- Several doc references are conceptual mentions, not broken paths — should not be touched
- `agent-support-levels.md` Codex support level description may become stale — deferred, out of scope

---

## Work Objectives

### Core Objective
Remove all legacy adapter code, its backward-compat shim, CI test, and doc references to produce a cleaner codebase with zero dead references.

### Concrete Deliverables
- `adapters/` directory removed from repo
- `mimir_skills/install_codex.py` removed
- `ci.yml` legacy test step removed
- `tests/test_install_codex.py` → `tests/test_install.py` (1 legacy test removed, 10 active tests preserved)
- 7 doc files cleaned of adapter path references

### Definition of Done
- [ ] `python -m unittest discover -s tests -p "test_*.py"` passes with 0 failures
- [ ] `grep -r "install_codex\|adapters/codex\|install_codex_skills" --include="*.py" --include="*.md" --include="*.yml" .` returns no output
- [ ] `python -m mimir_skills install --target codex` still works
- [ ] `python -m mimir_skills list` still works

### Must Have
- All adapter code and references removed
- All 10 active install tests preserved and passing
- Primary install paths (`python -m mimir_skills install`, `npx mimir-skills install`) unaffected

### Must NOT Have (Guardrails)
- DO NOT delete `test_install_codex.py` entirely — surgically edit it
- DO NOT touch `template/` or `.npmignore` — already handled
- DO NOT touch `docs/adapter-feedback-loop.md` — conceptual doc, not broken references
- DO NOT touch `docs/always-loaded-rules.md` — generic adapter concept mentions only
- DO NOT touch `docs/agent-support-levels.md` — out of scope for this cleanup
- DO NOT rewrite doc content beyond removing/replacing adapter-specific path references
- DO NOT touch `scripts/`, `bin/cli.js`, `evaluations/`, `examples/`, or `skills/` content
- DO NOT touch `.workspace/` files

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES
- **Automated tests**: YES (tests-after — run existing test suite to verify no regressions)
- **Framework**: Python unittest
- **Test command**: `python -m unittest discover -s tests -p "test_*.py"`

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **CLI verification**: Use Bash — Run commands, assert exit codes + output
- **Reference sweep**: Use Bash (grep) — Verify zero remaining dead references

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — code removal + test fix):
├── Task 1: Remove legacy adapter code, shim, CI step, fix tests [quick]

Wave 2 (After Wave 1 — doc cleanup):
├── Task 2: Clean adapter references from all docs [quick]

Wave FINAL (After ALL tasks — verification):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
├── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

### Dependency Matrix
- **Task 1**: No deps → Blocks Task 2
- **Task 2**: Depends on Task 1 → Blocks Final Wave

### Agent Dispatch Summary
- **Wave 1**: 1 task — T1 → `quick`
- **Wave 2**: 1 task — T2 → `quick`
- **FINAL**: 4 tasks — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

- [ ] 1. Remove legacy adapter code, shim, CI step, and fix tests

  **What to do**:
  1. Run `python -m unittest discover -s tests -p "test_*.py"` to establish green baseline
  2. Delete `adapters/` directory entirely (including `adapters/codex/scripts/install_codex_skills.py` and any `__pycache__`)
  3. Delete `mimir_skills/install_codex.py`
  4. In `.github/workflows/ci.yml`: remove the "Smoke-test legacy install_codex_skills.py" step (lines 48-52, the entire step block including the `- name:` line through the `test -f` assertions)
  5. In `tests/test_install_codex.py`:
     - Remove the import `from mimir_skills.install_codex import main as install_main` (line 12)
     - Remove the entire `test_legacy_script_main_still_installs` method (lines 138-157)
     - Rename the file from `test_install_codex.py` to `test_install.py`
  6. Run `python -m unittest discover -s tests -p "test_*.py"` — must pass with 0 failures
  7. Verify primary install paths still work:
     - `python -m mimir_skills install --target codex --codex-home "$TEMP/qa-codex" --workflows prepare-handoff`
     - `python -m mimir_skills list`

  **Must NOT do**:
  - Do NOT delete `test_install_codex.py` entirely — it has 10 active tests
  - Do NOT touch `mimir_skills/install.py` or `mimir_skills/cli.py`
  - Do NOT touch any docs (that's Task 2)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Straightforward file deletions, one surgical test edit, one CI edit
  - **Skills**: []
    - No special skills needed — standard file operations and test running
  - **Skills Evaluated but Omitted**:
    - `git-master`: Not needed — commit is separate from implementation

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (solo)
  - **Blocks**: Task 2
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `adapters/codex/scripts/install_codex_skills.py` — the 15-line file to delete (thin wrapper calling `mimir_skills.install_codex.main()`)
  - `mimir_skills/install_codex.py` — the 44-line backward-compat shim to delete (delegates everything to `install.py`)

  **API/Type References** (contracts to preserve):
  - `mimir_skills/install.py` — the REAL install logic. Must NOT be touched. `run_install()` function is the canonical entry point.
  - `mimir_skills/cli.py` — the CLI entry point. Imports from `.install` directly, NOT from `.install_codex`. Must NOT be touched.

  **Test References** (critical — surgical edit):
  - `tests/test_install_codex.py:12` — `from mimir_skills.install_codex import main as install_main` — REMOVE this import
  - `tests/test_install_codex.py:138-157` — `test_legacy_script_main_still_installs` method — REMOVE this entire test method
  - `tests/test_install_codex.py` (rest of file) — 10 active tests using `from mimir_skills.cli import main as cli_main` — PRESERVE all of these

  **CI References**:
  - `.github/workflows/ci.yml:48-52` — "Smoke-test legacy install_codex_skills.py" step — REMOVE this entire step

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Tests pass after removal
    Tool: Bash
    Preconditions: All deletions and edits complete
    Steps:
      1. Run `python -m unittest discover -s tests -p "test_*.py"`
      2. Assert exit code is 0
      3. Assert output contains "OK" and does not contain "FAIL"
    Expected Result: All tests pass, 0 failures
    Failure Indicators: Non-zero exit code, "FAIL" or "ERROR" in output
    Evidence: .sisyphus/evidence/task-1-tests-pass.txt

  Scenario: Legacy files actually deleted
    Tool: Bash
    Preconditions: Deletions complete
    Steps:
      1. Run `test -d adapters && echo FAIL || echo PASS`
      2. Run `test -f mimir_skills/install_codex.py && echo FAIL || echo PASS`
      3. Run `test -f tests/test_install_codex.py && echo FAIL || echo PASS` (old name gone)
      4. Run `test -f tests/test_install.py && echo PASS || echo FAIL` (new name exists)
    Expected Result: All 4 checks output "PASS"
    Failure Indicators: Any check outputs "FAIL"
    Evidence: .sisyphus/evidence/task-1-files-deleted.txt

  Scenario: Primary install path still works
    Tool: Bash
    Preconditions: All changes complete
    Steps:
      1. Run `python -m mimir_skills install --target codex --codex-home "$TEMP/qa-codex" --workflows prepare-handoff`
      2. Assert exit code 0
      3. Run `test -f "$TEMP/qa-codex/skills/prepare-handoff/SKILL.md" && echo PASS || echo FAIL`
      4. Run `python -m mimir_skills list`
      5. Assert exit code 0 and output contains "prepare-handoff"
    Expected Result: Install succeeds, SKILL.md exists, list shows workflows
    Failure Indicators: Non-zero exit code, missing SKILL.md, empty list output
    Evidence: .sisyphus/evidence/task-1-install-works.txt

  Scenario: Active tests preserved (count check)
    Tool: Bash
    Preconditions: Rename and edit complete
    Steps:
      1. Run `grep -c "def test_" tests/test_install.py`
      2. Assert output is "10"
      3. Run `grep -c "test_legacy_script_main_still_installs" tests/test_install.py`
      4. Assert output is "0"
    Expected Result: 10 test methods remain, legacy test is gone
    Failure Indicators: Count is not 10, or legacy test name still present
    Evidence: .sisyphus/evidence/task-1-test-count.txt
  ```

  **Commit**: YES
  - Message: `refactor: remove legacy adapter code and install_codex shim`
  - Files: `adapters/` (deleted), `mimir_skills/install_codex.py` (deleted), `.github/workflows/ci.yml`, `tests/test_install.py` (renamed from `test_install_codex.py`)
  - Pre-commit: `python -m unittest discover -s tests -p "test_*.py"`

- [ ] 2. Clean adapter references from all documentation

  **What to do**:
  1. In `docs/quick-start.md`: Find the "older direct script" / legacy adapter block around lines 140-144 that references `python adapters/codex/scripts/install_codex_skills.py`. Remove the entire block/paragraph.
  2. In `docs/quick-start.ko.md`: Mirror the same removal (Korean version of the same block around lines 140-144)
  3. In `docs/codex-local-install.md`: Find the section around lines 82-90 that references `python adapters/codex/scripts/install_codex_skills.py`. Remove the entire legacy section.
  4. In `docs/workflow-surface.md`: Remove adapter proof-point references at lines ~46, ~72, ~102, ~140. Each is a bullet or sub-bullet mentioning `adapters/codex/scripts/install_codex_skills.py`. Remove the entire bullet in each case.
  5. In `README.md`: Remove `adapters/` from the "Repository Layout" code block (~line 124) and from the "Secondary helper surface" list (~line 138)
  6. In `README.ko.md`: Mirror the same two removals (~lines 124, 138)
  7. In `skills/README.md`: At line 28, remove `, and \`adapters/\`` from the sentence about helper code
  8. Run final grep sweep: `grep -r "install_codex\|adapters/codex\|install_codex_skills" --include="*.py" --include="*.md" --include="*.yml" .` — must return empty

  **Must NOT do**:
  - Do NOT touch `docs/adapter-feedback-loop.md` — conceptual doc, not broken paths
  - Do NOT touch `docs/always-loaded-rules.md` — generic "adapter" concept mentions only
  - Do NOT touch `docs/agent-support-levels.md` — out of scope
  - Do NOT rewrite surrounding paragraphs — only remove/replace adapter-specific path references
  - Do NOT touch any Python or JS files (that was Task 1)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Text find-and-remove across markdown files, no logic changes
  - **Skills**: []
    - No special skills needed
  - **Skills Evaluated but Omitted**:
    - `git-master`: Not needed — commit is separate

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (after Task 1)
  - **Blocks**: Final Verification Wave
  - **Blocked By**: Task 1 (must verify code removal first)

  **References** (CRITICAL - Be Exhaustive):

  **Doc References** (exact locations to edit):
  - `docs/quick-start.md:140-144` — legacy adapter script block. Read surrounding context to identify exact block boundaries.
  - `docs/quick-start.ko.md:140-144` — Korean mirror of above
  - `docs/codex-local-install.md:82-90` — "Legacy Codex Install" or equivalent section with `python adapters/codex/scripts/install_codex_skills.py`
  - `docs/workflow-surface.md:46` — bullet about "the Codex-local install path under `adapters/codex/scripts/install_codex_skills.py`"
  - `docs/workflow-surface.md:72` — same pattern, different section
  - `docs/workflow-surface.md:102` — same pattern, different section  
  - `docs/workflow-surface.md:140` — same pattern, different section
  - `README.md:124` — `adapters/` in Repository Layout code block
  - `README.md:138` — `- adapters/` in Secondary helper surface list
  - `README.ko.md:124` — Korean mirror of layout
  - `README.ko.md:138` — Korean mirror of secondary surface
  - `skills/README.md:28` — sentence mentioning `adapters/` alongside `mimir_skills/` and `skills/*/scripts/`

  **Docs to NOT touch** (explicit exclusions):
  - `docs/adapter-feedback-loop.md` — conceptual methodology doc, "adapter" is a concept not a path
  - `docs/always-loaded-rules.md:32` — "Future adapters may mirror..." is generic guidance
  - `docs/agent-support-levels.md:51,57` — conceptual support level descriptions

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Zero dead references remain
    Tool: Bash
    Preconditions: All doc edits complete
    Steps:
      1. Run `grep -r "install_codex" --include="*.py" --include="*.md" --include="*.yml" .`
      2. Assert no output
      3. Run `grep -r "adapters/codex" --include="*.md" --include="*.yml" .`
      4. Assert no output
      5. Run `grep -r "install_codex_skills" --include="*.md" --include="*.yml" .`
      6. Assert no output
    Expected Result: All 3 grep commands return empty (exit code 1, no matches)
    Failure Indicators: Any grep returns output
    Evidence: .sisyphus/evidence/task-2-grep-sweep.txt

  Scenario: Excluded docs untouched
    Tool: Bash
    Preconditions: All doc edits complete
    Steps:
      1. Run `git diff docs/adapter-feedback-loop.md`
      2. Assert empty (no changes)
      3. Run `git diff docs/always-loaded-rules.md`
      4. Assert empty (no changes)
      5. Run `git diff docs/agent-support-levels.md`
      6. Assert empty (no changes)
    Expected Result: All 3 diffs are empty — files were not touched
    Failure Indicators: Any diff shows changes
    Evidence: .sisyphus/evidence/task-2-excluded-docs.txt

  Scenario: Tests still pass after doc changes
    Tool: Bash
    Preconditions: All doc edits complete
    Steps:
      1. Run `python -m unittest discover -s tests -p "test_*.py"`
      2. Assert exit code 0
    Expected Result: All tests pass (doc changes shouldn't break tests, but verify)
    Failure Indicators: Non-zero exit code
    Evidence: .sisyphus/evidence/task-2-tests-still-pass.txt
  ```

  **Commit**: YES
  - Message: `docs: remove legacy adapter references from documentation`
  - Files: `docs/quick-start.md`, `docs/quick-start.ko.md`, `docs/codex-local-install.md`, `docs/workflow-surface.md`, `README.md`, `README.ko.md`, `skills/README.md`
  - Pre-commit: `grep -r "install_codex\|adapters/codex\|install_codex_skills" --include="*.py" --include="*.md" --include="*.yml" .` must return empty

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists. For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `python -m unittest discover -s tests -p "test_*.py"`. Review all changed files for leftover references, broken imports, or stale comments. Check no `install_codex` references remain anywhere.
  Output: `Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Execute EVERY QA scenario from EVERY task. Test: `python -m mimir_skills install --target codex`, `python -m mimir_skills install --target claude`, `python -m mimir_skills list`. Capture evidence. Run full grep sweep for dead references.
  Output: `Scenarios [N/N pass] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify nothing beyond spec was built (no creep). Check "Must NOT do" compliance. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | VERDICT`

---

## Commit Strategy

- **Commit 1** (Task 1): `refactor: remove legacy adapter code and install_codex shim` — `adapters/`, `mimir_skills/install_codex.py`, `.github/workflows/ci.yml`, `tests/test_install.py` (renamed from `test_install_codex.py`)
  - Pre-commit: `python -m unittest discover -s tests -p "test_*.py"`
- **Commit 2** (Task 2): `docs: remove adapter references from documentation` — all affected doc files
  - Pre-commit: `grep -r "install_codex\|adapters/codex\|install_codex_skills" --include="*.py" --include="*.md" --include="*.yml" .` must return empty

---

## Success Criteria

### Verification Commands
```bash
python -m unittest discover -s tests -p "test_*.py"  # Expected: all pass, 0 failures
grep -r "install_codex" --include="*.py" --include="*.md" --include="*.yml" .  # Expected: no output
grep -r "adapters/codex" --include="*.md" --include="*.yml" .  # Expected: no output
grep -r "install_codex_skills" --include="*.md" --include="*.yml" .  # Expected: no output
python -m mimir_skills list  # Expected: exit 0, outputs workflow list
python -m mimir_skills install --help  # Expected: exit 0, shows help
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All tests pass
- [ ] Zero dead references remain

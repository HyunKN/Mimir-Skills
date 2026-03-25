# Obsidian Workspace (Optional)

Obsidian is an optional local review workspace for Mimir-Skills outputs.
It is useful when you want a more visual way to browse linked Markdown artifacts, but it is not required for the workflows to work.

## Without Obsidian

Nothing changes.

- keep using the canonical JSON under `.ai/records/decisions/` and `.ai/records/memories/`
- read the derived Markdown summaries under `.ai/records/reports/`
- use your editor, file tree, grep, or GitHub review flow as usual

This remains the default path.

## With Obsidian

Use Obsidian as a local browsing layer over the derived Markdown artifacts.

- open the project as a local vault
- browse linked notes under `.ai/records/reports/`
- use backlinks and graph view to see how decision, report, and memory notes connect

The graph becomes useful because the derived notes include Obsidian-style wikilinks such as `[[dec-...]]` and `[[mem-...]]`.

## First Use Preference

On the first Obsidian export request in a project, ask the user where Obsidian-friendly notes should go.

Recommended choices:

1. `.ai/records/reports/`
   - keeps the notes next to the other derived Markdown artifacts
   - makes project review and verification simpler

2. the user's Obsidian vault path
   - opens more naturally inside an existing personal vault
   - depends on a user-specific local path

After that first choice, keep using the same project-level default until the user asks to change it.

The saved project-local preference lives at:

```text
.ai/local/obsidian-output.json
```

You can manage it explicitly with:

```bash
python -m mimir_skills obsidian-config show
python -m mimir_skills obsidian-config set-reports
python -m mimir_skills obsidian-config set-vault "C:\\path\\to\\your\\Obsidian Vault\\Mimir-Skills"
python -m mimir_skills obsidian-config clear
```

## How To Turn It On

Nothing is always-on here.

Obsidian support is a manual opt-in review path:

- keep using the workflows normally
- render Obsidian-friendly notes only when you want graph-friendly Markdown
- open the project or artifact folder as a vault only when you want that browsing experience
- on the first Obsidian export request in a project, ask which output location to use before rendering

Decision record:

```bash
python skills/_internal/decision-capture/scripts/render_obsidian_note.py .ai/records/decisions/<id>.json
```

Memory artifact:

```bash
python skills/_internal/memory-promote/scripts/render_obsidian_note.py .ai/records/memories/<candidate|validated>/<id>.json
```

If you prefer to ask an agent instead of running the scripts yourself, a practical first-use request is:

```text
If this is the first Obsidian export in this project, first ask whether to keep notes under `.ai/records/reports/` or send them to my Obsidian vault path, explain the difference briefly, then render this decision record as an Obsidian-friendly note.
```

Later, once the preference is known, a shorter request is:

```text
Render this memory artifact as an Obsidian-friendly note using the current project default output location.
```

## Current Output Location

By default, Obsidian-friendly notes render into `.ai/records/reports/`.

That means they sit next to the other derived human-readable artifacts such as summaries.

Current rationale:

- `reports/` is already the home for derived Markdown artifacts
- non-Obsidian users can ignore the extra notes without changing their normal workflow
- the canonical JSON remains under `.ai/records/decisions/` and `.ai/records/memories/`
- keeping one review-oriented folder is simpler than requiring a separate vault export path

For now this is the recommended default.
If the reports folder becomes too noisy later, the repository can revisit whether a separate `reports/obsidian/` layer is justified.

## Changing the Preference Later

The output location should be changeable later.

Examples:

```text
Change the default Obsidian output location for this project to my Obsidian vault path.
```

```text
Switch the default Obsidian output location for this project back to `.ai/records/reports/`.
```

Or persist the change directly:

```bash
python -m mimir_skills obsidian-config set-vault "C:\\path\\to\\your\\Obsidian Vault\\Mimir-Skills"
python -m mimir_skills obsidian-config set-reports
```

## Expected Benefits

- faster human review of related artifacts
- easier visual navigation from reports to source decisions
- clearer follow-up tracing when one decision supersedes another or feeds a memory artifact

## Boundaries

- canonical truth still lives in the JSON records
- Markdown remains derived and review-oriented
- no plugin is required
- this is not an approval system, audit system, or collaboration layer
- the graph is only trustworthy when the derived notes are kept current
- if you do not use Obsidian, do not change anything; keep using the normal JSON plus Markdown review flow

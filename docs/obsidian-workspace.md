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

- open `.ai/records/reports/` as a local vault when you want a clean, artifact-only view
- browse linked notes under `.ai/records/reports/`
- use backlinks and graph view to see how decision, report, and memory notes connect

The graph becomes useful because the derived notes include Obsidian-style wikilinks such as `[[dec-...]]` and `[[mem-...]]`.

## Default Output Location

By default, Obsidian-friendly notes render into:

```text
.ai/records/reports/
```

This is the recommended default because it keeps the Obsidian-friendly notes next to the other derived Markdown artifacts.
If you want to inspect them in Obsidian, open that folder as a vault.

## How To Turn It On

Nothing is always-on here.

Obsidian support is a manual opt-in review path:

- keep using the workflows normally
- render Obsidian-friendly notes only when you want graph-friendly Markdown
- open `.ai/records/reports/` as a vault when you want that browsing experience

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
Render this decision record as an Obsidian-friendly note under the default project output location.
```

For existing project records:

```text
Render the existing decision and memory records in this project as Obsidian-friendly notes under the default project output location so I can browse them in Obsidian.
```

## Changing the Preference Later

If you later want a different output location, change it explicitly.

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

The saved project-local preference lives at:

```text
.ai/local/obsidian-output.json
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

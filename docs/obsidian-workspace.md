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

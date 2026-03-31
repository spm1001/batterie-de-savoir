# Maintaining the Batterie Documentation

When a tool is **added, renamed, or removed** from the suite, update all of the following. This checklist exists because a single tool touches 6+ locations across the docs.

## Checklist: Adding a New Tool

1. **README.md** — add row to the brigade table (keep sort order: stable first, then beta, then alpha)
2. **docs/index.md** — add row to the brigade table (same order as README)
3. **docs/index.md** — update the prose paragraph below the table that names all tools
4. **docs/for-agents.md** — add to ALL of these tables:
   - Vocabulary table
   - Tool routing table
   - Dependency direction table
   - Key repos table
5. **docs/getting-started.md** — add a "When to use this" section (placed by adoption order, not alphabetical)
6. **docs/getting-started.md** — add a paragraph to "How the Tools Compose" section showing how the new tool relates to others
7. **docs/getting-started.md** — if Python-based, add to the Prerequisites paragraph listing Python tools
8. **docs/assets/brigade.mmd** — add node, subgraph, edges, and class definition
9. **docs/assets/brigade.png** — re-render the Mermaid diagram (use `mmdc` or Mermaid Live Editor)
10. **docs/tools/<name>.md** — create the tool page following the pattern of existing pages (see Template below)
11. **docs/principles.md** — if the tool exemplifies a principle, add it to the relevant "In practice" section
12. **CLAUDE.md (global)** — add to "The Kitchen" table if not already there
13. **Skill frontmatter** — if the tool has a skill, ensure the description mentions the kitchen name

## Checklist: Pushing Plugin Changes

Claude Code's plugin cache is **version-keyed**. If you push content changes without bumping the version in `.claude-plugin/plugin.json`, users with the old version cached will never see the update — `/plugin install` says "already at latest."

**Every push that changes plugin behaviour must bump the version:**

1. Edit `.claude-plugin/plugin.json` — increment the patch version (e.g., `1.0.0` → `1.0.1`)
2. Commit the version bump alongside the content changes (or as a follow-up if you forget)

This applies to all batterie repos that have a `.claude-plugin/plugin.json`: bon, trousse, mise, passe, garde-manger, todoist-gtd, plongeur, aboyeur.

**What counts as a behaviour change:** hook scripts, skills, MCP server code, plugin.json fields (description, keywords, hooks). Does NOT include: README, CLAUDE.md, tests, docs, non-plugin scripts.

### Version source of truth

For plugins that ship a CLI tool (bon, garde-manger, passe, todoist-gtd), the version lives in **one place only**: `.claude-plugin/plugin.json`. The `pyproject.toml` reads it dynamically via hatchling:

```toml
[project]
dynamic = ["version"]

[tool.hatch.version]
path = ".claude-plugin/plugin.json"
pattern = "\"version\":\\s*\"(?P<version>[^\"]+)\""
```

**Never add a static `version = "X.Y.Z"` to pyproject.toml in these repos.** Bump plugin.json and both the marketplace and `<tool> --version` follow automatically.

Plugins without CLIs (trousse, mise) only have plugin.json — no sync concern.

## Checklist: Changing a Tool's Maturity

1. **README.md** — update the Robustness column
2. **docs/index.md** — update the Robustness column
3. **CLAUDE.md (global)** — if the Kitchen table has maturity info, update there too

## Checklist: Removing a Tool

Reverse of adding — remove from all 13 locations above.

## Tool Page Template

Every tool page follows this structure:

```markdown
---
layout: default
title: <Name>
---

# <Name> — <Station tagline>

<One paragraph: what problem this solves and why it exists.>

## When to use / When NOT to use

<Two bullet lists. "Do NOT use" should point to the right tool.>

## Key concepts

<3-5 subsections explaining the tool's core ideas.>

## How it relates to other tools

<Table or prose showing dependencies and complements.>

## CLI / API

<Command reference or code examples.>

## Repo

Install, usage, and full reference: [github.com/spm1001/<name>](https://github.com/spm1001/<name>)
```

## Registry-Driven Generation (current)

Several sections across the docs are now generated from `brigade.toml` — the single source of truth for tool metadata. The scripts live in `scripts/`.

### Day-to-day workflow

When adding, renaming, or changing maturity of a tool:

1. **Edit `brigade.toml`** — update the relevant `[tool.{slug}]` section
2. **Run the render script** — `uv run --script scripts/render.py`
3. **Commit** — the updated files will show in `git diff`

To check for drift without changing anything:

```
uv run --script scripts/lint.py
```

Exits 0 if clean, exits 1 with a diff if any GENERATED section is stale.

### What's generated

| File | Marker | Content |
|------|--------|---------|
| `README.md` | `brigade-table` | Brigade table (links to GitHub repos) |
| `docs/index.md` | `brigade-table` | Brigade table (links to docs tool pages) |
| `docs/for-agents.md` | `vocabulary` | Tool vocabulary rows |
| `docs/for-agents.md` | `tool-routing` | Tool routing table |
| `docs/for-agents.md` | `dependency-direction` | Dependency direction table |
| `docs/for-agents.md` | `key-repos` | Key repos table |

Generated regions are fenced with `<!-- GENERATED:{name}:START -->` / `<!-- GENERATED:{name}:END -->` markers. Do not hand-edit content between these markers — it will be overwritten on the next render.

### What remains manual

The following checklist items are **not** generated and still require hand-editing:

- **`docs/getting-started.md`** — "When to use this" section and "How the Tools Compose" paragraph
- **`docs/tools/<name>.md`** — tool page creation (follow the Template below)
- **`docs/principles.md`** — "In practice" additions
- **`docs/assets/brigade.mmd` / `brigade.png`** — diagram (re-render with `mmdc`)
- **`CLAUDE.md` (global)** — "The Kitchen" table
- **Skill frontmatter** — description mentioning the kitchen name

### Deliberate exclusions — do not "fix" these

Some rows sit **outside** the GENERATED markers by design:

- **`docs/for-agents.md` vocabulary table** — the "Brigade" row and the GTD terms (Outcome, Action, Brief, Handoff, Skill, Draw-down, Draw-up) are static. Only the per-tool rows are generated. The vocabulary table order now follows `meta.order` in brigade.toml — this is intentional, not a bug to revert.
- **`docs/for-agents.md` key-repos table** — the "This docs site → spm1001/batterie-de-savoir" row is a meta-reference, not a tool entry. It lives outside the generated region deliberately.

### Tool pages are hand-authored, not generated

`docs/tools/*.md` pages will never be generated from `brigade.toml`. The registry holds metadata (one-liners, stations, routing hints) — tool pages hold judgement (key concepts, design decisions, how tools relate). That richness can't be templated without losing what makes the pages useful.

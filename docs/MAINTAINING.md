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
8. **docs/tools/<name>.md** — create the tool page following the pattern of existing pages (see Template below)
9. **docs/principles.md** — if the tool exemplifies a principle, add it to the relevant "In practice" section
10. **CLAUDE.md (global)** — add to "The Kitchen" table if not already there
11. **Skill frontmatter** — if the tool has a skill, ensure the description mentions the kitchen name

## Checklist: Pushing Plugin Changes

**The one-command way: `/batterie:publish`** (run from the source repo you edited). It bumps `plugin.json`, commits, pushes, triggers the `assemble.yml` CI, watches it green, then pulls this machine current. `--patch` (default), `--minor`, `--major`. The engine is `scripts/publish.py`; the rest of this section is what it does under the hood — read it to understand the moving parts, but reach for the verb.

Claude Code's plugin cache is **version-keyed**. If you push content changes without a version bump, users with the old version cached will never see the update — `/plugin install` says "already at latest."

**Since 2026-06-28 the suite carries ONE version number** (the `batterie` plugin's `plugin.json` in this repo), and you never hand-bump anything to release:

1. Run `/batterie:publish` from the source repo you edited — it bumps the **suite** version centrally, commits, pushes (a 2-repo push when the edited repo isn't this one), triggers assembly, and watches it green.
2. The assembler stamps every vendored `plugin.json` to the suite version. A source repo's own `plugin.json` version is local-dev-only — **do NOT hand-bump it to "release"; the stamp overwrites it.**
3. A red assemble is almost always a suite-level version-ratchet quarantine: vendored content changed without a suite bump. Ship the change via `/batterie:publish` rather than editing versions by hand.

This applies to all suite source repos: batterie-de-savoir (this repo — the suite plugin), bon, trousse, mise-en-space, todoist-gtd. (passe left the suite 2026-07-07; plongeur and aboyeur were never published plugins.)

**What counts as vendored content (needs a suite bump):** `CLAUDE.md`, `instructions.md`, `skills/`, `hooks/`, `.claude-plugin/` — plus full source for MCP plugins (mise). Does NOT include: README, tests, `docs/`, `.bon/`, `.github/` — those are plain commit+push. The authoritative list is `assemble.sh`'s copy-list; read it rather than guessing.

The full mechanics (stamp, ratchet, lazy CLI stamping) are canonically described in this repo's `CLAUDE.md` → **Versioning convention** — that section is the source of truth; this checklist is a pointer.

### Version source of truth

For plugins that ship a CLI tool (bon, todoist-gtd), `pyproject.toml` reads the version dynamically from `.claude-plugin/plugin.json` via hatchling:

```toml
[project]
dynamic = ["version"]

[tool.hatch.version]
path = ".claude-plugin/plugin.json"
pattern = "\"version\":\\s*\"(?P<version>[^\"]+)\""
```

**Never add a static `version = "X.Y.Z"` to pyproject.toml in these repos.** Post-cutover, a CLI's `--version` reports *the suite release that last changed that CLI* (`publish.py` lazy-stamps the source repo being published) — a CLI number below the suite number is expected, not drift.

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
- **`CLAUDE.md` (global)** — "The Kitchen" table
- **Skill frontmatter** — description mentioning the kitchen name

### Deliberate exclusions — do not "fix" these

Some rows sit **outside** the GENERATED markers by design:

- **`docs/for-agents.md` vocabulary table** — the "Brigade" row and the GTD terms (Outcome, Action, Brief, Handoff, Skill, Draw-down, Draw-up) are static. Only the per-tool rows are generated. The vocabulary table order now follows `meta.order` in brigade.toml — this is intentional, not a bug to revert.
- **`docs/for-agents.md` key-repos table** — the "This docs site → spm1001/batterie-de-savoir" row is a meta-reference, not a tool entry. It lives outside the generated region deliberately.

### Tool pages are hand-authored, not generated

`docs/tools/*.md` pages will never be generated from `brigade.toml`. The registry holds metadata (one-liners, stations, routing hints) — tool pages hold judgement (key concepts, design decisions, how tools relate). That richness can't be templated without losing what makes the pages useful.

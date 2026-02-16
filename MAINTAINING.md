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

## Future: Registry-Driven Generation

The manual checklist above works but doesn't scale. A better pattern (filed as a bon outcome):

1. A `brigade.toml` file as the single source of truth for tool metadata
2. A PEP 723 render script that generates tables and page headers from the registry
3. A lint script that detects drift between registry and docs
4. Generated sections fenced with `<!-- GENERATED:START -->` / `<!-- GENERATED:END -->` markers

This is the pattern used by mise (jdx/mise) and Homebrew's formulae site. It would reduce this checklist to: "edit brigade.toml, run the render script."

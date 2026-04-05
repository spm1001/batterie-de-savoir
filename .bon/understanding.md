# Understanding

## Marketplace Architecture

Batterie-de-savoir serves dual roles: it's the CLI marketplace (listing all plugins via `marketplace.json`) and itself a plugin (hosting cross-cutting commands like `/batterie-update`). The self-reference uses `"source": "./"` — trailing slash required, `"."` fails schema validation. This mirrors Anthropic's official marketplace pattern.

A second repo (`spm1001/batterie`) exists for Desktop/Cowork, which rejects external `source: url` references. `assemble.sh` copies plugin content physically into that repo.

The architectural direction is "better assembly, not monorepo." Source repos stay separate for clean git history and independent development. The published marketplace should converge to a single repo — `spm1001/batterie` — serving both CLI and Desktop. The bridge is assembly automation: `assemble.sh` copies `.claude-plugin/`, `skills/`, `hooks/`, `commands/` from each source repo into `plugins/<name>/`. `scripts/batterie-lint.py` can run post-assembly to catch drift. The key unsolved problem: making assembly reliable enough for CI automation (the `mise/` gitignore issue is one instance).

## Plugin Format

`commands/` is legacy; `skills/` is preferred. Both are loaded identically by Claude Code — same frontmatter, same runtime. The only difference: `skills/` supports `references/` and `scripts/` subdirectories. Batterie's `/batterie-update` was converted to `/batterie:update` using the skills format. Claude Code surfaces skills by **directory name**, not frontmatter `name:` field.

## Versioning

CLI-bearing plugins (bon, garde-manger, passe, todoist-gtd) keep version in one place: `.claude-plugin/plugin.json`. Each `pyproject.toml` reads it dynamically via hatchling regex. No dual-maintenance drift.

## Update Mechanics

`claude plugin update` checks against a cached marketplace index. The index must be refreshed first via `claude plugin marketplace update` — otherwise updates appear current when they're not. `/batterie-update` handles this by always refreshing first.

## Current Marketplace

8 plugins in the CLI marketplace (guéridon removed — it's infrastructure, not a Claude capability).

## Library Extraction Lessons

When extracting a library from a working script, inventory knowledge artifacts alongside the code. ccconv's 40-line docstring was doing double duty as API documentation and CC JSONL schema reference. When parsing functions moved to deglacer, the code moved but the documentation didn't — the canonical schema reference now lives in a file that will become a thin shim. Code extraction without knowledge extraction is half the job. Future extractions should ask: "what docs, comments, and skill files describe this code, and where should they live in the new structure?"

## CC Session Knowledge Layers

CC session data has three distinct layers that were historically conflated:
- **Schema** — what the JSONL fields mean
- **Parsing** — how to load and deduplicate
- **Interpretation** — what constitutes a turn, what's noise

Deglacer consolidates parsing and interpretation. The schema reference still needs a home. The open question for bds-nijaja: should deglacer also own the skill and schema docs (single source of truth) or should trousse keep the skill as a wrapper? Trade-off is self-containment vs separation of concerns.

## Session Lifecycle Direction

The lifecycle is being redesigned around a single primary artifact: the handoff. Currently /close produces six outputs; the new design collapses to one handoff with two zones — a Now zone (Gotchas/Risks/Next/Commands) consumed by the next /open, and a Compost zone (Done/Reflection/Learned) processed overnight into understanding.md updates and garde extractions. The Learned section replaces the separate contribution file. Overnight composting reads unprocessed handoffs across all repos, produces garde extractions by parsing handoff sections (not LLM), and falls back to cold JSONL processing via deglacer only for sessions without handoffs. Auto-handoff becomes a thin mechanical safety net (git + bon state, instant, no race condition). Scratch repos route handoffs to target repos based on bon prefixes.

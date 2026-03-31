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

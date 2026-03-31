# Understanding

## Marketplace Architecture

Batterie-de-savoir serves dual roles: it's the CLI marketplace (listing all plugins via `marketplace.json`) and itself a plugin (hosting cross-cutting commands like `/batterie-update`). The self-reference uses `"source": "./"` — trailing slash required, `"."` fails schema validation. This mirrors Anthropic's official marketplace pattern.

A second repo (`spm1001/batterie`) exists for Desktop/Cowork, which rejects external `source: url` references. `assemble.sh` copies plugin content physically into that repo.

## Versioning

CLI-bearing plugins (bon, garde-manger, passe, todoist-gtd) keep version in one place: `.claude-plugin/plugin.json`. Each `pyproject.toml` reads it dynamically via hatchling regex. No dual-maintenance drift.

## Update Mechanics

`claude plugin update` checks against a cached marketplace index. The index must be refreshed first via `claude plugin marketplace update` — otherwise updates appear current when they're not. `/batterie-update` handles this by always refreshing first.

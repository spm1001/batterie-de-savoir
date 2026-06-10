# Batterie de Savoir

*Kitchen tools for knowledge work.*

> **Status:** Documentation — this is the umbrella repo

A suite of tools for AI-assisted knowledge work, each named for a station in a professional kitchen [brigade](https://en.wikipedia.org/wiki/Brigade_de_cuisine).

<!-- GENERATED:brigade-table:START -->
| Tool | Station | Description | Status |
|------|---------|-------------|--------|
| [**Bon**](https://github.com/spm1001/bon) | The ticket | GTD-flavoured work tracking — outcomes, actions, tactical steps | ⚡ Stable |
| [**Trousse**](https://github.com/spm1001/trousse) | The knife roll | Skills, hooks, data analysis, and session lifecycle for Claude Code | ⚡ Stable |
| [**Garde-manger**](https://github.com/spm1001/garde-manger) | The cold station | Persistent, searchable memory across sessions | ⚡ Stable |
| [**Jeton**](https://github.com/spm1001/jeton) | The token | Google OAuth token management for the suite | ⚡ Stable |
| [**Mise en Space**](https://github.com/spm1001/mise-en-space) | Mise en place | Content fetching and prep from Google Workspace and the web (MCP) | 🔧 Beta |
| [**Passe**](https://github.com/spm1001/passe) | The pass | Fast browser automation via Chrome DevTools Protocol | 🔧 Beta |
| [**Plongeur**](https://github.com/spm1001/plongeur) | The dishwasher | Streamlit data exploration UI — makes consommé accessible to non-technical users | 🔧 Beta |
| [**Todoist GTD**](https://github.com/spm1001/todoist-gtd) | The commis | Todoist integration with GTD coaching — human-owned tasks and deadlines | ⚡ Stable |
| [**Aboyeur**](https://github.com/spm1001/aboyeur) | The caller | Multi-session orchestrator — alternates workers and reflectors | 🧪 Alpha |
| [**Tafelmusik**](https://github.com/spm1001/tafelmusik) | Table music | Collaborative CRDT editing — co-edit markdown documents in real time (MCP) | 🔧 Beta |
<!-- GENERATED:brigade-table:END -->

## Install

**Via Claude Code plugin marketplace** (2.1+):

```
/plugin marketplace add spm1001/batterie
/plugin install bon@batterie
```

(Installed from `spm1001/batterie-de-savoir` before June 2026? Migrate: add the new marketplace, reinstall each plugin as `<name>@batterie`, then remove the old marketplace — plugin keys change, so a plain repoint isn't enough.)

**Manually** — each tool installs independently from its own repo. See [Getting Started](https://spm1001.github.io/batterie-de-savoir/getting-started) for the recommended adoption order.

## Documentation

**[spm1001.github.io/batterie-de-savoir](https://spm1001.github.io/batterie-de-savoir/)**

The docs site has per-tool pages, a [getting started](https://spm1001.github.io/batterie-de-savoir/getting-started) guide, [expanded design principles](https://spm1001.github.io/batterie-de-savoir/principles), and a [structured reference for AI agents](https://spm1001.github.io/batterie-de-savoir/for-agents).

## License

MIT

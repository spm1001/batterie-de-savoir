---
layout: default
title: Garde-manger
---

# Garde-manger — The cold station

Persistent, searchable memory across Claude sessions. Every new Claude session starts blank — it has no idea what you decided yesterday, what pattern you discovered last week, or which approach you tried and abandoned. Garde-manger solves this by indexing session summaries, handoffs, and local documents into a local SQLite database with full-text search, so any session can ask "didn't we figure out the auth pattern last month?" and get an answer in seconds, without replaying entire transcripts.

## When to use / When NOT to use

**Use garde-manger when:**

- You need to recall decisions, patterns, or solutions from past sessions
- You're starting a new session and want to check whether this problem has been solved before
- You want to search across session history by concept, tool, or entity
- You're doing a periodic review of what's been learned and want to surface patterns

**Do NOT use garde-manger when:**

- You need the current session's tactical state — that's **bon** (the active work tracker)
- You want to pass context to the *next* session — write a **handoff** (from trousse) instead
- You need cross-project behavioural patterns — that's **MEMORY.md**
- You want to fetch external content (web pages, Google Docs) — that's **mise**

## Key concepts

### Two-phase indexing

Garde-manger separates discovery from extraction. `garde scan` walks source directories and records metadata — file paths, timestamps, types — without touching the LLM. It's free and fast. `garde process` then sends content through Claude for entity extraction, summarisation, and relationship mapping. This costs API calls, so you control when and what gets processed. Scan early, process deliberately.

### Text search over summaries

The core insight: text search over well-structured summaries outperforms vector embeddings for this use case. SQLite's FTS5 gives fast, predictable full-text search with no embedding pipeline, no vector database, and no drift between what was indexed and what gets retrieved. Human-in-the-loop entity resolution — where the glossary maps aliases to canonical terms — handles the fuzziness that embeddings usually solve.

### Glossary and entity resolution

The glossary maps aliases to canonical terms (`oauth2` → `OAuth`, `GH` → `GitHub`). This means searches hit consistently regardless of how different sessions referred to the same concept. The glossary is maintained as a simple mapping, updated during processing.

### Token-efficient retrieval

Search returns summaries first — short, structured records that let the agent decide what's relevant before drilling into full content. This keeps context lean. The `/garde` skill loaded within sessions follows the same pattern: skim summaries, then fetch detail only when needed.

### Source types

Garde-manger indexes eight source types, each with its own scanner that knows where to find content and how to extract metadata:

| Source type | What it indexes |
|-------------|----------------|
| `claude_code` | Claude Code sessions (from `~/.claude/projects/`) |
| `claude_ai` | Claude.ai web exports |
| `cloud_session` | Cloud sessions (web Claude) |
| `handoff` | Session-to-session batons from trousse |
| `local_md` | Local markdown files |
| `bon` | Bon work tracker items |
| `knowledge` | Knowledge articles |
| `amp` | Amp thread transcripts |

### Local only

All data stays on your machine. The database lives at `~/.claude/memory/memory.db`. No cloud sync, no telemetry, no external dependencies beyond SQLite. Your session history is yours.

## How it relates to other tools

Garde-manger is the **deep memory** layer — the searchable ancestral record of what happened across all sessions. It sits in a specific place within the batterie's five memory layers:

| Layer | Scope | Durability | Tool |
|-------|-------|-----------|------|
| Tactical steps | Within a single action | Minutes | bon (steps) |
| Bon items | Project-level outcomes | Days–weeks | bon |
| Handoffs | Session-to-session baton | One transition | trousse |
| **Garde-manger** | **All past sessions** | **Permanent** | **garde-manger** |
| MEMORY.md | Cross-project patterns | Long-lived | manual |

Bon tracks what needs doing *now*. Garde-manger remembers what was done *before*. Handoffs from trousse are one of garde-manger's source types — once a handoff has been consumed by the next session, it gets indexed into the permanent record. The `/garde` skill is loaded on demand within sessions when retrieval is needed, keeping it out of context until called for.

This is the "memory is layered, not monolithic" principle in action — stock, jus, and reduction kept at different concentrations for different purposes.

## CLI and skill

Garde-manger has two interfaces: a CLI for maintenance (`garde scan`, `garde status`, `garde rebuild`) and a skill for in-session retrieval. The CLI is what you run between sessions to keep the index current. The skill is what a Claude session loads when it needs to search history.

## Repo

Install, usage, and CLI reference: [github.com/spm1001/garde-manger](https://github.com/spm1001/garde-manger)

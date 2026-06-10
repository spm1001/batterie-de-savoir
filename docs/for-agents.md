---
layout: default
title: For Agents
---

# For Agents

This repo is the documentation site for the Batterie de Savoir — a suite of tools for AI-assisted knowledge work.

## Vocabulary

{% comment %}GENERATED:vocabulary:START{% endcomment %}
| Term | Meaning |
|------|---------|
| **Bon** | Work tracker — outcomes, actions, tactical steps (GTD, not Agile) |
| **Trousse** | Skills, hooks, data analysis, and session lifecycle for Claude Code |
| **Garde-manger** | Persistent, searchable memory across sessions |
| **Jeton** | Google OAuth token management — scopes, refresh, multi-mode auth |
| **Mise (en Space)** | Content fetching from Google Workspace and the web (MCP server) |
| **Passe** | Fast browser automation via Chrome DevTools Protocol (CDP) |
| **Plongeur** | Streamlit data exploration UI powered by Vertex AI and BigQuery |
| **Todoist GTD** | Todoist integration — human-owned tasks, weekly review, pattern detection |
| **Aboyeur** | Multi-session orchestrator — alternates workers and reflectors |
| **Tafelmusik** | Collaborative CRDT editing — Yjs Y.Text + CodeMirror for real-time co-authoring |
{% comment %}GENERATED:vocabulary:END{% endcomment %}

### GTD & Brigade Terms

| Term | Meaning |
|------|---------|
| **Brigade** | The full tool suite, named after a kitchen's brigade de cuisine |
| **Outcome** | A desired result, not a task — the unit of work in bon |
| **Action** | A concrete next step that moves an outcome forward |
| **Brief** | The why / what / done fields attached to every bon item |
| **Handoff** | Markdown file carrying context from one session to the next |
| **Skill** | Behavioural document that teaches an agent how to use a tool |
| **Draw-down** | Reading a brief and activating its tactical steps for work |
| **Draw-up** | Filing completed work with full briefs for future sessions |

## Tool Routing

{% comment %}GENERATED:tool-routing:START{% endcomment %}
| Need | Use | NOT this |
|------|-----|----------|
| Track work, outcomes, actions | **bon** | — |
| Session lifecycle (/open → work → /close) | **trousse** | — |
| BigQuery analysis | **trousse** | mise |
| Search past sessions | **garde-manger** | — |
| Google OAuth tokens (acquire, refresh, status) | **jeton** | — |
| Fetch Google Workspace content | **mise** | passe |
| Clean article / blog extraction | **mise** | passe |
| DOM-faithful extraction (tables, code blocks) | **passe** | mise |
| Screenshots, browser interaction, form filling | **passe** | — |
| Non-technical data exploration UI | **plongeur** | trousse |
| Track human-owned tasks and deadlines | **todoist-gtd** | bon |
| Multi-session orchestration | **aboyeur** | — |
| Co-edit a document with Sameer in real time | **tafelmusik** | — |
| Comment on specific text passages inline | **tafelmusik** | — |
{% comment %}GENERATED:tool-routing:END{% endcomment %}

## Dependency Direction

What feeds what — arrows show data flow.

{% comment %}GENERATED:dependency-direction:START{% endcomment %}
| Source | → | Destination |
|--------|---|-------------|
| Mise en Space, Passe | → | Files on disk (content deposit) |
| Jeton | → | mise (OAuth credentials for Google APIs) |
| Bon | → | trousse (hooks inject tactical state) |
| Trousse | → | bon (session open/close triggers draw-down/draw-up) |
| Garde-manger | → | Any session (search retrieves past context) |
| Aboyeur | → | Multiple sessions (spawns workers, collects results) |
| Tafelmusik | → | Files on disk (flush_doc writes .md + git commits) |
| All tools | → | Filesystem (files are the protocol — no IPC, no daemons) |
{% comment %}GENERATED:dependency-direction:END{% endcomment %}

## Memory Layers

Thinnest to thickest — reach for the thinnest layer that has what you need.

| Layer | Scope | Durability | When to reach for it |
|-------|-------|------------|---------------------|
| **Tactical steps** | Within a single action | Session | Currently working on a drawn-down action |
| **Bon items** | Project-level outcomes | Persistent | Planning, prioritising, reviewing work |
| **Handoffs** | Session-to-session | Until next session | Starting a new session on the same project |
| **Garde-manger** | All sessions, all projects | Permanent | Stuck, need past decisions, patterns, or context |
| **MEMORY.md** | Cross-project patterns | Permanent | Recurring lessons learned over time |

## Key Repos

{% comment %}GENERATED:key-repos:START{% endcomment %}
| Tool | Repo |
|------|------|
| Bon | [spm1001/bon](https://github.com/spm1001/bon) |
| Trousse | [spm1001/trousse](https://github.com/spm1001/trousse) |
| Garde-manger | [spm1001/garde-manger](https://github.com/spm1001/garde-manger) |
| Jeton | [spm1001/jeton](https://github.com/spm1001/jeton) |
| Mise en Space | [spm1001/mise-en-space](https://github.com/spm1001/mise-en-space) |
| Passe | [spm1001/passe](https://github.com/spm1001/passe) |
| Plongeur | [spm1001/plongeur](https://github.com/spm1001/plongeur) |
| Todoist GTD | [spm1001/todoist-gtd](https://github.com/spm1001/todoist-gtd) |
| Aboyeur | [spm1001/aboyeur](https://github.com/spm1001/aboyeur) |
| Tafelmusik | [spm1001/tafelmusik](https://github.com/spm1001/tafelmusik) |
{% comment %}GENERATED:key-repos:END{% endcomment %}

| Tool | Repo |
|------|------|
| This docs site | [spm1001/batterie-de-savoir](https://github.com/spm1001/batterie-de-savoir) |

## Installation

Two paths:

**Plugin marketplace** (Claude Code 2.1+): `/plugin marketplace add spm1001/batterie` then `/plugin install <tool>@batterie`. Handles skills, hooks, and MCP config. CLI tools (bon, passe, todoist) still need `uv tool install` separately.

**Manual** (any agent): Clone repo → run `install.sh` or create symlinks per tool's README. Gives short command names (`/close` vs `/trousse:close`).

## What's Generated vs Authored

| File type | Status |
|-----------|--------|
| `bon.txt`, `.bon/` files | **Generated** by bon CLI — do not hand-edit |
| `handoff-*.md` | **Generated** by trousse /close — do not hand-edit |
| `mise-fetch/` deposits | **Generated** by mise — ephemeral, not committed |
| `SKILL.md` files | **Authored** — the training material for each tool |
| `CLAUDE.md` / `AGENTS.md` | **Authored** — repo-level agent guidance |
| `MEMORY.md` | **Authored** — distilled cross-project patterns |

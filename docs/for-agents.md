---
layout: default
title: For Agents
---

# For Agents

This repo is the documentation site for the Batterie de Savoir — a suite of tools for AI-assisted knowledge work.

## Vocabulary

| Term | Meaning |
|------|---------|
| **Bon** | Work tracker — outcomes, actions, tactical steps (GTD, not Agile) |
| **Trousse** | Skills, hooks, and session lifecycle for Claude Code |
| **Mise (en Space)** | Content fetching from Google Workspace and the web (MCP server) |
| **Passe** | Fast browser automation via Chrome DevTools Protocol (CDP) |
| **Garde-manger** | Persistent, searchable memory across sessions |
| **Consommé** | BigQuery data analysis — messy data in, clear insights out |
| **Aboyeur** | Multi-session orchestrator — alternates workers and reflectors |
| **Guéridon** | Mobile web UI for Claude Code |
| **Brigade** | The full tool suite, named after a kitchen's brigade de cuisine |
| **Outcome** | A desired result, not a task — the unit of work in bon |
| **Action** | A concrete next step that moves an outcome forward |
| **Brief** | The why / what / done fields attached to every bon item |
| **Handoff** | Markdown file carrying context from one session to the next |
| **Skill** | Behavioural document that teaches an agent how to use a tool |
| **Draw-down** | Reading a brief and activating its tactical steps for work |
| **Draw-up** | Filing completed work with full briefs for future sessions |

## Tool Routing

| Need | Use | NOT this |
|------|-----|----------|
| Track work, outcomes, actions | **bon** | — |
| Session lifecycle (/open → work → /close) | **trousse** | — |
| Fetch Google Workspace content | **mise** | passe |
| Clean article / blog extraction | **mise** | passe |
| DOM-faithful extraction (tables, code blocks) | **passe** | mise |
| Screenshots, browser interaction, form filling | **passe** | — |
| Search past sessions | **garde-manger** | — |
| BigQuery analysis | **consommé** | mise |
| Multi-session orchestration | **aboyeur** | — |
| Mobile access to Claude Code | **guéridon** | — |

## Dependency Direction

What feeds what — arrows show data flow.

| Source | → | Destination |
|--------|---|-------------|
| mise, passe | → | Files on disk (content deposit) |
| bon | → | trousse (hooks inject tactical state) |
| trousse | → | bon (session open/close triggers draw-down/draw-up) |
| garde-manger | → | Any session (search retrieves past context) |
| aboyeur | → | Multiple sessions (spawns workers, collects results) |
| All tools | → | Filesystem (files are the protocol — no IPC, no daemons) |

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

| Tool | Repo |
|------|------|
| Bon | [spm1001/bon](https://github.com/spm1001/bon) |
| Trousse | [spm1001/trousse](https://github.com/spm1001/trousse) |
| Mise en Space | [spm1001/mise-en-space](https://github.com/spm1001/mise-en-space) |
| Passe | [spm1001/passe](https://github.com/spm1001/passe) |
| Garde-manger | [spm1001/garde-manger](https://github.com/spm1001/garde-manger) |
| Consommé | [spm1001/consomme](https://github.com/spm1001/consomme) |
| Aboyeur | [spm1001/aboyeur](https://github.com/spm1001/aboyeur) |
| Guéridon | [spm1001/gueridon](https://github.com/spm1001/gueridon) |
| This docs site | [spm1001/batterie-de-savoir](https://github.com/spm1001/batterie-de-savoir) |

## What's Generated vs Authored

| File type | Status |
|-----------|--------|
| `bon.txt`, `.bon/` files | **Generated** by bon CLI — do not hand-edit |
| `handoff-*.md` | **Generated** by trousse /close — do not hand-edit |
| `mise-fetch/` deposits | **Generated** by mise — ephemeral, not committed |
| `SKILL.md` files | **Authored** — the training material for each tool |
| `CLAUDE.md` / `AGENTS.md` | **Authored** — repo-level agent guidance |
| `MEMORY.md` | **Authored** — distilled cross-project patterns |

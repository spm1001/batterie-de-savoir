---
layout: default
title: Aboyeur
---

# Aboyeur

*The caller.*

In a professional kitchen, the aboyeur stands at the pass — they don't cook, they call the tickets, check every plate before it goes out, and coordinate timing between stations. When something's wrong, they send it back. Aboyeur does the same for Claude sessions. It alternates **worker** sessions (do the work) with **reflector** sessions (review the work), using handoff files as the protocol between them. Each session gets a clean context, fresh eyes, and clear direction. The result is sustained, multi-session work that doesn't degrade as context fills up.

## When to use / When NOT to use

**Use Aboyeur when:**
- You have a body of work that exceeds a single context window — multiple bon items, a long refactor, a documentation pass across several repos
- You want genuine review, not just continuation — a fresh session that asks "what was missed?" rather than "what's next?"
- You're stepping away and want sessions to keep making progress, paging you only when genuinely stuck

**Do NOT use Aboyeur when:**
- The work fits comfortably in one session — the overhead of worker/reflector alternation isn't worth it for a quick fix
- You want tight, interactive control — Aboyeur is for autonomous stretches, not pair programming
- There's no [Bon](bon) in the project — without tracked work items, the orchestrator has nothing to drive toward (it won't break, but stuck-detection is disabled and you lose the main feedback signal)

## Key concepts

### Worker → Handoff → Reflector → Handoff → Worker

This is the core loop. The worker picks up work from Bon, builds, commits, and writes a handoff when context fills or work completes. The reflector reads that handoff with fresh eyes — what was missed? what could be better? what could go wrong? — does modest remedial work (bug fixes, plan adjustments, bon updates), and writes a handoff that becomes the next worker's brief.

The handoff files are the protocol. No custom formats, no databases, no IPC. Workers and reflectors communicate through the same handoff files that [Trousse's](trousse) `/open` and `/close` already use.

### The conductor is dumb

`conductor.sh` is the loop that alternates worker and reflector sessions. It does three things: start a session, wait for it to exit, check whether to page the human. That's it.

It pages when:
- A handoff contains `HUMAN REVIEW NEEDED`
- [Bon](bon) state hasn't changed for too long (configurable, default 60 minutes — detected via hash comparison)

All the intelligence lives in the prompt files (`worker-open.md` and `reflector-open.md`) and in the Claudes that read them. This is a deliberate design choice — the conductor is easy to reason about, easy to debug, and hard to break.

### The reflector prompt is the hard part

Writing a good reflector prompt is the highest-leverage work in the system. Too polite, and the reflector rubber-stamps everything — you've built an expensive echo chamber. Too aggressive, and it tears up good work. The reflector needs to find the things the worker couldn't see from inside its own context: missed edge cases, drifted plans, tests that pass but don't actually test anything.

### Harness-agnostic

Aboyeur doesn't care which agent runs the sessions. Adapters handle the mechanical differences — how to start a session, how to pass the initial prompt. Today there are adapters for [Pi](https://github.com/badlogic/pi-mono) and Claude Code. The prompts are the same regardless.

### Silent when no Bon

If the project has no `.bon/` directory, stuck-detection is disabled. The prompts still work — they just skip the bon-specific steps. But you lose the main feedback signal, so Aboyeur becomes a simple alternator without the ability to page when progress stalls.

## How it relates to other tools

Aboyeur is a **consumer** — it consumes [Bon](bon) (work tracking), [Trousse](trousse) (handoff protocol and session lifecycle), and agent harnesses, but owns none of them.

| Tool | What Aboyeur uses it for |
|------|--------------------------|
| [**Bon**](bon) | The work queue — outcomes and actions that the worker picks up and the reflector checks progress against. Bon's state hash is the stuck-detection signal. |
| [**Trousse**](trousse) | The handoff format — worker and reflector communicate through Trousse's handoff files. The `/open` and `/close` lifecycle gives each session clean entry and exit. |
| **Agent harness** | The Claude that does the work — Pi, Claude Code, or whatever adapter exists. Aboyeur starts sessions; the harness runs them. |

Aboyeur doesn't interact directly with [Mise](mise) or [Passe](passe) — but the workers and reflectors it spawns may use any of them, depending on the project's trousse configuration.

---

📦 **Repo:** [github.com/spm1001/aboyeur](https://github.com/spm1001/aboyeur) — install, usage, adapter reference

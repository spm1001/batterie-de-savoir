---
layout: default
title: Bon
---

# Bon — The Ticket

*GTD-flavoured work tracking for Claude-human collaboration.*

In a professional kitchen, the *bon* is the ticket — the slip of paper that tells the brigade what's been ordered and what needs to go out. This bon does the same for knowledge work: it tracks what needs doing, in GTD vocabulary, so that both human and AI can pick up where they left off. No sprints, no story points, no velocity — just outcomes, actions, and "what can I work on now?"

## When to Use / When NOT to Use

**Use bon when:**
- You need to track work across multiple sessions — outcomes that take days, actions that get interrupted
- You want a future Claude session to understand *why* something matters, not just *what* to do
- You're breaking a large goal into concrete next steps
- You want to file work for later with enough context that a cold session can pick it up

**Do NOT use bon when:**
- The task fits inside a single session — just do it
- You need project management features (dependencies, timelines, resource allocation) — bon is deliberately not that
- You want a shared team tracker — bon is per-workspace, for one human-AI pair
- You're tracking habits, recurring tasks, or calendared events — use Todoist or similar

## Key Concepts

### Outcomes and Actions

Bon has exactly two item types. **Outcomes** are desired results — the "what does done look like?" question. **Actions** are concrete next steps — the things you actually do. Actions can belong to an outcome, or stand alone. This is GTD's natural planning model: envision the result, then identify the next physical action.

### The Brief

Every item requires a **brief** with three fields: *why* (what makes this worth doing), *what* (the deliverable or change), and *done* (how you'll know it's finished). This isn't bureaucracy — it's the minimum context a future session needs to start working without asking "wait, what was this about?" The brief is what makes bon items portable across sessions.

### Tactical Steps — The Draw-Down Pattern

When you start working an action (`bon work`), bon generates **tactical steps** — a numbered checklist of how to get it done. You work through them one at a time with `bon step`, which marks the current step complete and shows the next. Only one action may have active tactical steps at a time — this enforces serial execution, the equivalent of working one ticket before grabbing the next. The final `bon step` auto-completes the action.

This is the **draw-down** pattern: read the item, activate steps, work with pauses. It prevents the drift that happens when an AI session wanders away from what was actually asked for.

### The Draw-Up Pattern

The inverse of draw-down. When you encounter work that shouldn't be done now, you **draw up** — file it as a new bon item with a complete brief. The brief quality matters because the session that eventually works this item will have no memory of the conversation where it was filed. Draw-up is how knowledge work accumulates without losing context.

### Readiness, Not Urgency

Bon's `list` command surfaces items by readiness — what's actionable right now — rather than by deadline or priority score. `bon wait` parks an item (and clears its tactical steps). `bon unwait` brings it back. This is GTD's core insight applied to AI collaboration: direct attention to what you *can* act on, not what's screaming loudest.

## How It Relates to Other Tools

Bon tracks *what* needs doing. The rest of the brigade handles the *how*:

- **[Trousse](trousse)** — Trousse's hooks inject bon's tactical state into every prompt via `bon-tactical.sh`. This means every Claude session automatically knows what step it's on without anyone having to explain. The `/open` skill loads bon context at session start.
- **[Aboyeur](aboyeur)** — The orchestrator reads `bon_hash` to detect whether sessions are making progress or stuck. Bon gives aboyeur the ground truth about work state.
- **[Garde-manger](garde-manger)** — Indexes bon items as a searchable source type, so you can find past work ("did we already do something like this?") across sessions.
- **[Mise](mise)**, **[Passe](passe)**, **[Consomme](consomme)** — These are the tools you reach for *while* working a bon action. Bon says what; they do the prep, the automation, the analysis.

## Design Principle

> **The human stays in the kitchen.** GTD not Agile, readiness not urgency.

Bon embodies this principle most directly. The vocabulary is deliberate — "outcomes" not "epics", "actions" not "stories", "waiting" not "blocked". The human decides what matters and when to engage. The AI works the station.

---

📦 **Install & usage:** [github.com/spm1001/bon](https://github.com/spm1001/bon)

[← Back to the brigade](../)

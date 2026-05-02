---
layout: default
title: Trousse
---

# Trousse — The Knife Roll

Trousse is a toolkit for Claude Code that solves its most fundamental limitation: statelessness. Every Claude Code session starts blank — no memory of what happened last time, no specialised knowledge of your tools, no sense of what's in progress. Trousse gives each session a briefing on arrival, a structured way to hand off when it leaves, and a drawer of skills it can reach for when the work demands something specific. It's the knife roll the chef carries between kitchens — open it up and everything you need is laid out in order.

## When to Use / When NOT to Use

**Use trousse when:**
- You want Claude Code sessions to remember what happened in the last session
- You need Claude to have specialised behaviours (diagramming, code review, browser automation, screenshots) without cramming instructions into the system prompt
- You're adopting any other tool in the batterie — trousse is how their skills get loaded

**Do NOT use trousse when:**
- You're doing a single, self-contained task that doesn't need session continuity
- You want a tool, not a toolkit — trousse doesn't *do* anything itself; it equips the agent to do things
- You're not using Claude Code — trousse is built around Claude Code's hook system and slash commands

## Key Concepts

### Session Lifecycle

Trousse turns each Claude Code session from a blank slate into a shift with a handover. Three hooks fire automatically:

- **Startup hook** — reads the last handoff for this project, loads the tactical brief, shows the agent what was done and what's next. The session begins oriented, not lost.
- **Prompt hook** — injects a lightweight tactical reminder on every prompt. Keeps the current step visible without the agent having to re-read state.
- **Close** — the `/close` command writes a structured handoff to `~/.claude/handoffs/<project>/`. The handoff contains three sections: **Done** (what was accomplished), **Next** (what should happen in the following session), and **Gotchas** (anything the next session needs to watch out for). This is the baton pass.

The handoff protocol is simple enough to be reliable and structured enough to be useful. It's markdown files in predictable locations — files are the protocol.

### The Skill Drawer

Skills are behavioural documents that teach Claude Code how to think with a specific tool or workflow. They're loaded on demand — not crammed into the system prompt — so they only cost tokens when needed.

The current skill set:

| Skill | What it teaches |
|-------|----------------|
| `/open` | Re-orient to session context; loads companion skills |
| `/close` | End-of-session ritual; writes the handoff |
| `/amp-close` | End-of-session ritual for Amp threads |
| `/titans` (`/review`) | Three-lens code review (hindsight, craft, foresight) |
| `/diagram` | Iterative diagram creation with render-and-check |
| `/screenshot` | Screen capture for verification |
| `/picture` | Image generation via Google Imagen |
| `/google-devdocs` | Google developer documentation lookup via REST API |
| `/server-checkup` | Systematic Linux server audit |
| `/github-cleanup` | Progressive GitHub account maintenance |
| `/sprite` | Controls inner Claude instances on VMs |
| `/setup` | Install skills from trousse onto a new machine |
| `/skill-forge` | Build and validate new skills |
| `/ia-presenter` | iA Presenter markdown authoring |

Each skill follows the principle that *the tool stays small; the skill carries the judgement*. Passe's skill teaches scout-then-act. Mise's skill teaches the search-then-retrieve loop. The heavy knowledge — patterns, gotchas, when to deviate — lives in the skill, loaded at the moment the agent picks up the knife.

### Symlinks, Not Copies

Trousse installs by creating symlinks from `~/.claude/` into the trousse repo. A `git pull` updates every skill immediately — no reinstall step. The `manifest.json` in claude-config is the single authority for what gets symlinked where. The `/setup` skill runs the installer.

## How It Relates to Other Tools

Trousse is the connective tissue of the batterie. It doesn't fetch content (that's mise), track work (that's bon), or remember across projects (that's garde-manger) — but it's how all of those tools get their skills loaded into a session.

- **Bon** — the `/open` command loads bon's skill, so each session knows how to read and update work items
- **Mise, Passe, Garde-manger** — each has a companion skill that trousse distributes; the tool is the CLI or MCP server, the skill is the behavioural training
- **Aboyeur** — orchestrates multiple sessions, and the handoff protocol that trousse maintains is the communication layer it coordinates across
- **Consomme** — its BigQuery analysis skill is loaded through trousse when data work begins

The design principle at work: *every tool ships with its own training*. Trousse is the mechanism that makes that principle operational — it's the drawer the training lives in, and the protocol that ensures each session opens it at the right time.

---

**Repo:** [spm1001/trousse](https://github.com/spm1001/trousse) — see the repo for installation and usage.

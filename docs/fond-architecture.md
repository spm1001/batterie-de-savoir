# Fond Architecture — Session Memory Redesign

Design brief from session 2026-04-04 (~/Repos, Mac). Spans bon, garde, and a new overnight composting process.

## Why "Fond"

In French cooking, **fond** is foundation stock — bones and scraps reduced into a rich base that everything else is built from. **Glace** is stock reduced further to a syrup, the most concentrated form.

| Kitchen | Ours |
|---------|------|
| Bones and scraps | Handoffs — session waste (what happened, what went wrong, what was learned) |
| Fond (stock) | Garde extractions — searchable base, derived from handoffs |
| Glace (reduction) | understanding.md — the most concentrated, distilled project knowledge |

The overnight process is literally reduction: taking a day's handoffs and reducing them into richer, more concentrated forms. Like real stock-making, you do it when the bones accumulate, not during service.

"Fond" in French also means "foundation" or "basis" — which is what this architecture provides for the whole batterie session lifecycle.

## Design Alternatives Considered

Three options were explored before arriving at the current design:

**Option A: Fond (chosen).** Handoff as the hub, overnight composting, MEMORY.md left to Anthropic. Two systems operating on different layers without collision. Described in full below.

**Option B: The Living Document.** understanding.md as the *only* durable knowledge store. Everything else ephemeral. Maximum simplicity — one file per project, git-synced, grows naturally. Rejected because it's xkcd 927 (yet another standard) and single-document approaches haven't worked well in practice. Also ignores MEMORY.md entirely rather than working alongside it.

**Option C: The Mycelium.** Instead of syncing stores, connect them via a lightweight knowledge map — a markdown index mapping concepts to locations across all layers. The network IS the memory. Rejected as "plausible but a lot of work and another layer." Solves the finding problem but not the capturing problem.

The key reason Option A won: it's the only design where Anthropic's improvements make our system better rather than conflicting with it. When autoDream improves, our MEMORY.md topic files get better consolidation for free. When the Sonnet selector improves, our topic files are surfaced more accurately. Options B and C ignore Anthropic's system; Option A feeds it.

## The Problem

The session lifecycle produces too many artifacts with too much duplication. /close currently writes 6 outputs: handoff, contribution, staged garde extraction, bon updates, git commit, and triggers garde ingest. The handoff and staged extraction contain ~90% the same content — same Claude, same moment, two formats. Contributions are a separate file that serves a similar purpose to a handoff section. The auto-handoff (for unclosed sessions) spawns a background Opus call that races the next /open.

Meanwhile, MEMORY.md is fragmented across machines. Mac and Hezza have different absolute paths to the same repos (/Users/modha vs /home/modha), producing different sanitized keys and therefore different memory directories. The 15 repos that exist on both machines have frozen, identical MEMORY.md copies from February 2026 — never updated because new sessions create memories under the local prefix. Garde's 661MB database (8,555 sessions, 7,222 extractions) exists only on hezza. Mac's garde DB is empty.

## What We Learned About CC's Memory System

Analysed the Claude Code source on hezza (~/Repos/claude-code). Key findings:

**Memory is keyed by canonical git root, not CWD.** `findCanonicalGitRoot()` resolves through worktrees, so all worktrees of the same repo share one memory directory. Subdirectories of a repo also share with the root. The fragmentation is per-machine (different home dirs) and per-repo (sibling repos can't see each other), not per-CWD.

**autoDream is a background consolidation agent** that fires as a forked subagent when ≥24 hours have passed and ≥5 sessions have accumulated. It reads session transcripts, reviews existing memory files, merges/prunes/updates. Currently feature-flagged (tengu_onyx_plover). Four phases: orient → gather → consolidate → prune.

**Memory Recall uses a Sonnet selector.** At query time, CC scans all topic files' frontmatter, sends the manifest to Sonnet, which selects up to 5 relevant ones to inject. MEMORY.md is always loaded; topic files are loaded on-demand by relevance. Good frontmatter descriptions are load-bearing.

**Team Memory (tengu_herring_clock)** adds a team/ subdirectory for shared memories. Extensive path-traversal security. Syncs at session start. Currently cross-user, not cross-machine.

**/remember skill** (ant-only) proposes promoting auto-memory entries to CLAUDE.md or CLAUDE.local.md. The designed promotion pathway.

**CC explicitly excludes** code patterns, architecture, and git history from memory — these are "derivable." Our understanding.md fills the gap CC intentionally leaves: experiential knowledge that isn't derivable from reading the code cold.

## The Memory Landscape

Five persistence layers, each serving a different function:

| Layer | What | Where | Syncs | Maintained by |
|-------|------|-------|-------|---------------|
| understanding.md | Project soul — design values, landmines, experiential knowledge | .bon/ (git) | Git push/pull | /open synthesizes contributions |
| Handoffs | Session record — what happened, what to watch, what's next | .bon/handoffs/ (git) | Git push/pull | /close writes, /open consumes |
| MEMORY.md topics | Typed observations — user/feedback/project/reference | ~/.claude/projects/ | Per-machine only | Auto-memory during session, autoDream between sessions |
| Garde extractions | Searchable semantic archive over all sessions | SQLite (hezza) / Dolt (future) | Hezza only / Dolt sync (future) | Backfill cron, staged extraction, overnight (new) |
| Bon items | Tactical state — outcomes, actions, progress | .bon/ (Dolt) | Dolt push/pull | Human + Claude during sessions |

**Key insight: supple vs brittle.** Eric Evans coined "supple design" in Domain-Driven Design — systems where the natural contours of change are easy to find and follow. The opposite of brittle isn't just resilient (withstands stress) — it's a design that bends to new shapes without rearchitecting. In our context: things in .bon/ (git-tracked) are supple — they sync across machines naturally, survive CC upgrades, adapt as Anthropic evolves the memory system. Things in ~/.claude/ are brittle — per-machine, per-path, at Anthropic's mercy. This observation drove every design decision: put durable knowledge where git carries it, treat ~/.claude/ as a local cache maintained by Anthropic's machinery.

**Key insight: the handoff is the richest single-session artifact.** Written by a Claude with full context, pre-structured, pre-reflected. The staged garde extraction duplicates it in JSON. The contribution distills one paragraph from it. autoDream would benefit from finding it in the session transcript. Making the handoff the primary artifact and deriving everything else from it eliminates duplication.

## The Design

### Two-Zone Handoff

/close produces one file with two temporal zones:

```markdown
# Handoff — {DATE}

session_id: {ID}
purpose: {one line}

## Now (next session consumes for orientation)

### Gotchas
(what would trip up the next Claude)

### Risks
(what could go wrong with what we built)

### Next
(direction for next session)

### Commands
(verification or continuation commands)

## Compost (overnight processes into understanding.md + garde)

### Done
(what was accomplished)

### Reflection
(process observations, what worked, what didn't)

### Learned
(one paragraph — architectural knowledge that transcends this session,
written to stand alone without session context. This is what /open
synthesizes into understanding.md.)
```

### Simplified /close

Handoff (one file, two zones) + bon updates + git commit. No staged extraction. No separate contribution file. No Orient 6-question ceremony.

### Why Learned Is a Separate Section (Not Just Better Reflection)

Comparing real handoff/contribution pairs from the same session (itv-slides-formatter, 2026-03-22) revealed they produce fundamentally different content:

- **Handoff Reflection**: "The review-then-fix cycle was valuable — 8 issues identified, 6 fixed immediately. Doc quality needs the same rigour as code." — This is about *process*. How the session went, what worked.
- **Contribution (now Learned)**: "The ITV domain admin blocks creating new Apps Script deployments with ANYONE execution access. The production deployment already exists and can be updated to new versions..." — This is about *architecture*. How the system works and why.

The framing "what did you learn that transcends this session" produces architecturally different content from "what happened in this session." One faces outward at the system, the other faces inward at the work. The Learned section must stand alone without session context — it'll be synthesized into understanding.md which has no session awareness. This constraint is what forces the architectural perspective.

### Updated /open

Reads handoff → orients from Now zone → synthesizes Learned section into understanding.md. The synthesis is onboarding, not busywork — the act of integrating forces the new Claude to read the existing understanding.md, hold it in mind, find where the new knowledge fits, and rewrite. By the time it's done, it *knows* the project in a way that just reading understanding.md cold doesn't achieve. It's the difference between reading a textbook and being asked to update one.

Handoff stays on disk after processing — never deleted.

### Overnight Composting

New daily process, runs across all repos:

1. Reads unprocessed handoffs (needs a processed marker)
2. Produces garde extractions by parsing Compost zone sections into structured fields (Done → builds, Gotchas → friction, Reflection → learnings, Learned → patterns). Section parse, not LLM call.
3. Synthesizes any Learned sections not yet integrated by /open (safety net)
4. Falls back to cold JSONL processing via deglacer for sessions without handoffs (unclosed sessions)
5. Marks handoffs as processed

Runs alongside autoDream — no conflict. autoDream maintains MEMORY.md. Overnight maintains understanding.md + garde. Different domains, complementary.

### Three Temporal Rhythms

The session lifecycle has three rhythms that shouldn't be conflated:

| Rhythm | Cadence | Carries | Mechanism |
|--------|---------|---------|-----------|
| Rapid cycle | ~30 /close+/open pairs per day | Operational context (Gotchas, Next) | Handoff Now zone |
| Overnight | Daily batch across all repos | Durable insight (Learned→understanding.md, Done→garde) | Composting process |
| Anthropic's background | autoDream every 24h + 5 sessions | Typed observations (feedback, project, reference) | autoDream from JSONL transcripts |

Each rhythm serves different knowledge at different time horizons. The handoff's two-zone structure maps directly to the first two rhythms. Anthropic's system feeds itself from the handoff content in the transcript — the third rhythm runs independently, finding our handoffs as high-quality signal in the JSONL.

### Feeding Anthropic's System (the transcript insight)

We don't write to MEMORY.md directly. We don't need to.

The handoff is written during the session using the Write tool. That Write call — file path, content, every section — lands in the session's JSONL transcript. When autoDream greps the transcript for signal, it finds a pre-structured, pre-reflected summary of the entire session sitting right there, written in plain prose, already structured into the exact categories autoDream wants to extract (learnings, friction, patterns).

The handoff is better signal than anything else in the transcript. autoDream's prompt says "grep narrowly, don't read whole files." It's searching for signal in thousands of lines of tool calls and file reads. But the handoff is a concentrated payload — Done, Gotchas, Risks, Reflection — already written by a Claude that understood the session.

It's like leaving a neatly labelled box of leftovers in the fridge for someone who was going to rummage through the bins.

This means: the richer our handoff, the better autoDream's MEMORY.md consolidation. We improve Anthropic's system by writing better handoffs, without touching ~/.claude/ at all. And when autoDream ships and improves, the benefit flows back to us — better MEMORY.md means the Sonnet recall selector surfaces better topic files, which means our sessions start with richer context.

### Auto-Handoff Simplification

Drop the background Opus call. Mechanical only: git commits + bon state + (auto) marker. Instant, no race condition. Overnight handles the rich extraction for unclosed sessions.

### Scratch/Workbench Routing

Scratch repos are transit points. /close in a workbench repo infers the target from bon item prefixes (e.g., passe-hifope → route to passe) and writes the handoff to the target repo's .bon/handoffs/.

### Handoffs Are Permanent

Never deleted. The handoff is the permanent session record. understanding.md is the living synthesis. garde is the searchable index.

## Workstreams

### 1. Bon — session lifecycle (bon repo)
- Two-zone handoff template
- Simplified /close skill
- Updated /open skill (synthesize Learned, no contributions pipeline)
- Scratch-to-target routing
- Mechanical-only auto-handoff (strip Opus call)
- Process and retire existing .bon/contributions/ files

### 2. Garde — handoff-native extraction (garde repo)
- Handoff adapter: parse two-zone format into extraction fields
- Retire staged extraction pipeline
- Replace ccconv with deglacer for fallback path
- Test extraction quality from handoff sections

### 3. Overnight composting (new, location TBD)
- Daily process across all repos
- Processed marker design
- Deglacer fallback for unclosed sessions
- Cross-machine: runs on hezza, reads git-synced handoffs from both machines

### 4. Cleanup
- Process 15 pending contribution files across repos
- Backfill existing handoffs into garde with new adapter (or just new ones going forward?)
- Update understanding.md in bon and garde repos
- End-to-end test of new /close → /open → overnight cycle

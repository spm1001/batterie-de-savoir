# Batterie de Savoir — Docs Site Plan

## What

Create `spm1001/batterie-de-savoir` — a public docs repo with GitHub Pages that serves as the canonical documentation for the entire tool suite. Individual tool READMEs link here for suite-level context. Both human-readable (the site) and machine-readable (raw markdown fetchable via curl/mise).

## Why

- `~/.claude` (claude-config) is personal — has paths, handoffs, MEMORY.md. Not shareable.
- Individual tool READMEs maintain inconsistent brigade tables (only passe and garde-manger have one, both now stale — missing consomme, gueridon, aboyeur).
- The suite needs a single canonical introduction that isn't tied to any one tool or any one person's config.
- The target audience is someone who wants to adopt individual tools or understand the philosophy — not a turnkey "install my kitchen" package.

## Content Structure

### Pages

1. **index.md** — The opening, brigade table, and design principles. This is mostly written already in `~/.claude/README.md` (the version edited today, 15 Feb 2026). Copy the opening through design principles. Drop everything from "What This Repo Is" onwards (that's private wiring).

2. **tools/** — One page per tool:
   - `bon.md` — work tracking, GTD vocabulary, the brief format
   - `trousse.md` — skills, hooks, session lifecycle, the /open → work → /close cycle
   - `mise.md` — content fetching, the 3 verbs, supported content types
   - `passe.md` — browser automation, the DSL, scout-then-act pattern
   - `garde-manger.md` — session memory, indexing, search
   - `consomme.md` — BigQuery analysis, the 5-stage methodology
   - `aboyeur.md` — multi-session orchestration, worker/reflector pattern
   - `gueridon.md` — mobile UI (may be thin — repo has no README yet)

   These should be richer than READMEs but not duplicates of CLAUDE.md. Think "the best parts of the README + the design intent, without the install commands." Each page should have:
   - What it is (one paragraph)
   - When to use it / when NOT to use it
   - Key concepts
   - How it relates to other tools in the brigade
   - Link to the repo for install/usage

3. **principles.md** — The design principles expanded with examples. The README has the tight versions; this page can breathe.

4. **getting-started.md** — How to adopt individual tools. NOT a "clone this and run setup" guide. More like: "If you want session memory, start with garde-manger. If you want work tracking, start with bon. Here's how they compose."

5. **for-agents.md** — The structured, low-prose reference page for AI agents arriving at this repo. Key files, vocabulary, tool routing table, what's generated vs authored. Follows the patterns from the research (see below).

### Static Site Generator

Keep it minimal. Options:
- **Just markdown + GitHub Pages with Jekyll** (zero config, GitHub does the build, no dependencies)
- **mkdocs-material** (nicer output, search, dark mode, but adds a Python dependency)

Recommendation: Start with raw Jekyll (default GitHub Pages). If it's not enough, upgrade to mkdocs-material later. The content matters more than the chrome.

### Machine-Readability

Raw markdown files are fetchable at `https://raw.githubusercontent.com/spm1001/batterie-de-savoir/main/docs/index.md` etc. Agents can use `mise fetch` or `curl` to get them. No need for llms.txt — that convention has near-zero actual consumption by LLM providers (see research below). The raw markdown IS the machine-readable format.

## Design Principles (final ordering, as agreed)

1. **Files are the protocol** — filesystem as shared state, folder-native thinking
2. **Token-efficiency** — context is the most precious ingredient
3. **Layered memory** — stock, jus, reduction — right context at right concentration
4. **Filleting knives** — tiny verb surfaces, brigade of specialists
5. **Tools referee themselves** — explicit "when NOT to use this" routing
6. **Every tool ships with its own training** — tool stays small, skill carries the judgement
7. **The human stays in the kitchen** — GTD not Agile, readiness not urgency

## Research Context

### llms.txt — Skip It
- Proposed by Jeremy Howard (Answer.AI), Sep 2024
- Well-designed spec (structured markdown index at /llms.txt)
- 800k+ sites adopted, but zero major LLM providers confirmed they read it
- Google's John Mueller compared it to the keywords meta tag
- SE Ranking study of 39k domains: no correlation with AI citations
- The raw markdown approach already works — agents can fetch .md files directly

### What Agents Need from Docs
From subagent research (5 respondents, no suite context):
- Vocabulary definitions (every project invents terms — the kitchen names need explaining)
- Dependency direction between tools (what feeds what)
- "When NOT to use this" routing (agents waste time with wrong tools)
- Structured > prose for procedures; prose > structured for principles
- "Do Not Edit" markers for generated content
- Key files list (the 5-8 load-bearing walls)

### The Emerging Convention
- README.md = for humans discovering the project
- CLAUDE.md / AGENTS.md / .cursorrules = for agents working in the project
- Separate files for separate audiences is winning over "one file serves both"
- The `for-agents.md` page on the docs site serves the cross-tool agent guidance role

## What's Already Done

- [x] Brigade table — all 8 tools, complete
- [x] Design principles — written, ordered, refined
- [x] Opening prose — Sameer wrote the personal voice version
- [x] Suite name — "Batterie de Savoir" confirmed, namespace clear on GitHub
- [x] All repos cloned and synced on Mac
- [x] manifest.json updated for bon rename + new repos (consomme, gueridon, aboyeur)
- [x] All symlinks healthy, bon CLI installed, setup-from-manifest.sh runs clean

## What the Next Claude Needs to Do

1. Create the `spm1001/batterie-de-savoir` repo on GitHub
2. Set up GitHub Pages (just enable it on main branch, /docs folder)
3. Copy the opening + brigade + principles from `~/.claude/README.md` into `docs/index.md`
4. Write the per-tool pages (read each tool's README.md and CLAUDE.md for source material)
5. Write `for-agents.md` with the structured reference format
6. Write `getting-started.md` with the "adopt one tool at a time" approach
7. Update individual tool READMEs to link to the docs site for suite context (replacing stale brigade tables)
8. Strip the private wiring sections from `~/.claude/README.md` — keep it as the internal reference, not the public face

## Source Material Locations

| What | Where |
|------|-------|
| Suite README (opening, principles) | `~/.claude/README.md` |
| Bon README + CLAUDE.md | `~/Repos/bon/` |
| Trousse README | `~/Repos/trousse/` |
| Mise README | `~/Repos/mise-en-space/` |
| Passe README + CLAUDE.md | `~/Repos/passe/` |
| Garde-manger README | `~/Repos/garde-manger/` |
| Consomme README | `~/Repos/consomme/` |
| Aboyeur README | `~/Repos/aboyeur/` |
| Gueridon | `~/Repos/gueridon/` (no README yet) |
| Research: agent doc needs | This plan file (Research Context section above) |
| Research: llms.txt | This plan file (Research Context section above) |

---
layout: default
title: Passe
---

# Passe — The Pass

Fast browser automation for Claude Code. One WebSocket connection, one process, no daemon. Where MCP-based browser tools need a model round-trip per action (~6 seconds each), Passe does everything in a single Bash call via raw Chrome DevTools Protocol. Navigate + screenshot in 213ms vs ~12,600ms. The speed comes from the protocol, not the hardware.

## When to Use / When NOT to Use

**Use Passe when you need:**
- Screenshots of web pages or application state
- Interaction with web UIs — clicking, typing, filling forms, selecting options
- DOM-faithful content extraction — tables, code blocks, structured markup that a readability-first parser would flatten
- Scouting an unknown page to discover interactive elements before scripting against them

**Do NOT use Passe when:**
- You need clean article or blog extraction — **use [Mise](mise)** instead. Its readability pipeline produces cleaner markdown for prose content, with less overhead.
- You want to fetch a Google Doc, Sheet, or Gmail thread — **use [Mise](mise)**, which handles Workspace content natively via MCP.
- You need to run a long-lived browser session or persistent scraping — Passe is designed for short, sharp interactions within a single Claude session, not background daemons.

## Key Concepts

### Line-Based DSL

Each Passe script is a sequence of lines, one verb per line, passed to a single Bash invocation. No SDK, no async orchestration, no multi-file setup. The entire interface fits in working memory.

**Navigate:** `goto`, `back`, `forward`, `scroll`
**Interact:** `click`, `click-text`, `type`, `fill`, `select`, `press`, `hover`
**Observe:** `screenshot`, `snapshot`, `read`, `eval`
**Control:** `wait`, `wait-for`, `wait-navigation`, `viewport`, `assert`, `log`

~20 verbs. That's the whole surface.

### Scout-Then-Act

The core workflow pattern. On an unknown page, run `snapshot` first — it lists every interactive element with its CSS selector. Then write your interaction script based on what the snapshot found. This avoids guessing at selectors, which is the most common failure mode in browser automation.

### `snapshot` vs `read`

Two observe verbs, two purposes. `snapshot` scouts — it returns a structured list of interactive elements (buttons, links, inputs) with their selectors, useful for writing scripts. `read` extracts — it runs Readability.js + Turndown.js inside Chrome's V8 to produce markdown from the visible content, faithful to the DOM structure including tables and code blocks.

### Structured Output

Every step emits NDJSON on stderr; the summary lands on stdout. Claude parses the JSON directly — no screen-scraping of terminal output, no regex on HTML. This keeps context clean and token costs predictable.

### Auto-Start

If no Chrome debug instance is running, Passe starts one. No manual setup, no "run this first" preamble.

## How It Relates to Other Tools

Passe and [Mise](mise) share the content-extraction space but referee each other. Passe's docs say "for clean articles, use mise." Mise's skill says "for DOM-faithful extraction, use passe read." The dividing line: if you need the structure of the page (tables, interactive elements, code blocks), use Passe. If you need the meaning of the text (article body, blog post), use Mise.

[Bon](bon) may track work that requires browser interaction — Passe executes those actions but doesn't manage the work items. [Garde-manger](garde-manger) can later surface what a session discovered via Passe, since screenshots and extracted content land on disk where they're indexable.

Passe embodies the *filleting knives, not cleavers* principle most directly: ~20 verbs, tiny surface, the entire interface fits in working memory. The companion skill carries the judgement — the scout-then-act pattern, the verb vocabulary, the gotchas — so the tool itself stays small.

---

**Repo:** [spm1001/passe](https://github.com/spm1001/passe) — install, usage, and CLI reference.

[← Back to the Brigade](../)

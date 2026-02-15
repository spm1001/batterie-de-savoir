---
layout: default
title: Mise en Space
---

# Mise en Space

*Mise en place for knowledge work.*

Mise en Space is an MCP server that preps content from Google Workspace and the web — so Claude can cook with it. Google Docs, Sheets, Slides, Gmail, PDFs, Office files, web pages, video, audio, images: Mise fetches them, extracts the useful content, and deposits clean markdown or CSV to disk. Peel and pith removed, everything prepped and in its place, ready for the chef to use. It's the sous-chef that does the unglamorous prep work — the chopping, the straining, the portioning — so the context window stays clean and the agent can focus on thinking.

## When to use it

- You need content from Google Drive or Gmail inside a Claude session
- You want to search across Drive and Gmail from one place
- You need to fetch a web page as clean markdown (not raw HTML)
- You need to extract text from a PDF, Office file, or media file
- You want to create a Google Doc, Sheet, or Slides deck from markdown

## When NOT to use it

- **DOM-faithful extraction** (tables, code blocks, interactive elements) — use [Passe](passe) with its `read` verb instead. Mise optimises for clean article text; Passe preserves the DOM structure.
- **BigQuery or data warehouse queries** — use [Consommé](consomme). Mise fetches *documents*, not *datasets*.
- **Browser automation** (clicking, filling forms, navigating SPAs) — use [Passe](passe). Mise fetches static content; it doesn't interact with pages.

## Key concepts

### Three verbs

Mise has exactly three tools: **search**, **fetch**, and **create**. That's ~3,000 tokens of tool definitions. (Google's own Workspace MCP server exposes ~50 tools at ~15,000 tokens — five times the context cost for a surface area no agent can hold in working memory.) The small verb surface means an agent can learn the entire interface from a single skill load and never need to re-read the docs.

### Sous-chef philosophy

Each call does the prep work you'd want done, not just the minimum. Fetch a Google Doc and you get the comments too. Fetch a Gmail thread and you get the attachments extracted. Search Gmail and you get subjects, senders, and snippets — not a bag of thread IDs that require five follow-up calls. One call, rich results.

### Filesystem deposits

Fetched content goes to disk as markdown or CSV files in a `mise-fetch/` directory — it does **not** get injected into the context window. The agent gets back a path and reads what it needs. This is the single most important design decision in Mise, and it directly implements the batterie's principle that *token-efficiency is a first-class constraint*. A 40-page Google Doc deposited to disk costs zero context tokens until the agent actually needs a section of it.

### Clean extraction

Web pages come back as clean markdown with boilerplate stripped. PDFs go through markitdown with an OCR fallback for scanned documents. Google Slides render as structured text. The goal is always the same: content in a format Claude can reason about, with the noise removed.

### Architecture layers

The codebase separates concerns cleanly: `tools/` defines the MCP tool surface, `adapters/` handle I/O with external services, and `extractors/` do format-specific content extraction. The key rule: **extractors never import from adapters** — they're pure functions that transform content, with no I/O of their own. This makes them testable and composable.

### CLI mode

Mise also ships a CLI (`cli.py`) for agents that don't speak MCP — or for humans who want to fetch content from the terminal. Same capabilities, different entry point.

## How it relates to other tools

Mise is the station that preps content from the outside world. It sits at the boundary between the kitchen and the ingredients:

- **[Passe](passe)** — Mise and Passe share the web-fetching space but referee each other. Passe's own README says "for clean article/blog extraction, use mise." Mise's skill says "for DOM-faithful extraction (tables, code blocks, technical docs), use passe read." If you want the *text* of an article, Mise. If you want the *structure* of a page, Passe.
- **[Consommé](consomme)** — Consommé handles data in BigQuery; Mise handles documents in Workspace. Consommé's skill explicitly routes Workspace content requests to Mise.
- **[Garde-manger](garde-manger)** — Mise fetches content from the outside; Garde-manger retrieves context from past sessions. Different sources, same idea: get the right context to the agent without bloating the window.
- **[Bon](bon)** — Mise deposits to the filesystem; Bon reads from it. A session might search Gmail via Mise, find actions to track, and file them with Bon. The filesystem is the shared protocol.

Content deposited to disk by Mise is available to every other tool in the batterie — because [files are the protocol](../#design-principles).

---

→ [mise-en-space on GitHub](https://github.com/spm1001/mise-en-space) for installation and usage

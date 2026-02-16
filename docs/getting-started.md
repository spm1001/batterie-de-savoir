---
layout: default
title: Getting Started
---

# Getting Started

*Pick up one knife. Learn the cut. Then reach for the next.*

The batterie is not a framework you install. There's no `npx create-batterie-app`, no monorepo to clone, no setup wizard that wires everything together. Each tool is its own repo with its own install, and you adopt them one at a time based on what you actually need.

This is deliberate. A kitchen doesn't arrive fully stocked on day one — you acquire tools as your cooking demands them. Start with the problem you have right now, pick up the tool that solves it, and add the next one when you feel the gap.

## Where to Start

### "I want my sessions to remember what happened last time"

**Start with [Trousse](tools/trousse).** It's the knife roll — session hooks that inject a handoff from the last session, plus a drawer of skills that load on demand. Without trousse, every Claude Code session starts blank. With it, each session arrives briefed on where you left off.

This is the most common first pick, because statelessness is the first pain you feel.

📦 [spm1001/trousse](https://github.com/spm1001/trousse)

### "I need to track work across sessions"

**Add [Bon](tools/bon).** It's a GTD-flavoured work tracker — outcomes, actions, tactical steps — designed so both human and AI can pick up where things stand. Bon works best with trousse already in place, because the session hooks inject your current tactical state automatically.

📦 [spm1001/bon](https://github.com/spm1001/bon)

### "I want to search what happened in past sessions"

**Add [Garde-manger](tools/garde-manger).** It indexes your session transcripts and makes them searchable. When you're stuck on something you know you solved three weeks ago, garde-manger finds it. It benefits from having trousse handoffs as a source — more structured handoffs mean better search results.

📦 [spm1001/garde-manger](https://github.com/spm1001/garde-manger)

### "I need Google Workspace access (Mise, Consommé, or anything with Google APIs)"

**[Jeton](tools/jeton)** handles Google OAuth for the suite. It acquires, refreshes, and manages tokens so the Google-facing tools don't have to reinvent auth. If you're adopting Mise or Consommé, you'll need Jeton first — it's the plumbing that makes their Google access work.

📦 [spm1001/jeton](https://github.com/spm1001/jeton)

### "I need to pull in content from Google Workspace or the web"

**[Mise en Space](tools/mise)** is an MCP server that fetches and preps content — Google Docs, Sheets, Slides, Gmail, web pages, PDFs, video, audio — and deposits clean markdown to disk. For Google Workspace content it uses **jeton** for authentication. If you work with Google Workspace, mise + jeton is probably your first pick regardless of anything else.

📦 [spm1001/mise-en-space](https://github.com/spm1001/mise-en-space)

### "I need to automate the browser"

**[Passe](tools/passe)** drives Chrome via DevTools Protocol — fast, headless, no Selenium. It's fully standalone, no dependency on other tools. If your work involves scraping, form-filling, or testing, you can start here without touching anything else.

📦 [spm1001/passe](https://github.com/spm1001/passe)

### "I need to analyse data in BigQuery"

**[Consommé](tools/consomme)** provides a structured methodology for BigQuery analysis — discover, understand, analyse, validate, present. It needs the BigQuery MCP server and works with either Claude Code or Gemini CLI. No dependency on the rest of the batterie.

📦 [spm1001/consomme](https://github.com/spm1001/consomme)

### "I want to orchestrate work across multiple sessions"

**[Aboyeur](tools/aboyeur)** is the capstone. It alternates worker and reflector sessions, using handoff files as the protocol between them. Aboyeur needs bon and trousse already in place — it orchestrates the infrastructure they provide. Don't start here. Get comfortable with the session lifecycle first.

📦 [spm1001/aboyeur](https://github.com/spm1001/aboyeur)

### "I want Claude Code on my phone"

**[Guéridon](tools/gueridon)** is a mobile web UI. It connects to your existing Claude Code setup and gives you tableside access from a phone or tablet.

📦 [spm1001/gueridon](https://github.com/spm1001/gueridon)

## How the Tools Compose

The tools are independent but they're designed to work together. Here's what feeds what:

**Trousse + Bon** is the natural first pair. Trousse provides the session lifecycle (hooks, handoffs, skills); bon provides the work tracking. Together they mean each session knows what happened last time *and* what needs doing next. Most of the batterie assumes this pair is in place.

**Jeton + Mise** — jeton provides OAuth credentials that mise needs for Google Workspace access. Without jeton, mise still works for web content but can't reach Drive, Gmail, or Sheets. If you're adding Google Workspace access, jeton is the prerequisite.

**Mise + Passe** complement each other. Mise fetches clean content from structured sources (Workspace, web articles). Passe automates the browser for everything else (interactive pages, form submissions, screenshots). Their skills even cross-reference each other — mise says "for DOM-faithful extraction, use passe"; passe says "for clean article extraction, use mise."

**Garde-manger + Trousse** — garde-manger gets better when trousse is producing structured handoffs. The handoffs become a high-quality source for indexing. Without trousse, garde-manger still works (it indexes raw transcripts), but the signal-to-noise ratio improves with structured session boundaries.

**Aboyeur** sits on top of everything. It uses bon for work items, trousse for session lifecycle, and handoff files for inter-session communication. It's the tool you reach for when the work exceeds a single context window and you need sustained, multi-session progress without degradation.

**Guéridon** extends the session lifecycle to mobile. The bridge spawns `claude -p` processes that load the same trousse skills, write the same handoffs, and track work in the same bon items. A session started from your phone is indistinguishable from one started in a terminal — same tools, same memory, same protocol. Where aboyeur orchestrates *multiple* sessions, guéridon untethers *one* session from the desk.

## Prerequisites

**An AI coding agent.** The batterie is built for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), but the filesystem-first design means most tools work with any agent that can read and write files.

**Python and uv.** Several tools (bon, garde-manger, jeton, mise, passe) are Python-based and use [uv](https://docs.astral.sh/uv/) for installation. If you don't have uv, that's your actual first step. (Consommé is a skill — a behavioural document — not a Python package. It has nothing to install via uv.)

**No monorepo.** Each tool installs independently from its own repo. There is no unified installer, no shared config, no dependency graph to resolve. This is the point.

---

[← Home](./) · [Design principles](principles) · [For agents](for-agents)

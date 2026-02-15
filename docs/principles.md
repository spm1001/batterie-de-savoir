---
layout: default
title: Design Principles
---

# Design Principles

The [index page](/) has the tight versions of these principles. This page has room to breathe — to show what each principle looks like in practice, and what goes wrong when you violate it.

---

## 1. Files are the protocol

**Handoffs are markdown. Work items are JSONL. Tactical state is a text file injected by a hook. There's no IPC, no daemon, no shared database between tools. Everything communicates through the filesystem.**

The filesystem is the one interface that every tool — human or AI — already knows how to use. It's inspectable, diffable, version-controllable, and survives any individual tool dying or being replaced. This is the deepest design choice in the batterie, and it's why knowledge work and code turn out to be so compatible — they're both folder-native ways of thinking.

### In practice

Bon stores its work items as `.jsonl` files — one JSON object per line, appendable, greppable, readable with any text editor. Handoff files between sessions are plain markdown, written to a known path, read by the next session's hook. Mise deposits fetched content to disk as markdown or CSV files, returning a path rather than injecting content directly. Every tool reads from and writes to the filesystem. There is no message bus, no socket, no service to keep running.

This means you can always see the state of the system by looking at the files. `ls` is your dashboard. `git diff` is your audit trail. Moving a file is a valid operation. Renaming a folder reorganises the work.

### The anti-pattern

The alternative is tools that communicate through in-memory state, shared databases, or API calls to each other. This creates invisible coupling — when tool A talks to tool B through a channel you can't see, you can't debug it, you can't inspect it between steps, and you can't replace either tool without understanding the protocol between them. Worse, when the agent's session crashes, all that shared state evaporates. Files on disk survive crashes, context exhaustion, and the human going to sleep. A daemon that needs to be running for tools to talk to each other is a daemon that will be down when you need it most.

---

## 2. Token-efficiency is a first-class constraint

**Context is the kitchen's most precious ingredient — expensive, finite, and ruined by clutter. Every tool treats the context window like a clean station.**

An agent's context window is not just limited, it's the primary bottleneck for everything it does. A cluttered context doesn't just cost tokens — it degrades reasoning. The signal-to-noise ratio of the context window directly determines the quality of the agent's work.

### In practice

Mise fetches web pages, Google Docs, and Gmail threads but deposits the extracted content to a file on disk, returning only the path. The agent reads what it needs from that file. Compare this to tools that dump an entire web page into the conversation — suddenly the agent is reasoning through a wall of nav bars, cookie banners, and footer links.

Bon's skill includes the instruction "NEVER run `bon list` via Bash — Read the file instead." Why? Because the CLI's terminal-formatted output — with ANSI colours, box-drawing characters, and padding — is two to three times larger than the raw data. The same information, presented through `Read bon.txt`, arrives as clean structured text that the agent can parse without wading through decoration.

Passe returns structured JSON summaries from browser interactions, not raw HTML. When it scouts a page, you get element counts and selectors, not the full DOM.

### The anti-pattern

Tools that "helpfully" inject their full output into the conversation. A web scraper that returns the entire page. A search tool that dumps twenty results with full snippets. A file browser that renders a tree with ASCII art. Each one individually seems fine — the context window is large, after all. But context fills the way a station gets cluttered: gradually, then all at once. By the time the agent notices, it's already lost track of what it was doing three steps ago. Token-efficiency isn't about saving money (though it does). It's about preserving the agent's ability to think clearly.

---

## 3. Memory is layered, not monolithic

**A good kitchen keeps its stock, its jus, and its reductions in different vessels for different purposes. The batterie has five memory layers, each with different durability, scope, and cost.**

Not all memory is created equal. The thing you need to remember for the next ten seconds is different from the thing you need to remember across projects for months. Treating all memory the same — shoving everything into one store — means either paying too much for ephemeral state or losing important patterns in a flood of tactical detail.

### In practice

The five layers, from most ephemeral to most durable:

1. **Tactical steps** — within a single bon action. "Run the build, check for errors, fix the type mismatch." These exist only for the current work session and disappear when the action completes.
2. **Bon items** — project-level outcomes and actions. "Ship the API redesign." These persist across sessions within a project, tracked in `.jsonl` files.
3. **Handoffs** — session-to-session baton passes. Written at the end of one session, read at the start of the next. They carry the minimum context needed to resume: what was done, what's next, what's blocked.
4. **Garde-manger** — searchable history across all sessions. Every session gets indexed. When you're stuck or disoriented, you search here: "have we solved this before? what did we decide about X?"
5. **MEMORY.md** — cross-project patterns learned over time. "This user prefers X. This codebase has a quirk around Y." The most concentrated, most durable, most carefully curated layer.

A fresh session reaches for the handoff. A stuck session searches garde-manger. A recurring pattern gets distilled into MEMORY.md. Each layer is the right concentration for its purpose — you don't reduce your entire stock into demi-glace, and you don't use demi-glace to blanch vegetables.

### The anti-pattern

A single flat memory store — one database, one long file, one vector index — where tactical noise ("ran npm install, got three warnings") sits next to strategic insight ("this team's data model assumes single-tenancy"). The tactical noise drowns the strategic insight. The agent retrieves twenty results and can't tell which matter. Or worse: no memory at all, so every session starts from zero, re-discovering the same things, making the same mistakes, asking the same questions the human answered three sessions ago.

---

## 4. Filleting knives, not cleavers

**Each tool has a tiny verb surface. The tools are narrow enough that an agent can hold the entire interface in working memory without re-reading the docs.**

A tool the agent can't fully remember is a tool the agent will misuse. The verb surface of each tool — the number of commands, the number of options — is kept deliberately small. Not because we couldn't add more, but because the agent's ability to reason about the tool depends on fitting the whole thing in its head at once.

### In practice

Passe has approximately 20 verbs — navigate, click, type, scout, screenshot, and so on. That's the entire browser automation surface. Bon has 18 commands for all of work tracking. Mise has exactly 3: search, fetch, create. That's it. Search your Drive and Gmail, fetch content from a URL or file ID, create a Google Workspace document.

These are filleting knives — precise, single-purpose, requiring skill but rewarding it. The agent doesn't need to remember which of forty options to pass. It doesn't need to look up the docs mid-task. The entire tool fits in working memory, so the agent can reason about *what to do* rather than *how to invoke*.

### The anti-pattern

The Swiss Army knife tool. One CLI with a hundred subcommands, each with twenty flags. The agent forgets whether it's `--recursive` or `--deep`, whether the output format is set with `--format` or `--output-type`, whether the file argument comes before or after the URL. So it guesses, gets it wrong, wastes a round-trip, tries again. Or it re-reads the docs, burning context on information it already read three steps ago. A tool with a large surface area isn't more powerful — it's more expensive to use correctly, and more likely to be used incorrectly.

---

## 5. Tools referee themselves

**Every tool includes explicit "when NOT to use this" guidance — pointing the agent to the right station instead. Most tools only advocate for themselves. In a brigade, the stations direct traffic.**

This is the principle that makes the brigade work as a system rather than a collection of parts. Each tool knows its own boundaries and actively routes the agent elsewhere when the task doesn't fit.

### In practice

Passe's README says: "for clean article extraction, use mise." Passe is a browser automation tool — it can certainly load a web page and extract text. But mise does it better for articles, with cleaner output and less overhead. So passe says so.

Mise's skill says: "for DOM-faithful extraction (tables, code blocks, technical docs), use passe read." Mise extracts content beautifully for articles and blog posts, but when you need the exact structure of a page — the table layout, the code formatting — passe's DOM access is more faithful. So mise says so.

Consomme's skill says: "for Workspace content, use mise." Consomme is a BigQuery tool. If the agent needs a Google Doc, consomme could theoretically help (it has GCP credentials), but mise is purpose-built for it. So consomme redirects.

The result is that an agent holding any one tool's documentation can find its way to the right tool, even if it started at the wrong station.

### The anti-pattern

Tools that try to handle everything, or tools that silently fail when given a task outside their scope. The agent asks a browser automation tool to fetch an article. The tool dutifully launches a headless browser, loads the page, extracts the text — taking ten seconds and a hundred tokens where a simple HTTP fetch would have taken one second and ten tokens. The agent never learns there was a better option because the tool never mentioned one. Silence is the worst kind of routing.

---

## 6. Every tool ships with its own training

**Each tool is paired with a skill — a behavioural document that teaches the agent not just what the tool can do, but how to think with it. The tool stays small; the skill carries the judgement.**

A tool's CLI help tells you the verbs and flags. A tool's README tells you the concepts. But the *skill* — loaded on demand into the agent's context — teaches the workflow, the patterns, the gotchas, and the judgement calls. This separation is deliberate: the tool stays small and fast, while the heavy knowledge loads only when needed.

### In practice

Bon's skill teaches the draw-down workflow: `bon show` → `bon work` → `bon step`, preventing the agent from drifting away from the current action. It also teaches brief quality — what makes a good outcome statement versus a vague one. None of this is in the CLI itself.

Passe's skill teaches scout-then-act: always scout a page to understand its structure before attempting to interact with elements. This prevents the agent from clicking blindly at selectors that might not exist or might have changed.

Mise's skill teaches the file→email→meaning loop: search Drive first, then check Gmail for related context, then synthesise meaning from both. It also teaches Gmail operator syntax and comment-checking patterns that the tool's three simple verbs don't encode.

The skill is loaded at the moment the agent picks up the tool — "you fit the agent to the tooling by giving it the manual at the moment it picks up the knife." When the task is done, the skill's tokens are no longer needed. This is another instance of token-efficiency: heavy knowledge on demand, not permanently resident.

### The anti-pattern

Baking all the workflow knowledge into the tool's output — verbose help text, unsolicited suggestions, "did you mean…?" prompts. This makes every invocation expensive, even when the agent already knows what it's doing. The opposite failure is equally bad: a tool with no training at all, where the agent has to figure out the workflow from first principles every time. The skill is the middle path — available when needed, absent when not.

---

## 7. The human stays in the kitchen

**The work tracker uses GTD vocabulary — outcomes, next actions, waiting-for — rather than Agile tickets and sprints. This isn't cosmetic.**

The vocabulary you use shapes how you think about work. Agile vocabulary — sprints, story points, blockers, velocity — is designed for teams shipping software on cadence. GTD vocabulary — outcomes, next actions, waiting-for, readiness — is designed for an individual directing attention where it matters most. The batterie is built for the second case.

### In practice

GTD directs attention by *readiness* ("what can I act on right now?") rather than *urgency* ("what's overdue? what's blocked?"). This changes the fundamental question the agent asks. Instead of "what's the highest-priority ticket in the sprint?" it asks "what's the next physical action I can take on this outcome?" The first question leads to triage and status reporting. The second leads to actual work.

The aboyeur — the multi-session orchestrator — pages the human only when genuinely stuck, not for routine approval. The handoff system means a human can step away from the pass and come back to find the station in order. The tools don't nag, don't create artificial urgency, don't generate status reports nobody reads.

The human stays in the kitchen — present, in control, able to pick up the tongs when the moment calls for it — but not standing over the stove stirring every pot. Though honestly, which one of us is Remy and which one is Linguini changes by the hour.

### The anti-pattern

AI tools that adopt project-management vocabulary and ceremony. Daily standup summaries. Sprint retrospectives. Burndown charts for a team of one human and one agent. The ceremony exists because humans on teams need synchronisation rituals. A human working with an AI agent doesn't need synchronisation — they need clarity about what's ready to do next. Importing Agile vocabulary imports Agile assumptions: that work comes in fixed-size chunks, that velocity is measurable and meaningful, that blocked work should be escalated. None of these assumptions serve knowledge work particularly well. GTD's quieter vocabulary — "what's the next action?" — turns out to be exactly the right question for an agent to ask.

---

[← Back to index](/) · [Getting started](getting-started) · [For agents](for-agents)

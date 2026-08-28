---
layout: default
title: Arête
---

# Arête

*The fishbone.*

An **arête** is what's left when you fillet a fish: the clean spine with its ribs coming off it. Which is, if you squint, exactly what a mind map looks like — and exactly what this tool makes.

MindNode is lovely and has one maddening gap. Paste twenty lines into it and you get **one node containing twenty lines**, not twenty nodes. There's no setting for it. So you either retype the list by hand or you don't use the app for the thing lists are for.

```bash
pbpaste | arete --stdin --title "Q3 themes"     # list  -> map
arete --extract "Q3 themes"                     # map   -> Markdown
```

That's the whole tool. The rest of this page is the interesting part: *why* it isn't as simple as it looks.

## The one thing to understand: MindNode fails quietly

Almost everything that goes wrong here goes wrong without an error.

**Fire two imports back to back and the second one vanishes.** No dialog, no exit code, nothing in the log — the document simply never appears. Arête waits for each map to show up in MindNode's library before returning, which detects the drop and retries once, and incidentally makes back-to-back calls safe.

**Import an OPML file wrapped in its own root node and you get two centre nodes,** one inside the other, because MindNode already makes a root from the filename. This looks like an app bug and isn't.

**A map you typed in the app can read as empty.** MindNode's library holds a *base snapshot* plus an operation log; a map created by import has a complete snapshot, a map you typed has an all-but-blank one. Read the snapshot alone and a rich map reports as a single node called "Mind Map". Arête refuses rather than answering, and prefers MindNode's own exporter, which always sees the live document.

The theme is worth stating plainly, because it shaped the whole design: **when an operation can fail silently, the tool checks the world afterwards rather than trusting the exit code.** Appending re-reads the map and confirms it grew by exactly the number of nodes sent.

## Tags, and why they're opt-in

MindNode's importers disagree with each other about hash tags:

| Import format | A trailing `#word` |
|---|---|
| OPML — the default | stays literal text |
| FreeMind — `arete --tags` | becomes a real tag |
| TaskPaper | refused outright, despite being a declared document type |

`--tags` is a flag rather than the default because the same parsing quietly eats the number out of `issue #42`. Given a choice between a lost capability and lost text, the capability waits for a flag.

## Two directions, two routes

Getting a list **in** needs nothing installed — it's OPML, and MindNode imports it.

Getting a map **out** prefers MindNode's own exporter, reached through a small Shortcut you build once (the app's automation actions can't be called from a shell directly). Without it, arête falls back to decoding the library snapshot itself — protobuf, with a fractional sibling index for ordering — which is exact for imported maps and refuses when it can't be trusted.

The same Shortcuts route is how `--append` adds a list *under a node of a map you already have*, which plain import can never do, since it always mints a new document.

## macOS only — but not Mac-session only

The CLI drives a desktop app, so it wants a Mac. It does **not** want an interactive one: both directions work from a non-interactive ssh session, so a Claude on another machine can reach the Mac over Tailscale.

```bash
ssh my-mac 'export PATH="$HOME/.local/bin:$PATH"; arete --extract "Q3 themes"'
```

The plugin ships the `mindnode-mapping` skill everywhere; the `arete` command installs on the Mac with `uv tool install`.

## Repo

[spm1001/arete](https://github.com/spm1001/arete) — setup guides for both Shortcuts live in `docs/`.

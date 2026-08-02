---
layout: default
title: Accomplis
---

# Accomplis

*The commis.*

The commis is the junior chef who keeps the routine work moving so the stations can cook. Accomplis (the *fait accompli* — outcomes written as achievements, and the imperative of *accomplir*) is the suite's bridge to [Todoist](https://todoist.com) — an `accomplis` CLI plus a coaching skill that teaches Claude to work a GTD system properly rather than just poke an API. Until 2026-08-02 it shipped as **todoist-gtd**.

The split that gives it a reason to exist: **[Bon](bon) tracks Claude-collaborative work; Todoist holds human-owned tasks and deadlines.** A bon action is something a Claude session can pick up and finish. A Todoist task is something the human does with hands, calendar and willpower — book the dentist, chase the invoice, prep for Thursday. Two trackers isn't duplication; it's the boundary between "our work" and "your errands", and blurring it is how both lists rot.

The coaching skill is the judgement layer, and it gates every Todoist operation. It carries the GTD semantics the raw API can't: it discovers where each user's outcomes live (sections in some projects, tasks under status lanes in others) instead of assuming; workspace and personal items filter differently; weekly review walks stale outcomes and overcommitment patterns; and outcome language gets coached toward achievements ("Taught the team X") rather than activities ("Do X"). Without the skill, a Claude reads Todoist as a flat todo list and optimises the wrong thing.

## When to use / When NOT to use

**Use Accomplis when:**
- Triaging the human's Todoist inbox, or running a weekly review
- Coaching an outcome into achievement language, or spotting overcommitment
- Anything where the deliverable is *the human's system staying trustworthy*

**Do NOT use Accomplis when:**
- Tracking work a Claude session will execute — that's [Bon](bon), with briefs and tactical steps
- You need per-step execution state — Todoist tasks are atoms; bon actions carry `--how` and step tracking

## Prerequisites

Installs from the marketplace (`claude plugin install accomplis@batterie`); the session hook installs the `accomplis` CLI from source when missing. Needs a Todoist API token.

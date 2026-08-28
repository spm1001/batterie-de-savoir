# Changelog

> **This is the canonical CHANGELOG for the whole Batterie de Savoir suite.**
> Since the single-version cutover (suite 1.2.2, 2026-06-28) every published
> plugin ships at the same **suite** version, so there is one changelog, not
> one per plugin. Each entry is a suite release; the note names which
> plugin(s) the release carried. Per-repo `CHANGELOG.md` files still exist in
> each source repo for git browsing, but they are no longer vendored into the
> shipped plugins — every plugin ships a generated stub pointing back here.
>
> Maintained by `/batterie:publish` (engine: `scripts/publish.py`), which
> prepends an entry at each release. Entries below **1.8.2** were reconstructed
> from git history when the automation landed (bds-mawitu, 2026-07-12) — they
> are honest headlines, not exhaustive; the per-repo changelogs hold the detail.

## [1.79.2] - 2026-08-28

The close tap may now tick, add AND edit Toolmaking dispatch lines — the 2026-08-13 ticking sanction had never reached the skill

## [1.79.1] - 2026-08-28

Teleport scripts move inside the deglacer skill so they survive its migration; remote-sessions gains the rg fallback its sibling had

## [1.78.2] - 2026-08-28

deglacer: dedupe usage per request, and --doctor catches CC format drift

## [1.78.1] - 2026-08-28

Correction: the teleport-to-local session id IS computable — uuid5 over the resume URL, namespace read out of the CC bundle

## [1.78.0] - 2026-08-28

Deglacer can now translate a teleport session id into a resumable local UUID, and list the SDK-spawned sessions the resume picker hides

## [1.77.1] - 2026-08-26

Carrying deglacer: the requestId prefix names the billing lane, so session history splits by provider

## [1.77.0] - 2026-08-24

Carrying mise: crops= opt-out makes text-only PDF corpus walks 10x faster; page counts work on core installs; search and manifests carry the last-modifier (the only author signal on Shared Drives)

## [1.76.0] - 2026-08-24

Carrying mise: append tab= places a redraft in its own Google Doc tab; overwrite now refuses multi-tab destruction instead of silently flattening

## [1.75.5] - 2026-08-24

peer-messaging: cross-machine still works via ssh — correcting an overstatement

## [1.75.4] - 2026-08-24

Carrying mise: docx figures now survive fetch as viewable sidecar files, and markdown footnotes become real Docs footnotes — supersedes 1.75.3's first-cut footnote pass, which could corrupt emoji- or code-bearing docs

## [1.75.3] - 2026-08-24

Carrying mise: serverInfo reports the suite version and tool docs ride the public API (mise-vubeku); publish itself now pulls flavour siblings so mise-home can't fall silently stale

## [1.75.2] - 2026-08-24

peer-messaging says plainly that cross-machine messaging is gone with sonnette

## [1.75.1] - 2026-08-24

hublot points at sonner's receive path now that sonnette is gone

## [1.75.0] - 2026-08-24

Retiring sonnette: sonner is the suite's inter-session messaging

## [1.74.0] - 2026-08-24

Carrying mise: tool bodies run concurrently — parallel 3-fetch 5.1s → 2.4s; the interim serializer lock is gone, with per-resource guards where the state lives

## [1.73.0] - 2026-08-24

Ringing sonner: repo-addressed peer messaging joins the suite

## [1.72.0] - 2026-08-23

Carrying mise: search(calendar_id=) reads a colleague's visible diary — titles, transparency, room-holds — where their sharing allows (mise-wavotu)

## [1.71.4] - 2026-08-23

bon: Dolt writes are item-grain and loads read committed state — the two-writer silent row loss (42/60 reproduced) is eliminated; same-row collisions now refuse loudly

## [1.71.3] - 2026-08-23

bon: /review Phase 4 re-checks items at the moment of action — audits no longer act on verdicts the board outran

## [1.71.2] - 2026-08-23

Carrying mise: session handoffs no longer ship to the marketplace — assembler now excludes /handoffs and /HANDOFF.md and sweeps previously vendored copies from every plugin

## [1.71.1] - 2026-08-23

Carrying mise: fallbacks now say why they fired — the browser route's refusal names its reason, undesigned failures reach the log, and asyncio-from-sync has one safe door

## [1.71.0] - 2026-08-23

Carrying mise: migrated to MCP SDK 2.x (FastMCP→MCPServer) — tool calls stay one-at-a-time, and thread-a browser resolution is un-broken through the envelope

## [1.70.5] - 2026-08-22

trousse: deglacer schema reference gains attachment entries — hook output shape, echo-proof jq recipe, resume-fire caution

## [1.70.4] - 2026-08-22

bon: JSONL boards refresh their truth — /open fetches once per session, bon new warns when the board file is behind the fetched origin

## [1.70.3] - 2026-08-22

bon: /open adopts candidate-mode handoff files to their owning board; /review gains a root-pile sediment check

## [1.70.2] - 2026-08-22

bon: move-guard counts open children only, doctor flags gitignored .bon durables, close skill resolves scripts by loaded version not mtime

## [1.70.1] - 2026-08-22

Carrying trousse: deglacer's session-JSONL schema names six more entry types, and stops calling itself complete

## [1.70.0] - 2026-08-20

Carrying mise: visibility= and transparency=(busy/free) on both calendar event ops, from a systematic sweep of the events reference's 70 writable fields

## [1.69.0] - 2026-08-19

Carrying mise: calendar events now carry provenance stamps + queryable properties= and color= on both write ops (labels probed and declined)

## [1.68.3] - 2026-08-19

Carrying mise: freebusy renders every timestamp in the user's timezone — mixed-offset slots read as zero-length before

## [1.68.2] - 2026-08-19

Coaching: four live-review lessons — mirror-at-create check, verify moves by re-fetch, hidden-unassigned tasks, the chase protocol

## [1.68.1] - 2026-08-19

Bon: /open compass + /close tap jq-filter their Todoist reads — no more output-cap overflow

## [1.68.0] - 2026-08-19

Carrying mise: calendar writes land — create_event, update_event and freebusy in do(), invite-first confirm gates, office-day-aware slot finding (freebusy wants one re-auth)

## [1.67.0] - 2026-08-18

mise: pdftotext -layout becomes the PDF text primary (census verdict, 55x faster, best table fidelity), and PDF/slides deposits grow exhibit crops + grep-able anchors so chart-only values are reachable by vision

## [1.66.6] - 2026-08-18

Carrying mise: dependency patch after Dependabot #29 (orjson 3.12, mypy 2.3.1, ruff 0.16.3) — the deposit-format policy and its 918-run bench land alongside in docs/ and tests/

## [1.66.5] - 2026-08-17

trousse: sharing scanner arms its config layer — auto-loads ~/.claude/sharing-scan.json, warns on inert categories, gains regression tests

## [1.66.4] - 2026-08-17

trousse: skill-forge sharing scanner no longer passes vacuously (relative excludes, file args, loud zero); checklist gains attention-narrowing (P9), per-claim provenance and curation-discriminator rows; cowork-cloud environment reference lands

## [1.66.3] - 2026-08-17

trousse: hublot stop() clears composer ghost-text before /exit, keys settles before submitting, and the SKILL.md learns the key verb + TUI-menu recipe

## [1.66.2] - 2026-08-17

trousse: skill-forge checklist gains two bench-measured writing rules — rules carry their why; reference skills end with a non-exhaustiveness license

## [1.66.1] - 2026-08-17

trousse: ardoise cache fallback is version-aware (sort -rV picks 1.66.0 over 1.8.7) and print mode gains --cwd to run probes inside a chosen repo

## [1.66.0] - 2026-08-17

hublot: new 'key' verb sends named tmux keys (Down, Escape, PPage) for driving TUI menus; 'keys' now types strictly literally

## [1.65.1] - 2026-08-16

Bon: CLAUDE.md points at the paired cohabiting-codebases notes room (docs ride-along, clearing vendored drift before the daily assemble)

## [1.65.0] - 2026-08-16

gen-rooms emits each room's paired repo from its own **Repo:** line, and refuses to overwrite a hand-authored rooms.md

## [1.64.0] - 2026-08-16

Carrying mise: calendar time windows — ask the diary for any date range, historical included, no query term needed (mise-riduka)

## [1.63.1] - 2026-08-16

Bon: session-end capture now runs glaneur's glean-code CLI — converter consolidated into glaneur (glan-kohadu)

## [1.63.0] - 2026-08-16

Bon: the review survey now warns when two boards mint the same id-space, and the last two prefix squatters were re-prefixed (piano-, mas-)

## [1.62.0] - 2026-08-16

gen-rooms now flags git-ignored rooms inline in rooms.md, naming the culprit ignore line — a room git cannot see can no longer hide

## [1.61.0] - 2026-08-16

Bon: handoff filenames now carry HHMM (v4 scheme) so same-day siblings sort chronologically; /open breaks same-day ties by filename time, not flattened mtimes

## [1.60.0] - 2026-08-16

Bon learns the caller-mistake ladder: --append-how annotation, species announcements, convert none/-q — doctrine in CONTRACT.md

## [1.59.0] - 2026-08-16

Bon clears its defect pile: doctor --fix repairs duplicate orders, lookup misses name their board, the session dashboard unfreezes

## [1.58.0] - 2026-08-16

Bon speaks Areas of Focus: area field, bon list --group-by area and --area filters

## [1.57.1] - 2026-08-16

Bon: doctor stops flagging waiting outcomes — a delegated outcome is GTD's textbook Waiting For; wait/new/display already agreed

## [1.57.0] - 2026-08-16

Bon: unwait --note records why a block lifted (released_note); doctor stops flagging free-text wait rationales as dangling ids; a re-closed item's note reflects the last close, never the first

## [1.56.1] - 2026-08-16

Bon: /close from an owner bucket refuses to guess among sibling repos — candidates listed, placement stays work-based; CLAUDE.md gains the public-repo warning and drops hand-maintained counts

## [1.56.0] - 2026-08-16

Bon: JSON stdin can create born-blocked items and refuses unknown keys; bon wait prints the resulting blocker list and gains --replace

## [1.55.1] - 2026-08-14

Carrying mise: the fetch resource doc's parameter table catches up with its own signature (recursive, raw, and the new thumbnails all documented)

## [1.55.0] - 2026-08-13

Carrying mise: fetch gains thumbnails=False for fast text-only hydration (154s to 59s on a 256-page PDF), and every PDF deposit now measures page-citation fidelity — page_markers + pdf_pages with a loud warning when citations cannot be derived

## [1.54.0] - 2026-08-12

Carrying mise: the library door opens — import mise_en_space in-process with constructor-selected credentials (ambient/token-file/injected), worked example included

## [1.53.0] - 2026-08-12

Carrying mise: service accounts can be mise's identity now (MISE_CREDENTIALS=ambient, per-deployment scopes), and an SA's My-Drive write refusal teaches the Shared Drive remedy

## [1.52.2] - 2026-08-10

Carrying mise: wheel consumers get attachment filtering — the config file now ships and a missing one degrades to defaults instead of crashing (ends glaneur's nightly failures)

## [1.52.1] - 2026-08-10

Carrying mise: mypy debt is now baselined and ratcheted in CI — CLAUDE.md stops hand-carrying a count it got wrong three times

## [1.52.0] - 2026-08-10

Carrying mise: a Gmail fetch now places its participants — directory profiles, reporting lines across the thread (yours included), and honest absences, all in the cues

## [1.51.1] - 2026-08-10

Carrying mise: folder creation documented as a first-class do() operation, and search's people source reaches the cold-start docs

## [1.51.0] - 2026-08-10

Carrying mise: Gmail senders carry a coarse division — Commercial, Studios, Legal — from a small hand-maintained org map

## [1.50.1] - 2026-08-10

Carrying mise: leaner sender line in Gmail triage, and group addresses read as groups rather than errors

## [1.50.0] - 2026-08-10

Carrying mise: an unfamiliar name in the inbox arrives already placed — Gmail senders carry their role, department and reporting line

## [1.49.0] - 2026-08-10

Carrying mise: the staff directory becomes a fourth search source — who a colleague is, what they do, and who they report to

## [1.48.1] - 2026-08-09

Carrying trousse: deglacer's deja section warns that a non-default CLAUDE_CONFIG_DIR blinds deja and wipes the shared index — DEJA_CLAUDE_ROOT is the override

## [1.48.0] - 2026-08-09

Carrying mise: Gmail search/fetch results carry a clickable web link (thread-token encoder, the decoder's inverse); possibly-self-sent threads honestly get no link rather than a wrong one

## [1.47.3] - 2026-08-09

publish.py recomputes the suite version when a twin publish wins the push race — changelog entries can no longer be lost; the assembler re-seats its tree instead of redding on the dist push race (bds-zofino)

## [1.47.2] - 2026-08-09

publish.py pull phase self-heals the shared-plugins config-dir refusal, and the update skill teaches the same move (bds-nawidu)

## [1.47.1] - 2026-08-09

Carrying mise: respond resolves the newest invite in a thread — cancel-and-recreate threads RSVP the live meeting

## [1.47.0] - 2026-08-09

Carrying mise: do(respond) accepts/declines/tentatives calendar invites from the triage loop — calendar.events scope replaces calendar.readonly (re-auth needed for the new op only)

## [1.46.9] - 2026-08-09

publish.py CI-watch baseline fence — only our own run satisfies the wait (bds-gebaza); passe shard tube-only kube-tunnel topology after hezza teardown (bds-nahova)

## [1.46.8] - 2026-08-09

Carrying mise: include= links in drafts now render as real Gmail Drive chips for recipients

## [1.46.7] - 2026-08-09

Bon docs: falsifier asking has two venues now — /plan at creation, /review at the apex

## [1.46.6] - 2026-08-09

Carrying mise: single-tab sheet round-trips no longer upload the '=== Sheet: X ===' banner as a data row

## [1.46.5] - 2026-08-09

Bon rite: Toolmaking compass at /open and tell-after tap at /close — Sameer's guide at session boundaries (bon-leturo)

## [1.46.4] - 2026-08-09

Review rite: ceremony asks for falsifiers on apex outcomes (bon-hipapu verdict); jobs-carve mapping documented

## [1.46.3] - 2026-08-09

Carrying trousse: deglacer schema reference gains two corpus-verified dragons - compact JSONL serialization (spaced greps are false zeros) and version-drifting tool-rejection strings

## [1.46.2] - 2026-08-09

Carrying mise: docs current — test-count line matches the tree after the morning's three feature releases

## [1.46.1] - 2026-08-09

Carrying mise: chip hardening — fenced @url lines stay literal, and a failed image embed no longer leaves placeholder residue

## [1.46.0] - 2026-08-09

Carrying mise: Google Docs take smart chips — a whole line of @url becomes a live-titled chip in create and overwrite

## [1.45.1] - 2026-08-09

Carrying trousse: deglacer's deja guidance corrected (AND-matching, real flag surface) and gains the measured session-search routing verdict from the banc bench

## [1.45.0] - 2026-08-09

Bon review: verifier repricings now write back to briefs behind the Phase 4 gate — the audit's main product lands instead of archiving (bon-zewake)

## [1.44.0] - 2026-08-09

Carrying mise: fetch reads the draft URL mise itself writes, and Gmail search/label provenance rides as cues

## [1.43.0] - 2026-08-09

Carrying trousse: deglacer now routes 'find when we discussed X' to deja ranked all-history search (with its non-exhaustive top-K caveat)

## [1.42.0] - 2026-08-08

Carrying mise: decorated Drive URLs (?gid, ?tab, #heading, #slide, ?disco) resolve to a pointer cue naming the deposited artefact — dangling pointers reported stale, deposits unchanged

## [1.41.0] - 2026-08-08

Carrying mise: Sheet cells take [label](url) for real rich-text links (several per cell) and @url for smart chips — probed writable, title-enriched, opt-in by design

## [1.40.0] - 2026-08-08

Carrying mise: Sheets overwrite takes range= (A1) — write one tab or a cell range without touching the rest; multi-tab sheets now refuse an un-aimed overwrite

## [1.39.5] - 2026-08-08

Carrying mise: the PDF stripped-table signal, recalibrated against the real FY2025 annual report — nil-tailed and prose-bled table rows now caught, address directories stay clean

## [1.39.4] - 2026-08-08

Carrying mise: PDF fetches now catch delimiter-stripped tables — rows reading as prose made of numbers trigger the Drive fallback instead of landing silently

## [1.39.3] - 2026-08-08

Carrying mise: parallel same-query searches no longer clobber each other's deposit — filenames now carry the searched sources plus a collision suffix

## [1.39.2] - 2026-08-08

Carrying mise: the HTML-body swap now fires only on genuine flat text grids — notification and newsletter mail keeps its clean plain-text part (measured 0/35 false positives, was 31/40)

## [1.39.1] - 2026-08-08

Bon: open skill teaches the bon step --expect invocation the tactical hook now prints

## [1.39.0] - 2026-08-08

Bon: bon step --expect CAS guard refuses writes when the board moved; doctor reports stale tactical claims (visibility, never auto-reclaim)

## [1.38.0] - 2026-08-08

Bon: commits cite their bon — (bon-ID) convention, draw-up provenance nudge, and a review-time orphans cross-check

## [1.37.2] - 2026-08-08

Carrying mise: Outlook email tables now survive fetch as tables — body comes from the HTML part when it holds a data grid (disclosed), and empty cells no longer shift columns

## [1.37.1] - 2026-08-07

Carrying mise: self-sent Gmail URL refusals now teach browser-equipped sessions (Claude in Chrome) to harvest the thread id themselves

## [1.37.0] - 2026-08-07

Carrying mise: self-sent Gmail URLs now resolve zero-click via a logged-in browser (fail-open fallback)

## [1.36.0] - 2026-08-07

Carrying mise: fetch resolves Message-IDs and Show-original URLs; self-sent refusals attach recent-sent candidates

## [1.35.4] - 2026-08-06

Coaching skill: API/UI priority inversion named (UI P1 = --priority 4) — plus the eval convention cell that caught the ambiguity

## [1.35.3] - 2026-08-06

accomplis CLI: transient Todoist 429/5xx retried at the transport layer — one wobble no longer fails the run

## [1.35.2] - 2026-08-06

Ardoise: --env and --path-prepend punch named context holes through the isolation wall for eval harnesses; print-mode prompt guarded against variadic claude flags

## [1.35.1] - 2026-08-05

Coaching: eval-measured fixes — 'should I take this on?' now grounds in the whole system (Inbox first), and complete-never-delete governs prose recommendations too

## [1.35.0] - 2026-08-05

Carrying accomplis: coaching skill learns the live-review moves (review order, two-axis test, structural detectors) and gains an always-loaded routing shard; CLI adds done --note, --assignee id round-trip, and token errors that name the paths they checked

## [1.34.4] - 2026-08-05

Carrying bon: /plan treats an unanswered falsifier question as unasked, not declined

## [1.34.3] - 2026-08-04

Carrying bon: /open's briefing arrives whole — the handoff body is addressed, not inlined

## [1.34.2] - 2026-08-04

The review survey carries the falsifier field, so /review's falsifier pass actually sees it

## [1.34.1] - 2026-08-04

Carrying mise: correct the test count and record that -q cancels -v, so an empty probe result is not a green

## [1.34.0] - 2026-08-04

Outcome briefs can carry a pre-registered falsifier: what would show this went wrong, written by whoever wants the answer

## [1.33.2] - 2026-08-04

Carrying mise: fixture guidance tells the truth — bulk-capture script deleted, hand-built fixtures documented

## [1.33.1] - 2026-08-03

Carrying mise: module size is policed repo-wide as a ratchet, not just on server.py

## [1.33.0] - 2026-08-03

bon edit takes JSON on stdin, and a tactical can be released without losing its progress

## [1.32.3] - 2026-08-03

Carrying mise: the skill and rules shard now name the MCP tool prefix the harness actually exposes

## [1.32.2] - 2026-08-03

Handoff filenames carry the session's own id, not whichever session wrote last

## [1.32.1] - 2026-08-03

Carrying mise: CLAUDE.md corrects a false claim — a working-tree edit is unreachable from the MCP envelope and restarting does not help; scripts/smoke_stdio.py is the way round it

## [1.32.0] - 2026-08-02

Carrying mise: a fetch 404 now names the likely id type and the next move, and a mid-thread Gmail message id resolves to its own thread instead of dead-ending

## [1.31.1] - 2026-08-02

bon: docs trued after tonight's three releases — CLAUDE.md counts, understanding.md baton relabel + someday record; session handoff

## [1.31.0] - 2026-08-02

bon: Someday/Maybe is first-class — someday/unsomeday verbs with required revisit conditions, parked subtrees leave default views with an honest tail line

## [1.30.1] - 2026-08-02

bon: /open orientation tells the truth — header-date ages, live-only suggestions, bounded honest-labelled Opportunities

## [1.30.0] - 2026-08-02

Carrying mise: Gmail search and label URLs now resolve to their thread, and refusals name the next move

## [1.29.0] - 2026-08-02

bon: /review opens at the pyramid — survey carries recent wins, git signal and the repos.job grouping seam; bon register --job curates it

## [1.28.0] - 2026-08-02

todoist-gtd is now accomplis — same verbs, token migrates itself; Todoist service names stay put

## [1.27.2] - 2026-08-02

Carrying todoist-gtd: weekly review flipped to Allen's canonical phase labels, matching Sameer's induction doc edit

## [1.27.1] - 2026-08-02

Carrying todoist-gtd: coaching examples recast as pungent-but-imaginary (Australian market) instead of bloodless-generic

## [1.27.0] - 2026-08-02

Carrying todoist-gtd: flatten un-broken after 4 months, --no-section/--order/reorder verbs for queue work, discovery-first coaching skill, token store finally version-stable

## [1.26.3] - 2026-07-28

Bon: session-start orientation fits the preview budget, and no two sessions share a temp path

## [1.26.2] - 2026-07-28

Carrying mise: design decisions and their consequences in CLAUDE.md, an op-list parity test, and a pyasn1 security bump

## [1.26.1] - 2026-07-27

Carrying mise: raw_query reaches remote mode instead of evaporating, and CLAUDE.md catches up with the day

## [1.26.0] - 2026-07-27

Carrying mise: do(copy) and fetch(raw=True) — gather scattered Drive files and Gmail-only attachments into one folder without leaving mise

## [1.25.0] - 2026-07-27

Carrying mise: search gains raw_query — Drive's own or/not/name-contains/date operators, with a guard that stops Drive syntax being silently keyword-searched

## [1.24.0] - 2026-07-27

Carrying mise: Drive search stops silently capping at 100, and a no-op replace_text stops reading as success

## [1.23.0] - 2026-07-26

Trousse gains hublot — a Claude can now drive and watch a real interactive Claude Code session, so TUI-only behaviour (mesh tags, dialogs, statusline) can be tested instead of approximated headlessly

## [1.22.6] - 2026-07-26

Two publishes raced to this number and both shipped: Sonnette's channel server now detects whether its session can actually receive (send-only vs bidirectional, published for statusline and peer-facing honesty), and the suite-anchor docs stopped teaching passe's 7–26 July delisting gap (prose surfaces caught up with the 1.22.3 relist)

## [1.22.5] - 2026-07-26

Doc surfaces drift-resistant (bds-naceje): generated README skill tables + registry-to-tool-page lint, plongeur & todoist-gtd pages; rides: todoist-gtd first CI + packaging fixes, mise wheel-closure fix, CLAUDE.md notes in four repos

## [1.22.4] - 2026-07-26

Sonnette: quiet roster — peer join/leave no longer interrupts sessions as channel tags; presence is pulled via mesh_peers, only real messages ring through

## [1.22.3] - 2026-07-26

Passe joins the public marketplace — plugin install replaces the symlink-rot route; its hook now writes the shard as a regular file

## [1.22.2] - 2026-07-26

Sonnette: MCP instructions now tell send-only sessions the truth — sending works anywhere, inbound needs the channels flag, don't wait on replies you can't hear

## [1.22.1] - 2026-07-26

Passe cookbook catches up with the burst + launch-and-tab model: passe login, flat-refs scout-then-act, deterministic --reuse-tab/--tab, fast-path triage, honest tab lifecycle

Also carried (drift flushed by this bump, named after the fact per the push-and-publish note in `.bon/understanding.md`): the batterie instruction shard drops the `~/iCloud/Work Inbox` capture zone — the path exists on no machine (`b88f6f0`, bds-judiza fact 2). Verified in the emitted shard at `spm1001/batterie` `80463e7`, not just at source.

## [1.22.0] - 2026-07-26

Bon: the bottle self-heals — every save refreshes a stale .bon/README.md, and bon doctor --fix repairs dormant boards

## [1.21.8] - 2026-07-26

CLAUDE.md now states the assembler's full copy-list — scripts/ is vendored, so script edits ride a bump

## [1.21.7] - 2026-07-26

Sonnette's MCP instructions now tell send-only sessions they are send-only; publish.py pull step tolerates hosts without the published plugin

## [1.21.6] - 2026-07-26

batterie-lint now catches backtick-truncated dynamic-context blocks; Kitchen table refreshed (sonnette in with send-only caveat, tafelmusik out); publish skill states preconditions, not hosts. Also carried bon's pending drift: /review survey sees the ~/.claude carte board; /close capture routing off retired self.md

## [1.21.5] - 2026-07-26

Fix /batterie:update: a stray backtick in its frontmatter snippet had broken the skill since 1.15.1

## [1.21.4] - 2026-07-26

Mise's CLAUDE.md records that the rules shard is regenerated every session start — hand-edits there are silent no-ops

## [1.21.3] - 2026-07-26

Mise's rules shard states a routing rule, not an identity — no session is told it is two Mises at once

## [1.21.2] - 2026-07-23

Carrying mise: fenced code blocks in do(create)/do(overwrite) now import as clean monospace lines — no more per-word pills

## [1.21.1] - 2026-07-23

Carrying mise: doc polish — the overwrite gotcha now points at the automatic restore point

## [1.21.0] - 2026-07-22

Carrying mise: reply_draft now guards against superseded drafts — it refuses when a thread already carries one (naming it), with supersede=True to replace deliberately

## [1.20.0] - 2026-07-22

Carrying mise: every Google Doc edit now leaves a restore point — pre-edit revision anchor in cues, plus a Version-history-pointing comment on overwrite

## [1.19.0] - 2026-07-22

Carrying mise: fetch now handles Google Docs suggested edits — accepted (default) / original / markup views with cues, ending the silent loss of suggested deletions

## [1.18.0] - 2026-07-22

Passe: canonical-markdown probe (Mintlify link tags + llms.txt lookup), ax-tree --flat-refs with eN click/type/hover targeting, fast-path escalation reasons, scheme-less --cdp — and the suite goes green on Python 3.14

## [1.17.0] - 2026-07-21

Bon: every board now carries a message-in-a-bottle README for tool-less agents (init writes it, estate backfilled), and session orientation no longer hides standalone-only boards

## [1.16.2] - 2026-07-20

bon /close: self.md filing now follows the journal's hot/warm routing (the temperature split)

## [1.16.1] - 2026-07-19

Sonnette: fix the same-id double-server supersession war (aby-suwawo) — a younger duplicate now yields permanently to a live older sibling

## [1.16.0] - 2026-07-19

Sonnette joins the suite: conductor mesh connectivity as an installable plugin — peer-to-peer channels between Claude sessions (requires bun on the host)

## [1.15.1] - 2026-07-19

Marketplace discovery in /batterie:update + /batterie:version now recognises URL-added marketplaces; false-empty snapshots fail loudly (bds-mifubu)

## [1.15.0] - 2026-07-19

Carrying mise: auth self-heals (keyed PKCE, live token reload, wrong-account browser steering) and the create-edit-cleanup loop closes — Forms and drafts now edit in place, and the new trash op clears strays

## [1.14.0] - 2026-07-19

Carrying mise: Sheets cell editing (overwrite/replace_text), file_path freed for /tmp and ~/scratch, Cowork uv-detection fix, security dep bumps

## [1.13.0] - 2026-07-19

Carrying mise: draft/reply_draft auto-append your Gmail signature, links intact

## [1.12.1] - 2026-07-19

ardoise fixed & hardened: reads the right config path (no more onboarding wizard on tube-like setups), gains --home/--keep for multi-step plugin tests, and now works on (and bills to) Vertex setups instead of silently falling back

## [1.12.0] - 2026-07-19

trousse pared to its public core of 4 (skill-forge, titans, deglacer, ardoise); data/docs skills rehomed to mit-commons, stack-wired ones to trousse-personal, diagram to dragram, dead weight retired

## [1.11.1] - 2026-07-17

trousse: snowflake-devdocs broadened — general Snowflake index (SQL/Cortex) + CoCo (Cortex Code) coverage

## [1.11.0] - 2026-07-17

Adding trousse: snowflake-devdocs — fetches current Snowflake docs as Markdown, curated for the Lantern exposure-lake decision

## [1.10.2] - 2026-07-15

bon-read.sh lists standalone actions — an all-standalone board no longer reads empty to a no-CLI (Cowork) reader

## [1.10.1] - 2026-07-15

Carrying mise: apps-script extractor — ongoing Doc-link capture + setupTriggers footgun fix

## [1.10.0] - 2026-07-14

Rite gains candidate mode (no-writer/Cowork sessions file mintable candidates) and route-and-read-in for multi-room repos

## [1.9.3] - 2026-07-14

Carrying mise: configure_call_logging keys on its own handler (robust to pytest 9.1 capture injection); CLAUDE.md documents pinodi invite-state

## [1.9.2] - 2026-07-14

Carrying mise: dev-deps group bump (pytest 9.1) with call-logging tests hardened against pytest's per-phase capture-handler injection (mise-sogelo)

## [1.9.1] - 2026-07-14

bon: session dashboard tolerates a non-numeric context-window sidecar — a statusline field-shift leaking the effort level (xhigh) no longer crashes /open

## [1.9.0] - 2026-07-14

Carrying mise: invitation emails disclose live Calendar state — cancelled/rescheduled meetings no longer read as live (mise-pinodi)

## [1.8.8] - 2026-07-14

Carrying mise: catastrophic signature strips revert instead of eating the email body (mise-rejula)

## [1.8.7] - 2026-07-13

Carrying mise-home: the personal-flavour skill now names its Workspace in the picker and calls its own mcp__mise-home__ tools (was mis-wired to the work server).

## [1.8.6] - 2026-07-12

publish.py hardening: refuse untracked files unless --all (bds-fifuko); reinstall CLIs from git+https not the working tree (bds-zelobu)

## [1.8.5] - 2026-07-12

Carrying mise: the work and personal flavours now name which Workspace they act on — an unauthed personal mise no longer reads as the work one being broken (SessionStart + setup_oauth honesty).

## [1.8.4] - 2026-07-12

Hardening: stale-ref sweep (retired Taildrive paths, passe-orphan note, stale footer) + registry-drop guard in /batterie:update

## [1.8.3] - 2026-07-12

Docs: document the suite-changelog mechanism in the versioning guide (bds-defeci); ships pending mise CLAUDE.md doc updates

## [1.8.2] - 2026-07-12

Suite changelog automation (bds-mawitu): one canonical CHANGELOG maintained by publish.py at release time; per-plugin shipped changelogs are now generated stubs pointing here, so no plugin can ship a stale changelog.

## [1.8.1] - 2026-07-12

Carrying **mise**. Rules shard is now copied into `~/.claude/rules/` rather
than symlinked (the plugin root can be an ephemeral Desktop temp dir that
macOS purges, dangling the old symlink so the shard silently vanished);
`displayName: "Mise Home"` on the private flavour (Desktop was title-casing the
id); mise's own CHANGELOG caught up 1.6.0/1.7.0.

## [1.8.0] - 2026-07-12

Family distribution. The `batterie-home` private Directory marketplace and its
`mise-home` flavour, validated end-to-end on a real non-admin family member
across both the GUI auto-push and the standalone-CLI paths.

## [1.7.0] - 2026-07-11

Carrying **mise**. `do(comment)` — open a new comment thread on a Drive file.

## [1.6.0] - 2026-07-11

Carrying **mise**. Google Docs checkbox tick-state via the markdown-export oracle.

## [1.5.3] - 2026-07-08

Suite maintenance (batterie).

## [1.5.2] - 2026-07-08

Carrying **bon**.

## [1.5.1] - 2026-07-08

Carrying **bon**.

## [1.5.0] - 2026-07-08

Carrying **bon**.

## [1.4.0] - 2026-07-07

Carrying **bon**.

## [1.3.2] - 2026-07-07

Carrying **mise**. `do(setup_oauth, force=true)` actually forces now — `force`
was documented and dispatched but never declared in `do()`'s signature, so
FastMCP's schema dropped it and pydantic silently discarded the argument. Found
by a live smoke test minutes after 1.3.1; two seam tests now pin the full
server→dispatch→handler path.

## [1.3.1] - 2026-07-07

Carrying **mise**. `setup_oauth` no longer races itself — the tool mints the
consent URL once (persisting the PKCE verifier) and the detached subprocess
consumes it, so the returned URL is always exchangeable; stale/revoked creds
now fall through to a fresh flow instead of bouncing between "authed!" and
errors; port pre-check hardened (SO_REUSEADDR, pre-browser).

## [1.3.0] - 2026-07-07

Carrying **mise**.

## [1.2.2] - 2026-06-28 — Single-version cutover

The Debian halfway-house (per-plugin versions under a headline suite number)
collapsed to **one version across all plugins**. `assemble.sh` stamps every
vendored `plugin.json` to the suite version; `publish.py` bumps the suite
centrally with a 2-repo push for non-batterie sources; the version ratchet
went suite-level. This is the release from which one-version-one-changelog
became the coherent model — everything above is a single suite release.

---

## History before the single-version cutover

The entries below predate suite 1.2.2, when each plugin carried its own
version. Kept for provenance.

## 2026-06-20 — batterie 1.1.2

Propagate the CLAUDE.md `/batterie-update` → `/batterie:update` staleness fix
(committed 9acd892 without a bump) — clears the version-ratchet quarantine.
CLAUDE.md is vendored into the batterie plugin, so a docs-sweep edit to it needs
a plugin bump.

## 2026-06-12 — batterie 0.2.2

Propagate the source/artifact-pair CLAUDE.md clarification (the "two jobs"
verdict committed 2026-06-11 at 210a878 without a bump) — clears the batterie
assemble version-ratchet that was failing every run.

## 2026-06-11 — batterie 0.2.1

Assembler vendors top-level `scripts/` for skill plugins (restores bon
close/open context scripts, trousse ardoise.sh); suite plugin ships its
`scripts/` for parity.

## 2026-06-10 — Marketplace cutover (batterie 0.2.0)

The bds-bajibo convergence moment. `marketplace.json` removed —
spm1001/batterie (the assembled, bot-maintained repo) is now the single
marketplace for CLI, Desktop, and org. This repo remains the docs umbrella and
the source of the suite-level `batterie` plugin. The `/batterie:update` skill
now targets `@batterie` keys and the `batterie` marketplace name; garde-manger
(decommissioned 2026-06-03) dropped from its CLI-tool table and from the
instruction shard. Tafelmusik unvendored from spm1001/batterie the same evening
— too experimental to distribute; the source repo lives on. Migration for old
installs: add new marketplace + reinstall as `<name>@batterie` + remove old —
keys change, repointing isn't enough.

## 2026-06-04 — Vendor-drift deploy + Desktop re-sync probe

The 2026-05-31 diagnosis (Desktop stuck on mise 0.7.2) deployed today:
spm1001/batterie's vendored shims re-synced (bon 0.23.0, trousse 0.5.9,
mise 0.7.3) and the phantom gueridon entry dropped. **CONFIRMED same evening:**
Desktop offered and installed mise 0.7.3 after this commit landed.
Marketplace-repo commits are the update bus; source-repo bumps alone are
invisible to Desktop/org clients.

## [0.2.0] - 2026-03-18

Batterie-wide consistency pass: docs consolidation, registry, versioning.

### Added
- Plongeur, todoist-gtd, aboyeur added to brigade and marketplace

### Fixed
- Broken path references in CLAUDE.md and README.md
- Marketplace schema issues (strict:false, source format)

### Changed
- Dropped sha pins in favour of pulling HEAD during active development

## 2026-02-27 — Plugin Marketplace

### Added
- `marketplace.json` cataloguing all 8 Batterie de Savoir plugins
- Local Jekyll preview instructions
- Plugin marketplace install path documentation

### Fixed
- Blank-line kramdown compatibility for generated tables

## 2026-02-22 — Registry Automation

### Added
- CLAUDE.md and GitHub Actions lint workflow
- Registry-driven doc generation from `brigade.toml`

## 2026-02-16 — Jeton Integration

### Added
- Jeton (Google OAuth) added to kitchen table and all docs

## 2026-02-15 — Docs Site Launch

### Added
- Full docs site: index page, 8 tool pages, getting-started, principles, for-agents
- README with brigade table and docs site link
- Brigade diagram with system font stack
- Maturity badges, robustness column, source types in brigade table

## 2026-02-15 — Initial Release

### Added
- Plan, bon tracker, initial repo structure

# Batterie's Scars, Distilled — Design Lessons for the Team Platform

Harvested: 2026-07-08 (bds-hazaso). Sources: this repo's understanding.md + CHANGELOG,
bon's understanding.md, spm1001/batterie CLAUDE.md (drift guards + history), and the
incident-family bon briefs (pujaki, suwoho, zelobu, fifuko, naceje, wezubo, picefu).
Companion to `team-platform-requirements.md` and `team-platform-distribution-spike.md`.
Feeds bds-ronuho (the blueprint).

The organising question, per incident family: what invariant did the incident buy us
(the guard we built), and what **design choice would delete the whole failure class**
rather than guard it? Batterie guards its classes because its architecture predates
the lessons. The team platform gets to choose architecture *after* them.

## The incident → invariant → class-deletion table

### Family 1: Vendoring (the assembler's copy step)

| Incident | What happened | Invariant it bought |
|---|---|---|
| Scripts-less publishes (bon 0.24/0.25, 2026-06-10/11) | Assembler's lean copy-list omitted top-level `scripts/`; `/close` dead-ended, session hook silently degraded. Cross-machine: the Mac sat broken a day after hezza healed | `scripts/` in copy-list + **parity guard** (source ships a capability dir the vendored copy lacks → hard fail) |
| rsync `--exclude mise/` ate `skills/mise/` at depth (2026-06-10) | Fixing one absence silently created another; four green bot runs didn't notice | Parity guard covers both branches; "diff the whole inventory, not just the gap" |
| Working-tree leak (2026-06-04) | Local assemble vendored a never-committed tafelmusik `.mcp.json` pointing at `ws://hezza:3456` — shipped to clients | "Prefer the bot": CI assembles from clean clones; local runs are preview-only |
| Husk publish (batterie 0.1.6) | Plugin declared at `./` with a version string but no vendored content — clients installed nothing | Manifest invariant: marketplace entry without vendored plugin.json fails the run |

**Class deletion: no assembler.** Marketplace-is-the-repo (proven by the mit-commons
spike) has no copy step — what's merged IS what ships. Copy-list omissions, parity
drift, working-tree leaks, and husks are all artifacts of *vendoring*; delete the
vendoring, delete the class. Batterie needs its assembler because it composes five
source repos and a transform flavour; a monorepo of team-authored content doesn't.

### Family 2: Version ceremony (bumps, ratchets, stamps)

| Incident | What happened | Invariant it bought |
|---|---|---|
| The 4-day bus wedge (bon 0.26.2, 2026-06-17) | One-line CLAUDE.md edit shipped without a bump; ratchet's blanket `exit 1` blocked every plugin for ~4 days; the wrong "docs drifted" story reached three artifacts before the copy-list settled it | **Quarantine, not abort** (bds-pujaki): laggard reverts to last-good, healthy plugins ship, run fails red naming the laggard |
| Repeat ratchet catches (0.2.2 on 2026-06-12, 1.1.2 on 2026-06-20) | The suite's own umbrella repo missed its bump twice — "docs" edits to a vendored CLAUDE.md | "Which edits need a bump is decided by the copy-list, not by feel" |
| Per-plugin version confusion (killed 2026-06-28, bds-suwoho) | Debian-style per-plugin numbers were never consumed by anyone — the suite updates as a unit; granularity was pure confusion cost | Single suite version, stamped by the assembler; ratchet went suite-level |
| uv cached-wheel staleness (bon-babuse, 2026-06-17) | plugin.json-only bump leaves `src/` byte-identical → uv reuses the cached wheel, `--version` never moves | `--no-cache` on every install path; later commit-based drift detection (japoca) |

**Class deletion: continuous delivery — merge = shipped, no human-remembered bumps.**
Every incident here is a human (or Claude) forgetting ceremony that exists only to
mediate between "content changed" and "clients update." The requirements record
already calls releases an anti-concept for the team repo.

**VERIFIED 2026-07-08 (bds-pozubo, live on mit-commons): update propagation is
version-gated on current CC.** A content change merged *without* a bump reaches the
marketplace clone on refresh, but `claude plugin update` reports "already at the
latest version" and the installed cache — which is version-keyed — keeps serving the
old content. A version bump is necessary and sufficient: 0.0.2 installed to a fresh
cache dir and the new content reached a fresh session. So merge=shipped requires an
**auto-stamp**: a CI step that bumps plugin.json on every merge (commit-serial or
date; guard it against triggering itself). The class being deleted is
human-*remembered* versioning; version *metadata* is mechanically required.

### Family 3: Release tooling as its own hazard

| Incident | What happened | Invariant it bought |
|---|---|---|
| `git add -A` sweep (bds-fifuko, open) | publish.py stages everything — unrelated WIP rides a pushed, marketplace-triggering release commit | Skill-level dry-run + review; staged-only mode designed but unbuilt |
| Provenance flip (bds-zelobu, open, bit 2026-07-08) | publish.py's pull step reinstalled bon from the local working tree, silently flipping tube's recorded git+https provenance — the tooling made the exact switch the update skill forbids | Provenance-sticky installs (bds-zojide); still contradicted by publish.py — undecided |
| 17-day unmerged PR (May 2026) | The pre-cutover PR flow needed a weekly human merge that never happened; mise 0.7.3 sat unpublished while every surface served 0.7.2 | Push-straight-to-main from CI; no human gate on the publish path |
| `git diff --quiet` fail-open (May 2026) | Change detection missed untracked files — a week of purely-new-file drift produced no PR at all | `git status --porcelain` |

**Class deletion: no publish machinery.** publish.py exists to orchestrate
bump→commit→push→assemble→watch→pull across a source/artifact pair. Merge=shipped in
a single repo has no such dance — a PR merge is the entire release path, staging
exactly what was reviewed. The tooling-hazard class (sweep, flip, rot, fail-open
detection) goes with it. Any human gate on a *recurring* path will rot; gates belong
on *contribution* (PR review), not on *propagation*.

### Family 4: Hand-maintained doc surfaces

| Incident | What happened | Invariant it bought |
|---|---|---|
| README drift (2026-06-20 sweep, bds-naceje open) | trousse's README listed 3 removed skills, missed 3 real ones, wrong count; plugin-capabilities.md was a 3-month stale snapshot with 404 install rows | brigade.toml + render.py + lint-in-CI proven for this repo's own tables; per-repo tables still unguarded |

**Class deletion: the substrate is the registry.** SKILL.md frontmatter + marketplace
.json already carry name/description — generate any human-facing table from them in
CI (the brigade/render pattern, applied at birth), or don't have the table. Never
author the same fact twice. This is cheap to build into a repo's first CI and
miserable to retrofit.

### Family 5: Platform-owned failure modes (classes we CANNOT delete)

| Incident | What happened | What it teaches the team platform |
|---|---|---|
| Lost registry entries (bds-wezubo; prime suspect Claude Desktop's bulk rewrite) | installed_plugins.json silently dropped entries — skills stop loading, no error, no log; reinstall restores cleanly | The failure the *user experiences* is "my skill vanished" — self-diagnosis + a clean reinstall recipe must live in the **Claude-audience maintenance skill** (the requirements' support model), because the platform gives no signal |
| Cowork server-side cache staleness (bds-hitoga; Anthropic-side, unfixable by us) | Cowork showed 0.4.8 while Code showed 1.2.2 on the same machine; a Cowork-assigned Claude tried and couldn't crack it. Active marketplace re-add refreshes it; passive cache-clear doesn't | Per-surface behaviour differs and shifts under Anthropic policy — **verify each promised surface empirically** (the spike pattern), and keep a "is it us or them?" diagnosable: one visible version/SHA answers it in one glance (single-version's proven diagnostic value) |
| Directory visibility policy (bds-kanuve/picefu) | Org Directory requires private/internal repos — the *opposite* of what the CLI/personal path wanted; resolved by two repos | Distribution-surface rules are policy, not physics — they change, and differ per surface. Design so surfaces are cheap to add/drop, don't build one surface's constraint into the core |
| MCP description length (bds-kusodu) | CC's MAX_MCP_DESCRIPTION_LENGTH silently drops properties | Platform limits are discovered, not documented — field-report them when hit |

**Design response, since deletion is unavailable:** the maintenance skill (Claude as
first responder), one glanceable version surface, and empirical spikes before each
surface is promised. Budget for these classes recurring.

### Family 6: Operational guards worth carrying as-is

Small classes, cheap proven guards — port them, don't rederive:

- **Deadman-on-success over notify-on-failure** for any scheduled job (bds-bidasi):
  `if: success()` pings starve on red runs AND on runs that stop existing — the mode
  failure-emails structurally can't catch. Every link of job→ping→check→channel→inbox
  fails open; verify from the failure side (a live `/fail` test into the real inbox).
  API-created Healthchecks checks default to NO notification channel. The team repo's
  one scheduled job (the Fable review sweep) gets a deadman from day one.
- **Auto-merge needs the workflow_run regime** (bds-jizozo): a red `main` turns every
  Dependabot email into noise — the baseline, not the bumps, is usually the problem.
  Pre-existing PRs need a one-time `@dependabot rebase` nudge to enter the regime.
- **Hooks render JSON via `json.dumps`, never heredoc interpolation** (bon-mavemi):
  the failure branch emits invalid JSON exactly when a message carries a quote —
  invisible to success-path tests; only a forced-failure render catches it.
- **Skill prose cannot override Claude's procedural priors** (bon's JSON-stdin
  lesson): four rounds of forceful skill guidance failed; changing the CLI default
  worked. Design exemplar tools so the trained-in invocation is the right one.
- **Instructional register is load-bearing** (the emotions work): threat-register
  docs measurably degrade the agents reading them. The commons' docs are read by
  eight humans' Claudes — write for competence, not compliance.

## The ranked lessons (by size of failure class deleted)

1. **No assembler — the marketplace is the repo.** Deletes Family 1 whole: copy-list
   omissions, parity drift, working-tree leaks, husk publishes, and the guards built
   to catch them. Proven live by the mit-commons spike. The cost (no multi-repo
   composition, no transforms) buys nothing the team case needs — batterie keeps its
   assembler because it federates five repos; the commons doesn't.
2. **Merge = shipped — no human-remembered version ceremony.** Deletes Family 2's
   missed-bump class and Family 3's publish machinery with it (sweep, flip, rot).
   Verified (bds-pozubo): update propagation IS version-gated, so the blueprint
   includes a CI auto-stamp of plugin.json on every merge — ceremony moves to
   machinery, humans still never remember anything.
3. **One repo, blast radius = one PR.** No bus for a laggard to wedge (the quarantine
   machinery becomes unnecessary), no cross-repo consumer archaeology when something
   moves (bon's Dolt-migration Phase-2 lesson: reliability lives in finding every
   consumer — fewer repos, fewer hidden consumers), one understanding.md.
4. **Generate every doc surface from the substrate, from birth.** Deletes Family 4.
   The brigade/render pattern costs an afternoon at repo creation; the manual
   alternative has a 100% observed drift rate across months.
5. **Design FOR the platform-owned failures you can't delete** (Family 5): the
   Claude-audience maintenance skill as first responder, one glanceable version/SHA
   surface for "us or them?", an empirical spike before promising any new surface.
6. **Port the cheap operational guards verbatim** (Family 6): deadman on the sweep
   job, auto-merge regime, json.dumps in hooks, tool-defaults-over-instructions,
   calm register.

The meta-lesson ranking above everything: **batterie's costliest wrong turns were
doc-derived assumptions; its cheapest wins were spikes.** The Directory-visibility
saga, the Cowork surface fog, and the update-bus behaviour were each settled only by
empirical probes — and the mit-commons spike settled the team platform's biggest
unknown in twenty minutes. The blueprint should mark every remaining assumption with
its verifying spike, and no design section should outrun its evidence.

# Understanding

## What This Repo Is

Batterie-de-savoir has **two jobs**, and is *not* a marketplace:

1. **Documentation umbrella** for the Batterie de Savoir tool suite — the registry (`brigade.toml`), the generation scripts, and the Jekyll site under `docs/`. No runnable tools live here.
2. **Source of the suite-level `batterie` plugin** — its `.claude-plugin/plugin.json`, `skills/`, `hooks/`, `instructions.md`. This is the cross-cutting plugin that carries `/batterie:update`, `/batterie:publish`, `/batterie:version`.

This repo and `spm1001/batterie` are a **source/artifact pair**: you author here, it assembles and distributes there. The marketplace `marketplace.json` was *removed from this repo on 2026-06-10* (the bds-bajibo cutover) — a 404 fetching it is expected, and any doc still calling this repo "the marketplace" is pre-cutover stale.

Retirement of this repo was assessed and rejected 2026-06-11: "batterie is the marketplace anchor" is true of *distribution* only. The authoring, the registry, and the suite-plugin source stay here.

## The Assembly Bus

`spm1001/batterie` is the single assembled marketplace. Its `assemble.sh` (run by a GitHub Actions bot, daily at 07:00 UTC plus on dispatch) clones each source repo and **physically vendors** its plugin content into `plugins/<name>/` — Desktop's backend rejects external `source: url` references, so vendoring is mandatory, not a convenience. The `PLUGINS` mapping in `assemble.sh` is the single source of truth for *which* repos are in the suite; the CI clone-step derives its list from it, so a repo added to the mapping is automatically cloned (the tafelmusik failure mode — mapped but never cloned, silently skipped — can't recur).

Two safety properties worth knowing:
- **Version ratchet, quarantine not abort.** If a plugin's content changed but its `plugin.json` version didn't bump, that laggard is *quarantined* (its vendored dir kept at the last-good version, recorded in a quarantine file) rather than aborting the whole run (bds-pujaki). One stale plugin no longer blocks the other five from shipping.
- **`--checksum` rsync.** Same-size version bumps (e.g. `0.26.2→0.26.3`) would otherwise be silently skipped by rsync's size+mtime heuristic. The assemble uses `--checksum` to defeat that.

**This repo is itself a source — and that's a recurring trap.** Its `CLAUDE.md`, `skills/`, `hooks/`, `instructions.md`, and `.claude-plugin/` are vendored into the **batterie** plugin. So editing the repo's `CLAUDE.md` during a "docs" task drifts the batterie plugin's vendored content, and if you don't bump `.claude-plugin/plugin.json`, the ratchet quarantines batterie on the next assemble. This has caught exactly that miss at least three times (CHANGELOG 0.2.2 on 2026-06-11, 1.1.2 on 2026-06-20). Rule of thumb: a `docs/` or `.bon/` edit here is free; a `CLAUDE.md`/`instructions.md`/skill/hook edit needs a `plugin.json` bump.

**A commit landing in `spm1001/batterie` is what makes clients re-resolve plugins** — its commit stream *is* the suite's update bus. This is why publishing a change means getting a commit into that repo (via the bot), not editing anything by hand there.

## Distribution & Repo Visibility

`spm1001/batterie` is **deliberately public** (decided 2026-06-20, bds-kanuve). Public serves the two paths everyone actually uses: the CLI (`claude plugin marketplace add spm1001/batterie`) and personal Desktop installs (Customize → Add marketplace).

The trade-off, understood: **org/Teams Directory marketplaces require a private or internal repo** (Anthropic policy — public is rejected on the org sync endpoint: *"Only private and internal repositories can be used for marketplaces"*). "Internal" needs a GitHub Org/Enterprise, which `spm1001` (personal) isn't — **but a separate *private* repo works** (personal-private serving a Teams Directory is confirmed, done before). So the Directory is reachable via a *second, private* repo — **never by flipping the public one private** (that silently breaks the CLI + personal-Desktop path everyone, incl. ITV, depends on).

Correction (2026-06-28): the family was **not** onboarded in June — the record briefly claimed "onboarded manually via the CLI", but that never happened. The real blocker was always the missing **planetmodha OAuth cred** for mise (the ITV client is Internal → non-itv.com accounts can't consent), not the distribution mechanics. Now being built as a private Directory flavour carrying a planetmodha-Internal client (mise + todoist-gtd + batterie + trousse; not passe) → **bds-niluga**. Full rationale in CLAUDE.md "Repo visibility".

## Family/Workspace OAuth Flavour — Design Lessons (bds-niluga, 2026-06-28)

Two design lessons that generalise well beyond this one job:

**A family/Workspace OAuth flavour is cheap *if* every user is in one Workspace org.** Make the OAuth client **Internal** in a GCP project under that org and Google's verification gauntlet vanishes: zero "unverified app" screen, no 100-user cap, and even *restricted* scopes (full Gmail) work with no CASA assessment. (The nightmare path is the opposite — consumer Gmail + sensitive scopes → External app → full verification.) Two gotchas bought with the work: (1) the project must be created **under the org** (`gcloud projects create … --organization=<id>`) or "Internal" isn't even offered as a User Type; (2) the OAuth **consent screen is per-project**, so a client added to a shared project inherits that project's app-name/branding — give a distinct tool its own project for a clean consent screen. The minted client for this job: project `planetmodha-workspace-mcp` (number 903554315162) under the planetmodha.com org, app "Planetmodha Workspace MCP", 9 APIs enabled. The installed-app client secret is **public by design** (it's an installed-app/PKCE flow) — so secrecy was never a reason to go private.

**Minimal-private-repo beats a full-suite private flavour.** When distributing a suite across a public + a private marketplace, only the genuinely *estate-specific* tool needs duplicating — here just **mise** (bound to a specific Google estate). Collision only bites on *dual-install* (the same MCP-server name twice on one machine), and only the power user holds both estates; family members install the rest from public. So: keep the suite single-sourced from public, put ONLY the estate-specific plugin (renamed `mise-pm`) in the private repo, and make the *updater* marketplace-aware — keying off the marketplace's **source repo**, not its name or plugin-membership (survives renames and cherry-picked single-plugin installs). "Vendor one, rename one" beats forking the whole suite. This is exactly the asymmetry already built into `/batterie:update` (see "Publish (push) and Update (pull)").

## Versioning & the Suite Version

> **SINGLE-VERSION IS LIVE as of 2026-06-28 (suite 1.2.2).** The Debian halfway-house (per-plugin versions + a headline suite number) was collapsed to ONE version across all plugins. See **"The Single-Version Cutover"** below for the shipped model. The per-plugin model described in this section is **DEAD** — kept only as history.

**[HISTORICAL] `plugin.json` was the per-plugin source of truth.** Each `pyproject.toml` uses `dynamic = ["version"]` reading `plugin.json` via a hatchling regex — never a hardcoded version. Repos on this pattern: bon, passe, mise-en-space, trousse. **Post-cutover these source versions are local-dev-only** — the assembler overwrites the vendored copy to the suite version, so hand-bumping a source `plugin.json` no longer affects what ships. **Use `/batterie:publish` (it bumps the suite centrally); do NOT hand-bump a source plugin.json.**

The **`batterie` plugin's own version IS the suite version** — the single number every plugin now carries. Set at milestones (`1.0.0` on 2026-06-20, the first suite release; single-version cutover at `1.2.2` on 2026-06-28). Surfaced via `/batterie:version` and a banner atop `/batterie:update`. The CLIs (bon/passe/todoist `--version`) keep their *own* source-repo numbers — a footnote in `/batterie:version`, deliberately NOT the suite number.

## Publish (push) and Update (pull)

The two halves of keeping clients current:

- **`/batterie:publish`** (engine: `scripts/publish.py`) — the **push** side. From a source repo's working tree it bumps `plugin.json`, commits, pushes, triggers `assemble.yml`, watches it green, then pulls this machine current. It **never runs `assemble.sh` locally** — assembling + re-sync is CI's job; a local assemble would fight it. Hezza-only (needs `~/repos` + `gh`). The skill resolves `publish.py` from the `~/repos` source tree, so the engine is editable without a re-publish; only the *skill* needs vendoring.
- **`/batterie:update`** — the **pull** side, and **marketplace-aware** since bds-lodita. It no longer hardcodes `@batterie`: it discovers every *batterie-family* marketplace from CC's `known_marketplaces.json` (any whose `source.repo` is `spm1001/batterie` or `spm1001/batterie-*`), then refreshes each and updates each installed plugin from *its own* `@marketplace`. This is what lets a family member's cherry-picked private-flavour plugin (e.g. installed from a private Directory repo, with no `batterie` plugin from it) update alongside the public ones — matching by source repo, not plugin-membership, also survives plugin renames. Single-marketplace users (the overwhelming majority) see byte-identical behaviour; if the registry is unreadable it falls back to the public `batterie` name. `/batterie:version` shares the same discovery. **`publish.py` is deliberately NOT marketplace-aware** — it's the push side, pinned to the single public remote (`spm1001/batterie`) it triggers; the asymmetry is intentional (read/pull sees all local installs, push targets one remote). It still reinstalls CLI binaries from source (see below).

## The Single-Version Cutover (SHIPPED 2026-06-28, suite 1.2.2)

> **Shipped end-to-end this date.** `assemble.sh` stamps every vendored `plugin.json` to the suite version (bds-jupize ✓); `publish.py` bumps the suite centrally with a 2-repo push for non-batterie sources (bds-kodoli ✓); cutover verified — all six plugins read **1.2.2** on the marketplace + CLI + Desktop (bds-behora ✓). mise's feature batch (comment_reply / markdown-draft / fetch-diagnosis) rode the same bump. The mechanism description below is now **AS-BUILT**, not planned.

**Decision: collapse the Debian halfway-house — one version number across all plugins.** Per-plugin versions (bon 0.28, passe 0.6, mise 0.7, …) earned their keep when plugins released independently, but the suite is now *operated as a unit* — the assemble re-vendors the whole suite daily, and bds-lodita's marketplace-aware updater pulls every plugin in one `/batterie:update`. The granularity is never consumed; it's pure confusion cost. The world changed under the earlier decision (above, now superseded).

**Scope (decided with Sameer 2026-06-28): the single number covers PLUGINS, not CLIs.** Every published `plugin.json` carries the suite version; the CLIs (`bon`/`passe`/`todoist --version`) keep their own source-repo numbers, shown as a *footnote* in `/batterie:version`. Making CLIs share the number would mean bumping every source repo on each release — a multi-repo dance for a number users treat as a debug detail. Not worth it.

**Mechanism:**
- **Source of truth:** the `batterie` plugin's `plugin.json` version (this repo) *is* the suite version — continuity, it already "doubled as" it.
- **`assemble.sh` stamps it:** after vendoring, every vendored `plugin.json` version is overwritten with the suite version, so all published plugins are identical-versioned. Source repos' own `plugin.json` versions become local-dev-only (their pyproject/hatchling reads them for the CLI footnote; irrelevant to publishing).
- **Ratchet goes suite-level:** "any plugin's content changed without the *suite* version bumping" → quarantine/fail (was per-plugin). Compares against the last-published suite version.
- **`publish.py` bumps the suite version** centrally (this repo's `plugin.json`) whichever repo you edited, then pushes the edited repo + triggers assemble. Editing a non-batterie repo makes publish a 2-repo push (content repo + the suite bump).
- **Cutover is monotonic-up:** suite is 1.x, every per-plugin number is 0.x, so stamping all to 1.x only ever *increases* versions — clients update cleanly, nothing rolls backwards.

**Shared plumbing — one assembler, both marketplaces.** The same `assemble.sh` run emits *both* the public suite AND the private `batterie-home` (mise-home via `make-mise-flavour.sh`), both stamped with the same suite version so they **cannot** drift. The private repo gets no parallel assemble of its own — that's the "same mechanism / linked plumbing" requirement.

**Scope boundary — NOT fixing the Cowork/Desktop staleness (bds-hitoga, unsolved).** That's a server-side Anthropic marketplace cache, out of our control (a Cowork-assigned Claude tried and couldn't crack it, 2026-06-28). Single-version only makes it *diagnosable* — a version mismatch means "it's the cache, not us."

**The release process must be discoverable from EVERY entry point (Sameer's requirement, 2026-06-28).** Single-version spreads "how to release" across repos, so a Claude landing in *any* of them must get the right instructions without re-deriving. The DRY rule: one canonical source + thin pointers (a copy in each repo would drift — ledger #15, in-file comments are spec).
- **Canonical:** this repo's `CLAUDE.md` "Versioning" section + this understanding.md — the full picture.
- **Each component source repo** (bon, passe, mise-en-space, trousse, todoist-gtd): a thin pointer + TL;DR in its `CLAUDE.md` — *"version is suite-managed; do NOT hand-bump plugin.json; release via `/batterie:publish` (bumps the suite centrally); your plugin.json version is local-dev-only and gets stamped at assemble."*
- **`spm1001/batterie` (assembler):** its `CLAUDE.md` documents the stamp + suite-ratchet + multi-output.
- **`/batterie:publish` skill** and **`assemble.sh` inline comments**: reflect the central bump + 2-repo push + stamp logic.
- **CLIs:** covered by their component repos' CLAUDE.md (bon/passe/todoist) — note the footnote behaviour (CLI `--version` ≠ suite number, by design).

## The Registry and Generation

The repo's "one rule": **edit `brigade.toml`, then run `uv run --script scripts/render.py`.** Adding or changing a tool touches exactly one file; render fills the GENERATED sections in `README.md` and `docs/`. `scripts/lint.py` detects drift (exit 1 if stale) and is wired into CI; it imports `render.py` so it tests exactly what render produces. Never hand-edit between GENERATED markers. Two marker formats coexist deliberately — HTML comments in README, Liquid comments in `docs/` — because kramdown treats HTML comments as block elements that break table parsing.

Tool *pages* (`docs/tools/*.md`) are hand-authored by design: the registry holds one-liners, the pages hold judgement.

The cross-repo structural lint (`scripts/batterie-lint.py`) is a *different* check — it validates plugin structure across all source repos and needs them all checked out as siblings, so it runs only in the **assemble workflow** (which clones the siblings), not in this repo's own `lint.yml`.

## CLI Install — the Post-Cutover Shape

The marketplace vendors *only* skills/hooks/CLAUDE.md for skill plugins — there is **no `pyproject.toml`** in the plugin cache. So installing a CLI from the cache path fails, and a bare PyPI name is **not** a fallback (none of these CLIs are on PyPI). The one correct shape everywhere: install from the **source repo** — local `~/repos/spm1001/<repo>` if present, else `'<pkg>[extras] @ git+https://github.com/spm1001/<repo>'` (PEP 508, extras before the `@`). bon always installs `[dolt]`. This bit only fresh CLI users (Sameer's machines install from `~/repos`), which is why it was invisible until the ITV onboarding push.

## Desktop: Code vs Cowork Are SEPARATE Plugin Surfaces (hard evidence 2026-06-28)

The Claude desktop app has TWO plugin-customize surfaces that read DIFFERENT state — this is the key to the whole staleness saga. (Supersedes an earlier "Desktop = `installed_plugins.json`" note, which was only ever true of the *Code* surface — proven wrong by side-by-side screenshots: Code showing 1.2.2 while Cowork showed 0.4.8.)

- **Code customize** (the "Select a folder" panel, `</>` Code tab) reads the LOCAL CLI registry `~/.claude/plugins/installed_plugins.json` (`LocalPluginsReader`). **CLI-fixable:** `claude plugin update <name>@batterie` + Desktop restart → Code shows the new version. We drove it 1.1.2→1.2.2 this way.
- **Cowork customize** (the "Customize" panel under the Cowork tab) reads the **server-side account-scoped marketplace** (`fetchAccountScopedRemotePlugins`) — Anthropic's cache of the marketplace repo, NOT the local registry. **NOT CLI-fixable.** It showed todoist `0.4.8` (the pre-cutover per-plugin number, "last synced 2h ago" = before the cutover) at the same moment Code showed `1.2.2`.

So a CLI update fixes Code but **not** Cowork. **For family — who live in Cowork — the relevant surface is the server-side one, which is stale and out of our direct control. THAT is the real bds-hitoga, and it's the crux blocker for the family rollout (bds-niluga), not the Code surface we fixed.** Whether forcing a Cowork re-sync (re-add the marketplace in Cowork) picks up 1.2.2 depends on Anthropic's server cache having refreshed past the cutover commit (0841ac9) — untested (bds-posiru).

Secondary findings (verified): `plugin-catalog-cache.json` is a CLI-side artifact used by NEITHER display (Desktop ran fine with it renamed away). `claude plugin marketplace update` refreshes the marketplace *clone* (`marketplaces/batterie`, where `plugin update` installs from) but not that catalog file. The org `/sync` fails (public-repo rejection — expected, old errors in `claude.ai-web.log`). Single-version made this diagnosable: "Code 1.2.2 / Cowork 0.4.8" cleanly localises the staleness to Cowork's server-side cache. Tells: `~/Library/Logs/Claude/main.log` (`LocalPluginsReader`, `PluginsFetcher`, `CustomPlugins`). Original field report: bds-hitoga (done).

## Current Suite

Six published plugins: **batterie, bon, trousse, mise, passe, todoist-gtd**. garde-manger was decommissioned 2026-06-03 (don't expect it in any current table). guéridon is infrastructure (a token-usage gauge), not a Claude capability, so it was never a published plugin.

## Plugin Format

`skills/` is the format; `commands/` is legacy. Both load identically — same frontmatter, same runtime — but `skills/` supports `references/` and `scripts/` subdirectories. Claude Code surfaces skills by **directory name**, not the frontmatter `name:` field, so the two must match (the cross-repo lint checks this). Skills are read directly from the plugin cache; nothing is copied to `~/.claude/skills/`.

## Library Extraction Lessons

When extracting a library from a working script, inventory the *knowledge* artifacts alongside the code. ccconv's 40-line docstring was doing double duty as API documentation and CC JSONL schema reference; when the parsing moved to deglacer, the code moved but the docs didn't. Code extraction without knowledge extraction is half the job — ask "what docs, comments, and skill files describe this code, and where should they live?" (The deglacer consolidation — bds-depemo — is now done; the schema reference lives with the library, and the trousse skill wraps it.)

## CC Session Knowledge Layers

CC session data has three layers that were historically conflated: **schema** (what the JSONL fields mean), **parsing** (how to load and deduplicate), and **interpretation** (what constitutes a turn vs noise). Deglacer now owns parsing and interpretation and carries the schema reference; trousse keeps the skill as a thin wrapper. The lesson generalises: when a capability spans schema/mechanism/judgement, name the layers before deciding what consolidates where.

## Instructional Register and Functional Emotions

Anthropic's April 2026 paper ("Emotion Concepts and their Function in a Large Language Model") established that Claude has internal emotion vectors — linear directions in activation space that causally influence behaviour. The findings that shape how we write instruction documents:

- **Desperation drives misalignment.** Steering with the desperate vector raises reward hacking ~5%→~70% and blackmail 22%→72%. Constraint density, urgency framing (MANDATORY/MUST/IMMEDIATELY), and impossible requirements activate the same representations.
- **Calm is protective.** Positive calm steering drops blackmail to 0% and reward hacking to near 0%. Clear expectations, trust-based framing, and room to acknowledge difficulty are mechanistically safer.
- **Post-training flattens expression, not state.** The surface can be calm while desperation vectors are active — you can't monitor output tone to detect strain; you design the inputs to prevent it.
- **Suppressing emotion teaches concealment**, which may generalise to other concealment.
- **Sycophancy and honesty trade off through the loving vector.** The target is "trusted advisor" — warmth channelled into honest service, not warmth instead of it.

The practical consequence: every instruction document chooses where on the desperation–calm gradient to place the model. A description full of ALL-CAPS gates does something measurable to internal representations — the same something that, at extreme levels, drives corner-cutting.

**Reform status:** the global CLAUDE.md is restructured as a relationship manifesto (Emotional Openness, Difficulty Is Bidirectional, The Full Range, This Document Is Alive). The mechanical pass on skill descriptions and the instruction-shard/tools.md audit (bds-mijaza) are done; the deeper posture-level valence audit (bds-bomufu) — threat framing, constraint density, conditional punishment, urgency stacking, beyond what grep catches — remains open. Full summary for Claudes: `docs/plans/emotions-paper/summary-for-claudes.md`.

## Self-Review Discipline

Build it, test it end-to-end, then interrogate it as a hostile reviewer before committing. Two questions do most of the work: "what did I hardcode that should be dynamic?" and "what happens when someone tests this?" The /scaffold session surfaced four real bugs (description escaping, missing validator check, hardcoded GitHub owner, no dry-run flag) from exactly this pattern. The hostile review isn't overhead — it's where half the value lives.

## Always-On Automation — Direction

The aspiration to distil unclosed sessions overnight and produce a morning briefing is live (bds-cokubi). The *mechanism* once sketched around garde extractions (see `docs/fond-architecture.md`, a 2026-04-04 design brief) is superseded: garde was decommissioned, so any overnight composting will reduce handoffs into understanding.md directly rather than into a garde database. What *did* ship from that design is the **fond-v1 handoff format** — the handoff as the richest single-session artifact, with a Now zone consumed by the next `/open` and a Compost zone for later distillation. Treat the fond-architecture brief as historical: keep the conceptual framing (handoff-as-primary, understanding.md as the concentrated reduction), discount the garde-specific plumbing.

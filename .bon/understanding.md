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

## Versioning & the Suite Version

**`plugin.json` is the single source of truth for version numbers.** Each `pyproject.toml` uses `dynamic = ["version"]` reading `plugin.json` via a hatchling regex — never a hardcoded version, so no dual-maintenance drift. Repos on this pattern: bon, passe, mise-en-space, trousse. To bump, edit the `"version"` field in `.claude-plugin/plugin.json` only.

The **`batterie` plugin's own version doubles as the human-facing suite version** (the Debian model: one headline number atop independent per-plugin versions). Per-plugin versions stay separate so each plugin's "update available" signal fires only when *that* plugin actually changes. Set the suite number at milestones — it reached `1.0.0` on 2026-06-20, the first real suite release. Surfaced via `/batterie:version` (the canonical "what am I on?", since Desktop's view can be unreliable) and a banner atop `/batterie:update`.

## Publish (push) and Update (pull)

The two halves of keeping clients current:

- **`/batterie:publish`** (engine: `scripts/publish.py`) — the **push** side. From a source repo's working tree it bumps `plugin.json`, commits, pushes, triggers `assemble.yml`, watches it green, then pulls this machine current. It **never runs `assemble.sh` locally** — assembling + re-sync is CI's job; a local assemble would fight it. Hezza-only (needs `~/repos` + `gh`). The skill resolves `publish.py` from the `~/repos` source tree, so the engine is editable without a re-publish; only the *skill* needs vendoring.
- **`/batterie:update`** — the **pull** side. Targets `@batterie` plugin keys and the `batterie` marketplace name. It refreshes the marketplace index first (`claude plugin marketplace update batterie`) — without that, `claude plugin update` compares against a stale cache and updates look current when they aren't. It also reinstalls CLI binaries from source (see below).

## The Registry and Generation

The repo's "one rule": **edit `brigade.toml`, then run `uv run --script scripts/render.py`.** Adding or changing a tool touches exactly one file; render fills the GENERATED sections in `README.md` and `docs/`. `scripts/lint.py` detects drift (exit 1 if stale) and is wired into CI; it imports `render.py` so it tests exactly what render produces. Never hand-edit between GENERATED markers. Two marker formats coexist deliberately — HTML comments in README, Liquid comments in `docs/` — because kramdown treats HTML comments as block elements that break table parsing.

Tool *pages* (`docs/tools/*.md`) are hand-authored by design: the registry holds one-liners, the pages hold judgement.

The cross-repo structural lint (`scripts/batterie-lint.py`) is a *different* check — it validates plugin structure across all source repos and needs them all checked out as siblings, so it runs only in the **assemble workflow** (which clones the siblings), not in this repo's own `lint.yml`.

## CLI Install — the Post-Cutover Shape

The marketplace vendors *only* skills/hooks/CLAUDE.md for skill plugins — there is **no `pyproject.toml`** in the plugin cache. So installing a CLI from the cache path fails, and a bare PyPI name is **not** a fallback (none of these CLIs are on PyPI). The one correct shape everywhere: install from the **source repo** — local `~/repos/spm1001/<repo>` if present, else `'<pkg>[extras] @ git+https://github.com/spm1001/<repo>'` (PEP 508, extras before the `@`). bon always installs `[dolt]`. This bit only fresh CLI users (Sameer's machines install from `~/repos`), which is why it was invisible until the ITV onboarding push.

## Desktop vs CLI Are Separate Codepaths

Claude Desktop loads plugins from Anthropic's **server-side** marketplace, not the local `~/.claude/plugins/cache` the CLI reads. They update independently. So a CLI can be fully current while Desktop shows a *frozen server-cached snapshot* (e.g. a pre-cutover version, or a since-decommissioned plugin), and local file checks can't diagnose a Desktop staleness — the relevant state is server-side and largely unseeable. Remove+reinstall re-fetches the same cache, so it isn't a fix. Tells live in `~/Library/Logs/Claude/claude.ai-web.log` + `main.log` (look for `fetchAccountScopedRemotePlugins`, marketplace `/sync` errors). Tracked in bds-hitoga.

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

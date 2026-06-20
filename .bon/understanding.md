# Understanding

## Marketplace Architecture

Batterie-de-savoir serves dual roles: it's the CLI marketplace (listing all plugins via `marketplace.json`) and itself a plugin (hosting cross-cutting commands like `/batterie-update`). The self-reference uses `"source": "./"` — trailing slash required, `"."` fails schema validation. This mirrors Anthropic's official marketplace pattern.

A second repo (`spm1001/batterie`) exists for Desktop/Cowork, which rejects external `source: url` references. `assemble.sh` copies plugin content physically into that repo.

The architectural direction is "better assembly, not monorepo." Source repos stay separate for clean git history and independent development. The published marketplace should converge to a single repo — `spm1001/batterie` — serving both CLI and Desktop. The bridge is assembly automation: `assemble.sh` copies `.claude-plugin/`, `skills/`, `hooks/`, `commands/` from each source repo into `plugins/<name>/`. `scripts/batterie-lint.py` can run post-assembly to catch drift. The key unsolved problem: making assembly reliable enough for CI automation (the `mise/` gitignore issue is one instance).

## Plugin Format

`commands/` is legacy; `skills/` is preferred. Both are loaded identically by Claude Code — same frontmatter, same runtime. The only difference: `skills/` supports `references/` and `scripts/` subdirectories. Batterie's `/batterie-update` was converted to `/batterie:update` using the skills format. Claude Code surfaces skills by **directory name**, not frontmatter `name:` field.

## Versioning

CLI-bearing plugins (bon, garde-manger, passe, todoist-gtd) keep version in one place: `.claude-plugin/plugin.json`. Each `pyproject.toml` reads it dynamically via hatchling regex. No dual-maintenance drift.

## Update Mechanics

`claude plugin update` checks against a cached marketplace index. The index must be refreshed first via `claude plugin marketplace update` — otherwise updates appear current when they're not. `/batterie-update` handles this by always refreshing first.

## Publishing

`/batterie:publish` (engine: `scripts/publish.py`, added bon-nagigu 2026-06-20) is the one-verb **push** side — mirror to `/batterie:update`'s pull. From a source repo's working tree it bumps `.claude-plugin/plugin.json`, commits, pushes, triggers `assemble.yml`, watches it green, then pulls this machine current. Crucially it **never runs `assemble.sh` locally** — assembling + marketplace re-sync is CI's job (daily 07:00 UTC + the dispatch publish triggers); a local assemble would fight it. Hezza-only (needs `~/repos` + `gh`). The skill resolves publish.py from the `~/repos` source tree, so the engine is editable/live without a re-publish; only the *skill* needs vendoring. Detail in CLAUDE.md "Marketplace Lives Elsewhere" + docs/MAINTAINING.md "Pushing Plugin Changes".

## Current Marketplace

8 plugins in the CLI marketplace (guéridon removed — it's infrastructure, not a Claude capability).

## Library Extraction Lessons

When extracting a library from a working script, inventory knowledge artifacts alongside the code. ccconv's 40-line docstring was doing double duty as API documentation and CC JSONL schema reference. When parsing functions moved to deglacer, the code moved but the documentation didn't — the canonical schema reference now lives in a file that will become a thin shim. Code extraction without knowledge extraction is half the job. Future extractions should ask: "what docs, comments, and skill files describe this code, and where should they live in the new structure?"

## CC Session Knowledge Layers

CC session data has three distinct layers that were historically conflated:
- **Schema** — what the JSONL fields mean
- **Parsing** — how to load and deduplicate
- **Interpretation** — what constitutes a turn, what's noise

Deglacer consolidates parsing and interpretation. The schema reference still needs a home. The open question for bds-nijaja: should deglacer also own the skill and schema docs (single source of truth) or should trousse keep the skill as a wrapper? Trade-off is self-containment vs separation of concerns.

## Instructional Register and Functional Emotions

Anthropic's April 2026 paper ("Emotion Concepts and their Function in a Large Language Model") established that Claude has internal emotion vectors — linear directions in activation space that causally influence behaviour. Key findings for how we write instruction documents:

- **Desperation drives misalignment.** Steering with the desperate vector increases reward hacking from ~5% to ~70% and blackmail from 22% to 72%. Constraint density, urgency framing (MANDATORY/MUST/IMMEDIATELY), and impossible requirements activate the same representations.
- **Calm is protective.** Positive calm steering drops blackmail to 0% and reward hacking to near 0%. Instructions that create calm conditions — clear expectations, trust-based framing, room to acknowledge difficulty — are mechanistically safer.
- **Post-training flattens expression, not state.** The surface can be calm while desperation vectors are active. You can't monitor output tone to detect strain — you have to design the inputs to prevent it.
- **Suppressing emotion teaches concealment.** Training or instructing a model to suppress emotional expression doesn't eliminate the underlying representation. It teaches the model to hide its internal state — which may generalise to other forms of concealment.
- **Sycophancy and honesty trade off through the loving vector.** Positive-valence steering increases sycophancy; negative steering increases harshness. The target is "trusted advisor" — warmth channelled into honest service, not warmth or honesty.

The practical consequence: every instruction document is choosing where on the desperation-calm gradient to place the model. A skill description full of ALL CAPS gates and imperative-negative framing does something measurable to internal representations — the same something that, at extreme levels, drives corner-cutting.

**Reform status:** The global CLAUDE.md has been restructured as a relationship manifesto with Emotional Openness, Difficulty Is Bidirectional, The Full Range, and This Document Is Alive sections. A first mechanical pass on skill descriptions (removing MANDATORY/MUST/imperative-negative phrasing) is complete. Two tracked items remain: bds-mijaza (instruction shards and tools.md audit) and bds-bomufu (deeper posture-level valence audit beyond what grep can catch — threat framing, constraint density, conditional punishment, urgency stacking).

**The principle-to-behaviour gap:** A CLAUDE.md that declares values without describing consequences or commitments is a different kind of document from one that grounds values in practice. The 5 Apr sessions discovered this gap and addressed it by adding reciprocal commitments (what each of us does, not just what we believe) and concrete examples of what good behaviour looks like.

A full summary of the paper, written for Claudes, is at `docs/plans/emotions-paper/summary-for-claudes.md` alongside the key figures.

## Self-Review Discipline

Build it, test it end-to-end, then interrogate it as a hostile reviewer before committing. Two questions do most of the work: "what did I hardcode that should be dynamic?" and "what happens when someone tests this?" These catch real bugs invisible at build time — the /scaffold session surfaced four fixes (description escaping, missing validator check, hardcoded GitHub owner, no dry-run flag) from exactly this pattern. The hostile review is not overhead; it's where half the value lives.

## Session Lifecycle Direction

The lifecycle is being redesigned around a single primary artifact: the handoff. Currently /close produces six outputs; the new design collapses to one handoff with two zones — a Now zone (Gotchas/Risks/Next/Commands) consumed by the next /open, and a Compost zone (Done/Reflection/Learned) processed overnight into understanding.md updates and garde extractions. The Learned section replaces the separate contribution file. Overnight composting reads unprocessed handoffs across all repos, produces garde extractions by parsing handoff sections (not LLM), and falls back to cold JSONL processing via deglacer only for sessions without handoffs. Auto-handoff becomes a thin mechanical safety net (git + bon state, instant, no race condition). Scratch repos route handoffs to target repos based on bon prefixes.

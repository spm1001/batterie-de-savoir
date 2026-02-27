# Batterie de Savoir — Agent Guide

This is the **documentation umbrella repo** for the Batterie de Savoir tool suite. It contains no runnable tools — just docs, a registry, and generation scripts.

## What this repo does

- `brigade.toml` — single source of truth for all tool metadata
- `scripts/render.py` — regenerates GENERATED sections in docs from the registry
- `scripts/lint.py` — detects drift between registry and docs (exit 1 if stale)
- `docs/` — Jekyll site, published to GitHub Pages

## The one rule

**Edit `brigade.toml`, then run `uv run --script scripts/render.py`.**

Adding or changing a tool means touching exactly one file. The render script handles the rest. Never hand-edit content between `<!-- GENERATED:*:START -->` and `<!-- GENERATED:*:END -->` markers — it will be overwritten.

To check for drift without writing: `uv run --script scripts/lint.py`

## What's generated vs authored

| File | Status |
|------|--------|
| Brigade tables in `README.md`, `docs/index.md` | **Generated** — run render.py |
| Vocabulary, routing, deps, repos in `docs/for-agents.md` | **Generated** — run render.py |
| `docs/tools/*.md` — individual tool pages | **Hand-authored** — never generated |
| `docs/getting-started.md` | **Hand-authored** |
| `docs/principles.md` | **Hand-authored** |
| `MAINTAINING.md` | **Hand-authored** |

Tool pages are hand-authored by design. The registry holds one-liners; tool pages hold judgement.

## Deliberate quirks — do not "fix" these

- **jeton has no public README** — it's the renamed `itv-google-auth` library. A 404 when fetching its README is expected.
- **`lint.py` imports `render.py` via `sys.path`** — intentional. Keeps one set of templates so lint tests exactly what render produces. Only safe because render.py's module-level code is side-effect-free (loads TOML, builds templates). Don't refactor by duplicating the rendering logic.
- **`from = ["all"]` in `[[dependency]]`** — sentinel for "All tools" in the dependency direction table. Documented in brigade.toml's schema comment.
- **Vocabulary and key-repos have static rows in separate tables** — GTD terms (Brigade, Outcome, Action, etc.) live in a "GTD & Brigade Terms" sub-table below the generated vocabulary table. The "This docs site" row lives in a separate mini-table below the generated key-repos table. Both are intentionally excluded from generation. The split exists because kramdown can't parse a table that spans across HTML comment markers.

## Python version note

This machine runs Python 3.9, which doesn't have `tomllib` (added in 3.11). The PEP 723 scripts declare `tomli; python_version < '3.11'` as a dependency — `uv run --script` handles this automatically. Don't validate TOML with bare `python3 -c "import tomllib"` — it'll fail. Use `uv run --with tomli python3 -c "import tomli; ..."` or just run the scripts via uv.

## Open outcomes

- `bds-lozeti` — Track Claude Office add-in bundle changes over time

---
layout: default
title: Consommé
---

# Consommé — Clarification

BigQuery data analysis for AI coding agents. Messy data goes in, crystal-clear insights come out — like the classical technique it's named for, where a raft of egg whites draws impurities from a murky stock and leaves behind a perfectly transparent broth. The technique does the work, not the person.

Consommé is a skill that pairs Google's BigQuery Data Analytics MCP extension with a structured methodology adapted from Anthropic's data plugin approach. It works with both Gemini CLI and Claude Code, giving either agent the same analytical discipline: a repeatable workflow from "what tables do we have?" to an interactive HTML dashboard with KPI cards and filters.

## When to use / When NOT to use

**Use Consommé when:**
- You need to explore, query, or analyse structured data in BigQuery
- You want interactive visualisations — HTML dashboards with Chart.js, filters, KPI cards
- You're building funnels, cohort analyses, or forecasts from warehouse data
- You need the agent to profile a dataset before jumping to conclusions

**Do NOT use Consommé when:**
- You need content from Google Workspace (Docs, Sheets, Gmail, Drive) — **use [Mise](mise)**
- You're working with local CSV/Excel files that aren't in BigQuery
- You need real-time streaming data rather than analytical queries

Consommé's own skill includes this routing explicitly. Tools referee themselves.

## Key concepts

### 5-stage methodology

1. **Discovery** — Catalogue search. What datasets and tables exist? What's the schema?
2. **Exploration** — 3-phase data profiling: structural (row counts, partitioning), column-level (types, nulls, cardinality), and relationships (keys, joins, referential patterns).
3. **SQL craft** — BigQuery-specific SQL reference: window functions, CTEs, funnels, cohort analysis, approximate aggregation.
4. **Analysis** — Execute queries via MCP tools (`execute_sql`, `forecast`, `analyze_contribution`). Interpret results in context.
5. **Validation** — Pre-delivery QA framework. Sense-check results before presenting. Does the total add up? Do the segments sum to the whole? Are there obvious outliers that signal a join gone wrong?

### MCP tools

Consommé works through Google's BQ Data Analytics MCP extension, which provides:
- `execute_sql` — run queries against BigQuery
- `forecast` — time-series forecasting
- `analyze_contribution` — driver analysis (what's contributing to a metric change?)
- Catalogue search — discover datasets and tables

### Visualisation

The output isn't a table dumped into chat. Consommé produces interactive HTML dashboards: Chart.js charts, filter controls, KPI summary cards — deposited to disk as a self-contained `.html` file the user can open in a browser. Token-efficient (the dashboard lives on disk, not in context) and human-friendly.

### Pre-delivery QA

Every analysis passes through a validation stage before the agent presents it. Row counts checked, segments verified to sum correctly, outliers flagged. The discipline is baked into the methodology, not left to the agent's discretion.

## How it relates to other tools

| Tool | Relationship |
|------|-------------|
| [**Mise**](mise) | Mise handles Google Workspace content (Docs, Sheets, Gmail, Drive). Consommé handles structured data in BigQuery. The boundary is explicit — Consommé's skill routes Workspace requests to Mise. |
| [**Bon**](bon) | An analysis task tracked as a bon outcome; Consommé does the analytical work within that outcome. |
| [**Garde-manger**](garde-manger) | Past analyses are searchable in garde-manger. Useful for "didn't we look at churn cohorts last month?" |

The Consommé ↔ Mise boundary is a concrete example of the **tools referee themselves** principle: Consommé's skill says "for Workspace content, use Mise." Neither tool tries to do both jobs. The brigade directs traffic.

## What Consommé is (and isn't)

Consommé is a **skill** — a behavioural document that teaches an AI agent a methodology. It is not a CLI, a library, or a Python package. There is nothing to `pip install` or `uv tool install`. You install it by symlinking the skill directory into `~/.claude/skills/` (or `~/.gemini/skills/`), and the agent loads it on demand when data work begins. The skill is invoked as `/consomme` in Claude Code.

The analytical capability comes from the external BQ MCP server (`bq-toolbox` or Google's BQ Data Analytics extension). Consommé provides the discipline — the structured methodology that turns "run some queries" into a repeatable analytical workflow.

## Repository

Source, skill content, and test plan: [github.com/spm1001/consomme](https://github.com/spm1001/consomme)

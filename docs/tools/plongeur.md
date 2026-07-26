---
layout: default
title: Plongeur
---

# Plongeur

*The dishwasher.*

In a kitchen the plongeur cleans what everyone else cooked with and hands it back ready for service. Plongeur does that for survey data: a Streamlit chat UI where a non-technical colleague asks a question in plain English, Gemini (via Vertex AI) writes and runs the BigQuery SQL, and the answer comes back as tables and branded charts.

It exists because the [Consommé](consomme) methodology — careful, weighted, schema-aware survey analysis — shouldn't require knowing SQL. Plongeur operationalises it with guardrails: a SQL linter that catches schema violations and statistical mistakes before queries reach BigQuery, a system prompt that encodes the survey-data domain rules (weighted percentages, Likert polarity, pre-aggregated vs respondent-level shapes), and self-documenting BigQuery tables underneath. The guardrails are the asset; the chat loop is just the door.

Two things that make it unusual in this suite:

- **It's not a Claude tool.** Plongeur is Gemini-powered and serves humans directly. Its place in the batterie is as the *other* door into the same curated data Claude reaches through Consommé — one methodology, two audiences.
- **It's estate-specific.** It lives in an ITV-internal repo ([`ITV/mit-plongeur`](https://github.com/ITV/mit-plongeur), private) and runs IAP-gated on ITV infrastructure. Unlike the rest of the suite, there's nothing here for an outside reader to install.

## When to use / When NOT to use

**Use Plongeur when:**
- A non-technical colleague wants to explore survey data conversationally — ask, look, refine
- You want the consommé guardrails (linter + methodology prompt) doing the statistical care, not the user

**Do NOT use Plongeur when:**
- You're a Claude session doing analysis — that's Consommé territory, via the BigQuery skills
- The data isn't in the curated, self-documenting BigQuery datasets — Plongeur only sees tables prepared for it

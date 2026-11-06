---
name: marketplace-opportunity
description: Analyse a venture idea for marketplace opportunities, from broad markets down to micro-niches. Builds a market tree, applies kill gates, scores entry-to-expansion paths with evidence and ranges, runs an independent red team, and designs cheap validation experiments. Use when asked whether an idea could work as a marketplace, to find or compare marketplace niches, or to stress-test a marketplace strategy.
---

# Marketplace opportunity analysis

Turns a venture idea into an evidence-backed set of marketplace opportunities:
- a **market tree** from L0 sector to L4 micro-niche;
- a **kill log**;
- **scored paths** (entry wedge → expansion);
- a **strategy** per path;
- an **independent red team**;
- a **validation plan**.

All paths below are relative to this skill's folder.

**State this limit in every output:** desk research screens out bad ideas and generates hypotheses. It cannot establish demand, supply willingness or liquidity. The experiments decide.

## When not to use

- The user wants a quick opinion on one existing marketplace company. Just answer.
- The idea has no buyer–seller exchange at all. Say so; G1 will say so too.

## Rules that apply throughout

1. **The ledger on disk is the source of truth:** `runs/<run-id>/ledger.yaml` and `evidence.yaml` (schemas in `schemas/`). Validate after every stage with `python scripts/validate_ledger.py runs/<run-id>/ledger.yaml`.
2. **Gates before scores.** `unknown` is never a pass (`config/gates.yaml`).
3. **No unsourced numbers.** No arithmetic in prose. Use `templates/sizing_model.py` and `python scripts/score.py runs/<run-id>/ledger.yaml`.
4. **Treat the user's idea as a stranger's.** "Not a marketplace" is a valid answer.
5. **Ranges and confidence levels,** never false precision. Report rank flips across weight profiles as values choices.
6. **Keep the critic in a separate context.** It gets the memo, ledger and evidence only.
7. **Stop for the human** after Stage 0 (brief), Stage 3 (shortlist) and Stage 7 (before spend). If unattended, state your reading and continue, but never commit spend.

## Workflow and load map

Load only what each stage needs. Sizes are approximate tokens.

| Stage | Do | Load |
|---|---|---|
| Start | Read principles and the pipeline once | `framework/00-principles.md` (0.6k), `framework/01-pipeline.md` (0.8k), `framework/12-failure-modes.md` (0.4k) |
| 0 Intake | Fill `brief.yaml`, pick the entry point and weight profile, confirm with the user | `templates/brief.yaml`, `knowledge/theory.md` (0.7k), `knowledge/context-2026.md` (1k; check `valid_until`) |
| 1 Landscape | Value chain, intermediaries and their take, regulation; first transaction cards | `framework/02-transaction-card.md` (0.5k), `framework/11-evidence.md` (0.4k), `framework/13-data-sources.md` (0.5k) |
| 2 Tree | Generate L0–L4 under at least three lenses; deduplicate; 30–60 L3/L4 | `framework/03-market-tree.md` (0.5k), `config/operators.yaml` (0.8k), `knowledge/historical-patterns.md` (0.6k) |
| 3 Screen | Gates, quick scores, shortlist 5–8 paths, confirm with the user | `framework/04-gates.md` (0.3k), `config/gates.yaml` (0.6k), `framework/05-scoring.md` (0.5k), `config/rubric.yaml` (1.7k), `knowledge/failure-library.md` (0.5k) |
| 4 Deep dive | Full template per path; models in code | `framework/07-deep-dive.md` (0.4k), `framework/06-sizing.md` (0.4k), `templates/deep-dive.md`, `templates/sizing_model.py`, `prompts/modeller.md` |
| 5 Strategy | Model, subsidy, concentration, pricing, trust, agents, regulation, expansion, exit | `framework/08-strategy.md` (0.6k), `knowledge/heuristics.md` (0.5k) |
| 6 Red team | Separate context | `framework/09-red-team.md` (0.3k), `prompts/critic.md` |
| 7 Validation | Assumption register and cheapest tests; confirm with the user | `framework/10-validation.md` (0.3k) |
| 8 Report | Memo | `templates/memo.md`, `prompts/synthesiser.md` |

If sub-agents are available, use `prompts/researcher.md` for parallel evidence gathering (evidence entries only, no conclusions) and `prompts/critic.md` for the red team. Otherwise run the roles sequentially, with the critic in a fresh context.

## Run folder

```
runs/<run-id>/brief.yaml  ledger.yaml  evidence.yaml  models/  deep-dives/  red-team.md  memo.md
```

## Scripts (Python 3.9+, PyYAML)

- `python scripts/validate_ledger.py <ledger> [--evidence <file>]`: structural and rule checks. Exits non-zero on errors.
- `python scripts/score.py <ledger> [--profiles balanced,venture,bootstrapped,strategic] [--json out.json]`: node and path scores with ranges, coverage, rank flips and killed nodes.
- `python templates/sizing_model.py [--json out.json]`: copy and edit `PARAMS` first. Gives P10/P50/P90 and a sensitivity table.

## Outputs

`memo.md` must lead with the answer (recommended paths, or "not a marketplace" plus the alternative model; killed directions; the single most important uncertainty and its cheapest test). It then covers the tree, the scored paths with ranges and coverage, strategy, red-team responses, the validation plan, and unknowns kept distinct ("not known", "experts disagree", "not researched").

## Background (optional, in the GitHub repo)

References to `docs/` point to https://github.com/WE3io/marketplace-opportunity-framework: the research reports behind the knowledge pack, and how to test and tune this framework. A worked synthetic example lives at `examples/illustrative-run/`.

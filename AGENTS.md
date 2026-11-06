# AGENTS.md

Instructions for AI agents working in this repository.

## What this repo is

A framework for analysing venture ideas as marketplace opportunities, from broad markets to micro-niches, designed to be run by an agent with a thinking model. Everything an agent needs at runtime is in **`skills/marketplace-opportunity/`**, which is also a self-contained Agent Skill.

## If you have been asked to analyse an idea

1. Read `skills/marketplace-opportunity/SKILL.md`. It has the rules, the stage-by-stage load map with token sizes, the scripts and the output contract.
2. Work in `runs/<run-id>/`. This folder is git-ignored because analyses are usually private. Do not commit run outputs unless the user asks.
3. Run the scripts from the repo root:
   ```bash
   pip install pyyaml            # jsonschema optional, for schema validation
   python skills/marketplace-opportunity/scripts/validate_ledger.py runs/<run-id>/ledger.yaml
   python skills/marketplace-opportunity/scripts/score.py runs/<run-id>/ledger.yaml
   cp skills/marketplace-opportunity/templates/sizing_model.py runs/<run-id>/models/<path-id>.py
   ```
4. To see the format end to end, inspect `examples/illustrative-run/`. It is synthetic data, never to be cited.

## If you have been asked to change the framework

- **Canonical sources.** Edit these, not the generated spec:
  - gates: `config/gates.yaml`
  - criteria and anchors: `config/rubric.yaml`
  - weights: `config/weights.yaml`
  - generation operators: `config/operators.yaml`
  - output contracts: `schemas/*.json`
- **Keep ids in sync.** If you add or rename a criterion or gate, update the schema, the templates, the example ledger, and any framework module that names it. Then run both scripts against `examples/illustrative-run/ledger.yaml`.
- **Regenerate the single-file spec** after editing modules or config: `python tools/build_spec.py`, which writes `docs/framework-spec.md`. Do not edit that file by hand.
- **The knowledge pack is perishable.** When updating `knowledge/context-2026.md`, update `as_of` and `valid_until`, cite sources, and keep confidence labels.
- **Tune with evidence.** Changes to weights or anchors should be justified with results from `docs/testing-the-framework.md` (backtests, consistency runs, golden set), not intuition.

## Conventions

- British English. Direct, evidence-first prose. Confidence labels (high, moderate, low) on disputable claims.
- Keep files small and single-purpose, so agents load only what a stage needs. Put a short front-matter block (purpose, stage, load_when) at the top of framework and knowledge modules.
- Numbers come from sources or code, never from memory.

## Map

```
skills/marketplace-opportunity/   # runtime: the skill
  SKILL.md                        # entry point and load map
  framework/  00-13 modules       # process and rules, one concern per file
  knowledge/                      # theory, heuristics, historical patterns, 2026 context, failure library
  config/                         # gates, rubric, weights, operators (canonical, machine-readable)
  schemas/                        # ledger and evidence JSON Schemas
  templates/                      # brief, ledger, deep dive, memo, sizing model
  prompts/                        # orchestrator, researcher, modeller, critic, synthesiser
  scripts/                        # validate_ledger.py, score.py
examples/illustrative-run/        # synthetic worked example
docs/                             # generated full spec, testing guide, research reports
tools/build_spec.py               # regenerates docs/framework-spec.md
```

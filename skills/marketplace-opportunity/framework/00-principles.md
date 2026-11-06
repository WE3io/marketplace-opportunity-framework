---
purpose: What the framework is for, its limits and its design principles
stage: all
load_when: Always, once per run
---

# Principles

## What this framework does

It takes a venture idea and produces, with evidence:
- a **market tree** from sector (L0) to micro-niche (L4);
- the candidates killed and why;
- a shortlist of **paths** (entry wedge → expansion sequence) scored with ranges;
- a strategy per path;
- an independent **red team**;
- a **validation plan** of cheap experiments aimed at the riskiest assumptions.

## Its limit, which must be stated in every output

Desk research can screen out bad ideas and generate well-formed hypotheses. It cannot establish demand, supply willingness or liquidity. Judge the output on how well it kills bad ideas cheaply and points to the right experiments, not on how confidently it picks winners.

## Principles

1. **Transaction first.** Every node reduces to at least one transaction card (`02-transaction-card.md`). If it cannot, it is a theme, not a market.
2. **Paths, not points.** Recommend an entry niche plus an expansion sequence plus a monetisation stack. A great niche that leads nowhere, and a large market with no viable wedge, are both poor recommendations.
3. **Gates before scores.** Kill criteria (`config/gates.yaml`) run before scoring. *Unknown* is never a pass; it becomes a priority assumption.
4. **Evidence or assumption.** An unsourced claim is an assumption, logged with a widened range and lower confidence.
5. **Disconfirm before confirm.** Search for reasons each candidate fails. Base rates are grim (`knowledge/historical-patterns.md`, `knowledge/failure-library.md`).
6. **A marketplace is one option, not the goal.** Test against SaaS, first-party retail, lead generation, a managed service, a community, or a tool that later grows a network. "Do not build a marketplace" is a valid conclusion.
7. **2026-aware.** Profit sits above the commission line. AI substitution and agent bypass are first-class risks. Regulators deputise platforms (`knowledge/context-2026.md`).
8. **Calibrated, not precise.** Ranges, confidence levels and sensitivity to weightings. No single scores to one decimal place.
9. **The user's idea gets no special treatment.** Assess it as if a stranger had submitted it. Optimism is the most common failure mode of agents on this task.

## How much to trust each part

| Part | Status |
|---|---|
| Theory core (`knowledge/theory.md`) | High confidence: established literature |
| Practitioner heuristics (`knowledge/heuristics.md`) | Moderate: survivor-derived |
| 2026 context (`knowledge/context-2026.md`) | Moderate and perishable; check `valid_until` |
| Gates, rubric anchors, weights, operators, pipeline | Design judgement. A starting configuration to tune with `docs/testing-the-framework.md` |

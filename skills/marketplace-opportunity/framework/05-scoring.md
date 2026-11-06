---
purpose: How to score nodes and paths, and how to read the results
stage: 3 (quick), 4 (full), 6 (revision)
load_when: Any time scores are written or interpreted
config: config/rubric.yaml (criteria and anchors), config/weights.yaml (profiles, path settings)
script: scripts/score.py
---

# Scoring

## Rules

1. **Score against the anchors** in `config/rubric.yaml`. Every criterion runs 1–5 and **5 is always favourable**: inverse risks such as leakage, multi-homing and AI substitution are phrased so that 5 means low risk. Interpolate 2 and 4.
2. **Every score has** `central`, `low`, `high`, `basis` and `evidence`.
   - `basis: evidence` requires at least one evidence id of moderate or high confidence.
   - Otherwise use `basis: assumed` and widen the range (typically ±1.5 or more).
3. **Missing criteria** are treated by the script as maximally uncertain (central 3, range 1–5). Coverage will show it.
4. **Never do weighted arithmetic in prose.** Run `scripts/score.py`.

## Profiles

Run every shortlist under at least three profiles (`config/weights.yaml`): **balanced**, **venture**, **bootstrapped**, plus **strategic** for corporate builders. `score.py` flags rank flips. If the ranking flips, the choice depends on the founder's values (ambition, capital, time), not on analysis. Say so.

## Reading the results

- **Attractiveness × confidence.** High score with low coverage means "research next", not "build". Low score with high coverage means "kill with confidence".
- **Ranges overlap.** If two paths' ranges overlap substantially, do not rank them strictly. Report them as tied, and say what evidence would separate them.
- **Path score.** It combines wedge quality (the first node), terminal value (the highest-level node in the sequence) and expansion plausibility, capped at the weakest component plus a margin. A brilliant wedge with no route upwards, or a large market with no viable wedge, cannot score highly.
- **Coverage.** The share of weighted criteria backed by evidence. Below about 50% at Stage 4, the deep dive is not finished.

## Quick scoring at Stage 3

Score only the criteria that cheap evidence can support (structure, regulation, AI substitution, incumbent proximity). Leave the rest missing and let the script widen the ranges. Shortlist on gates plus the top ranges, keeping at least one contrarian candidate whose upside range is high.

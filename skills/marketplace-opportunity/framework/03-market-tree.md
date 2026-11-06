---
purpose: How to generate the market tree from sector to micro-niche
stage: 2
load_when: Stage 2; Stage 4 when proposing expansion steps
config: config/operators.yaml (canonical list of levels, entry points, lenses, operators, controls, signals)
---

# Market tree generation

## Levels

L0 sector → L1 market → L2 segment → L3 niche → L4 micro-niche. Evaluation emphasis shifts down the tree:
- At L1–L2 the questions are about terminal value and structure.
- At L3–L4 the questions are about wedge quality, time to liquidity and hard-side access.

An **L4 micro-niche** is small enough that a small team can reach liquidity within months, and has a distinct vocabulary and buying criteria.

**Illustrative path** (shows mechanics only; not an assessment):
- L0 property services
- L1 landlord compliance services
- L2 safety certification for private rentals
- L3 certification for HMO landlords in London
- L4 bundled annual certification booking for HMO landlords in one borough

This is a regulation-first entry: a recurring mandate supplies frequency and urgency.

## Procedure

1. **Classify the entry point** of the user's idea (`config/operators.yaml → entry_points`). Each entry point favours certain operators.
2. **Pick at least three lenses** (`lenses`) that differ meaningfully. Generate candidates under each lens separately. One-pass generation collapses into the same few obvious ideas.
3. **Apply operators:**
   - `descend` operators to move down the tree;
   - `transform` operators to change the shape (flip sides, change the object, change matching mode, unbundle a horizontal, tool-to-network, compliance-led, agent-side, AI-revived graveyard);
   - `ascend` operators to sketch the expansion ladder for each promising L3/L4 node.
4. **Ground every node.** It needs a transaction card and at least one evidence item showing the transaction happens today. Use `micro_niche_signals` to find them.
5. **Cluster and deduplicate** across lenses. Merge near-duplicates and keep the best-evidenced version.
6. **Respect the caps:** 30–60 L3/L4 candidates. More dilutes depth.
7. **Reject templated suggestions.** "Uber for X" must be rewritten with named buyers, suppliers and trigger, or discarded.
8. **Record provenance.** For each node, record the lens and operator in the ledger, so ablation tests can tell which lenses produce survivors.

## Paths

A path is an ordered list of node ids: the entry wedge first, then expansion steps upwards or sideways. Create paths for nodes that survive the screen. Every path needs an `expansion_plausibility` score: how likely the wedge's network, brand and data are to carry over to the next step. `scripts/score.py` caps a path at its weakest component plus a margin (`config/weights.yaml → path`).

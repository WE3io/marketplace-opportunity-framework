---
purpose: How to test, tune and evolve the framework itself
audience: People and agents changing the framework, not running it
---

# Testing the framework

The gates, anchors, weights, operators and pipeline are a starting configuration, not tested values. Without the harness below you cannot tell whether the framework is any good.

## 1. Backtests (with an honest caveat)

- Run the framework blind on historical ideas as they looked at their founding date: successes, failures and repricings.
- **Include failures.** Otherwise the backtest teaches survivorship bias.
- **Contamination is unavoidable,** because the model knows outcomes. Mitigate by masking names and dates, using obscure regional cases, and weighting cases that post-date the model's training cut-off.
- **Measure:** did the gates kill the failures? Did the shortlists include the successes? Were confidence levels calibrated?

## 2. Golden set

- Have experienced marketplace operators label 20–30 opportunity briefs (pursue, pivot or kill), with reasons.
- Compare the agent's gate results and path rankings with the labels. Investigate disagreements before changing weights.

## 3. Consistency

- Run the same brief three to five times. Measure variance in the shortlist (overlap) and the rank order (for example Kendall's tau).
- High variance points to vague rubric anchors or generation without enough diversity controls. Fix the anchors before the weights.

## 4. Ablations

- Remove one component at a time: the critic, the lenses, individual gates, the profile comparison. Measure what changes.
- A component that never changes the output is cost without value.
- Use the `lens` and `operator` fields in the ledger to see which lenses produce survivors.

## 5. Planted-error tests for the critic

- Seed memos with known errors: an inflated market size, a missing licence requirement, a leakage-prone model scored as low-leakage, a vendor statistic presented as independent.
- Measure detection rate and false-alarm rate. The critic is valuable only if it catches errors, not merely if it produces objections.

## 6. Prospective tracking

- Log recommendations, stated confidence levels and the experiments run. Revisit after 6–12 months.
- Calibrate: do "high confidence" kills and recommendations hold up more often than "moderate" ones?

## 7. Knowledge-pack maintenance

- Refresh `knowledge/context-2026.md` at least quarterly, or rename it as the year changes. Update `as_of` and `valid_until`, re-verify figures, and keep confidence labels.
- Add to `knowledge/failure-library.md` only cases verified with sources.

## Build plan

- **v0 (days):** a single thinking-model session using the skill, run on three real ideas and inspected by hand. Goal: find vague anchors and gates that are hard to call.
- **v1 (weeks):** the multi-role pipeline (orchestrator, parallel researchers, a code modeller, an independent critic) with UK registry connectors where APIs exist (Companies House, Nomis).
- **v2 (ongoing):** this harness, weight tuning from the golden set, worked examples (including failures) as few-shot anchors, and quarterly knowledge-pack refreshes.

## Open decisions for whoever adopts this

1. **Default ambition profile:** venture, bootstrapped or strategic?
2. **Thresholds:** the minimum terminal market and the maximum time to liquidity.
3. **Geography scope:** UK only, UK plus EU, or global. This changes the regulatory modules materially.
4. **Data budget:** paid keyword, traffic and funding data. Without it, demand-side confidence is mostly moderate at best.
5. **Testing:** who supplies golden-set labels?

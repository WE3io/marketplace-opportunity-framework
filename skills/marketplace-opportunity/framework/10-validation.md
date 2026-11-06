---
purpose: Turn uncertainty into the cheapest falsification experiments
stage: 7
load_when: Stage 7
---

# Validation plan

1. **Assumption register** (in the ledger). Every assumption has:
   - **impact** (1–5): how much the decision changes if it is wrong;
   - **uncertainty** (1–5).

   Rank by impact × uncertainty, which is the expected value of information. Gate *unknowns* and the top sensitivity drivers from the model are always included.
2. **Design the cheapest test for each of the top three to five assumptions.** Each test has a design, a metric, a threshold, a cost and a time-box. Marketplace-specific tests:
   - **Hard-side commitment:** will suppliers commit time, inventory or a fee before demand exists?
   - **Concierge or manual matching** in one atomic network.
   - **Demand fake door or waitlist,** stronger with a deposit.
   - **Liquidity test:** match rate and time to match in one area or community.
   - **Take-rate acceptance:** price tests on the paying side.
   - **Leakage probe:** what share of repeat transactions come back through the platform?
   - **Trust test:** does verification or a guarantee change conversion?
3. **The founder sets the thresholds.** The agent may suggest ranges from comparables, flagged low confidence, but must not invent universal benchmarks.
4. **Write kill and continue criteria before running the tests.** Record them in the ledger so results cannot be reinterpreted afterwards.
5. **Sequence the tests** so the cheapest test that could kill the idea runs first.

---
purpose: Bottom-up sizing and unit economics
stage: 4
load_when: Before producing any market size, GMV, revenue or unit-economics figure
template: templates/sizing_model.py
---

# Sizing and unit economics

LLM agents are at their worst on market sizing. These rules exist to stop plausible fiction.

## Rules

1. **Bottom-up only.** Top-down and vendor figures are sanity checks at most, flagged low confidence. Resale and "industry" reports sponsored by operators are often survey-based and internally inconsistent.
2. **Count real populations,** from registries where possible. UK sources:
   - Companies House SIC codes and filed accounts;
   - ONS and Nomis business counts;
   - licensing and professional registers;
   - trade-association membership;
   - community and event sizes.

   Each input carries an evidence id.
3. **Triangulate with at least two methods.** For example, population × observed frequency × order value, set against incumbent revenue ÷ incumbent take rate. Report a range and a confidence level.
4. **Model in code** (`templates/sizing_model.py`). Use triangular (low, mode, high) inputs and report P10/P50/P90. Do no arithmetic in prose.
5. **Size the atomic network separately from the total market.** The size of the first network is often more decision-relevant than the size of the total market.
6. **Flag geography mismatches.** US benchmarks applied to a UK niche get a confidence penalty unless justified.

## Core identities

```
GMV            = transacting buyers × transactions per buyer per year × order value
Net revenue    = GMV × take rate + ancillary revenue
Contribution   = net revenue − payment costs − support and trust-and-safety − compliance − subsidies
Payback        = acquisition cost per buyer ÷ annual contribution per buyer
```

Leakage reduces on-platform repeat transactions. Model it explicitly, because it usually decides viability along with take rate and repeat rate.

## Outputs

- A model file in `models/`.
- A `sizing` block on the node: `gmv_low`, `gmv_high`, `currency`, `atomic_network`, `model_ref`, `confidence`.
- A sensitivity (tornado) table showing which inputs move contribution most. Those inputs become assumptions for Stage 7.

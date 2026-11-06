---
purpose: How to apply the kill gates
stage: 3 (and again in 4 and 6 when evidence changes)
load_when: Stage 3
config: config/gates.yaml (canonical gate definitions)
---

# Gates

Gates run **before** scoring, so effort goes into candidates that can survive.

## Rules

- Each gate returns `pass`, `fail` or `unknown`, with a one-line rationale and evidence ids.
- **fail:** set `status: killed` and write `kill_reason`, or redesign. A redesign is a new node (a narrower niche, a managed model, a different object) and its parent stays killed.
- **unknown:** never a pass. Add an assumption to the register with impact 4–5, and gather evidence before shortlisting.
- **G1 can conclude that the right answer is not a marketplace.** Record it in `alternative_model` (saas, first_party_retail, lead_generation, managed_service, community). That is a useful output, not a failure of the run.
- **G2 (leakage) and G7 (AI substitution)** are where 2026 differs most from the 2015 playbook. Give them the most evidence.
- **Re-run gates** when a deep dive or the red team changes the evidence.

## Gate order (cheapest evidence first)

G1 fit → G4 regulation → G5 incumbent → G7 AI substitution → G2 leakage → G3 atomic network → G6 economics. G6 usually needs the Stage 4 model, so at Stage 3 it can stay `unknown` unless the case is obvious.

## Kill log

Killed nodes stay in the ledger. The kill log is a valuable output: it shows the founder which directions were tested and why they fail, and it lets the red team check for over-zealous kills.

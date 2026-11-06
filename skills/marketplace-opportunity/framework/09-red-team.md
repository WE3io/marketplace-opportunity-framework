---
purpose: Independent critique of each path
stage: 6
load_when: Stage 6 (critic only)
prompt: prompts/critic.md
---

# Red team

The critic runs in a **separate context**. It receives the memo draft, `ledger.yaml` and `evidence.yaml`, and **not** the orchestrator's reasoning, so its judgement is not anchored on the generator's.

## Tasks

1. **Steelman the bear case** for each path.
2. **Pre-mortem:** "It is two years from now and this failed. What happened?" Give the three most likely causes.
3. **Reference class:** compare with `knowledge/failure-library.md` and the closest analogues, successful and failed. State the base rate.
4. **Audit the evidence:**
   - re-check every number that moves a gate or a top-three score;
   - flag single-source claims, vendor or investor interest, stale dates and geography mismatches.
5. **Search to falsify:** run queries designed to find disconfirming evidence, such as earlier failed attempts, incumbent features, regulatory blocks or supplier hostility.
6. **Incumbent response:** what the nearest big platform does if this works.
7. **Scenarios:** AI substitution and agent bypass played forward 24 months.
8. **Over-kill check:** sample killed nodes and test whether any was killed on weak evidence.

## Output (`red-team.md`)

Objections ranked by severity (critical, major, minor). Each one states:
- the gate or score it would change, and to what;
- the evidence that would resolve it.

Critical objections send the path back to Stage 4. The orchestrator must respond to each objection in the memo: accepted and changed, rebutted with evidence, or left open as an assumption.

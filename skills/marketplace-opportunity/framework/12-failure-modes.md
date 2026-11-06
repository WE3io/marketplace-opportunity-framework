---
purpose: Known failure modes of LLM agents on this task, and the guardrails against them
stage: all
load_when: Stage 0 (orchestrator); Stage 6 (critic)
---

# Failure modes and guardrails

| Failure mode | Why agents fall into it | Guardrail |
|---|---|---|
| Optimism or sycophancy towards the user's idea | Helpfulness training; the user's framing anchors | Treat the idea as a stranger's; independent critic; G1 can say "not a marketplace"; bear case required |
| Hallucinated or inflated market sizes | Plausible numbers are cheap | Bottom-up only; registry counts; code models; no unsourced numbers |
| Vendor market-size laundering | Vendor reports rank well in search | Interest flags; low confidence by default |
| Generic "Uber for X" ideas | Pattern completion | Transaction card required; named trigger and counterparties; lenses plus deduplication |
| Ignoring leakage and cold start | Invisible in desk research | G2 and G3 are hard gates; liquidity plan required |
| Treating marketplace, SaaS and e-commerce as one thing | Loose definitions | G1 with explicit alternatives |
| Recency and US bias | Training and search skew | Geography tags; UK sources first where relevant; confidence penalty for transplanted benchmarks |
| False precision | Weighted sums look rigorous | Ranges; coverage; several profiles; ties reported as ties |
| Breadth over depth | Ideas are cheaper than evidence | Caps; budget split; shortlist checkpoint |
| Self-grading | Generator and judge share a context | Critic in a separate context with evidence-only handover |
| Stale context | 2026 facts age fast | `valid_until` on the context pack; re-verify decision-critical facts |
| Over-killing on thin evidence | Gates feel decisive | `unknown` is allowed; critic samples killed nodes |
| Narrative drift across long runs | Context windows | Ledger on disk is the source of truth; validate after each stage |

---
purpose: Reference classes of marketplace failure and repricing, for screening and red-teaming
load_when: Stage 3 (screen) and Stage 6 (red team)
confidence: as marked per case. Add cases only after verifying them with sources.
---

# Failure library

Use these to build reference classes. For each candidate, name the closest failure and explain why this time is different. If the agent cannot, that is a finding.

| Case | Pattern | What failed | Lesson for gates and criteria | Confidence |
|---|---|---|---|---|
| Covisint (2000) | B2B exchange owned by rival buyers (Ford, GM, DaimlerChrysler) | Owner deadlock; only 40 of about 30,000 suppliers signed up in five months | G1/G3: supplier incentives and governance; a buyer consortium is not a neutral marketplace | moderate |
| Convoy (collapsed 2023) | Venture-funded digital freight marketplace | Cyclical, thin-margin market; its tech was sold for a fraction of the capital raised | Unit economics and cyclicality; G6 | moderate |
| Faire (repriced 2025) | Wholesale marketplace | Valued at $5.2bn in its Nov 2025 tender against $12.4bn in 2021 | Valuation is not viability; sizing discipline | high |
| OpenAI Instant Checkout (2025-26) | Agentic checkout inside a chat assistant | Handed back to merchants in Mar 2026; Walmart saw a third of the click-out conversion rate | Agent-bypass threat is real for discovery, weaker for checkout so far | high |
| Temu/Shein parcel model (2025-26) | Direct-from-factory cross-border parcels | Customs exemptions removed (US Aug 2025, EU Jul 2026); Shein's US revenue fell 14% in Q1 2026 | Policy is a first-order risk; G4 and the regulation criterion | moderate |
| Fiverr and Angi (2025-26) | Freelance and lead-generation marketplaces | Active buyers −26% (Fiverr) and revenue −9% (Angi), linked to AI substitution and lost search traffic | G7, discovery dependency | high (figures); moderate (causes) |
| Medieval English market grants (1300-1600) | Speculative franchises | Only 39% of 1300 market places survived to about 1600 | Base rate: most new markets fail | high |

## Add with verification

Classic service-marketplace failures attributed to leakage, and recent proptech and autotech collapses, belong here once sourced. Do not cite them from memory.

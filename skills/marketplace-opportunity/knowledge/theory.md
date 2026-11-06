---
purpose: Stable economic theory of marketplaces, used as priors when gating and scoring
load_when: Stage 0 (once per run); re-read before scoring if unsure
confidence: high (established literature)
---

# Marketplace theory: the stable core

Use these as priors. They explain *why* the gates and criteria exist.

| Idea | Source | What it means for the analysis |
|---|---|---|
| Price structure matters, not just price level | Rochet & Tirole, "Platform Competition in Two-Sided Markets" (2003), [doi](https://doi.org/10.1162/154247603322493212) | Volume depends on how fees are split between sides. Pricing one side below cost can be rational. Ask who should pay. |
| Divide and conquer | Caillaud & Jullien (2003) | Subsidise one side to attract it, then charge the other. The cold-start lever. |
| Competitive bottleneck | Armstrong, "Competition in Two-Sided Markets" (2006) | Platforms extract surplus from the side that uses only one platform. Multi-homing limits power: score it. |
| Network effects | Katz & Shapiro (1985) | Distinguish local from global, cross-side from same-side, and data or reputation effects. Local effects defend less but bootstrap faster. |
| Thick, uncongested, safe | Roth, "What Have We Learned from Market Design?" (2008), [doi](https://doi.org/10.1111/j.1468-0297.2007.02121.x); Nobel 2012 | A market needs enough participants (thickness), time to evaluate options (no congestion) and safety in participating. "Repugnance" (Roth 2007) limits what can be traded. |
| Lemons | Akerlof (1970), [jstor](https://www.jstor.org/stable/1879431) | When buyers cannot judge quality, good sellers exit. Trust infrastructure (verification, escrow, guarantees) is the product. |
| The platform's four jobs | Einav, Farronato & Levin, "Peer-to-Peer Markets" (2016), [nber](https://nber.org/papers/w21496) | Search, matching, pricing and trust. Ask which of the four the incumbents do badly. |
| Marketplace vs market principle | Bohannan & Dalton, *Markets in Africa* (1962) | Price-setting exchange can exist without a marketplace, and marketplaces can exist where prices do not govern. Many "markets" are better served without a platform. G1 applies this. |
| Information scarcity and clientelisation | Geertz, "The Bazaar Economy" (1978) | Where information is "poor, scarce, maldistributed", buyers form lasting ties with sellers rather than shopping around. That signals both an opportunity and a leakage risk. |
| Embeddedness | Granovetter (1985); Fligstein (2001) | Real markets run on relationships, law and politics. Markets become less *personal*, not less *social*. Design for the social layer. |
| Reputation systems inflate | Resnick & Zeckhauser (2002), eBay 1999 data | Feedback was "almost always positive" and reciprocal. Design ratings to resist inflation. |

## Implications the agent must carry into every run

1. Two-sided pricing means "what take rate?" is the wrong first question. Start with "who pays, for what, and who is subsidised?"
2. Liquidity is the product. The first unit to build is the smallest network in which matches happen reliably.
3. Trust is the reason many marketplaces can charge at all. If quality is obvious and cheap to verify, the take rate has little to stand on.
4. Concentration of supply, multi-homing and leakage cap pricing power more than anything the platform does.

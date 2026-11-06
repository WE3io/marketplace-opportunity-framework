---
purpose: The atomic unit of analysis
stage: 1, 2, 4
load_when: Before creating or editing any node
---

# The transaction card

Every node in the tree carries at least one card. A node is ready to score only when its card is filled from evidence, not imagination. Schema: `transaction_card` in `schemas/ledger.schema.json`.

| Field | Question |
|---|---|
| buyer | Who pays? Segment, count, and whether they are the decision-maker |
| seller | Who supplies? Segment, count, fragmentation |
| object | What changes hands: goods, a service, access, capacity, time, data, risk transfer or an outcome guarantee? |
| job | Why the buyer transacts |
| trigger | What forces the purchase: urgency, a mandate, a life event or a schedule |
| frequency | How often a buyer transacts, and with how many different suppliers |
| aov | Typical order value and the range |
| current_channels | How it happens today, including informal channels (WhatsApp or Facebook groups, forums, spreadsheets, word of mouth) |
| current_intermediary | Who sits in the middle today and what they take |
| frictions | Search cost, trust gap, price opacity, payment risk, logistics, compliance, scheduling |
| information_asymmetry | Who knows quality, and can it be verified before purchase? |
| persistence | After the first match, do the same parties keep transacting? This drives leakage (gate G2) |
| liability | Who bears risk if it goes wrong, and could the platform credibly take some of it? |
| regulation | Licences, safety rules, worker status, tax reporting, consumer law |
| ai_exposure | Could AI do the service itself (substitution)? Could a buyer's agent do the matching (bypass)? |
| evidence | Evidence ids supporting the card |

## Quality bar

- **Name the trigger.** "Small businesses need help" is not a trigger. "Landlords must renew a certificate every 12 months" is.
- **Count both sides.** If the agent cannot estimate even an order of magnitude for supply and demand in the entry niche, the card is incomplete.
- **Show the transaction happens today.** At least one evidence item must show it happening now, informally counts. If nobody transacts today, the idea is creating a market, not a marketplace: higher risk, flag it.

---
purpose: Where to find evidence, with access notes and fallbacks
stage: 1, 2, 4
load_when: Researchers; Stage 1 landscape
---

# Data sources

| Need | Sources (UK first) | Access note and fallback |
|---|---|---|
| Web research | Search and fetch tools | Some sites block agents; log what could not be reached rather than routing around it |
| Business populations | Companies House (SIC codes, accounts, officers); ONS UK Business Counts via Nomis; licensing and professional registers (e.g. Gas Safe Register, FCA register, CQC, local-authority licensing) | Free. Registries make micro-niche sizing tractable |
| Household and consumer counts | ONS, Census 2021, English Housing Survey, Ofcom reports | Free; check the reference period |
| Incumbent economics | Filed accounts, SEC filings (10-K, 10-Q, 8-K), investor relations, pricing pages, fee schedules | Small UK companies file abbreviated accounts; use proxies and flag them |
| Demand signals | Search-trend tools; keyword tools (often paid); app-store reviews; review sites | Paid tools may be unavailable; downgrade confidence |
| Informal trading and communities | Reddit, Mumsnet, specialist forums, public Facebook groups, Discord | Partly inaccessible to agents; flag for human checks |
| Supply signals | Job boards; trade directories; registers | Proxies only |
| Traffic and competition | Traffic-panel estimates; app rankings; category pages of incumbents | Panel estimates are moderate confidence at best |
| Funding and comparables | Crunchbase, Dealroom, PitchBook (paid); press | Fall back on press, low confidence |
| Regulation (UK) | legislation.gov.uk; gov.uk consultations and guidance; CMA; HMRC; Office for Product Safety and Standards | Primary sources; cite the section |
| Regulation (EU/US) | EUR-Lex; Commission DSA/DMA pages; FTC; CPSC; state statutes | Primary sources |
| Modelling | Python or spreadsheet sandbox | Required. No prose arithmetic |

## Research brief template (for researcher sub-agents)

```
Question: <one narrow question>
Node or path: <id>
Geography and period: <...>
Return: evidence entries in schemas/evidence.schema.json format only. No conclusions.
Prefer: <source types>. Flag: single-source, interested sources, stale data.
Stop when: the question is answered with at least one moderate- or high-confidence source, or after <N> searches. Then report what could not be found.
```

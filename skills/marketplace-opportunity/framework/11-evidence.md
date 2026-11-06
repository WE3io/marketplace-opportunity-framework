---
purpose: Evidence and confidence protocol for every claim and number
stage: all
load_when: Always (researchers in particular)
schema: schemas/evidence.schema.json
---

# Evidence protocol

## Source hierarchy (strongest first)

1. Company filings; official statistics
2. Regulator documents; court records; legislation
3. Independent analysis; peer-reviewed research
4. Analyst estimates; panels
5. Press reports
6. Vendor-sponsored surveys and models
7. Investor essays
8. Forums and anecdote (useful as demand signals, weak as measurement)

## Every evidence entry records

`id`, `claim`, `source` (publisher, title, URL, type), `published`, `period` described, `geography`, `confidence` (high, moderate or low), `interest_flag` (none, vendor, investor, operator) and `single_source`.

## Rules

- **No unsourced numbers in outputs.** A number without an evidence id is an assumption and must be labelled as one.
- **Arithmetic happens in code.** Cite the model output.
- **Distinguish three answers:**
  - **not known:** no adequate evidence exists;
  - **experts disagree:** informed sources conflict on the same evidence;
  - **not researched:** a gap in this run.

  Never merge them.
- **Single-source claims are flagged** and down-weighted, and never alone support a gate result.
- **Interested sources** (vendors, investors talking their book, operators) cannot alone support a high-confidence score.
- **Date-stamp everything.** Figures older than 18 months need a note on whether they still hold.
- **Geography:** a US figure used for the UK gets a confidence penalty unless justified.
- **Conflicts go in a table** (item, version A, version B, assessment) rather than being silently resolved.
- **Synthetic or illustrative data** must use `source.type: synthetic` and must never appear in a real memo.

## Confidence levels

| Level | Meaning |
|---|---|
| high | Primary or independent source, recent, directly measures the claim, ideally corroborated |
| moderate | Reputable but indirect, single-source, estimated or somewhat dated |
| low | Interested source, survey of unknown method, old, transplanted geography, or inference |

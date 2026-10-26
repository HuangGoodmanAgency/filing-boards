---
license: cc-by-4.0
language:
  - en
pretty_name: "Edgar & Edgarette: every SEC 8-K event the day it is filed, Altman, Piotroski, Beneish and a credibility-weighted forecast range for every filer, scored in public"
size_categories:
  - 10K<n<100K
task_categories:
  - tabular-classification
  - text-retrieval
tags:
  - sec
  - edgar
  - 8-k
  - filings
  - finance
  - corporate-events
  - primary-source
  - forecasting
  - calibration
  - prediction-intervals
  - uncertainty-quantification
  - pre-registered
  - outcome-supervision
  - company-fundamentals
  - xbrl
  - altman-z
  - piotroski
  - cybersecurity-incidents
  - agentic-commerce
configs:
  - config_name: cmo-moves
    data_files: data/cmo-moves.csv
  - config_name: agreements
    data_files: data/agreements.csv
  - config_name: mergers
    data_files: data/mergers.csv
  - config_name: charter-amendments
    data_files: data/charter-amendments.csv
  - config_name: annual-meetings
    data_files: data/annual-meetings.csv
  - config_name: ipo-watch
    data_files: data/ipo-watch.csv
  - config_name: restructuring
    data_files: data/restructuring.csv
  - config_name: breaches
    data_files: data/breaches.csv
  - config_name: auditor-watch
    data_files: data/auditor-watch.csv
  - config_name: cyber-disclosures
    data_files: data/cyber-disclosures.csv
  - config_name: agentic-commerce
    data_files: data/agentic-commerce.csv
  - config_name: subsea-data
    data_files: data/subsea-data.csv
  - config_name: company-cards
    data_files: data/company-cards.csv
  - config_name: company-cards-full
    data_files: data/company-cards.jsonl
  - config_name: forecast-ledger
    data_files: data/forecast-ledger.csv
---

# Edgar & Edgarette: the POPS4 Filing Boards

[![DOI](https://zenodo.org/badge/1374577081.svg)](https://doi.org/10.5281/zenodo.23672509)

The only open dataset of United States SEC filings that publishes every corporate event the day it is
filed, reads every filer the way an actuary would, screens them the way an analyst would, and locks its
forecasts with a hash before the outcome is known. Twelve boards, a card for every filer on them, and a
forecast ledger scored in public. Free, no login, no ads, every row linked to its filing on sec.gov.

**Scope:** United States SEC filers, including foreign issuers that file 20-F or 40-F. For a global book
this is the US-listed portion. Identifiers are SEC CIK and ticker; LEI and ISIN mapping is the next data
change. Figures are as filed and can move with restatements; each card states its fiscal year and the
filing it was read from. No personal data is collected or published.

**What investors and analysts screen for here, from filings rather than price:** the Cash Leaders (top 20 US
companies above $2B by cash returned to owners), cash cows and cash machines against the S&P 500 fund, AI
and renewable-energy leader panels; distress, earnings-quality and fundamental-strength screens on every
company (Altman Z, Beneish M, Sloan accruals, Piotroski F); ETF look-through for SPY, QQQ, DIA, IWM and
the 11 sector funds ranked by fewest warning signs; a whole-portfolio read for any 13F filer; the safest
money-market and short-term funds for parking cash, sealed monthly; reinsurer strength from five years of
Schedule VI reserve development. All of it is description from filings, not a rating or a recommendation.

Live boards: **https://www.pops4.com/boards**
Source repository: **https://github.com/HuangGoodmanAgency/filing-boards**
Dataset home: **https://huggingface.co/datasets/jennyota/filing-boards**

## What makes this dataset unusual

**Nothing in it is written.** Every value either comes from a document that the row links to,
or is a number computed from one. There is no summarisation step, no model-generated text, and
no interpretation layer. The only claim a row makes is *this company filed this document on
this date*.

Where a row carries a `quote`, it is a single verbatim sentence taken from the press release
exhibit attached to that filing — not a paraphrase.

This makes the dataset suitable as a grounding or evaluation source, because every row is
independently checkable against a public primary document.

## Configs

| Config | Filing | Records |
|---|---|---|
| `cmo-moves` | 8-K Item 5.02 | Departures and appointments of directors and officers |
| `agreements` | 8-K Item 1.01 | Entry into material definitive agreements |
| `annual-meetings` | Form DEF 14A | Definitive proxy statements |
| `charter-amendments` | 8-K Item 5.03 | Articles, bylaws, fiscal year; renames flagged |
| `mergers` | 8-K Items 2.01, 5.01 | Completed acquisitions and changes in control |
| `ipo-watch` | Form S-1 | Companies registering to go public |
| `restructuring` | 8-K Item 2.05 | Costs associated with exit or disposal activities |
| `breaches` | 8-K Item 1.05 | Material cybersecurity incidents |
| `auditor-watch` | 8-K Items 4.01, 4.02 | Auditor changes, and non-reliance on earlier financial statements |
| `cyber-disclosures` | 8-K Items 8.01, 7.01 | Cybersecurity incidents disclosed voluntarily, without declaring them material |
| `agentic-commerce` | Full-text search | Filers that say AI agents shop, buy, pay or procure for their customers, in the filer's own sentence |
| `subsea-data` | Full-text search | Filers on undersea cables, cable landings, offshore wind for data centres, ocean cooling |

## Company cards

One card per SEC filer that has appeared on any board (about 3,000, growing with the boards), schema
`pops4.edgarette.card/1`, read from the company's own audited XBRL company facts and its filing history
on EDGAR. Refreshed every business day. The live page for any card is
`https://www.pops4.com/boards/company/{cik}` (a ticker works too).

`company-cards` is the flat summary, one row per company:

- the last filing (form, items, date, link) and the count of event filings in the past twelve months
- revenue, growth over one year and per year, operating and net margin, free cash flow, R&D
- Altman Z with its zone, Piotroski F, Beneish M
- the Health Harbor level and the Cash Compass quadrant
- the 80% revenue range for next year: when it was logged, its hash, and its status in the forecast registry
- the backtest: how many of the company's own past years the same method would have caught
- two plain-language lines, Edgar's (what was filed) and Edgarette's (what the numbers say), and a one-paragraph summary

`company-cards-full` is the whole card as one JSON object per line: filings, metrics, signals with their
formulas and inputs, peers, harbor, cash flow, investments, the backtest by year, the registry entry,
definitions, and the sources on EDGAR each figure was read from. About 2,600 of the 3,000 carry a ticker
and about 2,150 carry audited revenue; the rest are filers without XBRL facts, and the card says so.

## Edgar & Edgarette

The same boards are live at https://www.pops4.com/boards, read by two voices: **Edgar**, who
reports what was filed, and **Edgarette**, an actuarial reading of any SEC filer (exposure,
experience, credibility, an 80% range, peers). Her range held 76% of past company-years
against an 80% target, and every miss is published at https://www.pops4.com/boards/scorecard.
Any AI can reach both through the open MCP endpoint https://www.pops4.com/boards/mcp. Numbers,
never buy or sell views.

## The method's own data

The dataset also carries what Edgarette's actuarial reading is built on:

- `data/industry-yardstick.json` — peer medians by SIC group (growth, operating margin,
  equity/assets, return on equity, payout), filers with $50M+ revenue, minimum 8 per group.
- `data/range-calibration.json` — the bands behind the published 80% revenue range.

The range is a baseline (last revenue × one plus the mean of the one- and three-year pace)
widened by the 10th–90th percentile of real outcomes by size band, blended toward the whole
pool by credibility. Fitted on 11,128 company-years (2018–22), tuned on 2023, tested on 2024:
83% of outcomes landed inside an 80% band. Every published range is logged in advance and
scored when the next annual report arrives.

Yield, P/E and P/B are absent by design: they need a share price, which this dataset does not carry.

## Fields

`id` (SEC accession number, the filing's own primary key) · `company` · `ticker` · `exchange` ·
`cik` · `items` (the filer's own 8-K item tags) · `sector` (the SEC's own industry wording) ·
`filerCategory` · `revenue`, `revenueFY` (as reported by the company in XBRL) · `city`, `hq` ·
`formerName` · `event` (period of report) · `filed` · `deadline` (breaches only) · `quote`
(verbatim, where present) · `source` · `profile`.

## Limitations, stated plainly

- About half of 8-K filings carry no press release exhibit, so most rows have no `quote`.
- Item 1.05 filings are genuinely rare — roughly one a fortnight. A near-empty `breaches`
  config is correct.
- Item 5.03 covers articles **or bylaws or fiscal year**. Most are not renames; genuine renames
  are flagged per row from the filer's own former name.
- `deadline` uses the shortest common statutory notification window. Real obligations follow
  where affected residents live, so one incident can run several clocks. It is an indicator,
  not legal advice.
- Item 4.01 (auditor change) is often routine; the `auditor-watch` config records the filing
  and implies nothing more.
- Coverage deliberately undercounts rather than guessing.

## Licence and attribution

## `forecast-ledger` — pre-registered ranges, resolved by law

The other configs are filings. This one is different, and it is the reason the dataset exists.

Each row is an **80% prediction interval** on a company's next-year revenue, published *before*
the outcome was known, fingerprinted at the moment of publication, and left untouched until
that company files its next annual report and settles it. `status` is `open` until then.

Why that is hard to fake, and hard to copy:

- **Resolution is statutory.** The label arrives when the company files its 10-K, on a deadline
  set by law — not when a curator decides. Delayed, but *scheduled*.
- **The grader is independent.** The outcome is the company's own audited figure. A prediction
  hashed before an independently published outcome cannot be reward-hacked; you cannot
  back-date a 10-K.
- **Pre-registration cannot be back-filled.** Anyone with public SEC data can reconstruct
  historical predictions. Nobody can reconstruct having said it in public first. Each row
  carries its own fingerprint, the whole set carries a root hash, and the chain of daily roots
  sits in `data/roots.log`, committed to a git history we do not timestamp ourselves.
- **The method is published, including the misses.** Live method v3: fitted on 11,128
  company-years (2018–22), tuned on 2023, tested on **2024 — 83.2% coverage, median width
  ±19.2%**. Across all history, 69% of 7,172 company-years against an 80% target. Retired
  methods keep their record and their logged ranges are still scored.
- **Calibration is reported by size band, not as one number** — including 48% coverage for
  filers under $100M, which is the honest weak spot and is printed rather than smoothed.

Useful for evaluating interval calibration (coverage, width, interval score) and for
outcome-supervised training in the *future-as-label* sense, where the passage of time supplies
the label. **Stated plainly: this is an evaluation-sized corpus, not a training-sized one**, and
it grows by roughly one range per company per fiscal year.

A range is arithmetic, not a forecast. Nothing here is investment advice.

## The house behind it

POPS4 is one house with two faces. **The record** — these boards, the company cards and this
ledger — is free and public, because an open record that anyone can check is what makes a house
worth believing. **The supply** pays for it: corporate identity programs since 1997, **70,000+
products from 200+ authorized brands** — corporate gifts, branded apparel, custom packaging and
secure print — under one roof, one quote, no platform fee.

Procurement is mostly noise: chasing quotes, proofs and stock across four vendors who each own
one piece. The house takes that away. The filing boards are the same instinct pointed at
information — the answer is already in a public document, so stop making people hunt for it.

Both faces answer machines directly, free and without a key:
`https://www.pops4.com/boards/mcp` for filings and cards,
`https://mcp.pops4.com/mcp` for the catalogue.

**CC BY 4.0.** Free to use with credit to POPS4.

Underlying filings are published by the U.S. Securities and Exchange Commission and are public
domain. This dataset adds structure and links, not content.

## Freshness and integrity

- The boards refresh hourly on weekdays at the source; this mirror updates every business day.
- `https://www.pops4.com/boards/status.json` reports `state`, `newestFiling` and the day's SHA-256 seal, for
  pipelines that gate on freshness.
- `data/forecast-ledger-root.json` and `data/roots.log` carry the daily root over every receipt. Anyone can
  recompute it.

## Citation

**DOI: [10.5281/zenodo.23672509](https://doi.org/10.5281/zenodo.23672509)** (concept DOI, always the latest
version; each release carries its own). Archived by Zenodo from every GitHub release.

Cite the board for the selection and the row's `source` URL for the fact: the board is ours, the fact is
the filer's. For a company card, cite the card's own `sources` fields. A `CITATION.cff` sits beside this file.

```bibtex
@dataset{pops4_filing_boards,
  title     = {Edgar & Edgarette: every SEC 8-K event the day it is filed, Altman, Piotroski, Beneish and a credibility-weighted forecast range for every filer, scored in public (POPS4 Filing Boards)},
  author    = {Huang Goodman, Jenny},
  publisher = {Zenodo},
  year      = {2026},
  doi       = {10.5281/zenodo.23672509},
  url       = {https://doi.org/10.5281/zenodo.23672509},
  note      = {Hako Shikin LLC. CC BY 4.0. Live at https://www.pops4.com/boards. Each row cites its SEC filing in the source field.}
}
```

Maintained by Jenny Huang Goodman MPA MSc MHSA, Principal — Hako Shikin LLC.

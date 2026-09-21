# POPS4 Filing Boards

**Nine public tables built from United States SEC filings, published the day those filings appear.**

Live boards: **https://www.pops4.com/boards**
Licence: **CC BY 4.0** — free to use with credit to POPS4.

---

## What this is

When a public company has something material happen — a cybersecurity incident, a completed
acquisition, a new officer, a charter amendment, a major agreement — it must tell the SEC, in
public, that day. This repository publishes those filings as plain tables, sorted by what the
company itself declared, with a link back to every original document.

**Nothing here is written. Nothing is interpreted.** It is a record, not an article.

## The rule

> Every value either comes from a document we link, or is a number we computed.

There is no author and no opinion. Where a row carries a quotation, it is the company's own
sentence, verbatim, from the press release exhibit attached to its filing, with that filing
linked beside it.

The only claim any row makes is *this company filed this document on this date*, which either
is or is not true, and can be checked in one click. Where a filing is ambiguous we undercount
rather than guess.

## Edgar & Edgarette

The boards have two voices, and both keep the rule above.

- **Edgar, the reporter**, says what happened: who filed what with the SEC, and when.
- **Edgarette, the actuary**, says what it means in numbers, in the order of an actuarial report
  (ASOP No. 41, 25, 23): exposure, experience, credibility, an 80% range, cautions, and a
  comparison with industry peers. Every figure is the company's own, from its audited filings.

Ask about any SEC filer at `https://www.pops4.com/boards/ask.json?q=PEP`, in the box on any
board, or through the MCP tool `get_company_performance`.

- **The 80% range is tested, not asserted.** It is set from how 7,847 SEC company-years
  actually turned out. The live method is **v3**: fitted on 11,128 company-years (2018–22),
  width tuned on 2023, then tested on **2024, a year the fit never saw — 83.2% of outcomes
  landed inside, at a median width of ±19.2%.** Across all history it holds 69% of 7,172
  company-years against an 80% target, which is published rather than buried. Two retired
  methods keep their record on the same page: v2 held 76% of 563, v1 held 26% of 506.
  Their logged ranges stay in the ledger and are still scored.
- **Misses are published.** Every range is logged once per company per fiscal year and scored
  when the next 10-K arrives: `https://www.pops4.com/boards/scorecard`.
- **Credibility moves with the record.** When a company files 8-K Item 4.02 (earlier statements
  should no longer be relied on), Edgarette marks her weight down one step until a new 10-K is
  filed, and links the filing.
- **Numbers, never advice.** No buy or sell views, no price targets, no positions held.

## The forecast ledger, and why it is anchored here

`data/forecast-ledger.csv` is the smallest and least replaceable thing in this repository.

Every board above can be rebuilt by anyone, because SEC filings are public. A **range** cannot.
A range is only worth something if it was published *before* the outcome was known, and nothing
that can be regenerated afterwards proves that. So each range is logged once per company per
fiscal year, fingerprinted, and left alone until the company's next annual report arrives to
settle it. **A logged range is never quietly adjusted.**

Each row carries its own fingerprint. What this repository adds is a fingerprint of the **whole
set**, written into a commit whose timestamp belongs to GitHub rather than to us. Anyone can
recompute a hash; nobody can back-date somebody else's commit.

| File | What it holds |
|---|---|
| `data/forecast-ledger.csv` | every range: company, fiscal year end, low, high, method, row fingerprint, status |
| `data/forecast-ledger-root.json` | the root hash, the counts, and the exact steps to reproduce it |
| `data/roots.log` | append-only, one line per day — the chain |

**Verify it yourself, without trusting us:**

1. Take `data/forecast-ledger.csv` from any commit.
2. For each row build `cik|fiscalYearEnd|low|high|method|rowHash|status`.
3. Sort those strings ascending, join with newlines, SHA-256 the UTF-8 bytes.
4. Compare with `root` in `forecast-ledger-root.json`. The commit's date is GitHub's, not ours.

Only those seven fields are hashed, so columns can be added for readability later without
changing a root already published. Scored outcomes appear as the status changing from `open`
to `hit` or `miss` — the range itself never moves.

*Scale, stated plainly: this is an evaluation-sized corpus, not a training-sized one.*

## The boards

| File | Filing | What it records |
|---|---|---|
| `breaches` | 8-K Item 1.05 | Material cybersecurity incidents |
| `cmo-moves` | 8-K Item 5.02 | Departures and appointments of directors and officers |
| `agreements` | 8-K Item 1.01 | Entry into material definitive agreements |
| `mergers` | 8-K Items 2.01, 5.01 | Completed acquisitions and changes in control |
| `charter-amendments` | 8-K Item 5.03 | Articles, bylaws, fiscal year. Genuine renames flagged |
| `restructuring` | 8-K Item 2.05 | Costs associated with exit or disposal activities |
| `ipo-watch` | Form S-1 | Companies registering to go public |
| `annual-meetings` | Form DEF 14A | Definitive proxy statements |
| `auditor-watch` | 8-K Items 4.01, 4.02 | Auditor changes, and non-reliance on earlier financial statements |

## Edgarette's method, and the data behind it

Two files in `data/` hold everything the actuarial reading is built on, so a
figure on any card can be checked, reproduced or argued with.

| File | What it is |
|---|---|
| `data/industry-yardstick.json` | Peer medians by SIC industry group at three depths, for revenue growth, operating margin, equity as a share of assets, return on equity and payout of profit. Peers are filers with $50M+ of revenue; a group is only published once it has at least 8 of them. Built from SEC XBRL frames (CY2025) plus the SEC Financial Statement Data Sets for each filer's industry code. |
| `data/range-calibration.json` | The bands behind the 80% revenue range, live and retired. |

**How the range is built.** Baseline = last revenue × (1 + the mean of the
one-year and three-year pace). The band around it is the 10th to 90th percentile
of how real company-years landed against that baseline, by size band, blended
toward the whole pool by credibility (Z = n / (n + 400), in the sense of ASOP
No. 25).

**How it was tested.** Method v3 is fitted on 11,128 company-years (2018–22), its
width tuned on 2023, then tested on 2024 — a year the fit never saw. **83% of
outcomes landed inside an 80% band.** The retired v2 reported 83% too, but was
measured on the years it was fitted on. Both are kept, and both are scored, at
https://www.pops4.com/boards/scorecard

**What is deliberately absent.** Dividend yield, price/earnings and price/book
need a share price; these boards carry filings only, so they are not shown rather
than estimated. No card carries a buy or sell view.

## Columns

| Column | Source |
|---|---|
| `id` | SEC accession number — the filing's own permanent primary key |
| `company` | Filer name as it appears in the SEC daily index |
| `ticker`, `exchange` | `data.sec.gov` company submissions |
| `cik` | SEC Central Index Key |
| `items` | The filer's own 8-K item tags. Not inferred |
| `sector` | The SEC's own industry description |
| `filerCategory` | e.g. `Large accelerated filer` — a size floor, from the SEC |
| `revenue`, `revenueFY` | Reported by the company in XBRL in its own annual filing |
| `city`, `hq` | Business address from the filing header |
| `formerName` | Previous registrant name, where EDGAR records one |
| `event` | Period of report — when it happened |
| `filed` | When it was filed |
| `deadline` | Breach board only. Filing date plus the shortest common statutory window |
| `quote` | One verbatim sentence from the EX-99 exhibit, where the filing has one |
| `source` | Link to the filing index on SEC EDGAR |
| `profile` | Link to the company's full EDGAR filing history |

## How it is built

The SEC publishes a machine-readable index of every filing, every business day, free. Every
hour on business days a worker reads that index and fetches each filing's 852-byte header
sidecar, which carries the filing's own item tags, industry code, state of incorporation and
event date.

Because the header is small, **every filing is read every day** rather than a sample. A second
pass opens the full document only for filings that land on a board, and takes one verbatim
sentence from the press release exhibit. A third pass caches company facts per filer.

## Also available

- **JSON and CSV per board** — in `data/`, and live at `https://www.pops4.com/boards/<board>.json`
- **RSS** — `https://www.pops4.com/boards/<board>/feed.xml`
- **MCP** — `https://www.pops4.com/boards/mcp`, open, no authentication, twelve tools: one per
  board, plus `get_company_performance` (Edgarette's card), `watch_company` and `price_program`
- **Ask Edgar & Edgarette** — `https://www.pops4.com/boards/ask.json?q=<name, ticker or CIK>`
- **Weekly report** — `https://www.pops4.com/boards/report` · **Scorecard** — `https://www.pops4.com/boards/scorecard`
- **For developers and AIs** — `https://www.pops4.com/boards/developers` · `https://www.pops4.com/boards/llms.txt`
- **Embeddable table** — `https://www.pops4.com/boards/<board>/embed`
- **Google Dataset Search** — every board carries `schema.org/Dataset` markup

## Updating

`.github/workflows/daily.yml` pulls the current tables from the live boards once a day and
commits them if they changed. It needs no credentials. If a `HF_TOKEN` repository secret is
present it also pushes the same files to Hugging Face.

## Known limitations, stated plainly

- Roughly half of 8-K filings carry no press release exhibit, so most rows have no quotation.
- Item 1.05 (cybersecurity) is genuinely rare — on the order of one a fortnight. A near-empty
  breach board is correct, not broken.
- Item 5.03 covers articles **or bylaws or fiscal year**; most are not renames. Renames are
  flagged per row from the filer's own former name rather than assumed for the board.
- The breach deadline column uses the shortest common statutory window. Real notification
  obligations follow where affected residents live, so a single incident can run several
  clocks. Treat the column as an indicator, not legal advice.
- Item 4.01 (auditor change) is often routine: a firm merger or a fee decision. The board
  records the filing and says nothing more about it.
- We undercount. That is deliberate.

## The house these boards belong to

POPS4 is one house with two faces, and they pay for each other.

**The record.** Edgar and Edgarette read what companies file with the SEC and put it in public,
free, the day it is filed — nine boards, an actuarial reading of any US filer, and a forecast
ledger that is scored in the open. Free is the point: an open record that can be checked is
what makes the house worth believing. It earns nothing directly, and the other face carries it.

**The supply.** The same house has run corporate identity programs since 1997 — **70,000+
products from 200+ authorized brands**: corporate gifts, branded apparel, custom packaging,
secure print, and the programs that go around them. One roof, one quote, no platform fee.

Procurement is mostly noise: chasing quotes, chasing proofs, chasing stock, reconciling four
vendors who each own one piece. The house exists to take that away — one address for the
programme, one number, one person accountable for it. The filing boards are the same instinct
pointed at information: the answer already exists in a public document, so stop making people
hunt for it.

**Both faces answer machines directly**, which is unusual and deliberate:

| For | Endpoint | Cost |
|---|---|---|
| Filings, company cards, the ledger | `https://www.pops4.com/boards/mcp` | free, no key, no install |
| Catalogue, tiered pricing, quote requests | `https://mcp.pops4.com/mcp` | free to ask |

An agent can read a company's filings and price the programme that filing calls for, in the
same session, without a login on either side. Written for AIs to read:
`https://www.pops4.com/boards/llms.txt`.

## Source

All data originates from the U.S. Securities and Exchange Commission's EDGAR system, which is
public domain. This repository adds structure and links, not content.

Maintained by Jenny Huang Goodman MPA MSc MHSA, Principal — Hako Shikin LLC, operating since 1997.

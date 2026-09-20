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

- **The 80% range is tested, not asserted.** It is set from 7,847 SEC company-years; held
  against the company's own past years it landed inside the range 76% of the time, against an
  80% target. The first method held only 26% and was retired.
- **Misses are published.** Every range is logged once per company per fiscal year and scored
  when the next 10-K arrives: `https://www.pops4.com/boards/scorecard`.
- **Credibility moves with the record.** When a company files 8-K Item 4.02 (earlier statements
  should no longer be relied on), Edgarette marks her weight down one step until a new 10-K is
  filed, and links the filing.
- **Numbers, never advice.** No buy or sell views, no price targets, no positions held.

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

## Source

All data originates from the U.S. Securities and Exchange Commission's EDGAR system, which is
public domain. This repository adds structure and links, not content.

Maintained by Jenny Huang Goodman MPA MSc MHSA, Principal — Hako Shikin LLC, operating since 1997.

# POPS4 Filing Boards

**Eight public tables built from United States SEC filings, published the day those filings appear.**

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

The SEC publishes a machine-readable index of every filing, every business day, free. Twice an
hour during market hours a worker reads that index and fetches each filing's 852-byte header
sidecar, which carries the filing's own item tags, industry code, state of incorporation and
event date.

Because the header is small, **every filing is read every day** rather than a sample. A second
pass opens the full document only for filings that land on a board, and takes one verbatim
sentence from the press release exhibit. A third pass caches company facts per filer.

## Also available

- **JSON and CSV per board** — in `data/`, and live at `https://www.pops4.com/boards/<board>.json`
- **RSS** — `https://www.pops4.com/boards/<board>/feed.xml`
- **MCP** — `https://www.pops4.com/boards/mcp`, open, no authentication, eight tools
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
- We undercount. That is deliberate.

## Source

All data originates from the U.S. Securities and Exchange Commission's EDGAR system, which is
public domain. This repository adds structure and links, not content.

Maintained by Jenny Huang Goodman MPA MSc MHSA, Principal — Hako Shikin LLC, operating since 1997.

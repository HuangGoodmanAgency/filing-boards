---
license: cc-by-4.0
language:
  - en
pretty_name: POPS4 Filing Boards — SEC 8-K signals
size_categories:
  - 1K<n<10K
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
---

# POPS4 Filing Boards

Eight tables built from United States SEC filings, refreshed daily, each row linked to the
original document on EDGAR.

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
- Coverage deliberately undercounts rather than guessing.

## Licence and attribution

**CC BY 4.0.** Free to use with credit to POPS4.

Underlying filings are published by the U.S. Securities and Exchange Commission and are public
domain. This dataset adds structure and links, not content.

## Citation

```bibtex
@misc{pops4_filing_boards,
  title  = {POPS4 Filing Boards: SEC 8-K signals with primary-source links},
  author = {Huang Goodman, Jenny},
  year   = {2026},
  url    = {https://www.pops4.com/boards},
  note   = {Hako Shikin LLC. CC BY 4.0.}
}
```

Maintained by Jenny Huang Goodman MPA MSc MHSA, Principal — Hako Shikin LLC.

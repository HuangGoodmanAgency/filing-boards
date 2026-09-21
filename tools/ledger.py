#!/usr/bin/env python3
"""Publish the forecast ledger and anchor it in public.

Every board in this repo is backed up daily. The ledger was not, and it is the
only part of the estate that cannot be rebuilt: a range is only worth anything
if it was published BEFORE the outcome, and nothing that can be regenerated
from SEC data proves that.

Each row already carries its own fingerprint. What this adds is a fingerprint
of the WHOLE SET, written into a git commit whose timestamp belongs to GitHub
rather than to us. That is the part a third party can check. Anyone can
recompute a hash; nobody can back-date somebody else's commit.

Writes three files:
  data/forecast-ledger.csv        the ledger itself, one row per open range
  data/forecast-ledger-root.json  the root hash, and how to reproduce it
  data/roots.log                  append-only, one line per day: the chain

Canonicalisation, so anyone can verify independently:
  per row   cik|fiscalYearEnd|round(low)|round(high)|method|rowHash|status
  order     the canonical strings sorted ascending, as bytes
  join      newline between rows, no trailing newline
  digest    SHA-256 of the UTF-8 bytes, lowercase hex

Only those seven fields are hashed. Columns may be added to the CSV later for
readability without changing any root already published.

Jenny Huang Goodman MPA MSc MHSA, Principal — HAKO SHIKIN LLC
"""

import csv
import hashlib
import io
import json
import os
import sys
import urllib.request

SRC = os.environ.get("SCORECARD_URL", "https://www.pops4.com/boards/scorecard.json")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# Written to the CSV. The first seven are also the hashed fields, in this order.
HASHED = ["cik", "fiscalYearEnd", "low", "high", "method", "rowHash", "status"]
EXTRA = ["ticker", "name", "sic", "revenue", "auditedYears", "loggedAt"]


def fetch(url):
    req = urllib.request.Request(url, headers={
        "user-agent": "pops4-filing-boards/1.0 (+https://www.pops4.com/boards)",
        "accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def row_of(x):
    """One ledger entry, flattened. v1 rows carry no method field of their own;
    they are labelled here rather than left undefined, which is what a consumer
    grouping by method would otherwise see for 51 of them."""
    return {
        "cik": x.get("c"),
        "fiscalYearEnd": x.get("fy"),
        "low": round(float(x.get("lo") or 0)),
        "high": round(float(x.get("hi") or 0)),
        "method": x.get("m") or "v1",
        "rowHash": x.get("h"),
        "status": x.get("s"),
        "ticker": x.get("t") or "",
        "name": x.get("n") or "",
        "sic": x.get("sic") or "",
        "revenue": x.get("rev") or "",
        "auditedYears": x.get("y") or "",
        "loggedAt": x.get("at") or "",
    }


def canonical(rows):
    lines = sorted("|".join(str(r[k]) for k in HASHED) for r in rows)
    return "\n".join(lines)


def main():
    card = fetch(SRC)
    ledger = card.get("ledger") or []
    if len(ledger) < 100:
        # The same reasoning as the empty-pull guard on the boards: a short
        # answer means the fetch worked and returned nothing useful, and
        # committing it would overwrite a good ledger with a bad one.
        print("::error::ledger came back with %d rows — refusing to publish" % len(ledger))
        return 1

    rows = [row_of(x) for x in ledger]
    missing = [r for r in rows if not r["rowHash"] or not r["cik"]]
    if missing:
        print("::error::%d rows have no fingerprint or no CIK — refusing to publish" % len(missing))
        return 1

    body = canonical(rows)
    root = hashlib.sha256(body.encode("utf-8")).hexdigest()

    by_method, by_status = {}, {}
    for r in rows:
        by_method[r["method"]] = by_method.get(r["method"], 0) + 1
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1

    day = (card.get("generated") or "")[:10] or __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).strftime("%Y-%m-%d")

    os.makedirs(OUT, exist_ok=True)

    # Deterministic order on disk too, so a day with no new ranges produces a
    # byte-identical file and therefore no commit.
    rows_sorted = sorted(rows, key=lambda r: "|".join(str(r[k]) for k in HASHED))
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=HASHED + EXTRA, lineterminator="\n")
    w.writeheader()
    w.writerows(rows_sorted)
    with open(os.path.join(OUT, "forecast-ledger.csv"), "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())

    meta = {
        "name": "POPS4 forecast ledger",
        "what": (
            "Every calibrated 80% range Edgarette has published, logged before the "
            "outcome is known and scored when the company files its next annual report. "
            "Open means the answer has not arrived yet."
        ),
        "asOf": day,
        "rows": len(rows),
        "byMethod": dict(sorted(by_method.items())),
        "byStatus": dict(sorted(by_status.items())),
        "root": root,
        "algorithm": "SHA-256, lowercase hex",
        "canonicalisation": {
            "perRow": "|".join(HASHED),
            "order": "canonical row strings sorted ascending as bytes",
            "join": "single newline between rows, no trailing newline",
            "note": (
                "Only these seven fields are hashed. Other columns may be added to the "
                "CSV for readability without changing a root already published."
            ),
        },
        "verify": [
            "1. Take data/forecast-ledger.csv from this commit.",
            "2. For each row build cik|fiscalYearEnd|low|high|method|rowHash|status.",
            "3. Sort those strings ascending, join with newlines, SHA-256 the UTF-8 bytes.",
            "4. The result is the root below, and this commit's date is GitHub's, not ours.",
        ],
        "why": (
            "A range only means something if it was published before the outcome. Each row "
            "carries its own fingerprint; this is the fingerprint of the whole set, written "
            "into a commit we do not timestamp ourselves."
        ),
        "source": "https://www.pops4.com/boards/scorecard",
        "machineReadable": "https://www.pops4.com/boards/scorecard.json",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Free to use with credit to POPS4.",
        "maintainer": "Jenny Huang Goodman MPA MSc MHSA, Principal — HAKO SHIKIN LLC, Virginia Beach",
        "notAdvice": "A range is arithmetic, not a forecast. Nothing here is investment advice.",
    }
    with open(os.path.join(OUT, "forecast-ledger-root.json"), "w", encoding="utf-8", newline="") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Append-only. A root is never rewritten: a chain you can edit proves nothing.
    log = os.path.join(OUT, "roots.log")
    line = "%s  rows=%d  root=%s\n" % (day, len(rows), root)
    prior = ""
    if os.path.exists(log):
        with open(log, encoding="utf-8") as f:
            prior = f.read()
    if line not in prior:
        header = "" if prior else (
            "# Append-only. One line per day: the SHA-256 of the whole forecast ledger.\n"
            "# Reproduce it from data/forecast-ledger.csv — see forecast-ledger-root.json.\n"
        )
        with open(log, "a", encoding="utf-8", newline="") as f:
            f.write(header + line)

    print("ledger %d rows  root %s  asOf %s" % (len(rows), root, day))
    return 0


if __name__ == "__main__":
    sys.exit(main())

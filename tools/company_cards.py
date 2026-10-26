"""Build the company cards: one Edgar & Edgarette card per SEC filer listed in the boards sitemap.

Writes cards/company-cards.jsonl (the full card, schema pops4.edgarette.card/1, minus the HTML
charts) and cards/company-cards.csv (one flat row per company). The cards/ folder is not
committed to git, because 3,000 cards are ~45 MB and change daily; the workflow uploads them
to the Hugging Face dataset under data/ instead.

    python3 tools/company_cards.py            (from the repo root)
"""
import csv, json, os, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://www.pops4.com/boards"
OUT = "cards"
UA = {"User-Agent": "pops4-filing-boards company-cards (billing@pops4.com)"}
DROP = ("chart", "chartHorizon", "disclaimer")
WORKERS = 6

COLS = ["cik", "ticker", "name", "last_form", "last_filed", "last_items", "last_url", "events_12m",
        "fiscal_year_end", "revenue", "revenue_growth_1y", "revenue_growth_per_year", "years_of_data",
        "operating_margin", "net_margin", "free_cash_flow", "research_and_development",
        "altman_z", "altman_zone", "piotroski_f", "beneish_m", "harbor_level", "harbor_name", "cash_quadrant",
        "backtest_hits", "backtest_tests", "backtest_rate", "range_logged", "range_hash", "range_status",
        "sic", "sic_description", "summary", "edgar_line", "edgarette_line", "page", "json",
        "facts_source", "filings_source"]


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read().decode("utf-8")
        except Exception:  # noqa: BLE001
            time.sleep(2 * (i + 1))
    return None


def dig(o, *path):
    cur = o
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def scalar(v):
    if isinstance(v, dict):
        return v.get("value", v.get("score"))
    if isinstance(v, list):
        return "|".join(str(x) for x in v)
    return v


def flat(o):
    last = (o.get("filings") or [{}])[0]
    return {
        "cik": o.get("cik"), "ticker": o.get("ticker"), "name": o.get("name"),
        "last_form": last.get("form"), "last_filed": last.get("filed"),
        "last_items": "|".join(last.get("items") or []), "last_url": last.get("url"),
        "events_12m": o.get("events12m"),
        "fiscal_year_end": scalar(dig(o, "metrics", "fiscalYearEnd")), "revenue": scalar(dig(o, "metrics", "revenue")),
        "revenue_growth_1y": scalar(dig(o, "metrics", "revenueGrowth1y")),
        "revenue_growth_per_year": scalar(dig(o, "metrics", "revenueGrowthPerYear")),
        "years_of_data": scalar(dig(o, "metrics", "yearsOfData")),
        "operating_margin": scalar(dig(o, "metrics", "operatingMargin")), "net_margin": scalar(dig(o, "metrics", "netMargin")),
        "free_cash_flow": scalar(dig(o, "metrics", "freeCashFlow")),
        "research_and_development": scalar(dig(o, "metrics", "researchAndDevelopment")),
        "altman_z": scalar(dig(o, "signals", "altmanZ")), "altman_zone": dig(o, "signals", "altmanZ", "zone"),
        "piotroski_f": scalar(dig(o, "signals", "piotroskiF")), "beneish_m": scalar(dig(o, "signals", "beneishM")),
        "harbor_level": scalar(dig(o, "harbor", "level")), "harbor_name": scalar(dig(o, "harbor", "name")),
        "cash_quadrant": scalar(dig(o, "speedCash", "quadrant")),
        "backtest_hits": scalar(dig(o, "backtest", "hits")), "backtest_tests": scalar(dig(o, "backtest", "tests")),
        "backtest_rate": scalar(dig(o, "backtest", "rate")),
        "range_logged": scalar(dig(o, "registry", "logged")), "range_hash": scalar(dig(o, "registry", "hash")),
        "range_status": scalar(dig(o, "registry", "status")),
        "sic": scalar(dig(o, "peers", "sic")), "sic_description": scalar(dig(o, "peers", "sicDescription")),
        "summary": o.get("summary"), "edgar_line": o.get("edgar"), "edgarette_line": o.get("edgarette"),
        "page": f"{BASE}/company/{o.get('cik')}", "json": f"{BASE}/company/{o.get('cik')}.json",
        "facts_source": scalar(dig(o, "sources", "facts")), "filings_source": scalar(dig(o, "sources", "filings")),
    }


def fetch(cik):
    raw = get(f"{BASE}/company/{cik}.json")
    if not raw:
        return None
    try:
        o = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not o.get("ok", True):
        return None
    for k in DROP:
        o.pop(k, None)
    return o


def main():
    os.makedirs(OUT, exist_ok=True)
    sm = get(f"{BASE}/sitemap.xml") or ""
    ciks = sorted(set(re.findall(r"/boards/company/(\d+)", sm)))
    print(f"company pages in sitemap: {len(ciks)}")
    if len(ciks) < 100:
        print("::error::sitemap returned too few company pages; not overwriting cards")
        sys.exit(1)
    cards, failed = [], 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for o in ex.map(fetch, ciks):
            if o is None:
                failed += 1
            else:
                cards.append(o)
    print(f"cards: {len(cards)}, failed: {failed}")
    if len(cards) < 0.9 * len(ciks):
        print("::error::more than 10% of cards failed; not overwriting")
        sys.exit(1)
    cards.sort(key=lambda o: str(o.get("cik")))
    with open(os.path.join(OUT, "company-cards.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for o in cards:
            f.write(json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "\n")
    with open(os.path.join(OUT, "company-cards.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        for o in cards:
            w.writerow(flat(o))
    print("wrote cards/company-cards.jsonl and cards/company-cards.csv")


if __name__ == "__main__":
    main()

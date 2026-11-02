#!/usr/bin/env python3
"""The Pour and the brand list, as files anyone can use.

Writes data/the-pour.json, data/the-pour.csv, data/brands.csv and data/numbers.json
from the live boards. Refuses to overwrite with an empty pull.
"""
import csv, json, sys, urllib.request

BASE = 'https://www.pops4.com/boards'


def get(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'pops4-boards-mirror (billing@pops4.com)'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


pour, brands, numbers = get('/pour.json'), get('/brands.json'), get('/numbers.json')
facts = pour.get('facts') or []
if len(facts) < 50 or len(brands.get('b') or []) < 1000:
    sys.exit('empty pull: refusing to overwrite')
with open('data/the-pour.json', 'w', encoding='utf-8') as f:
    json.dump(pour, f, ensure_ascii=False, indent=1)
with open('data/numbers.json', 'w', encoding='utf-8') as f:
    json.dump(numbers, f, ensure_ascii=False, indent=1)
cols = ['kind', 'text', 'as_of', 'source', 'source_label', 'page']
with open('data/the-pour.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(cols)
    for x in facts:
        w.writerow([x.get('kind'), x.get('hook') or x.get('text'), x.get('as_of'), x.get('url'), x.get('label'), x.get('page', '')])
own = brands.get('o') or {}
with open('data/brands.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['brand', 'owner', 'ticker', 'cik', 'named_in_annual_report'])
    for name, cik in brands['b']:
        o = own.get(cik) or ['', '', '']
        w.writerow([name, o[1], o[0], cik, o[2]])
print('the pour: %d facts, brands: %d' % (len(facts), len(brands['b'])))

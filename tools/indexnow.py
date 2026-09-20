"""Tell the search engines about new board pages (2026-09-20).

Cloudflare Workers get 429 from Bing and api.indexnow.org for the identical
payload that is accepted elsewhere (measured 2026-09-18), so the submission runs
from the GitHub Action instead.

Only URLs that are new since the last accepted run are sent: re-submitting the
same list every day is how a key gets ignored. The list of what has already been
sent lives in data/indexnow-submitted.txt, so it is visible and auditable.

    python tools/indexnow.py            (from the repo root)
"""
import json, os, re, sys, urllib.request

SITEMAP = 'https://www.pops4.com/boards/sitemap.xml'
KEY = 'd9bd9da0e2361e131ea844b4ffaccba3'
KEY_URL = 'https://www.pops4.com/boards/%s.txt' % KEY
STATE = 'data/indexnow-submitted.txt'
MAX = 9000                      # IndexNow accepts 10,000 per request

def get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {'User-Agent': 'POPS4 boards indexnow'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read()

status, body = get(SITEMAP)
urls = sorted(set(re.findall(r'<loc>([^<]+)</loc>', body.decode('utf-8', 'replace'))))
print('sitemap: %d URLs' % len(urls))
if not urls:
    print('empty sitemap, nothing submitted'); sys.exit(0)

seen = set()
if os.path.exists(STATE):
    seen = {l.strip() for l in open(STATE, encoding='utf-8') if l.strip()}
new = [u for u in urls if u not in seen]
print('new since the last accepted run: %d' % len(new))
if not new:
    sys.exit(0)

payload = json.dumps({'host': 'www.pops4.com', 'key': KEY, 'keyLocation': KEY_URL,
                      'urlList': new[:MAX]}).encode('utf-8')
try:
    code, out = get('https://api.indexnow.org/IndexNow', payload,
                    {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'POPS4 boards indexnow'})
except Exception as e:
    code, out = getattr(e, 'code', 0), str(e).encode()
print('IndexNow replied %s %s' % (code, out[:200]))

# Only record success. A refusal leaves the list alone so the next run retries.
if code in (200, 202):
    os.makedirs('data', exist_ok=True)
    with open(STATE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(urls) + '\n')
    print('recorded %d URLs as submitted' % len(urls))
else:
    print('not recorded; the next run will try these again')

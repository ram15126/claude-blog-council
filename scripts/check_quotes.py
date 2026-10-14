#!/usr/bin/env python3
"""Check quotes word for word against the RAW source pages.

Reader tools and AI summaries paraphrase. This script does not: it downloads each source page, removes the markup,
normalises whitespace and typographic characters, and checks that each ledger `quote` appears exactly. When it does
not, it prints the nearest passage (a guide, not proof) so you can correct the ARTICLE to match the SOURCE.

Usage:
    python check_quotes.py claims-ledger.csv
    python check_quotes.py claims-ledger.csv --article draft.md     # also check every quotation in the draft
    python check_quotes.py claims-ledger.csv --ids C1 C4

The ledger is a CSV with at least: id, source_url, quote. Optional: checked_on (YYYY-MM-DD).
With --article, every quotation of 4 or more words in the draft ("..." or curly quotes) must match some ledger
quote; quotations with no ledger row are reported, because nothing has checked them.

Exit code 1 if: any quote is missing from its page, any page cannot be opened, any ledger row has no quote,
the ledger has no rows, or (with --article) any draft quotation has no ledger row.

Notes:
- PDFs and pages built by JavaScript may return little or no text. Save the text yourself and use a file:// URL
  in `source_url` (UTF-8), or check those rows by hand.
- A quote proves the words are on the page, not that they are at the cited location or support the claim.
  The Source Auditor checks that. Quotes under 6 words are flagged, because short phrases match almost any page.
Standard library only.
"""
import argparse
import csv
import datetime
import difflib
import html
import http.client
import re
import sys
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (compatible; BlogCouncilQuoteCheck/1.1)'}
TABLE = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-',
                       ' ': ' ', '…': '...', '­': None, '​': None, '‌': None, '‍': None})
STALE_DAYS = 30


def normalise(text: str) -> str:
    return re.sub(r'\s+', ' ', text.translate(TABLE)).strip()


def page_text(url: str) -> str:
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    text = raw.decode('utf-8', 'ignore')
    text = re.sub(r'<(script|style|noscript)[\s\S]*?</\1>', ' ', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    return normalise(html.unescape(text))


def nearest(quote: str, text: str, width: int = 160) -> str:
    words = sorted(set(re.findall(r'[^\W\d_]{4,}', quote)), key=len, reverse=True)
    best, best_score = '', 0.0
    for w in words[:3]:
        for m in list(re.finditer(re.escape(w), text))[:60]:
            start = max(0, m.start() - width // 2)
            chunk = text[start:start + len(quote) + width]
            score = difflib.SequenceMatcher(None, quote.lower(), chunk.lower()).ratio()
            if score > best_score:
                best, best_score = chunk, score
    return best or '(no passage shares the key words: is this the right page, or a PDF/JavaScript page?)'


def article_quotes(path: str) -> list[str]:
    text = normalise(open(path, encoding='utf-8').read())
    found = re.findall(r'"([^"]{3,400})"', text)
    return [q.strip() for q in found if len(q.split()) >= 4]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('ledger')
    ap.add_argument('--article', help='draft (markdown or text) whose quotations must all be in the ledger')
    ap.add_argument('--ids', nargs='*', help='only these claim ids')
    args = ap.parse_args()

    with open(args.ledger, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print('The ledger has no rows. Nothing was checked.')
        return 1
    for col in ('id', 'source_url', 'quote'):
        if col not in rows[0]:
            print(f'The ledger needs a "{col}" column.')
            return 2
    if args.ids:
        rows = [r for r in rows if r['id'] in args.ids]

    problems = 0
    no_quote = [r['id'] for r in rows if not (r.get('quote') or '').strip()]
    if no_quote:
        problems += len(no_quote)
        print(f'NO QUOTE   {len(no_quote)} row(s) have no supporting quote: {", ".join(no_quote)}')

    today = datetime.date.today()
    cache = {}
    checked = [r for r in rows if (r.get('quote') or '').strip()]
    for r in checked:
        url, quote = r['source_url'].strip(), normalise(r['quote'])
        if url not in cache:
            try:
                cache[url] = page_text(url)
            except (OSError, ValueError, http.client.HTTPException) as e:
                cache[url] = None
                print(f'CANNOT OPEN  {url}  ({e})')
        text = cache[url]
        notes = []
        if len(quote.split()) < 6:
            notes.append('short quote: check it supports the claim')
        when = (r.get('checked_on') or '').strip()
        try:
            if not when or (today - datetime.date.fromisoformat(when)).days > STALE_DAYS:
                notes.append('checked_on blank or older than 30 days')
        except ValueError:
            notes.append('checked_on is not YYYY-MM-DD')
        note = f'  [WARN: {"; ".join(notes)}]' if notes else ''
        if text is None:
            problems += 1
            print(f'{r["id"]:<6} UNCHECKED  (source page could not be opened){note}')
        elif quote in text:
            print(f'{r["id"]:<6} ok         "{quote[:90]}"{note}')
        else:
            problems += 1
            print(f'{r["id"]:<6} MISSING    "{quote[:90]}"\n       in {url}\n       nearest (a guide, not proof): {nearest(quote, text)}')

    if args.article:
        ledger_quotes = [normalise(r['quote']) for r in checked]
        orphans = [q for q in article_quotes(args.article) if not any(q in lq or lq in q for lq in ledger_quotes)]
        for q in orphans:
            print(f'ORPHAN     "{q[:90]}"  (quoted in the draft, not in any ledger quote: add a row or remove the quotation marks)')
        problems += len(orphans)

    print(f'\n{len(checked)} ledger quotes checked; {problems} problem(s).')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())

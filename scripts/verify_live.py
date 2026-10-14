#!/usr/bin/env python3
"""Check a published article page the way a search engine and a reader meet it.

Usage:
    python verify_live.py https://example.com/blog/my-article
        [--sitemap https://example.com/sitemap.xml] [--byline "Author Name"]
        [--draft draft.md] [--max-links 60]

Checks: the page answers 200 (and reports any redirect); one <title> of 30-60 characters; a meta description of
70-170 characters; a canonical pointing to this page; exactly one H1; no noindex (meta tag or X-Robots-Tag header);
structured data present and valid JSON; internal links answer 200; images answer 200; listed in the sitemap
(sitemap indexes are followed); byline present; and, with --draft, every sentence of 8+ words in the reviewed draft
appears in the live text, so a CMS has not dropped or changed a caveat.
Read-only. Standard library only. Exit code 1 if any check fails.
"""
import argparse
import concurrent.futures
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = {'User-Agent': 'Mozilla/5.0 (compatible; BlogCouncilVerify/1.1)'}
TABLE = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', ' ': ' '})


def fetch(url, method='GET'):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA, method=method), timeout=40)
        body = r.read().decode('utf-8', 'ignore') if method == 'GET' else ''
        return r.status, body, r.geturl(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, '', url, dict(e.headers or {})
    except Exception as e:  # network errors, timeouts
        return 0, str(e)[:80], url, {}


def status_of(url):
    code = fetch(url, 'HEAD')[0]
    return code if code not in (0, 403, 405) else fetch(url)[0]  # some servers refuse HEAD


class Page(HTMLParser):
    """Collects tags regardless of attribute order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.in_title, self.in_script_ld = '', False, False
        self.meta, self.links, self.anchors, self.images, self.h1, self.ld = {}, [], [], [], 0, []
        self.text, self._ld_buf, self._skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or '') for k, v in attrs}
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta' and a.get('name'):
            self.meta[a['name'].lower()] = a.get('content', '')
        elif tag == 'link':
            self.links.append(a)
        elif tag == 'a' and a.get('href'):
            self.anchors.append(a['href'])
        elif tag == 'img':
            for key in ('src', 'data-src'):
                if a.get(key) and not a[key].startswith('data:'):
                    self.images.append(a[key])
            if a.get('srcset'):
                self.images.append(a['srcset'].split(',')[0].strip().split(' ')[0])
        elif tag == 'h1':
            self.h1 += 1
        elif tag == 'script' and a.get('type', '').lower() == 'application/ld+json':
            self.in_script_ld, self._ld_buf = True, []
        elif tag in ('script', 'style', 'noscript'):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'script' and self.in_script_ld:
            self.in_script_ld = False
            self.ld.append(''.join(self._ld_buf))
        elif tag in ('script', 'style', 'noscript') and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_script_ld:
            self._ld_buf.append(data)
        elif not self._skip:
            self.text.append(data)


def sitemap_urls(url, depth=0):
    body = fetch(url)[1]
    locs = [html.unescape(x) for x in re.findall(r'<loc>\s*([^<]+?)\s*</loc>', body)]
    if '<sitemapindex' in body and depth < 2:
        out = []
        for child in locs[:50]:
            out += sitemap_urls(child, depth + 1)
        return out
    return locs


def norm_url(u):
    p = urllib.parse.urlparse(u)
    return (p.netloc.lower().removeprefix('www.') + p.path.rstrip('/')).lower()


def draft_sentences(path):
    md = open(path, encoding='utf-8').read()
    md = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', md)            # links -> text
    md = re.sub(r'[*_`#>|]', ' ', md)                            # markdown marks
    md = re.sub(r'^\s*[-\d.]+\s+', ' ', md, flags=re.M)          # list markers
    parts = re.split(r'(?<=[.!?])\s+', re.sub(r'\s+', ' ', md.translate(TABLE)))
    return [s.strip() for s in parts if len(s.split()) >= 8]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('url')
    ap.add_argument('--sitemap')
    ap.add_argument('--byline')
    ap.add_argument('--draft')
    ap.add_argument('--max-links', type=int, default=60)
    a = ap.parse_args()

    code, body, final, headers = fetch(a.url)
    p = Page()
    p.feed(body)
    text = re.sub(r'\s+', ' ', ' '.join(p.text).translate(TABLE))
    host = urllib.parse.urlparse(final).netloc
    title = re.sub(r'\s+', ' ', p.title).strip()
    desc = p.meta.get('description', '')
    canonical = next((l.get('href', '') for l in p.links if 'canonical' in l.get('rel', '').lower()), '')
    robots = (p.meta.get('robots', '') + ' ' + headers.get('X-Robots-Tag', headers.get('x-robots-tag', ''))).lower()
    ld_ok = bool(p.ld)
    for block in p.ld:
        try:
            json.loads(block)
        except ValueError:
            ld_ok = False

    links = sorted({urllib.parse.urljoin(final, h).split('#')[0] for h in p.anchors
                    if urllib.parse.urlparse(urllib.parse.urljoin(final, h)).netloc == host})[:a.max_links]
    imgs = sorted({urllib.parse.urljoin(final, s) for s in p.images})[:30]
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        bad_links = [(u, s) for u, s in zip(links, ex.map(status_of, links)) if s != 200]
        bad_imgs = [(u, s) for u, s in zip(imgs, ex.map(status_of, imgs)) if s != 200]

    checks = [
        ('page answers 200', code == 200, code if final.rstrip('/') == a.url.rstrip('/') else f'{code}, redirected to {final}'),
        ('title 30-60 characters', 30 <= len(title) <= 60, f'{len(title)}: {title}'),
        ('meta description 70-170 characters', 70 <= len(desc) <= 170, len(desc)),
        ('canonical points to this page', bool(canonical) and norm_url(urllib.parse.urljoin(final, canonical)) == norm_url(final), canonical or 'none'),
        ('exactly one H1', p.h1 == 1, p.h1),
        ('no noindex (meta tag or header)', 'noindex' not in robots, robots.strip()),
        ('structured data present and valid JSON', ld_ok, f'{len(p.ld)} block(s)'),
        (f'internal links answer 200 ({len(links)} checked)', not bad_links, bad_links[:5] or ''),
        (f'images answer 200 ({len(imgs)} checked)', not bad_imgs, bad_imgs[:5] or ''),
    ]
    if a.sitemap:
        listed = {norm_url(u) for u in sitemap_urls(a.sitemap)}
        checks.append(('listed in the sitemap', norm_url(final) in listed, f'{len(listed)} URLs read'))
    if a.byline:
        checks.append((f'byline "{a.byline}" present', a.byline in text, ''))
    if a.draft:
        sents = draft_sentences(a.draft)
        missing = [s for s in sents if s not in text]
        checks.append((f'reviewed draft text present on the live page ({len(sents)} sentences)', not missing,
                       [m[:80] for m in missing[:3]] or ''))

    fails = 0
    for name, ok, detail in checks:
        fails += not ok
        print(f'{"PASS" if ok else "FAIL"}  {name}' + (f'  [{detail}]' if detail not in ('', None) else ''))
    print(f'\n{len(checks) - fails} of {len(checks)} checks pass for {final}')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())

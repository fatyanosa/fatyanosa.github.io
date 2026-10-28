#!/usr/bin/env python3
"""Fetch the public Google Scholar profile and write _data/scholar.json.

Usage: python3 scripts/update_scholar.py [SCHOLAR_USER_ID]
Keeps the existing file untouched if Scholar returns nothing (e.g. rate limiting).
"""
import html
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

USER = sys.argv[1] if len(sys.argv) > 1 else "odb3L2UAAAAJ"
OUT = Path(__file__).resolve().parent.parent / "_data" / "scholar.json"
PAGE = 100
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}


def clean(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ").strip()


def fetch(start):
    r = requests.get(
        "https://scholar.google.com/citations",
        params={"user": USER, "hl": "en", "cstart": start, "pagesize": PAGE, "sortby": "pubdate"},
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def parse_rows(page):
    pubs = []
    for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S):
        m = re.search(r'<a[^>]*href="([^"]+)"[^>]*class="gsc_a_at"[^>]*>(.*?)</a>', row, re.S)
        if not m:
            continue
        grays = re.findall(r'<div class="gs_gray">(.*?)</div>', row, re.S)
        cites = re.search(r'class="gsc_a_ac[^"]*"[^>]*>(\d*)<', row)
        year = re.search(r'class="gsc_a_h[^"]*"[^>]*>(\d{4})<', row)
        cid = re.search(r"citation_for_view=([^&\"]+)", m.group(1))
        venue = clean(re.sub(r'<span class="gs_oph">.*?</span>', "", grays[1])) if len(grays) > 1 else ""
        pubs.append({
            "title": clean(m.group(2)),
            "authors": clean(grays[0]) if grays else "",
            "venue": venue,
            "year": int(year.group(1)) if year else None,
            "citations": int(cites.group(1)) if cites and cites.group(1) else 0,
            "url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=%s&citation_for_view=%s"
            % (USER, html.unescape(cid.group(1)) if cid else ""),
        })
    return pubs


def parse_stats(page):
    cells = re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', page)
    if len(cells) >= 6:
        return {"citations": int(cells[0]), "h_index": int(cells[2]), "i10_index": int(cells[4])}
    return {}


def main():
    pubs, stats, start = [], {}, 0
    while True:
        page = fetch(start)
        if start == 0:
            stats = parse_stats(page)
        rows = parse_rows(page)
        pubs.extend(rows)
        if len(rows) < PAGE:
            break
        start += PAGE
        time.sleep(2)
    if not pubs:
        sys.exit("No publications parsed; keeping existing data.")
    pubs.sort(key=lambda p: (-(p["year"] or 0), -p["citations"], p["title"]))
    data = {
        "user": USER,
        "profile_url": "https://scholar.google.com/citations?user=" + USER,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "stats": stats,
        "publications": pubs,
    }
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote %d publications to %s" % (len(pubs), OUT))


if __name__ == "__main__":
    main()

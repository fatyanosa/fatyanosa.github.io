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
SCOPUS_ID = "57201530572"
SINTA_URL = "https://sinta.kemdiktisaintek.go.id/authors/profile/6869872"
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


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def bib_titles(path):
    """Return {bibkey: title} from a BibTeX file (brace/quote aware, no extra deps)."""
    text = path.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", text):
        end = re.search(r"\n\s*@\w+\s*\{", text[m.end():])
        body = text[m.end(): m.end() + end.start()] if end else text[m.end():]
        t = re.search(r"(?<![a-z])title\s*=\s*", body, re.I)
        if not t:
            continue
        i, opener = t.end(), body[t.end():t.end() + 1]
        if opener == "{":
            depth = 0
            for j in range(i, len(body)):
                depth += (body[j] == "{") - (body[j] == "}")
                if depth == 0:
                    out[m.group(1)] = body[i + 1:j]
                    break
        elif opener == '"':
            j = body.find('"', i + 1)
            out[m.group(1)] = body[i + 1:j]
    return out


def match_citations(pubs):
    """Map each bib entry key to its Scholar citation count by title."""
    import difflib
    bib = OUT.parent.parent / "_bibliography" / "papers.bib"
    scholar = {norm(p["title"]): p["citations"] for p in pubs}
    cited = {}
    for key, title in bib_titles(bib).items():
        n = norm(title)
        if n in scholar:
            cited[key] = scholar[n]
        else:
            close = difflib.get_close_matches(n, list(scholar), n=1, cutoff=0.9)
            if close:
                cited[key] = scholar[close[0]]
    return cited


def parse_stats(page):
    cells = re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', page)
    if len(cells) >= 6:
        return {"citations": int(cells[0]), "h_index": int(cells[2]), "i10_index": int(cells[4])}
    return {}


def fetch_scopus():
    """Scopus metrics as mirrored on the public SINTA profile (Scopus itself needs a login)."""
    try:
        r = requests.get(SINTA_URL, headers=HEADERS, timeout=30)
        r.raise_for_status()
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r.text)))
        m = re.search(r"Article (\d+) (\d+) (\d+) Citation (\d+) (\d+) (\d+) Cited Document \d+ \d+ \d+ H-Index (\d+) (\d+) (\d+)", text)
        if m:
            return {
                "author_id": SCOPUS_ID,
                "profile_url": "https://www.scopus.com/authid/detail.uri?authorId=" + SCOPUS_ID,
                "documents": int(m.group(1)),
                "citations": int(m.group(4)),
                "h_index": int(m.group(7)),
            }
    except requests.RequestException as e:
        print("SINTA fetch failed:", e)
    return None


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
        "cited": match_citations(pubs),
        "publications": pubs,
    }
    scopus = fetch_scopus()
    if scopus is None and OUT.exists():  # keep the previous values if SINTA is unavailable
        scopus = json.loads(OUT.read_text(encoding="utf-8")).get("scopus")
    if scopus:
        data["scopus"] = scopus
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote %d publications to %s" % (len(pubs), OUT))


if __name__ == "__main__":
    main()

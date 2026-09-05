#!/usr/bin/env python3
"""Fetch open-access PDFs for one paper folder's refs.bib.

    python3 _tools/fetch_pdfs.py P3_NextCamera_Prediction

Downloads only from sources that publish the PDF openly: arXiv, USENIX,
openaccess.thecvf.com, PMLR, NeurIPS proceedings, IETF, and DOIs that resolve to
an open PDF. Anything behind a paywall is listed at the end so it can be fetched
by hand through the institutional subscription; nothing is scraped or bypassed.

Files land in <paper>/literature/pdf/<citekey>.pdf and are gitignored.
Re-running skips files that already exist.
"""

from __future__ import annotations

import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "prahari-research-fetch/1.0 (academic use; contact the repository owner)"
TIMEOUT = 45

ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,]+),(.*?)\n\}", re.S)


def _split_fields(body: str) -> list[str]:
    """Split a BibTeX entry body on commas that sit at brace depth zero."""
    parts, depth, buf = [], 0, []
    for ch in body:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def parse_bib(text: str) -> list[dict]:
    out = []
    for _kind, key, body in ENTRY.findall(text):
        fields = {"citekey": key.strip()}
        for part in _split_fields(body):
            if "=" not in part:
                continue
            name, _, value = part.partition("=")
            value = value.strip().strip(",").strip()
            if value[:1] in "{\"" and value[-1:] in "}\"":
                value = value[1:-1]
            fields[name.strip().lower()] = " ".join(value.split())
        out.append(fields)
    return out


# DOI prefixes whose publishers serve the PDF openly. Anything else is treated as
# paywalled and reported for manual pickup rather than scraped.
OPEN_DOI_PREFIXES = {
    "10.3390": "mdpi",        # MDPI (Sensors, Entropy)
    "10.1140": "doi",         # EPJ Data Science
    "10.1038/srep": "doi",    # Scientific Reports
    "10.1186": "doi",         # SpringerOpen
    "10.1371": "doi",         # PLOS
    "10.3389": "doi",         # Frontiers
    "10.24963": "doi",        # IJCAI proceedings
    "10.1613": "doi",         # JAIR
    "10.17487": "rfc",        # IETF RFCs
}


def pdf_url(entry: dict) -> str | None:
    """Return a URL that serves the PDF openly, or None if a human must fetch it."""
    eprint = entry.get("eprint") or ""
    note = entry.get("note") or ""
    doi = (entry.get("doi") or "").strip()
    url = entry.get("url") or ""

    m = re.search(r"arXiv:\s*([\d.]+v?\d*)", note) or re.search(r"(\d{4}\.\d{4,5})", eprint)
    if not m:
        m = re.search(r"10\.48550/arXiv\.(\d{4}\.\d{4,5})", doi)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}"

    if url:
        if "usenix.org" in url:
            return url  # landing page; reported for manual pickup if it is not a PDF
        if "openaccess.thecvf.com" in url:
            return url.replace("/html/", "/papers/").replace("_paper.html", "_paper.pdf")
        if "proceedings.mlr.press" in url and url.endswith(".html"):
            return url[:-5] + ".pdf"
        if "proceedings.neurips.cc" in url:
            return url.replace("/hash/", "/file/").replace("-Abstract", "-Paper").replace(".html", ".pdf")
        if url.endswith(".pdf"):
            return url
        if "rfc-editor.org" in url or "datatracker.ietf.org" in url:
            return url

    for prefix, kind in OPEN_DOI_PREFIXES.items():
        if doi.startswith(prefix):
            if kind == "mdpi":
                return f"https://www.mdpi.com/{doi.split('/', 1)[1].replace('-', '/')}/pdf"
            if kind == "rfc":
                num = doi.rsplit("RFC", 1)[-1]
                return f"https://www.rfc-editor.org/rfc/rfc{num}.txt"
            return f"https://doi.org/{doi}"
    return None


def fetch(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"    failed: {exc}")
        return False
    if not data.startswith(b"%PDF"):
        print("    not a PDF (landing page or paywall)")
        return False
    dest.write_bytes(data)
    return True


def main(folder: str) -> None:
    root = Path(__file__).resolve().parents[1] / folder
    bib = root / "literature" / "refs.bib"
    if not bib.is_file():
        sys.exit(f"no refs.bib at {bib}")
    out = root / "literature" / "pdf"
    out.mkdir(parents=True, exist_ok=True)
    entries = parse_bib(bib.read_text(encoding="utf-8"))
    got, skipped, manual = 0, 0, []
    for e in entries:
        dest = out / f"{e['citekey']}.pdf"
        if dest.exists():
            skipped += 1
            continue
        url = pdf_url(e)
        if not url:
            manual.append((e["citekey"], e.get("doi") or e.get("url") or "no locator"))
            continue
        print(f"  {e['citekey']} <- {url}")
        if fetch(url, dest):
            got += 1
        else:
            manual.append((e["citekey"], url))
        time.sleep(1.5)  # be polite to arXiv and USENIX
    print(f"\n{folder}: {got} fetched, {skipped} already present, {len(manual)} need a human")
    if manual:
        print("\nFetch these by hand through the institutional subscription:")
        for key, loc in manual:
            print(f"  {key:32s} {loc}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

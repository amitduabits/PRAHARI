#!/usr/bin/env python3
"""Sanity-check a refs.bib: duplicate keys, missing year/title, malformed DOIs.

    python3 _tools/check_bib.py P1_Provenance_Dispatch

Does not touch the network. Verification against Crossref is a separate, manual
step; this only catches the mechanical defects.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_pdfs import parse_bib  # noqa: E402

DOI = re.compile(r"^10\.\d{4,9}/\S+$")


def main(folder: str) -> None:
    bib = Path(__file__).resolve().parents[1] / folder / "literature" / "refs.bib"
    entries = parse_bib(bib.read_text(encoding="utf-8"))
    problems = []
    keys = Counter(e["citekey"] for e in entries)
    for key, n in keys.items():
        if n > 1:
            problems.append(f"duplicate key: {key} ({n} times)")
    for e in entries:
        for field in ("title", "year"):
            if not e.get(field):
                problems.append(f"{e['citekey']}: missing {field}")
        doi = e.get("doi")
        if doi and not DOI.match(doi):
            problems.append(f"{e['citekey']}: malformed DOI {doi!r}")
        if not (e.get("doi") or e.get("url") or e.get("eprint")):
            problems.append(f"{e['citekey']}: no DOI, URL or arXiv id")
    print(f"{folder}: {len(entries)} entries, {len(problems)} problems")
    for p in problems:
        print("  " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

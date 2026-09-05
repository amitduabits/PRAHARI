#!/usr/bin/env python3
"""Report, without touching the network, how many refs each paper has and how many
have a URL the fetch script can retrieve openly."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_pdfs import parse_bib, pdf_url  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAPERS = sorted(p.name for p in ROOT.iterdir() if p.name.startswith("P") and p.is_dir())

print(f"{'paper':32s} {'refs':>5s} {'open':>5s} {'manual':>7s} {'have':>5s}")
tot = [0, 0, 0, 0]
for name in PAPERS:
    bib = ROOT / name / "literature" / "refs.bib"
    if not bib.is_file():
        continue
    entries = parse_bib(bib.read_text(encoding="utf-8"))
    pdfdir = ROOT / name / "literature" / "pdf"
    have = len(list(pdfdir.glob("*.pdf"))) if pdfdir.is_dir() else 0
    openable = sum(1 for e in entries if pdf_url(e))
    manual = len(entries) - openable
    print(f"{name:32s} {len(entries):5d} {openable:5d} {manual:7d} {have:5d}")
    tot = [a + b for a, b in zip(tot, (len(entries), openable, manual, have))]
print(f"{'TOTAL':32s} {tot[0]:5d} {tot[1]:5d} {tot[2]:7d} {tot[3]:5d}")

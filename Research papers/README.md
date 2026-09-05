# PRAHARI research papers

Six paper folders, a master plan, and the tools that keep the bibliographies honest.

## Start here

1. `ACTION_PLAN.md` — the programme plan, the ten steps per paper, and the
   **revised portfolio**. Read it before anything else: a verified prior-art review
   changed the plan substantially, and three of the six original mechanisms turn out
   to be published already.
2. `P<n>_<Name>/README.md` — one page per paper: the claim, what would refute it,
   and the honest position on novelty.
3. `P<n>_<Name>/literature/REVIEW.md` — the full verified prior-art review. The most
   valuable pages in this repository are section (B) of each review, where the
   verdict is stated bluntly, and P3's section (C) (real datasets) and P5's section
   (B) (five cited methods for choosing a deduplication window).

## Layout

```
ACTION_PLAN.md              the plan and the revised portfolio
Makefile                    make check | make fetch | make plan
_tools/                     fetch_pdfs.py, check_bib.py, plan.py
_templates/                 claim-evidence table, related work, limitations
P1_Provenance_Dispatch/     provenance-gated inference dispatch
P2_Fallback_Engines/        deterministic fallback and label-free estimation
P3_NextCamera_Prediction/   next-camera prediction without road networks
P4_Decoder_Admission/       decoder admission and probe coverage
P5_CrossModal_Fusion/       cross-modal collapse and alert dedup
P6_Platform_Architecture/   multi-authority platform design
```

Each paper folder holds `literature/` (REVIEW.md, matrix.md, refs.bib, pdf/),
`experiments/EXPERIMENTS.md`, `paper/outline.md`, and `review/` (CHECKLIST.md,
REVIEWER_Qs.md).

## Commands

```
make check      verify every refs.bib (no network) — currently 216 entries, 0 problems
make plan       how many references each paper has and how many PDFs are openly fetchable
make fetch      download the open-access PDFs into <paper>/literature/pdf/
make P3_NextCamera_Prediction    fetch one paper's PDFs
```

`make fetch` retrieves only from arXiv, USENIX, CVF open access, PMLR, NeurIPS
proceedings, IETF and open-access DOI prefixes. The 143 references behind IEEE,
ACM, Elsevier and Springer paywalls are listed at the end of the run so they can be
pulled through the institutional subscription by hand; nothing is scraped or
bypassed. PDFs are gitignored and never committed.

## The experiments

Reference implementations, baselines and figures for all six papers live in
`../09_Research/`. `make test` there runs 34 tests in about a second;
`make experiments` regenerates every results JSON and figure in about a minute,
with fixed seeds.

## The four programme gates

Nothing is submitted until all four hold:

1. No synthetic headline numbers — every number in an abstract comes from real data.
2. The five closest prior works appear before page 3.
3. Every results table has at least one row where a baseline beats us.
4. `make test && make experiments` on a clean clone regenerates every figure.

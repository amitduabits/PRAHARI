# PRAHARI research programme: action plan

Written 2026-09-05. This replaces the schedule in `START_HERE.md`, which assumed
six novel papers on a fixed calendar. A verified prior-art review of all six
topics has since been completed (`P*/literature/REVIEW.md`), and it changes the
plan materially: three of the six mechanisms are already published, and one
paper's central derivation is contradicted by our own experiments. The plan
below is built around what the evidence actually supports.

---

## 0. What changed, and why the plan is different

Six independent literature reviews were run against arXiv, ACM DL, IEEE Xplore,
USENIX, Crossref and DBLP. Findings that force a change of direction:

| Paper | Claimed novelty | Verdict from the literature |
|---|---|---|
| P1 | Registration-time compilation of a permitted-engine set | **Combinational.** Every ingredient is published (Capsicum, XEngine, Ancile, PBAC, INFaaS); the combination is not. Empirical "invoked vs released" separation is the stronger contribution. |
| P2 | Cross-class fallback + label-free accuracy estimation | **Both anticipated.** Fallback = NoScope / Neural Simplex. Stratified estimation = Mandoline with a provenance slice. Average Confidence is provably unbiased, which is why our own baseline beat us. |
| P3 | Transition-frequency next-camera prediction | **Published, twice, in two literatures.** Makris 2004 / Tieu 2005 in vision; Gambs 2012 Mobility Markov Chains in mobility; Lu 2013 showed first-order Markov is near-optimal. Mechanism novelty is not defensible. |
| P4 | Refuse-at-the-bound admission control | **Erlang-B, 1917.** The envelope result is definitional, not empirical. The K-allocation frontier between decode and probe budget is the real, unpublished contribution. |
| P5 | 120 s collapse window derived from FOV / speed | **Our own experiments refute the derivation** (geometric window is 1.3-9.6 s; the measured knee is 15-30 s). Entity-agnostic schema is standard practice (CEF, OCSF, JDL). |
| P6 | Registry rows instead of federation APIs | **Known pattern under four names** (mediators, dataspaces, catalogue federation, NGSI-LD registration). The sweep reconciliation loop and the transport-mix evidence are what is new. |

Consequence: **the programme is not six novel-mechanism papers.** It is two or
three defensible papers plus a set of results that belong in workshops or as
sections of other papers. Section 6 below states the recommended portfolio.

---

## 1. Folder convention

Each paper lives in `P<n>_<Slug>/` with a fixed layout:

```
P<n>_<Slug>/
  README.md            one page: claim, venue, status, the honest position
  literature/
    REVIEW.md          the full verified prior-art review (raw, unedited)
    matrix.md          axis-by-axis comparison table and the novelty gap
    refs.bib           verified BibTeX, one entry per work cited
    fetch_pdfs.py      downloads open-access PDFs into literature/pdf/
    pdf/               PDFs (gitignored; fetched locally, never committed)
  experiments/
    EXPERIMENTS.md     claim -> evidence table, what runs, what is missing
    results/           symlink or copy of ../../09_Research/results/p<n>_*.json
  paper/
    outline.md         section-by-section plan with word budgets
    main.tex           venue template (added at drafting time)
  review/
    CHECKLIST.md       venue submission checklist
    REVIEWER_Qs.md     anticipated reviewer questions with prepared answers
```

Shared material lives in `_templates/` (section templates, claim-evidence table
template) and `_tools/` (fetch script, bib checker).

---

## 2. The ten steps, per paper

Every paper follows the same sequence. A step is not done until its gate passes.

**Step 1. Position against prior art.**
Read `literature/REVIEW.md` in full, including section (A) closest prior art and
section (B) the blunt verdict. Write `literature/matrix.md`: one row per prior
work, columns for the axes that distinguish it, and a final paragraph stating in
one sentence what is left that is ours.
*Gate:* the sentence survives being read aloud to someone who has read the five
closest works. If it does not, stop and re-scope before writing anything else.

**Step 2. Fix the claim.**
Write the paper's single claim as one falsifiable sentence in `README.md`, plus
the experiment whose failure would refute it. A claim with no refuting
experiment is a description, not a result.
*Gate:* a colleague can state what result would make the paper wrong.

**Step 3. Get real data.**
Replace synthetic traces with a real dataset or a real deployment trace. Each
paper's `EXPERIMENTS.md` names its dataset and its access route. This is the
single largest gap across the whole programme.
*Gate:* every headline number comes from data we did not generate.

**Step 4. Implement the baselines the reviewers named.**
Section (A) of each review lists the five works a reviewer will raise. Implement
or faithfully reproduce the strongest two or three as baselines, not as
strawmen. Where a baseline dominates ours, report it.
*Gate:* the results table contains at least one row where a baseline wins.

**Step 5. Run the experiments.**
`cd 09_Research && make experiments`. Seeds are fixed; results are byte-identical
across runs except P1's wall-clock timing. Record the git commit and the
environment in the results JSON.
*Gate:* a clean clone reproduces every number in the paper.

**Step 6. Build the claim-to-evidence table.**
In `experiments/EXPERIMENTS.md`, one row per claim in the abstract, naming the
figure or table that supports it. Any claim without a row comes out of the
abstract.
*Gate:* no unsupported sentence survives in the abstract or introduction.

**Step 7. Draft.**
Follow `paper/outline.md`. Related work is written first, from `matrix.md`, and
names the closest prior art in the first two pages, not buried at the back.
*Gate:* the closest prior work is cited before page 3.

**Step 8. Write the limitations honestly.**
Every review's section (B) and (D) lists what we do not have. Those go in the
paper, in our words, before a reviewer writes them in theirs.
*Gate:* the limitations section contains at least one item that costs us
something.

**Step 9. Adversarial review.**
Answer every question in `review/REVIEWER_Qs.md` in writing. Where the honest
answer is "we cannot", either run the experiment or change the claim.
*Gate:* no question is answered with an assertion that has no evidence behind it.

**Step 10. Submit.**
Work `review/CHECKLIST.md`: anonymisation, page limit, supplementary, ethics
statement, artefact/reproducibility statement, licence for released code.

---

## 3. Literature protocol

- Every reference is verified against Crossref, arXiv, DBLP or the publisher page
  before it enters `refs.bib`. A DOI that does not resolve is a defect.
- `fetch_pdfs.py` downloads only open-access PDFs (arXiv, USENIX, openaccess.thecvf,
  publisher OA). Paywalled works are fetched through the institutional
  subscription by hand; the script lists them and stops.
- PDFs are never committed. `literature/pdf/` is gitignored.
- When a reviewer or co-author names a work not in `REVIEW.md`, it is added with
  the same verification standard and `matrix.md` is updated the same day.
- Reading order: the five closest works in section (A) first, in full. Everything
  else can be read from the abstract until it turns out to matter.

---

## 4. Experiment protocol

- Seeds live in one place (`09_Research/prresearch/seeds.py`). Nothing calls
  `numpy.random` or `random` directly.
- No `hash()` on strings anywhere in an experiment. Python salts it per process
  and it silently breaks cross-run reproducibility; this already bit us once.
- Every experiment writes a JSON with its parameters alongside its results.
- Temporal splits, never random splits, wherever the data has time in it.
- Report distributions, not point estimates: p50, p99, p99.9 and the full CDF for
  latency; bootstrap confidence intervals for accuracy.
- Report the cost of every win. A latency figure without its refusal rate, or an
  alert reduction without its masking rate, is not a result.
- Ablate every component that has a name in the paper. If the GIS fallback or the
  three-strike rule is named, it has an ablation row.

## 5. Comparison protocol

For each paper, the comparison table has one row per method and one column per
metric, with these rules:

1. Baselines come from section (A) of the review, implemented at their best.
2. A trivial baseline is always included (global prior, popularity, random). Most
   papers in these areas die on the trivial baseline; find out early.
3. Where our method loses, the row stays in the table and the text says so.
4. Runtime and memory are columns, not footnotes, whenever the argument is that
   the simple method suffices.
5. Statistical significance: bootstrap CIs over test units and a paired test
   against the strongest baseline.

---

## 6. Recommended portfolio, given the evidence

This supersedes the six-paper plan.

**Tier A, submit as full papers.**

- **P4 reframed** as *"Allocating one concurrency budget between decoding and
  health probing"*. The Erlang-B envelope is background, not contribution; the
  contribution is the frontier between refusal probability B(K,a) and coverage
  interval n/K*T when both draw on the same K, plus a derivation of the
  three-strike constant from a target false-alarm rate. Needs the multi-resource
  measurements listed in `P4/experiments/EXPERIMENTS.md`. Venue: IEEE TMM or
  ACM TOMM; a systems venue is also plausible.
- **P1 reframed** around the measurement rather than the mechanism: *the first
  quantification of model invocation, as distinct from output release, as a
  privacy harm in a deployed video pipeline*. Requires real instrumentation of
  `analyse.py` and a threat model that survives the "a permitted detector can be
  probed for identity" objection. Venue: CCS, PETS or USENIX Security is a better
  fit than CVPR, and the review says so.

**Tier B, submit if the data problem is solved.**

- **P3 reframed** as a characterisation study: *in which deployment regimes does
  a first-order transition table suffice, and where does it collapse?* Must run
  on CityFlow and VeRi-776, must include Flashback and a popularity prior, must
  cite Makris/Tieu/Gambs in the first paragraph as what is being reproduced.
  Venue: IJCAI or a transport/ITS journal.
- **P6 reframed** with one falsifiable claim (descriptor federation beats broker
  federation below X cameras per authority) and one external baseline (NGSI-LD
  registration or ONVIF auto-onboard), leading with the transport-mix failure
  distribution, which nobody has published at this scale. Venue: IEEE TETC.
  ACM Computing Surveys is not achievable for this artefact; a separate survey of
  cross-authority video federation is, and it is a different paper.

**Tier C, workshop or section, not a paper.**

- **P2** as it stands is a negative result: the provenance estimator does not beat
  Average Confidence at batch level, and Average Confidence is provably unbiased
  under calibration. That is worth a short workshop paper on monitoring two-tier
  pipelines, or a section inside P1. The reproducibility claim needs softening in
  either case.
- **P5** as it stands cannot be submitted while the geometric derivation stands,
  because our own data refutes it. Either replace the derivation with an
  inter-arrival or knee-based criterion from the alarm-management literature and
  resubmit as a full paper, or fold the collapse predicate into P6 as a design
  element.

**Sequencing.** P4 and P1 first, in parallel, because they need instrumentation
of a system we control. P3 and P6 second, gated on data access. P2 and P5 last,
after their reframing is settled.

---

## 7. Programme-wide gates

Nothing is submitted until all four hold:

1. **No synthetic headline numbers.** Every number in an abstract comes from real
   data or a real deployment.
2. **Closest prior art cited early.** The five works in section (A) appear before
   page 3 of each paper.
3. **At least one losing row.** Every results table contains a case where a
   baseline beats us, with an explanation.
4. **Reproducible from a clean clone.** `make test && make experiments` on a fresh
   checkout regenerates every figure.

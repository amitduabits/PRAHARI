# P2 — Deterministic fallback engines and reproducible inference

**Working title.** What Provenance Buys: A Negative Result on Label-Free Accuracy
Estimation in Two-Tier Video Pipelines.

**Target venue.** A workshop, not ICCV. The literature review is unambiguous:
both claimed contributions are anticipated, and one of them is contradicted by a
theorem. Candidates: an ICCV/CVPR workshop on uncertainty or deployment, the
NeurIPS workshop track on distribution shift, or MLSys.

**Status.** Reference implementation and four experiments run
(`09_Research/prresearch/p2_fallback`). Literature review complete.
**Reframing required before this can be submitted anywhere.**

## The claim, as it must now be stated

Carrying per-detection inference provenance does not improve *batch-level*
accuracy estimation over Average Confidence — and it provably cannot, because
Average Confidence is unbiased under calibration (`kivimaki2025confidence`, JAIR
2025). What it does buy is accuracy *sliced by inference path*: primary 0.66 vs
secondary 0.44, recovered to within 0.002, a quantity no unstratified estimator
can express and the only one an operator can act on.

**What would refute it.** Per-stratum ATC matching our estimator on the sliced
metric. If it does — and it is a three-line change to `garg2022atc` — the method
contribution collapses entirely to the provenance plumbing, and the paper becomes
a systems note. Run it before writing anything.

## The honest position

Three claims, three verdicts:

1. **Cross-class fallback with a shared record schema: anticipated.** `kang2017noscope`
   already cascades a classical detector with learned CNNs under one output schema
   and an accuracy budget. `phan2020neuralsimplex` is the same architecture in
   control. The degraded-mode reaction is a catalogued type in
   `ferreira2024safetymonitoring`. Do not claim this.
2. **Stratified label-free estimation: not exactly published, but the gap is thin.**
   `chen2021mandoline` does slice-conditioned estimation with arbitrary slicing
   functions. "Which engine ran" is a legal slicing function. Ours is an
   instantiation, not a new estimator.
3. **Bit-for-bit reproducibility of the classical tier: true but not novel, and
   overstated.** `shanmugavelu2024fpna` shows the learned primary *can* be made
   deterministic at a throughput cost. Soften to "reproducible without the cost of
   deterministic kernels".

What remains: the specific combination of three heterogeneous entity types each
with a classical counterpart, fallback on absence and empty result as well as
exception, and provenance carried into downstream analytics. That is an
engineering contribution and a reviewer will call it that. Plus the negative
result, which is worth publishing on its own.

## Files

`literature/REVIEW.md` (32 works, the SOTA survey in section C),
`literature/matrix.md`, `experiments/EXPERIMENTS.md`, `paper/outline.md`,
`review/REVIEWER_Qs.md`.

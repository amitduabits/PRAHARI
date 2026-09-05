# P3 — Next-camera prediction without road networks

**Working title.** When Counting Is Enough: A Regime Characterisation for
Transition-Frequency Next-Camera Prediction.

**Target venue.** IJCAI or AAMAS if the regime result holds on real data;
otherwise a transport/ITS journal (IEEE T-ITS) where the deployment framing is
worth more. **Not as a method paper anywhere.**

**Status.** Reference implementation and four experiments run
(`09_Research/prresearch/p3_nextcam`). Literature review complete.
**Blocked on real data. The synthetic result is worth nothing.**

## The claim, as it must now be stated

Not "we propose transition-frequency prediction" — that is `makris2004bridging`
(2004) and `gambs2012next` (2012). The defensible claim is a *characterisation*:

> Given camera density, deployment irregularity and ALPR coverage rate, there is a
> regime in which a first-order transition table matches or beats road-network
> reconstruction and learned sequence models, and a regime in which it collapses.
> We identify the boundary.

**What would refute it.** Flashback (`yang2020flashback`) or a road-network method
(`qi2021alprtraj`, 85% on real Ningbo ALPR data) beating the transition table
across every regime we test. Then there is no boundary and no paper.

## The honest position — read this before writing anything

**The mechanism is published, twice, in two independent literatures.**

- `makris2004bridging` (CVPR 2004) accumulates transition evidence across
  observations without solving correspondence, and states the by-product is
  "inter-camera transition times, which can be used to support predictive tracking
  across the camera network". That is our thesis, in 2004.
- `tieu2005inference` (ICCV 2005) generalises it, and notes prior work "assumed
  restricted parametric transition distributions" — i.e. the histogram approach was
  already the thing being generalised in 2005.
- `javed2003tracking`, `gilbert2006tracking`, `marinakis2006practical`,
  `loy2010timedelayed`, `cho2019joint` carry it forward to 2019.
- `gambs2012next` publishes the identical estimator as Mobility Markov Chains.
- `lu2013approaching` shows a first-order Markov chain is near information-
  theoretically optimal on sparse traces — so "frequency counting works well" is
  expected, not surprising.

If the paper claims mechanism novelty it will be shredded. Cite
Makris/Tieu/Javed/Gambs **in the first paragraph** as what we are reproducing at
scale, not in related work as what we differ from.

What is genuinely left: (i) the great-circle cold-start fallback, which is a
paragraph and an ablation, not a paper; (ii) the prospective top-k task framing
with a deployment-realistic temporal split, if we release the protocol; (iii) the
regime characterisation, which is the only thing that can carry a paper.

## Files

`literature/REVIEW.md` (33 works, plus a dataset survey and the full evaluation
protocol in sections C and D — the most useful document in this folder),
`literature/matrix.md`, `experiments/EXPERIMENTS.md`, `paper/outline.md`,
`review/REVIEWER_Qs.md`.

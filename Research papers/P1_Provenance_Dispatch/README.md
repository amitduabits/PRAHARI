# P1 — Provenance-gated inference dispatch

**Working title.** Invoked, Not Released: Measuring Model Exposure as a Distinct
Privacy Harm in Multi-Authority Video Analytics.

**Target venue.** ACM CCS, PETS, or USENIX Security. *Not CVPR.* The literature
review found the framing is established in the security community
(roesner2014wdac, kim2023erebus, bagdasaryan2019ancile) and absent from vision
venues — so a vision audience finds it novel and a security-literate reviewer
finds it familiar. Submitting to the community that already owns the framing, with
the measurement they do not have, is the stronger play.

**Status.** Reference implementation and four experiments run (`09_Research/prresearch/p1_provenance`).
Literature review complete. Blocked on real instrumentation of `app/services/analyse.py`.

## The claim, in one sentence

Compiling a camera's provenance attributes into a permitted-engine set at
registration time makes forbidden model *invocation* impossible rather than merely
filtering forbidden *output*, and that difference is measurable: naive
union-then-filter produces byte-identical results while running 17,377 forbidden
facial inferences over 20,000 frames.

**What would refute it.** A measurement showing that on a real deployment the
permitted engines leak the forbidden attribute anyway — that a permitted
person-detector can be probed for identity at accuracy comparable to the facial
engine. If that holds, the architectural guarantee buys nothing and the paper is
wrong. This experiment is not yet run and it is the one that matters most.

## The honest position

The mechanism is **combinational**, not new. Every ingredient is published:

- capability-style enforcement by unavailability — `watson2010capsicum`
- ahead-of-time policy compilation — `liu2008xengine`
- provenance-derived access decisions — `park2012pbac`
- policy that gates computation — `bagdasaryan2019ancile`
- lazy per-variant model materialisation — `romero2021infaas`

No published work combines them at the camera-registration boundary for video
inference. That is a legitimate but combinational claim and a strong reviewer will
read it that way. The paper is safe only if the **empirical** contribution carries
equal weight: no systems paper measures "the model saw the pixels" as a harm
distinct from "the output was released", and only `kaminski2017avertingroboteyes`
(a law review article) even asserts it.

## Files

- `literature/REVIEW.md` — 30 verified works, the five closest, and the blunt verdict
- `literature/matrix.md` — axis comparison and the novelty gap
- `experiments/EXPERIMENTS.md` — claim-to-evidence table and what is missing
- `paper/outline.md` — section plan
- `review/REVIEWER_Qs.md` — the questions we must be able to answer

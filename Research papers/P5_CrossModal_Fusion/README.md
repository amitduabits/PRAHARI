# P5 — Cross-modal collapse and alert deduplication

**Working title.** How Long Is a Presence? Choosing the Deduplication Window for
Cross-Modal Video Alerts, and Why the Geometric Derivation Is Wrong.

**Target venue.** IEEE TCSVT or Image and Vision Computing, **after** the
reframing. As currently written the paper cannot be submitted: its central
derivation is refuted by our own data.

**Status.** Reference implementation and four experiments run
(`09_Research/prresearch/p5_fusion`). Literature review complete. **Reframing is
mandatory, and the literature tells us exactly what to replace the derivation with.**

## The claim, as it must now be stated

Not "the 120 s window is FOV depth divided by permitted speed". That derivation is
wrong by one to two orders of magnitude: the geometric quantity is 1.3-9.6 s across
our estate (median ~3 s), while the measured reduction-versus-masking knee is at
15-30 s and 120 s masks 384 distinct incidents in 12,000. The claim becomes:

> On a deployed municipal camera network with incident-level ground truth, the
> deduplication window's operating curve can be measured, its knee located
> reproducibly, and the operating point chosen from a stated cost ratio between a
> masked incident and a redundant alert. A first-principles geometric derivation of
> that window is wrong, and we show by how much.

**What would refute it.** A per-camera fitted window (Method 1 below) clustering
near 120 s after all, or the masking we measure disappearing under a session-window
semantics that merges transitively on activity rather than anchoring to the first
observation. Both are checkable and neither has been checked.

## The honest position

1. **The schema is not novel.** IDMEF (RFC 4765, 2007), OCSF, CEF, LEEF, and JDL
   Level-0/1 common referencing are all exactly "one normalised record across
   heterogeneous detectors, no union type". Claiming it costs credibility on the
   parts that are defensible.
2. **The collapse predicate is not novel.** `debar2001aggregation` defines a
   duplicate relation over a normalised alert record collapsed within an explicit
   window, for the same reason (operator load), twenty-five years ago.
   `akidau2015dataflow` names the construct: a keyed session window with gap W.
   Use their vocabulary.
3. **The window derivation is wrong, and the right method is known.** Process
   control abandoned first-principles timer derivations over a decade ago in favour
   of duration-distribution-based design (`wang2022delaytimers`, `adnan2011detectiondelay`,
   `afzal2018timedeadbands`). Delete the geometric derivation; do not repair it.

**What is genuinely unclaimed**, and what the paper should be: an empirical
characterisation of the deduplication-window operating curve for cross-modal video
analytics with incident-level ground truth (no such measurement exists in
surveillance, and CityFlow and the Re-ID literature measure association accuracy,
not operator burden); the negative result about the geometric derivation; and the
empirical sufficiency result that one entity-keyed predicate suffices across three
unrelated analytics at a stated incident recall.

## Files

`literature/REVIEW.md` — 35 works plus 4 standards. **Section B is the most
valuable page in this whole folder: five named, cited methods for choosing W.**
Then `literature/matrix.md`, `experiments/EXPERIMENTS.md`, `paper/outline.md`,
`review/REVIEWER_Qs.md`.

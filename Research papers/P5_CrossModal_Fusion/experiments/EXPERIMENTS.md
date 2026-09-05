# P5 experiments

Code: `09_Research/prresearch/p5_fusion/`. Run: `cd 09_Research && python3 run_all.py P5`.
Results: `09_Research/results/p5_fusion.json`. Figure: `p5_window_tradeoff.png`.

## Claim-to-evidence table

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Entity-agnostic collapse cuts alerts sharply at full incident coverage | E5.1: 80.6% reduction vs one-alert-per-detection, incident recall 1.0 | **supported** (synthetic) |
| C2 | Cross-modal keying beats per-modality dedup | E5.4: extra reduction 10.7% → 43.7% as dual-tagged share rises 0.15 → 1.0 | **supported** (synthetic) |
| C3 | Confidence voting is not a usable operating point | E5.1: 88.1% reduction but 63% of incidents dropped | **supported** |
| C4 | W = FOV depth / permitted speed | E5.3: the geometric quantity is 1.3-9.6 s, median ~3 s | **REFUTES the claim** |
| C5 | 120 s is the right window | E5.2: knee at 15-30 s; 120 s masks 384/12,000 distinct incidents for 1.4% more reduction | **REFUTES the claim** |
| C6 | W chosen by a defensible method | — | **NOT RUN. This is the paper.** |
| C7 | Measured on real detections with incident ground truth | — | **NOT RUN** |

C4 and C5 are the useful rows. A negative result about a derivation we shipped is
more publishable than the derivation was.

## What is missing, in priority order

1. **Fit W properly (C6).** Implement all four families from `literature/matrix.md`:
   mixture crossover, distribution-based spec design, Kneedle, and the cost-weighted
   ROC point. Report per-camera fitted W and its distribution across the estate.
2. **Real detections with incident ground truth (C7).** The current generator makes
   incidents by construction, including the revisit process that creates the
   masking. Everything downstream inherits that choice. Needed: a labelled window of
   real PRAHARI detections where an operator has marked distinct incidents.
3. **Settle the window semantics.** Is the window anchored to the first observation
   or does it merge transitively on activity, as `akidau2015dataflow` sessions do?
   The two give materially different results under sustained presence, and 120 s
   means different things under each. The current implementation anchors to first;
   the deployed matcher's behaviour must be checked against it.
4. **Check the case-grouping hypothesis.** If the deployment alerts fast and groups
   into cases over 120 s, the masking objection largely dissolves and the paper
   changes shape. Check before writing.
5. **Operator-burden metric.** Alerts per operator per hour, the metric the alarm
   literature actually uses (`eemua191`, `wang2016alarmoverview`), rather than a
   raw alert count.
6. **A learned-boundary baseline** (`jones2008beyond`), since a reviewer who knows
   that literature will ask why W is fixed at all.

## Baselines implemented

`NaiveOr` (one alert per detection), `PerModalityDedup`, `ConfidenceVoting`,
`EntityAgnosticCollapse`. Valdes-Skinner-style multi-attribute weighted similarity
is **not** implemented and is the baseline the review names as closest.

## Metric note

`score()` reports two failure modes separately, and the paper must too:
under-collapsing costs operator attention (redundant alerts per incident), and
over-collapsing costs evidence (distinct incidents masked into one alert). A method
is only good if it drives the first down without pushing the second up. Reporting
alert reduction alone is how the 120 s figure survived this long.

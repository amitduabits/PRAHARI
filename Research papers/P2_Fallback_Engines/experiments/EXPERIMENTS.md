# P2 experiments

Code: `09_Research/prresearch/p2_fallback/`. Run: `cd 09_Research && python3 run_all.py P2`.
Results: `09_Research/results/p2_fallback.json`. Figure: `p2_yield_accuracy.png`.

## Claim-to-evidence table

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Two-tier never drops a frame | E2.1: yield 1.0 at every injected failure rate to 0.5; primary-only falls to 0.55 | **supported** (simulated engines) |
| C2 | The classical tier is bit-for-bit deterministic | E2.2: 0 mismatches over 5,000 samples × 3 pairs | **supported**, but see the caveat below |
| C3 | Provenance enables per-path accuracy estimation without labels | E2.3: primary 0.6605 vs secondary 0.4431 recovered to ±0.002 | **supported** |
| C4 | Provenance improves *batch* accuracy estimation | E2.3: global prior beats us on 2 of 3 pairs | **REFUTED by our own data, and by a theorem** |
| C5 | We beat the actual state of the art | — | **NOT RUN.** ATC, per-stratum ATC, COT, Mandoline-with-provenance-slices are all missing |
| C6 | The result holds on real YOLO/FaceNet/PaddleOCR, not behavioural models | — | **NOT RUN** |

C4 is the interesting row. `kivimaki2025confidence` proves Average Confidence is
unbiased and consistent under calibration, so losing to it at batch level is
expected. Report it as a finding, cite the theorem, and move the claim to C3.

## The determinism caveat

E2.2 shows the classical engine is deterministic, which is true and uninteresting.
`shanmugavelu2024fpna` shows the *learned* tier can also be made deterministic, at
a throughput cost. The defensible claim is therefore about cost, not capability,
and we do not currently measure that cost. Add: throughput of the primary with and
without deterministic kernels enabled.

## What is missing, in priority order

1. **The full baseline table (C5).** Rows required: AC/CBPE with the JAIR
   confidence intervals, global ATC, **per-stratum ATC**, DoC, COT, and Mandoline
   with the provenance field as a slicing function. Per-stratum ATC is the one that
   decides whether there is a method contribution at all.
2. **Real engines (C6).** The current primaries are behavioural models with a
   difficulty parameter. The determinism result transfers to real engines; the
   accuracy numbers do not, and no reviewer will accept them.
3. **A conditional-validity metric.** Batch accuracy is the wrong target. Report
   per-stratum calibration error and per-stratum estimation error, where
   stratification should help and the AC theorem does not apply.
4. **Confidence intervals on the estimate.** `angelopoulos2021conformal` — a
   reviewer will ask why conformal risk control was not used.
5. **Real failure rates.** The 0.05-0.50 sweep is injected. Measure the actual
   exception, absence and empty-result rates in the deployed pipeline.

## Baselines implemented

`SinglePipeline` (primary only), `RetryPipeline` (try again, 3 attempts),
`ConfidenceOnlyEstimator`, `GlobalPriorEstimator`.

Note that **retry beats two-tier on accuracy-over-all-frames at most failure
rates** (E2.1). That row stays in the table. The fallback's case is bounded
latency and determinism, not raw accuracy, and the paper must say so.

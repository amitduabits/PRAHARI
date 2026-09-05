# P1 experiments

Code: `09_Research/prresearch/p1_provenance/`. Run: `cd 09_Research && python3 run_all.py P1`.
Results: `09_Research/results/p1_provenance.json`. Figure: `09_Research/figures/p1_dispatch_latency.png`.

## Claim-to-evidence table

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Dispatch cost is O(1) in policy size | E1.1: 666-703 ns median, flat from 6 to 192 rules; RBAC rises 1568 → 24,778 ns | **supported** (synthetic policy) |
| C2 | Output-equivalent designs differ in exposure | E1.2: naive union returns 0 forbidden records but runs 24,445 forbidden calls, 17,377 facial | **supported** (simulated engines) |
| C3 | Lazy construction keeps forbidden weights out of memory | E1.3: face weights never resident when no camera permits; 16 MB of 64 MB never allocated | **supported** (simulated weights) |
| C4 | Registration-time compilation removes per-frame audit growth | E1.4: 0 vs 11.6 MB/camera/day at 0.5 fps | **supported** (analytic) |
| C5 | The permitted engines do not leak the forbidden attribute | — | **NOT RUN. This is the experiment that decides the paper.** |
| C6 | The same holds on the deployed system, not a model of it | — | **NOT RUN** |

An abstract may contain C1-C4. It may not contain C5 or C6 until they exist.

## What is missing, in priority order

1. **The leakage experiment (C5).** Train or fine-tune a probe on the *permitted*
   engines' outputs (person boxes, track ids, crops) and measure re-identification
   accuracy against the facial engine's. If the probe gets close, the architectural
   guarantee is cosmetic and the paper must say so. Reviewers will ask this first;
   `cangialosi2022privid` gives a formal guarantee we do not.
2. **Real instrumentation.** E1.2 derives call counts from each dispatcher's
   contract rather than instrumenting the engine. Replace with counters inside
   `app/services/analyse.py` and `app/engines/*_backend.py`, so the exposure
   number is measured, not inferred. The dispatchers are 20 lines each so the
   current accounting is sound, but a reviewer should not have to take that on trust.
3. **Real policy set.** The 192-rule sweep pads the real six-rule policy with
   inert rules. Get the actual multi-authority policy set (ownership, certificate
   status, data-use class, jurisdiction, and whatever the Gujarat MoU adds) and
   report its real cardinality.
4. **Memory measurement.** E1.3 uses a `bytearray` standing in for weights.
   Measure real RSS with the facial model loaded and not loaded.
5. **Re-registration semantics.** What happens when a camera's provenance changes
   after registration — does the mask recompile, and what happens to in-flight
   sessions? Currently unspecified, and it is the obvious attack.
6. **Shared backbones.** If two engines share a feature extractor, is the
   forbidden engine really unbuilt? This is a real hole in the lazy-construction
   claim on a production stack.

## Baselines implemented

`query_time_rbac`, `stateless_fallback`, `naive_union_postfilter`
(`p1_provenance/baselines.py`). All three are in the results table.

**Baselines still owed to the reviewers named in the review:** an Ancile-style
per-operation policy interpreter, and an XEngine-style compiled-but-per-request
evaluator, so the paper separates "compiled" from "consumed at construction time".

## Reproducibility

Seeded from `prresearch/seeds.py`. E1.2-E1.4 are byte-identical across runs.
E1.1 measures wall-clock and varies a few percent; that is stated in the results.

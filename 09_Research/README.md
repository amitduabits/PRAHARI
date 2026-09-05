# PRAHARI Research Programme: reference implementations and experiments

**Read `STATUS.md` first.** The literature review in `../Research papers/ACTION_PLAN.md`
re-scoped the programme: **P1 and P4 are Tier A**; P3 and P6 are Tier B (need external
data); P2 and P5 are workshop/hold. This is not six novel-mechanism papers.

Runnable code for all six. Each paper has a reference implementation, at least two
baselines, an experiment script that writes a results JSON, and a figure. Synthetic
experiments run on CPU in about a minute, with fixed seeds.

Headline P1/P4 numbers in `P1_main.tex` / `P4_main.tex` come from
`results/real/` (production `analyse()` / `StreamSession`). The `instrument_p1.py`
and `instrument_p4.py` files here are sleep() mocks and must not be quoted.

## Layout

```
prresearch/
  seeds.py          one master seed, derived per experiment
  traces.py         synthetic camera estate and vehicle traces (3 topologies)
  metrics.py        top-k, percentiles, bootstrap CI, calibration error
  p1_provenance/    Paper 1  provenance-gated inference dispatch      CVPR
  p2_fallback/      Paper 2  deterministic fallback engines           ICCV
  p3_nextcam/       Paper 3  next-camera prediction, no road network  IJCAI
  p4_admission/     Paper 4  admission-controlled decoders            IEEE TMM
  p5_fusion/        Paper 5  cross-modal collapse and dedup           IEEE TCSVT
  p6_platform/      Paper 6  multi-authority platform design          IEEE TETC
tests/              34 tests, including the honest-failure cases
results/            experiment output, one JSON per paper
figures/            one PNG per paper
```

Every module names the production module it mirrors, so a reviewer can check the
paper describes the deployed system: `app/services/analyse.py` for P1,
`app/services/objects.py` and `anpr.py` for P2, `app/services/predict.py` for P3,
`app/services/sessions.py` and `health_probe.py` for P4, `app/services/matcher.py`
for P5, the package layout itself for P6.

## Real-data instrumentation (P1 + P4 prompt book)

Synthetic traces in `prresearch/traces.py` remain for the paper microbenchmarks.
The production-path harness lives in `02_Code/prahari/scripts/instrument.py` and writes `results/real/`.

```
cd 02_Code/prahari
.\.venv\Scripts\python.exe scripts\instrument.py all --seconds 8 --frames 12 --k-frames 8
```

Live catalogue: set `SENTINEL_HOST` in `.env`. Do not archive raw video.

## Run

```
make test           # 34 tests, ~1 s
make experiments    # all six papers plus figures, ~90 s
make p3             # one paper
```

Needs `numpy`, `matplotlib`, `pytest`. Nothing else, no GPU, no network.

## What each experiment produced

### P1  Provenance-gated dispatch
Compiling the permitted-engine set at registration into a bitmask makes dispatch
flat at ~670 ns median regardless of policy size, while query-time RBAC grows
linearly and reaches 24.8 us at 192 rules, a 37x gap. Over 20,000 frames on an
800-camera estate, stateless dispatch and naive union-then-filter each ran 24,445
forbidden inference calls, 17,377 of them facial; naive union returned zero
forbidden records, so its output is indistinguishable from the gated method while
the pixels still reached the model. That difference is the paper's whole point and
it is only visible in the call counts, not in the results. With no camera in the
estate permitted facial inference, the facial weights are never materialised under
the gated method: 16 MB of the 64 MB weight budget never enters memory.

### P2  Two-tier deterministic fallback
The two-tier pipeline never drops a frame (yield 1.0 at every injected failure
rate up to 0.5), where primary-only yield falls to 0.55. The classical secondary
is bit-for-bit deterministic across runs on all three pairs.

Honest result: the stratified provenance estimator does **not** beat a global
prior at estimating whole-batch accuracy, because the production and calibration
distributions match by construction (abs error 0.0005 to 0.0118 vs. 0.0013 to
0.0095 for the prior). Where it wins is the number an operator actually needs,
accuracy sliced by inference path: it recovers primary 0.6605 vs. secondary 0.4431
to within 0.002, which the prior cannot express at all. The paper should claim the
per-path estimate, not the batch estimate, and should show the prior baseline.

Retry is a strong baseline on accuracy-over-all-frames and sometimes beats
two-tier. It is only defensible where a repeated call is free and the failure is
transient; the fallback wins on bounded latency and on determinism, not on raw
accuracy. Say so in the paper rather than leaving it for a reviewer to find.

### P3  Next-camera prediction
Transition frequency reaches top-1 0.721 / top-3 0.925 on a grid, 0.738 / 0.910 on
irregular topology. The road-network oracle, given the true adjacency, gets 0.275
and 0.307 top-1: it knows which cameras are reachable but not which one is likely.
Constant velocity is the weakest everywhere (0.215 down to 0.050), confirming that
a motion model is the wrong prior for an irregular estate. The method needs about
200 trips to overtake pure geography and about 800 to saturate; the GIS fallback
carries 30 to 48 percent of queries at 50 trips and under 0.1 percent at 800.

### P4  Admission-controlled decoders
Refusal holds peak concurrency at exactly the bound (4) and p99 latency flat at
6.5 to 6.9 s across offered loads from 0.8 to 4.0. Queueing keeps every request but
its p99 rises from 496 s to 7,705 s over the same range, so the refusal policy is
buying a bounded tail with a known refusal rate. Peak envelope is identical at 800,
8,000 and 80,000 cameras: the bound is a property of the decoder budget, not the
estate. Rotational sweep coverage matches the analytic bound n/k * probe_time to
within 0.1 percent, and three-strike hysteresis produced zero false-offline marks
at a 1 percent transient failure rate.

Caveat to state in the paper: refusal rate is high (0.22 at offered load 0.8)
because arrivals are bursty. The policy trades a large refusal rate for a flat
tail. That is the right trade for alerting, and the wrong one for evidence
retrieval; the paper must scope the claim.

### P5  Cross-modal collapse
Entity-agnostic collapse cuts alerts 80.6 percent against one-alert-per-detection
while covering every incident, and beats per-modality dedup by a further 10.7 to
43.7 percent as the dual-tagged share rises from 0.15 to 1.0. Confidence voting
gets the biggest reduction (88.1 percent) by dropping 63 percent of incidents,
which is not a usable operating point.

Honest result that contradicts the strategy document: the 120 s window is **not**
"tuned to camera FOV depth divided by permitted speed". The geometric dwell time
is 1.3 to 9.6 s across the estate, median about 3 s. On the reduction/masking
curve, the knee sits at 15 to 30 s; 120 s already masks 384 distinct incidents in
12,000 (distinct-incident recall 0.968) for a 1.4 percent further reduction in
alerts. Either the paper derives the window from revisit statistics rather than
geometry, or it defends 120 s on other grounds and drops the geometric story.

### P6  Multi-authority platform
Onboarding 80,000 cameras through the deployed mix costs 126 hours; the same
estate through the web form costs 1,044 hours. Bulk CSV import is 2,238x cheaper
per camera than the form, but 12 percent of cameras still route through the form
and that tail is over 95 percent of the total cost, so the headline saving is 8x,
not 2,000x. Transport negotiation leaves 29.3 percent of the estate needing no
decoder at all (HLS and file), which is the input to the P4 bound: 56,592 of
80,000 cameras need a decoder, and at 4 concurrent decoders the sweep covers them
every 283 minutes, at 32 every 35 minutes.

## Reproducibility

`results/p2_fallback.json` through `results/p6_platform.json` are byte-identical
across runs and across processes. `results/p1_provenance.json` is not, and cannot
be: E1.1 measures wall-clock dispatch latency, so its nanosecond figures move a
few percent between runs. Its other three experiments are exact.

One trap worth recording: the deterministic secondary engine originally keyed off
Python's built-in `hash()`, which is salted per process, so two runs of the same
script disagreed while `make test` passed. Stable hashing (`zlib.crc32`) fixed it.
Anything that must reproduce across processes has to avoid `hash()` on strings.

## Known limits

- The traces are synthetic. Nothing here is validated against operational footage,
  and every accuracy figure is a property of the generator as much as the method.
  Replacing `traces.py` with a replay of the seeded registry is the next step and
  should happen before any of these numbers appear in a submission.
- P1's exposure accounting derives calls from each dispatcher's contract rather
  than instrumenting the engine, which is fine here because the dispatchers are 20
  lines each, but should be replaced by real instrumentation of `analyse.py`.
- P2's engines are behavioural models with a difficulty parameter, not the real
  YOLO/FaceNet/PaddleOCR stacks. The determinism result transfers; the accuracy
  numbers do not.
- P4 models decoder occupancy, not CPU or memory. The claim that peak resource is
  bounded needs a measured CPU envelope from the deployed stack to stand up.

# Six-paper programme — status

Single repository: https://github.com/amitduabits/PRAHARI  
Code: `09_Research/prresearch/` (synthetic, reviewer-reproducible)  
MEASURED production path: `02_Code/prahari/scripts/instrument.py` → `09_Research/results/real/`  
Literature and outlines: `Research papers/P*/`

Portfolio follows `Research papers/ACTION_PLAN.md`. **Not six novel-mechanism papers.**

| Paper | Tier | Claim that survives the literature | Code | Data | Draft | Blocker |
|---|---|---|---|---|---|---|
| **P1** Provenance / invocation | A | Invocation (not release) is a measurable harm | `prresearch/p1_provenance` + `analyse.py` gate | MEASURED 24 cameras × 6 frames on `own_feed.mp4` | `P1_main.tex` (numbers patched) | 24 h live RTSP; FaceNet optional |
| **P4** Decode admission / retrial | A | Same $K$ is a retrial orbit, not Erlang-B loss | `prresearch/p4_admission` + `StreamSession` | MEASURED $K=1,2,4$; extra-admit retries 3/3 | `P4_main.tex` (numbers patched) | $K>4$ GPU/NVDEC soak |
| **P3** Next-camera | B | Regime characterisation, not a new predictor | `prresearch/p3_nextcam` | Synthetic only | outline only | VeRi-776 / CityFlow |
| **P6** Platform / onboarding | B | Descriptor federation vs broker; quantitative crossover | `prresearch/p6_platform` | Synthetic 80k model | outline only | External NGSI-LD/ONVIF baseline |
| **P2** Fallback / estimator | C | Negative result: batch estimator loses to Average Confidence | `prresearch/p2_fallback` | Synthetic | workshop only | Per-stratum ATC baseline |
| **P5** Collapse window | C | Geometric 120 s derivation is wrong; knee is 15–30 s | `prresearch/p5_fusion` | Synthetic | hold | Replace derivation or fold into P6 |

## How to run

```
cd 09_Research
python -m pytest tests -q
python run_all.py          # six synthetic experiments + figures
```

Production MEASURED P1/P4:

```
cd 02_Code/prahari
python scripts/instrument.py all --seconds 8 --frames 6 --k-frames 6 --seed-n 24 --k 1 2 4
```

`instrument_p1.py` and `instrument_p4.py` in this folder are **sleep() mocks**. Do not put their output in an abstract.

## Headline MEASURED numbers (do not inflate)

**P1** (`results/real/p1_invocation_measurements.json`):
- CONFIG A: faces invoked 144/144, face-path CPU 10.223 s, p50 70.02 ms
- CONFIG B: faces invoked 6/144 (138 skipped), CPU 0.413 s, p50 9.26 ms
- Audit: 0 violations

**P4** (`results/real/p4_frontier.json`):
- $K=1,2,4$ p99 10.85 / 11.39 / 11.32 ms
- One extra admit per $K$: refused then retried successfully; abandoned 0
- $K\ge 8$: DESIGN TARGET

## What this folder will not do

- Create six GitHub remotes. Papers stay in this repository.
- Submit CCS/SIGMETRICS this week. Drafts exist; checklists that were pre-ticked “ready” are wrong until live data and losing baselines are in the tables.
- Quote 1,043 events, 50 live cameras, or optimal $K=8$ as MEASURED.

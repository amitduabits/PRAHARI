# P3 experiments

Code: `09_Research/prresearch/p3_nextcam/`. Run: `cd 09_Research && python3 run_all.py P3`.
Results: `09_Research/results/p3_nextcam.json`. Figure: `p3_topology_accuracy.png`.

## Claim-to-evidence table

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Transition frequency beats road-network and motion methods on irregular topology | E3.1: top-1 0.738 vs oracle-adjacency 0.307 vs constant-velocity 0.050 | **synthetic only — worth nothing as stated** |
| C2 | It needs little history | E3.2: overtakes geography at ~200 trips, saturates at ~800 | **synthetic only** |
| C3 | The GIS fallback carries the cold start | E3.3: 30-48% of queries at 50 trips, <0.1% at 800 | **synthetic only** |
| C4 | The 120 s collapse window does not damage transition counts | E3.4: top-1 unchanged to 120 s, degrades to 0.605 at 600 s | **synthetic only** |
| C5 | The regime boundary exists and we can locate it | — | **NOT RUN. This is the paper.** |
| C6 | We beat the learned sequence models | — | **NOT RUN** |

Every current number is a property of `prresearch/traces.py` as much as of the
method. The generator chooses the irregularity that the method handles. **Nothing
in the current results may appear in an abstract.**

## The data problem, and how to fix it

From `literature/REVIEW.md` section C, ranked:

1. **VeRi-776** — 776 vehicles, 20 real cameras, 1 km², 24 h, **real plate strings,
   timestamps, and inter-camera distances**. Closest public analogue to our data.
   Access: email the maintainer with name and affiliation; non-commercial research
   only, no redistribution. **This should be the headline dataset.**
2. **CityFlow / CityFlowV2** — 40 cameras, 10 intersections, 666 cross-camera
   identities, **camera GPS via ground-plane homographies**, 2.5 km separation.
   Access: AI City Challenge request form plus a signed licence. Caveat: a regular
   intersection grid, the *opposite* of the irregular estates we claim to serve.
   Use it and say explicitly that it is a hard case for our thesis.
3. **NLPR_MCT** — 3-5 non-overlapping cameras per sub-dataset, ships the MCTA
   metric. Sanity check only, too small for a topology claim.
4. **DukeMTMC / DukeMTMC-reID** — **do not use.** Withdrawn by Duke in June 2019
   after reporting that it was used for surveillance of Uyghurs. Using a dataset
   withdrawn *for surveillance misuse* in a police-surveillance paper with a misuse
   section would be self-inflicted. Cite `ristani2016performance` for IDF1 only and
   state that we declined the data.
5. **WILDTRACK** — overlapping fields of view make the transition task degenerate. Skip.
6. **mapconstruction.org** (`ahmed2015comparison`) — open GPS traces, ground-truth
   maps and seven implemented map-construction algorithms, so the road-network
   baseline is real rather than a strawman.

Both VeRi-776 and CityFlow are obtainable within days by email or form. **There is
no defensible reason to submit on synthetic data.**

## Baselines required — all six tiers

1. Uniform random (floor).
2. **Global popularity prior** — rank by marginal detection frequency, ignoring the
   last-seen camera. *This is the baseline that most often kills transition-model
   papers. If we do not clearly beat it, there is no paper.* Not yet implemented.
3. Distance-only — implemented (`DistanceOnly`).
4. First and second-order Markov with smoothing (Laplace / Kneser-Ney). Raw counts
   on sparse data are a known failure mode; `MarkovBackoff` is implemented,
   Kneser-Ney is not.
5. Learned sequence models — ST-RNN, DeepMove, **Flashback**. At IJCAI, omitting
   Flashback is not survivable: it targets sparse traces and it is our venue.
6. Road-network methods — HMM map matching on OSM, a constant-velocity predictor
   (implemented), and a map-inference-then-match pipeline from Ahmed et al.

## Metrics and protocol required

- Hit@1/3/5, **MRR**, mean and median rank, full CMC curve.
- **Macro-average over cameras**, not only micro-average over events. A
  micro-average is dominated by hub cameras and flatters the method.
- NLL or perplexity of the true next camera — tests calibration, not just ranking.
- Normalised predictability against the entropy bound, using the **next-location**
  framing (`ikanovic2017alternative`, ~71%) not next-bin (`song2010limits`, 93%),
  and acknowledging `kulkarni2019examining`.
- **Cold-start rate** and accuracy conditioned on fallback vs non-fallback.
- **Temporal split, never random.** A random split leaks the transition table into
  the test set and is the most common fatal flaw in this genre.
- Coverage sweep: subsample to 20/40/60/80/100% and plot accuracy vs coverage.
  `qi2021alprtraj` found a ~50% cliff — either we have one or that is a finding.
- Stratify by camera history depth (<10, 10-100, >100 outgoing observations).
- **Stratify by deployment regularity, with a stated quantitative measure of it.**
  This is the paper's actual claim and needs at least two estates that differ.
- Bootstrap CIs and a paired test against the strongest baseline.
- Runtime and memory, since "simple beats complex" is half the argument.

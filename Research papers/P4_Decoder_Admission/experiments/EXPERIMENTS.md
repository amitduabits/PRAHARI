# P4 experiments

Code: `09_Research/prresearch/p4_admission/`. Run: `cd 09_Research && python3 run_all.py P4`.
Results: `09_Research/results/p4_admission.json`. Figure: `p4_latency_cliff.png`.

## Claim-to-evidence table

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Peak concurrency is exactly K | E4.1, E4.2: 4 at every load and every estate size | **definitional, not a finding.** State as an invariant with a proof |
| C2 | p99 latency is flat across load | E4.1: 6.5-6.9 s from load 0.8 to 4.0, vs queueing 496 → 7,705 s | **definitional for a loss system.** Keep the contrast, drop the framing |
| C3 | Envelope is independent of estate size | E4.2: identical at 800 / 8k / 80k | **definitional** |
| C4 | Sweep coverage matches ⌈n/K⌉·T | E4.3: within 0.1% at all three scales | supported; also near-definitional |
| C5 | Three-strike hysteresis avoids false offline marks | E4.3: 0 false-offline at 1% i.i.d. probe loss | **supported for i.i.d. loss only.** Real losses are correlated |
| C6 | The K-allocation frontier between decode and probe is non-trivial | — | **NOT RUN. This is the paper.** |
| C7 | The envelope holds for CPU/memory/NVDEC, not just the counter | — | **NOT RUN** |
| C8 | Refusals are not retried, so this is a loss system not a retrial queue | — | **NOT RUN, and it may be false** |

## The propositions to state and prove

From `literature/REVIEW.md` section C:

- **P1 (envelope invariant).** Live sessions ≤ K at every instant. Semaphore
  argument; state the atomicity assumption and multi-node behaviour. Frame as an
  invariant, not a result.
- **P2 (refusal probability, insensitive form).** B(K,a) = (a^K/K!)/Σ a^i/i! for
  *arbitrary* session-duration distribution with finite mean (`erlang1917`,
  `sevastyanov1957`). Give the recursion and use it as a **K-sizing rule**: the
  minimum K meeting a refusal SLO. This turns K from a magic constant into a
  derived quantity, which is the difference between a system paper and a config note.
- **P3 (coverage interval).** Every camera probed within C = ⌈n/K⌉·T; staleness < C.
  State the assumptions: bounded probe timeout, no starvation, sweep-pointer
  persistence across restarts. On a degraded estate T is the timeout, not the RTT.
- **P4 (detection latency and false alarms).** Offline no later than t+3C, no
  earlier than t+2T. Under i.i.d. loss p, false-marking is p³ per triple, giving
  MTBF C/p³. **Derive 3 from a target MTBF and a measured p.** If losses are
  correlated — and a switch flap takes 40 cameras at once — p³ is a lower bound.
- **Corollary (the contribution).** K_decode and K_probe draw from one budget.
  **Plot that frontier. That figure is the paper.**

## What is missing — the 24 measurements

Grouped from `literature/REVIEW.md` section D. Without the first group the central
claim reduces to "our semaphore works", because `bossen2012hevc` shows decode cost
varies by an order of magnitude across resolution, codec, bit depth and GOP.

**Per-session cost (blocking):** CPU distribution by resolution/codec/fps with its
coefficient of variation; resident and peak memory including the frame-buffer pool;
NVDEC/VAAPI engine occupancy and the vendor concurrent-session caps; memory and
PCIe bandwidth; fd/socket/thread counts.

**Envelope validation:** measured peak of each resource at K vs the linear
extrapolation K·mean — it will be superlinear via cache and bandwidth contention,
and that non-linearity must be reported honestly; worst-case mix (all K at 4K HEVC).

**Latency methodology:** say which latency (session establishment, first frame, or
steady-state frame-to-inference); **open-loop** generator, because a closed-loop one
cannot produce the tail divergence we claim to avoid and a reviewer will check;
full CDFs and p99.9, not p99 points; **refusal rate reported at every load point
alongside latency** — a flat p99 obtained by refusing 60% of requests is arithmetic,
and omitting this is the most likely cause of rejection.

**Scale:** whether 80k used real cameras, emulated RTSP, or a synthetic trace;
the observed arrival process (police estates are diurnal and incident-driven, which
breaks the Poisson assumption behind Erlang-B); the empirical session-duration
distribution, which is what justifies invoking insensitivity.

**Sweep and health:** measured coverage vs ⌈n/K⌉·T including the probe-completion
tail; measured probe-loss p and its **correlation structure**; detection latency and
false-positive rate for three-strike against `hayashibara2004phi`; and deliberately,
the interference case — does an estate-wide network incident starve decode
admission by filling the pool with timing-out probes? That is the most interesting
failure mode in the system.

**Baselines to implement:** bounded queue with timeout (SEDA), LRU eviction,
quality-reduction admission (the brownout arm), and a DAGOR-style dynamic
controller. All four on the same axes: p99, refusal/eviction/degradation rate, peak
envelope. Without these it is a single-system description.

**Correctness:** cost of the admission check under contention and the
synchronisation design across ingest nodes; behaviour on ingest-node failure — does
K become 2K under split brain?

## Unverified references

Falin (1990, *Queueing Systems*) and Artalejo & Gómez-Corral's monograph are the
standard entry points for retrial queues (needed for C8). **Neither has been
verified; verify before citing.**

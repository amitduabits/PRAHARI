# P4 outline — ~11 pages (IEEE TMM)

| § | Section | Words | Must establish |
|---|---|---|---|
| 1 | Introduction | 800 | The allocation problem, not the admission policy. State in the first column that refusal semantics are the Erlang loss system and that this is background. |
| 2 | Background: the loss system | 700 | Erlang-B, Sevastyanov insensitivity, why insensitivity matters for real decoder-session distributions. Concede everything here so nothing is left to concede later. |
| 3 | System model | 900 | Registry, ingest, one bound K, the sweep. State the assumptions the propositions need. |
| 4 | Analysis | 1400 | Propositions 1-4 with proofs, then the corollary that gives the frontier. The K-sizing rule from B(K,a). |
| 5 | Is it a loss system? | 600 | The retrial-queue objection, head on. Either prove refusals are never retried or model the orbit and report occupancy. **Do not omit this section.** |
| 6 | Implementation | 700 | The deployed ingest layer; the semaphore; multi-node synchronisation; split-brain behaviour. |
| 7 | Measurement setup | 700 | Open-loop generator; what "latency" means here; real vs emulated cameras; the observed arrival process and session-duration distribution. |
| 8 | Results | 2200 | Per-session cost distributions; envelope at K vs linear extrapolation with the non-linearity; the four baselines on p99 / refusal / envelope; the sweep coverage and its tail; three-strike vs φ-accrual; **the K-allocation frontier.** |
| 9 | The interference case | 500 | Estate-wide incident: timing-out probes starving decode admission. |
| 10 | Related work | 800 | Erlang, SWIM, Clockwork, DAGOR, VideoStorm. Concede each. |
| 11 | Limitations | 500 | Single-resource model; no priority classes; the perishability assumption asserted rather than demonstrated. |
| 12 | Conclusion | 200 | |

**Figures.** F1 the two-job budget. **F2 the K-allocation frontier — refusal
probability against coverage interval, the paper's central figure.** F3 measured
envelope vs K·mean, showing the superlinearity. F4 p99 and refusal rate on one
plot, four policies. F5 three-strike detection latency vs φ-accrual.

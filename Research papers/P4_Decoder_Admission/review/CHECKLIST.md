# P4 submission checklist (IEEE TMM / ACM TOMM)

- [ ] Erlang-B and Sevastyanov cited in the introduction, not buried
- [ ] Envelope invariant presented as a proposition, not an experimental finding
- [ ] The retrial-queue objection has its own section
- [ ] Per-session CPU, memory, bandwidth and NVDEC measurements present
- [ ] Measured envelope at K vs K·mean, with the superlinearity reported
- [ ] Open-loop load generator, stated
- [ ] Refusal rate reported at every load point, on the same axes as latency
- [ ] Full latency CDFs including p99.9
- [ ] All four baselines implemented: bounded queue, LRU eviction, brownout, DAGOR-style
- [ ] Three-strike constant derived from a target MTBF, not asserted
- [ ] φ-accrual benchmarked
- [ ] Probe-loss correlation structure measured
- [ ] The interference case (probes starving decode) measured deliberately
- [ ] Empirical arrival process and session-duration distribution reported
- [ ] 80k experiment: real, emulated or synthetic, stated plainly
- [ ] Falin / Artalejo retrial-queue references verified before citing

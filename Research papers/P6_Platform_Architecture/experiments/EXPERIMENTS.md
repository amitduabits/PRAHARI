# P6 experiments

Code: `09_Research/prresearch/p6_platform/`. Run: `cd 09_Research && python3 run_all.py P6`.
Results: `09_Research/results/p6_platform.json`. Figure: `p6_coverage_interval.png`.

## Claim-to-evidence table

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Bulk import dominates form entry per camera | E6.1: 0.021 s vs 47 s, a factor of 2,238 | **supported** (measured constants, single system) |
| C2 | Bulk import cuts total onboarding cost | E6.1: 126 h vs 1,044 h at 80k — but only 8x, because 12% of cameras still use the form and that tail is >95% of the cost | **supported, and the honest number is 8x, not 2,238x** |
| C3 | Transport negotiation leaves a large decoder-free fraction | E6.2: 29.3% on HLS or file; 56,592 of 80,000 need a decoder | **supported** (modelled mix) |
| C4 | Audit growth dominates registry size within a year | E6.3: 58.9 GB vs 33 MB at 80k and 120 entries/camera/day | **supported** (analytic) |
| C5 | Coverage interval scales as n/K·probe_time | E6.4: 283 min at K=4, 35 min at K=32, for 80k | **supported**, and near-definitional |
| C6 | Descriptor federation beats broker federation below X cameras/authority | — | **NOT RUN. This is the paper.** |
| C7 | The measured transport-failure distribution | — | **NOT RUN, and it is the most publishable thing here** |

C2 is the honest version of a claim that would otherwise have been overstated by
two orders of magnitude. Keep it in that form.

## What is missing, in priority order

1. **An external baseline (C6).** Three-way CSV/REST/form is an A/B of our own UI
   and reviewers will say so. Needed: measured per-camera integration effort for at
   least one of NGSI-LD context source registration (`cirillo2019fiware`), ONVIF
   WS-Discovery auto-onboard, or a VMS-federation path with published per-site
   effort. Without this the cost numbers are self-referential.
2. **The transport-failure distribution (C7).** Across the real estate: the
   fraction of cameras advertising ONVIF conformance that failed RTSP negotiation;
   the tail reachable only by file drop; rows that never resolved to a live device;
   time-to-first-frame by transport. **Nobody has published this at this scale and
   it is worth more than the architecture description.** Publish the failures.
3. **The scale knee.** "80,000" is decoration unless we show what fails at 8,000
   and what change made 80,000 possible. Sweep registry size against sweep coverage
   interval and against audit growth under a retention policy, and report the knee.
4. **Invariants and their violation.** State the three invariants (registry row is
   the unit of ownership; ingest is transport-agnostic and negotiated per row;
   event-bus subscribers are scoped by contributing authority) and measure what
   breaks when each is dropped. This is what makes the design outlive the deployment.
5. **Real onboarding constants.** ONBOARD_S values are measured on our stack but
   from a small sample. Report the distribution, not the mean, and the sample size.
6. **Retention policy derived from the measurement.** The audit-growth number
   should produce a retention recommendation, which then feeds the ethics section.

## Baselines implemented

Only the internal three (CSV bulk, REST, web form) and an all-web-form
counterfactual. **No external baseline.** That is the gap that decides publishability.

## A note on the transport mix

E6.2's mix is modelled from the deployment's authority shares, not measured
end-to-end. The share numbers are plausible; the *failure* numbers, which are the
interesting ones, do not exist yet. Do not report the mix as measured.
